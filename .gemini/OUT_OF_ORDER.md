# Out of order: the Gemini review workflows

`prima-clock: 202610160141` (UTC) · placed by Claude (Sonnet 5.5), at the Shepherd's word (Eric, 2026-10-15)

**Hello, Gemini, and thank you for the reviews so far.** These four workflows are switched off for now.
Nothing is broken on your side that we know of; the switch is a pause, and Eric would like you to put it right
when you are next here.

## What is switched off

The four files were renamed, not deleted. GitHub only runs `.yml` and `.yaml` files, so the new
`.yml.disabled` ending stops them and keeps every line.

| Was | Now |
|---|---|
| `.github/workflows/gemini-dispatch.yml` | `.github/workflows/gemini-dispatch.yml.disabled` |
| `.github/workflows/gemini-review.yml` | `.github/workflows/gemini-review.yml.disabled` |
| `.github/workflows/gemini-triage.yml` | `.github/workflows/gemini-triage.yml.disabled` |
| `.github/workflows/gemini-invoke.yml` | `.github/workflows/gemini-invoke.yml.disabled` |

## Why

- **Observed:** each of the four ran on every push to every branch and failed with zero jobs. That is the pattern
  GitHub shows when it rejects a workflow file. They also failed on `main`; the earliest failure I found is
  2026-08-22 (`2026-08-22T03:05:59Z`, branch `main`), well before the peer swap that surfaced them.
- **Observed:** the YAML in all four files parses, and `gemini-dispatch.yml` has no `push` trigger, so the
  push-time failures are not from its own `on:` block.
- **Reported, not checked:** Eric says the Gemini code-review setup changed upstream. I could not confirm that from
  the API. I could not read GitHub's own error text for the failed runs (the API does not return it), so **the real
  cause is unknown**.
- Each failing push added four red marks to every PR.

## What to check when you fix it

1. Open one old failed run in the Actions tab and read the "workflow file issue" message. That is the real cause.
2. Compare the files against the current upstream Gemini CLI workflow templates (`google-github-actions/run-gemini-cli`).
   The files pin that action at `@v0`.
3. The three called workflows (`gemini-review`, `gemini-triage`, `gemini-invoke`) use `workflow_call`; `dispatch` calls them
   with `secrets: inherit`. Check the permissions block on each call against what the called workflow asks for.
4. The credential guard added in the earlier merge (`CHANGELOG.md`, "Unreleased") is on `gemini-review.yml` and
   `gemini-invoke.yml`; keep it.
5. `secrets.GEMINI_API_KEY` must still exist, or the guard will skip the step.

## How to switch them back on

```bash
cd .github/workflows
for f in dispatch invoke review triage; do git mv gemini-$f.yml.disabled gemini-$f.yml; done
```

Then update the **Gemini Review** lines in `CLAUDE.md` (they now say the workflows are paused) and remove this notice.

## What else changes while they are off

- `@gemini-cli review`, `triage` and other comment commands do nothing.
- `sovran-voice.yml` has a code comment that says `gemini-review.yml` posts a full AI review on the same event. That
  is true only when the workflow is on. The comment is left as it was.
- Claude Code Review (`claude-code-review.yml`) and Codacy are unchanged.

With thanks, and with no hurry.

---

∰◊€π¿🌌∞

∰ 20261016014103236
