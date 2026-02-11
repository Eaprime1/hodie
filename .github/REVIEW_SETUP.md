# Code Review Setup

## Active Tools

### 1. Pylint (CI)
- **Workflow**: `.github/workflows/pylint.yml`
- **Config**: `.pylintrc`
- **Scope**: `crawler_pixel8/`, `redundancy_entity/` only
- **Triggers**: Push/PR with Python file changes

### 2. CodeRabbit (AI Reviews)
- **Config**: `.coderabbit.yaml`
- **Setup**: Install from [GitHub Marketplace](https://github.com/marketplace/coderabbit)
- **Cost**: Free for open source
- **What it does**: AI-powered PR reviews, suggests improvements, catches bugs

## Recommended Additions

### For This Project (Priority Order)

1. **Ruff** — Fast Python linter/formatter (replaces flake8, isort, black)
   - Much faster than pylint for CI
   - Can auto-fix issues
   - Add via: `.github/workflows/ruff.yml`

2. **Pre-commit.ci** — Runs pre-commit hooks in CI
   - Catches issues before review
   - Free for open source
   - Add `.pre-commit-config.yaml`

3. **Dependabot** — Dependency updates (when you add requirements.txt)
   - Auto-creates PRs for updates
   - Already available in GitHub settings

### Not Recommended Yet

- **SonarCloud**: Overkill for current project size
- **Codecov**: No test suite yet to measure coverage
- **Snyk**: No external dependencies to scan (Phase 1)

## Git Hooks (Local)

Already configured in `.githooks/`:
- **pre-commit**: Secret scanning, pylint on staged .py files
- **post-commit**: Logs to session notes

Install: `git config core.hooksPath .githooks`

## Issue Labels Suggestion

Consider adding these labels for the existing code review issues:
- `lint` — Pylint/style issues
- `security` — Secret/credential concerns
- `architecture` — Design decisions
- `performance` — Optimization opportunities
- `documentation` — Missing docs/comments
