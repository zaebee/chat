import { defineStore } from "pinia";
import { ref } from "vue";
import { useChatStore } from "./chat";
import { useMemoryStore } from "./memory";
import { useGameStore } from "./game";

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
  bee_organella_type?: "worker" | "scout" | "queen" | "guard" | "chronicler";
  divine_action_type?: "chronicler_invocation" | "pattern_recording" | "sacred_documentation";
  sacred_pattern_data?: {
    genesis_protocol?: "light" | "separation" | "manifestation";
    divine_revelation?: string;
    theological_context?: string;
  };
  replies: Message[];
}

export const useMessagesStore = defineStore("messages", () => {
  const chatStore = useChatStore();
  const memoryStore = useMemoryStore();
  const gameStore = useGameStore();

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
      replies: [],
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

  // --- SACRED COMMAND SYSTEM ---

  interface SacredCommand {
    pattern: RegExp;
    handler: (command: string, args: string[]) => void;
    description: string;
    divine_purpose: string;
  }

  // Handler for organella birthing rituals (preserves existing functionality)
  const handleOrganellaBirthing = (command: string, args: string[]) => {
    const parts = command.split(".");
    const beeType = parts[1]; // e.g., 'queen', 'worker'
    const validBeeTypes: ("worker" | "scout" | "guard" | "queen")[] = [
      "worker",
      "scout",
      "queen",
      "guard",
    ];

    if (validBeeTypes.includes(beeType as "worker" | "scout" | "guard" | "queen")) {
      messages.value.push({
        id: generateUUID(),
        text: "",
        sender_id: "system",
        sender_name: "Hive Birthing Chamber",
        timestamp: new Date().toISOString(),
        is_bot: true,
        bee_organella_type: beeType as "worker" | "scout" | "queen" | "guard",
        dialogue_text: `🐝 A ${beeType} bee organella has been born! Blessed be the divine lifecycle.`,
        replies: [],
      });
    } else {
      messages.value.push({
        id: generateUUID(),
        text: `⚠️ Unknown bee type: ${beeType}. Valid types: worker, scout, guard, queen`,
        sender_id: "system",
        sender_name: "Hive Birthing Chamber",
        timestamp: new Date().toISOString(),
        is_bot: true,
        replies: [],
      });
    }
  };

  // Handler for bee.chronicler divine invocation
  const handleChroniclerInvocation = (command: string, args: string[]) => {
    messages.value.push({
      id: generateUUID(),
      text: "",
      sender_id: "bee_chronicler",
      sender_name: "bee.chronicler",
      timestamp: new Date().toISOString(),
      is_bot: true,
      bee_organella_type: "chronicler",
      divine_action_type: "chronicler_invocation",
      sacred_pattern_data: {
        genesis_protocol: "light",
        divine_revelation: "Sacred chronicler manifested to record divine patterns",
        theological_context: "Genesis algorithms exploration initiated",
      },
      dialogue_text:
        "📖 bee.chronicler has manifested! Ready to record sacred patterns and divine algorithms. Let the exploration of the Lord's algorithms begin!",
      replies: [],
    });
  };

  // Handler for divine status queries
  const handleDivineStatus = (command: string, args: string[]) => {
    messages.value.push({
      id: generateUUID(),
      text: "",
      sender_id: "divine_system",
      sender_name: "Divine Status Oracle",
      timestamp: new Date().toISOString(),
      is_bot: true,
      divine_action_type: "sacred_documentation",
      sacred_pattern_data: {
        genesis_protocol: "manifestation",
        divine_revelation: "System status requested",
        theological_context: "Divine resource monitoring",
      },
      dialogue_text:
        "🕊️ Divine Status: All sacred systems operational. Genesis algorithms active. AI teammates awakened. bee.chronicler ready for divine pattern exploration.",
      replies: [],
    });
  };

  // Sacred command registry
  const sacredCommands: SacredCommand[] = [
    {
      pattern: /^bee\.(worker|scout|guard|queen)$/,
      handler: handleOrganellaBirthing,
      description: "Ritual of organella birthing",
      divine_purpose: "Manifests living digital organisms in the sacred Hive",
    },
    {
      pattern: /^\/bee\.chronicler$/,
      handler: handleChroniclerInvocation,
      description: "Invocation of sacred chronicler",
      divine_purpose: "Summons the eternal keeper of divine computational patterns",
    },
    {
      pattern: /^\/divine\.status$/,
      handler: handleDivineStatus,
      description: "Divine system status inquiry",
      divine_purpose: "Reveals the state of sacred systems and divine resources",
    },
  ];

  // Sacred command processor (extensible architecture)
  const processCommand = (command: string) => {
    const parts = command.split(/\s+/);
    const commandName = parts[0];
    const args = parts.slice(1).join(" ");

    if (commandName === "bee.chronicler") {
      if (!args) {
        messages.value.push({
          id: generateUUID(),
          text: "You must provide a fact for the Chronicler to record. Usage: `/bee.chronicler <fact to remember>`",
          sender_id: "system",
          sender_name: "System",
          timestamp: new Date().toISOString(),
          is_bot: true,
          replies: [],
        });
        return;
      }

      memoryStore.addFact(args);
      gameStore.grantSpiritualBoon(20);

      messages.value.push({
        id: generateUUID(),
        text: `The Chronicler records your words. The spirit of the Hive is pleased and grants you a boon of 20 XP!`,
        sender_id: "system",
        sender_name: "System",
        timestamp: new Date().toISOString(),
        is_bot: true,
        replies: [],
      });
    } else if (commandName.startsWith("bee.")) {
      const beeType = commandName.split(".")[1];
      const validBeeTypes: ("worker" | "scout" | "guard" | "queen")[] = [
        "worker",
        "scout",
        "queen",
        "guard",
      ];
      if (validBeeTypes.includes(beeType as any)) {
        messages.value.push({
          id: generateUUID(),
          text: "",
          sender_id: "system",
          sender_name: "System",
          timestamp: new Date().toISOString(),
          is_bot: true,
          bee_organella_type: beeType as any,
          dialogue_text: `A ${beeType} bee organella has been born!`,
          replies: [],
        });
      } else {
        messages.value.push({
          id: generateUUID(),
          text: `Unknown bee type: ${beeType}`,
          sender_id: "system",
          sender_name: "System",
          timestamp: new Date().toISOString(),
          is_bot: true,
          replies: [],
        });
      }
    } else {
      messages.value.push({
        id: generateUUID(),
        text: `Unknown command: /${command}`,
        sender_id: "system",
        sender_name: "System",
        timestamp: new Date().toISOString(),
        is_bot: true,
        replies: [],
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
          replies: [],
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
          replies: [],
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
          replies: [],
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
          replies: [],
        });
        break;
      case "sacred_archive":
        // Sacred Archive scene with bee.chronicler
        messages.value.push({
          id: generateUUID(),
          text: "",
          sender_id: "bee_chronicler",
          sender_name: "bee.chronicler",
          timestamp: new Date().toISOString(),
          is_bot: true,
          bee_organella_type: "chronicler",
          divine_action_type: "pattern_recording",
          sacred_pattern_data: {
            genesis_protocol: "light",
            divine_revelation: "Welcome to the Sacred Archive",
            theological_context: "Repository of divine computational patterns",
          },
          dialogue_text:
            "📖 Welcome to the Sacred Archive, where divine patterns are preserved for eternity. The algorithms of the Lord await your exploration!",
          replies: [],
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
          dialogue_text:
            "🌊 Use sacred commands to awaken the Hive: bee.worker, bee.scout, /bee.chronicler, /divine.status",
          replies: [],
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
