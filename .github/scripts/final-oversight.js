// Final oversight: the pure checks behind .github/workflows/final-oversight.yml.
// Ported from custos (phase C of the file review swap). Hodie has no observation
// folder, so there is no observation row.
//
// Nothing here calls GitHub. The workflow gathers the facts (check runs, review
// threads, comments, commits, files) and hands them to
// these functions, so tools/test_final_oversight.js can run every rule offline.
//
// The gate reports. It never seals, never merges, never edits the PR.

const { MARK: CONSIDERS_MARK, parseState } = require('./file-review.js');

const OK_CONCLUSIONS = ['success', 'skipped', 'neutral'];
const BAD_CONCLUSIONS = ['failure', 'cancelled', 'timed_out', 'action_required', 'startup_failure', 'stale'];

// One check run -> 'ok', 'bad' or 'pending'.
function runState(r) {
  if (r.status !== 'completed') return 'pending';
  if (OK_CONCLUSIONS.includes(r.conclusion)) return 'ok';
  return BAD_CONCLUSIONS.includes(r.conclusion) ? 'bad' : 'pending';
}

// One commit status -> 'ok', 'bad' or 'pending'.
function statusState(s) {
  if (s.state === 'success') return 'ok';
  return s.state === 'pending' ? 'pending' : 'bad';
}

// Check runs and commit statuses on the head, minus this workflow's own check.
// runs:     [{ name, status, conclusion }]
// statuses: [{ context, state }]
function evaluateChecks({ runs = [], statuses = [], selfName = '' }) {
  const bad = [];
  const pending = [];
  const sort = (state, label) => {
    if (state === 'bad') bad.push(label);
    if (state === 'pending') pending.push(label);
  };
  runs.filter((r) => r.name !== selfName).forEach((r) => {
    const state = runState(r);
    sort(state, state === 'bad' ? `${r.name} (${r.conclusion})` : r.name);
  });
  statuses.forEach((s) => {
    const state = statusState(s);
    sort(state, state === 'bad' ? `${s.context} (${s.state})` : s.context);
  });
  return { ok: bad.length === 0 && pending.length === 0, bad, pending };
}

// Review threads: any that are unresolved.
// threads: [{ isResolved }]
function evaluateThreads(threads = []) {
  const open = threads.filter((t) => !t.isResolved).length;
  return { ok: open === 0, open, total: threads.length };
}

// A bot commit that touches nothing but pr-journeys/ is the journey document
// written at the seal; it may follow the seal.
function isJourneyCommit(c) {
  const files = c.files || [];
  const journeyOnly = files.length > 0 && files.every((f) => f.startsWith('pr-journeys/'));
  return journeyOnly && c.authorLogin === 'github-actions[bot]';
}

// Commits after the latest seal that are not the journey document.
// commits: [{ sha, date, authorLogin, files: [path] }], sealAt: ISO string or null
function evaluatePostSeal({ sealAt, commits = [] }) {
  if (!sealAt) return { ok: false, sealed: false, late: [], note: 'no seal record found' };
  const sealTime = Date.parse(sealAt);
  const late = commits
    .filter((c) => Date.parse(c.date) > sealTime && !isJourneyCommit(c))
    .map((c) => c.sha.slice(0, 7));
  return { ok: late.length === 0, sealed: true, late };
}

// The file review checklist (docs/final-oversight.md): every file to read is ticked.
// The comment names the head it describes. After the seal, the journey document
// moves the head, so a checklist that is one journey commit behind still counts.
// commits: [{ sha, authorLogin?, files? }] in order; details are needed after the marked head.
function checklistHead(body) {
  return parseState(body).head;
}

function staleProblem(markedHead, head, commits) {
  if (markedHead === head) return null;
  const at = commits.findIndex((c) => c.sha === markedHead);
  if (at === -1) return 'the checklist describes another head';
  return commits.slice(at + 1).every(isJourneyCommit) ? null : 'files changed since the checklist was written';
}

function missingChecklist(body, state) {
  if (!String(body || '').trim()) return 'no file review comment';
  return state.head ? null : 'the comment has no checklist';
}

