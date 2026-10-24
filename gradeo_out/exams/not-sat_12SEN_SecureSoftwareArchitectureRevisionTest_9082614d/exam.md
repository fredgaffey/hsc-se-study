# 12SEN_SecureSoftwareArchitectureRevisionTest

- Syllabus: Software Engineering · Publisher: –
- Status: LIVE · results released
- **Score: – / 50** · answered 0/17 parts · marked 0/17
- Review page: https://platform.gradeo.com.au/reviewExam/9082614d-59df-4fc3-915f-a70b3420e0d5

---

## 1. Security Strategies & Tools (MC, TKS 2025) 

*Source: TKS 2025*

#### Part 1 — –/1 marks  `MULTI_CHOICE`

In what stage of development can SAST tools be applied?

- **A.** Only during integration testing.
- **B.** Only during initial design phases.
- **C.** Only after the code is completed.
- **D.** At any stage after Requirements definition.  ✅ *correct*

**Your answer:** (none) · **Correct:** D

---

## 2. Social/Ethical/Legal Issues (MC, TKS 2025)

*Source: TKS 2025*

**Stimulus:**

An online retailer updates its platform to include privacy controls that let users manage how their personal data is collected and used.

#### Part A — –/1 marks  `MULTI_CHOICE`

This change is most closely related to which concept?

- **A.** User control and compliance with privacy laws
- **B.** Providing open-source licensing options for developers  ✅ *correct*
- **C.** Introducing new automation tools to reduce staff workload
- **D.** Preventing the reuse of copyrighted media assets in advertisements

**Your answer:** (none) · **Correct:** B

---

## 3. Defensive Data (MC, TKS 2025)

*Source: TKS 2025*

**Stimulus:**

A web application checks user input both in the browser and on the server before processing it. The client-side checks improve user experience by catching errors early, but the server-side checks are essential for security.

#### Part A — –/1 marks  `MULTI_CHOICE`

Why is it important to perform both client-side and server-side validation?

- **A.** Both are equally secure and redundant
- **B.** Client-side validation is more secure; server-side validation prevents UI errors
- **C.** Server-side validation is more secure; client-side validation enhances usability  ✅ *correct*
- **D.** Client-side validation protects against hackers, server-side validation is for speed

**Your answer:** (none) · **Correct:** C

---

## 4. Security and Resilience of Software (MC, TKS 2025)

*Source: TKS2025*

#### Part A — –/1 marks  `MULTI_CHOICE`

Which combination of practices best helps determine vulnerabilities in a software system?

- **A.** Software deployment and version control checks
- **B.** Updating software licenses and permissions
- **C.** Load testing and memory usage analysis
- **D.** Penetration testing and user feedback  ✅ *correct*

**Your answer:** (none) · **Correct:** D

---

## 5. Fundamental Security Concepts (MC, TKS 2025)

*Source: TKS 2025*

**Stimulus:**

An online shopping platform implements a logging system that tracks which users accessed which orders and when. This feature is intended to help identify misuse or fraud

#### Part A — –/1 marks  `MULTI_CHOICE`

Which security concept does this feature best support?

- **A.** Integrity
- **B.** Availability
- **C.** Authorisation
- **D.** Accountability  ✅ *correct*

**Your answer:** (none) · **Correct:** D

---

## 6. File Security (OR, TKS 2025)

*Source: TKS 2025*

#### Part A — –/2 marks  `OBJECTIVE_RESPONSE`

For each situation below, select the most appropriate secure coding technique used to prevent the vulnerability

| Statement | Correct | Yours | |
|---|---|---|---|
| A web application allows file uploads and needs to prevent directory traversal. | File Path Sanitisation | – |  |
| A developer is writing cryptographic operations and wants to prevent timing attacks. | Blinding Technique | – |  |
| A script is logging into multiple services and only needs read access to user files. | Least Privilege | – |  |
| User input is being used in file names, leading to execution of untrusted commands. | Input Validation | – |  |

**Marking criteria:**
- [2] Correctly selects all options
- [1] Partially correct selection

---

## 7. Security Strategy & Tools (SA, TKS 2025)

*Source: TKS 2025*

#### Part A — –/4 marks  `SHORT`

Explain the purpose of penetration testing in system security.

*Word limit: 150*

**Your answer:**

_(not answered)_

