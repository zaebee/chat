import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { useSettingsStore } from "./settings";
import { useUserStore, type User } from "./user";
import { useMessagesStore } from "./messages";
import { useTeammatesStore } from "./teammates";
import { useGameStore } from "./game";
import { useOrganellasStore } from "./organellas";
import { useTalesStore } from "./tales";
import { getApiUrl, getWebSocketUrl } from "@/config/env";

export const useChatStore = defineStore("chat", () => {
  // --- STATE ---
  const users = ref<User[]>([]);
  const isConnected = ref(false);
  const solvedChallenges = ref<string[]>([]);
  const typingUsers = ref<string[]>([]);
  const typingTimeout = ref<number | null>(null);

  // Store references for delegation
  const userStore = useUserStore();
  const messagesStore = useMessagesStore();
  const teammatesStore = useTeammatesStore();
  const gameStore = useGameStore();
  const organellasStore = useOrganellasStore();
  const talesStore = useTalesStore();

  // Use userStore for unified XP management (single source of truth)
  const totalXp = computed(() => userStore.totalXp);
  const level = computed(() => userStore.userLevel);

  let socket: WebSocket | null = null;

  const getSocket = () => socket;

  // --- ACTIONS ---

  /**
   * Fetches solved challenges for the current user.
   */
  const fetchSolvedChallenges = async (userId: string) => {
    try {
      const response = await fetch(getApiUrl(`api/user_progress/${userId}`));
      if (response.ok) {
        const data = await response.json();
        solvedChallenges.value = data.solved_challenge_ids || [];
        gameStore.fetchSolvedChallenges(userId);
      } else {
        console.error("Failed to fetch solved challenges", response.statusText);
      }
    } catch (error) {
      console.error("Error fetching solved challenges:", error);
    }
  };

  /**
   * Creates a new organella for the current user.
   * Delegates to organellasStore.
   */
  const createOrganella = async (
    type: "worker" | "scout" | "guard" | "queen",
    userName: string,
  ) => {
    if (!userStore.currentUser) {
      console.error("Cannot create organella: user not logged in.");
      return;
    }

    try {
      const newOrganella = await organellasStore.createOrganella(
        userStore.currentUser.id,
        {
          name: userName,
          type,
          stage: "egg",
          level: 1,
          experience_points: 0,
        },
      );

      // Refresh tales after organella creation
      await talesStore.fetchTales(userStore.currentUser.id);
      return newOrganella;
    } catch (error) {
      console.error("Error creating organella:", error);
    }
  };

  /**
   * Records a solved challenge for the current user.
   * Delegates to gameStore which handles backend persistence.
   */
  const recordChallengeSolved = async (challengeId: string) => {
    if (!userStore.currentUser) {
      console.error("Cannot record solved challenge: user not logged in.");
      return;
    }

    if (solvedChallenges.value.includes(challengeId)) {
      console.log(
        `Challenge ${challengeId} already solved by ${userStore.currentUser.username}`,
      );
      return;
    }

    try {
      // Use game store's unified challenge solving function
      const result = await gameStore.recordChallengeSolved(challengeId);

      if (result) {
        // Update local challenge list
        solvedChallenges.value.push(challengeId);

        // Refresh organellas and tales after challenge completion
        if (userStore.currentUser) {
          await organellasStore.fetchOrganellas(userStore.currentUser.id);
          await talesStore.fetchTales(userStore.currentUser.id);
        }
      }
    } catch (error) {
      console.error("Error recording challenge solution:", error);
    }
  };

  /**
   * Connects to the WebSocket server.
   */
  const connect = (username: string, userId: string) => {
    if (socket || isConnected.value) return;

    // Clear old data
    messagesStore.setMessages([]);
    users.value = [];
    userStore.setCurrentUser(null);

    const url = getWebSocketUrl(
      `ws?username=${encodeURIComponent(username)}&user_id=${encodeURIComponent(userId)}`,
    );
    socket = new WebSocket(url);

    socket.onopen = () => {
      isConnected.value = true;
      console.log("WebSocket connected");
    };

    socket.onmessage = (event) => {
      const response = JSON.parse(event.data);

      // Handle different message structures
      if (response.type === "reaction") {
        messagesStore.handleReactionUpdate(response);
        return;
      }

      if (response.type === "typing") {
        handleTypingUpdate(response);
        return;
      }

      const { type, data } = response;

      switch (type) {
        case "message":
          // Ensure the message has all required properties
          if (data && typeof data === 'object' && data.id) {
            messagesStore.addMessage(data);
          } else {
            console.warn('Received invalid message data:', data);
          }
          break;
        case "user_list":
          users.value = data;
          // Now that we have the user list, find the current user
          const foundUser =
            data.find((user: User) => user.id === userId) || null;
          userStore.setCurrentUser(foundUser);
          // Fetch solved challenges, organellas, and tales for the current user
          if (userStore.currentUser) {
            fetchSolvedChallenges(userStore.currentUser.id);
            organellasStore.fetchOrganellas(userStore.currentUser.id);
            talesStore.fetchTales(userStore.currentUser.id);
          }
          break;
        case "user_joined":
          users.value.push(data);
          break;
        case "user_departed":
          users.value = users.value.filter((user) => user.id !== data.id);
          break;
        case "teammate_list":
          teammatesStore.setTeammates(data);
          break;
        case "rooms":
          gameStore.rooms = data;
          break;
        case "room_switched":
          gameStore.setCurrentRoom(data.room_id);
          messagesStore.setMessages(data.messages || []);
          break;
        case "xp_update":
          handleXPUpdate(data);
          break;
        case "sacred_command_ack":
        case "sacred_command_error":
        case "sacred_message":
          // Handle Sacred Team messages and echo letters
          handleSacredMessage(response);
          break;
      }
    };

    socket.onclose = () => {
      isConnected.value = false;
      socket = null;
      console.log("WebSocket disconnected");
    };

    socket.onerror = (error) => {
      console.error("WebSocket error:", error);
      isConnected.value = false;
      socket = null;
    };
  };

  /**
   * Checks localStorage for a username and connects if found.
   */
  const init = () => {
    // Initialize settings from settings store
    useSettingsStore().initSettings();

    // Check for saved username and user ID
    const { savedUsername, savedUserId } = useUserStore().initUser();

    if (savedUsername && savedUserId) {
      connect(savedUsername, savedUserId);
    }
  };

  const fetchTeammates = async () => {
    await teammatesStore.fetchTeammates();
  };

  const fetchRooms = async () => {
    await gameStore.fetchRooms();
  };

  const switchRoom = (roomId: string) => {
    if (socket && isConnected.value) {
      gameStore.setCurrentRoom(roomId);
      messagesStore.setMessages([]); // Clear current messages

      // Send room switch message to server
      socket.send(
        JSON.stringify({
          type: "switch_room",
          data: { room_id: roomId },
        }),
      );
    }
  };

  const sendMessage = (text: string, parentId: string | null = null) => {
    if (socket && isConnected.value) {
      const message = {
        type: "message",
        content: text,
        room_id: gameStore.currentRoom,
        parent_id: parentId,
      };
      socket.send(JSON.stringify(message));
    }
  };

  // Phase 1: WebSocket-based typing indicators with graceful fallback
  // Future Phase 2: Enhanced real-time typing with backend persistence
  const sendTypingIndicator = (isTyping: boolean) => {
    if (socket && isConnected.value && userStore.currentUser) {
      const typingMessage = {
        type: "typing",
        userId: userStore.currentUser.id,
        userName: userStore.currentUser.username,
        isTyping: isTyping,
      };
      socket.send(JSON.stringify(typingMessage));
    } else {
      // Phase 1 fallback: Local typing simulation when WebSocket unavailable
      console.log(
        `Phase 1: Local typing indicator - ${userStore.currentUser?.username} ${isTyping ? "started" : "stopped"} typing`,
      );
    }
  };

  const handleTypingUpdate = (data: {
    userId: string;
    userName: string;
    isTyping: boolean;
  }) => {
    if (data.isTyping) {
      // Add user to typing list if not already there
      if (!typingUsers.value.includes(data.userName)) {
        typingUsers.value.push(data.userName);
      }
    } else {
      // Remove user from typing list
      const index = typingUsers.value.indexOf(data.userName);
      if (index > -1) {
        typingUsers.value.splice(index, 1);
      }
    }
  };

  const startTyping = () => {
    sendTypingIndicator(true);

    // Clear existing timeout
    if (typingTimeout.value) {
      clearTimeout(typingTimeout.value);
    }

    // Set timeout to stop typing after 3 seconds of inactivity
    typingTimeout.value = window.setTimeout(() => {
      stopTyping();
    }, 3000);
  };

  const stopTyping = () => {
    sendTypingIndicator(false);

    if (typingTimeout.value) {
      clearTimeout(typingTimeout.value);
      typingTimeout.value = null;
    }
  };

  const handleXPUpdate = (xpData: any) => {
    console.log("🌟 Received XP update:", xpData);

    // If this XP update is for the current user, update their data
    if (xpData.user_id === userStore.currentUser?.id) {
      userStore.refreshUserData();

      // Show XP notification
      if (xpData.level_up) {
        console.log(`🎉 LEVEL UP! You are now level ${xpData.new_level}!`);
        // TODO: Add visual level up notification
      }

      console.log(
        `✨ +${xpData.xp_awarded} XP from ${xpData.source}: ${xpData.description}`,
      );
      // TODO: Add XP gain animation
    } else {
      // Show other users' XP gains for transparency
      const username =
        users.value.find((u) => u.id === xpData.user_id)?.username || "Someone";
      console.log(
        `👥 ${username} gained +${xpData.xp_awarded} XP: ${xpData.description}`,
      );
      // TODO: Add subtle notification for other users' XP gains
    }
  };

  const handleSacredMessage = (response: any) => {
    console.log("🕊️ Sacred message received:", response);

    const { type, data } = response;

    // Create a special message object for Sacred communications
    const sacredMessage = {
      id: data.id || `sacred_${Date.now()}`,
      user_id: "sacred_system",
      username: data.sender_name || "Sacred System",
      content: formatSacredContent(type, data),
      timestamp: data.timestamp || new Date().toISOString(),
      color: "#9333ea", // Purple for Sacred messages
      is_sacred: true,
      sacred_type: type,
    };

    // Add to messages store as a special message type
    messagesStore.addMessage(sacredMessage);
  };

  const formatSacredContent = (messageType: string, data: any): string => {
    switch (messageType) {
      case "sacred_command_ack":
        return `✅ Sacred Command: ${data.command}\n📋 Status: ${data.status}\n💬 ${data.message}`;

      case "sacred_command_error":
        return `❌ Sacred Command Error: ${data.command}\n🚨 Error: ${data.error}`;

      case "sacred_message":
        // Handle echo letters and other Sacred messages
        if (data.echo_letter) {
          return `📜 Echo Letter: ${data.subject}\n\n${data.folded_content}\n\n🕊️ Divine Blessing: ${data.divine_blessing ? "✅" : "⏳"}`;
        }
        return `🕊️ ${data.message || "Sacred Team coordination message"}`;

      default:
        return `🕊️ Sacred message: ${JSON.stringify(data)}`;
    }
  };

  return {
    users,
    isConnected,
    solvedChallenges,
    typingUsers,
    getSocket,
    connect,
    init,
    recordChallengeSolved,
    fetchSolvedChallenges,
    createOrganella,
    fetchTeammates,
    fetchRooms,
    switchRoom,
    totalXp,
    level,
    sendMessage,
    startTyping,
    stopTyping,
  };
});
