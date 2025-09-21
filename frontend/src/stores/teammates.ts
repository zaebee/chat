import { defineStore } from "pinia";
import { ref } from "vue";
import { getApiUrl } from "@/config/env";

export interface HiveTeammate {
  id: string;
  name: string;
  type: string;
  status: string;
  capabilities: string[];
  active_tasks: number;
  health: string;
}

export const useTeammatesStore = defineStore("teammates", () => {
  // --- STATE ---
  const teammates = ref<HiveTeammate[]>([]);
  const isLoading = ref(false);

  // --- ACTIONS ---

  /**
   * Fetches teammates from the Hive API.
   */
  const fetchTeammates = async () => {
    isLoading.value = true;
    try {
      const response = await fetch(getApiUrl("api/hive/teammates"));
      if (!response.ok) {
        throw new Error(`Failed to fetch teammates: ${response.statusText}`);
      }
      const data = await response.json();
      teammates.value = Array.isArray(data) ? data : [];
    } catch (error) {
      console.error("Error fetching teammates:", error);
      // Ensure teammates remains an array even on error
      if (!Array.isArray(teammates.value)) {
        teammates.value = [];
      }
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Sets the teammates array directly.
   */
  const setTeammates = (newTeammates: HiveTeammate[]) => {
    teammates.value = newTeammates;
  };

  /**
   * Gets a teammate by ID.
   */
  const getTeammateById = (id: string): HiveTeammate | undefined => {
    return teammates.value.find(teammate => teammate.id === id);
  };

  /**
   * Gets teammates by type.
   */
  const getTeammatesByType = (type: string): HiveTeammate[] => {
    return teammates.value.filter(teammate => teammate.type === type);
  };

  /**
   * Gets teammates by status.
   */
  const getTeammatesByStatus = (status: string): HiveTeammate[] => {
    return teammates.value.filter(teammate => teammate.status === status);
  };

  /**
   * Updates a teammate's status.
   */
  const updateTeammateStatus = (id: string, status: string) => {
    const teammate = teammates.value.find(t => t.id === id);
    if (teammate) {
      teammate.status = status;
    }
  };

  return {
    teammates,
    isLoading,
    fetchTeammates,
    getTeammateById,
    getTeammatesByType,
    getTeammatesByStatus,
    updateTeammateStatus,
    setTeammates,
  };
});