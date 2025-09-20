import { defineStore } from "pinia";
import { ref } from "vue";

export const useMemoryStore = defineStore("memory", () => {
  // --- STATE ---
  const facts = ref<string[]>([]);

  // --- ACTIONS ---

  /**
   * Adds a new fact to the memory.
   */
  const addFact = (fact: string) => {
    facts.value.push(fact);
  };

  return {
    facts,
    addFact,
  };
});
