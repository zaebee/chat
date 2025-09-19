import { defineStore } from "pinia";
import { ref } from "vue";
import { useChatStore } from "./chat";

// Helper to generate a UUID
function generateUUID(): string {
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (c) {
    const r = (Math.random() * 16) | 0,
      v = c === "x" ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

export interface Message {
  id: string;
  text: string;
  sender_id: string;
  sender_name: string;
  timestamp: string;
  room_id?: string;
  parent_id?: string;
  is_bot?: boolean;
  code_content?: string;
  code_language?: string;
  editor_id?: string;
  hero_properties?: {
    skinColor?: string;
    shirtColor?: string;
    swordBladeColor?: string;
    swordGuardColor?: string;
    strokeColor?: string;
    size?: number;
    animateSwing?: boolean;
  };
  dialogue_text?: string;
  isPeaking?: boolean; // Temporary for testing "Peak" effect
  isDecaying?: boolean; // Temporary for testing "Decay" effect
  bee_organella_type?: "worker" | "scout" | "queen" | "guard";
}

export const useMessagesStore = defineStore("messages", () => {
  const chatStore = useChatStore();

  // --- STATE ---
  const messages = ref<Message[]>([]);
  const inputPrompt = ref<string | null>(null);
  const inputResolver = ref<((value: string) => void) | null>(null);
  const isAiThinking = ref(false);
  const replyToMessageId = ref<string | null>(null);

  // --- ACTIONS ---

  /**
   * Sends input to a waiting Python script.
   */
  const sendPythonInput = (text: string) => {
    if (inputResolver.value) {
      inputResolver.value(text);
      inputPrompt.value = null;
      inputResolver.value = null;
    } else {
      console.warn("No Python input requested.");
    }
  };

  /**
   * Adds a Python output message to the chat.
   */
  const addPythonOutputMessage = (text: string) => {
    const message: Message = {
      id: generateUUID(),
      text: text,
      sender_id: "python_runtime",
      sender_name: "Python",
      timestamp: new Date().toISOString(),
      is_bot: true,
    };
    messages.value.push(message);
  };

  /**
   * Requests Python input from the user.
   */
  const requestPythonInput = (prompt: string, resolve: (value: string) => void) => {
    inputPrompt.value = prompt;
    inputResolver.value = resolve;
  };

  /**
   * Sends a message over the WebSocket by delegating to the chat store.
   */
  const sendMessage = (text: string, parentId: string | null = null) => {
    chatStore.sendMessage(text, parentId);
  };

  const setReplyToMessageId = (id: string | null) => {
    replyToMessageId.value = id;
  };

  const processCommand = (command: string) => {
    const parts = command.split(".");
    if (parts.length >= 2 && parts[0] === "bee") {
      const beeType = parts[1]; // e.g., 'queen', 'worker'
      const validBeeTypes: ("worker" | "scout" | "guard" | "queen")[] = [
        "worker",
        "scout",
        "queen",
        "guard",
      ];
      if (validBeeTypes.includes(beeType as "worker" | "scout" | "guard" | "queen")) {
        // Validate beeType
        messages.value.push({
          id: generateUUID(),
          text: "",
          sender_id: "system",
          sender_name: "System",
          timestamp: new Date().toISOString(),
          is_bot: true,
          bee_organella_type: beeType as "worker" | "scout" | "queen" | "guard", // Cast to OrganellaType after validation
          dialogue_text: `A ${beeType} bee organella has been born!`,
        });
      } else {
        messages.value.push({
          id: generateUUID(),
          text: `Unknown bee type: ${beeType}`,
          sender_id: "system",
          sender_name: "System",
          timestamp: new Date().toISOString(),
          is_bot: true,
        });
      }
    } else {
      messages.value.push({
        id: generateUUID(),
        text: `Unknown command: ${command}`,
        sender_id: "system",
        sender_name: "System",
        timestamp: new Date().toISOString(),
        is_bot: true,
      });
    }
  };

  const loadScene = (sceneName: string) => {
    // Clear existing messages for a fresh scene
    messages.value = [];

    switch (sceneName) {
      case "forest_clearing":
        // Set background
        // setBackgroundTheme('forest');

        // Spawn a hero with dialogue
        messages.value.push({
          id: generateUUID(),
          text: "",
          sender_id: "game_master",
          sender_name: "Game Master",
          timestamp: new Date().toISOString(),
          is_bot: true,
          hero_properties: {
            skinColor: "#f0cfb0",
            shirtColor: "#2b6cb0",
            swordBladeColor: "#e6eef6",
            swordGuardColor: "#b8860b",
            strokeColor: "#222",
            size: 1.2,
            animateSwing: true,
          },
          dialogue_text:
            "Welcome, brave adventurer, to the Forest Clearing! A new quest awaits you.",
        });

        // Spawn some worker bees
        messages.value.push({
          id: generateUUID(),
          text: "",
          sender_id: "worker_bee_1",
          sender_name: "Worker Bee",
          timestamp: new Date().toISOString(),
          is_bot: true,
          bee_organella_type: "worker",
          dialogue_text: "Buzzing with energy, ready to work!",
        });
        messages.value.push({
          id: generateUUID(),
          text: "",
          sender_id: "worker_bee_2",
          sender_name: "Worker Bee",
          timestamp: new Date().toISOString(),
          is_bot: true,
          bee_organella_type: "worker",
          dialogue_text: "Collecting pollen for the Hive!",
        });
        break;
      case "mountain_pass":
        // Set background
        // setBackgroundTheme('mountains');

        // Spawn a scout bee with dialogue
        messages.value.push({
          id: generateUUID(),
          text: "",
          sender_id: "scout_bee_1",
          sender_name: "Scout Bee",
          timestamp: new Date().toISOString(),
          is_bot: true,
          bee_organella_type: "scout",
          dialogue_text: "The path ahead is treacherous, but the view is grand!",
        });
        break;
      default:
        // Default scene (e.g., clear background, no special characters)
        // setBackgroundTheme('default');
        messages.value.push({
          id: generateUUID(),
          text: "The ocean is calm. What will emerge next?",
          sender_id: "system",
          sender_name: "System",
          timestamp: new Date().toISOString(),
          is_bot: true,
        });
        break;
    }
  };

  /**
   * Adds a message to the messages array.
   */
  const addMessage = (message: Message) => {
    messages.value.push(message);
  };

  /**
   * Sets the entire messages array (used for room switching).
   */
  const setMessages = (newMessages: Message[]) => {
    messages.value = newMessages;
  };

  return {
    messages,
    inputPrompt,
    inputResolver,
    isAiThinking,
    replyToMessageId,
    sendPythonInput,
    addPythonOutputMessage,
    requestPythonInput,
    addMessage,
    setMessages,
    sendMessage,
    setReplyToMessageId,
    processCommand,
    loadScene,
  };
});
