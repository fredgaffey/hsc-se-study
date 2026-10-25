"""Hand-transcribed entries for papers/2026 TH Software Tuition SE Trial.pdf (text layer, no marking guidelines).
MC keys are Claude's (key_source 'claude'); Q12 left unkeyed because the cost multiple depends on an unnamed source."""
import json
SRC = '2026 TH Software Tuition SE Trial.pdf'
def base(sec, n, prompt, marks, **kw):
    e = {'id': f'th-{sec.lower()}{n:02d}', 'origin': 'TH Software Tuition', 'reserved': False,
         'source': f'TH Software Tuition 2026 SE Trial (papers/{SRC}) Section {sec} Q{n}', 'source_paper': 'TH Software Tuition 2026 SE Trial',
         'publisher': 'TH Software Tuition', 'question_title': f'TH Trial Section {sec} Question {n}', 'part': f'Question {n}',
         'stimulus': None, 'prompt': prompt, 'marks': marks, 'images': [], '_paper': 'th-trial'}
    e.update(kw); return e
mc = [
 ('What is a key feature of progressive web apps (PWAs)?', ['Require a constant Internet connection', 'Can be installed like native apps', 'Only work in Internet Explorer', 'Do not use JavaScript'], 'B'),
 ('Which language is typically used for client-side programming?', ['SQL', 'PHP', 'Python', 'JavaScript'], 'D'),
 ('Which record types map a hostname to an IPv4 or IPv6 address?', ['MX and SRV', 'NS and SOA', 'A and AAAA', 'CNAME and TXT'], 'C'),
 ('Which protocol and default port does HTTPS use?', ['HTTP over UDP, port 80', 'HTTP over TLS on TCP, port 443', 'TLS over UDP, port 443', 'HTTP over TCP, port 80'], 'B'),
 ('Which is true about TCP vs UDP?', ['TCP establishes a connection and guarantees ordered delivery; UDP does not', 'Both TCP and UDP use handshakes', 'Both TCP and UDP retransmit lost packets by default', 'UDP guarantees delivery and ordering; TCP does not'], 'A'),
 ('What does TLS primarily provide?', ['Confidentiality, integrity, authentication', 'Compression, routing, congestion control', 'Name resolution, caching, negative responses', 'Load balancing, multiplexing, prioritisation'], 'A'),
 ('Place these in the correct order for a first HTTPS request with a cold DNS cache: DNS resolution, TCP handshake, TLS handshake, HTTP request.', ['TCP handshake, DNS resolution, HTTP request, TLS handshake', 'HTTP request, TCP handshake, TLS handshake, DNS resolution', 'DNS resolution, TCP handshake, TLS handshake, HTTP request', 'TLS handshake, DNS resolution, HTTP request, TCP handshake'], 'C'),
 ('Which of the following is an INDIRECT cost of a security breach?', ['Customer churn and reputation damage', 'Customer notification expenses', 'Incident response and forensics', 'Legal fees and regulatory fines'], 'A'),
 ('Which of the following is a business benefit of strong security, beyond simply "avoiding attacks"?', ['It always slows down every feature with no other benefit', 'It removes the need for regulatory compliance', 'It has no effect on customer behaviour', 'It can build customer trust and act as a market differentiator'], 'D'),
 ('A weak password policy that allows "password123" as a valid password is an example of which type of security failure?', ['Process failure', 'Human failure', 'Not a security failure', 'Technical failure'], 'A'),
 ('Which STRIDE category describes an attacker gaining higher access than they were intended to have?', ['Spoofing', 'Repudiation', 'Elevation of privilege', 'Denial of service'], 'C'),
 ('Roughly how much more expensive is it, on average, to fix a security flaw in production compared to preventing it at the design phase?', ['There is no meaningful difference', 'About 5 times', 'About 15 times', 'About 48 times'], None),
 ('Which STRIDE category describes an attacker pretending to be someone else?', ['Elevation of privilege', 'Spoofing', 'Tampering', 'Information disclosure'], 'B'),
 ('What does the "security-usability paradox" describe?', ['Usability has no relationship to security', 'Users always prefer the most secure option available', 'Security and usability always improve together', 'Overly difficult security controls often get bypassed, creating new vulnerabilities'], 'D'),
 ('Which statement correctly describes the relationship between AI and ML?', ['ML is a subset of AI', 'AI is a subset of ML', 'AI and ML are exactly the same thing', 'AI and ML are unrelated, separate fields'], 'A'),
 ('Which of the following is an example of AI that is NOT machine learning?', ['A spam filter that learns from labelled examples', 'A recommendation system trained on user data', 'A rule-based expert system with hand-coded decision rules', 'An image classifier trained on thousands of photos'], 'C'),
 ('Which type of automation focuses on redesigning and optimising an entire end-to-end business process, often integrating multiple systems?', ['RPA', 'BPA', 'Manual processing', 'None of the above'], 'B'),
 ('Which ML training paradigm uses ONLY labelled data, where every example has a known correct answer?', ['None of the above', 'Unsupervised learning', 'Supervised learning', 'Reinforcement learning'], 'C'),
 ('Which ML training paradigm is most suitable for grouping customers into segments based on purchasing behaviour, with no predefined "correct" groups?', ['Reinforcement learning', 'None of the above', 'Supervised learning', 'Unsupervised learning'], 'D'),
]
out = []
for n, (pr, opts, k) in enumerate(mc, 1):
    e = base('I', n, pr, 1, answer_type='MULTI_CHOICE', options=[{'letter': 'ABCD'[i], 'text': t, 'image': None, 'correct': 'ABCD'[i] == k} for i, t in enumerate(opts)])
    if k: e['key_source'] = 'claude'; e['key_confidence'] = 'medium' if n in (10,) else 'high'
    else: e['issues'] = ['no key: the paper has no marking guidelines and the cost multiple depends on an unnamed source (commonly quoted figures are 6x/15x/100x), so no option was marked correct']
    if n == 10: e.setdefault('issues', []).append('key (A, process failure) is Claude\'s: a policy that permits weak passwords is a process failure, but B (human failure) is arguable')
    out.append(e)
