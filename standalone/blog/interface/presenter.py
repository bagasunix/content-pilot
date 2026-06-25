"""Presenter — turns application result objects into human-facing text.

All Indonesian CLI output lives here, so the core stays free of formatting.
Each renderer returns a list of lines; gate also returns an exit code.
"""
from __future__ import annotations

from ..application.results import (
    GateOutcome,
    NextResult,
    StageActionResult,
    StatusResult,
)

TOKEN_PATH = "~/Project/blog-lifecycle/workspace/token.json"


def render_status(r: StatusResult) -> list[str]:
    if not r.rows:
        return ["Pipeline kosong. Belum ada artikel."]
    lines = [f"{'IDEA_ID':<42} {'STAGE':<12} {'UPDATED'}", "-" * 78]
    for row in r.rows:
        flag = " *WIP" if row.is_wip else ""
        lines.append(f"{row.idea_id:<42} {row.stage:<12} {row.updated[:19]}{flag}")
    lines.append("-" * 78)
    lines.append(f"WIP in flight: {r.wip_count}/{r.wip_limit}")
    return lines


def render_next(r: NextResult) -> list[str]:
    if r.status == "wip_full":
        return [f"⛔ WIP penuh ({r.wip_count}/{r.wip_limit}). Selesaikan/approve dulu: "
                f"{', '.join(r.in_flight)}"]
    if r.status == "empty":
        return ["Idea-bank kosong (atau cuma contoh). Tambahkan topik dulu di "
                "~/Project/blog-lifecycle/workspace/idea-bank.md"]
    if r.status == "exhausted":
        return ["✅ Semua ide di idea-bank sudah masuk pipeline. Tambahkan topik baru."]
    idea = r.idea
    lines = []
    if r.angle_missing:
        lines.append(f"⚠️  '{idea.idea_id}' belum punya angle/pengalaman (§14). "
                     f"Isi dulu sebelum diproduksi.")
    lines += [
        f"➡️  NEXT: {idea.title}",
        f"    idea_id : {idea.idea_id}",
        f"    priority: {idea.priority}   kategori: {idea.category}",
        f"    keyword : {idea.keyword}",
        f"    angle   : {idea.angle or '(kosong — isi dulu)'}",
        "",
        f"    Jalankan: python3 pipeline.py start {idea.idea_id}",
    ]
    return lines


def render_research(r: StageActionResult) -> list[str]:
    if r.status == "idea_not_found":
        return [f"❌ idea_id '{r.idea_id}' tidak ada di idea-bank. Cek `pipeline.py next`."]
    if r.status == "exists":
        return [f"⚠️  '{r.idea_id}' sudah di stage '{r.from_stage}'. Tidak perlu research ulang."]
    if r.status == "wip_full":
        return [f"⛔ WIP penuh ({r.wip_count}/{r.wip_limit}). Tidak mulai topik baru."]
    return [
        f"✅ Research brief created: {r.path}",
        f"   idea_id: {r.idea_id}",
        f"   Next: agent isi brief via blog-topic-research, lalu 'draft {r.idea_id}'",
    ]


def render_draft(r: StageActionResult) -> list[str]:
    if r.status == "not_found":
        return [f"❌ '{r.idea_id}' tidak ditemukan. Jalankan 'research' dulu."]
    if r.status == "already":
        return [f"⚠️  '{r.idea_id}' sudah drafted. Lihat {r.path}"]
    if r.status == "wrong_stage":
        return [f"⚠️  '{r.idea_id}' di stage '{r.from_stage}', bukan 'researching/outlined'."]
    return [
        f"✅ Draft template created: {r.path}",
        f"   Next: agent isi draft via blog-writer (+voice +hooks +humanizer)",
    ]


def render_review(r: StageActionResult) -> list[str]:
    if r.status == "wrong_stage":
        return [f"❌ '{r.idea_id}' harus 'drafted' untuk review (sekarang: {r.from_stage})"]
    if r.status == "missing_file":
        return [f"❌ Draft file tidak ditemukan: {r.path}"]
    return [
        f"✅ '{r.idea_id}' masuk review queue.",
        f"   Next: blog-editor (model beda) review → 'gate {r.idea_id}'",
    ]


