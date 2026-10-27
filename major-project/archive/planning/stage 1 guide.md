# Software Engineering AT3a - Stage 1: Identifying and Defining

## Project Overview

You are tasked with developing a web application that addresses a real-world need or problem. The application should be designed to be user-friendly, functional, and provide a meaningful service or solution. Your project can be tailored to any area of interest, including education, entertainment, productivity, health, or social engagement.

The web-app should feature personalised elements where applicable, such as customisable settings or AI-driven recommendations, and must prioritise security to protect user data. The application's design, features, and overall purpose are entirely up to you. The goal is to create a web-based solution that enhances user experience securely and meaningfully.

---

## Stage 1: Identifying and Defining (20 Marks)

**Deadline: Term 1, Week 3**

This is the first critical phase of your software engineering project. Stage 1 requires you to establish a clear understanding of your project, including who it's for, what problem it solves, and how you'll measure success. This foundation will guide all subsequent development work.

### Why This Stage Matters

One of the leading causes of project failure in software development is the lack of clear and well-defined requirements. Studies show that a significant percentage of software projects fail because they run over budget, miss deadlines, or don't deliver what users need. Many of these issues stem from poor initial planning and an incomplete understanding of the problem.

The requirements phase must be thorough and accurate. It serves several key purposes:

- **Guiding development**: The requirements act as a roadmap for the development team.
- **Validating success**: The final product can be tested against the requirements to determine whether it meets its objectives.
- **Setting expectations**: Clear requirements ensure that all stakeholders understand what the system will and will not deliver.

---

## 1.1 Client Scenario (3 Marks)

### What You Need to Do

Define a clear scenario based on the client's needs, including the application's purpose, target audience, and main goals.

### How to Approach It

The first step in defining the requirements is to clearly establish the need for your software solution or identify an opportunity where technology can bring improvement. You should begin by identifying and documenting the needs through techniques such as:

- **Interviews with stakeholders** to understand their needs
- **Questionnaires** to gather input from a wide range of potential users
- **Observations** of current systems or processes to pinpoint inefficiencies

Your client scenario should answer these questions:

- Who is your client or end user? (Be specific about your target audience)
- What problem does your application solve for them?
- What is the current situation or challenge they face?
- How would your application improve their situation?
- What is the primary purpose of your application?

**By the end of this section, you should have a clear understanding of why your project is necessary.**

### Example Approach

Instead of a vague statement like "I'm making a task manager," you would write: "The application is designed for busy university students who struggle to manage multiple assignments across different subjects. The primary purpose is to provide a centralised platform where students can track assignment deadlines, set reminders, and receive personalised alerts based on their submission dates."

---

## 1.2 Environmental Specification (3 Marks)

### What You Need to Do

Document the software and hardware environments needed, specifying platform, browser, and technical compatibility.

### How to Approach It

This section outlines the technical requirements and constraints within which your application must operate. You need to consider both the software and hardware environment.

**Software Environment:**
- Which operating systems will your application run on? (Windows, macOS, Linux, or all?)
- Which web browsers will it support? (Chrome, Firefox, Safari, Edge, or all?)
- What framework will you use? (Flask is the requirement, unless you have teacher approval for an alternative)
- What database system will you use? (e.g., SQLite, PostgreSQL, MySQL)
- What programming languages and libraries will you need?

**Hardware Environment:**
- What are the minimum system requirements? (RAM, storage space, processor)
- What internet connectivity is required?
- Will the application work on mobile devices or tablets, or desktop only?
- What screen resolutions should it support?

**Technical Compatibility:**
- Will the application need to integrate with any external services or APIs?
- What are the performance expectations? (e.g., must load in under X seconds)
- What security standards must be met?

### Example Environmental Specification

"The application will be built using Flask as the web framework with a SQLite database backend. It will run on all major operating systems (Windows, macOS, Linux) and be compatible with the latest versions of Chrome, Firefox, Safari, and Edge. The application is designed for desktop use with a minimum screen resolution of 1024x768. It requires a stable internet connection for real-time features and will be hosted on a cloud platform. The application must load within 3 seconds and comply with GDPR data protection standards."

---

## 1.3 List of Objectives (3 Marks)

### What You Need to Do

Develop a list of specific objectives the application must achieve, focusing on functionality, user experience, and performance.

### How to Approach It

Objectives are specific, measurable goals that your application must accomplish. They should be clear enough that you can determine at the end of development whether you've achieved them or not.

**Functional Objectives** (What the application must do):
- What core features must the application have?
- What data must users be able to input, store, and retrieve?
- What actions should users be able to perform?

**User Experience Objectives** (How the application should feel):
- Should the interface be intuitive and easy to navigate?
- Should the application be accessible to users with different abilities?
- Should the application provide real-time feedback to users?

**Performance Objectives** (How well it should work):
- How responsive should the application be?
- How many concurrent users should it support?
- What data capacity must it handle?

