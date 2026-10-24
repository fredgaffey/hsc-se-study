# Attempt: Drill 1 - Explain and SDLC

- Started: 2026-10-24T03:16:23.671Z · Submitted: 2026-10-24T03:25:06.256Z
- Auto-marked (MC + objective response): **2/3**. Written answers: to be marked by Claude.
- Time used: 9 min of 18 · Rest breaks: 0 (0 min)

---

## 1. Usability and security

### Part A (4 marks, SHORT)

Explain the challenges of balancing usability with security in software design, and suggest ways developers can address these challenges.

**Your answer:**

> The chalanges with balancing usabily with secrity is that as you make a product more useable there is a larger atack surfes. ie moving from a staktic fount end that is stored localy to having a datbase then hagving to deal with the chanlanges of CSRF, XSS, and SQL enjection.
> 
> But these chanalnfges can be mitigated by secure developemnt pracisis such as good defuault and data minimiation. Haging good deafault will allow the nontecnical users to to have secure defaut enfryption settings and force them to have a seurre passowd ie 12 char 1 cap spical carter and numbers. This can help protect them from bure force atacs. 
> Autenticating user is chanlanging but with paskeys this allow apps to be more secuer with also improving the user experince. But this comes that the cost of when sigin in on a new device anoying 2FA.

*144 words*

---

## 2. Installation methods

### Part A (1 marks, MULTI_CHOICE)

A hospital uses its new booking system in one ward for a month, then rolls it out to every ward. Which installation method is this?

**Your answer:** D · correct: D → **1/1** (auto)

---

## 3. Testing

### Part A (1 marks, MULTI_CHOICE)

Which type of testing checks that separately developed modules work correctly together?

**Your answer:** C · correct: B → **0/1** (auto)

---

## 4. Performance testing

### Part A (1 marks, MULTI_CHOICE)

A developer checks how a website performs with the 2000 users it normally expects at the same time. Which type of testing is this?

**Your answer:** A · correct: A → **1/1** (auto)

---

## 5. Validation

### Part A (3 marks, SHORT)

Explain why the online store should validate the quantity on the server, even though it is already checked in the browser.

**Your answer:**

> This is becaus of the pricipl of least trust. The server can't trust the fount end as this can be controed and minulated but running raw JS in the conlole (one of many ways) this could allow that the user could pay for 1 item but aculaty receve 10 this could lead to abus. This is why server side validation is allways importatn as it stop a milious user from exployting and taking advantage of the site.

*77 words*
