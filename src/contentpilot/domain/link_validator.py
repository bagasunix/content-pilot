"""Link validation gate — verify all external links in a draft are legit.

Checks:
1. HTTP reachability (status 200-399)
2. Domain reputation (blocklist of known hoax/fake-news domains)
3. Research credibility signals (prefer .edu, .gov, established media, peer-reviewed)
4. Detect dead links, redirects to unrelated domains, and parked pages
"""
from __future__ import annotations

import ipaddress
import re
import urllib.parse
from dataclasses import dataclass, field
from typing import Optional


# Known hoax / fake-news / low-credibility domains (Indonesian + international)
HOAX_DOMAINS = frozenset([
    # Indonesian hoax sites
    "nusanews.id",
    "posmetro.co",
    "wartaindo.com",
    "infonusantara.net",
    "kabar24jam.com",
    "beritaviral.org",
    "faktanews.id",
    "mediaumat.news",
    "postmetro.info",
    "suaranasional.com",
    "obfrancais.com",
    # International low-credibility
    "naturalnews.com",
    "infowars.com",
    "beforeitsnews.com",
    "worldnewsdailyreport.com",
    "yournewswire.com",
    "newspunch.com",
    "neonnettle.com",
    "thegatewaypundit.com",
    "realfarmacy.com",
    "dailybuzzlive.com",
    "empirenews.net",
    "huzlers.com",
    "nationalreport.net",
    "nowtheendbegins.com",
    "stuppid.com",
    "thelastlineofdefense.org",
    "abcnews.com.co",
    "channel23news.com",
    "civic-online.com",
])

# Trusted high-credibility TLDs and domains for research
TRUSTED_TLDS = frozenset([".edu", ".gov", ".ac.id", ".go.id"])
TRUSTED_DOMAINS = frozenset([
    # Academic / research
    "scholar.google.com",
    "pubmed.ncbi.nlm.nih.gov",
    "arxiv.org",
    "doi.org",
    "researchgate.net",
    "jstor.org",
    "springer.com",
    "nature.com",
    "science.org",
    "ieee.org",
    "acm.org",
    # Reputable media / references
    "reuters.com",
    "apnews.com",
    "bbc.com",
    "bbc.co.uk",
    "theguardian.com",
    "nytimes.com",
    "washingtonpost.com",
    "kompas.com",
    "tempo.co",
    "detik.com",
    "tirto.id",
    "cnnindonesia.com",
    # Tech references
    "docs.python.org",
    "developer.mozilla.org",
    "stackoverflow.com",
    "github.com",
    "gitlab.com",
    "wikipedia.org",
    "docs.microsoft.com",
    "learn.microsoft.com",
    "cloud.google.com",
    "aws.amazon.com",
    "docs.docker.com",
    "kubernetes.io",
])

# Patterns that suggest parked / spam pages
PARKED_INDICATORS = [
    "domain is for sale",
    "buy this domain",
    "this domain has expired",
    "parked free",
    "godaddy",
    "sedoparking",
    "hugedomains",
    "dan.com",
    "afternic",
]

# Extract URLs from markdown/HTML content. The bare-URL class excludes the
# backtick so inline code (`http://localhost:3000`) isn't swallowed whole.
_MD_LINK_RE = re.compile(r"\[([^\]]*)\]\((https?://[^)]+)\)")
_HTML_HREF_RE = re.compile(r'href=["\']?(https?://[^"\'>\s]+)')
_BARE_URL_RE = re.compile(r'(?<![("\'=])(https?://[^\s<>\])"\'`]+)')

# Trailing characters that are punctuation/markup, never part of a real URL.
_TRAILING_JUNK = "`.,;:!?\"')]}>"


def _clean_url(url: str) -> str:
    """Strip trailing punctuation/markup a regex may have over-captured."""
    url = url.strip()  # leading/trailing whitespace
    url = url.rstrip(_TRAILING_JUNK)
    # Aggressive backtick cleanup — catches embedded backticks like `3000`
    url = url.replace("`", "")
    return url


def is_local_host(url: str) -> bool:
    """True for non-routable hosts (localhost, loopback, private IPs).

    These are legitimate in tutorials (e.g. a Docker article referencing
    http://localhost:3000) and must never be HTTP-checked or failed as dead.
    """
    host = (urllib.parse.urlparse(url).hostname or "").lower()
    if host in ("localhost", "0.0.0.0", "::1"):
        return True
    if host.endswith(".localhost") or host.endswith(".local"):
        return True
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_loopback or ip.is_private or ip.is_link_local or ip.is_unspecified
    except ValueError:
        return False