**Marking criteria:**
- [4] Clearly explains the purpose of penetration testing in system security.
- [3] Describes the purpose of penetration testing in system security.
- [2] Outlines a reason why penetration testing may be used in system security.
- [1] Provides some relevant information.

**Sample answer:**

Penetration testing, or "pen testing," is a security practice that involves simulating cyberattacks to evaluate a system’s defences. Its purpose is to identify vulnerabilities that could be exploited by malicious actors, allowing organisations to strengthen their security before real threats occur. One technique used is simulated attacks, where ethical hackers attempt to bypass authentication, access sensitive data, or escalate privileges. This helps uncover flaws in access controls and data protection mechanisms. Another technique involves using manual and automated tools, such as Metasploit or Kali Linux, to replicate realistic attack scenarios. These tools can scan for known vulnerabilities and test system responses. By combining these approaches, penetration testing provides a comprehensive view of an application’s security posture. It not only reveals technical weaknesses but also highlights gaps in security policies and procedures, enabling targeted remediation and improved resilience against future attacks.

---

## 8. Social/Ethical/Legal Issues (SA, TKS 2025)

*Source: TKS 2025*

#### Part A — –/3 marks  `SHORT`

Describe the concept of digital disruption and how the development of secure software can both cause and respond to it.

**Your answer:**

_(not answered)_

**Marking criteria:**
- [3] Clearly describes digital disruption and how secure software relates to it, with examples.
- [2] Provides a general description of digital disruption with some link to secure software
- [1] Makes a vague or minimal connection between digital disruption and security.

**Sample answer:**

Digital disruption refers to how new technologies change or replace traditional business models. Secure software development can cause digital disruption by enabling innovative services, like blockchain-secured transactions, that make older methods obsolete. It also helps enterprises respond to disruption by protecting data and systems from cyber threats, allowing them to adopt new digital tools safely. For example, a financial company using secure blockchain tech disrupts traditional banking with faster, safer services. At the same time, secure software helps businesses protect themselves and adapt to these technological changes.

---

## 9. File Security (SA, TKS 2025)

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

---

## 10. Minimise Vulnerabilities (SA, TKS 2025)

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

## 11. APIs (SA, TKS 2025)

*Source: TKS 2025*

#### Part A — –/3 marks  `SHORT`

Describe the role of HTTPS in securing API communications and explain why it is preferred over HTTP.

**Your answer:**

_(not answered)_

**Marking criteria:**
- [3] Provides a thorough explanation of HTTPS&rsquo;s role in encryption and security, clearly contrasts HTTPS with HTTP, and explains why HTTPS is preferred to protect data integrity and confidentiality
- [2] Provides a sound explanation of HTTPS encryption and its benefits, with some contrast to HTTP.
- [1] Gives a basic explanation mentioning encryption or security but lacks detail or comparison with HTTP.

**Sample answer:**

HTTPS secures API communication by encrypting data sent between the client and server, preventing eavesdropping or man-in-the-middle attacks. Unlike HTTP, which sends data in plain text, HTTPS uses SSL/TLS protocols to protect data integrity and confidentiality. This ensures sensitive information, such as authentication tokens or personal data, cannot be intercepted or tampered with during transmission, making HTTPS the preferred choice for secure APIs.

---

## 12. Defensive Data (SA, TKS 2025)

*Source: TKS 2025*

#### Part A — –/3 marks  `SHORT`

Describe one difference between client-side and server-side input validation, and explain why both are important in a secure application

**Your answer:**

_(not answered)_

**Marking criteria:**
- [3] Clearly describes the difference and explains the importance of using both client- and server-side validation in a secure context
- [2] Describes the difference and gives a sound explanation of one reason why both are used.
- [1] Identifies a basic difference but explanation is unclear or incomplete.

**Sample answer:**

Client-side validation is performed in the user’s browser before the data is sent to the server, while server-side validation happens after the data reaches the server. Client-side checks improve the user experience by providing quick feedback, but they can be bypassed by attackers. Server-side validation is more secure because it ensures all data is properly checked before it is processed or stored. Using both together ensures better usability and strong protection against invalid or malicious input

---

## 13. Privacy By Design (SA, TKS 2025)

*Source: TKS 2025*

**Stimulus:**

An e-commerce platform is being developed. During planning, the team performs a privacy impact assessment and decides to minimise customer data collection, avoid storing payment details, and enable encrypted guest checkout.

#### Part A — –/3 marks  `SHORT`

Explain how the team’s actions demonstrate the _Privacy by Design_ approach

