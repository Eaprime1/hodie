#!/usr/bin/env python3
"""
Workflow Expression Injection Checker
∰◊€π¿🌌∞

Scans GitHub Actions workflow files for expression injection:
${{ github.* }} or similar expressions used directly inside run: shell steps.

This is the pattern Codacy/Semgrep flags as HIGH security (CWE-20).
Fix: move ${{ }} expressions to the step's env: block, then reference
as $ENV_VAR in the shell script.

Usage:
  python scripts/check_workflow_injection.py [--check DIR] [FILE ...]

Exits 0 if clean, 1 if injection patterns found.
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple

# Matches any ${{ ... }} expression (GitHub Actions template syntax)
EXPRESSION_RE = re.compile(r"\$\{\{[^}]+\}\}")

# run: key variants
RUN_BLOCK_RE = re.compile(r"^\s*run:\s*[\|>-]*\s*$")
RUN_INLINE_RE = re.compile(r"^\s*run:\s+(.+)$")


def check_file(path: Path) -> List[Tuple[int, str, str]]:
    """
    Scan *path* for expression injection in run: steps.

    Returns a list of (line_number, line_text, context) tuples.
    """
    issues: List[Tuple[int, str, str]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        print(f"  ⚠ Could not read {path}: {exc}", file=sys.stderr)
        return issues

    in_run_block = False
    run_indent = 0

    for lineno, raw in enumerate(lines, 1):
        stripped = raw.lstrip()
        indent = len(raw) - len(stripped)

        # Single-line run: run: some command ${{ expr }}
        m = RUN_INLINE_RE.match(raw)
        if m:
            if EXPRESSION_RE.search(m.group(1)):
                issues.append((lineno, raw.rstrip(), "run: (inline)"))
            in_run_block = False
            continue

        # Multi-line run block: run: | or run: |-
        if RUN_BLOCK_RE.match(raw):
            in_run_block = True
            run_indent = indent
            continue

        if in_run_block:
            # End of block: non-empty line at or before run_indent
            if raw.strip() and indent <= run_indent:
                in_run_block = False
                # Check this line normally (it may start a new key)
            else:
                if EXPRESSION_RE.search(raw):
                    issues.append((lineno, raw.rstrip(), "run: block"))
                continue

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check GitHub Actions workflow files for expression injection.",
        epilog=(
            "Expression injection: using ${{ github.* }} directly inside run: steps.\n"
            "Fix: assign to env: block, reference as $ENV_VAR in shell.\n"
            "\n"
            "Example fix:\n"
            "  env:\n"
            "    GH_EVENT: ${{ github.event_name }}\n"
            "  run: |\n"
            "    echo $GH_EVENT\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--check",
        metavar="DIR",
        default=None,
        help="Directory to scan for *.yml files (e.g. .github/workflows/)",
    )
    parser.add_argument(
        "files",
        nargs="*",
        type=Path,
        help="Specific workflow files to check",
    )
    args = parser.parse_args()

    targets: List[Path] = list(args.files)
    if args.check:
        targets += sorted(Path(args.check).glob("*.yml"))

    if not targets:
        print("No files to check. Pass --check DIR or file paths.")
        return 0

    total_issues = 0

    for path in targets:
        issues = check_file(path)
        if issues:
            total_issues += len(issues)
            print(f"\n🚩 {path}  ({len(issues)} issue(s))")
            for lineno, line, context in issues:
                print(f"   Line {lineno} [{context}]: {line.strip()}")
            print()
            print(
                "   Fix: move each ${{ }} expression to the step's env: block,\n"
                "   then reference it as $ENV_VAR in the run: script."
            )

    if total_issues == 0:
        print(f"✅ {len(targets)} workflow file(s) checked — no expression injection found.")
        return 0

    print(f"\n⛔ {total_issues} expression injection issue(s) across {len(targets)} file(s).")
    return 1


if __name__ == "__main__":
    sys.exit(main())

# ∰⏱🃏 20260724120000000
