// Gathers the facts for one PR and hands them to final-oversight.js.
// Called from .github/workflows/final-oversight.yml (the BASE branch copy).
// Ported from custos; hodie has no observation folder and no stale-claims tool.
const THREADS_QUERY = `query($o:String!,$r:String!,$n:Int!){
  repository(owner:$o,name:$r){pullRequest(number:$n){
    reviewThreads(first:100){nodes{isResolved}}}}}`;

async function gatherChecks(ctx) {
  const { github, fo, owner, repo, head } = ctx;
  const runs = await github.paginate(github.rest.checks.listForRef, { owner, repo, ref: head, per_page: 100 });
  const combined = await github.rest.repos.getCombinedStatusForRef({ owner, repo, ref: head, per_page: 100 });
  return fo.evaluateChecks({
    runs: runs.map((r) => ({ name: r.name, status: r.status, conclusion: r.conclusion })),
    statuses: combined.data.statuses.map((s) => ({ context: s.context, state: s.state })),
    selfName: 'final-oversight',
  });
}

async function gatherThreads(ctx) {
  const { github, fo, owner, repo, number } = ctx;
  const data = await github.graphql(THREADS_QUERY, { o: owner, r: repo, n: number });
  return fo.evaluateThreads(data.repository.pullRequest.reviewThreads.nodes);
}

function latestSealTime(comments, fo) {
  const isSeal = (c) => c.user && c.user.login === 'github-actions[bot]'
    && c.body.startsWith(fo.SEAL_START);
  const seals = comments.filter(isSeal);
  return seals.length ? seals[seals.length - 1].created_at : null;
}

async function commitDetail(ctx, c) {
  const { github, owner, repo } = ctx;
  const full = await github.rest.repos.getCommit({ owner, repo, ref: c.sha });
  return {
    sha: c.sha,
    date: c.commit.committer.date,
    authorLogin: c.author ? c.author.login : '',
    files: (full.data.files || []).map((f) => f.filename),
  };
}

async function commitsAfter(ctx) {
  const { github, owner, repo, number, sealAt } = ctx;
  const all = await github.paginate(github.rest.pulls.listCommits, { owner, repo, pull_number: number, per_page: 100 });
  const later = all.filter((c) => Date.parse(c.commit.committer.date) > Date.parse(sealAt));
  return Promise.all(later.map((c) => commitDetail(ctx, c)));
}

async function gatherSeal(ctx) {
  const sealAt = latestSealTime(ctx.comments, ctx.fo);
  const commits = sealAt ? await commitsAfter({ ...ctx, sealAt }) : [];
  return ctx.fo.evaluatePostSeal({ sealAt, commits });
}

// The file review comment, and the commits after the head it describes (with their files).
async function gatherFileReview(ctx) {
  const { github, fo, owner, repo, number, head, comments } = ctx;
  const mine = comments.find((c) => c.user && c.user.type === 'Bot' && c.body.startsWith(fo.CONSIDERS_MARK));
  const body = mine ? mine.body : '';
  const marked = fo.checklistHead(body);
  const all = await github.paginate(github.rest.pulls.listCommits, { owner, repo, pull_number: number, per_page: 100 });
  const at = all.findIndex((c) => c.sha === marked);
  const detail = (c, i) => (i > at ? commitDetail(ctx, c) : { sha: c.sha });
  const commits = at === -1 ? [] : await Promise.all(all.map(detail));
  return fo.evaluateFileReview({ body, head, commits });
}

async function upsertComment(ctx) {
  const { github, fo, owner, repo, number, comments, body } = ctx;
  const mine = comments.find((c) => c.user && c.user.type === 'Bot' && c.body.startsWith(fo.MARK));
  if (mine) await github.rest.issues.updateComment({ owner, repo, comment_id: mine.id, body });
  else await github.rest.issues.createComment({ owner, repo, issue_number: number, body });
}

module.exports = async function run({ github, context, core, fo }) {
  const { owner, repo } = context.repo;
  const pr = context.payload.pull_request;
  const base = { github, fo, owner, repo, number: pr.number, head: pr.head.sha };
  const comments = await github.paginate(github.rest.issues.listComments, { owner, repo, issue_number: base.number, per_page: 100 });
  const files = await github.paginate(github.rest.pulls.listFiles, { owner, repo, pull_number: base.number, per_page: 100 });
  const names = files.map((f) => f.filename);

  const watched = fo.watchedPaths(names);
  const facts = {
    head: base.head,
    checks: await gatherChecks(base),
    threads: await gatherThreads(base),
    post: await gatherSeal({ ...base, comments }),
    fileReview: await gatherFileReview({ ...base, comments }),
    watched,
    unnamed: fo.unnamedWatched(watched, pr.body || ''),
  };

  const body = fo.render(facts);
  await upsertComment({ ...base, comments, body });
  core.summary.addRaw(body).write();
  if (fo.hardFail(facts)) {
    core.setFailed('Final oversight found something that needs attention. See the comment on the PR.');
  }
};
