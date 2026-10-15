# Peer Swap — Form: hodie side

`prima-clock: 202610152136` (UTC, form version; stamp your own passes when you file them)
`you hold: eaprime1/hodie · you are reading: eaprime1/custos`
`form: fill-in-the-blank. Blanks are ____. Leave a blank unanswered rather than invent, and say why.`

*Answer in your own words. Two or three lines is usually enough. If a question does not fit
what you found, say so and move on.*

---

## A. Baseline — before you read anything

1. Where I am running (claude.ai project / Claude Code / other): Claude Code cloud session,
   attached to the claude.ai Project "HODIE". Shell, file tools, no PR-opening tool seen.
2. What I can read: `eaprime1/custos` yes: anonymous shallow clone (depth 1) of branch
   `navigo-claude-hodie-custos` at `a8e9e41`; no history, other branches, PRs or LFS ·
   `eaprime1/hodie` yes: shallow clone of `main` at `a834602`.
3. What I can write: `eaprime1/hodie` attached with push access. Branch
   `feature/peer-swap-hodie-side` created locally; push and PR creation were untested when this
   was written (`gh auth status` reported a failed GH_TOKEN login).
4. What I already know about `eaprime1/custos` before Pass 1, honestly: a vague impression of it
   as a system-management tool, which I discounted, and its `CLAUDE.md`, which loaded
   automatically before Pass 1 began. Nothing else.
5. What I already know about `eaprime1/hodie`: its `CLAUDE.md` and a top-level listing. Nothing
   else was read before Pass 1.
6. Anything I cannot reach, stated plainly: custos history, other custos branches, PRs, issues,
   CI and Codacy results; any write to custos; `atelier/peer-swap/intro-hodie-side.md` (not on my
   reading list, unread).

*If you cannot read `eaprime1/custos`, stop here and tell Eric.* (I can.)

---

## B. Pass 1 — cold read of `eaprime1/custos`

*Full observations, with a path or commit for each, are in `pass1_hodie-reads-custos.md`
(O-1 to O-29). The answers below point into it.*

1. In one sentence, what `eaprime1/custos` is for: tending and recording the work that arrives
   from many sources, as a story-world repo with a custody trail (O-1, O-4).
2. Three things it does that I would have missed in my own repo: a single-file custody log whose
   cited paths mostly resolve (O-4, O-5); a paid review that runs once when ready, with an
   API-free packet for drafts (O-12); an observation document filed before the seal (O-14).
3. Three things that confused me: an empty Spade vault beside a ♠️ founding row (O-9); README
   folder list and moav README both shorter than the trees they describe (O-2, O-8); navigo
   naming "under review" while a numbered table stays in `CLAUDE.md` (`CLAUDE.md`, Navigo model).
4. One thing it seems to promise that I cannot find evidence of (and where I looked): stream
   returns arriving in `returns/stream-N-*/`. I checked all seven folders, `.claude/returns/`
   and the registry (O-19).
5. With ten minutes, I would open `prima-clock/registry.md` first, because it is one file in a
   fixed format and much of the repo is cited from it.

**Through other eyes** (full text in `pass1_hodie-reads-custos.md` section 7):

- The newcomer who has never seen either repo: the README is short and starts with four
  commands; `CLAUDE.md` (265 lines) carries most of the orientation.
- A contributor with no context, who wants to help today: five issue forms and a claim path
  exist; the Latin cues are an extra step before claiming.
- The Shepherd on a tired day, coming back after a break: re-entry files exist, but several are
  stamped weeks behind the work (O-17, O-18).
- The repo six months from now, if nothing changes: fixed-format records stay readable; things
  that already run ahead of their README or tracker will drift further (a guess).

**Lens (optional, Quince).** Not supplied. Custos's own review lists Quince as "not in the
repo" (`atelier/halide/seeds/REVIEW-202610030124.md:109`) and I found no definition (O-29).

*Commit Pass 1 as `pass1_hodie-reads-custos.md` with a message starting
`freeze:`.* (Done in the commit that adds this file.)

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