**Your answer:**

_(not answered)_

**Marking criteria:**
- [3] Demonstrates a thorough understanding of the Privacy by Design approach; clearly connects scenario elements to key principles
- [2] Shows sound understanding; identifies at least two principles with relevant explanation.
- [1] Identifies one relevant principle with some basic explanation.

**Sample answer:**

The team’s actions reflect several key principles of Privacy by Design. Conducting a privacy impact assessment early shows a _proactive_ approach by identifying potential risks before launch. Choosing not to store payment details and enabling encrypted guest checkout are examples of _embedding privacy into the design_, ensuring secure and minimal data handling from the outset. Limiting the amount of data collected respects users' privacy by reducing exposure risk and enhancing user trust. Together, these practices show a comprehensive application of the Privacy by Design framework.

---

## 14. Security of Programming Code (SA, TKS 2025)

#### Part A — –/4 marks  `SHORT`

Discuss ONE strength and ONE limitation of using only static application security testing (SAST) to secure application code.

**Your answer:**

_(not answered)_

**Marking criteria:**
- [4] Clearly explains 1 strength and 1 limitation of using only SAST.
- [3] Explains 1 strength OR 1 limitation of using only SAST.
- [2] Outlines a strength and limitation.
- [1] Provides some relevant information.

**Sample answer:**

Static testing, such as SAST, is useful for detecting common coding vulnerabilities early in development without running the code. It’s fast, repeatable, and integrates easily into the development workflow. However, it has limitations, it can’t find runtime issues or logic flaws that only appear when the application is running, meaning some serious vulnerabilities may be missed if dynamic testing isn’t also used.

---

## 15. Security By Design (SA, TKS 2025)

*Source: TKS 2025*

#### Part 1 — –/3 marks  `SHORT`

A software company is testing a new chat application. How can sandboxing help during the testing phase to improve security?

**Your answer:**

_(not answered)_

**Marking criteria:**
- [3] Clearly explains how sandboxing helps improve security during testing, such as isolating code and preventing system-wide damage.
- [2] Describes how sandboxing helps improve security during testing, such as isolating code and preventing system-wide damage.
- [1] Shows some understanding of sandboxing in testing, but explanation is vague or incomplete.

**Sample answer:**

Sandboxing helps by running the chat application’s new features in an isolated environment where any bugs or vulnerabilities can be detected without risking the main system. This containment prevents harmful code from affecting other parts of the software or the operating system. It allows developers to safely test untrusted or experimental code, reducing the risk of security breaches during development.

---

## 16. Security Features (SA, TKS 2025)

*Source: TKS 2025*

#### Part A — –/3 marks  `SHORT`

A company wants to protect sensitive customer information both when stored and during transmission.

Explain how encryption achieves this and why it is important for data protection

**Your answer:**

_(not answered)_

**Marking criteria:**
- [3] Clearly explains how encryption secures data at rest and in transit

Explains why encryption is important for protecting sensitive information
- [2] Explains one aspect of encryption (either storage or transmission)

Provides some understanding of its importance
- [1] Shows basic understanding of encryption or data protection

**Sample answer:**

Encryption transforms data into a coded format that can only be read by someone with the correct decryption key. When data is stored (at rest), encryption protects it from unauthorised access if the storage device is compromised. For data in transit (sent over networks), encryption prevents attackers from intercepting and reading sensitive information. This dual use of encryption is crucial because it maintains the confidentiality and integrity of customer data, ensuring it cannot be easily stolen or altered.

---

## 17. Developing Secure Code (ER, TKS 2025)

*Source: TKS 2025*

**Stimulus:**

_"Secure software design plays a vital role in protecting users from malicious activity and ensuring optimal application performance"_

#### Part A — –/10 marks  `SHORT`

Discuss how a software developer can design and implement secure and efficient code by considering:

-   User action controls such as broken authentication and XSS
    
-   Defensive input handling
    
-   File and side-channel attack mitigation
    
-   Efficient execution (memory, session, and exception management)
    
-   API security principles
    

In your response, include relevant examples and refer to key principles such as _least privilege_, _input validation_, and _secure session management_

**Your answer:**

_(not answered)_

