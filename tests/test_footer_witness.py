"""
Tests for the Prima Witness footer scanner.
∰◊€π¿🌌∞
"""

import json
from pathlib import Path

import pytest

# Ensure scripts/ is importable
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from footer_witness import (  # noqa: E402
    WITNESS_PATTERN,
    build_compliance_report,
    build_egress_marker,
    build_flagged_report,
    build_new_docs_report,
    check_file_witness,
    is_valid_timestamp,
    iter_scannable_files,
    load_state,
    now_witness_stamp,
    save_state,
    scan,
    to_centesimal_minutes,
)


# ---------------------------------------------------------------------------
# Timestamp utilities
# ---------------------------------------------------------------------------


class TestNowWitnessStamp:
    def test_returns_17_digits(self):
        stamp = now_witness_stamp()
        assert len(stamp) == 17
        assert stamp.isdigit()

    def test_year_prefix(self):
        stamp = now_witness_stamp()
        year = int(stamp[:4])
        assert 2024 <= year <= 2099

    def test_multiple_stamps_are_unique_or_increasing(self):
        stamps = [now_witness_stamp() for _ in range(5)]
        # Timestamps must be non-decreasing (same-millisecond ties are OK)
        assert stamps == sorted(stamps)


class TestIsValidTimestamp:
    def test_valid_stamp(self):
        assert is_valid_timestamp("20260424024720123") is True

    def test_wrong_length(self):
        assert is_valid_timestamp("202604240247201") is False  # 15 digits
        assert is_valid_timestamp("202604240247201234") is False  # 18 digits

    def test_non_digit(self):
        assert is_valid_timestamp("2026042402472012X") is False

    def test_invalid_month(self):
        assert is_valid_timestamp("20261304024720123") is False

    def test_invalid_day(self):
        assert is_valid_timestamp("20260432024720123") is False

    def test_invalid_hour(self):
        assert is_valid_timestamp("20260424254720123") is False

    def test_invalid_minute(self):
        assert is_valid_timestamp("20260424026020123") is False

    def test_invalid_second(self):
        assert is_valid_timestamp("20260424024760123") is False

    def test_all_zeros(self):
        # 00:00:00 on 0001-01-01 is a valid datetime
        assert is_valid_timestamp("00010101000000000") is True


class TestToCentesimalMinutes:
    def test_midnight_is_zero(self):
        result = to_centesimal_minutes("20260424000000000")
        assert result == pytest.approx(0.0)

    def test_noon_is_5000(self):
        # 12:00:00 → 12*3600/86400*10000 = 5000
        result = to_centesimal_minutes("20260424120000000")
        assert result == pytest.approx(5000.0)

    def test_end_of_day(self):
        # 23:59:59 → very close to 10000
        result = to_centesimal_minutes("20260424235959000")
        assert result is not None
        assert result < 10000.0
        assert result > 9990.0

    def test_invalid_stamp_returns_none(self):
        assert to_centesimal_minutes("notavalidstamp17") is None


# ---------------------------------------------------------------------------
# Witness pattern regex
# ---------------------------------------------------------------------------


class TestWitnessPattern:
    def test_matches_valid_line(self):
        line = "∰ 20260424024720123"
        assert WITNESS_PATTERN.search(line) is not None

    def test_matches_with_multiple_spaces(self):
        line = "∰   20260424024720123"
        assert WITNESS_PATTERN.search(line) is not None

    def test_does_not_match_symbol_alone(self):
        assert WITNESS_PATTERN.search("∰") is None

    def test_does_not_match_16_digits(self):
        # 16 digits — too short (MS must be 3 digits: 000–999)
        assert WITNESS_PATTERN.search("∰ 2026042402472012") is None

    def test_does_not_match_text_after_symbol(self):
        assert WITNESS_PATTERN.search("∰ hello world") is None

    def test_matches_in_markdown_footer(self):
        content = "Some document text\n\n---\n\n∰ 20260424024720123\n"
        assert WITNESS_PATTERN.search(content) is not None

    def test_matches_in_python_comment(self):
        content = "# some code\n\n# ∰ 20260424024720123\n"
        assert WITNESS_PATTERN.search(content) is not None

    def test_does_not_match_stamp_split_across_lines(self):
        content = "∰\n20260424024720123"
        assert WITNESS_PATTERN.search(content) is None

    def test_does_not_match_18_digits(self):
        assert WITNESS_PATTERN.search("∰ 202604240247201234") is None

    def test_does_not_match_trailing_text_after_timestamp(self):
        assert WITNESS_PATTERN.search("∰ 20260424024720123 trailing text") is None
