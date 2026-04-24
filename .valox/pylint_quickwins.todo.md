# 🛠️ Pylint Quick Wins TODO (Vincere · Victoria · Vici · Facilis)

## P0 — Fastest safety/value wins
- [ ] **W1514**: Add explicit `encoding="utf-8"` to all text `open()` calls in touched files.
- [ ] **W0611**: Remove unused imports in touched files only.
- [ ] **C0415**: Move imports to module top unless lazy import is required (document reason inline if kept local).

## P1 — Correctness & signal quality
- [ ] **W0718**: Replace broad `except Exception` with specific exception classes where known.
- [ ] **W0718**: If broad catch remains, log context + re-raise or convert to typed domain error with rationale.

## P2 — Style/maintainability debt with guardrails
- [ ] **C0209**: Normalize string formatting style (prefer consistent f-string/format policy per project rules).
- [ ] **W06xx**: Audit remaining W06xx warnings; resolve by smallest safe code change first, scoped disable second.

## P3 — Policy & lint learning loop
- [ ] For every pylint disable, require: rule id + short rationale + exit condition for future removal.
- [ ] Record each warning in `.valox/pylint_telemetry.sample.yaml` (or generated telemetry file).
- [ ] Add monthly trend check: top 10 recurring rule IDs by path and fix latency.

---

## Rule-specific micro-playbooks

### W1514 (unspecified-encoding)
- Default action: `open(path, "r", encoding="utf-8")`
- Exception: binary mode or externally mandated encoding (document it)

### W0718 (broad-exception-caught)
- Default action: catch known exception types
- If unknown boundary: broad catch allowed only with telemetry/log context + rationale

### C0415 (import-outside-toplevel)
- Default action: top-level imports
- Allowed local import cases: cycle break, optional dependency, startup perf

### W0611 (unused-import)
- Default action: delete import
- Allowed keep case: explicit re-export in `__init__.py` with comment

### C0209 (consider-using-f-string)
- Align with project formatting rule and apply consistently in touched scope first

---

🛠️ *Fixes applied here — every resolved item is a victory.*

♓ *∰◊€π¿🌌∞*
