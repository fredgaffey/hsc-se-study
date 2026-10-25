# Builds tools/nesa_entries.json: the NESA Software Engineering Familiarisation paper and the 2025 HSC paper,
# captured from fam.hsconline.nesa.nsw.edu.au (raw/nesa_*.json, converted by nesa_md.mjs) and cleaned by hand.
# 2025 HSC keys / criteria / sample answers: papers/marking/2025 HSC - Marking Guidelines (official).pdf and
# "Full-mark sample answers (official).pdf". Familiarisation paper keys: written by Claude (key_source "claude").
import json, re

L = lambda *xs: '\n'.join(xs)
def crit(*rows):  # rows: (marks, text)
    return [{'marks': str(m), 'criterion': t} for m, t in rows]
def opts(texts, correct):
    return [{'letter': 'ABCDEFGH'[i], 'text': t, 'image': None, 'correct': i in correct} for i, t in enumerate(texts)]

FAM = 'NESA HSC Software Engineering Familiarisation Questions (updated 30/01/2025)'
fam = []
def F(q, **kw):
    e = {'id': f'nesa-fam-q{q}', 'origin': 'NESA', 'reserved': False, 'source': f'{FAM} Q{q}', 'source_paper': FAM, 'publisher': 'NESA',
         'question_title': f'Familiarisation Question {q}', 'part': f'Question {q}', 'key_source': 'claude', 'quality': 3, 'issues': [], 'images': []}
    e.update(kw); fam.append(e)

F('1', prompt='Place the following software development steps in the correct order.\n\n- Design\n- Installation\n- Maintenance\n- Development\n- Testing and debugging\n- Determining specifications',
  answer_type='SORTING', marks=1,
  sorting={'items': ['Design', 'Installation', 'Maintenance', 'Development', 'Testing and debugging', 'Determining specifications'],
           'correct_order': ['Determining specifications', 'Design', 'Development', 'Testing and debugging', 'Installation', 'Maintenance']},
  criteria=crit((1, 'Places all six steps in the correct order')),
  sample_answer='Determining specifications → Design → Development → Testing and debugging → Installation → Maintenance',
  key_confidence='high', syllabus=['SSA-2'])

PRODUCTS = L('| ProductID | ProductName | ProductPrice |', '|---|---|---|', '| P001 | The Plant (DVD) | 28.00 |', '| P002 | Discovery 1 and 2 (DVD) | 26.98 |',
             '| P003 | Travel 1 and 2 (Blu-Ray) | 22.00 |', '| P004 | The Best Movie (DVD) | 19.98 |', '| P005 | Celebration (DVD) | 12.00 |')
COLS = ['Products', 'ProductID', 'ProductName', 'ProductPrice']
F('2', stimulus=L('An online business is planning to use a database to keep track of its products. The contents of the Products table during testing are shown.', '', '**Products**', '', PRODUCTS, '',
                  'After executing a SQL query, the following results were obtained.', '', '| ProductName | ProductPrice |', '|---|---|',
                  '| Discovery 1 and 2 (DVD) | 26.98 |', '| The Plant (DVD) | 28.00 |', '| Travel 1 and 2 (Blu-Ray) | 22.00 |'),
  prompt='Select the correct item from each dropdown menu to show how the results were obtained.\n\n`SELECT [1] , [2]`  \n`FROM [3]`  \n`WHERE [4] [5] [6]`  \n`ORDER BY [7] [8]`',
  answer_type='DROPDOWN', marks=3,
  dropdowns=[{'label': '1 (SELECT)', 'options': COLS, 'correct': ['ProductName']}, {'label': '2 (SELECT)', 'options': COLS, 'correct': ['ProductPrice']},
             {'label': '3 (FROM)', 'options': COLS, 'correct': ['Products']}, {'label': '4 (WHERE field)', 'options': COLS, 'correct': ['ProductPrice']},
             {'label': '5 (operator)', 'options': ['<', '=', '>=', '<=', '<>'], 'correct': ['>=']}, {'label': '6 (value)', 'options': ['12.00', '19.98', '22.00', '26.98', '28.00'], 'correct': ['22.00']},
             {'label': '7 (ORDER BY)', 'options': COLS, 'correct': ['ProductName']}, {'label': '8 (direction)', 'options': ['ASC', 'DESC'], 'correct': ['ASC']}],
  criteria=crit((3, 'Selects the correct fields, table, condition and ordering'), (2, 'Mostly correct (e.g. correct condition but incorrect ordering)'), (1, 'Some correct selections')),
  sample_answer='SELECT ProductName, ProductPrice FROM Products WHERE ProductPrice >= 22.00 ORDER BY ProductName ASC  (the results are in alphabetical order of name, and include the 22.00 product)',
  key_confidence='high', syllabus=['WEB-18'])

F('3', prompt='Match each of the features to the relevant protocol(s).', answer_type='OBJECTIVE_RESPONSE', marks=2,
  objective={'columns': ['POP3', 'SMTP', 'IMAP'], 'multi_select_per_row': True, 'rows': [
      {'statement': 'Commonly used for sending email', 'correct': ['SMTP']},
      {'statement': 'Commonly used for receiving email', 'correct': ['POP3', 'IMAP']},
      {'statement': 'Allows email to synchronise across devices', 'correct': ['IMAP']},
      {'statement': 'Server deletes messages when they are downloaded and opened', 'correct': ['POP3']}]},
  criteria=crit((2, 'Correctly matches all features'), (1, 'Correctly matches at least two features')), key_confidence='high', syllabus=['WEB-3'])

F('4', stimulus='This structure chart describes a hotel booking system.\n\n![](assets/fam_Q4s-1.png)', images=['assets/fam_Q4s-1.png', 'assets/fam_Q4s-1.svg'],
  prompt='Select the items that are TRUE about this structure chart. (Multiple items may be selected.)', answer_type='MULTI_SELECT', marks=2,
  options=opts(['**Booking made** is a flag.', '**Login** is the first module called.', '**Booking ID** may only be true or false.', '**Display new bookings** may not be executed.',
                'Members do not need to log in to browse hotels.', 'A choice is continually offered between **Browse hotels** and **Book**.',
                '**Login** calls **Enter member details and validate** when Member ID is set to true.'], {0, 1, 3, 5}),
  criteria=crit((2, 'Selects all TRUE statements and no FALSE statements'), (1, 'Selects at least two TRUE statements with at most one error')),
  sample_answer=L('TRUE: Booking made is a flag (filled circle = control parameter); Login is called first (modules execute left to right); Display new bookings may not be executed (diamond = selection); a choice is continually offered between Browse hotels and Book (diamond inside the "Until done" loop).',
                  'FALSE: Booking ID is a data parameter (open circle), not a flag; Login is always called before Browse hotels, so members must log in; Login repeats Enter member details and validate until Valid is true — Member ID is data, not a Boolean.'),
  key_confidence='medium-high (no official key; standard structure-chart conventions assumed)', syllabus=['PROJ-11'])

