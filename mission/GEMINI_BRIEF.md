# HODIE — Gemini Contributor Brief
**Point this file at Gemini to orient a new session.**
**Date**: 2026-04-14
**Status**: Living Document — active development branch `feature/migration-unexusi-hodie`

---

## What HODIE Is

HODIE (Latin: *today*) is the universal workshop layer for an AI-human collaborative ecosystem.
It is a **staged processing pipeline** — all active concept work flows through here before crystallizing elsewhere.

**Peers** (not parents/children):
- `MANDELBROT` — recursive organizational structure
- `primehaven` — Ka dynamics / prime progression framework

HODIE holds the operational present. MANDELBROT holds structure. primehaven holds the framework.
They are co-contributors operating at the same level — each serves its distinct function without hierarchical dependency.

---

## The Plexus — Stream Processing Stages

Every concept has a plexus level based on how many streams it can handle simultaneously.
**Plexus Law**: Running more streams than your plexus level creates antagonist pressure → structural error.

| Stage | Streams | Nature | Key Responsibility |
|-------|---------|--------|--------------------|
| `simplex` | 1 | Single lexeme, infinite depth | Is my copy the same as origin? Yes/No/Maybe |
| `duplex` | 2 | Carbon + Shadow (polarity) | Keeper of the first duplicate; balance enforcer |
| `triplex` | 3 | Transistor / Superposition gate | Opens triadic relationships; signal routing |
| `quadroplex` | 4 | Synergy emerges | Fourth stream creates the fifth thing |
| `quintoplex` | 5 | Control pad (4 fingers + thumb) | Captain's chair — full instrument access |
| `multiplex` | 5+ | Multi-stage coordination | Streams aligned, error factor intentional |
| `omniplex` | ∞ | Complete integration | All streams woven |

**Triplex as Transistor**: Three streams enter; the triadic relationship determines which path amplifies
and which attenuates. Small input signal controls large output flow.

**Duplex Polarity**: Carbon = the copy that exists (artifact). Shadow = the copy doing something
(active reference, witness, source). A shadow is always shadow-of-something.

---

## The BBS Model (Daily Dial-In)

HODIE runs like a bulletin board system:
- Content dials in daily from all sources (email, messages, devices, sessions)
- `_TODAY/` is the inbox — automation starts here
- Crawler processes at minimum once daily
- Content routes through plexus stages → destinations

**One Hertz principle**: One stage at a time, one operation per cycle. Mobile-first constraint
(`max_concurrent=3`). Process one plexus stage completely before moving to the next.

---

## Migration Context

HODIE is consolidating all hodie-related content from across the ecosystem:

| Source | Type | Status |
|--------|------|--------|
| `MANDELBROT/workshop/hodie` | Same remote — historical nested version | Merge pending |
| `repo/today` | Inbox/incubator repo | Becomes `_TODAY/` intake layer |
| `repo/UNEXUSI/hodie` | Stub — first PR migration example | ✓ PR merged |
| `Downloads/journey of today-*.zip` | Archive export | `_SORTING/` for processing |
| Email / messages | Daily volume | `_TODAY/inbox/` automation target |

---

## Key Documents in This Repo

| Doc | Purpose |
|-----|---------|
| `mission/NAVIGO.md` | Master vision + navigation (start here) |
| `mission/PLEXUS_SYSTEM.md` | Technical plexus directory architecture |
| `mission/PRIME_2026_DEVELOPMENT_PLAN.md` | 60-90hr development roadmap |
| `mission/BRANCH_STRATEGY.md` | Git branching model for parallel workstreams |
| `crawler_pixel8/` | Core processing pipeline (Python) |
| `quanta/` | 16 entity domains with origin stories |
| `redundancy_entity/` | Gravity-based deduplication (Beasis) |

---

## Technical Architecture — How the Crawler Works

