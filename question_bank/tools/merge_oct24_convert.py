"""Stage 1 of the 24 Oct merge: convert private_papers/*/exam.json parts into bank-format entries.
Writes tools/_merge_candidates.json. Images are copied into assets/ with unique 'pp-<paper>-' names."""
import json, glob, os, re, html, shutil, sys
ROOT = '/Users/fred/gradeo'; QB = ROOT + '/question_bank'; PP = ROOT + '/private_papers'
PUB = {'cssa-2025-trial': 'CSSA', 'cssa-familiarisation': 'CSSA', 'nsw-doe-sample-exam': 'NSW Department of Education',
       'nesa-hsc-familiarisation': 'NESA', 'nesa-hsc-sample-exam': 'NESA', 'girraween-trial': 'Girraween High School',
       'merewether-trial': 'Merewether High School', 'normanhurst-trial': 'Normanhurst Boys High School',
       'north-sydney-boys-trial': 'North Sydney Boys High School', 'independent-trial': 'Independent Trial Exams',
       'nsw-software-engineering-paper': None, 'preliminary-year-11-paper': 'Baulkham Hills High School (BHHS)'}

def cell(s):
    s = re.sub(r'<br\s*/?>|</p>', '\n', s or ''); s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'[ \t  ]+', ' ', html.unescape(s)).strip()
def tidy(s):
    if s is None: return None
    s = html.unescape(s).replace(' ', ' ').replace(' ', ' ')
    s = re.sub(r'[ \t]+\n', '\n', s); s = re.sub(r'\n{3,}', '\n\n', s).strip()
    return s or None

def convert(slug):
    e = json.load(open(f'{PP}/{slug}/exam.json'))
    out = []
    for q in e['questions']:
        for pi, p in enumerate(q['parts']):
            qq = p.get('question') or {}
            at = p['answer_type']
            ent = {'id': 'pp-' + p['part_id'], 'origin': 'paper.is', 'reserved': False,
                   'source': f"{e['exam']} (paper.is, via SEN Discord) Q{q['number']}" + (f" {p['part']}" if p['part'] and p['part'] != f"Question {q['number']}" else ''),
                   'source_paper': e['exam'], 'publisher': PUB.get(slug), 'question_title': q['title'], 'part': p['part'],
                   '_paper': slug, '_qno': q['number'], '_pidx': pi}
            st = tidy(q.get('stimulus'))
            ent['stimulus'] = st
            pr = tidy(p['prompt'])
            for im in (q.get('stimulus_images') or []):
                ent.setdefault('_extra_images', []).append(im)
            ent['prompt'] = pr
            ent['marks'] = p['marks_available']
            t = at
            if t is None: t = 'SHORT'; ent['_type_guess'] = True
            if t == 'PSEUDOCODE': t = 'CODING'; ent['language'] = 'PSEUDOCODE'
            ent['answer_type'] = t
            if at == 'MULTI_CHOICE':
                ent['options'] = [{'letter': o['letter'], 'text': tidy(o['text']), 'image': o.get('image'), 'correct': bool(o['correct'])} for o in qq['options']]
                nc = sum(o['correct'] for o in ent['options'])
                ent['_ncorrect'] = nc
                if nc > 1: ent['answer_type'] = 'MULTI_SELECT'
            elif at == 'OBJECTIVE_RESPONSE':
                ent['objective'] = {'columns': [cell(c) for c in qq['columns']], 'rows': [{'statement': cell(r['statement']), 'correct': [cell(c) for c in r['correct']]} for r in qq['rows']]}
            elif at == 'RICH_TABLE':
                ent['table'] = [[({'type': c['type'], 'text': cell(c.get('text'))} if c['type'] == 'text' else
                                  {'type': c['type'], 'options': c.get('options'), 'correct': c.get('correct')} if c['type'] == 'dropdown' else c) for c in row] for row in qq['table']]
            elif at == 'SORTING_TABLE':
                rp = qq['raw_parameters']; ent['sorting'] = rp
            elif at == 'CODING':
                ent['language'] = qq.get('language'); 
                if qq.get('starter_code'): ent['starter_code'] = qq['starter_code']
            elif at == 'SQL':
                ent['dataset_setup_sql'] = qq.get('dataset_setup_sql'); 
                if qq.get('starter_query'): ent['starter_query'] = qq['starter_query']
            elif at == 'SHORT':
                if qq.get('word_limit'): ent['word_limit'] = qq['word_limit']
                if qq.get('accepted_answers'): ent['accepted_answers'] = qq['accepted_answers']
            if ent['answer_type'] == 'SHORT' and (p['marks_available'] or 0) >= 6: ent['extended'] = True
            crit = p.get('marking_criteria')
            if crit: ent['criteria'] = [{'marks': c.get('marks'), 'criterion': tidy(c.get('criterion'))} for c in crit]
            ent['rubric'] = tidy(p.get('marking_rubric')); ent['guidance'] = tidy(p.get('marking_guidance'))
            ent['sample_answer'] = tidy(p.get('sample_answer'))
            ent['_imgs'] = list(p.get('prompt_images') or []) + list(p.get('sample_answer_images') or [])
            ent['sample_answer_images'] = list(p.get('sample_answer_images') or [])
            ent['_raw_syl'] = p.get('syllabus')
            out.append(ent)
    return out

IMG_RE = re.compile(r'assets/[^)\s"\'<>]+')
def fix_images(ent, slug):
    """copy images referenced in any string of the entry to question_bank/assets with unique names"""
    used = []
    extra = ent.pop('_extra_images', [])
    def rep(m):
        rel = m.group(0); src = f'{PP}/{slug}/{rel}'
        if not os.path.exists(src): ent.setdefault('issues', []).append(f'image missing in source paper: {rel}'); return rel
        new = f'assets/pp-{slug}-' + os.path.basename(rel).replace(' ', '_')
        if not os.path.exists(f'{QB}/{new}'): shutil.copy(src, f'{QB}/{new}')
        if new not in used: used.append(new)
        return new
    def walk(x):
        if isinstance(x, str): return IMG_RE.sub(rep, x)
        if isinstance(x, list): return [walk(i) for i in x]
        if isinstance(x, dict): return {k: walk(v) for k, v in x.items()}
        return x
    for k in list(ent):
        if k in ('id',): continue
        ent[k] = walk(ent[k])
    # extra images (stimulus_images) are listed as paths that may not be in text
    for im in extra:
        if isinstance(im, dict): im = im.get('src') or im.get('path') or ''
        if im and IMG_RE.fullmatch(im):
            r = rep(IMG_RE.match(im))
            ent['stimulus'] = ((ent['stimulus'] + '\n\n') if ent['stimulus'] else '') + f'![]({r})'
    ent['images'] = used
    ent.pop('_imgs', None)

if __name__ == '__main__':
    allc = []
    for d in sorted(glob.glob(PP + '/*/exam.json')):
        slug = d.split('/')[-2]
        for ent in convert(slug):
            fix_images(ent, slug); allc.append(ent)
    json.dump(allc, open(QB + '/tools/_merge_candidates.json', 'w'), indent=1, ensure_ascii=False)
    print(len(allc))