F('5', stimulus=L('Consider the following algorithm.', '', '```', 'BEGIN determineGrade', '    get Mark', '    CASEWHERE Mark', '        >=80 : Grade = "H"', '        >=50 : Grade = "P"',
                  '        OTHERWISE : Grade = "N"', '    ENDCASE', '    print Grade', 'End determineGrade', '```'),
  prompt='Use the following table to provide a set of test data that will thoroughly test the algorithm. Include the expected outputs and reasons for inclusion. You may assume that all input data are valid.\n\n| Test data (Mark) | Expected output (Grade) | Reason for inclusion |\n|---|---|---|\n| | | |\n| | | |\n| | | |\n| | | |\n| | | |',
  answer_type='RICH_TABLE', marks=3,
  criteria=crit((3, 'Provides test data covering each path and the boundaries (79/80 and 49/50) with correct expected outputs and reasons'),
                (2, 'Provides test data covering each path with correct expected outputs, OR boundary data with some reasons'), (1, 'Provides some appropriate test data or expected outputs')),
  sample_answer=L('| Mark | Grade | Reason |', '|---|---|---|', '| 90 | H | Typical value in the H range |', '| 80 | H | Boundary: lowest mark that gives H |',
                  '| 79 | P | Boundary: highest mark below H |', '| 50 | P | Boundary: lowest mark that gives P |', '| 49 | N | Boundary: highest mark that gives N (OTHERWISE path) |'),
  key_confidence='high', syllabus=['PROJ-24', 'PROJ-21'])

F('6', stimulus='A new operating system is to be developed for a mobile phone. The operating system needs to allow users to install a variety of third-party applications such as social media applications and games on the phone.',
  prompt='Discuss the use of *sandboxing* in this operating system.', answer_type='SHORT', marks=3, word_limit=70,
  criteria=crit((3, 'Discusses advantages AND disadvantages/limitations of sandboxing third-party apps in this operating system'),
                (2, 'Outlines how sandboxing works in the OS and a benefit OR limitation'), (1, 'Provides some relevant information about sandboxing')),
  sample_answer=('Sandboxing runs each third-party app in an isolated environment with its own storage and only the permissions it is granted, so a malicious or buggy game cannot read '
                 'other apps\' data or damage the operating system, protecting users\' privacy and system stability. However, isolation adds memory and processing overhead on a '
                 'resource-limited phone, and apps that legitimately need to share data (e.g. a social media app accessing photos) need extra permission mechanisms, which adds '
                 'complexity and can frustrate users if permissions are too restrictive.'),
  key_confidence='high', syllabus=['SSA-6'])

TREE_STIM = 'Consider the following decision tree of a trained machine learning model that determines whether to purchase a vehicle.\n\n![](assets/fam_SEFAM07S.png)'
F('7a', stimulus=TREE_STIM, images=['assets/fam_SEFAM07S.png'], part='Question 7 (a)',
  prompt='Using the decision tree, determine the outcome of each of the following situations.', answer_type='OBJECTIVE_RESPONSE', marks=1,
  objective={'columns': ['Buy', 'Do not buy'], 'rows': [
      {'statement': 'Mileage = 8000 km, Colour = Silver, Optional Accessories = No', 'correct': ['Buy']},
      {'statement': 'Mileage = 11 000 km, Colour = Red, Optional Accessories = Yes', 'correct': ['Buy']},
      {'statement': 'Type = SUV, Colour = Red, Optional Accessories = No', 'correct': ['Buy']}]},
  criteria=crit((1, 'Correct outcome for all three situations')),
  sample_answer='All three are Buy: 8000 km silver → Buy (whether or not it is an SUV); 11 000 km with accessories → Buy (SUV or not); any SUV → Buy.',
  key_confidence='high', syllabus=['AUTO-5'])
F('7b', stimulus=TREE_STIM, images=['assets/fam_SEFAM07S.png'], part='Question 7 (b)',
  prompt='The decision tree can be simplified without compromising its logic. Redraw the decision tree to reduce the number of branches.', answer_type='DRAWING', marks=3,
  criteria=crit((3, 'Draws a correct simplified tree with Type = SUV tested first (SUV → Buy), then mileage, with the Colour and Optional Accessories tests on the correct branches'),
                (2, 'Draws a simplified tree with minor errors'), (1, 'Shows some understanding of simplifying the tree')),
  sample_answer=L('Type = SUV?', '- Yes → Buy', '- No → Mileage < 10 000 km?', '  - Yes → Colour = Silver? (Yes → Buy; No → Do not buy)', '  - No → Optional Accessories? (Yes → Buy; No → Do not buy)',
                  '', 'Both original Type = SUV nodes lead to Buy on Yes, so Type can be tested once at the root (8 branches instead of 10).'),
  key_confidence='high', syllabus=['AUTO-5', 'PROJ-11'])

F('8', stimulus=L('The following subroutine is intended to search an array for an item and output the position of that item in the array. There are several mistakes in the algorithm.', '', '```',
                  'BEGIN Search (SearchItem)', '    Set LastIndex to the number of elements in ItemArray', '    Index = 1', '    WHILE Found = FALSE OR Index < LastIndex',
                  '        IF Index = SearchItem THEN', '            Found = TRUE', '        ENDIF', '    ENDWHILE', '    IF Found = TRUE THEN', "        Display 'Position', Index",
                  '    ELSE', "        Display 'Not found'", '    ENDIF', 'END Search', '```'),
  prompt='Copy the algorithm into the space below and modify the algorithm logic so that it achieves its intended purpose. The array is called ItemArray and it is indexed from 1.',
  answer_type='SHORT', marks=3,
  criteria=crit((3, 'Corrects all errors: initialises Found, uses AND and <= in the loop condition, compares ItemArray(Index) with SearchItem, increments Index'),
                (2, 'Corrects most of the errors'), (1, 'Corrects one error')),
  sample_answer=L('```', 'BEGIN Search (SearchItem)', '    Set LastIndex to the number of elements in ItemArray', '    Index = 1', '    Found = FALSE',
                  '    WHILE Found = FALSE AND Index <= LastIndex', '        IF ItemArray[Index] = SearchItem THEN', '            Found = TRUE', '        ELSE',
                  '            Index = Index + 1', '        ENDIF', '    ENDWHILE', '    IF Found = TRUE THEN', "        Display 'Position', Index", '    ELSE', "        Display 'Not found'",
                  '    ENDIF', 'END Search', '```'),
  key_confidence='high', syllabus=['PROJ-15'])

REG = L('An online store allows users to register for an account using their name, phone number and date of birth. Users must also create a username and password.', '',
        'Each username must satisfy these rules.', '', '- There must be no more than 8 characters.', '- Only uppercase and lowercase letters are accepted.',
        '- The character “<” is not allowed, to prevent attempts at injecting code through the username.')
