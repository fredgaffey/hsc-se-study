# North Sydney Boys Trial

- Syllabus: Software Engineering · Publisher: –
- Status: private
- **Score: – / 50** · answered 0/18 parts · marked 0/18
- Review page: -

---

## 1. Question 1

#### Question 1 — –/1 marks  `MULTI_CHOICE`

A part of an application with a GUI requires from the user to answer several questions. For one type of question there are several correct responses, and the user must select all the correct ones from a set of five options. Which screen element would be best suited for this type of question?

- **A.** Radio buttons
- **B.** Command buttons
- **C.** Checkboxes  ✅ *correct*
- **D.** List box

**Your answer:** (none) · **Correct:** C

---

## 2. Question 2

#### Question 2 — –/1 marks  `SORTING_TABLE`

Order the 4 steps in the model development part of MLOps.

**Your answer:**

_(not answered)_

**Sample answer:**

1.  Data wrangling
2.  Feature engineering
3.  Model training
4.  Model testing and validation

---

## 3. Question 3

#### Question 3 — –/1 marks  `MULTI_CHOICE`

Which of the following best describes metadata?

- **A.** The primary content of a document or file
- **B.** Descriptive information about data that helps to organise, find, and understand it  ✅ *correct*
- **C.** A summary of the given data that highlights its main statistics
- **D.** Encrypted data that is primarily used in social networking software like Facebook

**Your answer:** (none) · **Correct:** B

---

## 4. Question 4

#### Question 4 — –/1 marks  `MULTI_CHOICE`

How can SQL code be improved to prevent SQL injection attacks?

- **A.** By using user input directly in the SQL query with no sanitisation
- **B.** By using dynamic SQL queries that concatenate user input directly into the query
- **C.** By using only stored procedures with no parameterisation
- **D.** By implementing prepared statements with parameterised queries  ✅ *correct*

**Your answer:** (none) · **Correct:** D

---

## 5. Question 5

#### Question 5 — –/2 marks  `MULTI_CHOICE`

Which features of OOP can be seen in the following Python code?

```
class Person:
  def __init__(self, fname, lname):
    self.__firstname = fname
    self.__lastname = lname  
  def printname(self):
    print(self.__firstname,self.__lastname.upper(), end="")
  def greet(self):
    print("G’day ", end="")
    self.printname()
    print()

class Student(Person):
  def __init__(self, fname, lname, sid, gradyear):
    super().__init__(fname, lname)
    self.__studentID = sid
    self.graduationyear = gradyear
  def greet(self):
    self.printname()
    print(", welcome to the Class of", self.graduationyear)
```

- **A.** Encapsulation  ✅ *correct*
- **B.** Inheritance  ✅ *correct*
- **C.** Instantiation
- **D.** Polymorphism  ✅ *correct*

**Your answer:** (none) · **Correct:** A, B, D

---

## 6. Question 6

#### Question 6 — –/2 marks  `OBJECTIVE_RESPONSE`

Complete the text below by selecting 1 word for each provided space.

| Statement | Correct | Yours | |
|---|---|---|---|
| ______________ management catches unexpected problems in a program, helping to achieve a smooth recovery. | Exception | – |  |
| ______________ management helps keep track of user interactions with a website/application. | Session | – |  |
| ______________ management helps ensure that computer’s storage space is used wisely. | Memory | – |  |

---

## 7. Question 7

#### Question 7 — –/2 marks  `MULTI_CHOICE`

Which of the following machine learning models are NOT suitable for a classification problem?

- **A.** Decision tree
- **B.** Neural network
- **C.** Linear regression  ✅ *correct*
- **D.** Logistic regression
- **E.** K-nearest neighbours (KNN)
- **F.** Polynomial regression  ✅ *correct*

**Your answer:** (none) · **Correct:** C, F

---

## 8. Question 8

#### Question 8 — –/2 marks  `OBJECTIVE_RESPONSE`

