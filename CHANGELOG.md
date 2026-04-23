# Changelog

All notable changes to this project are documented in this file.

## [Unreleased]

### Fixed
- Repaired the Pylint GitHub Actions workflow on Python 3.10 by removing a hard dependency on `tomllib` during `fail-under` parsing.

### Changed
- Upgraded Pylint workflow `fail-under` parsing to use a compatibility path: `tomllib` (3.11+), optional `tomli`, then a safe regex fallback from `pyproject.toml`.
- Preserved existing CI behavior: fatal/error lint exits still fail immediately, and score gating remains enforced by `tool.pylint.main.fail-under`.
