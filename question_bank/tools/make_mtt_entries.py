# Builds tools/mtt_entries.json from /Users/fred/hsc-se-resources (github.com/miketeachestech/hsc-software-engineering-resources,
# CC BY-NC 4.0, (c) Michael Grassi 2025):
#   Practice Questions/[1-4]*/*_QB.md + *_ANS.md   (Year 12 question banks; '5. Year 11 Revision' skipped)
#   Practice Exams/1/prac-trial-exam.md + prac-trial-answers.md
#   Practice Exams/2/exam.pdf + answers.pdf        (hand-transcribed below; it reproduces NESA's HSC SE Sample Examination
#                                                    and its official marking guidelines dated 21 May 2025)
# Syllabus tags / quality come later from tools/review_mtt.txt.
import json, re, glob, os, shutil

R = '/Users/fred/hsc-se-resources'
QB_ASSETS = '/Users/fred/gradeo/question_bank/assets'
REPO = 'miketeachestech/hsc-software-engineering-resources'
LETTERS = 'ABCDEFGH'
out = []

def clean(s):
    s = re.sub(r'[ \t]+\n', '\n', s.strip())
    return re.sub(r'\n{3,}', '\n\n', s).strip() or None

# ---------------------------------------------------------------- question banks
qnum = re.compile(r'^\*\*(\d+)\.\*\*\s*\*\((\d+)\s*marks?\)\*\s*(.*)$')
for qb in sorted(glob.glob(f'{R}/Practice Questions/[1-4]*/*_QB.md')):
    ans = qb.replace('_QB.md', '_ANS.md')
    rel = os.path.relpath(qb, R)
    topic = re.sub(r'^# \*\*Practice Questions: (.*)\*\*$', r'\1', open(qb).readline().strip())
    def blocks(path):
        cur, section, res = None, None, {}
        for line in open(path).read().split('\n'):
            if line.startswith('## '):
                section = 'MC' if 'Multiple' in line else 'ER' if 'Extended' in line else 'SA'
                cur = None; continue
            m = qnum.match(line.strip())
            if m:
                cur = int(m.group(1)); res[cur] = {'marks': int(m.group(2)), 'first': m.group(3).strip(), 'lines': [], 'section': section}
                continue
            if line.strip() == '---': cur = None; continue
            if cur is not None: res[cur]['lines'].append(line)
        return res
    Q, A = blocks(qb), blocks(ans)
    for n, q in Q.items():
        opts = [re.match(r'^\s*-\s*([A-H])\)\s*(.*)$', l) for l in q['lines']]
        opts = [(m.group(1), m.group(2).strip()) for m in opts if m]
        extra = [l for l in q['lines'] if not re.match(r'^\s*-\s*[A-H]\)', l)]
        prompt = clean(q['first'] + '\n' + '\n'.join(extra))
        a = A.get(n)
        e = {'id': f'mtt-qb-{os.path.basename(qb)[:-6].lower()}-q{n}', 'origin': 'MikeTeachesTech', 'reserved': False,
             'source': f'MikeTeachesTech practice questions – {topic} Q{n} ({REPO}: {rel})', 'source_paper': f'MikeTeachesTech QB: {topic}',
             'publisher': 'MikeTeachesTech (Michael Grassi, CC BY-NC 4.0)', 'question_title': f'{topic} Q{n}', 'part': f'Question {n}',
             'stimulus': None, 'prompt': prompt, 'marks': q['marks'], 'images': [], 'issues': [], 'key_source': 'MikeTeachesTech answers file'}
        if opts:
            ca = None
            if a:
                m = re.search(r'Correct Answer:\s*\*\*([A-H])\)', '\n'.join(a['lines']))
                ca = m.group(1) if m else None
            e['answer_type'] = 'MULTI_CHOICE'
            e['options'] = [{'letter': L, 'text': t, 'image': None, 'correct': L == ca} for L, t in opts]
            e['criteria'] = [{'marks': '1', 'criterion': 'Identifies the correct answer'}]
            if not ca: e['issues'].append('no answer key found')
        else:
            e['answer_type'] = 'SHORT'
            if q['section'] == 'ER': e['extended'] = True
            pts = [re.sub(r'^\s*-\s*', '', l).strip() for l in (a['lines'] if a else []) if l.strip().startswith('-')]
            e['criteria'] = [{'marks': (re.search(r'\*\*(\d+) marks?\*\*', p) or [None, '1'])[1], 'criterion': re.sub(r'\*\*', '', p)} for p in pts] or None
            e['rubric'] = 'Marking points (one mark each unless stated):\n' + '\n'.join('- ' + re.sub(r'\*\*', '', p) for p in pts) if pts else None
            if not pts: e['issues'].append('no marking points found')
        out.append(e)

