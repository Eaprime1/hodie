# MOAV CARRIERS

MOAV (Mother of All Vinegar) — transformation/fermentation path.

JSON carriers live here. Each carrier documents a formal transition —
in hodie's case so far, duplicate-content consolidation into
`eaprime1/duplicatus`: multiple copies of the same content found across
hodie, reduced to one surviving copy sent to duplicatus, with every
removed instance's unique data (original path, link, icon, any award)
preserved in the carrier rather than lost.

Naming convention: `hodie_moav_[event].json`; each carrier must include
its prima-clock stamp in the JSON payload. Adopted from custos's
`moav/README.md` convention.

## Existing Carriers

- hodie_moav_dedupe_prime02.json — first worked example, PRIME_02 dedupe candidate (4 redundant copies → 1 carbonite copy in duplicatus), 202608212008, CANDIDATE/OPEN, format approved by eaprime1 202608212020
- hodie_moav_dedupe_prime03.json — PRIME_03_Triadic_Stability.md dedupe candidate (4 redundant copies → 1 carbonite copy in duplicatus), 202608212026, CANDIDATE/OPEN
- hodie_moav_dedupe_prime05.json — PRIME_05_Quintessence_Amplification.md dedupe candidate (4 redundant copies → 1 carbonite copy in duplicatus), 202608212026, CANDIDATE/OPEN
- hodie_moav_dedupe_prime07.json — PRIME_07_Sacred_Completion.md dedupe candidate (4 redundant copies → 1 carbonite copy in duplicatus), 202608212026, CANDIDATE/OPEN
- hodie_moav_dedupe_prime11.json — PRIME_11_Architectural_Complexity.md dedupe candidate (4 redundant copies → 1 carbonite copy in duplicatus), 202608212026, CANDIDATE/OPEN
- hodie_moav_dedupe_prime13.json — PRIME_13_Complexity_Navigation.md dedupe candidate (4 redundant copies → 1 carbonite copy in duplicatus), 202608212026, CANDIDATE/OPEN
- hodie_moav_dedupe_prime17.json — PRIME_17_Heritage_Crystallization.md dedupe candidate (4 redundant copies → 1 carbonite copy in duplicatus), 202608212026, CANDIDATE/OPEN
- hodie_moav_dedupe_13_17_transition_framework_index.json — 13-17_transition_framework_index.md dedupe candidate (2 redundant copies → 1 carbonite copy in duplicatus), 202608212026, CANDIDATE/OPEN
- hodie_moav_dedupe_13_17_transition_part1_foundation.json — 13-17_transition_part1_foundation.md dedupe candidate (2 redundant copies → 1 carbonite copy in duplicatus), 202608212026, CANDIDATE/OPEN
- hodie_moav_dedupe_13_17_transition_part2_assessment.json — 13-17_transition_part2_assessment.md dedupe candidate (2 redundant copies → 1 carbonite copy in duplicatus), 202608212026, CANDIDATE/OPEN
- hodie_moav_dedupe_13_17_transition_part3_trajectory.json — 13-17_transition_part3_trajectory.md dedupe candidate (2 redundant copies → 1 carbonite copy in duplicatus), 202608212026, CANDIDATE/OPEN
- hodie_moav_dedupe_13_17_transition_part4_procedures.json — 13-17_transition_part4_procedures.md dedupe candidate (2 redundant copies → 1 carbonite copy in duplicatus), 202608212026, CANDIDATE/OPEN
- hodie_moav_dedupe_13_17_transition_part5_verification.json — 13-17_transition_part5_verification.md dedupe candidate (2 redundant copies → 1 carbonite copy in duplicatus), 202608212026, CANDIDATE/OPEN
- hodie_moav_dedupe_prime_project_survey.json — PRIME_PROJECT_SURVEY_20251211.md dedupe candidate (1 redundant copy → 1 carbonite copy in duplicatus), 202608212026, CANDIDATE/OPEN

All of the above are CANDIDATE/OPEN, not formally closed — eaprime1 approved
the *format* (per the PRIME_02 worked example) but has not yet reviewed each
individual consolidation. `duplicates_check/`, `PRIME_documents/`, and
`transition_frameworks/` are now fully resolved and removed from
`_CONSOLIDATED/` — everything they held is either the untouched canonical
copy still in `CODEX_documents/`, or a carbonite candidate in duplicatus.
