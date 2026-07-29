#!/usr/bin/env python3
"""hodie_log.py — HODIE session log reader, reporter, and checklist builder.

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

_SUMMARIES = {
    "zero_point": lambda e: f"Zero-point '{e.get('zero_point', '?')}' from {Path(e.get('document', '')).name}",
    "migration": lambda e: f"Migrated: {e.get('source', '?')} → {e.get('destination', '?')}",
    "intake": lambda e: f"Intake: {e.get('file', '?')} → {e.get('plexus_stage', '?')}",
    "note": lambda e: e.get("text", "")[:80],
}


def _summarize_entry(entry: dict) -> str:
    op = entry.get("operation", "note")
    handler = _SUMMARIES.get(op)
    if handler:
        return handler(entry)
    return json.dumps({k: v for k, v in entry.items() if k not in ("timestamp", "operation")})[:80]


def _format_op_section(op: str, items: list[dict]) -> list[str]:
    plexus = PLEXUS_HINTS.get(op, "simplex")
    lines = [
        f"## {op.replace('_', ' ').title()} ({len(items)})",
        f"*Suggested plexus stage: {plexus}*",
    ]
    for item in items[-5:]:
        ts = item.get("timestamp", "")[:19].replace("T", " ")
        lines.append(f"- `{ts}` {_summarize_entry(item)}")
    lines.append("")
    return lines


def render_report(entries: list[dict], target_date: str) -> str:
    if not entries:
        return f"No log entries for {target_date}.\n"
    by_op: defaultdict[str, list] = defaultdict(list)
    for e in entries:
        by_op[e.get("operation", "unknown")].append(e)
    lines = [
        f"# HODIE Session Report — {target_date}",
        f"**Entries**: {len(entries)}  |  **Operations**: {len(by_op)}",
        "",
    ]
    for op, items in sorted(by_op.items()):
        lines.extend(_format_op_section(op, items))
    return "\n".join(lines)

# ---------------------------------------------------------------------------
# Checklist builder
# ---------------------------------------------------------------------------

_STANDARD_CHECKLIST = [
    "- [ ] [simplex] Check _TODAY/inbox/ for new arrivals",
    "- [ ] [duplex] Run redundancy scan on new content",
    "- [ ] [triplex] Route processed content to plexus stages",
    "- [ ] [quadroplex] Review open PRs and AI review comments",
    "- [ ] [simplex] Write session note to _TODAY/daily/",
]


def _classify_entries(entries: list[dict]) -> tuple[list[str], list[str]]:
    """Separate log entries into open and done checklist items."""
    open_items: list[str] = []
    done_items: list[str] = []
    for entry in entries:
        status = entry.get("status", "")
        op = entry.get("operation", "")
        summary = _summarize_entry(entry)
        if status in ("complete", "done"):
            done_items.append(f"- [x] {summary}")
        elif op in ("zero_point", "migration", "intake", "pr_review"):
            plexus = PLEXUS_HINTS.get(op, "simplex")
            open_items.append(f"- [ ] [{plexus}] {summary}")
    return open_items, done_items


def build_checklist(entries: list[dict]) -> str:
    """Build a TODO checklist from log entries.

    Anything with status='open', 'pending', or no status gets a checkbox.
    Completed items get a checked box.
    """
    open_items, done_items = _classify_entries(entries)
    lines = ["# HODIE Checklist — Auto-generated", ""]
    if open_items:
        lines += ["## Open", *open_items, ""]
    lines += ["## Standard (One Hertz)", *_STANDARD_CHECKLIST, ""]
    if done_items:
        lines += ["## Done", *done_items, ""]
    return "\n".join(lines)

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _watch_log(log_path: Path) -> None:
    """Tail the log file, printing new entries as they arrive."""
    print(f"Watching {log_path} (Ctrl+C to stop)...")
    last_size = 0
    while True:
        try:
            if log_path.exists():
                current_size = log_path.stat().st_size
                if current_size > last_size:
                    entries = read_log(log_path)
                    if entries:
                        ts = entries[-1].get("timestamp", "")[:19]
                        print(f"[{ts}] {_summarize_entry(entries[-1])}")
                    last_size = current_size
            time.sleep(2)
        except KeyboardInterrupt:
            break


def main():
    parser = argparse.ArgumentParser(description="HODIE session log reader and checklist builder")
    parser.add_argument("--date", default=date.today().isoformat(), help="Date to report (YYYY-MM-DD)")
    parser.add_argument("--checklist", action="store_true", help="Print actionable checklist")
    parser.add_argument("--watch", action="store_true", help="Tail the log live")
    parser.add_argument("--append", metavar="NOTE", help="Append a manual note to today's log")
    args = parser.parse_args()

    log_path = log_file_for(args.date)

    if args.append:
        append_log(log_path, {
            "timestamp": datetime.now().isoformat(),
            "operation": "note",
            "text": args.append,
            "status": "open",
        })
        print(f"✓ Note logged: {args.append}")
        return

    if args.watch:
        _watch_log(log_path)
        return

    entries = read_log(log_path)
    print(build_checklist(entries) if args.checklist else render_report(entries, args.date))


if __name__ == "__main__":
    main()