F('9a', stimulus=REG, part='Question 9 (a)', prompt='Design a user interface for registering an account. Clearly label all features.', answer_type='DRAWING', marks=3,
  criteria=crit((3, 'Designs a clear, labelled registration screen with all required fields, appropriate input controls (e.g. date picker) and guidance on the username rules / feedback'),
                (2, 'Designs a screen with most required fields and some labels'), (1, 'Provides a basic screen layout')),
  sample_answer=L('Labelled screen "Create account": text boxes for Name, Phone number (numeric keypad/format hint), Date of birth (date picker), Username (with hint "max 8 letters, A–Z/a–z only"),',
                  'Password and Confirm password (masked, show/hide toggle, strength meter); inline error messages next to invalid fields; Register button (disabled until valid) and Cancel/Back link; consistent fonts and colours, logical top-to-bottom tab order.'),
  key_confidence='high', syllabus=['WEB-21', 'PROJ-20'])
F('9b', stimulus=REG, part='Question 9 (b)', prompt='Write a function in Python that will check whether a username satisfies the rules.', answer_type='CODING', language='PYTHON', marks=3,
  criteria=crit((3, 'Correct function that checks length ≤ 8 and that every character is an upper/lowercase letter, returning a correct result'),
                (2, 'Function checks most rules correctly'), (1, 'Shows some understanding of the problem or Python')),
  sample_answer=L('```python', 'def valid_username(username):', '    if len(username) == 0 or len(username) > 8:', '        return False', '    for ch in username:',
                  "        if not ('a' <= ch <= 'z' or 'A' <= ch <= 'Z'):   # also rejects '<'", '            return False', '    return True', '```'),
  key_confidence='high', syllabus=['SSA-10', 'PROJ-15'])

F('10', stimulus=L('Consider the following source code for a web page.', '', '```html', '<html>', '<body>', '<link rel="stylesheet" href="style3.css"/>',
                   '<script src="image-gallery.js"/><!--this script is slow to load-->', '<link rel="stylesheet" href="styles1.css"/>', '<link rel="stylesheet" href="styles2.css"/>',
                   '<h1>My Awesome Website!</h1>', '<p>I hope you like my website, I spent a lot of time designing it.</p>', '<h2>Photos from my holiday</h2>',
                   '<img src="holiday1_4000x3000.jpg" width="640" height="480"/>', '<img src="holiday2_4000x3000.jpg" width="640" height="480"/>',
                   '<img src="holiday3_4000x3000.jpg" width="640" height="480"/>', '<img src="holiday4_4000x3000.jpg" width="640" height="480"/>', '</body>', '</html>', '```'),
  prompt='The web page is loading too slowly. Explain how the load time of this page can be improved.', answer_type='SHORT', marks=4, word_limit=90,
  criteria=crit((4, 'Explains at least two relevant improvements related to the code (e.g. image sizes, script loading, combining/minifying CSS) and why each reduces load time'),
                (3, 'Explains one improvement and outlines another'), (2, 'Outlines one or more improvements'), (1, 'Provides some relevant information')),
  sample_answer=('The images are 4000×3000 but displayed at 640×480, so resizing/compressing them to the display size (or using lazy loading) greatly reduces the data downloaded. '
                 'The slow image-gallery.js script blocks rendering because it is loaded before the content; moving it to the end of the body or adding async/defer lets the text display first. '
                 'The three stylesheets could be combined and minified into one file in the <head>, reducing the number of HTTP requests, and caching/CDNs would speed repeat visits.'),
  key_confidence='high', syllabus=['WEB-13'])

XSS = L('Bob is testing a website for vulnerability. The website allows the user to add their name at the end of the URL and prints their name on the webpage.', '',
        'In addition to his name, Bob has added some code to the URL and the following is displayed.', '', '![](assets/fam_SEFAM11S.png)', '',
        '(The URL is `localhost:8080/Bob<script>alert("Is this supposed to happen")</script>`; the page shows "Hello, Bob." and an alert box "Is this supposed to happen?")')
F('11a', stimulus=XSS, images=['assets/fam_SEFAM11S.png'], part='Question 11 (a)', prompt='What type of vulnerability is being demonstrated?', answer_type='MULTI_CHOICE', marks=1,
  options=opts(['Invalid redirecting', 'Cross site scripting', 'Broken authentication', 'Cross site request forgery'], {1}), key_confidence='high', syllabus=['SSA-13'])
F('11b', stimulus=XSS, images=['assets/fam_SEFAM11S.png'], part='Question 11 (b)', prompt='Explain ONE way to minimise this vulnerability.', answer_type='SHORT', marks=2, word_limit=35,
  criteria=crit((2, 'Explains a relevant way to minimise XSS and how it prevents the script running'), (1, 'Identifies a relevant way')),
  sample_answer='Sanitise/encode user input before displaying it: characters such as < and > are escaped (e.g. &lt;script&gt;), so the browser displays the text instead of executing it as a script.',
  key_confidence='high', syllabus=['SSA-13', 'SSA-10'])

DB = L('An online business is planning to use a database to keep track of its products, customers and orders. The contents of the Products, Customers and Orders tables during testing are shown.', '',
       '**Products**', '', PRODUCTS, '', '**Customers**', '', '| CustID | CustName | CustEmail |', '|---|---|---|', '| C001 | Nicky Singh | N.Singh@nesa.edu.au |', '| C002 | Casey He | C.He@bos.edu.au |',
       '| C003 | Ash Lee | A.Lee@bosnsw.edu |', '| C004 | Kim Smith | K.Smith@nesa.edu.au |', '| C005 | Pat Alvardo | P.Alvardo@bos.edu.au |', '', '**Orders**', '',
       '| OrderID | CustID | ProductID | OrderQuantity |', '|---|---|---|---|', '| T001 | C001 | P004 | 2 |', '| T002 | C004 | P005 | 1 |', '| T003 | C002 | P003 | 1 |',
       '| T004 | C001 | P002 | 2 |', '| T005 | C005 | P002 | 2 |')
F('12a', stimulus=DB, part='Question 12 (a)', prompt=L('The following SQL query is run to test the database.', '', '```sql', 'SELECT ProductName, ProductPrice', 'FROM Products', 'WHERE ProductPrice > 22.00', 'ORDER BY ProductPrice ASC', '```', '',
                                                      'Fill in the table below with the result of running the SQL query. You may not need to use all the rows or columns. (4 rows × 3 columns provided)'),
  answer_type='RICH_TABLE', marks=2, criteria=crit((2, 'Correct rows, columns and order'), (1, 'Correct rows OR correct order with minor error')),
  sample_answer=L('| ProductName | ProductPrice |', '|---|---|', '| Discovery 1 and 2 (DVD) | 26.98 |', '| The Plant (DVD) | 28.00 |', '', '(22.00 is excluded because the condition is > not >=.)'),
  key_confidence='high', syllabus=['WEB-18'])