For each of the given descriptions, indicate the most suitable network protocol.

| Statement | Correct | Yours | |
|---|---|---|---|
| Sending email messages from a client to a server or between servers. | SMTP | – |  |
| Addressing and routing data packets between devices on a network. | IP | – |  |
| Retrieving and managing emails directly on a mail server, allowing access from multiple devices. | IMAP | – |  |
| Ensuring reliable, ordered and error-checked delivery of data packets between devices. | TCP | – |  |
| Securely exchanging encrypted website data between a web browser and a web server. | HTTPS | – |  |
| Encrypting data transmitted over a network to ensure secure communication and protect against eavesdropping and tampering. | TLS | – |  |
| Downloading emails from a mail server to a local client, typically deleting them from the server. | POP 3 | – |  |
| Transferring files over a secure shell connection. | SFTP | – |  |

---

## 9. Question 9

**Stimulus:**

BEGIN AverageListOfNumbers
	average = -1
	arrayOfNumbers = GetNumbers()
	IF number of items in arrayOfNumbers != 0 THEN
		average = CalculateAverage(arrayOfNumbers)
		PrintAverageToScreen(average)
	ELSE
		PRINT "No numbers entered"
	END IF
END AverageListOfNumbers

#### Question 9 — –/4 marks  `DRAWING_V2`

Draw a structure chart to represent the AverageListOfNumbers algorithm given above.

**Your answer:**

_(not answered)_

**Marking criteria:**
- [4] Correct structure chart representing this algorithm
- [3] Substantially correct structure chart representing this algorithm, with some minor errors or omissions
- [2] An attempt at constructing a structure chart to represent this algorithm
- [1] An attempt at constructing a structure chart

**Sample answer:**

![A structure chart representing the algorithm is shown.](img/nsb/a9.png)  

In this diagram, the “diamond” (rotated square) with 2 lines going from the same vertex denotes OPTIONAL execution of BOTH CalculateAverage and PrintAverageToScreen subprograms (either BOTH of them are executed or NONE of them is executed). This is NOT a choice between executing either 1 of these 2 subprorams (a choice would be indicated by having the 2 lines coming from 2 different vertices of the “diamond”). The built-in commands like PRINT/DISPLAY and GET/INPUT are NOT shown on a structure chart.

---

## 10. Question 10

**Stimulus:**

BEGIN AverageListOfNumbers
	average = -1
	arrayOfNumbers = GetNumbers()
	IF number of items in arrayOfNumbers != 0 THEN
		average = CalculateAverage(arrayOfNumbers)
		PrintAverageToScreen(average)
	ELSE
		PRINT "No numbers entered"
	END IF
END AverageListOfNumbers

#### Question 10 — –/3 marks  `PSEUDOCODE`

For the AverageListOfNumbers algorithm given above, write pseudocode for the function CalculateAverage(arrayOfNumbers). Assume that arrayOfNumbers contains only numbers. However, check whether arrayOfNumbers is empty, so that your function CalculateAverage(arrayOfNumbers) can be also reused in other contexts.

**Your answer:**

_(not answered)_

**Marking criteria:**
- [3] Substantially correct algorithm
- [2] Partially correct algorithm, with some errors or omissions
- [1] An attempt at writing an algorithm to meet the requirements

**Sample answer:**

```
BEGIN CalculateAverage(arrayOfNumbers)
  count = LENGTH(arrayOfNumbers)
  IF count > 0 THEN
    total = 0
    FOR i = 1 TO count STEP 1 REM Assumes indexing from 1
      total = total + arrayOfNumbers[i]
    NEXT i
    RETURN total / count
  ELSE
    RETURN Null REM No value; impossible to calculate average
  END IF
END CalculateAverage
```

---

## 11. Question 11

#### Question 11 — –/3 marks  `SHORT`

Explain how the capabilities of end users influence the secure design features of software.

**Your answer:**

_(not answered)_

