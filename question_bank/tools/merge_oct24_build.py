"""Stage 3 of the 24 Oct merge. Reads bank.before-merge.json + tools/_merge_candidates.json (+ tools/th_entries.json),
clusters near-duplicates, merges each cluster into one entry and writes tools/_merged_stage.json plus a log.
Tags/quality/issues for new entries come from tools/merge_oct24_tags.json (applied by merge_oct24_finish.py)."""
import json, re, sys, collections, itertools
sys.path.insert(0, '/Users/fred/gradeo/question_bank/tools')
from merge_oct24_match import *
QB = '/Users/fred/gradeo/question_bank'
bank = json.load(open(QB + '/bank.before-merge.json'))
cand = json.load(open(QB + '/tools/_merge_candidates.json'))
try: cand += json.load(open(QB + '/tools/th_entries.json'))
except FileNotFoundError: pass
allx = [dict(e, _src='bank') for e in bank] + [dict(e, _src='cand') for e in cand]
bid = {e['id']: i for i, e in enumerate(allx)}
P = [prep(e) for e in allx]

# ---- pairs
PT = [set(p['p'].split()) for p in P]
inv = collections.defaultdict(list)
for i, tk in enumerate(PT):
    for w in tk: inv[w].append(i)
pairs = {}
NOT_DUP_FAMILY = {'g-16ac6c9c-e68b-46f9-8a78-6191bb661ac2', 'g-170dfb22-e3a0-4fae-8e66-f77f9911e7b4', 'g-79a38fb0-6de4-47ab-999a-45090328e862',
                  'g-e33e79d6-b0d2-4168-856b-6a0aead0a32c', 'g-f8ea62b4-8479-4afd-afdf-1fe989aec9d7', 'g-7bc1497d-6eb7-44c7-8085-562bc3f0aeb7',
                  'g-ebce0b4e-83c3-4bdf-8492-f2e36b1ab0e6', 'g-c754c7cd-7c57-4c77-88b2-9278ef3cb90b', 'g-fee1fb5b-fdf8-46e4-b9cb-2cd832d2c09f'}
for i in range(len(allx)):
    if not PT[i] or allx[i]['reserved']: continue
    cnt = collections.Counter()
    for w in PT[i]:
        l = inv[w]
        if len(l) > 800: continue
        for j in l:
            if j > i and not allx[j]['reserved']: cnt[j] += 1
    for j, c in cnt.items():
        if c / len(PT[i] | PT[j]) < 0.6: continue
        if allx[i]['id'] in NOT_DUP_FAMILY and allx[j]['id'] in NOT_DUP_FAMILY: continue
        ok, s, n = compare(P[i], P[j])
        if ok: pairs[(i, j)] = (s, n)
# forced pairs: NESA fam / sample exam are the same papers as nesa-fam-q* / mtt-exam2-q*
for i, e in enumerate(allx):
    if e['_src'] == 'cand' and e.get('_paper') in ('nesa-hsc-familiarisation', 'nesa-hsc-sample-exam'):
        m = re.match(r'Question (\d+)\s*\(?([a-z])?\)?', e['part'])
        t = ('nesa-fam-q' if 'famil' in e['_paper'] else 'mtt-exam2-q') + m.group(1) + (m.group(2) or '')
        j = bid[t]; pairs[(min(i, j), max(i, j))] = (1.0, 'same NESA paper, matched by question number')
for i, e in enumerate(allx):  # parsed part ids equal Gradeo part ids for papers exported from Gradeo
    if e['_src'] == 'cand' and e['id'].startswith('pp-') and ('g-' + e['id'][3:]) in bid:
        j = bid['g-' + e['id'][3:]]; pairs.setdefault((min(i, j), max(i, j)), (1.0, 'same Gradeo part id'))
# ---- union-find
par = list(range(len(allx)))
def f(x):
    while par[x] != x: par[x] = par[par[x]]; x = par[x]
    return x
for (i, j) in pairs: par[f(i)] = f(j)
clusters = collections.defaultdict(list)
for i in range(len(allx)): clusters[f(i)].append(i)

RANK = {'NESA': 0, 'paper.is': 1, 'TH Software Tuition': 1, 'Gradeo': 2, 'MikeTeachesTech': 3}
def has_key(e):
    if e.get('options') and any(o.get('correct') for o in e['options']): return True
    if e.get('objective') and all(r['correct'] for r in e['objective']['rows']): return True
    if e.get('table') and any(c.get('correct') for r in e['table'] for c in r if c.get('type') == 'dropdown'): return True
    if e.get('sorting') and (e['sorting'].get('correct_order')): return True
    return False
def completeness(e):
    s = 0
    if has_key(e): s += 3
    if e.get('criteria'): s += 2
    if e.get('sample_answer'): s += 2
    if e.get('rubric') or e.get('guidance'): s += 1
    if e.get('key_source') == 'claude': s -= 2.5
    return s
