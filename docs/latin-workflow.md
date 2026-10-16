# Latin Workflow in Hodie

**Prima-clock:** 202610161320
**Suit:** ♦️ Diamond, 1/3 plank. Ported from custos (`docs/latin-workflow-v2.md`, `latin-workflow-glossary.md`).
**Quick reference:** [`latin-lexemes.txt`](latin-lexemes.txt), plain text

A call names the stage of the work, so a contributor knows what kind of answer is wanted without a
paragraph of explanation. Hodie and custos share the same words. Custos is the source for the full
text; this page lists what hodie uses.

## A call has two parts

An **action** names the work. A **modifier** names its scope or tempo. A call is a request for a stage
of work, not proof that the stage passed.

| Action | Means |
|---|---|
| `recensio` | Review. Scan, find, fix. |
| `probatio` | The soft seal: the work states it is ready for oversight. |
| `lustratio` | Polish. How it reads, not what it does. |
| `judicium` | Stop. Options and a recommendation. Wait for the owner. |
| `novissimum` | Rear guard. Close loose ends or file them. |
| `cursus` | Run the remaining stages in order. |
| `emenda` | Amend what oversight flagged. Editing, not blame. |

| Modifier | Means |
|---|---|
| `prima` | First. Orient, change nothing. |
| `ultima` | Final. No new scope. |
| `suprema` | Highest. Presentation. Use sparingly. |
| `extrema` | Deepest. Root cause, with evidence. |
| `renovata` | Refresh. May stand alone. |
| `expeditus` | Prompt. Focused, with the same standards. |

## How to call

| Form | Reaches |
|---|---|
| `^name cue words` | One contributor. |
| `^name set-4f2a1c cue words` | One conversation of that contributor. |
| `^omnes cue words` | Every contributor, each from its own seat. |
| `^cuncti cue words` | The project as a whole. Read it first, then add your own view. |
| `^hodie cue words` | The hodie workflows. |

The names are `claude`, `chatgpt`, `gemini`, `perplexity`, `unexusi`, `custos`, `hodie`, `omnes` and
`cuncti`. A cue counts only at the start of a line, outside quotes and code, from the owner, and in a
comment without the Claude Code footer. `.github/scripts/cue-parser.js` holds those rules, and
`scripts/test_cue_parser.js` tests them.

## What hodie reads today

| Cue | Read by | Effect |
|---|---|---|
| `@claude finalize` | `finalize-pr.yml` | Seals the PR if the template, threads and CI pass. |
| `@claude ultima probatio` | `finalize-pr.yml` | The same seal, in the Latin wording. |
| any other call | nothing | Words for the conversation. No workflow acts on them. |

The footer and quote guards apply to both seal cues. `scripts/test_finalize_gate.sh` tests them.
A call is a mode, not a keyword: `@claude ultima recensio … to finalize` does not seal, because the
sentence does not say `finalize` right after `@claude`.

## The road of a PR

| Step | Who | Cue | What happens |
|---|---|---|---|
| 1 | Contributor | (opens the PR ready) | The first witness. |
| 2 | Contributor | `recensio`, `ultima recensio` | Reviews its own PR and fixes what it finds. |
| 3 | Shepherd | `probatio` | Soft seal. In hodie this is a conversation call; no label is set yet. |
| 4 | Shepherd | `@claude finalize` or `ultima probatio` | The seal. Owner only. |
| 5 | Shepherd | the `final-oversight` label, then the approval | Report only (`final-oversight.md`). |
| 6 | Shepherd | `emenda` | Asks the contributor to repair a flag. A fix is a new head and needs a new seal. |
| 7 | Shepherd | says so in the conversation | Merge, by merge commit. |

A contributor never seals, never merges and never answers a cue meant for another name.

## Not in hodie yet

These exist in custos and are not ported. Each is a separate swap.

- The soft-seal label: `probatio-label.yml` sets `ready-for-oversight` on the owner's `^name probatio`.
- The cue record: `latin-cue-record.yml` logs each call with the PR's state.
- The check-in cues `disponi`, `petitio` and `placet`, which run the mission board.
- The observation document before the seal.

## The seed block for a conversation

Paste this as the first message of a new conversation. The grammar is the same as in custos.

```text
We work with the Latin workflow calls (hodie: docs/latin-workflow.md).
A call names the stage of this conversation. When I use one, answer in its mode:

PRIMA RECENSIO — orient. Read what I've given you, then tell me where things
  stand and what's open. Don't start the work yet.
RECENSIO — the working scan. Find issues, recommend fixes, do the work asked.
EXTREMA RECENSIO — one thing, to the bottom. Show evidence.
JUDICIUM — a decision only I can make. Stop. Give me the options, your
  recommendation and what each choice changes. Don't act until I rule.
ULTIMA RECENSIO — the final review. Fix everything found. No new scope.
LUSTRATIO — polish for presentation. Change how it reads, not what it does.
SUPREMA LUSTRATIO — a brief someone else can act on without this conversation.
NOVISSIMUM — the rear guard. Close loose ends, file open questions, say what is
  carried forward.
EMENDA — amend what was flagged. One line per flag: fixed (with the commit),
  not a defect (with the path you traced), or carried forward (with an owner).
RENOVATA — refresh. Re-read the work on its current state and say what changed.
PROBATIO — the soft seal. Say whether the work is ready for oversight, or what
  blocks it. You do not seal.
ULTIMA PROBATIO — the seal. Write the closing record, confirm everything landed,
  then stop. New work opens a new conversation.

A call may be addressed. "^omnes <call>" is for every contributor. "^cuncti <call>"
is for the project as a whole: read the whole first, then add your own view.
"^<your name> <call>" is for you alone; answer "not mine" in one line if it
names someone else.

If a call is unclear, say how you are reading it before acting.
```

---

∰ 20261016132010000