F('12b', stimulus=DB, part='Question 12 (b)', prompt=L('The contents of the Orders table need to be displayed as follows.', '', '| Customer | Product | Quantity |', '|---|---|---|',
                                                      '| Nicky Singh | The Best Movie (DVD) | 2 |', '| Kim Smith | Celebration (DVD) | 1 |', '| Casey He | Travel 1 and 2 (Blu-Ray) | 1 |',
                                                      '| Nicky Singh | Discovery 1 and 2 (DVD) | 2 |', '| Pat Alvardo | Discovery 1 and 2 (DVD) | 2 |', '', 'Write a SQL query that can produce this result.'),
  answer_type='SQL', marks=3,
  criteria=crit((3, 'Correct query joining all three tables with the correct join conditions and column names/aliases'), (2, 'Query joins the tables with minor errors'), (1, 'Shows some understanding of SQL')),
  sample_answer=L('```sql', 'SELECT Customers.CustName AS Customer, Products.ProductName AS Product, Orders.OrderQuantity AS Quantity', 'FROM Orders',
                  'JOIN Customers ON Orders.CustID = Customers.CustID', 'JOIN Products ON Orders.ProductID = Products.ProductID', 'ORDER BY Orders.OrderID;', '```'),
  key_confidence='high', syllabus=['WEB-18'])

F('13', stimulus=L("In a computer game, each player has 10 rounds and the maximum score for each round is 5. The score for each round is equal to the number of points, except when bonus points are assigned. Every time a player scores 5, the score from the next round is added as bonus points. If a player scores 5 in the last round, they get 10 points.", '',
                   "A player's scores and corresponding points for a full game are shown.", '', '| Round | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |', '|---|---|---|---|---|---|---|---|---|---|---|',
                   '| Score | 3 | 5 | 5 | 2 | 1 | 4 | 0 | 1 | 4 | 5 |', '| Points | 3 | 10 | 7 | 2 | 1 | 4 | 0 | 1 | 4 | 10 |'),
  prompt=L('Write a program in Python that will:', '', "- display the player's scores and corresponding points", '- calculate and display the total points for the player, taking into account the bonuses.', '',
           'Start your program with: `scores = [3,5,5,2,1,4,0,1,4,5]`', '', 'The output of the program should match the following:', '', '```', 'Round Score Points', '1     3     3', '2     5     10', '3     5     7',
           '4     2     2', '5     1     1', '6     4     4', '7     0     0', '8     1     1', '9     4     4', '10    5     10', 'TOTAL POINTS: 42', '```'),
  answer_type='CODING', language='PYTHON', marks=6,
  criteria=crit((6, 'Correct program: loops through all rounds, applies the bonus rule (including the last round), displays round/score/points in the required format and the correct total'),
                (5, 'Substantially correct program with a minor error'), (4, 'Program applies the bonus rule with some errors, OR correct output without the last-round rule'),
                (3, 'Program displays scores and calculates a total without correct bonuses'), (2, 'Some correct Python relevant to the problem'), (1, 'Shows some understanding of the problem')),
  sample_answer=L('```python', 'scores = [3,5,5,2,1,4,0,1,4,5]', 'total = 0', "print('Round', 'Score', 'Points')", 'for i in range(len(scores)):', '    points = scores[i]',
                  '    if scores[i] == 5:', '        if i == len(scores) - 1:', '            points = 10', '        else:', '            points = scores[i] + scores[i + 1]',
                  '    total = total + points', '    print(i + 1, scores[i], points)', "print('TOTAL POINTS:', total)", '```'),
  key_confidence='high', syllabus=['PROJ-15', 'PROJ-13'])

SL = [f'assets/fam_SEFAM17S{i}.png' for i in range(1, 13)]
F('14', stimulus=L('The following slideshow was prepared by a student as part of a research project.', '', ' '.join(f'![slide {i}]({p})' for i, p in enumerate(SL, 1)), '',
                   'Slide text (summary): "How many times have you interacted with artificial intelligence this week?"; "How many decisions have been made about YOU this week by artificial intelligence?"; '
                   '"AI can notice patterns in enormous data sets that are beyond the ability of human perception to detect. AI technology can make even ordinary and seemingly trivial data valuable."; '
                   '"AI can facilitate decision-making and improve productivity."; AI is used in social media, weather forecasting, recommendation systems in e-commerce, video sharing and streaming, '
                   'entertainment websites, virtual personal assistants, image recognition; "AI robots can take on risky or boring tasks", "AI medical assistants can diagnose diseases based on patients\' symptoms", '
                   '"Chatbots can answer customer service questions", "AI can even filter out hostile activities to protect cyber security"; algorithms decide social media feeds, credit scores, what products to buy, '
                   'what to binge watch, whether a person gets a job interview, how much people pay for home or car insurance; how machines learn: supervised, unsupervised, semi-supervised, reinforcement learning; '
                   '"AI needs LARGE amounts of training data. Big data is the raw material that fuels AI algorithms and models."; how they learn about us: social media, shopping history, online surveys, '
                   'internet browsing history and preference, everyday interactions with technology; "What will our future relationship with AI be?"'),
  images=SL, prompt='Assess the use of artificial intelligence in our society. Support your answer with information from the slideshow.', answer_type='SHORT', extended=True, marks=8, word_limit=300,
  criteria=crit((8, 'Makes an informed judgement about the use of AI in society, weighing benefits and drawbacks/risks, well supported by relevant information from the slideshow'),
                ('6–7', 'Assesses the use of AI with reference to benefits and drawbacks, supported by information from the slideshow'),
                ('4–5', 'Describes benefits and/or drawbacks of AI with some reference to the slideshow'), ('2–3', 'Outlines some uses or impacts of AI'), (1, 'Provides some relevant information')),
  sample_answer=('AI is now embedded in everyday life — social media feeds, recommendation systems, streaming, weather forecasting and virtual assistants — and on balance it is highly beneficial but '
                 'carries significant risks that must be managed. Its main strength is detecting patterns in enormous data sets beyond human perception, which improves decision-making and productivity: '
                 'medical assistants diagnose diseases from symptoms, robots take on risky or boring tasks (improving worker safety), chatbots answer customer service questions around the clock, and AI filters '
                 'hostile activity to protect cyber security. However, the slideshow notes that AI needs LARGE amounts of training data harvested from our social media, shopping and browsing history and online '
                 'surveys, raising privacy concerns about how "ordinary and seemingly trivial" personal data is collected and used. More seriously, algorithms now make high-stakes decisions about people — credit '
                 'scores, insurance prices and whether a person gets a job interview — often without transparency. If the training data reflects human or dataset bias, these decisions can be unfair and hard to '
                 'challenge. Overall, AI\'s benefits to productivity, health and safety are substantial, but its use is only appropriate where data is collected with consent, models are tested for bias, and humans '
                 'remain accountable for decisions that significantly affect people\'s lives.'),
  key_confidence='high', syllabus=['AUTO-9', 'AUTO-11'])

