import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { useSettingsStore } from "./settings";
import { useUserStore, type User } from "./user";
import { useMessagesStore } from "./messages";
import { useTeammatesStore } from "./teammates";
import { useGameStore } from "./game";
import { useOrganellasStore } from "./organellas";
import { useTalesStore } from "./tales";

export const useChatStore = defineStore("chat", () => {
  // --- STATE ---
  const users = ref<User[]>([]);
  const isConnected = ref(false);
  const solvedChallenges = ref<string[]>([]);

  // Store references for delegation
  const userStore = useUserStore();
  const messagesStore = useMessagesStore();
  const teammatesStore = useTeammatesStore();
  const gameStore = useGameStore();
  const organellasStore = useOrganellasStore();
  const talesStore = useTalesStore();

  // Gamification constants
  const XP_PER_CHALLENGE = 100;
  const XP_FOR_LEVEL_UP = 500; // Example: 500 XP to level up

  // Computed properties for gamification
  const totalXp = computed(() => {
    return solvedChallenges.value.length * XP_PER_CHALLENGE;
  });

  const level = computed(() => {
    return Math.floor(totalXp.value / XP_FOR_LEVEL_UP) + 1;
  });

  let socket: WebSocket | null = null;

  // --- ACTIONS ---

  /**
   * Fetches solved challenges for the current user.
   */
  const fetchSolvedChallenges = async (userId: string) => {
    try {
      const response = await fetch(`/api/user_progress/${userId}`);
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
      const newOrganella = await organellasStore.createOrganella(userStore.currentUser.id, {
        type,
        name: userName,
      });

      // Refresh tales after organella creation
      await talesStore.fetchTales(userStore.currentUser.id);
      return newOrganella;
    } catch (error) {
      console.error("Error creating organella:", error);
    }
  };

  /**
   * Records a solved challenge for the current user.
   * Delegates to gameStore.
   */
  const recordChallengeSolved = async (challengeId: string) => {
    if (!userStore.currentUser) {
      console.error("Cannot record solved challenge: user not logged in.");
      return;
    }
    if (solvedChallenges.value.includes(challengeId)) {
      console.log(`Challenge ${challengeId} already solved by ${userStore.currentUser.username}`);
      return;
    }

    try {
      const response = await fetch("/solve_challenge", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: userStore.currentUser.id,
          challenge_id: challengeId,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log(data.message);
        solvedChallenges.value.push(challengeId);
        gameStore.recordChallengeSolved(challengeId);

        // Refresh organellas and tales after challenge completion
        if (userStore.currentUser) {
          await organellasStore.fetchOrganellas(userStore.currentUser.id);
          await talesStore.fetchTales(userStore.currentUser.id);
        }
      } else {
        console.error("Failed to record challenge solution", response.statusText);
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

    const url = `wss://${window.location.host}/ws?username=${encodeURIComponent(username)}&user_id=${encodeURIComponent(userId)}`;
    socket = new WebSocket(url);

    socket.onopen = () => {
      isConnected.value = true;
      console.log("WebSocket connected");
    };

    socket.onmessage = (event) => {
      const response = JSON.parse(event.data);
      const { type, data } = response;

      switch (type) {
        case "message":
          messagesStore.addMessage(data);
          break;
        case "user_list":
          users.value = data;
          // Now that we have the user list, find the current user
          const foundUser = data.find((user: User) => user.id === userId) || null;
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
        data: {
          text: text,
          room_id: gameStore.currentRoom,
          parent_id: parentId,
        },
      };
      socket.send(JSON.stringify(message));
    }
  };

  return {
    users,
    isConnected,
    solvedChallenges,
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
  };
});