### Structure Your Objectives

Write your objectives using clear, specific language. Use action verbs and make them measurable:

- **Good objective**: "Users must be able to create, edit, and delete personal tasks with due dates, and the system must send email reminders 24 hours before a due date."
- **Poor objective**: "Make a task manager that works well."

### Example List of Objectives

1. Allow users to register and log into the application securely
2. Enable users to create, view, edit, and delete personal tasks
3. Automatically categorise tasks by subject or priority level
4. Send email reminders 24 hours before assignment deadlines
5. Display a visual calendar showing all upcoming deadlines
6. Allow users to share tasks with classmates and assign responsibilities
7. Provide a dashboard that shows task completion progress
8. Store all user data securely and maintain data privacy
9. Ensure the application loads within 3 seconds on standard internet connections
10. Provide a mobile-responsive interface for tablets and smartphones

---

## 1.4 Performance Criteria (3 Marks)

### What You Need to Do

Outline performance metrics, such as security standards, usability goals, and loading times, to guide development and testing.

### How to Approach It

Performance criteria are the measurable standards against which you will evaluate whether your application successfully meets the objectives. They include security, usability, and technical performance metrics.

**Security Standards:**
- How will user data be protected? (encryption, password hashing, etc.)
- What authentication methods will be used?
- How will you prevent common vulnerabilities? (SQL injection, cross-site scripting, etc.)
- What data backup and recovery procedures will be in place?

**Usability Goals:**
- How quickly can new users learn to use the application?
- What is the maximum number of clicks to complete a task?
- Should the interface follow specific design principles?
- Will the application be accessible to users with disabilities?

**Performance Metrics:**
- What is the maximum acceptable page load time?
- How many simultaneous users should the application support?
- What is the maximum database size the application should handle?
- How often should the system be available? (uptime requirement)

### Example Performance Criteria

| Criterion | Target |
|-----------|--------|
| Page load time | < 3 seconds on standard internet connections |
| Database encryption | All passwords hashed with bcrypt algorithm |
| User authentication | Secure login with email and password |
| Data backup | Daily automated backups to cloud storage |
| Accessibility | WCAG 2.1 AA compliance for colour contrast and keyboard navigation |
| Concurrent users | Support minimum 100 simultaneous users |
| Form completion | Maximum 3 clicks to create a new task |
| Browser compatibility | Latest versions of Chrome, Firefox, Safari, Edge |
| Mobile responsiveness | Functional on screens 320px and wider |

---

## 1.5 IPO (Input-Process-Output) Chart (3 Marks)

### What You Need to Do

Create an IPO chart to outline each application feature's inputs, processes, and outputs.

### What is an IPO Chart?

An IPO chart is a planning tool that breaks down each major feature or function of your application into three components:

- **Input**: What data or information does the user provide or what data is received from external sources?
- **Process**: What happens to that data? What operations, calculations, validations, or transformations occur?
- **Output**: What result, information, or feedback is presented to the user or stored in the system?

### How to Create Your IPO Chart

For each major feature of your application, create a row in a table with these three columns. Be specific and detailed about what happens at each stage.

### Example IPO Chart

| Feature | Input | Process | Output |
|---------|-------|---------|--------|
| **User Registration** | Username, email, password, confirm password | Validate email format; Check username uniqueness; Hash password; Store in database | Success message; Redirect to login page; Error message if validation fails |
| **Create Task** | Task title, description, due date, subject, priority | Validate all fields are filled; Assign to logged-in user; Store in database; Check for scheduling conflicts | Task appears on dashboard; Calendar updates; Confirmation message displayed |
| **Set Reminder** | Task ID, reminder time before deadline | Calculate reminder date/time; Store in reminder table; Schedule notification | Confirmation message; Reminder appears in user's reminder list |
| **View Dashboard** | User ID (automatically from login) | Retrieve all user's tasks from database; Filter by status; Sort by due date; Calculate completion percentage | Display list of tasks; Show progress bar; Display upcoming deadlines in calendar view |
| **Edit Task** | Task ID, updated fields (title, date, etc.) | Validate changes; Update database record; Check for conflicts | Confirmation message; Updated task displays on dashboard |

### Tips for Your IPO Chart

- Include all major features of your application
- Be detailed enough that someone else could understand the process
- Consider what could go wrong and how errors are handled (validation, error messages)
- Think about how data flows through your system
- Remember that some inputs might come from the database or system, not just the user

---

## 1.6 Gantt Chart (5 Marks)

### What You Need to Do

Prepare a Gantt chart that maps out the timeline for each task, with key milestones and deadlines.

### What is a Gantt Chart?

A Gantt chart is a visual tool that shows the timeline of a project. It displays tasks as horizontal bars along a timeline, showing when each task starts, when it finishes, and how long it takes. Gantt charts are essential for project management because they help you:

