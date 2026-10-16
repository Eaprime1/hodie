// Offline test table for .github/scripts/file-review.js. No network, no GitHub.
// Run: node scripts/test_file_review.js

const fr = require('../.github/scripts/file-review.js');

let failed = 0;
let total = 0;
const say = (text) => process.stdout.write(`${text}\n`);
const same = (name, got, want) => {
  total += 1;
  if (JSON.stringify(got) !== JSON.stringify(want)) {
    failed += 1;
    say(`FAIL ${name}: ${JSON.stringify(got)} != ${JSON.stringify(want)}`);
  }
};

// Which files need no reading.
const skipRows = [
  ['journey document', 'pr-journeys/202610_PR1_x.md', 'journey document, written by the seal bot'],
  ['lockfile by suffix', 'yarn.lock', 'lockfile'],
  ['binary image', 'docs/pic.png', 'binary image'],
  ['ordinary document', 'docs/final-oversight.md', null],
  ['workflow stays in', '.github/workflows/finalize-pr.yml', null],
  ['watched beats a skip rule', 'moav/photo.png', null],
  ['custody lock file stays in', 'branch-tracker/old.lock', null],
  ['moav stays in', 'moav/x.json', null],
  ['scripts stay in', '.github/scripts/file-review.js', null],
];
skipRows.forEach(([name, path, want]) => {
  same(`skip: ${name}`, fr.skipReason(path), want);
});

// Reading earlier ticks.
const line = (box, path, sha) => `- [${box}] [\`${path}\`](x) <!--fr ${encodeURIComponent(path)} ${sha}-->`;
const body = ['<!-- hodie-file-review -->', line('x', 'a.md', 'aaa'), line(' ', 'b b.md', 'bbb'),
  line('X', 'dir/c (1).md', 'ccc'), '- [x] a line with no mark'].join('\n');
const marks = fr.readMarks(body);
same('marks: ticked', marks.get('a.md'), { checked: true, sha: 'aaa' });
same('marks: unticked, path with a space', marks.get('b b.md'), { checked: false, sha: 'bbb' });
same('marks: capital X, parentheses', marks.get('dir/c (1).md'), { checked: true, sha: 'ccc' });
same('marks: line without a mark is ignored', marks.size, 3);
same('marks: empty body', fr.readMarks('').size, 0);
same('marks: undefined body', fr.readMarks().size, 0);

// Judging one file against the earlier ticks.
const judged = (file) => {
  const j = fr.judge(file, marks);
  return [j.checked, j.skipped, j.note];
};
same('judge: new file waits', judged({ filename: 'new.md', sha: 'n1' }), [false, false, '']);
same('judge: tick kept on the same version', judged({ filename: 'a.md', sha: 'aaa' }), [true, false, '']);
same('judge: tick cleared when the file changed', judged({ filename: 'a.md', sha: 'a2' }),
  [false, false, 'changed since you ticked it']);
same('judge: unticked stays unticked', judged({ filename: 'b b.md', sha: 'bbb' }), [false, false, '']);
same('judge: skipped file is ticked with its reason', judged({ filename: 'pr-journeys/x.md', sha: 'l1' }),
  [true, true, 'journey document, written by the seal bot']);

// Building the two lists.
const linkFor = (f) => `[\`${f.filename}\`](x)`;
const built = fr.build({
  files: [{ filename: 'a.md', sha: 'aaa' }, { filename: 'new.md', sha: 'n1' }, { filename: 'pr-journeys/x.md', sha: 'l1' }],
  marks, linkFor,
});
same('build: read count', [built.toRead, built.done], [2, 1]);
same('build: read lines', built.read.map((l) => l.slice(0, 6)), ['- [x] ', '- [ ] ']);
same('build: skipped line carries its reason', built.skipped.length === 1 && built.skipped[0].includes('journey document'), true);

// Round trip: the text the workflow writes is read back the same.
const text = ['<!-- hodie-file-review -->', ...built.read, ...built.skipped].join('\n');
const back = fr.readMarks(text);
same('round trip: ticks survive', back.get('a.md'), { checked: true, sha: 'aaa' });
same('round trip: unticked survives', back.get('new.md'), { checked: false, sha: 'n1' });

// What a gate reads from the comment.
const state = fr.parseState(`<!-- hodie-file-review -->\n<!--fr-head abc123 total=9 shown=7-->\n${text}`);
same('state: head', state.head, 'abc123');
same('state: counts', [state.total, state.shown], [9, 7]);
same('state: unticked files', state.open, ['new.md']);
same('state: no comment', fr.parseState(''), { head: null, total: 0, shown: 0, open: [] });

say(`${total - failed} of ${total} passed`);
process.exit(failed ? 1 : 0);
