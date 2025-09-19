import { defineStore } from "pinia";
import { ref, computed } from "vue";

export interface Room {
  id: string;
  name: string;
  description: string;
  type: string;
  created_by: string;
  created_at: string;
  is_archived: boolean;
}

import { useUserStore } from "./user";

export const useGameStore = defineStore("game", () => {
  const userStore = useUserStore();

  // --- STATE ---
  const rooms = ref<Room[]>([]);
  const currentRoom = ref<string>("general");
  const currentLevel = ref(1);
  const isConnected = ref(false);
  const solvedChallenges = ref<string[]>([]);

  // Gamification constants - these could be moved to a config store later
  const XP_PER_CHALLENGE = 100;
  const XP_FOR_LEVEL_UP = 500;

  // --- COMPUTED ---
  const totalXp = computed(() => {
    return solvedChallenges.value.length * XP_PER_CHALLENGE;
  });

  const level = computed(() => {
    return Math.floor(totalXp.value / XP_FOR_LEVEL_UP) + 1;
  });

  const xpProgress = computed(() => {
    return totalXp.value % XP_FOR_LEVEL_UP;
  });

  const xpToNextLevel = computed(() => {
    return XP_FOR_LEVEL_UP - xpProgress.value;
  });

  // --- ACTIONS ---

  /**
   * Fetches solved challenges for the current user.
   */
  const fetchSolvedChallenges = async (userId: string) => {
    try {
      const response = await fetch(`/api/user_progress/${userId}`);
      if (!response.ok) {
        throw new Error(`Failed to fetch solved challenges: ${response.statusText}`);
      }
      const data = await response.json();
      solvedChallenges.value = data.solved_challenges || [];
    } catch (error) {
      console.error("Error fetching solved challenges:", error);
    }
  };

  /**
   * Records a solved challenge.
   */
  const recordChallengeSolved = (challengeId: string) => {
    if (!solvedChallenges.value.includes(challengeId)) {
      solvedChallenges.value.push(challengeId);
    }
  };

  /**
   * Fetches available rooms.
   */
  const fetchRooms = async () => {
    try {
      const response = await fetch("/api/rooms");
      if (!response.ok) {
        throw new Error(`Failed to fetch rooms: ${response.statusText}`);
      }
      const data = await response.json();
      console.log("API response for rooms:", data);

      // Handle API response structure: {"rooms": [...]}
      const roomsArray = data.rooms || data;

      // Ensure we have an array and add missing fields with defaults
      if (Array.isArray(roomsArray)) {
        rooms.value = roomsArray.map((room: any) => ({
          id: room.id,
          name: room.name,
          description: room.description,
          type: room.type || "public", // Default type
          created_by: room.created_by || "system", // Default creator
          created_at: room.created_at,
          is_archived: room.is_archived || false // Default not archived
        }));
        console.log("Processed rooms:", rooms.value);
      } else {
        console.warn("Rooms data is not an array:", roomsArray);
        rooms.value = [];
      }
    } catch (error) {
      console.error("Error fetching rooms:", error);
      // Ensure rooms remains an array even on error
      if (!Array.isArray(rooms.value)) {
        rooms.value = [];
      }
    }
  };

  /**
   * Sets the current room.
   */
  const setCurrentRoom = (roomId: string) => {
    currentRoom.value = roomId;
  };

  /**
   * Sets connection status.
   */
  const setConnectionStatus = (connected: boolean) => {
    isConnected.value = connected;
  };

  /**
   * Sets the current level being viewed.
   */
  const setCurrentLevel = (level: number) => {
    currentLevel.value = level;
  };

  /**
   * Gets room by ID.
   */
  const getRoomById = (roomId: string): Room | undefined => {
    return rooms.value.find(room => room.id === roomId);
  };

  /**
   * Creates a new room.
   */
  const createRoom = async (roomData: { name: string; description: string; type: string; metadata: { theme: string } }) => {
    const currentUser = userStore.currentUser;
    if (!currentUser) {
      console.error("Cannot create room: user not logged in.");
      return;
    }

    const roomBlueprint = {
      ...roomData,
      created_by: currentUser.id,
    };

    try {
      const response = await fetch("/api/rooms/create", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(roomBlueprint),
      });

      if (!response.ok) {
        throw new Error(`Failed to create room: ${response.statusText}`);
      }

      // After creating, refresh the room list
      await fetchRooms();
    } catch (error) {
      console.error("Error creating room:", error);
    }
  };

  return {
    // State
    rooms,
    currentRoom,
    currentLevel,
    isConnected,
    solvedChallenges,

    // Computed
    totalXp,
    level,
    xpProgress,
    xpToNextLevel,

    // Actions
    fetchSolvedChallenges,
    recordChallengeSolved,
    fetchRooms,
    setCurrentRoom,
    setCurrentLevel,
    setConnectionStatus,
    getRoomById,
    createRoom,

    // Constants (exported for use in components)
    XP_PER_CHALLENGE,
    XP_FOR_LEVEL_UP,
  };
});