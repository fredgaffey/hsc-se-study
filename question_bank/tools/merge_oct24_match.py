"""Near-duplicate detection used by merge_oct24_build.py.
Two parts are duplicates when prompt, stimulus and option/grid text are each >= 0.9 similar (difflib, after normalising
case, markdown/HTML, punctuation and whitespace) and, where both have images, the images are (mostly) the same files."""
import re, html, difflib, hashlib, os
QB = '/Users/fred/gradeo/question_bank'
def strip(s):
    s = html.unescape(s or ''); s = re.sub(r'!\[[^\]]*\]\([^)]*\)', ' ', s); s = re.sub(r'<[^>]+>', ' ', s)
    s = re.sub(r'\\([_*#\[\]()])', r'\1', s)
    s = re.sub(r'\b(refer to the stimulus|marks)\b', ' ', s.lower())
    s = re.sub(r'[*_`#|>\\~-]', ' ', s)
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9 ]', '', s)).strip()
def opts_text(e):
    if e.get('options'): return ' '.join(sorted(strip(o.get('text') or '') for o in e['options']))
    if e.get('objective'): return ' '.join(sorted(strip(r['statement']) for r in e['objective']['rows'])) + ' ' + ' '.join(sorted(strip(c) for c in e['objective']['columns']))
    if e.get('table'): return ' '.join(sorted(strip(c.get('text', '')) for r in e['table'] for c in r if c.get('type') == 'text'))
    if e.get('sorting'):
        s = e['sorting']
        if 'rows' in s: return ' '.join(sorted(strip(c['text']) for r in s['rows'] for c in r['cells']))
        return ' '.join(sorted(strip(x) for x in s.get('items', [])))
    return ''
_h = {}
def fhash(rel):
    if rel not in _h:
        p = f'{QB}/{rel}'
        _h[rel] = hashlib.md5(open(p, 'rb').read()).hexdigest() if os.path.exists(p) else rel
    return _h[rel]
def imgs_of(e):
    s = set(e.get('images') or [])
    return {fhash(i) for i in s}
def prep(e):
    return {'p': strip(e.get('prompt')), 's': strip(e.get('stimulus')), 'o': opts_text(e), 'im': imgs_of(e)}
def r(a, b):
    if a == b: return 1.0
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()
def compare(a, b):
    """-> (is_dup, score, note)"""
    if not a['p'] and not a['s'] or not b['p'] and not b['s']: return False, 0, ''
    pr = r(a['p'], b['p'])
    notes = []
    if pr < 0.9:
        # the stimulus is sometimes folded into the prompt on one side
        if bool(a['s']) != bool(b['s']) and r(a['s'] + ' ' + a['p'], b['s'] + ' ' + b['p']) >= 0.93 and not (a['o'] and b['o'] and r(a['o'], b['o']) < 0.9):
            return True, 0.93, 'stimulus folded into prompt on one side'
        return False, pr, ''
    if a['s'] and b['s']:
        st = r(a['s'], b['s'])
        if st < 0.9: return False, st, ''
    elif a['s'] or b['s']:
        # one side has a stimulus the other lacks (often the stimulus is folded into the prompt): need a very close prompt
        st = None
        if max(len(a['s']), len(b['s'])) > 40 and not (pr >= 0.97 and len(a['p']) >= 60): return False, pr * 0.9, ''
        notes.append('stimulus only on one side')
    else: st = 1
    if a['o'] and b['o']:
        op = r(a['o'], b['o'])
        if op < 0.9: return False, op, ''
    elif a['o'] or b['o']:
        if max(len(a['o']), len(b['o'])) > 30: return False, 0, ''
        op = 1
    else: op = 1
    if a['im'] and b['im'] and len(a['im'] & b['im']) / len(a['im'] | b['im']) < 0.5: return False, 0, 'different images'
    sc = min(x for x in (pr, st, op) if x is not None)
    return True, sc, '; '.join(notes)