# ---------------------------------------------------------------------------
# File-level witness check
# ---------------------------------------------------------------------------


class TestCheckFileWitness:
    def test_compliant_markdown(self, tmp_path):
        f = tmp_path / "doc.md"
        f.write_text("# Hello\n\nContent here.\n\n∰ 20260424024720123\n", encoding="utf-8")
        ok, witness, provenance = check_file_witness(f)
        assert ok is True
        assert witness == "∰ 20260424024720123"
        assert provenance == []

    def test_missing_witness(self, tmp_path):
        f = tmp_path / "doc.md"
        f.write_text("# Hello\n\nContent here.\n", encoding="utf-8")
        ok, witness, provenance = check_file_witness(f)
        assert ok is False
        assert witness is None
        assert provenance == []

    def test_witness_in_python_comment(self, tmp_path):
        f = tmp_path / "module.py"
        f.write_text("def foo():\n    pass\n\n# ∰ 20260424024720123\n", encoding="utf-8")
        ok, witness, _ = check_file_witness(f)
        assert ok is True

    def test_witness_anywhere_in_document_detected(self, tmp_path):
        # Accumulation semantics: the scanner searches the entire document,
        # so a witness at line 0 of a 21-line file IS detected.
        lines = ["line " + str(i) for i in range(20)]
        lines.insert(0, "∰ 20260424024720123")  # 21 total lines; witness at index 0
        f = tmp_path / "doc.txt"
        f.write_text("\n".join(lines), encoding="utf-8")
        ok, witness, provenance = check_file_witness(f)
        assert ok is True
        assert provenance == []  # only one witness — no provenance

    def test_accumulation_semantics_validates_last_witness(self, tmp_path):
        # Multiple witness lines: scanner validates the last (most recent) one;
        # earlier ones are returned as provenance and must never be removed.
        content = (
            "# Document\n\n"
            "∰ 20260101000000000\n\n"
            "More content...\n\n"
            "∰⏱🃏 20260724120000000\n"
        )
        f = tmp_path / "doc.md"
        f.write_text(content, encoding="utf-8")
        ok, witness, provenance = check_file_witness(f)
        assert ok is True
        assert "20260724120000000" in (witness or "")
        assert len(provenance) == 1
        assert "20260101000000000" in provenance[0]

    def test_invalid_timestamp_not_accepted(self, tmp_path):
        f = tmp_path / "doc.md"
        f.write_text("# Doc\n\n∰ 20261304999999999\n", encoding="utf-8")  # month 13
        ok, witness, _ = check_file_witness(f)
        assert ok is False

    def test_nonexistent_file_returns_false(self, tmp_path):
        ok, witness, provenance = check_file_witness(tmp_path / "ghost.md")
        assert ok is False
        assert witness is None
        assert provenance == []


# ---------------------------------------------------------------------------
# File iteration
# ---------------------------------------------------------------------------