sa = [
 (3, 'Trace through the SQL query below and explain exactly what it returns, describing the effect of each clause in order.\n\n```sql\nSELECT category_id, COUNT(*)\nFROM posts\nWHERE published = 1\nGROUP BY category_id;\n```', 'SQL', 'FROM posts selects the table; WHERE published = 1 keeps only published rows; GROUP BY category_id groups the remaining rows by category; SELECT returns one row per category_id with COUNT(*), the number of published posts in that category.'),
 (3, 'The query below is intended to join every post to its author’s username, but it contains a syntax error. Identify the error and rewrite the query correctly.\n\n```sql\nSELECT users.username, posts.title\nFROM users\nINNER JOIN posts WHERE users.id = posts.author_id;\n```', 'SQL', 'The INNER JOIN has no ON clause (WHERE cannot supply the join condition). Corrected: SELECT users.username, posts.title FROM users INNER JOIN posts ON users.id = posts.author_id;'),
 (2, 'Explain why DNS primarily uses UDP, but sometimes switches to using TCP instead. Give ONE specific reason TCP is used.', None, None),
 (3, 'List the THREE security guarantees TLS provides, and briefly explain what each one means in the context of a user logging into an online banking site.', None, None),
 (3, 'The Python code below builds a login query. Identify the vulnerability, and state exactly what a malicious user could type into "username" to bypass the password check entirely.\n\n```python\nquery = "SELECT * FROM users WHERE username = \'" + username + "\' AND password = \'" + password + "\'"\ncursor.execute(query)\n```', None, None),
 (3, 'The Flask endpoint below has a security flaw. Identify it, naming the specific security principle it violates, and describe the fix.\n\n```python\n@app.route("/api/orders/<order_id>")\ndef get_order(order_id):\n    order = db.get_order(order_id)\n    return jsonify(order)\n```', None, None),
 (3, 'The Flask route below transfers money but is vulnerable to CSRF. Identify what is missing, and rewrite the route to fix it.\n\n```python\n@app.route("/transfer", methods=["POST"])\ndef transfer_money():\n    amount = request.form["amount"]\n    to_account = request.form["to_account"]\n    process_transfer(current_user, to_account, amount)\n    return "Transfer complete"\n```', None, None),
 (2, 'A vulnerability is rated likelihood 2/5 and impact 5/5. Calculate the risk score and identify which risk-response category it falls into.', None, None),
 (3, 'Classify the following as a technical, process or human security failure, explaining your reasoning: an employee clicks a link in a phishing email and enters their company password on a fake login page.', None, None),
 (3, 'Trace the function below for an email where contains_urgent = True, sender = "colleague", has_deadline = True. State the exact return value, and list the sequence of branches taken.\n\n```python\ndef classify_email(email):\n    if email["contains_urgent"]:\n        if email["sender"] == "boss":\n            if email["has_deadline"]:\n                return "High priority"\n            else:\n                return "Medium priority"\n        else:\n            return "Medium priority"\n    else:\n        return "Low priority"\n```', 'CODING', 'Returns "Medium priority". Branches: contains_urgent is True (take the outer if); sender == "boss" is False (take the inner else); has_deadline is never tested.'),
 (3, 'Trace the predict() method below for a Perceptron object where weights = [0.5, -0.2], bias = 0.1, using the step activation function (output 1 if z ≥ 0, else 0). Calculate z and state the returned output for inputs = [4, 3].\n\n```python\ndef activate(self, z):\n    return 1 if z >= 0 else 0\n\ndef predict(self, inputs):\n    z = sum(w * x for w, x in zip(self.weights, inputs)) + self.bias\n    return self.activate(z)\n```', 'CODING', 'z = 0.5*4 + (-0.2)*3 + 0.1 = 2.0 - 0.6 + 0.1 = 1.5. Since 1.5 >= 0 the step function returns 1.'),
 (2, 'Explain what RPA is, using the phrase "simulates user actions" in your answer.', None, None),
]
for n, (m, pr, kind, ans) in enumerate(sa, 1):
    e = base('II', n, pr, m, answer_type='SHORT', extended=False)
    if ans:
        e['sample_answer'] = ans; e['key_source'] = 'claude'; e['key_confidence'] = 'high'
    else:
        e['issues'] = ['no marking guidelines or sample answer in the source paper']
    out.append(e)