# ------------------------------------------------------------------ 2025 HSC (RESERVED) ------------------------------------------------------------------
P25 = '2025 HSC Software Engineering'
SRC = 'RESERVED – 2025 HSC (unseen until Sunday) — ' + P25
md25 = json.load(open('/Users/fred/gradeo/question_bank/raw/nesa_2025hsc_RESERVED.parsed.json'))
G = {g['n']: g for g in md25['groups']}
def stim(n): return G[n]['stimulus'] or None
def item(n, k=0): return G[n]['items'][k]['md']
hsc = []
def H(q, **kw):
    e = {'id': f'nesa-hsc2025-q{q}', 'origin': 'NESA', 'reserved': True, 'source': f'{SRC} Q{q}', 'source_paper': P25, 'publisher': 'NESA',
         'question_title': f'2025 HSC Question {q}', 'part': f'Question {q}', 'key_source': 'NESA 2025 HSC Marking Guidelines (official)', 'quality': 3, 'issues': [], 'images': []}
    e.update(kw); hsc.append(e)
ID = crit((1, 'Identifies the correct answer'))
mc = {1: (['Pilot', 'Direct', 'Phased', 'Parallel'], 0, 'PROJ-3'), 3: (['Supervised learning', 'Unsupervised learning', 'Reinforcement learning', 'Semi-supervised learning'], 0, 'AUTO-3'),
      4: (['recursive code.', 'list comprehensions.', 'language-dependent code optimisation.', 'using a hash table to create shorter solutions.'], 2, 'PROJ-22'),
      5: (['Excess load times', 'Biases in machine learning', 'Exposure of more data than intended', 'Inappropriate use of screen elements'], 2, 'SSA-11'),
      6: (['Delivering packets between hosts on the internet', 'Dropping malformed packets before they reach a host computer', 'Adding headers to data packets containing authentication information',
           'Ensuring that parties exchanging information are who they claim to be'], 3, 'WEB-3'),
      7: (['White background, black text, green border', 'Centre aligned, italic, increased letter spacing', 'Blue background, white text, border around the heading',
           'Left aligned, bold, and 2.5 times larger than the rest of the page'], 2, 'WEB-9'),
      8: (['Race conditions', 'Invalid redirection', 'Cross-site scripting', 'Authentication issues'], 0, 'SSA-13')}
def fixcode(s):  # code blocks collapsed by the HTML: restore line breaks for known fragments
    return s
for n, (o, c, syl) in mc.items():
    p = item(n)
    H(str(n), stimulus=stim(n), prompt=p, answer_type='MULTI_CHOICE', marks=1, options=opts(o, {c}), criteria=ID, syllabus=[syl] + (['WEB-4'] if n == 6 else []),
      images=['assets/hsc25_SEN25Q03.png'] if n == 3 else [])
# code-fragment stimuli with restored line breaks
for e in hsc:
    if e['id'].endswith('q3'):
        e['stimulus'] = e['stimulus'].replace('![](assets/hsc25_zoom-cursor.png)![](assets/hsc25_zoom-icon.svg)', '').strip()
    if e['id'].endswith('q4'):
        e['stimulus'] = L('Fragment 1 and Fragment 2 are Python code that achieve the same purpose.', '', '**Fragment 1**', '```python', 'numbers = [1, 2, 3, 4, 5]', 'total = 0', 'for num in numbers:',
                          '    total += num', 'print(total)', '```', '', '**Fragment 2**', '```python', 'numbers = [1, 2, 3, 4, 5]', 'print(sum(numbers))', '```')
    if e['id'].endswith('q7'):
        e['stimulus'] = L('Consider the following cascading style sheet (CSS) code fragment for a website.', '', '```css', 'body {', '    font-size: 100%;', '    font-style: italic;', '    line-height: 1.8;',
                          '    font-weight: normal;', '}', 'h1 {', '    text-align: center;', '    font-style: normal;', '    font-size: 250%;', '    letter-spacing: 5px;',
                          '    background-color: rgb(0, 0, 100);', '    color: white;', '    font-weight: 900;', '    border: 3px solid green;', '}', '```')
H('2', prompt='Complete the statement by selecting the correct term from each dropdown menu.\n\nThe [1] approach typically requires extensive documentation, while the [2] approach often emphasises working software over documentation.',
  answer_type='DROPDOWN', marks=1, dropdowns=[{'label': '1', 'options': ['Agile', 'Waterfall', 'WAgile'], 'correct': ['Waterfall']}, {'label': '2', 'options': ['Agile', 'Waterfall', 'WAgile'], 'correct': ['Agile']}],
  criteria=crit((1, 'Identifies the correct item from each dropdown')), syllabus=['PROJ-4', 'PROJ-5'])
H('9', prompt='Two approaches that can be used when programming databases for use in web applications are Object-Relational Mapping (ORM) and Structured Query Language (SQL).\n\nMatch each characteristic to the appropriate approach.',
  answer_type='OBJECTIVE_RESPONSE', marks=1, objective={'columns': ['Object-Relational Mapping (ORM)', 'Structured Query Language (SQL)'], 'multi_select_per_row': True, 'rows': [
      {'statement': 'Code is focused on object manipulation', 'correct': ['Object-Relational Mapping (ORM)']},
      {'statement': 'Tables can be joined to enhance searching', 'correct': ['Object-Relational Mapping (ORM)', 'Structured Query Language (SQL)']},
      {'statement': 'Programmers can choose the language used to access the database', 'correct': ['Object-Relational Mapping (ORM)']}]},
  criteria=crit((1, 'Correctly matches each characteristic to the appropriate approach')), syllabus=['WEB-19'])
def ms(n, items, correct, syl, marks=1, crt=None):
    H(str(n), prompt=re.sub(r'\n\n- .*', '', item(n), flags=re.S).strip(), answer_type='MULTI_SELECT', marks=marks, options=opts(items, correct),
      criteria=crt or crit((1, 'Identifies ALL the correct items')), syllabus=syl)
ms(10, ['Limiting the need for software updates', 'Protecting sensitive data from unauthorised access', 'Allowing developers to bypass security features when needed',
        'Reducing the testing time required during software development', 'Ensuring software applications meet legal and industry standards'], {1, 4}, ['SSA-5'])
ms(11, ['Rapid feedback', 'Freedom from bias', 'Procedural fairness', 'Automation of repetitive tasks', 'Collaboration and shared ownership'], {0, 3, 4}, ['AUTO-1'])
ms(12, ['Identifying whether a received email is spam', 'Determining the outcome of a two-party election', 'Calculating house prices based on size of the land',
        'Investigating the relationship between height and weight', 'Estimating the rate at which a contagious illness will spread', 'Working out if someone will be admitted to a university course'],
   {0, 1, 5}, ['AUTO-6'], marks=2, crt=crit((2, 'Identifies true or false correctly for all SIX check boxes'), (1, 'Identifies true or false correctly for FOUR of the six checkboxes')))