**Marking criteria:**
- [3] Explains causal relationships between capabilities of end users and the secure design features of software
- [2] Discusses capabilities of end users relevant for secure design features of software
- [1] Identifies a capability of end users relevant for secure design features of software

**Sample answer:**

Capabilities of end users, such as their technical proficiency, security awareness and accessibility requirements, significantly impact the design features of software. They influence the user interface, accessibility options, customisation preferences and security settings. Developers must consider the capabilities of end users to create secure, usable, and effective software. (Additionally, they should provide appropriate documentation, training, and support to users with different capabilities.)

1.  **Technical Proficiency:** End users have diverse levels of technical expertise, from beginners to advanced users. Software needs to be designed with intuitive interfaces and security settings (e.g. built-in prompts for secure actions) for less tech-savvy users, while providing advanced features for those who need them and can use them without introducing vulnerabilities.
2.  **Security Awareness:** Users' understanding of security threats and security practices differs greatly. Software needs to account for the varying levels of security awareness among its users and mitigate risks associated with less security-conscious users. Commonly, this includes providing secure defaults (e.g. requiring multi-factor authentication by default), restricting unnecessary user permissions and displaying clear security prompts. Software designers often need to balance security enhancements with user experience, ensuring that security measures are as seamless as possible to encourage compliance and reduce the likelihood of users bypassing security for convenience.
3.  **Accessibility requirements:** End users may have different accessibility requirements, influencing how security features are implemented. For instance, software design must ensure that security measures (e.g. multi-factor authentication) are accessible to users with disabilities, ensuring that security does not come at the cost of usability.

---

## 12. Question 12

#### Question 12 — –/3 marks  `SHORT`

Describe what a template engine in web development is and how it works.

**Your answer:**

_(not answered)_

**Marking criteria:**
- [3] Describes both what a template engine is AND how it works
- [2] Describes either what a template engine is OR how it works
- [1] States a feature of a template engine

**Sample answer:**

A template engine (a.k.a. templating engine) is used to rapidly and easily build web applications and dynamic HTML pages. It leverages HTML/JavaScript templates (some are pre-made but configurable, others can be written by designers) that contain placeholders, including variables, loops iterating over collections and conditionals. Different template engines (e.g. EJS, Pug, Handlebars, etc.) use different notations (syntaxes) to describe their templates and placeholders. When the web application is running, the template engine on the web server replaces the variables/placeholders in the used template file with actual values, then sends this dynamically customised HTML web page content to the client (which never sees the used templates). Templates also enable fast rendering of server-side data that needs to be passed to the application. By using a template engine, developers can separate HTML presentation structure from the application logic, making the code cleaner and easier to maintain. Designers can work on templates while developers focus on the backend logic.

---

## 13. Question 13

#### Question 13 — –/3 marks  `DRAWING_V2`

Draw a decision tree (resulting from machine learning) for decisions whether a person should be accepted into a software engineering student club meeting. A female is always accepted. Other persons are accepted only if they study Software Engineering or are proficient in C.

**Your answer:**

_(not answered)_

**Marking criteria:**
- [3] Substantially correct decision tree
- [2] Partially correct decision tree, with some errors or omissions
- [1] An attempt at drawing a decision tree to meet the requirements

**Sample answer:**

![A decision tree is shown. The first node asks 'Female?'. The 'Yes' branch leads to 'Accept!'. The 'No' branch leads to a node asking 'Studies Software Engineering?'. The 'Yes' branch leads to 'Accept!'. The 'No' branch leads to a node asking 'Proficient in C?'. The 'Yes' branch leads to 'Accept!'. The 'No' branch leads to 'Do NOT accept!'.](img/nsb/a13.png)

---

## 14. Question 14

#### Question 14 — –/3 marks  `SHORT`

Compare and contrast cross-site scripting (XSS) and cross-site request forgery (CSRF).

**Your answer:**

_(not answered)_