er = [
 (4, 'A company is building a live video-conferencing feature into their web application. Recommend whether the underlying transport should use TCP or UDP, and justify your answer using at least TWO specific characteristics of the chosen protocol.'),
 (4, 'Explain TWO reasons a development team should use HTTPS instead of plain HTTP for their web application, even if the application does not process payments.'),
 (4, 'The Python function below is vulnerable to SQL injection. Rewrite it using a parameterised query so it is safe.\n\n```python\ndef find_user(username):\n    query = "SELECT * FROM users WHERE username = \'" + username + "\'"\n    return cursor.execute(query).fetchone()\n```'),
 (4, 'Using the risk = likelihood × impact model, explain why a company should sometimes invest more in preventing a LOW-likelihood risk than a HIGH-likelihood one, using a specific example.'),
 (5, 'The train_one() method below is missing its weight and bias update logic. Complete the method so it correctly implements the perceptron learning rule: wᵢ = wᵢ + α(target − prediction) × xᵢ, and the equivalent update for the bias.\n\n```python\nclass Perceptron:\n    def __init__(self, num_inputs, learning_rate=0.1):\n        self.weights = [0.0] * num_inputs\n        self.bias = 0.0\n        self.lr = learning_rate\n\n    def predict(self, inputs):\n        z = sum(w * x for w, x in zip(self.weights, inputs)) + self.bias\n        return 1 if z >= 0 else 0\n\n    def train_one(self, inputs, target):\n        prediction = self.predict(inputs)\n        # TODO: update self.weights and self.bias here\n        pass\n```'),
 (6, 'Choose ONE concept from Programming for the Web, ONE from Secure Software Architecture, and ONE from Software Automation studied this year, and explain how they connect to a single, unifying idea: that good software engineering requires deliberately weighing trade-offs using specific, named factors rather than following one "default" answer. Use a specific example from each strand.'),
]
for n, (m, pr) in enumerate(er, 1):
    e = base('III', n, pr, m, answer_type='CODING' if n in (3, 5) else 'SHORT', extended=True)
    if n in (3, 5): e['language'] = 'PYTHON'; e['extended'] = False
    e['issues'] = ['no marking guidelines or sample answer in the source paper']
    out.append(e)
e = out[-1]; 
if n == 5: pass
if __name__ == '__main__':
    json.dump(out, open('/Users/fred/gradeo/question_bank/tools/th_entries.json', 'w'), indent=1, ensure_ascii=False); print(len(out), sum(x['marks'] for x in out))
