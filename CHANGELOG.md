# Changelog

All notable changes to this project are documented in this file.

## [Unreleased]

### Fixed
- Removed `f` prefix from two f-strings without interpolation in `crawler_pixel8/cli/main.py`
  (Codacy/pylint W1309 — `f-string-without-interpolation`).
- Added `googleapiclient` and its sub-modules to `.pylintrc` `ignored-modules` list so that
  optional Drive dependency import errors are suppressed correctly.

### Added
- `.codacy.yml`: Codacy configuration to exclude legacy/archived directories
  (`_CONSOLIDATED/`, `_SORTING/`, `_BOX_SIMULATION/`, `migrations/`) from analysis.
- `setup.cfg`: flake8 configuration matching the pylint scope and line-length settings,
  ensuring consistent lint behaviour across all tools.

### Changed
- `.gitignore`: Added `*.pdf`, `*.docx`, `*.pptx` and related document extensions to prevent
  binary document files from being committed (they belong in Google Drive).
- `README.md`: Updated with accurate structure, Quick Start section, grammar improvements,
  and a Prima Witness footer stamp.

### Resolved
- Pylint workflow failure on Python < 3.11 by implementing a compatibility path for pyproject.toml parsing.

### Changed (previous)
- Enhanced Pylint workflow with clearer reporting of lint results and robust score-gating enforcement.

## 2026-04-23

- Required `RUNNER_TEMP` to be set in pylint workflow temp file setup; removed silent
  fallback to `$TMPDIR`/`/tmp` so misconfigurations are caught immediately with a clear error.

## 2026-04-18

- Repaired pylint CI behavior to gate on configured `fail-under` score from `pyproject.toml`
  instead of failing on pylint's raw non-zero exit code when messages are present.
- Improved workflow diagnostics by requiring RUNNER_TEMP for temp file setup and printing parsed pylint score and threshold in job output.
- Fixed repository metadata by removing invalid gitlink entry `plexus (1)` that caused
  GitHub Actions post-job submodule cleanup warnings.