**Marking criteria:**
- [3] Discusses at least 2 similarities AND at least 2 differences between XSS and CSRF
- [2] Discusses either ONLY similarities OR ONLY differences between XSS and CSRF
OR
Outlines a similarity AND a difference between XSS and CSRF
- [1] Provides some correct information about XSS or CSRF

**Sample answer:**

**Similarities between XSS and CSRF include:**

1.  Both XSS and CSRF are vulnerabilities that specifically target web applications.
2.  Both attacks rely on exploiting the trust that users and web applications have, particularly the inherent trust a website has in its users and their browsers.
3.  Both vulnerabilities can lead to client-side consequences, affecting what a user can see or do on a web application.
4.  Both XSS and CSRF can lead to serious consequences, including access to sensitive information, data breaches, account hijacking, and website defacement.

**Differences between XSS and CSRF include:**

1.  **Different focus:** While XSS primarily targets the user's browser and client-side security, CSRF primarily targets the server and authentication mechanisms.
2.  **Different attack mechanisms (vectors):** XSS involves injecting malicious scripts (typically JavaScript) into a website, which then executes in the user's browser when they visit the compromised page. Contrary, CSRF involves an attacker crafting a malicious link or form that, when clicked or submitted by the unsuspecting user, sends a request to the target website as if it were from the user themselves.
3.  **Different data handing:** In XSS the attacker can potentially read the response of the malicious script's execution and extract data to their own server. In CSRF, the attacker can only send requests, but they cannot directly receive the responses from the target website.
4.  **Different session requirement:** XSS can be successful regardless of the user's session status (authenticated or not), but CSRF requires the user to have an active session with the targeted website.

---

## 15. 2025 CSSA, Fam_Q15,   SQL

#### Question 15 — –/3 marks  `SQL`

An online business is planning to use a database to keep track of its products. The contents of the **Products** table during testing are shown below:

| ProductID | ProductName | ProductPrice |
|---|---|---|
| P001 | The Plant (DVD) | 28.00 |
| P002 | Discovery 1 and 2 (DVD) | 26.98 |
| P003 | Travel 1 and 2 (Blu-Ray) | 22.00 |
| P004 | The Best Movie (DVD) | 19.98 |
| P005 | Celebration (DVD) | 12.00 |

After executing a SQL query, the following results were obtained:

| ProductName | ProductPrice |
|---|---|
| Celebration (DVD) | 12.00 |
| The Best Movie (DVD) | 19.98 |
| Travel 1 and 2 (Blu-Ray) | 22.00 |

Write the SQL **SELECT** query that produced the above results.

Dataset:
```sql
CREATE TABLE Products (
  ProductID TEXT PRIMARY KEY,
  ProductName TEXT NOT NULL,
  ProductPrice REAL NOT NULL
);

INSERT INTO Products (ProductID, ProductName, ProductPrice) VALUES
('P001','The Plant (DVD)',28.00),
('P002','Discovery 1 and 2 (DVD)',26.98),
('P003','Travel 1 and 2 (Blu-Ray)',22.00),
('P004','The Best Movie (DVD)',19.98),
('P005','Celebration (DVD)',12.00);
```

**Your answer:**

_(not answered)_

**Marking criteria:**
- [3] Substantially correct SQL SELECT statement
- [2] Partially correct SQL select statement, with some errors or omissions
- [1] An attempt at writing a SQL SELECT statement to meet the requirements

**Sample answer:**

```
SELECT ProductName, ProductPrice
FROM Products
WHERE ProductPrice <= 22.00
ORDER BY ProductPrice ASC;
```

  

_An alternative sample answer:_

```
SELECT ProductName, ProductPrice
FROM Products
WHERE ProductPrice <= 22.00
ORDER BY ProductName ASC;
```

---

## 16. Question 16

**Stimulus:**

An ISBN is the International Standard Book Number, a globally unique number to identify books. This is usually printed above the barcode on the back cover of most books.

