"""Make a drill in the exam app from question-bank entries (real questions, not generated).

  python3 -I study/bank_drill.py "Title" <bank-id> [<bank-id> ...]

Copies stimulus/prompt/criteria/rubric/guidance/sample and any images into papers/drills/<name>/,
via exam-app/drill.mjs (which validates the questions). Drawing questions become DRAWING_V2 (Excalidraw
with NESA's shape library). Prints the drill folder name.
"""
import json, os, re, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QB = os.path.join(ROOT, 'question_bank')
TYPE = {'DRAWING': 'DRAWING_V2', 'DRAWING_V2': 'DRAWING_V2', 'IMAGE': 'DRAWING_V2', 'SHORT': 'SHORT',
        'CODING': 'CODING', 'SQL': 'SQL', 'MULTI_CHOICE': 'MULTI_CHOICE', 'MULTI_SELECT': 'MULTI_CHOICE'}

title, ids = sys.argv[1], sys.argv[2:]
bank = json.load(open(os.path.join(QB, 'bank.json')))
bank = bank if isinstance(bank, list) else bank.get('questions', bank)
by = {x['id']: x for x in bank}

questions, images = [], set()
for i in ids:
    x = by[i]
    if x.get('reserved'):
        sys.exit(f'{i} is reserved ({x.get("reserved_for") or "trial paper"}): not using it')
    t = TYPE.get(x.get('answer_type'), 'SHORT')
    part = {'type': t, 'marks': x.get('marks') or 1, 'prompt': x.get('prompt') or '',
            'criteria': x.get('criteria'), 'guidance': '\n\n'.join(filter(None, [x.get('guidance'), x.get('rubric')])) or None,
            'sample': x.get('sample_answer'), 'syllabus': (x.get('syllabus') or [None])[0],
            'source': f"{x.get('origin')} · {x.get('source_paper') or x.get('source')}"}
    if t == 'CODING' and 'python' not in (x.get('prompt') or '').lower():
        part['language'] = 'PSEUDOCODE'   # "algorithm" questions are pseudocode in this course; Python only when named
    if t == 'MULTI_CHOICE':
        part['options'] = [o.get('text') or (f"![]({o['image']})" if o.get('image') else None) for o in x.get('options') or []]
        part['correct'] = [chr(65 + k) for k, o in enumerate(x.get('options') or []) if o.get('correct')]
    questions.append({'title': x.get('question_title') or title, 'stimulus': x.get('stimulus') or None, 'parts': [part]})
    for fld in (x.get('stimulus'), x.get('prompt'), x.get('sample_answer'), x.get('guidance'), x.get('rubric')):
        images |= set(re.findall(r'\]\((assets/[^)]+)\)', fld or ''))
    images |= set(x.get('images') or [])

marks = sum(q['parts'][0]['marks'] for q in questions)
spec = {'title': title, 'minutes': max(6, marks * 2 + 2), 'reading_minutes': 0, 'questions': questions}
with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f:
    json.dump(spec, f)
out = subprocess.run(['node', os.path.join(ROOT, 'exam-app', 'drill.mjs'), f.name], capture_output=True, text=True)
if out.returncode:
    sys.exit(out.stderr)
name = out.stdout.strip()
dest = os.path.join(ROOT, 'papers', 'drills', name, 'assets')
os.makedirs(dest, exist_ok=True)
for im in images:
    src = os.path.join(QB, im)
    if os.path.exists(src):
        shutil.copy(src, dest)
if any(q['parts'][0]['type'] == 'SQL' and not q['parts'][0].get('dataset_setup_sql') for q in questions):
    print('WARNING: SQL question(s) have no dataset_setup_sql; the Run button will say "no such table". Add one.', file=sys.stderr)
print(name)
