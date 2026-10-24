# 12SEN_Cycle6

- Syllabus: Software Engineering · Publisher: –
- Status: COMPLETED · results released · submitted 2026-04-20
- **Score: 6 / 11** (55%) · answered 5/5 parts · marked 5/5
- Review page: https://platform.gradeo.com.au/reviewExam/c31fb9f2-2f38-4769-9419-d4282efee1be

---

## 1. WAgile Approach (MC, TKS2025)

*Source: TKS 2025*

#### Part A — 0/1 marks  `MULTI_CHOICE`

Why might WAgile be unsuitable for very small projects?

- **A.** It requires no documentation at all.
- **B.** It doesn&rsquo;t support team collaboration.
- **C.** Its iterative cycles are too short for small teams.  ⬅️ **your choice**
- **D.** The structured setup may cause extra overhead.  ✅ *correct*  ⬅️ **your choice**

**Your answer:** C, D · **Correct:** D ✘

---

## 2. Feedback (SA, TKS 2025)

*Source: TKS 2025*

#### Part A — 0/3 marks  `SHORT`

Describe two steps involved in analysing feedback during software development.

*Word limit: 120*

**Your answer:**

> revevint it 
> 
> then implmeting it

*(5 words)*

**Marking criteria:**
- [3] Clearly describes two steps involved in analysing feedback during software development.
- [2] Outlines AT LEAST ONE step involved in analysing feedback during software development.
- [1] Provides some relevant information

**Sample answer:**

One step in analysing feedback is categorisation, where feedback is sorted based on its source such as user, stakeholder, peer, or automated. This helps developers prioritise feedback appropriately, ensuring that critical issues like user-reported bugs are addressed before less urgent suggestions. Another step is impact analysis, which involves evaluating how implementing the feedback will affect the software’s architecture, performance, or user experience. This helps developers avoid introducing new problems and ensures that changes lead to meaningful improvements.

---

## 3. Backup (SA, TKS 2025)

*Source: TKS 2025*

#### Part A — 2/3 marks  `SHORT`

Describe how programmed data backup supports business continuity in software systems.

*Word limit: 100*

**Your answer:**

> Programed/automated backups suport bisnues connutit plans by providing a way of reverting and resorring. so if there is a ransomwhere atack  of acidentil dedeation of the prod database the compony can insted of losing the data they can restor from a backup. this allows bunuess opration to contue.

*(48 words)*

**Feedback (TKS CST, 2 marks):** Expand on how the programmed or automated nature of the backups specifically helps by ensuring data is saved at regular, scheduled intervals without requiring manual intervention. You should also explicitly mention how this process minimises operational downtime and helps maintain overall system reliability and data integrity during a disruption.

**Marking criteria:**
- [3] Clearly describes how programmed data backup supports business continuity in software systems.
- [2] Outlines how programmed data backup can support business continuity in software systems.
- [1] Provides some relevant information

**Sample answer:**

Programmed data backup supports business continuity by automatically creating copies of important data at scheduled intervals. This reduces the risk of data loss due to hardware failure, accidental deletion, or cyber threats like ransomware. By ensuring that backups are consistently made without manual input, organisations can quickly restore data and continue operations with minimal disruption, helping maintain both data integrity and system reliability.

---

## 4. Version Control (MC + SA, TKS 2025)

*Source: TKS 2025*

**Stimulus:**

A development team is working on a collaborative project using Git and GitHub. Each developer is assigned a feature and works on a separate branch. Before merging their work into the main branch, the team conducts code reviews and tests for compatibility. One developer notices that their branch has diverged significantly from main due to recent updates by others.

#### Part A — 3/3 marks  `SHORT`

Describe the steps the developer should take to ensure their branch is compatible with the latest version of main before merging.

*Word limit: 120*

**Your answer:**

> they should pull from the lates in origen/master/main or whatever branch then wish 
> 
> they should follow best practis (keping the signture of a function the same where posible ect) 
> 
> then they will need to relve any mearge conflicts
> 
> then make a PR

*(42 words)*

**Marking criteria:**
- [3] Clearly describes the steps the developer should take to ensure their branch is compatible with the latest version of main before merging.
- [2] Outlines how the developer can ensure their branch is compatible with main without causing unnecessary conflicts.
- [1] Provides some relevant information

**Sample answer:**

To ensure their branch is compatible with the latest version of main, the developer should first use "git fetch" to retrieve the most recent changes from the remote repository. Then, they can use "git rebase main" while on their feature branch to apply their changes on top of the updated "main" branch. This helps integrate the latest updates and resolve any conflicts before merging. Git supports this process by allowing developers to rebase or merge branches, which helps maintain a clean and linear project history. Rebasing is especially useful for keeping feature branches up to date without creating unnecessary merge commits.

#### Part B — 1/1 marks  `MULTI_CHOICE`

In addition, what is the most appropriate action the developer should take to maintain team workflow discipline and avoid integration issues?

- **A.** Skip code review and merge their branch immediately to avoid delaying the sprint timeline.
- **B.** Archive their branch and start a new one from main, assuming the original work will be too difficult to integrate.
- **C.** Push their branch to the remote repository and collaborate with other team members to resolve any conflicts during the merge.
- **D.** Communicate with the team, pull the latest changes from main, and rebase their branch to align with the current codebase before requesting a merge.  ✅ *correct*  ⬅️ **your choice**

**Your answer:** D · **Correct:** D ✔