The last (i.e. the 13th) digit in a 13-digit ISBN (International Standard Book Number) is known as the "check digit". The check digit is calculated in the following way:

-   Each of the other 12 digits of the ISBN from left to right is multiplied alternately by 1 or 3. This means that the first digit is multiplied by 1, the second by 3, the third by 1, the fourth by 3, etc.
-   The results are added together and then divided by 10.
-   The remainder of this division is subtracted from 10 to give the check digit.
-   If the check digit is 10 then it is replaced with 0 – this ensures that the check digit is always a single digit.

For example, in an ISBN of **9780980874921** the last digit (in this case 1) is the check digit. However, we should re-calculate that check digit to ensure that the ISBN has not been entered incorrectly.

(9×1) + (7×3) + (8×1) + (0×3) + (9×1) + (8×3) + (0×1) + (8×3) + (7×1) + (4×3) + (9×1) + (2×3) = 129.

Then, 129 ÷ 10 = 12 remainder 9. Therefore, the check digit is 10 - 9 = 1. In this case the ISBN is valid as our calculated value of 1 matches the provided check digit.

#### Question 16 — –/5 marks  `CODING`

In Python, write the function `checkDiqitOK(isbn_str)` that takes a 13-digit ISBN as the string `isbn_str` and returns True or False indicating whether the ISBN is valid in terms of its check digit. Assume that the provided string `isbn_str` always contains 13 digits – do NOT check whether there are fewer/more digits and do NOT check whether some of the characters are not digits. Do NOT write the main program nor any other subprogram calling `checkDiqitOK(isbn_str)`.

**Hints:**

-   The 13-digit ISBN is provided as a string, so conversion of individual characters into integer digits is needed for the calculations.
-   You can use Python’s `%` operator to calculate the remainder of a division.

**Your answer:**

_(not answered)_

**Marking criteria:**
- [5] Correct Python program that includes ALL of the following 5 features:Loops through each ISBN digit (except the last) and works out the sum of digitsCorrectly distinguishes between digits to multiply by 3 and add vs those to just addCorrectly calculates the check digitPerforms a check to see whether the check digit is 10 and replaces it with 0Compares the calculated check digit to the last digit of the entered ISBN and returns True if they match (correct check digit) or False if they do not (incorrect check digit)
- [4] Substantially correct Python program that includes at least 4 of the above features
- [3] A sound attempt at the Python program that includes at least 3 of the above features
- [2] An attempt at writing the Python program that includes at least 2 of the above features
- [1] An attempt at writing the Python program that includes at least 1 of the above features

**Sample answer:**

```
#Checks whether the check digit of an ISBN is valid
def checkDigitOK(isbn_str): #assumes a string with 13 digits provided
  sumOfDigits = 0 #accumulator for the sum of digits
  for i in range(12): #loops thru the first 12 digits but not the last/13th
    #1st digit has Python index 0 (even); 2nd digit has index 1 (odd), etc.
    if i % 2 == 0: #an even Python index, the digit is multiplied by 1
      sumOfDigits = sumOfDigits + int(isbn_str[i]) * 1
    else: #an odd Python index, the digit is multiplied by 3
      sumOfDigits = sumOfDigits + int(isbn_str[i]) * 3
  sumModulo = sumOfDigits % 10 #calculates the remainder of division by 10
  checkDigit = 10 - sumModulo #calculates the check digit
  if checkDigit == 10: #the special case; checkDigit must have only 1 digit
    checkDigit = 0
  #Checking whether the provided ISBN contains the correct check digit
  if int(isbn_str[-1]) == checkDigit: #last element is at Python index -1
    return True
  else:
    return False
```

  

_An alternative sample answer:_

