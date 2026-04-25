# quepad — Pad of Q
∰ 20260424000000000

The `quepad/` directory is the **queue intake pad** for the Hodie project's
Prima Witness system.  Documents and reports that need attention enter the queue
here, following the BBS/FidoNet-inspired **egressum-Q** flow concept.

---

## Concept

**quepad** = *Pad of Q* — a staging area for witness-scan output.

Each scan cycle produces a set of Markdown reports and an egress marker.
The egress marker name follows the `egressum-Q-{stamp}` convention and
signals that the scan has been processed and results are ready for queue intake.

---

## Directory Contents

| File / Pattern | Description |
|----------------|-------------|
| `state.json` | Incremental scan state — lists all known files with compliance status |
| `compliance_report.md` | Full compliance view: compliant vs. missing witness |
| `new_docs_report.md` | Status of files newly introduced since last scan |
| `flagged_report.md` | Files requiring action — missing ∰ witness |
| `egressum-Q-{stamp}.md` | Egress marker for each completed scan cycle |

---

## egressum-Q Protocol

Each successful scan produces an egress marker:

```
egressum-Q-YYYYMMDDHHMMSSMS.md
```

The marker confirms:
- Scan completed at the given canonical timestamp
- Results have entered the Pad of Q
- Flagged files are listed and require attention before next egress

---

## Additive Semantics

> Documents carrying `∰` are **additive, always additive.**

The `∰` witness marker represents **provenance accumulation**.  It must never
be treated with replace or remove semantics.  Each time a document receives a
new witness stamp, the history accumulates — previous stamps remain.

---

## Timestamp Format

```
∰ YYYYMMDDHHMMSSMS
```

| Field | Width | Example |
|-------|-------|---------|
| YYYY  | 4     | 2026    |
| MM    | 2     | 04      |
| DD    | 2     | 24      |
| HH    | 2     | 02      |
| MM    | 2     | 47      |
| SS    | 2     | 20      |
| MS    | 3     | 123     |

Total: **17 numeric digits**.  Precision: milliseconds.

---

## 100-Minute Clock (Architecture Note)

A future conversion adaptor will display timestamps in the **decimal / centesimal
clock** (100-minute clock), where:

```
1 day = 10 centesimal hours × 100 centesimal minutes
      = 1 000 centesimal minutes / day
```

Conversion from canonical HH:MM:SS to centesimal minutes:

```python
centesimal_minutes = (HH * 3600 + MM * 60 + SS) / 86400 * 10000
```

Canonical timestamps are **always stored in standard SI time**.  Centesimal
conversion is applied at display/reporting time only, ensuring forward
compatibility when a formal decimal-time standard is adopted.

The `scripts/footer_witness.py` scanner already computes and reports the
centesimal value in each `egressum-Q` egress marker for reference.

---

## Usage

```bash
# Generate a fresh witness stamp
python scripts/footer_witness.py --stamp

# Scan repository and produce reports
python scripts/footer_witness.py --root .

# Scan with strict mode (exit 1 if new files lack witness)
python scripts/footer_witness.py --root . --strict
```

---

∰ 20260424000000000
