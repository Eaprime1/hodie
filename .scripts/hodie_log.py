#!/usr/bin/env python3
"""
hodie_log.py — HODIE session log reader, reporter, and checklist builder.

Every operation that touches HODIE can log a structured JSON entry to
_TODAY/daily/session.log. This script reads that log and produces:
  - Summary report of today's activity
  - Auto-generated TODO checklist from open items
  - Plexus routing suggestions based on content processed

Usage:
  python3 .scripts/hodie_log.py                  # today's report
  python3 .scripts/hodie_log.py --date 2026-04-14  # specific date
  python3 .scripts/hodie_log.py --checklist        # print actionable checklist
  python3 .scripts/hodie_log.py --watch            # tail -f the log live
  python3 .scripts/hodie_log.py --append "note"    # add a manual note
"""

import argparse
import json
import sys
import time
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

HODIE_ROOT = Path(__file__).parent.parent
LOG_DIR = HODIE_ROOT / "_TODAY" / "daily"

PLEXUS_HINTS = {
    "zero_point": "triplex",       # needs relationship mapping
    "migration": "duplex",          # shadow + carbon tracking
    "intake": "simplex",            # single stream, assess first
    "pr_review": "quadroplex",      # synergy — multiple reviewers
    "entity_update": "triplex",     # transistor routing to quanta
    "session_note": "simplex",      # one entry per cycle
    "checklist": "duplex",          # open + done sides
}

# ---------------------------------------------------------------------------
# Log I/O
# ---------------------------------------------------------------------------

def log_file_for(target_date: str) -> Path:
    return LOG_DIR / f"{target_date}-session.log" if target_date != date.today().isoformat() \
           else LOG_DIR / "session.log"


def read_log(log_path: Path) -> list[dict]:
    if not log_path.exists():
        return []
    entries = []
    for line in log_path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            # Plain text note
            entries.append({"timestamp": "", "operation": "note", "text": line})
    return entries


def append_log(log_path: Path, entry: dict) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry) + '\n')

# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def render_report(entries: list[dict], target_date: str) -> str:
    if not entries:
        return f"No log entries for {target_date}.\n"

    by_op = defaultdict(list)
    for e in entries:
        by_op[e.get("operation", "unknown")].append(e)

    lines = [
        f"# HODIE Session Report — {target_date}",
        f"**Entries**: {len(entries)}  |  **Operations**: {len(by_op)}",
        "",
    ]

    for op, items in sorted(by_op.items()):
        lines.append(f"## {op.replace('_', ' ').title()} ({len(items)})")
        plexus = PLEXUS_HINTS.get(op, "simplex")
        lines.append(f"*Suggested plexus stage: {plexus}*")
        for item in items[-5:]:  # last 5 per operation type
            ts = item.get("timestamp", "")[:19].replace("T", " ")
            summary = _summarize_entry(item)
            lines.append(f"- `{ts}` {summary}")
        lines.append("")

    return "\n".join(lines)


def _summarize_entry(entry: dict) -> str:
    op = entry.get("operation", "note")
    if op == "zero_point":
        zp = entry.get("zero_point", "?")
        doc = Path(entry.get("document", "")).name
        return f"Zero-point '{zp}' from {doc}"
    if op == "migration":
        return f"Migrated: {entry.get('source', '?')} → {entry.get('destination', '?')}"
    if op == "intake":
        return f"Intake: {entry.get('file', '?')} → {entry.get('plexus_stage', '?')}"
    if op == "note":
        return entry.get("text", "")[:80]
    return json.dumps({k: v for k, v in entry.items() if k not in ("timestamp", "operation")})[:80]

# ---------------------------------------------------------------------------
# Checklist builder
# ---------------------------------------------------------------------------

def build_checklist(entries: list[dict]) -> str:
    """
    Build a TODO checklist from log entries.
    Anything with status='open', 'pending', or no status gets a checkbox.
    Completed items get a checked box.
    """
    lines = ["# HODIE Checklist — Auto-generated", ""]

    open_items = []
    done_items = []

    for entry in entries:
        status = entry.get("status", "")
        op = entry.get("operation", "")
        summary = _summarize_entry(entry)

        if status == "complete" or status == "done":
            done_items.append(f"- [x] {summary}")
        elif op in ("zero_point", "migration", "intake", "pr_review"):
            # These are completable actions
            plexus = PLEXUS_HINTS.get(op, "simplex")
            open_items.append(f"- [ ] [{plexus}] {summary}")

    # Add standard recurring HODIE checklist items
    standard = [
        "- [ ] [simplex] Check _TODAY/inbox/ for new arrivals",
        "- [ ] [duplex] Run redundancy scan on new content",
        "- [ ] [triplex] Route processed content to plexus stages",
        "- [ ] [quadroplex] Review open PRs and AI review comments",
        "- [ ] [simplex] Write session note to _TODAY/daily/",
    ]

    if open_items:
        lines.append("## Open")
        lines.extend(open_items)
        lines.append("")

    lines.append("## Standard (One Hertz)")
    lines.extend(standard)
    lines.append("")

    if done_items:
        lines.append("## Done")
        lines.extend(done_items)
        lines.append("")

    return "\n".join(lines)

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="HODIE session log reader and checklist builder")
    parser.add_argument("--date", default=date.today().isoformat(), help="Date to report (YYYY-MM-DD)")
    parser.add_argument("--checklist", action="store_true", help="Print actionable checklist")
    parser.add_argument("--watch", action="store_true", help="Tail the log live")
    parser.add_argument("--append", metavar="NOTE", help="Append a manual note to today's log")
    args = parser.parse_args()

    log_path = log_file_for(args.date)

    if args.append:
        entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": "note",
            "text": args.append,
            "status": "open",
        }
        append_log(log_path, entry)
        print(f"✓ Note logged: {args.append}")
        return

    if args.watch:
        print(f"Watching {log_path} (Ctrl+C to stop)...")
        last_size = 0
        while True:
            try:
                if log_path.exists():
                    current_size = log_path.stat().st_size
                    if current_size > last_size:
                        entries = read_log(log_path)
                        if entries:
                            newest = entries[-1]
                            ts = newest.get("timestamp", "")[:19]
                            print(f"[{ts}] {_summarize_entry(newest)}")
                        last_size = current_size
                time.sleep(2)
            except KeyboardInterrupt:
                break
        return

    entries = read_log(log_path)

    if args.checklist:
        print(build_checklist(entries))
    else:
        print(render_report(entries, args.date))


if __name__ == "__main__":
    main()