- Plan timelines and understand project duration
- Track task dependencies (which tasks must be completed before others can start)
- Identify the critical path (essential task sequences that directly affect the project timeline)
- Show which phases of the project can run simultaneously
- Keep track of deadlines and ensure everyone knows their responsibilities
- Monitor progress and adjust plans as needed

### Key Elements of a Gantt Chart

**Tasks**: Break your project down into major phases and tasks. Common phases for software projects include:
- Planning and requirements gathering (current stage)
- System design and architecture
- Frontend development
- Backend development
- Database design and implementation
- Integration and testing
- Deployment and final review

**Timeline**: Your chart should span from now until the submission deadline (Friday, March 20, 2026).

**Milestones**: Mark important checkpoints, such as:
- Completion of Stage 1 (Week 3)
- Completion of Stage 2 (research and planning)
- Start of development
- Completion of core features
- Start of testing
- Submission deadline

**Dependencies**: Show which tasks must be completed before others can start. For example, database design must typically occur before backend development.

**Resources**: Indicate who is responsible for each task (in this case, it's you, but if working in a team, assign team members).

### Planning Your Project Timeline

Your project runs from now until the submission deadline on **Friday, March 20, 2026**. Work backwards from this date:

- **Stage 1 deadline**: Term 1, Week 3
- **Stage 2 deadline**: Term 1 (research and planning)
- **Stage 3.1 deadline**: Development phase
- **Final submission**: March 20, 2026

### How to Create Your Gantt Chart

You can create your Gantt chart using:
- Excel or Google Sheets (with conditional formatting or built-in features)
- Dedicated tools like Microsoft Project, Asana, Trello, or Jira
- Online Gantt chart creators
- Paper and pencil (though digital is preferred)

**Your chart should show:**
1. Task names and descriptions
2. Start and end dates for each task
3. Duration of each task (in days or weeks)
4. Task dependencies with arrows or lines
5. Milestones marked as diamonds or special symbols
6. A clear timeline along the top showing dates or weeks
7. Indication of who is responsible for each task

### Example Gantt Chart Structure

```
Task                          | Week 1-2 | Week 3 | Week 4-5 | Week 6-8 | Week 9-10 | Week 11-14
--------------------------------------------------------------------------------------------------
Stage 1: Requirements         | [████]   |        |          |          |           |
  - Client Scenario           | [██]     |        |          |          |           |
  - Environmental Spec        | [██]     |        |          |          |           |
  - Objectives & Criteria     | [██]     |        |          |          |           |
  - IPO & Gantt               |   [██]   |        |          |          |           |
Stage 2: Research & Planning  |          | [██████████]  |          |           |
  - Research technologies     |          | [██]   |          |          |           |
  - Design database schema    |          | [██]   |          |          |           |
  - Wireframe design          |          |   [██████]    |          |           |
Stage 3: Development          |          |        | [██████████████]  |           |
  - Backend setup (Flask)     |          |        | [██]     |          |           |
  - Database implementation   |          |        | [██]     |          |           |
  - Core feature development  |          |        |      [████████]    |           |
  - Frontend development      |          |        |      [████████]    |           |
  - Integration & testing     |          |        |          | [██████] |           |
  - Final review & polish     |          |        |          |      [██████]      |
Final Submission              |          |        |          |          |           | [Submit]
```

### Tips for Your Gantt Chart

- Be realistic about how long tasks will take
- Build in buffer time for unexpected issues
- Identify which tasks are on the critical path (delays here delay the whole project)
- Update your Gantt chart regularly during development to reflect actual progress
- Show dependencies between tasks so you understand what can be done in parallel
- Include all team members' names if working in a group

---

## Requirements Verification

Once you have completed all sections of Stage 1, verify that your requirements are clear, complete, and achievable.

Verification involves reviewing your work to confirm that:
- Your client scenario clearly explains who the users are and why they need your application
- Your environmental specification is detailed and realistic
- Your objectives are specific, measurable, and achievable
- Your performance criteria are testable and realistic
- Your IPO chart covers all major features with sufficient detail
- Your Gantt chart is realistic and includes all major phases

Effective requirement verification also ensures that every requirement is testable. For each objective, there should be a clear way to measure whether your final application meets the specified criteria.

---

## Submission Requirements

All Stage 1 documentation should be completed and submitted on OneDrive according to the milestones set. Your submission should include:

1. **Client Scenario** (3 marks)
2. **Environmental Specification** (3 marks)
3. **List of Objectives** (3 marks)
4. **Performance Criteria** (3 marks)
5. **IPO Chart** (3 marks)
6. **Gantt Chart** (5 marks)

**Total Stage 1: 20 Marks**

---

## Key Takeaways

- Stage 1 establishes the foundation for your entire project
- Clear requirements prevent costly mistakes and delays later
- Take time to thoroughly understand the problem before coding
- Document everything so it can guide your development
- Verify that all requirements are clear and achievable
- Your Gantt chart will help you stay on schedule throughout the project

Good luck with your Software Engineering Project!