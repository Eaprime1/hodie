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
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

WITNESS_SYMBOL = "∰"

# Canonical pattern: ∰ <space/tab(s)> YYYYMMDDHHMMSSMS (17 digits)
# Use horizontal whitespace only so a witness split across lines is not
# treated as valid when matching against a multi-line footer string.
WITNESS_PATTERN = re.compile(
    r"∰[ \t]+(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})(\d{3})"
)

# Number of lines from end of file to consider as "footer"
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


def check_file_witness(filepath: Path) -> Tuple[bool, Optional[str]]:
    """
    Check whether *filepath* has a valid ∰ witness in its footer.

    Returns:
        (is_compliant, witness_string_or_None)
    """
    try:
        text = filepath.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False, None

    lines = text.splitlines()
    footer = "\n".join(lines[-FOOTER_LINES:])

    match = WITNESS_PATTERN.search(footer)
    if match:
        stamp = "".join(match.groups())
        if is_valid_timestamp(stamp):
            return True, f"∰ {stamp}"

    return False, None


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
        json.dumps(state, indent=2, ensure_ascii=False),
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
    """Return the flagged-documents report as a Markdown string."""
    lines = _report_header("Prima Witness — Flagged Documents", scan_stamp)
    lines += [
        f"**Flagged count:** {len(flagged)}",
        "",
        "Newly introduced files listed below are missing the ∰ footer witness.",
        "Add a footer witness line in the canonical format:",
        "",
        "```",
        f"∰ {scan_stamp}",
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
) -> Tuple[List[Tuple[str, str]], List[str], List[Tuple[str, str]], List[str]]:
    """Classify all scannable files under *root* into compliant/missing buckets."""
    compliant: List[Tuple[str, str]] = []
    missing: List[str] = []
    new_compliant: List[Tuple[str, str]] = []
    new_missing: List[str] = []

    for filepath in iter_scannable_files(root):
        rel = str(filepath.relative_to(root))
        is_new = rel not in known_files
        ok, witness = check_file_witness(filepath)
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
    """Write all quepad report files for this scan cycle.

    Args:
        buckets:    Dict with keys compliant, missing, new_compliant, new_missing.
        summary:    Aggregated counts dict.
        scan_stamp: Canonical 17-digit witness timestamp for this scan.
    """
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


def scan(root: Path, strict: bool = False) -> int:
    """
    Run the footer witness scan.

    Args:
        root:   Repository root to scan.
        strict: If True, exit nonzero when any newly introduced file is
                missing the ∰ witness.

    Returns:
        0 on success / full compliance, 1 if violations detected (strict mode).
    """
    scan_stamp = now_witness_stamp()
    print(f"∰ Prima Witness Scanner — {scan_stamp}")
    print(f"  Root   : {root}")
    print(f"  Strict : {strict}")
    print()

    state = load_state()
    known_files: Dict = state.get("known_files", {})

    compliant, missing, new_compliant, new_missing = _classify_files(root, known_files)

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

    # Update incremental state
    new_known: Dict = dict(known_files)
    for rel, witness in compliant:
        new_known[rel] = {"compliant": True, "witness": witness, "last_seen": scan_stamp}
    for rel in missing:
        new_known[rel] = {"compliant": False, "witness": None, "last_seen": scan_stamp}
    state["last_scan"] = scan_stamp
    state["known_files"] = new_known
    save_state(state)

    print("  Reports → quepad/")
    print(f"  State   → {STATE_FILE}")

    if new_missing:
        print()
        print("🚩 FLAGGED — new files missing ∰ footer witness:")
        for f in sorted(new_missing):
            print(f"   {f}")
        print()
        print("  Add a footer witness line in the canonical format:")
        print(f"  ∰ {scan_stamp}")
        print()
        if strict:
            return 1

    return 0


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
    args = parser.parse_args()

    if args.stamp:
        stamp = now_witness_stamp()
        print(f"∰ {stamp}")
        cent = to_centesimal_minutes(stamp)
        if cent is not None:
            print(f"  centesimal: {cent:.4f} cmin  (100-min clock)")
        return

    root = args.root.resolve()
    sys.exit(scan(root, strict=args.strict))


if __name__ == "__main__":
    main()

# ∰ 20260424000000000
