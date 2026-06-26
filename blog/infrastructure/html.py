"""Minimal markdown → HTML converter (stdlib only).

Just enough to render the constructs the drafts actually use — headings,
paragraphs, lists, blockquotes, fenced/inline code, bold, links, images — into
the HTML body Blogger's API expects. Not a spec-complete markdown engine; it
covers what the pipeline produces and escapes everything else safely.
"""
from __future__ import annotations

import html as _html
import re

_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
_IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
_CODE_RE = re.compile(r"`([^`]+)`")
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
_TABLE_ROW_RE = re.compile(r"^\|(.+)\|$")
_TABLE_SEP_RE = re.compile(r"^\|[-| :]+\|$")


def _inline(text: str) -> str:
    """Escape, then apply inline markdown. Inline code is escaped but verbatim."""
    # Pull inline code out first so its contents aren't treated as markup.
    spans: list[str] = []

    def _stash(m: re.Match) -> str:
        spans.append(f"<code>{_html.escape(m.group(1))}</code>")
        return f"\x00{len(spans) - 1}\x00"

    text = _CODE_RE.sub(_stash, text)
    text = _html.escape(text)
    text = _IMG_RE.sub(
        lambda m: f'<img src="{m.group(2)}" alt="{m.group(1)}" loading="lazy"/>', text
    )
    text = _LINK_RE.sub(lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', text)
    text = _BOLD_RE.sub(lambda m: f"<strong>{m.group(1)}</strong>", text)
    # restore code spans
    text = re.sub(r"\x00(\d+)\x00", lambda m: spans[int(m.group(1))], text)
    return text


def markdown_to_html(md: str) -> str:
    md = _COMMENT_RE.sub("", md)  # drop HTML comments (e.g. imagery placeholders)
    lines = md.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    i = 0
    n = len(lines)

    def close_list(tag: str | None) -> None:
        if tag:
            out.append(f"</{tag}>")

    list_tag: str | None = None

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # Fenced code block
        if stripped.startswith("```"):
            close_list(list_tag); list_tag = None
            lang = stripped[3:].strip()
            buf: list[str] = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1  # skip closing fence
            cls = f' class="language-{lang}"' if lang else ""
            out.append(f"<pre><code{cls}>" + _html.escape("\n".join(buf)) + "</code></pre>")
            continue

        # Blank line
        if not stripped:
            close_list(list_tag); list_tag = None
            i += 1
            continue

        # Heading
        m = _HEADING_RE.match(stripped)
        if m:
            close_list(list_tag); list_tag = None
            level = len(m.group(1))
            out.append(f"<h{level}>{_inline(m.group(2).strip())}</h{level}>")
            i += 1
            continue

        # Horizontal rule
        if stripped in ("---", "***", "___"):
            close_list(list_tag); list_tag = None
            out.append("<hr/>")
            i += 1
            continue

        # Table (markdown pipe table)
        if _TABLE_ROW_RE.match(stripped) and i + 1 < n and _TABLE_SEP_RE.match(lines[i + 1].strip()):
            close_list(list_tag); list_tag = None
            # Parse header row
            header_cells = [c.strip() for c in stripped.strip("|").split("|")]
            i += 2  # skip header + separator
            # Parse data rows
            rows = []
            while i < n and _TABLE_ROW_RE.match(lines[i].strip()):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                rows.append(cells)
                i += 1
            # Build HTML table
            out.append('<table border="1" cellpadding="5" cellspacing="0">')
            out.append("<thead><tr>")
            for cell in header_cells:
                out.append(f"<th>{_inline(cell)}</th>")
            out.append("</tr></thead>")
            out.append("<tbody>")
            for row in rows:
                out.append("<tr>")
                for cell in row:
                    out.append(f"<td>{_inline(cell)}</td>")
                out.append("</tr>")
            out.append("</tbody></table>")
            continue

        # Unordered list item
        if re.match(r"^[-*+]\s+", stripped):
            if list_tag != "ul":
                close_list(list_tag); out.append("<ul>"); list_tag = "ul"
            item = re.sub(r"^[-*+]\s+", "", stripped)
            out.append(f"<li>{_inline(item)}</li>")
            i += 1
            continue

        # Ordered list item
        if re.match(r"^\d+\.\s+", stripped):
            if list_tag != "ol":
                close_list(list_tag); out.append("<ol>"); list_tag = "ol"
            item = re.sub(r"^\d+\.\s+", "", stripped)
            out.append(f"<li>{_inline(item)}</li>")
            i += 1
            continue

        # Blockquote
        if stripped.startswith(">"):
            close_list(list_tag); list_tag = None
            out.append(f"<blockquote>{_inline(stripped.lstrip('> ').strip())}</blockquote>")
            i += 1
            continue

        # Paragraph
        close_list(list_tag); list_tag = None
        out.append(f"<p>{_inline(stripped)}</p>")
        i += 1

    close_list(list_tag)
    return "\n".join(out)
