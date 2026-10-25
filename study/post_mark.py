"""Answer the exam app's "Ask Claude" requests (results are pushed live to the page).

  python3 -I study/post_mark.py <request-id> <mark> <feedback.md>     # post a mark
  python3 -I study/post_mark.py reply <request-id> <message.md>       # reply in the question's chat
"""
import json, sys, urllib.request

def post(path, body):
    req = urllib.request.Request(f'http://localhost:7788/api/claude-mark/{path}', method='POST',
                                 data=json.dumps(body).encode(), headers={'content-type': 'application/json'})
    print(urllib.request.urlopen(req).read().decode())

if sys.argv[1] == 'reply':
    post(f'{sys.argv[2]}/message', {'from': 'claude', 'text': open(sys.argv[3]).read()})
else:
    rid, mark, fb = sys.argv[1], sys.argv[2], open(sys.argv[3]).read()
    post(f'{rid}/result', {'mark': float(mark) if '.' in mark else int(mark), 'feedback': fb})