class TestIterScannableFiles:
    def test_finds_md_txt_rst_py(self, tmp_path):
        (tmp_path / "a.md").write_text("a", encoding="utf-8")
        (tmp_path / "b.txt").write_text("b", encoding="utf-8")
        (tmp_path / "c.rst").write_text("c", encoding="utf-8")
        (tmp_path / "d.py").write_text("d", encoding="utf-8")
        (tmp_path / "e.yml").write_text("e", encoding="utf-8")  # not scanned
        found = list(iter_scannable_files(tmp_path))
        names = {p.name for p in found}
        assert names == {"a.md", "b.txt", "c.rst", "d.py"}

    def test_excludes_git_dir(self, tmp_path):
        git_dir = tmp_path / ".git"
        git_dir.mkdir()
        (git_dir / "config.md").write_text("x", encoding="utf-8")
        found = list(iter_scannable_files(tmp_path))
        assert not any(".git" in str(p) for p in found)

    def test_excludes_quepad(self, tmp_path):
        quepad = tmp_path / "quepad"
        quepad.mkdir()
        (quepad / "report.md").write_text("x", encoding="utf-8")
        found = list(iter_scannable_files(tmp_path))
        assert not any("quepad" in str(p) for p in found)

    def test_excludes_consolidated(self, tmp_path):
        c_dir = tmp_path / "_CONSOLIDATED"
        c_dir.mkdir()
        (c_dir / "doc.md").write_text("x", encoding="utf-8")
        found = list(iter_scannable_files(tmp_path))
        assert not any("_CONSOLIDATED" in str(p) for p in found)


# ---------------------------------------------------------------------------
# State management
# ---------------------------------------------------------------------------


class TestStateManagement:
    def test_load_state_empty_when_no_file(self, tmp_path, monkeypatch):
        import footer_witness

        monkeypatch.setattr(footer_witness, "STATE_FILE", tmp_path / "nonexistent.json")
        state = load_state()
        assert state["last_scan"] is None
        assert state["known_files"] == {}

    def test_save_and_load_roundtrip(self, tmp_path, monkeypatch):
        import footer_witness

        monkeypatch.setattr(footer_witness, "STATE_FILE", tmp_path / "state.json")
        monkeypatch.setattr(footer_witness, "QUEPAD_DIR", tmp_path)

        state = {
            "last_scan": "20260424024720123",
            "known_files": {"README.md": {"compliant": True, "witness": "∰ 20260424024720123"}},
        }
        save_state(state)
        loaded = load_state()
        assert loaded["last_scan"] == "20260424024720123"
        assert "README.md" in loaded["known_files"]

    def test_corrupt_state_file_returns_empty(self, tmp_path, monkeypatch):
        import footer_witness

        bad_file = tmp_path / "state.json"
        bad_file.write_text("{corrupt json{{", encoding="utf-8")
        monkeypatch.setattr(footer_witness, "STATE_FILE", bad_file)
        state = load_state()
        assert state["known_files"] == {}


# ---------------------------------------------------------------------------
# Report builders
# ---------------------------------------------------------------------------


class TestReportBuilders:
    _STAMP = "20260424024720123"

    def test_compliance_report_contains_symbol(self):
        report = build_compliance_report(
            [("docs/README.md", f"∰ {self._STAMP}")],
            ["docs/MISSING.md"],
            self._STAMP,
        )
        assert "∰" in report
        assert "README.md" in report
        assert "MISSING.md" in report

    def test_new_docs_report_flags_missing(self):
        report = build_new_docs_report([], ["new_doc.md"], self._STAMP)
        assert "new_doc.md" in report
        assert "ACTION REQUIRED" in report

    def test_flagged_report_lists_files(self):
        report = build_flagged_report(["alpha.md", "beta.txt"], self._STAMP)
        assert "alpha.md" in report
        assert "beta.txt" in report

    def test_flagged_report_empty_when_no_flags(self):
        report = build_flagged_report([], self._STAMP)
        assert "queue is clear" in report.lower() or "none" in report.lower()

    def test_egress_marker_contains_centesimal(self):
        summary = {
            "total": 10,
            "compliant": 8,
            "missing": 2,
            "new_compliant": 1,
            "new_missing": 1,
        }
        marker = build_egress_marker(self._STAMP, summary)
        assert "centesimal" in marker.lower() or "cmin" in marker.lower()
        assert "egressum-Q" in marker

    def test_egress_marker_carries_witness_stamp(self):
        summary = {"total": 1, "compliant": 1, "missing": 0, "new_compliant": 0, "new_missing": 0}
        marker = build_egress_marker(self._STAMP, summary)
        assert f"∰ {self._STAMP}" in marker

    def test_reports_carry_additive_note(self):
        for report in [
            build_compliance_report([], [], self._STAMP),
            build_new_docs_report([], [], self._STAMP),
            build_flagged_report([], self._STAMP),
        ]:
            assert "additive" in report.lower()


