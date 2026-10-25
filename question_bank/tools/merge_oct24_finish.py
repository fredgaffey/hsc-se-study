"""Stage 4 of the 24 Oct merge: apply tags to new entries, run key sanity checks, clean up, write bank.json
(atomically), prune unused pp-* assets and regenerate coverage.md.  Run after merge_oct24_build.py."""
import json, re, os, sys, glob, collections, tempfile
sys.path.insert(0, '/Users/fred/gradeo/question_bank/tools')
from merge_oct24_match import strip
QB = '/Users/fred/gradeo/question_bank'; ROOT = '/Users/fred/gradeo'
merged = json.load(open(QB + '/tools/_merged_stage.json'))
orig = {e['id']: e for e in json.load(open(QB + '/bank.before-merge.json'))}
tags = json.load(open(QB + '/tools/merge_oct24_tags.json'))
POINTS = json.load(open(ROOT + '/study/syllabus_points.json')); PID = {p['id'] for p in POINTS}
LETTERS = 'ABCDEFGHIJ'
EXTRA_ISSUES = {  # known problems in existing entries found during the merge
    'g-0fc8049d-8da9-4f5d-ab82-79eae6341c38': 'sample answer is buggy: minute = TotalMinutes//60 should be TotalMinutes % 60, so the minutes it prints are wrong',
}
stats = collections.Counter()
OUT_RE = re.compile(r'prolog|assembler|assembly|two.?s complement|ieee 754|sign modulus|logic paradigm|\bcase tool', re.I)

def has_img_ref(s): return bool(s and re.search(r'\(/?img/[^)]*\)', s))
def drop_broken(e, fld):
    v = e.get(fld)
    if isinstance(v, str) and has_img_ref(v):
        e[fld] = re.sub(r'!\[[^\]]*\]\(/?img/[^)]*\)', '[image not available in the source export]', v)
        e.setdefault('issues', []).append(f'{fld} referenced an image that is missing from the source export (img/...)'); stats['broken_img'] += 1

