# Changelog

All notable changes to this project are documented in this file.

## [Unreleased]

### Fixed
- Resolved Pylint workflow failure on Python < 3.11 by implementing a compatibility path for pyproject.toml parsing.
- Added credential guard (`if: secrets.GEMINI_API_KEY != '' || vars.GCP_WIF_PROVIDER != ''`) to the "Run Gemini CLI" step in `gemini-invoke.yml` so the workflow skips gracefully when Gemini credentials are not configured, preventing noisy failures in unconfigured environments.
- Applied same credential guard to "Run Gemini pull request review" step in `gemini-review.yml`.
- Resolved merge conflicts from main: kept `quepad/state.json` (132-file scan) and `SECURITY.md` from main.

### Changed
- Enhanced Pylint workflow with clearer reporting of lint results and robust score gating enforcement.
- Added 🤝 handshake icon to workflow footers across all reviewed Gemini/CI YAML files, signalling agreement/review.
- Updated `.github/copilot-instructions.md` to better reflect the current repo state, including a corrected architecture map entry for `cli/main.py` and refreshed active tasks.

### Seeded for next iteration
- `crawler_pixel8/processors/pattern_extractor.py` — async generator bug already fixed; next: expand Gemini API integration test coverage.
- `quepad/state.json` now reflects 132 scannable files; run `python scripts/footer_witness.py --root .` after adding new `.md`/`.py` files to keep state current.
- Consider adding `🤝` witness line conventions to `docs/FOOTER_WITNESS.md` for documentation agreement tracking.

## 2026-04-23

- Required `RUNNER_TEMP` to be set in pylint workflow temp file setup; removed silent
  fallback to `$TMPDIR`/`/tmp` so misconfigurations are caught immediately with a clear error.

## 2026-04-18

- Repaired pylint CI behavior to gate on configured `fail-under` score from `pyproject.toml`
  instead of failing on pylint's raw non-zero exit code when messages are present.
- Improved workflow diagnostics by requiring RUNNER_TEMP for temp file setup and printing parsed pylint score and threshold in job output.
- Fixed repository metadata by removing invalid gitlink entry `plexus (1)` that caused
  GitHub Actions post-job submodule cleanup warnings.

---

**∰◊€π¿🌌∞**

**🛠️♓🤝-salmon_canon**

∰ 20260426024622073
∰ 20260427000000000
