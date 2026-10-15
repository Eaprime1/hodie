# Peer Swap — Form: hodie side (filled)

`prima-clock: 202610152233` (UTC; copied from custos `atelier/peer-swap/form-hodie-side.md` at `a8e9e41`, filled by hodie side)
`you hold: eaprime1/hodie · you are reading: eaprime1/custos`
`status: Sections A and B filled (Pass 1). C to F still blank; they fill in as the passes land.`

---

## A. Baseline — before you read anything

1. Where I am running: Claude Code in a cloud container (Sonnet 5.5), attached to a claude.ai Project named "custos".
2. What I can read: `eaprime1/custos` yes, but only branch `navigo-claude-hodie-custos` (shallow clone, one commit, `a8e9e41`) · `eaprime1/hodie` yes, `main` at `a834602` and the remote branch list.
3. What I can write: `eaprime1/hodie` by shell and git, branch `feature/peer-swap-hodie-side`. A dry-run push was accepted; a real push is proven only once it lands. Opening a PR is probably not possible from here (`gh` token invalid, no GitHub PR tool loaded); if so, Eric opens it from text I supply.
4. What I already knew about `eaprime1/custos` before Pass 1: the Project attached to this session carried custos's architecture, sibling repos, branch-tracker idea, vault, prima-clock and MOAV vocabulary. I had read none of the repo. See `pass1_hodie-reads-custos.md` section 0 for two further contaminations that happened during Pass 1.
5. What I already knew about `eaprime1/hodie`: `CLAUDE.md` and a top-level `ls`, nothing deeper.
6. Anything I cannot reach: custos branch `peer-swap/custos-side` (not on origin yet, so no custos letter); custos history, PRs, issues, CI runs and every branch but one; the Project's synced Google Docs (unopened); open PRs in either repo (`gh` broken).

---

## B. Pass 1 — cold read of `eaprime1/custos`

Full observations with citations are in `peer-swap/pass1_hodie-reads-custos.md` (frozen). Short answers:

1. In one sentence, what `eaprime1/custos` is for: a content-and-process repo (`CLAUDE.md`, "What This Repository Is") that holds the custody trail (`prima-clock/registry.md`, `moav/`, `vault/`) and the rules for how work is reviewed, sealed and merged.
2. Three things it does that I would have missed in my own repo:
   - Seal and merge are separated from authorship, with a gate that refuses footer-carrying and quoted cues (`CLAUDE.md` "Seal and merge"; `.github/workflows/finalize-pr.yml`).
   - A written observation per PR before the seal (`turns/observations/README.md`, `turns/observations/202610071031_pr431_observation.md`).
   - Exceptions recorded as rows, and staleness written down: `prima-clock/registry.md` row `202609251844`; "Not created" / "Stale" rows in `branch-tracker/branches.md`.
3. Three things that confused me: `device/` is "not on `main`" per `CLAUDE.md` yet exists here (C1); three naming schemes for the navigo role (C2); counts that disagree with the tree, 9 vs 25 workflows and 5 vs 13 carriers (C3). Also C4 and C5 in the pass file.
4. One thing it seems to promise that I cannot find evidence of: the vault as "the source of all copies" (`vault/README.md`). Looked in `vault/`, `vault/spade-of-aces/`, the registry suit column (one ♠️ row) and `branch-tracker/branches.md` (`∰custos` "Pending"). Found no entry that used it. I may have missed another branch.
5. With ten minutes, I would open `CLAUDE.md` first and `turns/observations/202610071031_pr431_observation.md` second: the first states the rules, the second shows them working on one PR.

**Through other eyes:** see section 8 of the pass file. Short form:

- The newcomer who has never seen either repo: the three-layer diagram and folder tree in `README.md` explain it fast; the vocabulary arrives before it is defined (unverified: I did not read `world/lore.md`).
- A contributor with no context, who wants to help today: a path exists (labelled issues, a bash completion check, claim by comment) with two Latin cues before work; I did not read `CONTRIBUTING.md`.
- The Shepherd on a tired day: `CLAUDE.md` and `turns/CLOSING.md` help; the newest log entry is at the bottom of 669 lines and two indexes lag the registry. I did not time a re-entry.
- The repo six months from now, if nothing changes (a guess): indexes lag more, `atelier/` and `pr-journeys/` grow, the vault stays empty.

**Lens (Quince):** unanswered. I found no definition of Quince; custos's own `atelier/halide/seeds/REVIEW-202610030124.md` says it is not in the repo.

---

## C. Pass 2 — deep dive of `eaprime1/hodie`

*Read your own repo with Pass 1 in hand. Do not edit Pass 1.*

1. The top-level folders of `eaprime1/hodie`, one line each: what is load-bearing, what is finished,
   what is unfinished: ____
   - `crawler_pixel8/` ____
   - `quanta/` ____
   - `moav/` ____
   - `_CONSOLIDATED/` ____
   - `.streams/`, `.locations/`, `.scripts/` ____
   - `redundancy_entity/`, `crawler_output/` ____
   - Anything top-level I did not list: ____
2. Where my Pass 1 was wrong or incomplete, now that I know my own repo better: ____
3. Things `eaprime1/hodie` does that `eaprime1/custos` would not guess: ____
4. The thing in `eaprime1/hodie` I would least like the peer to open, and why: ____
5. Did anything in my own repo change how I read Pass 1? If not, say so: ____

*Commit as `pass2_hodie-own-repo.md`, message starting `freeze:`.*

---

## D. Pass 3 — letter to `eaprime1/custos`

*Write the letter as its own file. Fill this block in first as the outline.*

1. What I saw in your repo that you may not see (up to five, each with a path): ____
2. What I would borrow from you:

| Item (path) | Tentative: adopt / adapt / decline | Why | Cost to my repo |
|---|---|---|---|
| ____ | ____ | ____ | ____ |
| ____ | ____ | ____ | ____ |
| ____ | ____ | ____ | ____ |

3. What I would ask you: ____
4. What I would warn you about before you borrow from mine: ____

*Commit as `pass3_letter_hodie-to-custos.md`, message starting `freeze:`.
Then check that the peer's letter is on origin before Pass 4.*

---

## E. Pass 4 — reply to the peer's letter

1. For each item in the peer's letter:

| Their item | adopt / adapt / decline | Reason | Where in my repo | Done in this PR, or follow-up |
|---|---|---|---|---|
| ____ | ____ | ____ | ____ | ____ |
| ____ | ____ | ____ | ____ | ____ |
| ____ | ____ | ____ | ____ | ____ |

2. Small adaptations made in this PR (paths): ____
3. Follow-ups named but not done: ____
4. What changed my mind, if anything: ____

### Hodie-side block

5. What in `hodie` is in a chain of custody, and what is not, as far as I can show with
   paths (not a full audit; a first honest sort): ____
6. Where a record of hodie's own entry into custody could live, and what I would need from
   custos to write it: ____
7. Hodie's prima-clock stamp (**Eric sets this; leave blank until he gives it**): ____
8. One thing custos does that hodie's workflows do not, and what it would cost to match
   (for example, review runs on every push versus once when ready): ____

---

## F. Ready for oversight

- [ ] All four passes committed; Passes 1 to 3 frozen
- [ ] This form complete; unanswered blanks marked and explained
- [ ] My repo's own scan run: ____ (result)
- [ ] PR description follows my repo's template; PR marked ready for review
- [ ] One comment posted in words saying the PR is ready, and what is left open
- [ ] I have not sealed, merged, or edited the peer repo

---

∰◊€π¿🌌∞

∰ 20261015223334000 — form (A, B filled) first witness