def render_gate(r: GateOutcome) -> tuple[list[str], int]:
    if r.status == "wrong_stage":
        return ([f"❌ '{r.idea_id}' harus 'reviewing'/'drafted' untuk gate "
                 f"(sekarang: {r.current_stage})"], 0)
    lines = [f"   ⚠️  {w}" for w in (r.result.warnings if r.result else [])]
    if r.status == "fail":
        lines.append(f"⛔ GATE FAIL — '{r.idea_id}' belum eligible:")
        for f in r.result.failures:
            lines.append(f"   ❌ {f}")
        lines.append("   → balik ke writer/humanizer, jangan naik ke human gate.")
        return (lines, 1)
    lines.append(f"✅ GATE PASS — '{r.idea_id}' eligible, masuk human go-live gate "
                 f"(autonomy:gated).")
    lines.append(f"   Approve manual: python3 pipeline.py approve {r.idea_id}")
    return (lines, 0)


def render_approve(r: StageActionResult) -> list[str]:
    if r.status == "wrong_stage":
        return [f"❌ '{r.idea_id}' harus 'gated' untuk approve (sekarang: {r.from_stage})"]
    return [
        f"✅ '{r.idea_id}' di-approve untuk go-live.",
        f"   Next: python3 pipeline.py publish {r.idea_id}  (butuh token.json)",
    ]


def render_publish(r: StageActionResult) -> list[str]:
    if r.status == "wrong_stage":
        return [f"❌ '{r.idea_id}' harus 'approved' untuk publish (sekarang: {r.from_stage})"]
    if r.status == "already_published":
        return [f"⛔ '{r.idea_id}' sudah ada di published/. Stop — anti double-publish."]
    if r.status == "no_token":
        return [
            f"🔒 OAuth belum di-setup ({TOKEN_PATH} tidak ada).",
            f"   Publish butuh login Google — lihat ~/Project/blog-lifecycle/docs/setup-credentials.md",
            f"   Stage tetap 'approved'; jalankan lagi setelah token.json siap.",
        ]
    if r.status == "pre_publish_fail":
        return [
            f"⛔ PRE-PUBLISH FAIL — '{r.idea_id}' punya marker unresolved:",
            *[f"   ❌ {f}" for f in r.failures],
            f"   → bersihkan marker di draft dulu, lalu jalankan ulang publish.",
        ]
    return [
        f"➡️  Siap publish '{r.idea_id}'. Jalankan blog-publisher untuk upload ke Blogger,",
        f"   lalu catat: pipeline akan transisi approved → published via publisher.",
    ]


def render_push_draft(r: StageActionResult) -> tuple[list[str], int]:
    if r.status == "wrong_stage":
        return ([f"❌ '{r.idea_id}' harus 'approved' untuk push-draft (sekarang: {r.from_stage})"], 1)
    if r.status == "already_pushed":
        return ([f"⛔ '{r.idea_id}' sudah pernah di-push ke Blogger (published/{r.idea_id}.json). Stop."], 0)
    if r.status == "no_token":
        return ([
            f"🔒 OAuth belum di-setup ({TOKEN_PATH} tidak ada).",
            f"   Push butuh login Google — lihat docs/setup-credentials.md",
        ], 1)
    if r.status == "missing_file":
        return ([f"❌ draft file '{r.idea_id}' hilang: {r.path}"], 1)
    if r.status == "pre_publish_fail":
        return ([
            f"⛔ PRE-PUSH FAIL — '{r.idea_id}' punya marker unresolved:",
            *[f"   ❌ {f}" for f in r.failures],
        ], 1)
    return ([
        f"✅ '{r.idea_id}' ter-push ke Blogger sebagai DRAFT (belum live).",
        f"   post_id: {r.post_id}",
        f"   url    : {r.url}",
        f"   Next: python3 pipeline.py attach-images {r.idea_id}  → lalu set permalink+deskripsi di editor → go-live.",
    ], 0)


def render_attach_images(r: StageActionResult) -> tuple[list[str], int]:
    if r.status == "not_pushed":
        return ([f"❌ '{r.idea_id}' belum di-push ke Blogger (jalankan push-draft dulu; stage: {r.from_stage})"], 1)
    if r.status == "no_assets":
        return ([f"❌ tidak ada gambar di assets/{r.idea_id}/ — imagery belum bikin aset?"], 1)
    if r.status == "missing_file":
        return ([f"❌ draft file '{r.idea_id}' hilang: {r.path}"], 1)
    return ([
        f"✅ '{r.idea_id}': {r.detail} gambar ter-host + tersisip, post Blogger di-update.",
        f"   Hero = thumbnail. Next: set permalink + deskripsi penelusuran di editor → go-live.",
    ], 0)