**Marking criteria:**
- [9-10] Demonstrates a comprehensive understanding of secure and efficient coding practices across multiple areas (user input, APIs, file safety, memory, etc.). Effectively integrates principles such as least privilege, input validation, and session security. Provides relevant, technically accurate examples and justifies strategies clearly. Shows deep insight into why and how these practices prevent vulnerabilities
- [7-8] Demonstrates a well-developed understanding of most secure coding areas. Discusses a range of mitigation strategies and principles with generally accurate examples. Explanation shows clarity and depth, though some minor technical inaccuracies or omissions may be present.
- [5-6] Demonstrates a sound understanding of some security and efficiency concepts. Response includes basic examples or principles, but may lack depth or integration across topics. Some discussion of mitigation is present, though may be partially underdeveloped or simplistic.
- [3-4] Demonstrates limited understanding of secure coding. Identifies one or two basic ideas, but lacks clarity or technical accuracy. May include irrelevant or vague references to examples or principles.
- [1-2] Demonstrates minimal understanding of security concepts. Provides isolated statements or keywords with little explanation. Does not address most aspects of the question.

**Sample answer:**

Designing secure and efficient software is crucial for protecting systems from vulnerabilities while maintaining performance and reliability. A well-designed application must safeguard against threats such as broken authentication, file and side-channel attacks, and input-based vulnerabilities, while also ensuring efficient memory use, robust session management, and secure API integration.

One of the most common and damaging vulnerabilities is broken authentication, where poor session and credential handling allows attackers to impersonate legitimate users. To mitigate this, developers should implement strong password policies (e.g., minimum length, character diversity), hash passwords using secure algorithms (e.g., bcrypt or Argon2), and avoid storing passwords in plaintext. Furthermore, session tokens should be uniquely generated, stored using secure HTTP-only cookies, and tied to session expiration policies. Implementing multi-factor authentication (MFA) can provide an additional security layer against account compromise.

Cross-Site Scripting (XSS) is another significant threat, occurring when attackers inject malicious scripts into websites that are then executed in users’ browsers. Developers should employ input validation and output encoding to neutralise untrusted input. For example, escaping special characters like <, > and " prevents injected scripts from being executed. A Content Security Policy (CSP) further limits the sources from which scripts can be run, mitigating risks even if sanitisation fails.

Alongside secure user interaction, defensive input handling is fundamental. Developers should apply input validation to ensure data adheres to expected formats (e.g., type, length, and range checks) and sanitisation to remove harmful characters. This prevents attacks like SQL injection or command injection. For instance, using a whitelist to accept only alphanumeric characters for usernames can block script injection attempts.

Security vulnerabilities also arise in how applications handle file operations and system-level interactions. File attacks, such as path traversal or insecure file uploads, exploit weaknesses in how files are accessed or stored. To prevent this, developers should use file path sanitisation, ensuring all file paths are resolved as absolute and constrained to safe directories. Additionally, uploaded files should be restricted by type (e.g., blocking .exe or .php files) and stored with unique randomised names in non-executable directories.

Side-channel attacks exploit hardware signals—like timing, power, or electromagnetic emissions—to leak sensitive data such as cryptographic keys. To mitigate this, developers can use constant-time algorithms for comparisons and cryptographic operations, preventing attackers from inferring information based on execution time. Blinding and masking techniques can randomise inputs and computations, making power or timing patterns meaningless. Sensitive data should also be encrypted and never left in memory longer than necessary.

In terms of efficiency, secure software must also be optimised for performance. Memory management is essential—developers should avoid unnecessary object creation and use generators for large data processing to reduce memory load. Tools like memory profilers can help identify leaks or excessive allocation. Session management should limit stored session data and implement timeouts to release server resources for inactive users.

Exception management plays a dual role in both security and user experience. Programs must avoid crashing or exposing sensitive details when errors occur. Instead, developers should catch specific exceptions, log technical errors securely (e.g., without exposing stack traces to the user), and return general error messages like “Invalid input” or “Something went wrong” to the user interface.

Finally, when building Application Programming Interfaces (APIs), developers must ensure they’re protected from abuse. Use of HTTPS ensures secure transmission, while authentication methods like API keys or OAuth2 prevent unauthorised access. Rate limiting can stop denial-of-service attacks by restricting how frequently clients can make requests. Input validation and CSRF tokens further harden APIs against request forgery.

In conclusion, secure and efficient coding requires a layered approach, combining validation, encryption, access control, session handling, and secure defaults. By adhering to principles such as least privilege, defensive programming, and fail-safe defaults, developers can significantly reduce the attack surface while maintaining high system performance and a positive user experience.
