# Changelog

All notable changes to this project are documented in this file.

## [Unreleased]

### Fixed
- Repaired the Pylint GitHub Actions workflow on Python 3.10 by removing a hard dependency on `tomllib` during `fail-under` parsing.

### Changed
- Upgraded Pylint workflow `fail-under` parsing to use a compatibility path: `tomllib` (3.11+), optional `tomli`, then a safe regex fallback from `pyproject.toml`.
- Preserved existing CI behavior: fatal/error lint exits still fail immediately, and score gating remains enforced by `tool.pylint.main.fail-under`.

## 2026-04-23

- Required `RUNNER_TEMP` to be set in pylint workflow temp file setup; removed silent
  fallback to `$TMPDIR`/`/tmp` so misconfigurations are caught immediately with a clear error.

## 2026-04-18

- Repaired pylint CI behavior to gate on configured `fail-under` score from `pyproject.toml`
  instead of failing on pylint's raw non-zero exit code when messages are present.
- Improved workflow diagnostics by requiring RUNNER_TEMP for temp file setup and printing parsed pylint score and threshold in job output.
- Fixed repository metadata by removing invalid gitlink entry `plexus (1)` that caused
  GitHub Actions post-job submodule cleanup warnings.
