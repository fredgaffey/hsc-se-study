"""Builds the written-answer practice queue from gradeo_out/exams/*/exam.json.

  practice/QUEUE.md   questions only (no answers), in priority order, with status
  practice/key.json   criteria, rubric, guidance, sample answers, previous attempts (for Claude to mark with)
  practice/progress.json  status per question id, kept across rebuilds (Claude updates it)

Run:  python3 -I practice/make_queue.py   (from ~/gradeo)
"""
import json, glob, os, re, hashlib
from collections import OrderedDict, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAMS = os.path.join(ROOT, 'gradeo_out', 'exams')
OUT = os.path.join(ROOT, 'practice')
MOCK = 'SEN Holiday Practise 2026'          # reserved for the Monday mock
YEAR11 = 'ITE Software Engineering Y11'     # Year 11 content: lowest priority
LEGAL = re.compile(r'ethic|legal|social|privacy|intellectual|copyright|licen|\bbias|automation|human behaviour|'
                   r'cultur|stakeholder|accessib|inclusiv|end user|impact|employment|data protection', re.I)

def norm(s):
    return re.sub(r'\W+', '', s or '').lower()

qs = OrderedDict()
for f in sorted(glob.glob(os.path.join(EXAMS, '*', 'exam.json'))):
    e = json.load(open(f))
    folder = os.path.relpath(os.path.dirname(f), ROOT)
    for q in e['questions']:
        for p in q['parts']:
            if p['answer_type'] != 'SHORT' or not p['prompt']:
                continue
            key = norm(p['prompt'] + (q['stimulus'] or '')[:200])[:300]
            qid = hashlib.sha1(key.encode()).hexdigest()[:6]
            fix = lambda md: re.sub(r'\]\((assets/[^)]+)\)', lambda m: f']({os.path.join("..", folder, m.group(1))})', md or '')
            item = qs.setdefault(qid, dict(
                id=qid, title=q['title'] + (f" — {p['part']}" if len(q['parts']) > 1 and p['part'] else ''), topic=q['topic'], marks=p['marks_available'] or 0,
                stimulus=fix(q['stimulus']), prompt=fix(p['prompt']), word_limit=p['question'].get('word_limit'),
                exams=[], attempts=[],
                key=dict(criteria=p['marking_criteria'], rubric=p['marking_rubric'], guidance=p['marking_guidance'],
                         sample_answer=fix(p['sample_answer']))))
            item['exams'].append(e['exam'])
            if not item['key']['sample_answer'] and p['sample_answer']:
                item['key'] = dict(criteria=p['marking_criteria'], rubric=p['marking_rubric'],
                                   guidance=p['marking_guidance'], sample_answer=fix(p['sample_answer']))
            r = p['your_response']
            if r['answered'] or p['result']['mark'] is not None:
                item['attempts'].append(dict(exam=e['exam'], mark=p['result']['mark'], words=r.get('word_count'),
                                             answer=r.get('text'), feedback=[x['feedback'] for x in p['result']['feedback'] if x['feedback']]))

def history(q):
    marked = [a for a in q['attempts'] if a['mark'] is not None]
    if not q['attempts']:
        return 'never'
    if marked and max(a['mark'] for a in marked) / max(q['marks'], 1) >= 0.5:
        return 'ok'
    if any((a['words'] or 0) < 15 for a in q['attempts']) or (marked and all(a['mark'] / max(q['marks'], 1) < 0.5 for a in marked)):
        return 'blank/low'
    return 'unmarked'

def tier(q):
    ex = ' '.join(q['exams'])
    if all(MOCK in x for x in q['exams']):
        return 9
    if all(YEAR11 in x for x in q['exams']):
        return 8
    h = history(q)
    if q['marks'] >= 6:
        return 1
    if LEGAL.search(q['title'] + ' ' + q['prompt']):
        return 2
    if h == 'blank/low':
        return 3
    if h in ('never', 'unmarked'):
        return 4
    return 5

