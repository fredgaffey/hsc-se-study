"""Post Claude's mark for an "Ask Claude to mark" request back to the exam app (pushed live to the page).

  python3 -I study/post_mark.py <request-id> <mark> <feedback.md>
"""
import json, sys, urllib.request

rid, mark, fb = sys.argv[1], sys.argv[2], open(sys.argv[3]).read()
req = urllib.request.Request(f'http://localhost:7788/api/claude-mark/{rid}/result', method='POST',
                             data=json.dumps({'mark': float(mark) if '.' in mark else int(mark), 'feedback': fb}).encode(),
                             headers={'content-type': 'application/json'})
print(urllib.request.urlopen(req).read().decode())
