#!/usr/bin/env python3
"""Status newsroom — jawab cepat: lagi diproses atau nggak?

Tampilkan: gateway/dispatcher hidup?, tiap artikel di board + stage mana yang
jalan/blocked/selesai, dan worker aktif. Untuk live: lihat tip di bawah.

Usage: python3 scripts/status.py [--board <slug>]
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

def _load_board():
    """Load board name from workspace/variables.json or config.yaml."""
    vpath = Path(__file__).resolve().parent.parent / "workspace" / "variables.json"
    if vpath.exists():
        data = json.loads(vpath.read_text())
        domain = data.get("DOMAIN", "")
        return domain.split(".")[0] if domain else ""
    cpath = Path(__file__).resolve().parent.parent / "workspace" / "config.yaml"
    if cpath.exists():
        import yaml
        cfg = yaml.safe_load(cpath.read_text())
        domain = cfg.get("domain", "")
        return domain.split(".")[0] if domain else ""
    return ""

BOARD = _load_board()
STAGES = ["research", "write", "edit", "imagery", "gate", "publish", "promote", "analyze"]
ICON = {"done": "✓", "running": "●", "blocked": "⊘", "ready": "◌", "todo": "○",
        "review": "◑", "scheduled": "◔", "triage": "△", "archived": "·"}


def sh(*args):
    return subprocess.run(args, capture_output=True, text=True)


def main() -> int:
    board = BOARD
    if "--board" in sys.argv:
        board = sys.argv[sys.argv.index("--board") + 1]

    # 1. Gateway / dispatcher
    gw = sh("hermes", "gateway", "status")
    gw_up = "running" in (gw.stdout + gw.stderr).lower()
    print("═══ NEWSROOM STATUS ═══")
    print(f"Gateway/dispatcher : {'🟢 NYALA (task ready akan diproses)' if gw_up else '🔴 MATI (task NGGAK akan jalan — `hermes gateway run`)'}")

    # 2. Tasks on the board
    r = sh("hermes", "kanban", "--board", board, "list", "--json")
    try:
        tasks = json.loads(r.stdout)
        if isinstance(tasks, dict):
            tasks = tasks.get("tasks", tasks.get("items", []))
    except Exception:
        tasks = []

    by_idea = {}
    for t in tasks:
        m = re.match(r"\[([^\]]+)\]\s*(\w+)", t.get("title", ""))
        if not m:
            continue
        idea, stage = m.group(1), m.group(2)
        by_idea.setdefault(idea, {})[stage] = t.get("status", "?")

    any_running = False
    if not by_idea:
        print("\nBelum ada artikel di pipeline newsroom.")
        print(f"Mulai: python3 scripts/newsroom.py <idea_id>")
    else:
        print(f"\nArtikel di board '{board}':\n")
        for idea, stages in by_idea.items():
            chain = []
            active = None
            for s in STAGES:
                st = stages.get(s)
                if st is None:
                    continue
                chain.append(f"{ICON.get(st, '?')}{s}")
                if st == "running":
                    active = s
                    any_running = True
            print(f"  ▸ {idea}")
            print(f"    {' → '.join(chain)}")
            if active:
                print(f"    ⏳ SEDANG DIPROSES: tahap '{active}'")
            elif all(stages.get(s) in ("done", None) for s in STAGES):
                print(f"    ✅ selesai (atau nunggu stage berikutnya)")
            elif any(v == "blocked" for v in stages.values()):
                blk = [s for s in STAGES if stages.get(s) == "blocked"]
                print(f"    ⛔ nunggu (blocked): {', '.join(blk)}  — mis. gate butuh approval")
            print()

    # 3. Worker proses aktif
    ps = sh("bash", "-c", "ps -ef | grep -oE 'hermes -p [a-z]+ .*kanban task t_[0-9a-f]+' | grep -v grep")
    workers = [l for l in ps.stdout.splitlines() if l.strip()]
    if workers:
        print("Worker aktif sekarang:")
        for w in workers:
            mp = re.search(r"-p (\w+)", w)
            mt = re.search(r"task (t_\w+)", w)
            print(f"  • {mp.group(1) if mp else '?'}  ({mt.group(1) if mt else '?'})")
    else:
        print("Worker aktif: (tidak ada yang jalan saat ini)")

    # 4. Verdict + live tip
    print("\n" + ("⏳ Newsroom SEDANG memproses." if (any_running or workers)
                   else "😴 Newsroom idle (tidak ada yang sedang diproses)."))
    print(f"\nLive monitor (real-time): hermes kanban --board {board} watch")
    print(f"Detail 1 artikel       : python3 scripts/pipeline.py status")
    return 0


if __name__ == "__main__":
    sys.exit(main())