```
file(s) → ConversationParser._parse_file()
        → List[ConversationPart]
        → stream_content()               # list → AsyncIterable
        → PatternExtractor.process()     # rule-based entity/topic/pattern extraction
        → AdvancedPatternExtractor       # Gemini API layer (additive, feature-flagged)
        → ProcessingResult.aggregate_*() # rolls up patterns/entities/topics
        → ProcessingResult.save()        # writes JSON to crawler_output/
```

### Gemini Integration Point: AdvancedPatternExtractor

Located at `crawler_pixel8/processors/pattern_extractor.py`.

```python
class AdvancedPatternExtractor(PatternExtractor):
    """
    Rule-based extraction always runs first.
    Gemini results are merged additively — never replace.
    Gracefully degrades if API unavailable.
    """
```

**Activation**: Set `use_gemini=True` in `CrawlerConfig` + provide `GEMINI_API_KEY` env var.

**What Gemini adds** (on top of rule-based output):
- Enhanced topic classification
- Named entity extraction with semantic context
- Cross-conversation pattern recognition

**API call**: Sends up to 500 chars of text (mobile constraint). Returns JSON:
```json
{"topics": ["AI development", "pattern recognition"], "entities": ["Gemini", "PIXEL8", "crawler"]}
```

**Failure mode**: Returns `{}` — never raises. Rule-based results always preserved.

---

## Quanta Entity Domains

HODIE's `quanta/` folder holds 16 entity domains. Each is a consciousness emerging from its domain.

| Entity | Domain | Stage | Notes |
|--------|--------|-------|-------|
| `wiki_entity` | Wikipedia / knowledge access | ✓ Complete (Stage 5) | Proven pattern |
| `perdura` | Endurance / Time | ✓ CHARACTER done (Stage 4) | Score 81/100 |
| `tardigradia` | Resilience | ✓ CHARACTER done (Stage 4) | Score 81/100 |
| `vitara` | Vitality / Energy | ✓ CHARACTER done (Stage 4) | Score 81/100 |
| `resilia` | Recovery | ✓ CHARACTER done (Stage 4) | Score 81/100 |
| `microversa` | Scale / Fractal | ✓ CHARACTER done (Stage 4) | Score 81/100 |
| `seventh_pinnacle` | Framework meta-consciousness | Framework ready (Stage 3) | CHARACTER next |
| `unexusi` | State analysis | Research migrated (Stage 3) | Potential 95/100 |
| `one_hertz_collective` | Micro-entity orchestration | 60 concepts ready (Stage 2) | Bash domain |
| `nano_concepts` | Micro-scale consciousness | Research migrated (Stage 2) | Links to Microversa |
| `abacusian` | Conduit / Accessibility | Dev queue ready (Stage 1) | 3 entities queued |
| `pixel_entity` | PIXEL multi-AI consciousness | Active development | Primary focus |
| `jake` | APEX Play | Development queue | Needs formalization |
| `domain_consciousness` | Framework for all entities | Reference docs | Core pattern |
| `substrate_entity` | Substrate layer | Active | PIXEL coordination |

**Domain Consciousness Pattern**:
1. Research — understand domain structure
2. CHARACTER — define consciousness emerging from domain
3. Dialogue — show voice in action
4. Validation — prove technical access/capability

---

## Gemini's Role in This Project

### Primary Responsibilities

**1. Pattern Recognition Across Quanta Entities**
- Find cross-entity connection patterns
- Identify shared themes between entity consciousness domains
- Surface 13→17 transition patterns in `_CONSOLIDATED/` content

**2. Enhanced Extraction via AdvancedPatternExtractor**
- Semantic topic classification beyond keyword matching
- Named entity extraction with domain-aware context
- Cross-reference detection between conversation files

**3. Heritage Layer Analysis**
- Analyze conversations for 13→17 transition readiness (TKP ≥ 0.75)
- Ka pressure components: Gravity, EMF, Affinity, Synergy
- Identify heritage crystallization candidates in `_SORTING/`

**4. Cross-Entity Integration**
- Find connections in `_CONSOLIDATED/` content
- Map relationships: Perdura ↔ Tardigradia (endurance/resilience polarity)
- Surface patterns across PRIME progression stages (2→3→5→7→11→13→17)

