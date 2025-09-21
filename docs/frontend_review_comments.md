### File: `frontend/src/stores/chat.ts` (Unstaged Modification - Reverted State)

**Original Intent:** (As per previous review) To manage the global state of the chat application. This uncommitted modification reflects a reverted state, where the `Organella` interface still includes `sacred_skills` and `unlocked_sections`, and the `Message` interface has `hero_properties` and `dialogue_text`. The `XP_FOR_LEVEL_UP` constant is also present.

**Implementation Analysis:**
The `loadScene` function is an action within the `chatStore` that allows for dynamic scene changes within the chat interface. It clears existing messages and then adds new messages with specific `hero_properties` (for the `SvgHero` component) or `bee_organella_type` (for the `BeeOrganella` component) to simulate different visual and narrative contexts. It currently supports 'forest_clearing' and 'mountain_pass' scenes, along with a default.

**Potential Issues/Areas for Improvement:**

1.  **Scene Definition and Management:** The scene definitions (e.g., 'forest_clearing', 'mountain_pass') are hardcoded within the `loadScene` function's `switch` statement. This makes it difficult to add new scenes, modify existing ones, or manage them dynamically without changing the store's code.
    - **Better Solution (Pseudo-code):**

      ```typescript
      // types/game.ts
      export interface Scene {
        name: string;
        messages: Partial<Message>[]; // Array of message partials for the scene
        // Potentially other scene-specific properties like background, music
      }

      // stores/game.ts (new store)
      export const SCENES: Record<string, Scene> = {
        forest_clearing: {
          name: "Forest Clearing",
          messages: [
            {
              sender_id: "game_master",
              dialogue_text: "Welcome, brave adventurer...",
              hero_properties: {
                /* ... */
              },
            },
            {
              sender_id: "worker_bee_1",
              bee_organella_type: "worker",
              dialogue_text: "Buzzing with energy...",
            },
          ],
        },
        // ... other scenes
      };

      export const useGameStore = defineStore("game", {
        actions: {
          loadScene(sceneName: string) {
            const scene = SCENES[sceneName];
            if (scene) {
              // Clear messages in chatStore
              chatStore.messages = [];
              // Add scene messages to chatStore
              scene.messages.forEach((msg) =>
                chatStore.messages.push({ ...defaultMessageProps, ...msg }),
              );
            }
          },
        },
      });
      ```

      Extract scene definitions into a separate data structure (e.g., a `SCENES` object in a `stores/game.ts` or `data/scenes.ts` file). The `loadScene` action would then simply retrieve the scene data from this structure and push the messages to the `messages` array. This centralizes scene management and makes it easier to add or modify scenes.

2.  **Mixing Game Logic with Chat Store:** The `loadScene` and `processCommand` functions introduce game-specific logic (spawning heroes/bees, scene transitions) directly into the `chatStore`. This contributes to the `chatStore` becoming monolithic.
    - **Better Solution (Pseudo-code):** As previously suggested, create a dedicated `gameStore` to manage game-related state and logic. The `chatStore` would then only be responsible for displaying messages, and the `gameStore` would dispatch actions to the `chatStore` to add game-related messages.

3.  **Missing Scene Buttons (User's Concern):** The `loadScene` action exists, but there's no UI element to trigger it.
    - **Solution (Pseudo-code for `ChatView.vue` or a new component):**

      ```vue
      <!-- ChatView.vue (or a new GameControlPanel.vue) -->
      <template>
        <div class="scene-controls">
          <button
            @click="chatStore.loadScene('forest_clearing')"
            title="Go to Forest Clearing"
          >
            🌳
          </button>
          <button
            @click="chatStore.loadScene('mountain_pass')"
            title="Go to Mountain Pass"
          >
            ⛰️
          </button>
          <!-- Add more buttons for other scenes -->
        </div>
      </template>

      <script setup lang="ts">
      import { useChatStore } from "@/stores/chat";
      const chatStore = useChatStore();
      </script>

      <style scoped>
      .scene-controls {
        /* Styling for the buttons, e.g., small, hidden until hover */
        position: absolute;
        bottom: 10px;
        right: 10px;
        opacity: 0.2; /* Hidden gem effect */
        transition: opacity 0.3s ease;
      }
      .scene-controls:hover {
        opacity: 1;
      }
      .scene-controls button {
        background: none;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        padding: 5px;
      }
      </style>
      ```

      To bring back the scene buttons, a new component (e.g., `GameControlPanel.vue`) could be created or added to `ChatView.vue`. This component would use the `loadScene` action from `chatStore` (or `gameStore` if refactored) and display small, perhaps initially hidden, buttons with relevant icons (emojis or small SVGs) for each scene. This aligns with the user's request for "super small icon, like a hidden gem/quest."