out = []
for e in merged:
    if e.get('_src') == 'bank' and not e.get('_cluster'):   # untouched existing entry: pass through verbatim
        o = json.loads(json.dumps(orig[e['id']]))
        if e['id'] in EXTRA_ISSUES and not o['reserved']: o['issues'].append(EXTRA_ISSUES[e['id']])
        o['_verbatim'] = True; out.append(o); continue
    e = dict(e)
    is_new_tag = False
    if not e.get('syllabus'):
        t = None
        for i in ([e['id']] + e.get('_cluster', [])):
            if i in tags: t = tags[i]; break
        if t is None: raise SystemExit('untagged ' + e['id'])
        e['syllabus'] = t['syllabus']; e['quality'] = t['quality']
        e['issues'] = list(dict.fromkeys(list(e.get('issues') or []) + t['issues']))
        e['reviewed'] = True
        if t.get('key') and e.get('options'):
            for o in e['options']: o['correct'] = o['letter'] in t['key']
            e['key_source'] = 'claude'; e['key_confidence'] = 'medium'
            e['issues'].append("source paper has no key; the key is Claude's")
        is_new_tag = True
    e.setdefault('issues', [])
    if e['id'] == 'nesa-fam-q2':   # the paper.is copy is a multiple-choice variant with a differently ordered results table
        e.pop('sample_answer', None); e.pop('key_confidence', None)
        e['issues'].append('merged: the paper.is copy is a multiple-choice variant (results ordered by price, key A); the earlier NESA dropdown copy (results ordered by name) was replaced and its sample answer dropped as it no longer applies')
        e['merge_note'] = 'criteria from the earlier dropdown copy; sample answer dropped (variant differs)'
    e['issues'] = [i for i in e['issues'] if i != 'no key in source']
    # --- clean-ups for parsed entries
    if e['id'].startswith('pp-') or e['id'].startswith('th-') or e.get('_paper'):
        if not (e.get('prompt') or '').strip() and e.get('stimulus'):
            e['prompt'], e['stimulus'] = e['stimulus'], None; stats['stim_to_prompt'] += 1
        for f in ('prompt', 'stimulus', 'sample_answer'): drop_broken(e, f)
        if e.get('sample_answer_images'):
            e['sample_answer_images'] = [i for i in e['sample_answer_images'] if i.startswith('assets/')]
            if not e['sample_answer_images']: e.pop('sample_answer_images')
        if e.get('sample_answer') and re.search(r'\[image not available', e['sample_answer']) and len(re.sub(r'\[image not available[^\]]*\]', '', e['sample_answer']).strip()) < 5:
            e['sample_answer'] = None
    # --- key sanity checks (new + merged entries only)
    probs = []
    t = e['answer_type']
    if t in ('MULTI_CHOICE', 'MULTI_SELECT') and e.get('options'):
        nc = sum(1 for o in e['options'] if o.get('correct'))
        if nc == 0 and not any('no key' in i or 'no answer key' in i for i in e['issues']): probs.append('no answer key: no option is marked correct')
        if t == 'MULTI_CHOICE' and nc > 1 and e['id'][:3] in ('pp-', 'th-'): probs.append(f'{nc} options are marked correct on a single-answer item')
        for o in e['options']:
            tx = (o.get('text') or '').strip()
            if tx in ('', '(no answer)', 'no answer', '-') and not o.get('image') and e['id'][:3] in ('pp-', 'th-') and not re.fullmatch(r'[A-D]\.?', tx):
                if tx != '': probs.append(f'blank/placeholder option {o["letter"]}: "{tx}"')
    if re.search(r'(^|\n)\s*\(?[A-D][.)]\s+\S', (e.get('prompt') or '')) and e.get('options') and (e['id'][:3] in ('pp-', 'th-')):
        probs.append('options are pasted into the question text as well')
    if t == 'OBJECTIVE_RESPONSE' and e.get('objective') and any(not r['correct'] for r in e['objective']['rows']) and e['id'][:3] == 'pp-':
        probs.append('matching grid has rows with no correct answer')
    if t == 'RICH_TABLE' and e.get('table') and e['id'][:3] == 'pp-':
        dd = [c for r in e['table'] for c in r if c.get('type') == 'dropdown']
        if dd and any(not c.get('correct') for c in dd): probs.append('dropdown table has cells with no correct answer')
    if t in ('MULTI_SELECT',) and e.get('options') and e['id'][:3] in ('pp-',):
        nc = sum(1 for o in e['options'] if o.get('correct'))
        if nc and nc != e['marks'] and e['marks'] == 1 and nc > 2: probs.append(f'{nc} correct options for a 1-mark item')
    # criteria that don't relate to the prompt (copied from a different question)
    if e.get('criteria') and e['id'][:3] == 'pp-' and t in ('SHORT',):
        ct = set(strip(' '.join(c['criterion'] or '' for c in e['criteria'])).split()); pt = set(strip((e.get('stimulus') or '') + ' ' + (e.get('prompt') or '')).split())
        stop = {'the', 'a', 'of', 'and', 'to', 'in', 'is', 'that', 'how', 'for', 'or', 'with', 'an', 'as', 'by', 'on', 'be', 'are', 'their', 'this', 'it', 'at', 'from', 'students', 'correctly', 'identifies', 'explains', 'describes', 'provides', 'response', 'clearly', 'some', 'one', 'two', 'marks'}
        ctc = {w for w in ct if w not in stop and len(w) > 3}; ptc = {w for w in pt if w not in stop and len(w) > 3}
        if ctc and ptc and len(ctc & ptc) == 0 and len(ctc) >= 8: probs.append('marking criteria share no key words with the question (possibly copied from a different question)')
    # unkeyed new entries: nothing to mark against
    keyed = bool(e.get('criteria') or e.get('sample_answer') or e.get('rubric') or e.get('guidance') or
                 (e.get('options') and any(o.get('correct') for o in e['options'])) or
                 (e.get('objective') and e['objective']['rows'] and all(r['correct'] for r in e['objective']['rows'])) or
                 (e.get('table') and any(c.get('correct') for r in e['table'] for c in r if c.get('type') == 'dropdown')) or e.get('sorting', {}).get('correct_order'))
    if not keyed and e['id'][:3] in ('pp-', 'th-'):
        if not any(('no ' in i and ('key' in i or 'marking' in i)) for i in e['issues'] + probs): probs.append('no answer key, criteria or sample answer in the source')
        if e['quality'] > 2: e['quality'] = 2
    if e.get('_paper') and not e.get('key_source') and keyed and e['_paper'] != 'th-trial':
        e['key_source'] = 'paper.is (exam.json answers)'
    for p in probs:
        if p not in e['issues']: e['issues'].append(p); stats['auto_issue'] += 1
    if e['id'] in EXTRA_ISSUES and EXTRA_ISSUES[e['id']] not in e['issues']: e['issues'].append(EXTRA_ISSUES[e['id']])
    if OUT_RE.search((e.get('prompt') or '') + (e.get('stimulus') or '')) and is_new_tag and e['syllabus'] not in (['OUT'], ['Y11']): stats['out_candidates'] += 1; print('check OUT?', e['id'], e['prompt'][:80])
    for s in e['syllabus']:
        if s not in PID and s not in ('Y11', 'OUT'): raise SystemExit('bad syllabus ' + s + ' ' + e['id'])
    if is_new_tag and e.get('_paper') in ('nsw-software-engineering-paper',): e['review_note'] = 'student-written paper (unofficial); marking criteria are the author\'s'
    out.append(e)