STAGES = ['Testing and evaluating', 'Identifying and defining', 'Researching and planning', 'Producing and implementing']
H('13', prompt='A software developer plans to use static application security testing (SAST) and dynamic application security testing (DAST) to check an application that is being developed.\n\nFor each strategy, choose the most appropriate stage in software development for it to be applied. Indicate whether access to source code is required.',
  answer_type='DROPDOWN', marks=2, dropdowns=[{'label': 'SAST – timing', 'options': STAGES, 'correct': ['Producing and implementing']}, {'label': 'SAST – access to source code', 'options': ['Yes', 'No'], 'correct': ['Yes']},
                                               {'label': 'DAST – timing', 'options': STAGES, 'correct': ['Testing and evaluating']}, {'label': 'DAST – access to source code', 'options': ['Yes', 'No'], 'correct': ['No']}],
  criteria=crit((2, 'Correctly identifies the timing and source code access for each strategy'), (1, 'Correctly identifies the timing and source code access for ONE strategy OR correctly identifies the timing for each strategy')),
  syllabus=['SSA-9'])
H('14', stimulus=L('Consider this code fragment.', '', '```', 'FOR index = 5 TO 3', '    word[index] = word[index-2]', 'NEXT index', '```', '', 'The array, word, contains the following data.', '',
                   '| index | 1 | 2 | 3 | 4 | 5 |', '|---|---|---|---|---|---|', '| word[index] | S | M | A | R | T |'),
  prompt='Select the correct item from each dropdown menu to show the contents of the array after the code is run. (Five dropdowns, one per element; options A, M, R, S, T.)',
  answer_type='DROPDOWN', marks=1, dropdowns=[{'label': f'word[{i}]', 'options': ['A', 'M', 'R', 'S', 'T'], 'correct': [c]} for i, c in enumerate('SMSMA', 1)],
  criteria=crit((1, 'Identifies the correct item from each dropdown')), syllabus=['PROJ-15'])
DT = ['Array', 'Boolean', 'Integer', 'String']
H('15a', part='Question 15 (a)', stimulus='A computer game is being developed.',
  prompt=L('Part of a data dictionary for the computer game is shown. Select the correct entries to complete the data dictionary.', '',
           '| Variable | Data type | Format for display | Size in bytes | Description | Example |', '|---|---|---|---|---|---|', '| PlayerId | [1] | NXXXXN | [2] | Identifies player | [3] |',
           '| PlayerName | [4] | XX...XX | 15 | Player name | Nat Kim |', '| Level | [5] | NN | 1 | Level of player | 27 |', '| OnMission | [6] | X | 1 bit | Y or N | Y |',
           '| LastSave | Date and Time | [7] | 12 | Time last saved 24-hour time | 13:45:21.221 |'),
  answer_type='DROPDOWN', marks=3, dropdowns=[{'label': '1 PlayerId data type', 'options': DT, 'correct': ['String']}, {'label': '2 PlayerId size', 'options': ['5', '6', '7', '8'], 'correct': ['6']},
                                               {'label': '3 PlayerId example', 'options': ['NATHAN', '2ATHA2', 'NATH22', 'N2222N'], 'correct': ['2ATHA2']}, {'label': '4 PlayerName data type', 'options': DT, 'correct': ['String']},
                                               {'label': '5 Level data type', 'options': DT, 'correct': ['Integer']}, {'label': '6 OnMission data type', 'options': DT, 'correct': ['Boolean']},
                                               {'label': '7 LastSave format', 'options': ['hhmmss.sss', 'hh:mm:ss.sss', 'hh:mm:ss', 'ss:mm:hh.hhh'], 'correct': ['hh:mm:ss.sss']}],
  criteria=crit((3, 'Correctly completes ALL the dropdowns'), (2, 'Correctly completes FIVE dropdowns'), (1, 'Correctly completes THREE dropdowns')), syllabus=['PROJ-2'])
FM = lambda *ns: [f'assets/hsc25_fullmark_{n}.png' for n in ns]
def W(q, n, k, syl, marks, crt, sample, fm=(), part=None, prompt=None, atype='SHORT', **kw):
    g = G[n]
    s = g['stimulus'] or None
    p = prompt or re.sub(r'^\*\*\([a-c]\)\*\*\s*', '', item(n, k)).strip()
    imgs = FM(*fm)
    sa = sample + (('\n\n**Official full-mark student response(s):** ' + ' '.join(f'![]({i})' for i in imgs)) if imgs else '')
    H(q, stimulus=s, prompt=p, answer_type=atype, marks=marks, criteria=crt, sample_answer=sa, sample_answer_images=imgs, images=imgs, syllabus=syl, part=part or f'Question {q}', **kw)
W('15b', 15, 1, ['PROJ-21'], 3, crit((3, 'Outlines TWO relevant software debugging tools'), (2, 'Outlines ONE relevant software debugging tool OR identifies TWO relevant software debugging tools'), (1, 'Provides some relevant information')),
  'Breakpoints can be added to specific lines of code to halt program execution, allowing the programmer to check the value of specific variables or to step through the program line by line. Debugging output statements can be added to the code to indicate that a certain section of code has been reached or to show the contents of a variable.',
  part='Question 15 (b)', prompt='While this game is being developed, there are persistent issues with the code. Outline TWO software debugging tools that can be used to identify these logic errors.')
for e in hsc:
    if e['id'].endswith('q15b'): e['stimulus'] = 'A computer game is being developed.'
W('16a', 16, 0, ['WEB-1', 'WEB-21'], 3, crit((3, 'Compares the use of a PWA with an interactive website for the weather app'), (2, 'Outlines features of a PWA and/or an interactive website'), (1, 'Identifies a feature of a PWA or an interactive website')),
  'Both PWAs and interactive websites are platform-independent, allowing users to access the app on any device with a browser. PWAs can pre-cache updates to enable offline updates when a stable internet connection is not available but may not provide real time updates for the most recent changes to weather or warnings. Meanwhile, interactive websites require a constant internet connection to provide any updates.\n\nAnswers could include: Some PWAs prompt for initial installation or setup which might deter some users.',
  fm=['002'], part='Question 16 (a)')
W('16b', 16, 1, ['WEB-13'], 3, crit((3, 'Outlines TWO ways, other than the use of a PWA, to minimise the load time of the weather app'), (2, 'Outlines ONE way, other than the use of a PWA, to minimise load time OR identifies TWO ways'), (1, 'Provides some relevant information')),
  'One way would be to provide the option to select lower resolution images or text only display. Another way would be to utilise caching as this would provide high speed access to commonly requested weather data.', fm=['003'], part='Question 16 (b)')
