#!/usr/bin/env python3
"""
Prima Witness Footer Scanner — PIXEL8 / Hodie
∰◊€π¿🌌∞

Scans project documents for the ∰ footer witness symbol with canonical timestamp.

ADDITIVE SEMANTICS
------------------
Documents carrying ∰ are ADDITIVE, ALWAYS ADDITIVE — representing provenance
accumulation, not replacement or removal.  The ∰ marker must never be treated
with replace/remove semantics.  It is a prima witness of a document's existence
and evolution.

A document may carry multiple ∰ witness lines, one per meaningful iteration.
The scanner validates only the most recent (last) witness line.  All earlier
lines are retained as provenance — they must never be removed.

TIMESTAMP FORMAT
----------------
  ∰ YYYYMMDDHHMMSSMS

  Where:
    YYYY = year         (4 digits)
    MM   = month        (2 digits)
    DD   = day          (2 digits)
    HH   = hour         (2 digits, 24 h)
    MM   = minute       (2 digits)
    SS   = second       (2 digits)
    MS   = milliseconds (3 digits, 000–999)

  Total: 17 numeric digits.
  Example: ∰ 20260424024720123

ICON-EMBEDDED FORMAT
--------------------
Icons (emoji or symbols) may be placed directly after ∰ with no space, before
the timestamp whitespace.  Examples:

  ∰⏱ 20260424024720123          (time/arrival icon)
  ∰⏱🃏 20260424024720123        (arrival + current iteration)

Use --list-icons <file> to inspect which icons appear in a file's witness lines.
The icon registry lives in quepad/icon-registry.md.

QUEPAD / EGRESS
---------------
Reports are written to quepad/ (Pad of Q — queue intake concept).
Egress markers follow the egressum-Q naming convention, compatible with
BBS/FidoNet-style flow.

ARCHITECTURE NOTE — 100-MINUTE CLOCK
--------------------------------------
A future conversion adaptor will map canonical timestamps to decimal/centesimal
time (100-minute clock). In this representation, 1 day = 10 centesimal hours,
each centesimal hour = 100 centesimal subunits, for a total of 10 000
centesimal day-units per day.

Conversion from canonical HH:MM:SS to centesimal day-units ("cmin" in this
module's current naming):
  total_seconds      = HH * 3600 + MM * 60 + SS
  centesimal_minutes = total_seconds / 86400 * 10000   (range 0 – 9999.99…)

Canonical timestamps are stored in standard SI time for interoperability.
The 100-minute conversion is applied only at display/reporting time, not to
the stored stamp.  This design ensures forward compatibility when the official
decimal-time standard is formalised.
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

WITNESS_SYMBOL = "∰"

# Canonical pattern: ∰ [optional icons] <space/tab(s)> YYYYMMDDHHMMSSMS (17 digits)
#
# Icons are non-whitespace, non-digit characters (emoji, symbols) placed
# directly after ∰ with no intervening space.  The timestamp follows after
# one or more horizontal whitespace characters.
#
# Examples:
#   ∰ 20260424024720123          (plain — original format)
#   ∰⏱ 20260424024720123         (one icon)
#   ∰⏱🃏 20260424024720123       (icon + iteration marker)
#
# Enforce full-token match: after the 17-digit timestamp only optional
# horizontal whitespace is allowed before end-of-line or end-of-string,
# so trailing text such as "∰ 20260424024720123 extra" is rejected.
WITNESS_PATTERN = re.compile(
    r"∰[^\s\d]*[ \t]+(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})(\d{3})[ \t]*$",
    re.MULTILINE,
)

# Extracts the icon string between ∰ and the first whitespace
_ICON_EXTRACT_RE = re.compile(r"^∰([^\s\d]*)")

# Number of lines from end of file to consider as "footer"
# (kept for egress marker context; accumulation scan searches full document)
FOOTER_LINES = 15

# File extensions scanned for footer witness
SCANNABLE_EXTENSIONS = frozenset({".md", ".txt", ".rst", ".py"})

# Directory names excluded from scanning
EXCLUDED_DIRS = frozenset(
    {
        "_CONSOLIDATED",
        "_SORTING",
        "_BOX_SIMULATION",
        ".git",
        "venv",
        "env",
        "__pycache__",
        "quepad",
        "node_modules",
        ".github",
        "dist",
        "build",
        ".pytest_cache",
        ".mypy_cache",
        "migrations",
        ".eric",
        ".agents",
        ".codex",
    }
)

QUEPAD_DIR = Path("quepad")
STATE_FILE = QUEPAD_DIR / "state.json"
ICON_REGISTRY_FILE = QUEPAD_DIR / "icon-registry.md"

# Built-in icon definitions used when quepad/icon-registry.md does not exist.
# Update quepad/icon-registry.md to extend or override without editing this file.
BUILTIN_ICON_REGISTRY: Dict[str, str] = {
    "⏱": "time / ledger arrival",
    "🃏": "joker / current iteration",
    "🛠": "tooling / build",
    "📋": "documentation / checklist",
}


# ---------------------------------------------------------------------------
# Timestamp utilities
# ---------------------------------------------------------------------------


def now_witness_stamp() -> str:
    """Generate a canonical witness timestamp: YYYYMMDDHHMMSSMS (17 chars)."""
    ts = datetime.now(timezone.utc)
    ms = ts.microsecond // 1000  # microseconds → milliseconds (3 digits)
    return f"{ts.strftime('%Y%m%d%H%M%S')}{ms:03d}"


def is_valid_timestamp(stamp: str) -> bool:
    """Return True if *stamp* is a valid 17-digit witness timestamp."""
    if len(stamp) != 17 or not stamp.isdigit():
        return False
    try:
        year = int(stamp[0:4])
        month = int(stamp[4:6])
        day = int(stamp[6:8])
        hour = int(stamp[8:10])
        minutes = int(stamp[10:12])
        second = int(stamp[12:14])
        # Milliseconds (stamp[14:17], range 000-999): no further validation
        # needed beyond the isdigit() check already performed above.
        datetime(year, month, day, hour, minutes, second)
        return True
    except ValueError:
        return False


def to_centesimal_minutes(stamp: str) -> Optional[float]:
    """
    Convert a 17-digit witness stamp to centesimal minutes (100-minute clock).

    Returns the centesimal minute value in the range [0, 10000), or None if
    the stamp is invalid.  See module docstring for conversion formula.
    """
    if not is_valid_timestamp(stamp):
        return None
    hour = int(stamp[8:10])
    minute = int(stamp[10:12])
    second = int(stamp[12:14])
    total_seconds = hour * 3600 + minute * 60 + second
    return total_seconds / 86400.0 * 10000.0


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------


def get_git_new_files(root: Path, base_ref: str) -> Optional[Set[str]]:
    """Return repo-relative paths of files added since *base_ref*, or None on failure.

    Uses ``git diff --name-only --diff-filter=A <base_ref>...HEAD`` so only
    files that are genuinely new to this branch are treated as "new" by the
    scanner.  This is the correct behaviour for PR checks where state.json
    is not persisted between runs — it prevents every file from appearing
    new on every pull_request event.
    """
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=A", f"{base_ref}...HEAD"],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        )
        return {line.strip() for line in result.stdout.splitlines() if line.strip()}
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


# ---------------------------------------------------------------------------
# Witness line utilities — accumulation semantics
# ---------------------------------------------------------------------------


def extract_witness_lines(filepath: Path) -> List[Tuple[str, str, str]]:
    """
    Find ALL ∰ witness lines in *filepath*, searching the entire document.

    Accumulation semantics: a document may carry one ∰ line per meaningful
    iteration.  The scanner searches the whole file — not just the footer
    — so every provenance stamp is discovered.  The last entry in the
    returned list is the current (most recent) witness; all earlier entries
    are provenance and must never be removed.

    Returns a list of (raw_line_stripped, icons, stamp) tuples in document
    order (oldest first).
    """
    try:
        text = filepath.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []

    results: List[Tuple[str, str, str]] = []
    for m in WITNESS_PATTERN.finditer(text):
        raw = m.group(0).strip()
        stamp = "".join(m.groups())
        icon_m = _ICON_EXTRACT_RE.match(raw)
        icons = icon_m.group(1) if icon_m else ""
        results.append((raw, icons, stamp))
    return results


def _parse_icon_table_row(line: str) -> Optional[Tuple[str, str]]:
    """Parse one markdown table row; return (icon, meaning) or None."""
    if not line.startswith("|"):
        return None
    parts = [p.strip() for p in line.strip("|").split("|")]
    if len(parts) < 2:
        return None
    icon = parts[0]
    if not icon or "Icon" in icon or not icon.strip("-"):
        return None
    meaning = parts[-1]
    return (icon, meaning) if meaning else None


def load_icon_registry() -> Dict[str, str]:
    """
    Load the icon → meaning mapping from quepad/icon-registry.md.

    Falls back to BUILTIN_ICON_REGISTRY when the file does not exist.
    Entries in the file extend and override the built-ins.
    """
    registry: Dict[str, str] = dict(BUILTIN_ICON_REGISTRY)
    if not ICON_REGISTRY_FILE.exists():
        return registry
    try:
        for raw_line in ICON_REGISTRY_FILE.read_text(encoding="utf-8").splitlines():
            parsed = _parse_icon_table_row(raw_line.strip())
            if parsed is not None:
                registry[parsed[0]] = parsed[1]
    except OSError:
        pass
    return registry


def _print_icon_summary(witnesses: List[Tuple[str, str, str]], registry: Dict[str, str]) -> None:
    """Print the unique-icon summary block for ``list_file_icons``."""
    seen: Set[str] = set()
    unique: List[str] = []
    for _, icons, _ in witnesses:
        for ch in icons:
            if ch not in seen:
                seen.add(ch)
                unique.append(ch)
    if unique:
        print()
        print(f"  Unique icons: {''.join(unique)}")
        for ch in unique:
            print(f"    {ch}  {registry.get(ch, '(unknown)')}")


def _print_witness_line(
    i: int, count: int, entry: Tuple[str, str, str], registry: Dict[str, str]
) -> None:
    """Print one ∰ witness entry with its icon annotations."""
    raw, icons, stamp = entry
    label = "current  " if i == count - 1 else f"provenance[{i}]"
    valid_mark = "✓" if is_valid_timestamp(stamp) else "✗ INVALID"
    cent = to_centesimal_minutes(stamp)
    cent_str = f"  [{cent:.2f} cmin]" if cent is not None else ""
    print(f"  [{label}] {raw}  {valid_mark}{cent_str}")
    if icons:
        for ch in icons:
            meaning = registry.get(ch, "(unknown)")
            if meaning != "(unknown)":
                print(f"              {ch!r} → {meaning}")
    else:
        print("              (no icons)")


def list_file_icons(filepath: Path) -> None:
    """
    Print ∰ witness lines and their icon annotations from *filepath*.

    Called by the ``--list-icons`` CLI flag.  Exits after printing —
    does not run a full repository scan.
    """
    registry = load_icon_registry()
    witnesses = extract_witness_lines(filepath)

    if not witnesses:
        print(f"No ∰ witness lines found in: {filepath}")
        return

    count = len(witnesses)
    print(f"∰ witness lines in {filepath.name}  ({count} total):")
    print()

    for i, entry in enumerate(witnesses):
        _print_witness_line(i, count, entry, registry)

    _print_icon_summary(witnesses, registry)


# ---------------------------------------------------------------------------
# File scanning
# ---------------------------------------------------------------------------


def iter_scannable_files(root: Path):
    """Yield all scannable files under *root*, honouring EXCLUDED_DIRS."""
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix not in SCANNABLE_EXTENSIONS:
            continue
        # Reject if any ancestor directory name is in the exclusion list
        rel_parts = path.relative_to(root).parts
        if any(part in EXCLUDED_DIRS for part in rel_parts):
            continue
        yield path


def check_file_witness(filepath: Path) -> Tuple[bool, Optional[str], List[str]]:
    """
    Check whether *filepath* has a valid ∰ witness.

    Accumulation semantics: searches the entire document for all ∰ witness
    lines; validates only the most recent (last) one; returns earlier lines
    as provenance.  Provenance lines do not affect the compliance verdict.

    Returns:
        (is_compliant, current_witness_or_None, provenance_lines)
    """
    witnesses = extract_witness_lines(filepath)
    if not witnesses:
        return False, None, []

    provenance = [raw for raw, _, _ in witnesses[:-1]]
    _, icons, stamp = witnesses[-1]

    if is_valid_timestamp(stamp):
        witness_str = f"∰{icons} {stamp}" if icons else f"∰ {stamp}"
        return True, witness_str, provenance

    return False, None, [raw for raw, _, _ in witnesses]


# ---------------------------------------------------------------------------
# State management
# ---------------------------------------------------------------------------


def load_state() -> Dict:
    """Load the incremental scan state from quepad/state.json."""
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {"last_scan": None, "known_files": {}}


def save_state(state: Dict) -> None:
    """Persist state to quepad/state.json."""
    QUEPAD_DIR.mkdir(exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(state, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Report builders
# ---------------------------------------------------------------------------


def _report_header(title: str, scan_stamp: str) -> List[str]:
    return [
        f"# {title}",
        f"∰ {scan_stamp}",
        "",
        "> **Additive semantics:** Documents carrying ∰ are additive, always",
        "> additive.  This marker represents provenance accumulation and must",
        "> never be treated with replace/remove semantics.",
        "",
        f"**Scan timestamp:** `{scan_stamp}`",
        "",
        "---",
        "",
    ]


def build_compliance_report(
    compliant: List[Tuple[str, str]],
    missing: List[str],
    scan_stamp: str,
) -> str:
    """Return the full compliance report as a Markdown string."""
    lines = _report_header("Prima Witness — Compliance Report", scan_stamp)
    lines += [
        f"**Compliant files:** {len(compliant)}  ",
        f"**Missing witness:** {len(missing)}",
        "",
        "## ✅ Compliant (∰ witness present)",
        "",
    ]
    if compliant:
        for fpath, witness in sorted(compliant):
            lines.append(f"- `{fpath}` — `{witness}`")
    else:
        lines.append("*(none)*")

    lines += [
        "",
        "## ⚠️ Missing Footer Witness",
        "",
    ]
    if missing:
        for fpath in sorted(missing):
            lines.append(f"- `{fpath}`")
    else:
        lines.append("*(none — all scanned files are compliant)*")

    lines += ["", f"∰ {scan_stamp}", ""]
    return "\n".join(lines)


def build_new_docs_report(
    new_compliant: List[Tuple[str, str]],
    new_missing: List[str],
    scan_stamp: str,
) -> str:
    """Return the new-documents report as a Markdown string."""
    lines = _report_header("Prima Witness — New Documents Report", scan_stamp)
    lines += [
        f"**New compliant files:** {len(new_compliant)}  ",
        f"**New files missing witness:** {len(new_missing)}",
        "",
        "## ✅ New Compliant Files",
        "",
    ]
    if new_compliant:
        for fpath, witness in sorted(new_compliant):
            lines.append(f"- `{fpath}` — `{witness}`")
    else:
        lines.append("*(none)*")

    lines += [
        "",
        "## 🚩 New Files Missing Witness (ACTION REQUIRED)",
        "",
    ]
    if new_missing:
        for fpath in sorted(new_missing):
            lines.append(f"- `{fpath}`")
    else:
        lines.append("*(none — all new files carry the ∰ witness)*")

    lines += ["", f"∰ {scan_stamp}", ""]
    return "\n".join(lines)


def build_flagged_report(flagged: List[str], scan_stamp: str) -> str:
    """Return the flagged-documents report as a Markdown string.

    Shows the SI timestamp and centesimal equivalent side by side so
    operators can read the scan time in both the canonical and 100-minute
    clock systems.
    """
    cent = to_centesimal_minutes(scan_stamp)
    cent_str = f"{cent:.2f}" if cent is not None else "n/a"

    lines = _report_header("Prima Witness — Flagged Documents", scan_stamp)
    lines += [
        f"**Flagged count:** {len(flagged)}",
        "",
        f"**Scan stamp (SI):**         `{scan_stamp}`  ",
        f"**Scan stamp (centesimal):** `{cent_str}` cmin  *(100-min clock)*",
        "",
        "Newly introduced files listed below are missing the ∰ footer witness.",
        "Add a footer witness line in the canonical format:",
        "",
        "```",
        f"∰ {scan_stamp}",
        f"# centesimal: {cent_str} cmin",
        "```",
        "",
        "---",
        "",
    ]
    if flagged:
        for fpath in sorted(flagged):
            lines.append(f"- `{fpath}`")
    else:
        lines.append("*(no new non-compliant files detected — queue is clear)*")

    lines += ["", f"∰ {scan_stamp}", ""]
    return "\n".join(lines)


def build_egress_marker(scan_stamp: str, summary: Dict) -> str:
    """Return an egressum-Q egress marker document as a Markdown string."""
    cent = to_centesimal_minutes(scan_stamp)
    cent_str = f"{cent:.2f}" if cent is not None else "n/a"
    return "\n".join(
        [
            "# egressum-Q — Prima Witness Egress Marker",
            f"∰ {scan_stamp}",
            "",
            "## Queue Intake Summary",
            "",
            "| Field                  | Value                   |",
            "|------------------------|-------------------------|",
            f"| Scan stamp (canonical) | `{scan_stamp}`          |",
            f"| Scan stamp (centesimal)| `{cent_str}` cmin       |",
            f"| Total files scanned    | {summary['total']}       |",
            f"| Compliant              | {summary['compliant']}   |",
            f"| Missing witness        | {summary['missing']}     |",
            f"| New compliant          | {summary['new_compliant']}|",
            f"| New missing (flagged)  | {summary['new_missing']} |",
            "",
            "## egressum-Q Protocol",
            "",
            "This marker confirms the witness scan has been processed and",
            "results have entered the Pad of Q (quepad) intake.",
            "All flagged files must receive ∰ witness stamps before next egress.",
            "",
            "## Additive Semantics",
            "",
            "Documents carrying ∰ are **additive, always additive**.",
            "Witness stamps accumulate — they represent provenance,",
            "never replacement or removal.",
            "",
            "## 100-Minute Clock Note",
            "",
            "The centesimal minute column above shows the time of this scan",
            "expressed in the 100-minute (decimal) clock system:",
            "  1 day = 10 centesimal hours × 100 centesimal minutes.",
            "Canonical stamps are stored in SI time; centesimal conversion",
            "is applied at display time only.",
            "",
            f"∰ {scan_stamp}",
            "",
        ]
    )


# ---------------------------------------------------------------------------
# Main scan logic
# ---------------------------------------------------------------------------


def _classify_files(
    root: Path,
    known_files: Dict,
    git_new_files: Optional[Set[str]] = None,
) -> Tuple[List[Tuple[str, str]], List[str], List[Tuple[str, str]], List[str]]:
    """Classify all scannable files under *root* into compliant/missing buckets.

    *git_new_files*: when provided (e.g. from ``get_git_new_files``), a file is
    considered "new" only if its repo-relative path is in this set.  This is the
    correct behaviour for pull_request CI runs where ``state.json`` is not
    persisted between runs — it prevents every untracked file from appearing new
    on every PR check (the "only run once" guarantee).

    When *git_new_files* is None the legacy state-based logic applies: a file is
    "new" if it has no entry in *known_files*.
    """
    compliant: List[Tuple[str, str]] = []
    missing: List[str] = []
    new_compliant: List[Tuple[str, str]] = []
    new_missing: List[str] = []

    for filepath in iter_scannable_files(root):
        rel = str(filepath.relative_to(root))
        if git_new_files is not None:
            is_new = rel in git_new_files
        else:
            is_new = rel not in known_files
        ok, witness, _provenance = check_file_witness(filepath)
        if ok and witness is not None:
            compliant.append((rel, witness))
            if is_new:
                new_compliant.append((rel, witness))
        else:
            missing.append(rel)
            if is_new:
                new_missing.append(rel)

    return compliant, missing, new_compliant, new_missing


def _persist_reports(buckets: Dict, summary: Dict, scan_stamp: str) -> None:
    """Write all quepad report files for this scan cycle."""
    compliant = buckets["compliant"]
    missing = buckets["missing"]
    new_compliant = buckets["new_compliant"]
    new_missing = buckets["new_missing"]

    QUEPAD_DIR.mkdir(exist_ok=True)
    _write_report("compliance_report.md", build_compliance_report(compliant, missing, scan_stamp))
    _write_report(
        "new_docs_report.md",
        build_new_docs_report(new_compliant, new_missing, scan_stamp),
    )
    _write_report("flagged_report.md", build_flagged_report(new_missing, scan_stamp))
    _write_report(f"egressum-Q-{scan_stamp}.md", build_egress_marker(scan_stamp, summary))


def _persist_state(
    state: Dict,
    known_files: Dict,
    compliant: List[Tuple[str, str]],
    missing: List[str],
    scan_stamp: str,
) -> None:
    """Merge scan results into state and write state.json.

    Only touches an entry's last_seen when the file is new to known_files or
    its compliant/witness value actually changed since the last scan --
    previously every entry was rewritten with the fresh scan_stamp
    unconditionally on every run, so a push that changed one file produced a
    full-state diff touching every known file. That's the confirmed cause of
    state.json's rapid, largely-noise growth.
    """
    new_known: Dict = dict(known_files)

    def _update(rel: str, entry: Dict) -> None:
        existing = new_known.get(rel)
        if existing is None or existing.get("compliant") != entry["compliant"] or existing.get("witness") != entry["witness"]:
            new_known[rel] = {**entry, "last_seen": scan_stamp}
        # else: unchanged since last scan -- leave the existing entry (and its
        # last_seen) untouched, so the diff stays proportional to real change.

    for rel, witness in compliant:
        _update(rel, {"compliant": True, "witness": witness})
    for rel in missing:
        _update(rel, {"compliant": False, "witness": None})
    state["last_scan"] = scan_stamp
    state["known_files"] = new_known
    save_state(state)


def _report_flagged(new_missing: List[str], scan_stamp: str, strict: bool) -> int:
    """Print flagged-file warning and return the appropriate exit code."""
    if not new_missing:
        return 0
    cent = to_centesimal_minutes(scan_stamp)
    cent_str = f"{cent:.2f} cmin" if cent is not None else ""
    print()
    print("🚩 FLAGGED — new files missing ∰ footer witness:")
    for f in sorted(new_missing):
        print(f"   {f}")
    print()
    print(f"  Add a footer witness line: ∰ {scan_stamp}  [{cent_str}]")
    print()
    return 1 if strict else 0


def scan(root: Path, strict: bool = False, git_base: Optional[str] = None) -> int:
    """
    Run the footer witness scan.

    Args:
        root:     Repository root to scan.
        strict:   If True, exit nonzero when any newly introduced file is
                  missing the ∰ witness.
        git_base: If set, use ``git diff --diff-filter=A <git_base>...HEAD``
                  to determine which files are "new" instead of relying on
                  state.json.  Pass the PR base branch (e.g. ``origin/main``)
                  here on pull_request CI runs so each file is only flagged
                  once — the first time it is introduced.

    Returns:
        0 on success / full compliance, 1 if violations detected (strict mode).
    """
    scan_stamp = now_witness_stamp()
    print(f"∰ Prima Witness Scanner — {scan_stamp}")
    print(f"  Root   : {root}")
    print(f"  Strict : {strict}")
    if git_base:
        print(f"  Git base: {git_base} (git-diff new-file detection)")
    print()

    state = load_state()
    known_files: Dict = state.get("known_files", {})

    git_new_files: Optional[Set[str]] = None
    if git_base:
        git_new_files = get_git_new_files(root, git_base)
        if git_new_files is None:
            print("  ⚠ git diff failed — falling back to state.json new-file detection")
        else:
            print(f"  Git-new files: {len(git_new_files)}")

    compliant, missing, new_compliant, new_missing = _classify_files(
        root, known_files, git_new_files=git_new_files
    )

    summary: Dict = {
        "total": len(compliant) + len(missing),
        "compliant": len(compliant),
        "missing": len(missing),
        "new_compliant": len(new_compliant),
        "new_missing": len(new_missing),
    }

    flagged_label = " ← FLAGGED" if new_missing else ""
    print(f"  Files scanned  : {summary['total']}")
    print(f"  Compliant      : {summary['compliant']}")
    print(f"  Missing witness: {summary['missing']}")
    print(f"  New compliant  : {summary['new_compliant']}")
    print(f"  New missing    : {summary['new_missing']}{flagged_label}")
    print()

    buckets: Dict = {
        "compliant": compliant,
        "missing": missing,
        "new_compliant": new_compliant,
        "new_missing": new_missing,
    }
    _persist_reports(buckets, summary, scan_stamp)

    _persist_state(state, known_files, compliant, missing, scan_stamp)

    print("  Reports → quepad/")
    print(f"  State   → {STATE_FILE}")

    return _report_flagged(new_missing, scan_stamp, strict)


def _write_report(filename: str, content: str) -> Path:
    """Write *content* to quepad/*filename* and return the Path."""
    QUEPAD_DIR.mkdir(exist_ok=True)
    path = QUEPAD_DIR / filename
    path.write_text(content, encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> None:
    """CLI entry point for the Prima Witness footer scanner."""
    parser = argparse.ArgumentParser(
        prog="footer_witness",
        description="Prima Witness Footer Scanner — validates ∰ witness in document footers.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Timestamp format: ∰ YYYYMMDDHHMMSSMS  (17 digits, ms precision)\n"
            "Example:          ∰ 20260424024720123\n"
            "\n"
            "Accumulation semantics: a document may carry multiple ∰ lines,\n"
            "one per meaningful iteration.  Only the last line is validated;\n"
            "earlier lines are preserved as provenance — never remove them.\n"
            "\n"
            "Documents carrying ∰ are additive, always additive.\n"
        ),
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Repository root to scan (default: current directory)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with code 1 if any newly introduced file is missing its witness",
    )
    parser.add_argument(
        "--stamp",
        action="store_true",
        help="Print a fresh canonical witness stamp and exit",
    )
    parser.add_argument(
        "--git-base",
        metavar="REF",
        default=None,
        help=(
            "Use git diff against REF (e.g. origin/main) to identify newly added "
            "files instead of state.json.  Recommended for pull_request CI runs "
            "so each file is flagged only once — the first time it is introduced."
        ),
    )
    parser.add_argument(
        "--list-icons",
        metavar="FILE",
        default=None,
        help=(
            "Scan FILE and print all ∰ witness lines with icon annotations. "
            "Icons are looked up in quepad/icon-registry.md (falls back to "
            "built-ins). Exits after printing — does not run a full scan."
        ),
    )
    args = parser.parse_args()

    if args.stamp:
        stamp = now_witness_stamp()
        print(f"∰ {stamp}")
        cent = to_centesimal_minutes(stamp)
        if cent is not None:
            print(f"  centesimal: {cent:.4f} cmin  (100-min clock)")
        return

    if args.list_icons:
        list_file_icons(Path(args.list_icons))
        return

    root = args.root.resolve()
    sys.exit(scan(root, strict=args.strict, git_base=args.git_base))


if __name__ == "__main__":
    main()

# ∰ 20260424000000000
# ∰⏱🃏 20260724120000000