ORDER = ['id', 'origin', 'reserved', 'source', 'source_paper', 'publisher', 'also_in', 'question_title', 'part', 'stimulus', 'prompt', 'answer_type', 'marks', 'options', 'objective', 'table', 'sorting', 'word_limit', 'accepted_answers', 'extended', 'language', 'starter_code', 'dataset_setup_sql', 'starter_query', 'background_images', 'raw_parameters', 'criteria', 'rubric', 'guidance', 'sample_answer', 'sample_answer_images', 'key_source', 'key_confidence', 'images', 'syllabus', 'quality', 'issues', 'review_note', 'merge_note', 'reviewed']
def sec(i):
    if i == 'Y11': return 9998
    if i == 'OUT': return 9999
    return ['SSA', 'WEB', 'AUTO', 'PROJ'].index(i.split('-')[0]) * 100 + int(i.split('-')[1])
out.sort(key=lambda e: (e['reserved'], sec((e['syllabus'] or ['Y11'])[0]), e['id']))
clean = []
for e in out:
    if e.get('_verbatim'): e.pop('_verbatim'); clean.append(e); continue
    o = {}
    for k in ORDER:
        if k in e and (e[k] is not None or k == 'answer_type') and not (isinstance(e[k], list) and not e[k] and k not in ('issues', 'syllabus', 'images')): o[k] = e[k]
    o.setdefault('issues', []); o.setdefault('images', [])
    clean.append(o)
# every referenced asset must exist; prune unused pp-* assets
used = set()
txt = json.dumps(clean)
for m in re.finditer(r'assets/[^)"\\\s]+', txt): used.add(m.group(0))
for e in clean:
    for i in e.get('images', []): used.add(i)
missing = [u for u in used if not os.path.exists(f'{QB}/{u}')]
print('missing assets:', missing[:10], len(missing))
pruned = 0
for f in (glob.glob(QB + '/assets/pp-*') if '--prune' in sys.argv else []):
    if 'assets/' + os.path.basename(f) not in used: os.remove(f); pruned += 1
print('pruned', pruned, 'stats', dict(stats))
# write atomically
data = json.dumps(clean, indent=1, ensure_ascii=False)
json.loads(data)
fd, tmp = tempfile.mkstemp(dir=QB, suffix='.json'); os.write(fd, data.encode()); os.close(fd)
json.load(open(tmp)); os.replace(tmp, QB + '/bank.json')
print('bank entries', len(clean))
json.dump(clean, open('/private/tmp/claude-501/-Users-fred/95b6a376-48d8-41ac-9482-73ff72274d96/scratchpad/final_view.json', 'w'))
