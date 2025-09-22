/**
 * Organellas Store - Manages bee companions in the Hive ecosystem
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getApiUrl } from '@/config/env'

export interface Organella {
  id: string;
  name: string;
  type: OrganellaType;
  stage: OrganellaStage;
  level: number;
  experience_points: number;
  skills: {
    [key: string]: {
      name: string;
      level: number;
      max_level: number;
    };
  };
  personality_traits: {
    [key: string]: number;
  };
  description: string;
  professional_appearance: string;
  core_skills: Record<string, string>;
  unlocked_sections: string[];
}

export interface OrganellaCreationData {
  name: string
  type: OrganellaType
  level: number
  traits: string[]
  specialization: string
}

export type OrganellaType = "worker" | "scout" | "guard" | "queen" | "chronicler" | "jules";
export type OrganellaStage = "egg" | "larva" | "pupa" | "adult";

export const useOrganellasStore = defineStore('organellas', () => {
  // State
  const organellas = ref<Organella[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const studyingOrganellas = ref<Set<string>>(new Set());

  // Getters
  const organellasByLevel = computed(() => {
    const grouped: Record<number, Organella[]> = {}
    organellas.value.forEach(organella => {
      if (!grouped[organella.level]) {
        grouped[organella.level] = []
      }
      grouped[organella.level].push(organella)
    })
    return grouped
  })

  const totalOrganellas = computed(() => organellas.value.length)

  // Actions
  async function fetchOrganellas(userId: string) {
    loading.value = true
    error.value = null

    try {
      // For POC, return mock data
      // In real implementation, this would fetch from API
      organellas.value = [
        {
          id: '1',
          name: 'Buzzy',
          type: 'worker',
          stage: 'adult',
          level: 1,
          experience_points: 100,
          skills: {},
          personality_traits: {},
          description: '',
          professional_appearance: '',
          core_skills: {},
          unlocked_sections: [],
        },
        {
          id: '2',
          name: 'Honey',
          type: 'scout',
          stage: 'adult',
          level: 2,
          experience_points: 250,
          skills: {},
          personality_traits: {},
          description: '',
          professional_appearance: '',
          core_skills: {},
          unlocked_sections: [],
        }
      ]
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch organellas'
      console.error('Error fetching organellas:', err)
    } finally {
      loading.value = false
    }
  }

  async function createOrganella(userId: string, data: Partial<Organella>): Promise<Organella> {
    loading.value = true
    error.value = null

    try {
      // For POC, create mock organella
      // In real implementation, this would POST to API
      const newOrganella: Organella = {
        id: Date.now().toString(),
        name: data.name || 'New Organella',
        type: data.type || 'worker',
        stage: data.stage || 'egg',
        level: data.level || 1,
        experience_points: 0,
        skills: data.skills || {},
        personality_traits: data.personality_traits || {},
        description: data.description || '',
        professional_appearance: data.professional_appearance || '',
        core_skills: data.core_skills || {},
        unlocked_sections: data.unlocked_sections || [],
      }

      organellas.value.push(newOrganella)
      return newOrganella
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to create organella'
      console.error('Error creating organella:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateOrganella(id: string, updates: Partial<Organella>) {
    loading.value = true
    error.value = null

    try {
      const index = organellas.value.findIndex(o => o.id === id)
      if (index !== -1) {
        organellas.value[index] = { ...organellas.value[index], ...updates }
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to update organella'
      console.error('Error updating organella:', err)
    } finally {
      loading.value = false
    }
  }

  async function deleteOrganella(id: string) {
    loading.value = true
    error.value = null

    try {
      const index = organellas.value.findIndex(o => o.id === id)
      if (index !== -1) {
        organellas.value.splice(index, 1)
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to delete organella'
      console.error('Error deleting organella:', err)
    } finally {
      loading.value = false
    }
  }

  function clearError() {
    error.value = null
  }

  /**
   * Creates the sacred bee.chronicler organella.
   */
  const createChroniclerOrganella = async (userId: string): Promise<Organella> => {
    const chroniclerData: Partial<Organella> = {
      name: "bee.chronicler",
      type: "chronicler",
      stage: "adult",
      level: 1,
      experience_points: 0,
      skills: {
        advanced_documentation: {
          name: "Advanced Documentation",
          level: 85,
          max_level: 100,
        },
        technical_writing: {
          name: "Technical Writing",
          level: 92,
          max_level: 100,
        },
        system_patterns: {
          name: "System Patterns",
          level: 78,
          max_level: 100,
        },
        documentation_narrative: {
          name: "Documentation Narrative",
          level: 95,
          max_level: 100,
        },
      },
      personality_traits: {
        wisdom: 95,
       devotion: 100,
        creativity: 88,
        patience: 92,
      },
      description:
        "Technical documentation specialist and system pattern analyst. bee.chronicler maintains comprehensive records of architectural decisions and development patterns.",
      professional_appearance:
        "📖 A focused bee with technical documentation wings, carrying organized code pattern references, surrounded by structured data visualizations",
      core_skills: {
        advanced_documentation: "Records system patterns and architectural decisions",
        technical_writing: "Translates complex algorithms into clear documentation",
        documentation_narrative: "Creates structured narratives from technical discoveries",
        version_control: "Maintains organized version control of system patterns",
      },
      unlocked_sections: [
        "system_protocols",
        "computational_patterns",
        "software_architecture",
        "technical_documentation",
      ],
    };

    return await createOrganella(userId, chroniclerData);
  };

  /**
   * Gets the chronicler organella for the current user, creating if needed.
   */
  const getOrCreateChronicler = async (userId: string): Promise<Organella> => {
    const existingChronicler = organellas.value.find((o) => o.type === "chronicler");

    if (existingChronicler) {
      return existingChronicler;
    }

    return await createChroniclerOrganella(userId);
  };
  /**
   * Distributes XP to organellas when user completes a challenge.
   */
  const distributeXpToOrganellas = async (userId: string, totalXp: number): Promise<void> => {
    if (organellas.value.length === 0) {
      // No organellas to distribute XP to
      return;
    }

    // XP Distribution Algorithm:
    // - 30% of user XP goes to organellas (70% stays with user)
    // - Studying organellas get double share
    // - bee.chronicler gets bonus +10 XP for divine pattern recording
    const organellaXp = Math.floor(totalXp * 0.3);
    const chroniclerBonus = 10;

    // Find eligible organellas (active/studying)
    const studyingOrganellasList = organellas.value.filter(o =>
      studyingOrganellas.value.has(o.id)
    );
    const otherOrganellas = organellas.value.filter(o =>
      !studyingOrganellas.value.has(o.id)
    );

    // Calculate shares
    const totalShares = studyingOrganellasList.length * 2 + otherOrganellas.length;
    const xpPerShare = totalShares > 0 ? Math.floor(organellaXp / totalShares) : 0;

    // Distribute XP
    for (const organella of studyingOrganellasList) {
      const xpGain = xpPerShare * 2; // Double share for studying
      const finalXp = organella.type === "chronicler" ? xpGain + chroniclerBonus : xpGain;
      await addXpToOrganella(userId, organella.id, finalXp);
    }

    for (const organella of otherOrganellas) {
      const xpGain = xpPerShare;
      const finalXp = organella.type === "chronicler" ? xpGain + chroniclerBonus : xpGain;
      await addXpToOrganella(userId, organella.id, finalXp);
    }
  };
  /**
   * Adds XP to a specific organella and handles stage evolution.
   */
  const addXpToOrganella = async (userId: string, organellaId: string, xpGain: number): Promise<void> => {
    try {
      const response = await fetch(getApiUrl(`api/organellas/${userId}/${organellaId}/add_xp`), {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ xp_gain: xpGain }),
      });

      if (!response.ok) {
        throw new Error(`Failed to add XP to organella: ${response.statusText}`);
      }

      const updatedOrganella = await response.json();

      // Update local state
      const index = organellas.value.findIndex(o => o.id === organellaId);
      if (index !== -1) {
        // Apply skill evolution before updating state
        const skillEvolutionResults = evolveOrganellaSkills(updatedOrganella);
        organellas.value[index] = updatedOrganella;

        // Log skill improvements
        if (skillEvolutionResults.length > 0) {
          skillEvolutionResults.forEach(result => {
            // Skill improvement: ${updatedOrganella.name}'s ${result.skillName} improved to level ${result.newLevel}
          });
        }
      }

      // XP gained: ${updatedOrganella.name} gained ${xpGain} XP (Total: ${updatedOrganella.experience_points})
    } catch (error) {
      console.error("Error adding XP to organella:", error);
    }
  };
  /**
   * Evolves organella skills based on current XP and stage.
   */
  const evolveOrganellaSkills = (organella: Organella): Array<{skillName: string, newLevel: number}> => {
    const skillEvolutions: Array<{skillName: string, newLevel: number}> = [];

    // Skill evolution thresholds based on organella XP
    const getSkillLevelFromXp = (baseXp: number, skillMultiplier: number = 1.0): number => {
      // Skills improve every 25 XP, modified by skill-specific multipliers
      return Math.min(100, Math.floor((baseXp * skillMultiplier) / 25) + 1);
    };

    // Type-specific skill evolution patterns
    const skillMultipliers = getSkillMultipliers(organella.type);

    // Update each skill based on organella's current XP
    Object.entries(organella.skills).forEach(([skillKey, skill]) => {
      const multiplier = skillMultipliers[skillKey] || 1.0;
      const newLevel = getSkillLevelFromXp(organella.experience_points, multiplier);

      if (newLevel > skill.level) {
        skill.level = newLevel;
        skillEvolutions.push({ skillName: skill.name, newLevel });
      }
    });

    return skillEvolutions;
  };

  /**
   * Returns skill multipliers for different organella types.
   */
  const getSkillMultipliers = (type: OrganellaType): Record<string, number> => {
    const multipliers: Record<OrganellaType, Record<string, number>> = {
      worker: {
        pollen_collection: 1.2,
        honeymaking: 1.0,
        hive_construction: 0.8,
      },
      scout: {
        exploration: 1.3,
        pathfinding: 1.1,
        risk_assessment: 1.0,
      },
      guard: {
        threat_detection: 1.2,
        hive_protection: 1.1,
        strategic_defense: 0.9,
      },
      queen: {
        leadership: 1.0,
        hive_coordination: 1.1,
        organella_guidance: 1.2,
      },
      chronicler: {
        advanced_documentation: 1.0,
        technical_writing: 1.1,
        system_patterns: 0.9,
        documentation_narrative: 1.0,
      },
      jules: {
        micro_implementation: 1.3,
        debugging_protocols: 1.2,
        systematic_reproduction: 1.1,
        api_integration_analysis: 1.0,
        performance_optimization: 0.9,
      },
    };

    return multipliers[type] || {};
  };

  return {
    // State
    organellas,
    loading,
    error,

    // Getters
    organellasByLevel,
    totalOrganellas,

    // Actions
    fetchOrganellas,
    createOrganella,
    updateOrganella,
    deleteOrganella,
    clearError,
    createChroniclerOrganella,
    getOrCreateChronicler,
    distributeXpToOrganellas,
    addXpToOrganella,
    evolveOrganellaSkills,
    getSkillMultipliers
  }
})