W('16c', 16, 2, ['SSA-7'], 3, crit((3, "Describes ONE way that the 'privacy by design' approach could be implemented in the weather app"), (2, "Outlines ONE feature of the 'privacy by design' approach"), (1, "Identifies a feature of the 'privacy by design' approach")),
  "Embedded within the design of the weather app would be a process for regularly deleting identifiable data. For example, the app would likely record a person's live location to deliver relevant weather details. The privacy by design approach would incorporate a regular process to delete these locations from cache.", fm=['004'], part='Question 16 (c)')
W('17', 17, 0, ['PROJ-15'], 3, crit((3, 'Provides a substantially correct pseudocode algorithm'), (2, 'Provides a pseudocode algorithm that addresses some aspects of the problem'), (1, 'Shows some understanding of the problem or pseudocode')),
  L('```', 'BEGIN RiskRating', '    Total = 0', '    index = 0', '    REPEAT', '        Total = Total + Risks[index]', '        index = index + 1', '    UNTIL index = 10', '    IF Total > 35 THEN', '        Rating = "High"',
    '    ELSE', '        IF Total < 20 THEN', '            Rating = "Low"', '        ELSE', '            Rating = "Medium"', '        ENDIF', '    ENDIF', '    Display Rating', 'END RiskRating', '```', '',
    '(The guidelines also accept a CASEWHERE or ELSEIF version of the selection.)'), atype='SHORT')
W('18', 18, 0, ['WEB-5'], 3, crit((3, 'Explains how metadata and data mining can be used to prevent technical difficulties during the broadcast of the live event'), (2, 'Outlines how metadata AND/OR data mining can be used to prevent broadcast technical difficulties'), (1, 'Identifies a feature of metadata or data mining')),
  'Metadata describes the content, structure and meaning of raw data, enabling more effective, accurate and efficient data mining. Data mining identifies user preferences and viewing patterns from large datasets, helping streaming services personalise recommendations and identify times of predicted high demand. Streaming service management uses this along with real-time user data to balance server loads and deliver smooth playback experiences.', fm=['005'])
W('19', 19, 0, ['SSA-10', 'PROJ-15'], 3, crit((3, 'Provides correct code for the problem'), (2, 'Provides partially correct code that includes a correct selection structure OR password creation'), (1, 'Shows some understanding of the scenario and Python programming')),
  L('```python', "uName = input('What is your username?')", "password = input('What is your password?')", 'passwordP1 = uName[:3]', "passwordP1 = passwordP1 + '123'", 'if passwordP1 == password:',
    "    print('Welcome!')", 'else:', "    print('Incorrect password entered')", '```'), fm=['006', '007'], atype='CODING', language='PYTHON')
W('20', 20, 0, ['SSA-12'], 3, crit((3, 'Describes how session management can affect code execution efficiency'), (2, 'Identifies some features of session management'), (1, 'Provides some relevant information')),
  'Efficient session management limits memory consumption by restricting session data size and lifetime. Excessive reading, writing or storing large objects increases input/output operations and slows code execution for the user. Removing sessions when they are no longer required is essential to prevent unnecessary resource consumption.\n\nAnswers could include:\n- Reducing database and network bottlenecks – frequent access to session stores, especially in distributed environments, can cause latency\n- Preventing memory leaks – poor session handling, particularly in server-side storage, can lead to memory leaks, triggering more frequent garbage collection and degrading performance.\n- Enabling scalable, responsive systems – asynchronous or lazy cleanup can further optimise execution.', fm=['008'])
W('21', 21, 0, ['WEB-18'], 4, crit((4, "Provides a correct SQL query that extracts 'Pending' and 'Escalated' jobs for the 'Software' and 'Hardware' categories, counts the jobs for each status in each category, and outputs results in descending order"),
                                 (3, 'Provides an SQL query that addresses most of the requirements of the problem'), (2, 'Provides an SQL query that shows some understanding of the problem'), (1, 'Shows some understanding of SQL or the problem')),
  L('```sql', 'SELECT Category, Status, COUNT(JobID) AS Jobs', 'FROM Issues', "WHERE (Status = 'Pending' OR Status = 'Escalated')", 'GROUP BY Status, Category', 'ORDER BY Jobs DESC', '```'), fm=['010', '011'],
  prompt=L('Construct a SQL query that displays:', '', '- the number of pending software jobs', '- the number of pending hardware jobs', '- the number of escalated software jobs', '- the number of escalated hardware jobs', '',
           'List the results in order from the highest to lowest, based on the number of jobs.'), atype='SQL',
  dataset_setup_sql=re.search(r'`(CREATE TABLE[^`]*)`', item(21)).group(1))
W('22', 22, 0, ['PROJ-11'], 3, crit((3, 'Constructs a correct class diagram that shows inheritance and removes redundant attributes from each class'), (2, 'Constructs a class diagram that shows some understanding of the problem'), (1, 'Provides some relevant information')),
  L('Official sample (diagram), in text form:', '- **Animal**: Colour, Size', '  - **Reptile** (inherits Animal): Scale type, Tongue type', '  - **Mammal** (inherits Animal): Birth type, Number of teeth',
    '    - **Dog** (inherits Mammal): Breed, Fur', '    - **Whale** (inherits Mammal): Blowhole type, Migration location', 'Inheritance arrows point from each subclass to its superclass.'), fm=['013'], atype='DRAWING')
W('23a', 23, 0, ['SSA-17'], 3, crit((3, 'Outlines relevant social and ethical issues'), (2, 'Outlines ONE relevant social or ethical issue OR identifies relevant social and/or ethical issues'), (1, 'Identifies ONE relevant social or ethical issue')),
  'The website will need to ensure payment and address data is appropriately secured and accessible only to authorised personnel. It also needs to ensure that pages can be viewed in a wide variety of languages and that the information about dishes displayed is accurate and representative of the product.', fm=['014'], part='Question 23 (a)')
W('23b', 23, 1, ['WEB-7', 'WEB-15'], 3, crit((3, 'Explains why server-side web programming is needed to develop the website with examples from the scenario'), (2, 'Outlines some features of server-side web programming for developing the website with examples from the scenario'), (1, 'Identifies a feature of server-side web programming and/or providing relevant examples from the scenario')),
  'Server-side development will need to be used to provide dynamic information to the front-end (website). There are many dynamic aspects to the website, including the menu which changes along with subscription information and order tracking information. Server-side scripting will need to be written to read the relevant information from storage (most likely, a database) and then provide this information to the front-end.', fm=['015'], part='Question 23 (b)',
  prompt='Explain why server-side web programming would be needed to develop this website. Support your answer with examples from the website.')
