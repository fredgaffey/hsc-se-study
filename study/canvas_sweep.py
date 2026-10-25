"""Build a syllabus sweep drill from the SEN Online (Canvas) quiz bank.

  python3 -I study/canvas_sweep.py "Unit 1" "Sweep 1b - Secure Software Architecture" 2 > spec.json
  node exam-app/drill.mjs spec.json

Picks the hardest-looking keyed questions per Canvas quiz (Multiple Answer and long scenario stems first,
no True/False), shuffles options, and tags each with the syllabus point (Canvas quiz "1.N" = SSA-N,
"2.N" = WEB-N, "3.N" = AUTO-N).
"""
import json, random, re, sys

BANK = '/Users/fred/canvas/app/data/questions.json'
PREFIX = {'1': 'SSA', '2': 'WEB', '3': 'AUTO'}

unit, title, per_quiz = sys.argv[1], sys.argv[2], int(sys.argv[3])
rng = random.Random(title)
# The SEN Online export has scraping artefacts: blank "(no answer)" options, the selected option pasted
# into the question text ("... Answer, X"), and "select all" questions with no correct option kept.
BLANK = re.compile(r'^\(?no answer\)?$', re.I)
def clean(q):
    q = dict(q)
    q['opts'] = [o for o in (q.get('opts') or []) if (o.get('t') or '').strip() and not BLANK.match(o['t'].strip())]
    return q
skipped = {'pasted option': 0, 'no correct option': 0, 'too few options': 0}
qs = []
for q in map(clean, json.load(open(BANK))):
    if q['course'] != '12951' or not q['unit'].startswith(unit) or not q.get('key') or q['type'] not in ('Multiple Choice', 'Multiple Answer'):
        continue
    if re.search(r'\bAnswer,\s', q['q']): skipped['pasted option'] += 1; continue
    if not any(o['c'] for o in q['opts']): skipped['no correct option'] += 1; continue
    if len(q['opts']) < 3: skipped['too few options'] += 1; continue
    qs.append(q)

def hardness(q):
    opt_len = sorted(len(o['t']) for o in q['opts'])
    similar = opt_len[0] / max(opt_len[-1], 1)          # options of similar length are harder to guess
    return (q['type'] == 'Multiple Answer') * 120 + len(q['q']) + 60 * similar + 10 * len(q['opts'])

by_quiz = {}
for q in qs:
    by_quiz.setdefault(q['quiz'], []).append(q)

def quiz_key(name):
    m = re.match(r'(\d+)\.(\d+)', name)
    return (int(m.group(1)), int(m.group(2))) if m else (99, 99)

questions = []
for quiz in sorted(by_quiz, key=quiz_key):
    m = re.match(r'(\d+)\.(\d+)', quiz)
    tag = f"{PREFIX.get(m.group(1), '?')}-{m.group(2)}" if m else None
    for q in sorted(by_quiz[quiz], key=hardness, reverse=True)[:per_quiz]:
        opts = list(q['opts'])
        rng.shuffle(opts)
        letters = 'ABCDEFGH'
        multi = q['type'] == 'Multiple Answer'
        prompt = q['q'] + ('' if not multi or 'apply' in q['q'].lower() else ' (Select all that apply.)')
        questions.append({'title': quiz, 'parts': [{
            'type': 'MULTI_CHOICE', 'marks': 1, 'prompt': prompt,
            'options': [o['t'] for o in opts],
            'correct': [letters[i] for i, o in enumerate(opts) if o['c']],
            'syllabus': tag, 'source': f"SEN Online · {quiz} · id {q['id']}",
        }]})

print(json.dumps({'title': title, 'minutes': max(10, round(len(questions) * 0.9)), 'reading_minutes': 0, 'questions': questions}))
print(f'{len(questions)} questions from {len(by_quiz)} quizzes; skipped broken: {skipped}', file=sys.stderr)