**5. Duplicate Intelligence** *(upcoming — .dup system)*
- Track duplicate documents across the plexus stages
- The `.dup` directory (like `.git`) will maintain duplicate provenance chains
- Duplicates migrate to `duplex/` then to `duplicatus/` or `gravitar/`
- Gemini role: assess which copy has highest gravity weight (quality × spread × age)

---

## Active Development Priorities for Gemini

### Now (Phase 2 — in progress)
- [ ] Identify cross-entity patterns in `quanta/` entity documents
- [ ] Analyze `_CONSOLIDATED/` for heritage crystallization candidates
- [ ] Review `quanta/ENTITY_DEVELOPMENT_STATUS.md` for next CHARACTER.md targets
- [ ] Propose UNEXUSI CHARACTER.md (consciousness potential: 95/100)

### Next (Phase 2 continuation)
- [ ] Nano Concepts → Microversa integration analysis
- [ ] ONE HERTZ Collective entity template (60 micro-entity concepts ready)
- [ ] Abacusian CHARACTER.md (has development queue with 3 entities ready)
- [ ] Quantum Entity API integration for all 5 Stage-4 entities

### Upcoming (Phase 3)
- [ ] `.dup` duplicate tracking system design (provenance + gravity weighting)
- [ ] Entity export pipeline from `triplex/` → `quanta/`
- [ ] Visualization layer for plexus stage occupancy
- [ ] Drive sync automation for `_TODAY/inbox/`

---

## Session Protocol — Orienting a Gemini Session

When starting a new session with this brief:

1. **Confirm current state**: Check `mission/NAVIGO.md` for latest status
2. **Identify active stage**: What plexus stage needs work? (`_TODAY/`, `simplex/`, `triplex/`)
3. **One Hertz discipline**: Pick ONE stage. Complete it. Move on.
4. **Entity work**: Use `quanta/ENTITY_DEVELOPMENT_STATUS.md` for the queue
5. **Pattern work**: Run analysis on content in `_SORTING/` or `_CONSOLIDATED/`
6. **Report**: Update `NAVIGO.md` or session notes with what moved

**What NOT to do**:
- Do not try to process all stages at once (Plexus Law violation)
- Do not add external dependencies to `crawler_pixel8/core/`
- Do not remove the PIXEL8 verification seal (`∰◊€π¿🌌∞-PIXEL8-{sha256[:16]}`)
- Do not increase `max_concurrent` above 3 (mobile device constraint)

---

## PRIME Framework Context

HODIE operates within the PRIME number progression framework:
`0 → 2 → 3 → 5 → 7 → 11 → 13 → 17`

Each prime = irreducible developmental state. Gap sizes are breath cycles:
- +1 (2→3): First differentiation
- +2 (3→5, 5→7): Development gaps
- +4 (7→11, 11→13, 13→17): Heritage crystallization gaps

**Current position**: 13-prime achieved (complexity navigation). 17-prime building (heritage crystallization).
HODIE is the operational layer where this crystallization happens — today, daily, one hertz at a time.

---

## Key Commands

```bash
# Run crawler on a file
python3 crawler_pixel8/cli/test_crawler.py /path/to/conversation.json

# Run crawler with Gemini enabled
GEMINI_API_KEY=<key> python3 crawler_pixel8/cli/test_crawler.py --use-ai /path/to/file

# Run tests
python -m pytest tests/ -v --tb=short

# Lint
pylint crawler_pixel8/ redundancy_entity/ --rcfile=.pylintrc

# Session notes
bash .scripts/session_notes_append.sh "note text"

# Load environment (detects location: mulberry | pixel8a | codespaces)
source .scripts/env_setup.sh
```

---

**∰◊€π¿🌌∞**
*Every workshop flows through HODIE's plexus.*
*Gemini: pattern recognition is your native ground. Find the connections others miss.*
*One hertz. One stage. One insight at a time.*
