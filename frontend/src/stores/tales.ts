import { defineStore } from "pinia";
import { ref } from "vue";

export interface TaleChapter {
  id: string;
  chapter_number: number;
  title: string;
  content: string;
  organella_involved: string | null;
  challenge_trigger: string | null;
  unlocked_at: string;
  chapter_type: "birth" | "milestone" | "evolution" | "discovery" | "triumph" | "collaboration";
  mood: string;
}

export const useTalesStore = defineStore("tales", () => {
  // --- STATE ---
  const tales = ref<TaleChapter[]>([]);
  const isLoading = ref(false);

  // --- ACTIONS ---

  /**
   * Fetches tales for the current user.
   */
  const fetchTales = async (userId: string) => {
    isLoading.value = true;
    try {
      const response = await fetch(`/api/tales/${userId}`);
      if (!response.ok) {
        throw new Error(`Failed to fetch tales: ${response.statusText}`);
      }
      const data = await response.json();
      tales.value = data;
    } catch (error) {
      console.error("Error fetching tales:", error);
    } finally {
      isLoading.value = false;
    }
  };
 /**
   * Gets tales by type.
   */
  const getTalesByType = (type: TaleChapter["chapter_type"]): TaleChapter[] => {
    return tales.value.filter((tale) => tale.chapter_type === type);
  };

  /**
   * Gets tales involving a specific organella.
   */
  const getTalesByOrganella = (organellaId: string): TaleChapter[] => {
    return tales.value.filter((tale) => tale.organella_involved === organellaId);
  };

  /**
   * Gets the latest tale.
   */
  const getLatestTale = (): TaleChapter | undefined => {
    return tales.value.sort(
      (a, b) => new Date(b.unlocked_at).getTime() - new Date(a.unlocked_at).getTime(),
    )[0];
  };

  /**
   * Gets tales sorted by chapter number.
   */
  const getSortedTales = (): TaleChapter[] => {
    return [...tales.value].sort((a, b) => a.chapter_number - b.chapter_number);
  };

  /**
   * Adds a new tale chapter.
   */
  const addTale = (tale: TaleChapter) => {
    tales.value.push(tale);
  };
  
  return {
    tales,
    isLoading,
    fetchTales,
    getTalesByType,
    getTalesByOrganella,
    getLatestTale,
    getSortedTales,
    addTale,
  };
});