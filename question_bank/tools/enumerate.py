# Read-only: enumerate every question ID Gradeo's quiz generator can draw from (Software Engineering, Y12),
# by slicing the bank by syllabus item / subtopic / answer type until each slice is <=50 (the summary cap).
import json, time, urllib.request, urllib.parse, sys
B = 'http://127.0.0.1:7777/api/'
SY = 'd1a54432-597e-4e3c-a5c6-ad7a134726e4'
OUT = '/Users/fred/gradeo/question_bank/raw/'
last = [0.0]
def get(p):
    dt = time.time() - last[0]
    if dt < 0.6: time.sleep(0.6 - dt)
    last[0] = time.time()
    with urllib.request.urlopen(B + p) as r: return json.load(r)
def q(**kw):
    parts = [('syllabusId', SY)]
    for k, v in kw.items():
        if isinstance(v, list):
            parts += [(f'{k}[{i}]', x) for i, x in enumerate(v)]
        else: parts.append((k, v))
    return urllib.parse.urlencode(parts)
TYPES = ['MULTI_CHOICE','SHORT','EXTENDED','CODING','DRAWING_V2','DRAWING','OBJECTIVE_RESPONSE','RICH_TABLE','SQL','NUMERIC','IMAGE','SORTING_TABLE','SPREADSHEET','EQUATION']
syl = get(f'syllabus/{SY}')
json.dump(syl, open(OUT + 'syllabus_gradeo.json', 'w'), indent=1)
summ, tags = {}, {}
def grab(label, **kw):
    n = get('question-bank/question-many-quiz/count?' + q(**kw))['questionCount']
    if n == 0: return 0, True
    got = set()
    for attempt in range(1 if n <= 50 else 6):
        for x in get('question-bank/question-many-quiz/summary?' + q(questionCount=50, **kw)):
            summ[x['id']] = x; got.add(x['id']); tags.setdefault(x['id'], set()).add(label)
        if len(got) >= n: break
    return n, len(got) >= n
total = get('question-bank/question-many-quiz/count?' + q())['questionCount']
print('total', total)
for t in syl['topics']:
    for st in t['subtopics']:
        for it in st['items']:
            n, full = grab('item:' + it['id'], subtopicItemIds=[it['id']])
            if not full:
                for ty in TYPES:
                    grab('item:' + it['id'], subtopicItemIds=[it['id']], answerTypeList=[ty])
            print(f"{st['title'][:30]:30} {it['text'][:50]:50} n={n} full={full} union={len(summ)}", flush=True)
        n, full = grab('sub:' + st['id'], subtopicIds=[st['id']])
        print('SUBTOPIC', st['title'], n, full, len(summ), flush=True)
# anything not reachable via items: slice by type, then random draws
for ty in TYPES:
    n, full = grab('type:' + ty, answerTypeList=[ty]); print('TYPE', ty, n, full, len(summ), flush=True)
for i in range(30):
    if len(summ) >= total: break
    grab('random'); print('random', len(summ), flush=True)
for k in summ: summ[k]['_slices'] = sorted(tags.get(k, []))
json.dump(list(summ.values()), open(OUT + 'quiz_pool_summary.json', 'w'), indent=1)
print('DONE', len(summ), 'of', total)
