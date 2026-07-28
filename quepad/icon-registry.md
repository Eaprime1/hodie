# Prima Witness — Icon Registry

Mapping of iteration icons used in ∰ witness lines.
Update this file to add new icons; the scanner reads it automatically.

| Icon | Name | Meaning |
|------|------|---------|
| ⏱ | Time / Ledger Arrival | Marks arrival in the daily ledger (Hodie) |
| 🃏 | Joker / Current Iteration | Marks the active iteration of a document |
| 🛠 | Tooling / Build | Applied to workflow, script, or build changes |
| 📋 | Documentation / Checklist | Applied to documentation or checklist documents |

## Usage

Icons are appended directly after ∰ with no space, before the timestamp:

```
∰⏱🃏 20260724054842000
```

A document accumulates one witness line per meaningful iteration.
The most recent line is the current witness; older lines are provenance.
Provenance lines must never be removed — they record the document's history.

## Icon assignment guide

- Add ⏱ when the document formally enters the ledger (first stamp or PR finalize)
- Add 🃏 on every active-iteration change (marks "I touched this in this session")
- Add 🛠 for workflow, Makefile, or infrastructure-only changes
- Add 📋 for README, checklist, or documentation-only changes

---
_quepad/ — Pad of Q, queue intake for the Prima Witness system_

∰⏱🃏 20260724120000000