# ---------------------------------------------------------------- practice exam 1 (markdown)
P1 = f'{R}/Practice Exams/1'
os.makedirs(QB_ASSETS, exist_ok=True)
shutil.copy(f'{P1}/structurechart.png', f'{QB_ASSETS}/mtt_exam1_structurechart.png')
def qsplit(text):
    parts = re.split(r'^### Question\s*(\d*)\s*\((\d+) marks?\)\s*$', text, flags=re.M)
    res, i = [], 1
    while i < len(parts):
        res.append((parts[i] or None, int(parts[i + 1]), parts[i + 2].strip().strip('-').strip())); i += 3
    return res
EX = qsplit(open(f'{P1}/prac-trial-exam.md').read())
AN = qsplit(open(f'{P1}/prac-trial-answers.md').read())
for k, (num, marks, body) in enumerate(EX):
    n = int(num) if num else k + 1
    ans = AN[k][2] if k < len(AN) else None
    body = body.replace('./structurechart.png', 'assets/mtt_exam1_structurechart.png').replace('[Your answer here]', '').strip()
    # split sub-parts (a)/(b)/(c)
    ps = re.split(r'^\*\*\(([a-c])\)\s*', body, flags=re.M)
    aps = re.split(r'^\*\*\(([a-c])\)\**\s*', ans or '', flags=re.M)
    base = dict(origin='MikeTeachesTech', reserved=False, publisher='MikeTeachesTech (Michael Grassi, CC BY-NC 4.0)',
                source_paper='MikeTeachesTech Practice Trial Exam 1', key_source='MikeTeachesTech answers file', issues=[])
    src = f'MikeTeachesTech Practice Trial Exam 1 Q{n} ({REPO}: Practice Exams/1/prac-trial-exam.md)'
    if len(ps) > 1 and len(aps) == len(ps):
        stim = clean(ps[0])
        for j in range(1, len(ps), 2):
            letter, txt = ps[j], re.sub(r'^\*\*\s*', '', ps[j + 1])
            if txt.count('**') % 2: txt = txt.replace('**', '', 1)
            mm = re.search(r'\((\d+) marks?', txt)
            out.append({**base, 'id': f'mtt-exam1-q{n}{letter}', 'source': src.replace(f'Q{n} ', f'Q{n}({letter}) '), 'question_title': f'Practice Trial Exam 1 Q{n}',
                        'part': f'Question {n} ({letter})', 'stimulus': stim, 'prompt': clean(txt), 'marks': int(mm.group(1)) if mm else None,
                        'answer_type': 'SHORT', 'sample_answer': clean(aps[j + 1]), 'images': ['assets/mtt_exam1_structurechart.png'] if 'structurechart' in (stim or '') else []})
    else:
        opts = re.findall(r'^- \[ \]\s*(.*?)\s*$', body, flags=re.M)
        e = {**base, 'id': f'mtt-exam1-q{n}', 'source': src, 'question_title': f'Practice Trial Exam 1 Q{n}', 'part': f'Question {n}',
             'stimulus': None, 'prompt': clean(re.sub(r'^- \[ \].*$', '', body, flags=re.M)), 'marks': marks, 'sample_answer': clean(ans or ''), 'images': []}
        if opts:
            corr = set(re.findall(r'^\s*-\s*(.+?)\s*$', (ans or '').split('**Justification')[0], flags=re.M)) | set(re.findall(r'\*\*Correct answer:\*\*\s*(.+?)\s*$', ans or '', flags=re.M))
            e['options'] = [{'letter': LETTERS[i], 'text': t, 'image': None, 'correct': t.strip() in {c.strip() for c in corr}} for i, t in enumerate(opts)]
            nc = sum(o['correct'] for o in e['options'])
            e['answer_type'] = 'MULTI_SELECT' if 'More than one' in body or nc > 1 else 'MULTI_CHOICE'
            if nc == 0: e['issues'].append('answer key could not be matched to an option')
        elif 'Steps to arrange' in body: e['answer_type'] = 'SORTING'
        elif 'SQL' in body: e['answer_type'] = 'SQL'
        elif 'def ' in body or 'Python' in body: e['answer_type'] = 'CODING'
        elif 'class diagram' in body.lower(): e['answer_type'] = 'DRAWING'
        else: e['answer_type'] = 'SHORT'
        out.append(e)

exec(open('/Users/fred/gradeo/question_bank/tools/mtt_exam2.py').read())
rv = {}
for line in open('/Users/fred/gradeo/question_bank/tools/review_mtt.txt'):
    if line.strip():
        i, syl, q, iss = line.rstrip('\n').split('|', 3); rv[i] = (syl.split(','), int(q), iss)
for e in out:
    syl, q, iss = rv[e['id']]
    e['syllabus'] = syl; e['quality'] = q
    if iss: e['issues'] = e.get('issues', []) + [iss]
json.dump(out, open('/Users/fred/gradeo/question_bank/tools/mtt_entries.json', 'w'), indent=1, ensure_ascii=False)
print(len(out), 'entries')
import collections; print(collections.Counter(e['answer_type'] for e in out)); print([e['id'] for e in out if e['issues']])