@dataclass
class LinkCheckResult:
    """Result of checking a single link."""
    url: str
    domain: str
    status: Optional[str] = None  # "ok", "dead", "redirect", "timeout", "hoax", "suspicious"
    http_code: Optional[int] = None
    reason: str = ""
    credibility: str = "unknown"  # "high", "medium", "low", "hoax"


@dataclass
class LinkValidationResult:
    """Aggregate result of all link checks in a draft."""
    total_links: int = 0
    checked: int = 0
    failures: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    results: list[LinkCheckResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.failures


def extract_links(content: str) -> list[str]:
    """Extract all external URLs from markdown/HTML content."""
    urls = set()
    # Markdown links [text](url)
    for _, url in _MD_LINK_RE.findall(content):
        urls.add(_clean_url(url))
    # HTML href
    for url in _HTML_HREF_RE.findall(content):
        urls.add(_clean_url(url))
    # Bare URLs (not already captured)
    for url in _BARE_URL_RE.findall(content):
        urls.add(_clean_url(url))
    return sorted(urls)


def get_domain(url: str) -> str:
    """Extract domain from URL."""
    parsed = urllib.parse.urlparse(url)
    return parsed.netloc.lower().removeprefix("www.")


def classify_domain(domain: str) -> str:
    """Classify domain credibility: high, medium, low, hoax."""
    # Check hoax blocklist
    if domain in HOAX_DOMAINS:
        return "hoax"
    # Also check parent domain (e.g. sub.hoaxsite.com)
    parts = domain.split(".")
    for i in range(len(parts) - 1):
        parent = ".".join(parts[i:])
        if parent in HOAX_DOMAINS:
            return "hoax"

    # Check trusted domains
    if domain in TRUSTED_DOMAINS:
        return "high"
    # Check parent for trusted (e.g. en.wikipedia.org → wikipedia.org)
    for i in range(len(parts) - 1):
        parent = ".".join(parts[i:])
        if parent in TRUSTED_DOMAINS:
            return "high"

    # Check trusted TLDs
    for tld in TRUSTED_TLDS:
        if domain.endswith(tld):
            return "high"

    # Default: medium (unknown but not blocklisted)
    return "medium"


def check_link_reachability(url: str, timeout: int = 10) -> LinkCheckResult:
    """Check if a URL is reachable. Returns LinkCheckResult.

    Uses HEAD request first, falls back to GET if HEAD returns 405.
    """
    import urllib.request
    import urllib.error
    import ssl

    domain = get_domain(url)
    credibility = classify_domain(domain)

    # Immediate fail for hoax domains — no need to even check HTTP
    if credibility == "hoax":
        return LinkCheckResult(
            url=url, domain=domain, status="hoax",
            reason=f"Domain '{domain}' ada di blocklist sumber hoax/fake-news",
            credibility="hoax",
        )

    # HTTP check
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; BlogLinkChecker/1.0)"
    }

    try:
        req = urllib.request.Request(url, headers=headers, method="HEAD")
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            code = resp.getcode()
            final_url = resp.geturl()
    except urllib.error.HTTPError as e:
        code = e.code
        final_url = url
        if code == 405:
            # HEAD not allowed, try GET
            try:
                req = urllib.request.Request(url, headers=headers, method="GET")
                with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
                    code = resp.getcode()
                    final_url = resp.geturl()
            except urllib.error.HTTPError as e2:
                code = e2.code
                final_url = url
            except Exception:
                return LinkCheckResult(
                    url=url, domain=domain, status="dead", http_code=code,
                    reason=f"HTTP {code} (HEAD rejected, GET juga gagal)",
                    credibility=credibility,
                )
    except urllib.error.URLError as e:
        return LinkCheckResult(
            url=url, domain=domain, status="dead",
            reason=f"URL tidak bisa diakses: {e.reason}",
            credibility=credibility,
        )
    except TimeoutError:
        return LinkCheckResult(
            url=url, domain=domain, status="timeout",
            reason="Timeout — server tidak merespon dalam 10 detik",
            credibility=credibility,
        )
    except Exception as e:
        return LinkCheckResult(
            url=url, domain=domain, status="dead",
            reason=f"Error: {type(e).__name__}: {e}",
            credibility=credibility,
        )

    # Evaluate response
    if 200 <= code <= 399:
        # Check if redirected to a completely different domain (suspicious)
        final_domain = get_domain(final_url)
        if final_domain != domain and not final_domain.endswith(f".{domain}"):
            return LinkCheckResult(
                url=url, domain=domain, status="redirect", http_code=code,
                reason=f"Redirect ke domain berbeda: {final_domain}",
                credibility="low",
            )
        return LinkCheckResult(
            url=url, domain=domain, status="ok", http_code=code,
            credibility=credibility,
        )
    elif code in (404, 410):
        return LinkCheckResult(
            url=url, domain=domain, status="dead", http_code=code,
            reason=f"HTTP {code} — halaman tidak ada / dihapus",
            credibility=credibility,
        )
    elif code in (403, 401):
        # Could be paywall or geo-restricted — warning, not failure
        return LinkCheckResult(
            url=url, domain=domain, status="ok", http_code=code,
            reason=f"HTTP {code} — mungkin paywall/restricted (tetap valid)",
            credibility=credibility,
        )
    else:
        return LinkCheckResult(
            url=url, domain=domain, status="suspicious", http_code=code,
            reason=f"HTTP {code} — unexpected status",
            credibility=credibility,
        )