# ---------------------------------------------------------------------------
# Full scan integration
# ---------------------------------------------------------------------------


class TestScan:
    def _setup_quepad(self, tmp_path, monkeypatch):
        """Point module-level QUEPAD_DIR and STATE_FILE at tmp_path."""
        import footer_witness

        q = tmp_path / "quepad"
        q.mkdir()
        monkeypatch.setattr(footer_witness, "QUEPAD_DIR", q)
        monkeypatch.setattr(footer_witness, "STATE_FILE", q / "state.json")
        return q

    def test_scan_passes_with_all_compliant(self, tmp_path, monkeypatch):
        stamp = "20260424024720123"
        (tmp_path / "README.md").write_text(f"# Readme\n\n∰ {stamp}\n", encoding="utf-8")
        q = self._setup_quepad(tmp_path, monkeypatch)
        exit_code = scan(tmp_path, strict=True)
        assert exit_code == 0
        assert (q / "compliance_report.md").exists()

    def test_scan_fails_strict_with_missing_witness(self, tmp_path, monkeypatch):
        (tmp_path / "no_witness.md").write_text("# Doc\n\nNo witness here.\n", encoding="utf-8")
        self._setup_quepad(tmp_path, monkeypatch)
        exit_code = scan(tmp_path, strict=True)
        assert exit_code == 1

    def test_scan_non_strict_returns_zero_even_with_missing(self, tmp_path, monkeypatch):
        (tmp_path / "no_witness.md").write_text("# Doc\n\nNo witness here.\n", encoding="utf-8")
        self._setup_quepad(tmp_path, monkeypatch)
        exit_code = scan(tmp_path, strict=False)
        assert exit_code == 0

    def test_scan_produces_egress_marker(self, tmp_path, monkeypatch):
        (tmp_path / "README.md").write_text(
            "# Readme\n\n∰ 20260424024720123\n", encoding="utf-8"
        )
        q = self._setup_quepad(tmp_path, monkeypatch)
        scan(tmp_path)
        egress_files = list(q.glob("egressum-Q-*.md"))
        assert len(egress_files) == 1

    def test_scan_updates_state_json(self, tmp_path, monkeypatch):
        stamp = "20260424024720123"
        (tmp_path / "doc.md").write_text(f"# Doc\n\n∰ {stamp}\n", encoding="utf-8")
        q = self._setup_quepad(tmp_path, monkeypatch)
        scan(tmp_path)
        state = json.loads((q / "state.json").read_text(encoding="utf-8"))
        assert state["last_scan"] is not None
        assert "doc.md" in state["known_files"]

    def test_second_scan_treats_existing_files_as_known(self, tmp_path, monkeypatch):
        """After first scan, previously seen files should not appear as 'new missing'."""
        import footer_witness

        # File with no witness
        (tmp_path / "old.md").write_text("# Old\n\nNo witness.\n", encoding="utf-8")
        q = self._setup_quepad(tmp_path, monkeypatch)

        # First scan — old.md is new and missing → exit 1 in strict
        exit1 = scan(tmp_path, strict=True)
        assert exit1 == 1

        # Second scan — old.md is now known, no NEW missing files → exit 0 in strict
        exit2 = scan(tmp_path, strict=True)
        assert exit2 == 0

# ∰ 20260424000000000
