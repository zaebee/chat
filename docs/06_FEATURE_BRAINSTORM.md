# 6. Feature Brainstorm & Analysis

This document contains a list of potential features for development, along with an analysis of their value and complexity. This serves as a high-level backlog for future planning.

### Learning Module - Content & Navigation

| Feature               | Description                                                                                        | Value Proposition                                                                                                  | Est. Complexity |
| :-------------------- | :------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------- | :-------------- |
| **More Challenges**   | Add more coding problems (e.g., string manipulation, list operations) to our `challenges.ts` file. | Provides more content for students to engage with immediately. It makes the playground more useful and replayable. | **Low**         |
| **Challenge List UI** | Create a UI where users can see and select from the list of all available challenges.              | A necessary UI improvement to make the playground scalable. It allows users to choose their learning path.         | **Low**         |

### Learning Module - Core Gamification

| Feature               | Description                                                                                                | Value Proposition                                                                                                   | Est. Complexity |
| :-------------------- | :--------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------ | :-------------- |
| **Core Gamification** | Implement a backend system to track user progress. Award XP for solved challenges and display user levels. | This is the "gamification" hook. It adds motivation, a sense of progression, and long-term engagement for students. | **Medium**      |

### Learning Module - Visual Challenges & Narrative (Current Focus)

| Feature                                    | Description                                                                                                                                                                                                                                                                                                                                                     | Value Proposition                                                                                   | Est. Complexity |
| :----------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------- | :-------------- |
| **Visual Challenges Research & Prototype** | Investigate Pyodide's capabilities for visual output (e.g., Python Turtle, SVG generation) and create a minimal end-to-end prototype.                                                                                                                                                                                                                           | Unlocks a new, highly engaging type of challenge. Essential for game-like learning experiences.     | **Medium-High** |
| **fAIry Tale / Hero Quest Narrative**      | Design and implement a narrative layer where user progress is visualized as a hero's journey, board game, or quest map. The "Hive of Seven Levels" SVG will serve as the visual map for this journey. **The "Benzene Honeyprint" and "Bee's Journey" SVGs are also excellent candidates for representing specific concepts or processes within the narrative.** | Provides strong motivation and a sense of purpose. Integrates gamification into a compelling story. | **Medium-High** |

### Future Vision Features

| Feature                                  | Description                                                                                                                                                | Value Proposition                                                                                                                   | Est. Complexity |
| :--------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------- | :-------------- |
| **Rich Chat Messages**                   | Improve the chat input to be a multiline text area and add support for Markdown, clickable links, and image previews.                                      | Massively improves the core chat experience, making it more expressive, modern, and useful for sharing code snippets and resources. | **Medium**      |
| **Teacher/Mentor Mode**                  | Create a special "teacher" role. Teachers could review student code submissions, send private hints ("whispers"), and see a dashboard of student progress. | Directly serves the "teacher" user role. Transforms the tool from just a playground into a true teaching and mentoring platform.    | **High**        |
| **AI Learning Assistant**                | Integrate an AI bot (`@HintBot`). A stuck student could ask it for a small hint, a simpler explanation of an error, or a breakdown of a concept.           | Aligns with the "Human-AI Symbiosis" vision. Provides scalable, 24/7 assistance to students, freeing up teacher time.               | **High**        |
| **Collaborative Playground**             | Upgrade the playground to support real-time collaborative editing, like Google Docs or VS Code Live Share, with multiple cursors.                          | Massively enhances collaboration. Enables pair programming, live teacher demonstrations, and group problem-solving in real-time.    | **High**        |
| **Decentralized User Identity (libp2p)** | Shift user identity from UUIDs to libp2p Peer IDs, enabling true decentralized user management.                                                            | Foundational for a fully sovereign and decentralized application. Aligns with core project vision.                                  | **Very High**   |
| **Blockchain/Jetton Minting**            | Store challenge definitions on IPFS/blockchain and verify solutions via smart contracts, with token rewards for completion.                                | Creates a verifiable, incentivized, and decentralized learning ecosystem.                                                           | **Very High**   |

### Recommended Plan (Updated)

Our current focus is on **Visual Challenges & Narrative**.

1.  **Visual Challenges Research & Prototype**
2.  **fAIry Tale / Hero Quest Narrative (Design & Initial Implementation)**