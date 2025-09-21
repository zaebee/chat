# FRD: Python Learning & Gamification Module

## 1. Feature Overview

This document outlines the requirements for a **Python Learning Module** to be integrated into the Hive Chat application. The module is designed for children and students learning Python, with a focus on collaboration, gamification, and direct interaction within the chat interface. It will provide a safe and engaging environment for students to learn, practice, and receive feedback on their coding skills, with tools for teachers to guide the process.

## 2. Core Components

### 2.1. Interactive Code Editor

A core component of the module is a browser-based code editor accessible directly within the chat UI.

- **Functionality:**
  - Opens in a modal, a new tab/pane, or as a special message type.
  - Python syntax highlighting.
  - Line numbers.
  - Basic code completion (optional V1, desirable V2).
  - Displays code output, including errors and print statements.
- **UX:** Clean, simple, and inviting for beginners. Distraction-free.

### 2.2. Sandboxed Python Runner

To ensure security and prevent abuse, all user-submitted code must be executed in a secure, sandboxed environment. No code should run on the server backend.

- **Proposed Technology:** **Pyodide** (or similar WebAssembly-based solution).
- **Rationale:**
  - **Security:** Code executes entirely within the user's browser. The server is never exposed to untrusted code.
  - **Performance:** Execution is immediate, with no server round-trip latency.
  - **Simplicity:** Reduces server-side complexity and maintenance overhead significantly.
- **Limitations:** The execution environment is limited to the browser and cannot interact with the server's file system or external services beyond what the browser allows.

### 2.3. Challenge & Quest System

This is the primary driver of the learning and gamification experience.

- **Challenge Types:**
  - **"Fix the Bug":** Students are given a piece of code with an error and must find and fix it.
  - **"Complete the Function":** A function signature and docstring are provided, and the student must write the body.
  - **"Code Golf":** Solve a problem using the fewest characters/lines.
  - **"Output This":** Write code that produces a specific, predefined output.
- **Teacher/Admin Role:** Teachers can create, assign, and manage challenges for their students or channels.
- **Challenge Bot:** A dedicated AI agent (`@CodeMaster`) can be implemented to automatically post daily or weekly challenges to a designated channel.

## 3. Gamification Elements

The goal is to make learning feel like a game, not a chore.

- **Experience Points (XP):** Students earn XP for:
  - Solving a challenge.
  - Completing a daily streak (e.g., solving one challenge per day).
  - Getting their code "starred" or upvoted by a teacher or peers.
- **Levels:** A simple leveling system where students advance based on XP earned.
- **Badges & Achievements:** Awarded for milestones.
  - _Examples:_ "First Function!", "Bug Squasher", "Loop Master", "Pythonista Level 5", "10-Day Streak".
- **Leaderboards:**
  - Displayed in a dedicated channel or tab.
  - Can be filtered by "Weekly" and "All-Time".
- **Social Reinforcement:** When a student solves a challenge or earns a badge, a celebratory message is automatically posted to the chat (e.g., "🎉 Congrats to **@student_name** for earning the **Bug Squasher** badge!").

## 4. User Experience (UX) & Chat Integration

### 4.1. Student Workflow

1.  A student sees a new challenge posted by the `@CodeMaster` bot or a teacher in a channel.
2.  They click a "Start Challenge" button directly on the message.
3.  The interactive code editor opens, pre-populated with the challenge's starting code.
4.  The student writes their code and can click a "Run" button to test it against predefined checks.
5.  The output and success/failure status are displayed directly in the editor pane.
6.  Once the solution is correct, they click "Submit".
7.  The system awards XP and any relevant badges, and a success message is posted to the channel.

### 4.2. Teacher Workflow

1.  A teacher can use a special command (e.g., `/create_challenge`) in the chat.
2.  A form opens in a modal to define the challenge type, description, starting code, and solution/test cases.
3.  The teacher can assign the challenge to a specific channel or user.

### 4.3. UI Integration

- **Code Snippet Message Type:** A new message format for displaying code. It should include syntax highlighting and a "Fork" or "Run" button.
- **"Playground" Channel:** A dedicated channel where students can freely write and share code snippets without being in a specific challenge.
- **Gamification Tab:** A section in the sidebar to view leaderboards, personal stats (XP, level), and earned badges.

## 5. Future Enhancements

- **Collaborative Coding:** Allow two or more students to work on the same code editor in real-time (pair programming).
- **Visualizations:** For more advanced topics, integrate a `matplotlib` or similar library (supported by Pyodide) to allow students to create plots and visualizations.
- **Code Replay:** Allow teachers to "replay" a student's coding process to see their thought process.
- **AI-Powered Hints:** An AI agent could provide contextual hints to students who are stuck on a problem.