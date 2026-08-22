# wellspring queue

Ordered list of what's currently waiting. One entry per item; remove the
entry (and the file, if applicable) once it's been reviewed and disposed of.

---

## 1. Root-level PDFs (7 files)

**Arrived**: 2026-08-21, via hodie cleanup pass
**Source**: sitting directly in repo root, no subfolder
**Why here**: not duplicates of anything else in the repo (confirmed distinct
md5 hashes across all 7), and not referenced by name in any root `.md` doc —
a tidiness question, not a dedup one. No existing folder in hodie is an
obvious fit, so they wait here rather than getting a folder invented for
them or staying loose in root.
**Status**: waiting for review
**Destination**: TBD — pending eaprime1 review of each file's actual content

| File | Size |
|---|---|
| `Automated Prime Progression Gateway.pdf` | 105K |
| `Oper.pdf` | 134K |
| `pinn_other.pdf` | 44K |
| `pinnref.pdf` | 41K |
| `pinn_workflow.pdf` | 42K |
| `pinref.pdf` | 300K |
| `thehodie.pdf` | 230K |

---

## 2. Temphold_needs_review/ (89 files, ~9.3M)

**Arrived**: 2026-08-21, via hodie cleanup pass — moved whole from
`_CONSOLIDATED/CODEX_documents/Temphold/`
**Source**: raw PDF exports, mostly named `Copy of Untitled document-N.pdf`,
apparently a Google Drive dump of printed/exported Claude.ai conversations
**Why here**: sampled 2 of 89 (files `-1` and `-45`). They are NOT
interchangeable duplicates or disposable debris — one was a completely
unrelated personal D&D character-roleplay conversation, the other was
on-topic "SDWG Visionary" project chat content (Quantum-Runic math, legacy
document consolidation). The folder is a genuine mixed bag spanning
unrelated topics and possibly-personal content, so filename pattern alone
can't be used to bulk-delete or bulk-classify it, and it isn't this cleanup
pass's place to make that call file-by-file. Moved intact, nothing deleted,
nothing else opened beyond the 2-file sample.
**Status**: waiting for eaprime1 review (whole folder, not yet triaged item
by item)
**Destination**: TBD per-file — likely a mix of "fold into canonical CODEX
content" (SDWG-relevant material), "unrelated, route elsewhere or discard"
(non-project personal content like the D&D file), and possibly more
duplicates of already-canonical content once actually read

---

## 3. CODEX_fragments_needs_review/ (16 files)

**Arrived**: 2026-08-21, via hodie cleanup pass — moved from loose files
sitting in `_CONSOLIDATED/CODEX_documents/` root, named after their opening
words/characters (`Absolutely,.txt`, `Certainly!.txt`, `{.txt`, `#.txt`,
two files literally named after shebang lines, etc.)
**Source**: raw pasted chat-response and code fragments — Quantum-Runic
framework discussion, a QuantumDice class, a directory-structure generator,
a bash "ONE HERTZ INSTALLER" script, a Termux game engine core
(`sacred_empire_core.py`), an unrelated `sudo apt install brave-browser`
snippet
**Why here**: read all 16 in full before deciding anything (learned from
the Temphold folder not to trust filenames). Checked each for content
overlap against canonical `CODEX_documents/` files (grepped distinctive
class names/strings — `QuantumDice`, `prime_codex_v2`, `CrystalAllocation`,
the brave-browser keyring URL) — none found elsewhere, so none are
confirmed-redundant duplicates safe to delete. All are genuine, on-topic
project material (no personal/unrelated content like Temphold had), just
never titled or integrated anywhere.
**Status**: waiting for eaprime1 review
**Destination**: TBD — likely folding each into the relevant canonical doc
or a proper new file with a real name, once reviewed
