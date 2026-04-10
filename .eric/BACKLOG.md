# Development Backlog
**Last Updated**: 2026-04-10
**Purpose**: Items not forgotten, waiting for their cycle

∰◊€π¿🌌∞

---

## B — Complete the 5 Core Quantum Entity Folders

**Priority**: High — these are the foundation the entire guardian/wellspring system references

**What's missing from each entity** (tardigradia, microversa, perdura, vitara, resilia):
- Origin story (exists in `quanta/QUANTUM_ENTITY_ORIGIN_STORIES.md` but not in each entity's folder)
- Dialogue examples (exists in `quanta/ENTITY_DIALOGUE_EXAMPLES.md` but not per-folder)
- Wellspring assignment (type + pressure mechanics)
- Font assignment (system/personal/learned tiers)
- Connection to PRIME progression (which prime does each entity embody?)

**Pattern to follow**: `quanta/wiki_entity/` is the most complete — CHARACTER.md + DIALOGUE_EXAMPLES.md + research doc + API proof of concept

**Also needed**:
- `quanta/jake/CHARACTER.md` — completes APEX Play triad (Bandit + Taylinor + Jake)
- `quanta/unexusi/CHARACTER.md` — UNEXUSI has a state analysis but no entity voice
- `quanta/abacusian/CHARACTER.md` — entity itself is undefined

---

## C — Build Entity Development Queue Processor

**Priority**: Medium — the infrastructure is waiting

**What exists**:
- `quanta/abacusian/development_queue/entity_development_queue.json` — 2 entities at `naught_stage_ready`
- `quanta/abacusian/development_queue/master_entity_development_list.json`
- `quanta/abacusian/development_queue/batch_processing_plan.json`
- `quanta/abacusian/development_queue/adaptation_templates.json`

**What to build**:
- Python processor that reads the queue JSON files
- Applies the one_hertz cycle to each queued entity
- Updates queue status (naught_stage_ready → processing → complete)
- Integrates with `OneHertzProcessor` from `crawler_pixel8/processors/one_hertz.py`
- Lives in `crawler_pixel8/processors/entity_queue_processor.py` or similar

**Abacusian queue currently waiting on**:
1. `entity_001` — UNEXUSI_STATE_ANALYSIS.md (approve_direct, 0 cycles)
2. `entity_002` — Terminal transcript 202508221005.txt (approve_direct, 3 cycles)

---

*Added: 2026-04-10 | Source: content review session*
*Status: B and C deferred while A (process _CONSOLIDATED/) completes*