CON = ['integrity', 'availability', 'authorisation', 'accountability', 'confidentiality', 'authentication']
rows23 = [('The system verifies that the total price displayed matches the actual total after items are added to the cart.', 'integrity'), ('The backend ensures the website remains accessible during peak order times.', 'availability'),
          ('The system logs all user actions, such as changes to subscriptions or delivery addresses.', 'accountability'), ('User payment details, such as credit card numbers, are encrypted during transactions.', 'confidentiality'),
          ('A user with a basic account can place orders but cannot access admin features.', 'authorisation')]
H('23c', part='Question 23 (c)', stimulus=G[23]['stimulus'], prompt='Security features have been included in the design of the website. Choose the fundamental security concept that matches each of the security features.\n\n' + '\n'.join(f'{i}. {r}' for i, (r, _) in enumerate(rows23, 1)),
  answer_type='DROPDOWN', marks=3, dropdowns=[{'label': r, 'options': CON, 'correct': [c]} for r, c in rows23],
  criteria=crit((3, 'Provides the correct response for ALL items'), (2, 'Provides the correct response for THREE items'), (1, 'Provides the correct response for ONE item')), syllabus=['SSA-4'])
W('24', 24, 0, ['AUTO-9'], 5, crit((5, 'Provides a comprehensive discussion of the impact of the safety monitoring system on workers with reference to the scenario'), (4, 'Outlines both positive and negative ways, that the safety monitoring system can affect workers'),
                                  (3, 'Outlines some ways that the safety monitoring system can affect workers'), (2, 'Outlines ONE way that the safety monitoring system can affect workers OR identifies some ways that the safety monitoring system can affect workers'), (1, 'Provides some relevant information')),
  "The AI monitoring system can improve safety on site by reducing human error through real-time alerts and remote monitoring. It can also help supervisors track workers' compliance with PPE requirements and identify risky behaviours, potentially preventing accidents. However, some workers might feel their privacy is invaded, especially if the wearables continue monitoring during breaks or in private areas like bathrooms. There's also a risk of the system misidentifying safe behaviour as unsafe, leading to unnecessary alerts or stress which could cause distractions at critical times. Additionally, the long-term data collection could be used to improve training, but workers may worry about how the data is stored or used.",
  fm=['016', '017'])
W('25', 25, 0, ['AUTO-5', 'AUTO-4'], 5, crit((5, 'Explains how the neural network supports the virtual personal assistant; includes one positive AND one negative impact of using the virtual personal assistant'),
                                            (4, 'Explains how the neural network supports the virtual personal assistant OR outlines how the neural network supports the assistant and includes one positive AND one negative impact'),
                                            (3, 'Outlines features of neural network AND/OR impacts of using the virtual personal assistant'), (2, 'Outlines a feature of neural network OR an impact of using the virtual personal assistant OR identifies features of neural network AND/OR impacts'), (1, 'Provides some relevant information')),
  'Neural networks recognise natural language patterns to categorise common support queries, such as lost luggage, and use nodes to assist with processing. They assess language tone to gauge frustration or urgency, allowing the virtual personal assistant to recommend specific phrasing for customer service staff. For instance, calming language may be suggested for distressed customers. By tracking customer ratings and turnaround times, the neural network uses weightings to refine recommendations to prioritise high-frequency queries or improve suggestions for poorly rated interactions. While this system streamlines support processes and improves response accuracy, it may also impact the role of customer service staff. As the neural network learns from interactions, staff may rely more on its recommendations, potentially reducing their familiarity with emerging query trends or response strategies. Customers may come to expect faster, more precise service, raising the standard for human interactions.',
  fm=['018'])
W('26', 26, 0, ['PROJ-13', 'PROJ-15'], 5, crit((5, 'Provides a correct python program that addresses the following requirements: creates a list of unique randomly generated numbers; processes the generated list correctly; uses selection and looping structures; provides correctly formatted output; uses inbuilt python functions'),
                                              (4, 'Provides a substantially correct python program that addresses most of the requirements'), (3, 'Provides a python program that addresses some of the requirements'), (2, 'Provides a python program that addresses one requirement'), (1, 'Shows some understanding of the problem')),
  L('```python', 'import random', '', 'randList = []', 'for x in range(15):', '    nextInt = random.randint(1,25)', '    while nextInt in randList:', '        nextInt = random.randint(1,25)', '    randList.append(nextInt)', '',
    'pos = 0', 'while pos < 25:', '    if pos in randList:', '        print ("| X", end=" ")', '    else:', '        print ("| ", end=" ")', '    pos = pos + 1', '    if (pos % 5 == 0):', '        print("| \\n")', '```'),
  atype='CODING', language='PYTHON')
for e in hsc:
    if e['id'].endswith('q26'):
        e['stimulus'] = G[26]['stimulus']
W('27', 27, 0, ['AUTO-11'], 6, crit((6, 'Explains how human bias could affect the usefulness of AI solutions; supports answer with reference to the video'), (5, 'Describes how human bias could affect the usefulness of AI solutions; refers to a scenario(s) in the video'),
                                   (4, 'Outlines how human bias could affect AI solutions; refers to the video'), ('2–3', 'Identifies some sources/examples of human bias AND/OR identifies effects of human bias on AI solutions AND/OR outlines how AI learns'), (1, 'Provides some relevant information')),
  "AI develops its ability by analysing vast amounts of data. The quality of these data can be influenced by human bias, and in turn, affect the usefulness of AI solutions.\n\nHuman bias may be explicit or implicit. Explicit biases are intentional. For example, a researcher may favour male physicists and only collect pictures of male physicists for training an AI solution, as shown in the video. Implicit biases operate unconsciously and may be shaped by social and cultural factors. Whether the bias was explicit or implicit, the choice of male physicists would suggest to the AI solution that physicists are male.\n\nHuman bias can occur in various stages of the development of AI solutions. As shown in the photo library example, training data needs to be diverse and representative, otherwise AI solutions may produce inaccurate or unhelpful responses. The process of labelling training data may also introduce biases as people may have different interpretations of the same data. The video shows that if most people draw shoes in particular ways, certain types of shoes will not be recognised as a shoe.",
  fm=['020', '021'], prompt='Explain how human bias could affect the usefulness of artificial intelligence (AI) solutions. Support your answer with reference to the video.')
for e in hsc:
    if e['id'].endswith('q27'):
        e['stimulus'] = 'Watch the video, and then answer the question. (The video is not available online: "Due to copyright restrictions, this material cannot be displayed until permission has been obtained.")'
        e['issues'] = ['video stimulus not available (copyright); answer from general knowledge']
        e['quality'] = 2
    if e['id'].endswith('q3'):
        e['images'] = ['assets/hsc25_SEN25Q03.png']

out = fam + hsc
for e in out:
    for k in ['stimulus', 'prompt']:
        if e.get(k): e[k] = e[k].strip()
json.dump(out, open('/Users/fred/gradeo/question_bank/tools/nesa_entries.json', 'w'), indent=1, ensure_ascii=False)
print(len(fam), 'fam parts;', len(hsc), '2025 parts')
