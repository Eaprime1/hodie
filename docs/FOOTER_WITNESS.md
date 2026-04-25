# Footer Witness — Usage, Semantics & Design
∰ 20260424000000000

---

## Overview

The **Prima Witness** system ensures every document in the Hodie project carries
a `∰` footer witness stamp.  This stamp is the project's canonical proof of
a document's existence and provenance.

---

## Additive Semantics (Critical Invariant)

> **Documents carrying `∰` are additive, always additive.**

The `∰` marker represents **provenance accumulation** — not replacement, not
removal.  When a document receives a new witness stamp, the stamp is *added*
alongside any previous stamps.  Historical stamps must never be deleted.

This invariant is enforced at the workflow level: the scanner validates presence
of the witness, not uniqueness.  Multiple witness lines in a document are normal
and expected over a document's lifetime.

---

## Timestamp Format

Every `∰` occurrence in a document footer must be followed by a canonical
timestamp on the same line:

```
∰ YYYYMMDDHHMMSSMS
```

| Segment | Width | Description          | Example |
|---------|-------|----------------------|---------|
| YYYY    | 4     | Year                 | 2026    |
| MM      | 2     | Month (01–12)        | 04      |
| DD      | 2     | Day (01–31)          | 24      |
| HH      | 2     | Hour, 24 h (00–23)   | 02      |
| MM      | 2     | Minute (00–59)       | 47      |
| SS      | 2     | Second (00–59)       | 20      |
| MS      | 3     | Milliseconds (000–999)| 123    |

Total: **17 numeric digits**.

**Example footer witness line:**

```
∰ 20260424024720123
```

---

## Getting a Fresh Stamp

```bash
python scripts/footer_witness.py --stamp
```

Output:

```
∰ 20260424024720123
  centesimal: 1666.8056 cmin  (100-min clock)
```

---

## Where to Place the Witness

Place the `∰ YYYYMMDDHHMMSSMS` line in the **last 15 lines** of the file:

- **Markdown / RST / TXT** — a bare line at the end of the document:
  ```markdown
  ∰ 20260424024720123
  ```
- **Python** — as a comment at the end of the file:
  ```python
  # ∰ 20260424024720123
  ```

The scanner checks the final 15 lines of each file.

---

## Running the Scanner

```bash
# Scan current directory, produce quepad/ reports
python scripts/footer_witness.py --root .

# Strict mode — exit 1 if any new file is missing its witness
python scripts/footer_witness.py --root . --strict
```

---

## CI / GitHub Actions

The workflow `.github/workflows/footer-witness.yml` runs automatically on:

- **push** — when `.md`, `.txt`, `.rst`, or `.py` files change
- **pull_request** — same file paths
- **workflow_dispatch** — manual trigger

On each run, the scanner produces reports in `quepad/` which are uploaded as
workflow artifacts (`quepad-reports-{run_id}`).

If new files are missing the `∰` witness, the workflow **fails** and prints
the flagged-documents report.

---

## quepad / egressum-Q Reports

All reports are written to `quepad/` (Pad of Q):

| File | Description |
|------|-------------|
| `quepad/state.json` | Incremental state (known files + compliance) |
| `quepad/compliance_report.md` | Full compliance view |
| `quepad/new_docs_report.md` | Newly introduced documents |
| `quepad/flagged_report.md` | Files requiring `∰` witness (action required) |
| `quepad/egressum-Q-{stamp}.md` | Egress marker per scan cycle |

---

## Architecture Note — 100-Minute Clock

The project tracks the concept of a **100-minute (decimal/centesimal) clock**
for future timestamp display.

Standard wall-clock time uses **1 440 minutes/day** (24 h × 60 min).
The decimal clock divides the day into **1 000 centesimal minutes**
(10 centesimal hours × 100 centesimal minutes each).

Conversion formula:

```
centesimal_minutes = (HH × 3600 + MM × 60 + SS) / 86400 × 10000
```

Example: `02:47:20` UTC → `1 162.04…` centesimal minutes.

**Design decision:** Canonical witness stamps are always stored in standard
SI time (YYYYMMDDHHMMSSMS) for interoperability and future-proofing.
The centesimal conversion is performed at *display/reporting time only*
and is already included in each `egressum-Q` egress marker.

When an official decimal-time standard is formalised, the stored timestamps
will remain valid and only the display layer will need updating.

---

## Incremental State

The file `quepad/state.json` records all known files across scans, allowing
the scanner to distinguish **new** files from previously seen ones.

Committing `quepad/state.json` to the repository enables truly incremental
tracking: only newly introduced files will be flagged on subsequent runs.

If `state.json` is absent (e.g. first run or CI without cache), all files
are treated as new.

---

∰ 20260424000000000