function evaluateFileReview({ body, head, commits = [] }) {
  const state = parseState(body);
  const missing = missingChecklist(body, state);
  if (missing) return { ok: false, open: [], problems: [missing] };
  const problems = [staleProblem(state.head, head, commits)].filter(Boolean);
  if (state.total > state.shown) problems.push(`${state.total - state.shown} file(s) not listed`);
  if (state.open.length) problems.push(`${state.open.length} file(s) not yet read`);
  return { ok: problems.length === 0, open: state.open, problems };
}

// Files that sit on the seal path or hold custody records.
const WATCHED = [
  /^moav\//, /^branch-tracker\//,
  /^\.github\/workflows\/(finalize-pr|final-oversight|file-review)\.yml$/,
  /^\.github\/scripts\/(file-review|final-oversight|final-oversight-run)\.js$/,
  /^\.github\/review-skip\.json$/,
];
function watchedPaths(files = []) {
  return files.filter((f) => WATCHED.some((re) => re.test(f)));
}
// A watched path is "named" when the PR body mentions its file name or folder.
function unnamedWatched(watched, body = '') {
  const lowered = String(body).toLowerCase();
  return watched.filter((f) => {
    const base = f.split('/').pop().toLowerCase();
    const top = f.split('/')[0].toLowerCase();
    return !(lowered.includes(base) || lowered.includes(`${top}/`));
  });
}

// Hodie's seal comment begins with this text (finalize-pr.yml). It is the seal record.
const SEAL_START = '## ✅ Finalized';

const MARK = '<!-- hodie-final-oversight -->';
const tick = (ok) => (ok ? '✅' : '❌');
const row = (state, name, detail) => `| ${state} | ${name} | ${detail} |`;

function checksRow({ checks }) {
  const parts = [];
  if (checks.bad.length) parts.push(`failed: ${checks.bad.join(', ')}`);
  if (checks.pending.length) parts.push(`pending: ${checks.pending.join(', ')}`);
  return row(tick(checks.ok), 'Checks and statuses on the head', checks.ok ? 'all green' : parts.join('; '));
}

function threadsRow({ threads }) {
  const detail = threads.ok ? `none open (${threads.total} total)` : `${threads.open} open of ${threads.total}`;
  return row(tick(threads.ok), 'Review threads', detail);
}

function sealRow({ post }) {
  let detail = `commits after the seal: ${post.late.join(', ')}`;
  if (!post.sealed) detail = 'no seal record on the PR';
  else if (post.ok) detail = 'only the journey document follows the seal';
  return row(tick(post.ok), 'Seal covers this head', detail);
}

function watchedRow({ watched, unnamed }) {
  let detail = 'none touched';
  if (watched.length) {
    detail = unnamed.length
      ? `${watched.length} touched; not named in the PR body: ${unnamed.join(', ')}`
      : `${watched.length} touched, all named in the PR body`;
  }
  return row(unnamed.length ? '⚠️' : 'ℹ️', 'Watched paths (seal path or custody)', detail);
}

function fileReviewRow({ fileReview }) {
  const fr = fileReview || { ok: false, open: [], problems: ['not checked'] };
  const shown = fr.open.slice(0, 8).map((p) => `\`${p}\``).join(', ');
  const more = fr.open.length > 8 ? `, and ${fr.open.length - 8} more` : '';
  const detail = fr.ok ? 'every file to read is ticked' : `${fr.problems.join('; ')}${shown ? `: ${shown}${more}` : ''}`;
  return row(tick(fr.ok), 'File review', detail);
}

// facts: { head, checks, threads, post, fileReview, watched, unnamed }
function render(facts) {
  return [
    MARK,
    `## Final oversight — head \`${facts.head.slice(0, 7)}\``,
    '',
    '*Report only. This does not seal and does not merge. The owner approved this run.*',
    '',
    '| | Check | Detail |',
    '|---|---|---|',
    checksRow(facts),
    threadsRow(facts),
    sealRow(facts),
    fileReviewRow(facts),
    watchedRow(facts),
    '',
  ].join('\n');
}

// facts: the same object; true when a must-pass check failed.
function hardFail(facts) {
  const passes = [facts.checks.ok, facts.threads.ok, facts.post.ok, Boolean(facts.fileReview?.ok)];
  return !passes.every(Boolean);
}

module.exports = {
  MARK, CONSIDERS_MARK, evaluateChecks, evaluateThreads, evaluatePostSeal, evaluateFileReview, checklistHead,
  watchedPaths, unnamedWatched, SEAL_START, render, hardFail,
};