def correct_texts(e):
    if e.get('options'): return {strip(o['text'] or o.get('image') or '') for o in e['options'] if o.get('correct')}
    return None

def same_sets(a, b):
    def cov(x, y): return all(any(r(i, j) >= 0.85 for j in y) for i in x)
    return cov(a, b) and cov(b, a)
def describe(e): return f"{e['origin']}: {e['source']} [{e['id']}]"
def label_of(e):
    return e['source_paper'] or e['source']

merged = []; log = []
for root, mem in clusters.items():
    if len(mem) == 1:
        e = allx[mem[0]]; merged.append(e); continue
    es = [allx[i] for i in mem]
    es.sort(key=lambda e: (-completeness(e), RANK[e['origin']], e['id']))
    base = dict(es[0]); others = es[1:]
    notes = []; also = list(base.get('also_in') or []); issues = list(base.get('issues') or [])
    marks = {e['marks'] for e in es}
    for o in others:
        also.append(describe(o)); also += [a for a in (o.get('also_in') or []) if a not in also]
        for fld in ('criteria', 'rubric', 'guidance', 'sample_answer', 'sample_answer_images'):
            if not base.get(fld) and o.get(fld):
                base[fld] = o[fld]; notes.append(f'{fld} from {o["id"]}')
                if fld in ('sample_answer', 'sample_answer_images'):
                    base['images'] = list(dict.fromkeys((base.get('images') or []) + [i for i in (o.get('images') or []) if i in json.dumps(o[fld])]))
        if not base.get('stimulus') and o.get('stimulus') and len(P[bid[o['id']]]['s']) > 0 and base['answer_type'] == o['answer_type']:
            base['stimulus'] = o['stimulus']; notes.append(f'stimulus from {o["id"]}'); base['images'] = list(dict.fromkeys((base.get('images') or []) + (o.get('images') or [])))
        # options key fill / conflict
        if base.get('options') and o.get('options'):
            bc, oc = correct_texts(base), correct_texts(o)
            if not bc and oc:
                for op in base['options']:
                    if strip(op['text'] or '') in oc: op['correct'] = True
                notes.append(f'correct option(s) from {o["id"]}')
            elif bc and oc and not same_sets(bc, oc):
                issues.append(f'KEY CONFLICT between sources: kept "{sorted(bc)}" ({base["origin"]}: {base["source"][:50]}) but {o["origin"]} copy {o["id"]} says "{sorted(oc)}"')
        # key_source: if base was claude-keyed and we pulled official bits
        for fld in ('key_source', 'key_confidence'):
            pass
        for i in o.get('issues') or []:
            if i not in issues and o['origin'] != 'paper.is': issues.append(i)
        # review fields: a copy that already has syllabus tags / quality / review wins over an untagged base
        if not base.get('syllabus') and o.get('syllabus'):
            for fld in ('syllabus', 'quality', 'review_note', 'reviewed'):
                if o.get(fld) is not None: base[fld] = o[fld]
            issues = list(dict.fromkeys(issues + [i for i in (o.get('issues') or [])]))
        for im in o.get('images') or []:
            pass
    if len(marks) > 1: issues.append(f'marks differ between copies ({sorted(marks)}); kept {base["marks"]}')
    if base.get('_paper') in ('nesa-hsc-familiarisation', 'nesa-hsc-sample-exam') or any(o.get('_paper') in ('nesa-hsc-familiarisation', 'nesa-hsc-sample-exam') for o in others):
        if base['origin'] != 'NESA': notes.append(f"origin {base['origin']} -> NESA (NESA's own paper)"); base['origin'] = 'NESA'; base['publisher'] = 'NESA'
    bank_members = [e for e in es if e['_src'] == 'bank']
    if base['_src'] == 'cand' and bank_members:   # keep the stable bank id
        also = [a for a in also if f'[{bank_members[0]["id"]}]' not in a] + [describe(base)]
        base['id'] = bank_members[0]['id']
        if bank_members[0].get('source') and base['_src'] == 'cand': notes.append(f'adopted id of {base["id"]}')
    base['also_in'] = also
    base['issues'] = issues
    if notes: base['merge_note'] = '; '.join(notes)
    base['_cluster'] = [e['id'] for e in es]
    merged.append(base)
    log.append({'kept': base['id'], 'dropped': [e['id'] for e in others], 'notes': notes, 'sim': [pairs[k] for k in pairs if k[0] in mem or k[1] in mem][:1]})
json.dump(merged, open(QB + '/tools/_merged_stage.json', 'w'), indent=1, ensure_ascii=False)
json.dump(log, open(QB + '/tools/_merge_log.json', 'w'), indent=1)
n_c_new = sum(1 for e in merged if e['_src'] == 'cand' and '_cluster' not in e)
print('entries', len(allx), '->', len(merged), '| clusters', len(log), '| brand-new candidates', n_c_new)
print(collections.Counter((e['_src'], bool(e.get('_cluster'))) for e in merged))
