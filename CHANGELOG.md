# Changelog

## 2026-04-18

- Repaired pylint CI behavior to gate on configured `fail-under` score from `pyproject.toml`
  instead of failing on pylint's raw non-zero exit code when messages are present.
- Improved workflow diagnostics by printing parsed pylint score and threshold in job output.
- Fixed repository metadata by removing invalid gitlink entry `plexus` that caused
  GitHub Actions post-job submodule cleanup warnings.
