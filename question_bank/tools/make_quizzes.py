# Creates Gradeo quizzes (same POST /exam-edit/quiz call the "Generate quiz" button makes, createExamSession:true,
# no timer) from the enumerated quiz pool, 50 questions each, then reads each quiz's questions + answers from
# marking-session/question/<markingSessionId>. Never starts a session, never saves answers.
import json, time, urllib.request, sys, os, glob
B = 'http://127.0.0.1:7777'
SY = 'd1a54432-597e-4e3c-a5c6-ad7a134726e4'
RAW = '/Users/fred/gradeo/question_bank/raw/'
LOG = RAW + 'quizzes_created.json'
last = [0.0]
def throttle():
    dt = time.time() - last[0]
    if dt < 0.6: time.sleep(0.6 - dt)
    last[0] = time.time()
def get(p):
    throttle()
    with urllib.request.urlopen(B + '/api/' + p) as r: return json.load(r)
def ev(js):
    throttle()
    req = urllib.request.Request(B + '/eval', data=js.encode(), method='POST')
    with urllib.request.urlopen(req) as r: return json.load(r)
def create(ids):
    body = json.dumps({'title': 'Generated quiz ' + time.strftime('%Y-%m-%d %H:%M:%S'), 'syllabusId': SY, 'questionIds': ids,
                       'showTimer': False, 'readingTimeLimitSeconds': None, 'workingTimeLimitSeconds': None, 'createExamSession': True})
    js = f"""(async()=>{{const k=Object.keys(localStorage).find(k=>k.startsWith('@@auth0spajs@@')&&k.includes('api.portal.gradeo.com.au'));
const t=JSON.parse(localStorage[k]).body.access_token; const id=crypto.randomUUID();
const r=await fetch('/api/exam-edit/quiz',{{method:'POST',headers:{{'content-type':'application/json',authorization:'Bearer '+t,'x-request-id':id,'x-correlation-id':id,'correlation-id':id}},body:{json.dumps(body)}}});
return {{status:r.status, body:await r.text()}};}})()"""
    return ev(js), json.loads(body)['title']
log = json.load(open(LOG)) if os.path.exists(LOG) else []
have = set()
for f in glob.glob(RAW + 'quizq_*.json'):
    for q in json.load(open(f)).get('questions', []): have.add(q['id'])
existing_ids = set()
for f in glob.glob('/Users/fred/gradeo/gradeo_out/raw/*-*.json'):
    for q in json.load(open(f)).get('questions') or []: existing_ids.add(q['id'])
pool = json.load(open(RAW + 'quiz_pool_summary.json'))
used = {i for e in log for i in e['questionIds']}
todo = [x['id'] for x in pool if x['id'] not in used and x['id'] not in existing_ids]
n = int(sys.argv[1]) if len(sys.argv) > 1 else 1
print('todo', len(todo))
for k in range(n):
    ids = todo[k*50:(k+1)*50]
    if not ids: break
    res, title = create(ids)
    print(title, res['status'], res['body'][:200], flush=True)
    if res['status'] != 200: break
    b = json.loads(res['body'])
    entry = {'title': title, 'examId': b['examId'], 'examSessionId': b['examSessionId'], 'questionIds': ids, 'created': time.strftime('%Y-%m-%dT%H:%M:%S')}
    log.append(entry); json.dump(log, open(LOG, 'w'), indent=1)
# resolve marking-session ids and fetch questions
sess = []
for off in range(0, 1000, 50):
    d = get(f'exam-process/session-participant?limit=50&offset={off}'); sess += d['list']
    if len(sess) >= d['pgn']['total'] or not d['list']: break
for e in log:
    s = next((s for s in sess if s['session']['id'] == e['examSessionId']), None)
    if not s: print('no session row for', e['title']); continue
    e['markingSessionId'] = s['markingSessionId']; e['status'] = s['status']
    out = RAW + f"quizq_{e['markingSessionId']}.json"
    if not os.path.exists(out):
        qs = get(f"marking-session/question/{e['markingSessionId']}")
        json.dump({'title': e['title'], 'markingSessionId': e['markingSessionId'], 'questions': qs}, open(out, 'w'))
        print('fetched', e['title'], len(qs), 'questions; status', s['status'])
json.dump(log, open(LOG, 'w'), indent=1)