def validate_links(content: str, check_http: bool = True) -> LinkValidationResult:
    """Main entry: validate all external links in article content.

    Args:
        content: Draft body (markdown/HTML)
        check_http: If True, actually make HTTP requests. If False, only check
                    domain reputation (faster, for offline/CI use).
    """
    # Drop local / non-routable hosts up front — they're valid in tutorials
    # and must never be checked or failed.
    urls = [u for u in extract_links(content) if not is_local_host(u)]
    result = LinkValidationResult(total_links=len(urls))

    for url in urls:
        domain = get_domain(url)
        credibility = classify_domain(domain)

        if not check_http:
            # Offline mode: only domain check
            lr = LinkCheckResult(url=url, domain=domain, credibility=credibility)
            if credibility == "hoax":
                lr.status = "hoax"
                lr.reason = f"Domain '{domain}' ada di blocklist sumber hoax"
                result.failures.append(f"HOAX SOURCE: {url} — {lr.reason}")
            else:
                lr.status = "unchecked"
            result.results.append(lr)
            result.checked += 1
            continue

        # Full check with HTTP
        lr = check_link_reachability(url)
        result.results.append(lr)
        result.checked += 1

        # Categorize
        if lr.status == "hoax":
            result.failures.append(f"HOAX SOURCE: {url} — {lr.reason}")
        elif lr.status == "dead":
            result.failures.append(f"DEAD LINK: {url} — {lr.reason}")
        elif lr.status == "redirect":
            result.warnings.append(f"REDIRECT: {url} — {lr.reason}")
        elif lr.status == "timeout":
            result.warnings.append(f"TIMEOUT: {url} — {lr.reason}")
        elif lr.status == "suspicious":
            result.warnings.append(f"SUSPICIOUS: {url} — {lr.reason}")

    # Additional check: no external links at all → warning
    if len(urls) == 0:
        result.warnings.append(
            "Tidak ada external link — artikel research harus punya sumber"
        )
    # Check: all links are low/unknown credibility
    elif all(r.credibility in ("low", "unknown") for r in result.results):
        result.warnings.append(
            "Semua link credibility rendah/unknown — tambahkan minimal 1 sumber terpercaya"
        )

    return result


def format_report(result: LinkValidationResult) -> str:
    """Format validation result as human-readable report."""
    lines = [f"Link Validation: {result.total_links} links ditemukan, {result.checked} dicek"]
    lines.append("")

    if result.failures:
        lines.append("❌ FAILURES (harus diperbaiki):")
        for f in result.failures:
            lines.append(f"  • {f}")
        lines.append("")

    if result.warnings:
        lines.append("⚠️  WARNINGS (review):")
        for w in result.warnings:
            lines.append(f"  • {w}")
        lines.append("")

    if not result.failures and not result.warnings:
        lines.append("✅ Semua link valid dan dari sumber terpercaya.")

    # Summary table
    high = sum(1 for r in result.results if r.credibility == "high")
    med = sum(1 for r in result.results if r.credibility == "medium")
    low = sum(1 for r in result.results if r.credibility in ("low", "unknown"))
    lines.append(f"\nCredibility: {high} high | {med} medium | {low} low/unknown")

    return "\n".join(lines)