```
#Checks whether the check digit of an ISBN is valid
def checkDigitOK(isbn_str): #assumes a string with 13 digits provided
  sumOfDigits = 0 #accumulator for the sum of digits
  #the first 12 digits of ISBN contain 6 groups of 2 digits:
  # the 1st of these 2 digits is multiplied by 1
  # the 2nd of these 2 digits is multiplied by 3
  for i in range(6):
    sumOfDigits = sumOfDigits + int(isbn_str[2*i]) * 1
    sumOfDigits = sumOfDigits + int(isbn_str[2*i+1]) * 3
  sumModulo = sumOfDigits % 10 #calculates the remainder of division by 10
  checkDigit = 10 - sumModulo #calculates the check digit
  if checkDigit == 10: #the special case; checkDigit must have only 1 digit
    checkDigit = 0
  #Checking whether the provided ISBN contains the correct check digit
  if int(isbn_str[12]) == checkDigit: #last/13th digit is at Python index 12
    return True
  else:
    return False
```

---

## 17. Question 17

**Stimulus:**

Your team is developing the secure PWA ‘nAIs Skin Check PWA’. Using this app, a user first uploads images of their skin moles, personal information (e.g. name, phone number, email, …), demographic information (e.g. age, gender, occupation, …) and medical history. Then, the app uses machine learning / artificial intelligence to determine and show on the screen the probability of melanoma (dangerous skin cancer) in the given skin mole images.

#### Question 17 — –/3 marks  `SHORT`

Discuss how the 3 main principles of the ‘privacy by design’ approach should be applied in the development of the ‘nAIs Skin Check PWA’ app.

**Your answer:**

_(not answered)_

**Marking criteria:**
- [3] Discusses applying on the given scenario of 3 of the main principles of 'privacy by design'
- [2] Discusses applying on the given scenario of 1 or 2 of the main principles of ‘privacy by design'
OR
Outlines 2 or 3 of the main principles of ‘privacy by design'
- [1] Shows some understanding of 'privacy by design'
OR
Outlines 1 of the main principles of 'privacy by design'

**Sample answer:**

The 'privacy by design' is built around the 7 main principles: Proactive not reactive; Privacy as a default setting; Privacy embedded into design; Full functionality; End-to-end security; Visibility and transparency; and Respect for user privacy. From these 7, our Software Engineering syllabus emphasises only #1, #3 and #7 so their application on the given ‘nAIs Skin Check PWA' app scenario is discussed here.

**Proactive not reactive approach** is about anticipating risks and preventing privacy-invasive events before they occur. In the ‘nAIs Skin Check PWA' app scenario, the personal and medical information (possibly also some of the demographic information) is personally identifiable information (PII) that must be kept private and protected. It can be anticipated that this sensitive information could be compromised on the client side, transport over the Internet or the server side. Therefore, all information provided by a user should be protected (e.g. encrypted) in transport over the Internet and any client-side and server-side handling, including storage. This is protection in transit, in use and rest.

**Embed privacy into design** is about ensuring that privacy becomes one of the core functions of any system or service. In the ‘nAIs Skin Check PWA' app scenario, this means the app's design must include the decisions to protect all user's information in transport/storage/handling, not storing any user information (neither on the server nor on the client) after a user is shown the probability of melanoma in the given images, and not providing any user information to any 3rd party.

**Respect for user privacy** is about keeping the interest of individuals paramount for any system or service, e.g. by offering strong privacy defaults and user-friendly options, as well as ensuring appropriate notices are given. In the ‘nAIs Skin Check PWA' app scenario, the default protection of all user information in transit/rest/use, the default server-side and client-side secure deletion/destruction of all user information, and the default of not providing of any user information to any 3rd party are strong with respect to user privacy.

---

## 18. Question 18

**Stimulus:**

Your team is developing the secure PWA ‘nAIs Skin Check PWA’. Using this app, a user first uploads images of their skin moles, personal information (e.g. name, phone number, email, …), demographic information (e.g. age, gender, occupation, …) and medical history. Then, the app uses machine learning / artificial intelligence to determine and show on the screen the probability of melanoma (dangerous skin cancer) in the given skin mole images.

