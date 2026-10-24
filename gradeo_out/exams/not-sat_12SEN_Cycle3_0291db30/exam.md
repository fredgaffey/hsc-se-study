# 12SEN_Cycle3

- Syllabus: Software Engineering · Publisher: –
- Status: LIVE · results released
- **Score: – / 11** · answered 0/3 parts · marked 0/3
- Review page: https://platform.gradeo.com.au/reviewExam/0291db30-06f5-4233-ac26-47d469166ff5

---

## 1. APIs (SA, TKS 2025)

#### Part A — –/4 marks  `SHORT`

Explain the difference between authentication and authorisation in API security and why both are necessary.

**Your answer:**

_(not answered)_

**Marking criteria:**
- [4] Thoroughly explains both authentication (verifying identity) and authorisation (permission levels), and clearly justifies why both are critical for API security
- [3] Provides a clear explanation of both terms and their roles with some reasoning on their necessity.
- [2] Gives a basic explanation of authentication and authorisation but lacks clarity or full understanding.
- [1] Mentions one or both terms vaguely with limited understanding.

**Sample answer:**

Authentication is the process of verifying who a user is, often through tokens or passwords. Authorisation determines what actions or data that authenticated user is allowed to access or modify. Both are necessary to ensure that only legitimate users can access the API (authentication) and that they can only perform actions permitted by their role or permissions (authorisation). This layered security helps protect sensitive data and system integrity.

---

## 2. Minimise Vulnerabilities (SA, TKS 2025)

*Source: TKS 2025*

#### Part A — –/4 marks  `SHORT`

Explain what Cross-Site Scripting (XSS) attacks are and describe two ways developers can protect their applications against them.

**Your answer:**

_(not answered)_

**Marking criteria:**
- [4] Thorough explanation of XSS and two clear, accurate mitigation methods with reasoning.
- [3] Thorough explanation of XSS and two clear, accurate mitigation methods with reasoning.
- [2] Basic understanding of XSS and at least one mitigation method explained.
- [1] Vague or limited explanation of XSS or mitigation methods.

**Sample answer:**

Cross-Site Scripting (XSS) is a security vulnerability where attackers inject malicious scripts into web pages viewed by other users. These scripts execute in the victim’s browser, allowing attackers to steal sensitive data or perform actions on behalf of the user. To protect against XSS, developers should validate and sanitize all user inputs to remove harmful code or characters. Additionally, encoding output before rendering it in web pages prevents injected scripts from executing by treating them as text rather than code. Implementing a Content Security Policy (CSP) is also effective in restricting the execution of untrusted scripts. Together, these measures reduce the risk of XSS attacks and improve application security.

---

## 3. File Security (SA, TKS 2025)

*Source: TKS 2025*

**Stimulus:**

A web application allows users to upload profile images. A developer implements file upload functionality but does not restrict the file type or directory in which files are stored.

#### Part A — –/3 marks  `SHORT`

Explain two security risks associated with this implementation and suggest one strategy for mitigating each.

**Your answer:**

_(not answered)_

**Marking criteria:**
- [3] Identifies two valid risks and clearly explains a mitigation strategy for each.
- [2] Identifies one valid risk with a relevant mitigation, or two risks with limited or unclear strategies.
- [1] Mentions one risk or a mitigation without clear connection or explanation.

**Sample answer:**

One risk is insecure file upload, where an attacker could upload a malicious script (e.g., `.php`) and execute it on the server. This can lead to remote code execution. To mitigate this, restrict uploads to specific file types such as `.jpg` or `.png` and store files outside the web root.

Another risk is directory traversal, where attackers manipulate file paths to access sensitive system files. This can be prevented by sanitising file paths, resolving them to absolute paths, and verifying they stay within the intended upload directory. Input validation should also block any relative path indicators like `../`.
