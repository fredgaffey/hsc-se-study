"""Regenerates coverage.md and _coverage_rows.json from bank.json (same logic as the end of build_bank.mjs)."""
import json
QB = '/Users/fred/gradeo/question_bank'
POINTS = json.load(open('/Users/fred/gradeo/study/syllabus_points.json'))
clean = json.load(open(QB + '/bank.json'))
def sec(i):
    if i == 'Y11': return 9998
    if i == 'OUT': return 9999
    return ['SSA', 'WEB', 'AUTO', 'PROJ'].index(i.split('-')[0]) * 100 + int(i.split('-')[1])
MC = {'MULTI_CHOICE', 'OBJECTIVE_RESPONSE', 'RICH_TABLE', 'SORTING_TABLE', 'MULTI_SELECT', 'DROPDOWN', 'SORTING'}
cov = {p['id']: dict(w=0, mc=0, q3=0, q3w=0, n=0, res=0) for p in POINTS}
for e in clean:
    for i in e['syllabus']:
        c = cov.get(i)
        if not c: continue
        if e['reserved']: c['res'] += 1; continue
        c['n'] += 1
        ismc = e['answer_type'] in MC
        c['mc' if ismc else 'w'] += 1
        if e['quality'] == 3:
            c['q3'] += 1
            if not ismc: c['q3w'] += 1
yr11 = sum(1 for e in clean if 'Y11' in e['syllabus']); outn = sum(1 for e in clean if 'OUT' in e['syllabus']); resn = sum(1 for e in clean if e['reserved'])
rows = [dict(p, **cov[p['id']]) for p in POINTS]
rows.sort(key=lambda r: (r['q3'], r['n'], sec(r['id'])))
L = ['# Syllabus coverage of the question bank', '',
     f'{len(clean)} unique question parts ({resn} reserved, {yr11} Year 11-only, {outn} old-SDD/out-of-syllabus). Each part is tagged with 1–2 syllabus points, so a part can count twice. "Objective" = multiple choice and other auto-marked formats (matching grids, dropdown tables, ordering); "Written" = short answer, extended response, code, SQL and drawing.', '',
     'Sorted by number of quality-3 (HSC-like) parts, fewest first, so gaps are at the top.', '',
     f'Counts exclude the {resn} RESERVED 2025 HSC parts (shown separately in the last column) and Year 11 / out-of-syllabus parts.', '',
     '| Point | Content | Written | Objective | Total | Quality 3 (all) | Quality 3 written | Reserved 2025 HSC |', '|---|---|---:|---:|---:|---:|---:|---:|']
for r in rows:
    t = r['text'].replace('|', '/')
    L.append(f"| {r['id']} | {t[:95]}{'…' if len(t) > 95 else ''} | {r['w']} | {r['mc']} | {r['n']} | {r['q3']} | {r['q3w']} | {r['res']} |")
json.dump([{k: r[k] for k in ('id', 'text', 'w', 'mc', 'n', 'q3', 'q3w')} for r in rows], open(QB + '/_coverage_rows.json', 'w'), indent=1, ensure_ascii=False)
weak = [r for r in rows if r['q3'] <= 1 or r['n'] <= 4]
now = [r for r in rows if r['q3w'] == 0]
L += ['', '## Weakest-covered points', '', 'Points with at most one HSC-like (quality 3) part, or four or fewer parts in total:', '']
for r in weak: L.append(f"- **{r['id']}** {r['text']} — {r['n']} parts ({r['w']} written, {r['mc']} objective), {r['q3']} quality 3")
L += ['', 'Points with no quality-3 written (short-answer/extended/code) question: ' + ', '.join(r['id'] for r in now) + '.']
open(QB + '/coverage.md', 'w').write('\n'.join(L) + '\n')
print('\n'.join(L[:30])); print(len(weak), [r['id'] for r in weak]); print([r['id'] for r in now])