#### Question 18 — –/8 marks  `SHORT`

Explain, illustrate on examples from the ‘nAIs Skin Check PWA’ scenario and evaluate strategies that your software development team should use to manage security of programming code, including: code review, SAST, DAST, vulnerability assessment, penetration testing.

**Your answer:**

_(not answered)_

**Marking criteria:**
- [8] Explains and evaluates all 5 listed strategies for managing security of programming code AND supports this with examples from the given scenario
- [7] Explains and evaluates some of the 5 listed strategies for managing security of programming code (while only discussing the others OR explaining them but without evaluating them OR explaining & evaluating them but with errors) AND supports this with examples from the given scenario
- [6] Discusses all 5 listed strategies for managing security of programming code AND supports this discussion with examples from the given scenario
- [5] Discusses some of 5 listed strategies for managing security of programming code (while only outlining the others or discussing them but with errors) AND supports this discussion with examples from the given scenario
- [4] Correctly outlines all 5 listed strategies for managing security of programming code
- [3] Correctly outlines some of the 5 listed strategies for managing security of programming code
- [2] Shows some understanding of strategies for managing security of programming code
- [1] Provides some relevant information

**Sample answer:**

**Code review**, Static Application Security Testing (SAST), Dynamic Application Security Testing (DAST), vulnerability assessments, and penetration testing are all valuable strategies for managing the security of programming code, but they serve different purposes and are most effective when used in combination.

**Code review** is a manual (or partially automated) process of systematically examining source code to identify security flaws, logic errors, other mistakes or quality issues, and adherence to coding standards. In the ‘nAIs Skin Check PWA' app scenario, this would mean that some team members systematically review code written by other team members and provide improvement feedback. Code review encourages knowledge sharing, catches vulnerabilities and bugs early in the development cycle, reduces the cost of remediation, and enhances both code quality and security. Its limitations include: can be time-consuming and may not identify all runtime vulnerabilities.

**Static Application Security Testing (SAST)** is a white-box testing method that analyses source code for security vulnerabilities without executing the program. In the ‘nAIs Skin Check PWA' app scenario, some team members would use SAST tools to perform SAST on the app's code without executing it. SAST can identify vulnerabilities (such as SQL injection, buffer overflows, insecure APIs) early in the development process. Its limitations include producing false positives and not detecting runtime-specific vulnerabilities.

**Dynamic Application Security Testing (DAST)** is a black-box testing method that runs software and analyses its behaviour (e.g. when exposed to simulated attacks) to find vulnerabilities that are only apparent during runtime. In the scenario, team members would use DAST tools to test the running app with simulated attacks. DAST identifies real-world runtime vulnerabilities and can find issues related to configuration and runtime environments. Its limitations include occurring later in the development cycle and being more time-consuming than SAST.

**Vulnerability assessment** is a systematic process of identifying, quantifying, classifying and prioritizing security vulnerabilities in an application. In the ‘nAIs Skin Check PWA' app scenario, team members would use appropriate tools to systematically scan for, identify and prioritise security vulnerabilities in the app. It provides a comprehensive overview of vulnerabilities and helps prioritise remediation efforts. Its limitations include not identifying all vulnerabilities and becoming outdated quickly if not performed regularly.

**Penetration testing** is performing simulated real-world attacks on a system to identify vulnerabilities that can be exploited. In the scenario, external hired white-hat hackers would perform simulated attacks on the running app. It provides a realistic real-world assessment of the security posture and identifies vulnerabilities that may not be detected by other methods. Its limitations include being time-consuming, resource-intensive and expensive, and it is a point-in-time assessment.

Incorporating a combination of these strategies provides a robust approach to managing code security. By integrating these methods into the software development lifecycle, the ‘nAIs Skin Check PWA' app team can significantly enhance their security posture and reduce the risk of vulnerabilities being exploited.