TIERS = {1: 'Extended responses (6+ marks) — at least one a day',
         2: 'Legal, social & ethical (incl. AI bias, privacy, IP, automation)',
         3: 'Previously blank or under half marks',
         4: 'Never attempted / never marked',
         5: 'Previously scored half or better (revisit last)',
         8: 'Year 11 paper (likely not in the HSC; check with your teacher)',
         9: f'RESERVED for Monday mock ({MOCK}) — do not practise these'}

def interleave(items):
    """Round-robin across topics so consecutive questions differ."""
    by = defaultdict(list)
    for q in sorted(items, key=lambda q: (-q['marks'], q['title'])):
        by[q['topic']].append(q)
    out = []
    while any(by.values()):
        for t in sorted(by, key=lambda t: -len(by[t])):
            if by[t]:
                out.append(by[t].pop(0))
    return out

progress_path = os.path.join(OUT, 'progress.json')
progress = json.load(open(progress_path)) if os.path.exists(progress_path) else {}

# Year 11 paper excluded: not relevant to the HSC (decided 24 Oct).
for k in [k for k, v in qs.items() if all(YEAR11 in x for x in v['exams'])]:
    del qs[k]

groups = defaultdict(list)
for q in qs.values():
    q['tier'] = tier(q)
    q['history'] = history(q)
    groups[q['tier']].append(q)

n = 0
L = ['# Practice queue — written answers', '',
     'Questions only. Answers, criteria and your old attempts are in `key.json`, which Claude marks with. **Don\'t open it.**', '',
     '**Loop:** type the answer timed (2 min per mark, spell-check off) → mark it yourself against the criteria verbs →',
     'Claude marks it (band + 1–2 fixes) → rewrite once from memory → log the fix in REVISION.md.', '',
     'Tell Claude: *"next question"* or *"question #12"*. Status: ⬜ to do · 🔁 rewrite pending · ✅ done (best mark).', '']
total = defaultdict(int)
for t in sorted(groups):
    items = interleave(groups[t])
    L += ['', f'## {TIERS[t]}', '']
    for q in items:
        n += 1
        q['num'] = n
        st = progress.get(q['id'], {})
        icon = {'done': '✅', 'rewrite': '🔁'}.get(st.get('status'), '⬜')
        best = f" **{st['best']}/{q['marks']}**" if st.get('best') is not None else ''
        hist = {'never': 'new', 'blank/low': 'was blank/low', 'unmarked': 'attempted, unmarked', 'ok': 'scored ≥50% before'}[q['history']]
        mins = q['marks'] * 2
        L.append(f'### {icon} #{n} · {q["title"]} — {q["marks"]} marks · {mins} min · ~{q["marks"] * 35} words{best}')
        L.append(f'<sub>id `{q["id"]}` · {hist}</sub>')
        L.append('')
        if q['stimulus']:
            L.append('> ' + q['stimulus'].replace('\n', '\n> '))
            L.append('')
        L.append(q['prompt'])
        if q['word_limit']:
            L.append(f'\n*Word limit: {q["word_limit"]}*')
        L.append('')
        total[t] += 1

L.insert(10, '**Counts:** ' + ' · '.join(f'{TIERS[t].split(" (")[0].split(" —")[0]}: {c}' for t, c in sorted(total.items())) + '\n')
open(os.path.join(OUT, 'QUEUE.md'), 'w').write('\n'.join(L) + '\n')
json.dump({q['id']: {k: q[k] for k in ('num', 'title', 'marks', 'tier', 'history', 'prompt', 'stimulus', 'key', 'attempts', 'exams')}
           for q in qs.values()}, open(os.path.join(OUT, 'key.json'), 'w'), indent=1)
if not os.path.exists(progress_path):
    json.dump({}, open(progress_path, 'w'))
print(f'{len(qs)} questions ->', dict(sorted(total.items())))
