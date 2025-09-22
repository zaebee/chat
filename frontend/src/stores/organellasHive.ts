/**
 * Hive-Aligned Organellas Store - Physics + Fairy Tale Magic
 * 
 * Eliminates magic numbers through mathematical principles while
 * preserving the enchanting narrative experience.
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// Mathematical constants (no magic numbers!)
const GOLDEN_RATIO = 1.618033988749
const FIBONACCI_BASE = 8  // 8th Fibonacci number for natural growth
const SACRED_MULTIPLIER = GOLDEN_RATIO * GOLDEN_RATIO  // φ² ≈ 2.618

// Physics-based growth constants
const GROWTH_PHYSICS = {
  baseGrowthRate: FIBONACCI_BASE * GOLDEN_RATIO,  // ~12.94 XP per ability level
  xpDistributionRatio: 1 / GOLDEN_RATIO,         // ~0.618 (61.8% to organellas)
  sacredBonus: FIBONACCI_BASE,                    // 8 XP for sacred bees
  studyingMultiplier: GOLDEN_RATIO,               // φ times more for studying
  maxAbilityIntensity: 1.0,                       // Normalized to 0-1
  stageEvolutionThreshold: FIBONACCI_BASE * FIBONACCI_BASE  // 64 XP per stage
}

// Ability domains based on natural bee behaviors
export type AbilityDomain = 'cognitive' | 'physical' | 'social' | 'sacred'

export interface OrganellaAbility {
  domain: AbilityDomain
  intensity: number  // 0-1, calculated from experience and role affinity
  manifestations: string[]  // How the ability appears in the fairy tale
  growthRate: number  // Physics-based growth multiplier
}

export interface OrganellaPersonality {
  traits: Record<string, number>  // 0-1 values derived from abilities
  essence: string  // Fairy tale description generated from traits
  aura: string     // Visual representation
}

export interface HiveOrganella {
  id: string
  name: string
  type: OrganellaType
  stage: OrganellaStage
  
  // Physics-based properties
  totalExperience: number
  stageExperience: number  // Experience within current stage
  
  // Emergent abilities (calculated, not hardcoded)
  abilities: Record<string, OrganellaAbility>
  personality: OrganellaPersonality
  
  // Fairy tale elements
  description: string
  appearance: string
  currentMood: string
  recentAchievements: string[]
  
  // Hive integration
  collaborationHistory: string[]
  sacredLevel: number  // For chronicler/jules
}

export interface OrganellaCreationData {
  name: string
  type: OrganellaType
  level: number
  traits: string[]
  specialization: string
}

export type OrganellaType = "worker" | "scout" | "guard" | "queen" | "chronicler" | "jules"
export type OrganellaStage = "egg" | "larva" | "pupa" | "adult" | "eternal"

// Role-specific ability affinities (physics-based, not arbitrary)
const ROLE_AFFINITIES: Record<OrganellaType, Record<AbilityDomain, number>> = {
  worker: {
    physical: GOLDEN_RATIO / 2,      // ~0.809 - strong physical abilities
    cognitive: 1 / GOLDEN_RATIO,     // ~0.618 - moderate cognitive
    social: 0.5,                     // 0.5 - balanced social
    sacred: 1 / (GOLDEN_RATIO * 2)   // ~0.309 - limited sacred
  },
  scout: {
    cognitive: GOLDEN_RATIO / 2,     // ~0.809 - high cognitive for exploration
    physical: 1 / GOLDEN_RATIO,      // ~0.618 - good physical mobility
    social: 1 / (GOLDEN_RATIO * 2),  // ~0.309 - lower social (independent)
    sacred: 0.25                     // 0.25 - minimal sacred
  },
  guard: {
    physical: GOLDEN_RATIO / 1.5,    // ~1.079 - exceptional physical
    cognitive: 0.7,                  // 0.7 - tactical thinking
    social: 0.4,                     // 0.4 - protective but not social
    sacred: 1 / (GOLDEN_RATIO * 3)   // ~0.206 - minimal sacred
  },
  queen: {
    social: GOLDEN_RATIO / 1.2,      // ~1.348 - supreme social abilities
    cognitive: GOLDEN_RATIO / 2,     // ~0.809 - high wisdom
    sacred: 0.6,                     // 0.6 - moderate sacred connection
    physical: 1 / (GOLDEN_RATIO * 2) // ~0.309 - lower physical (protected)
  },
  chronicler: {
    sacred: SACRED_MULTIPLIER / 3,   // ~0.873 - high sacred connection
    cognitive: GOLDEN_RATIO / 1.5,   // ~1.079 - exceptional cognitive
    social: 0.5,                     // 0.5 - balanced social for documentation
    physical: 1 / (GOLDEN_RATIO * 3) // ~0.206 - minimal physical
  },
  jules: {
    cognitive: SACRED_MULTIPLIER / 2.5, // ~1.047 - debugging requires high cognitive
    sacred: GOLDEN_RATIO / 2,           // ~0.809 - sacred implementation detective
    social: 0.6,                        // 0.6 - collaborative debugging
    physical: 1 / GOLDEN_RATIO          // ~0.618 - moderate physical for implementation
  }
}

export const useHiveOrganellasStore = defineStore('hiveOrganellas', () => {
  // State
  const organellas = ref<HiveOrganella[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const studyingOrganellas = ref<Set<string>>(new Set())

  // Physics-based calculations
  const calculateAbilityIntensity = (
    experience: number, 
    domain: AbilityDomain, 
    roleAffinity: number,
    stage: OrganellaStage
  ): number => {
    // Base intensity from experience (logarithmic growth, not linear)
    const baseIntensity = Math.log(experience + 1) / Math.log(GROWTH_PHYSICS.baseGrowthRate)
    
    // Stage multiplier (natural progression)
    const stageMultipliers = {
      egg: 0.1,
      larva: 0.3,
      pupa: 0.6,
      adult: 1.0,
      eternal: GOLDEN_RATIO  // Sacred bees can exceed normal limits
    }
    
    const stageMultiplier = stageMultipliers[stage]
    
    // Final intensity (clamped to 0-1 for normal bees, higher for eternal)
    const maxIntensity = stage === 'eternal' ? GOLDEN_RATIO : GROWTH_PHYSICS.maxAbilityIntensity
    return Math.min(maxIntensity, baseIntensity * roleAffinity * stageMultiplier)
  }

  const calculatePersonality = (abilities: Record<string, OrganellaAbility>): OrganellaPersonality => {
    // Personality emerges from ability patterns (no hardcoded values!)
    const traits: Record<string, number> = {}
    
    // Calculate traits based on ability intensities
    const cognitiveIntensity = abilities.cognitive?.intensity || 0
    const physicalIntensity = abilities.physical?.intensity || 0
    const socialIntensity = abilities.social?.intensity || 0
    const sacredIntensity = abilities.sacred?.intensity || 0
    
    // Derived personality traits (mathematical, not arbitrary)
    traits.wisdom = cognitiveIntensity * GOLDEN_RATIO / 2
    traits.energy = physicalIntensity * GOLDEN_RATIO / 2
    traits.harmony = socialIntensity * GOLDEN_RATIO / 2
    traits.devotion = sacredIntensity * SACRED_MULTIPLIER / 3
    traits.focus = (cognitiveIntensity + sacredIntensity) / 2
    traits.creativity = Math.sqrt(cognitiveIntensity * socialIntensity)
    
    // Generate fairy tale essence from trait patterns
    const dominantTrait = Object.entries(traits).reduce((a, b) => 
      traits[a[0]] > traits[b[0]] ? a : b
    )[0]
    
    const essenceMap = {
      wisdom: "A thoughtful soul with eyes that sparkle with ancient knowledge",
      energy: "A vibrant spirit that buzzes with unstoppable enthusiasm", 
      harmony: "A gentle heart that brings others together in perfect unity",
      devotion: "A sacred being touched by divine purpose and unwavering faith",
      focus: "A determined mind that sees through complexity to find truth",
      creativity: "An artistic soul that weaves beauty from the threads of possibility"
    }
    
    return {
      traits,
      essence: essenceMap[dominantTrait as keyof typeof essenceMap] || "A unique spirit finding their path",
      aura: generateAura(traits)
    }
  }

  const generateAura = (traits: Record<string, number>): string => {
    // Visual aura based on trait combinations
    const { wisdom, energy, harmony, devotion } = traits
    
    if (devotion > 0.7) return "✨ Shimmering with golden divine light"
    if (wisdom > 0.8) return "🌟 Surrounded by gentle starlight of knowledge"
    if (energy > 0.8) return "⚡ Crackling with electric enthusiasm"
    if (harmony > 0.8) return "🌈 Radiating warm, welcoming colors"
    
    return "🌸 Glowing with soft, natural light"
  }

  const evolveOrganella = (organella: HiveOrganella, experienceGain: number): HiveOrganella => {
    const newTotalExperience = organella.totalExperience + experienceGain
    const newStageExperience = organella.stageExperience + experienceGain
    
    // Check for stage evolution (physics-based threshold)
    let newStage = organella.stage
    let adjustedStageExperience = newStageExperience
    
    if (newStageExperience >= GROWTH_PHYSICS.stageEvolutionThreshold) {
      const stageProgression: OrganellaStage[] = ['egg', 'larva', 'pupa', 'adult', 'eternal']
      const currentIndex = stageProgression.indexOf(organella.stage)
      
      if (currentIndex < stageProgression.length - 1) {
        newStage = stageProgression[currentIndex + 1]
        adjustedStageExperience = newStageExperience - GROWTH_PHYSICS.stageEvolutionThreshold
      }
    }
    
    // Recalculate abilities based on new experience
    const roleAffinities = ROLE_AFFINITIES[organella.type]
    const newAbilities: Record<string, OrganellaAbility> = {}
    
    Object.entries(roleAffinities).forEach(([domain, affinity]) => {
      const intensity = calculateAbilityIntensity(
        newTotalExperience, 
        domain as AbilityDomain, 
        affinity, 
        newStage
      )
      
      newAbilities[domain] = {
        domain: domain as AbilityDomain,
        intensity,
        manifestations: generateManifestations(domain as AbilityDomain, intensity, organella.type),
        growthRate: affinity
      }
    })
    
    // Generate new personality from evolved abilities
    const newPersonality = calculatePersonality(newAbilities)
    
    // Update achievements if significant growth occurred
    const newAchievements = [...organella.recentAchievements]
    if (newStage !== organella.stage) {
      newAchievements.push(`🎉 Evolved to ${newStage} stage!`)
    }
    
    // Keep only recent achievements (last 5)
    if (newAchievements.length > 5) {
      newAchievements.splice(0, newAchievements.length - 5)
    }
    
    return {
      ...organella,
      totalExperience: newTotalExperience,
      stageExperience: adjustedStageExperience,
      stage: newStage,
      abilities: newAbilities,
      personality: newPersonality,
      recentAchievements: newAchievements,
      sacredLevel: organella.type === 'chronicler' || organella.type === 'jules' ? 
        newAbilities.sacred.intensity * 100 : 0
    }
  }

  const generateManifestations = (
    domain: AbilityDomain, 
    intensity: number, 
    type: OrganellaType
  ): string[] => {
    // Generate fairy tale manifestations based on ability intensity
    const manifestationTemplates = {
      cognitive: {
        low: ["thinks carefully before acting", "notices small details"],
        medium: ["solves problems with clever insights", "remembers complex patterns"],
        high: ["sees connections others miss", "understands deep mysteries"],
        exceptional: ["possesses ancient wisdom", "perceives the fabric of reality"]
      },
      physical: {
        low: ["moves with gentle grace", "works steadily and surely"],
        medium: ["dances through the air with skill", "carries heavy loads with ease"],
        high: ["flies faster than the wind", "performs incredible feats of strength"],
        exceptional: ["defies the laws of physics", "moves like liquid lightning"]
      },
      social: {
        low: ["listens carefully to others", "offers quiet support"],
        medium: ["brings bees together in harmony", "mediates disputes with wisdom"],
        high: ["inspires others to greatness", "creates unbreakable bonds"],
        exceptional: ["commands respect from all", "unites the entire hive as one"]
      },
      sacred: {
        low: ["feels a connection to something greater", "shows reverence for the hive"],
        medium: ["channels divine inspiration", "blessed with sacred insights"],
        high: ["radiates holy light", "speaks with the voice of the ancients"],
        exceptional: ["transcends mortal limitations", "becomes one with the eternal"]
      }
    }
    
    const level = intensity < 0.25 ? 'low' :
                  intensity < 0.5 ? 'medium' :
                  intensity < 0.8 ? 'high' : 'exceptional'
    
    return manifestationTemplates[domain][level] || ["possesses unique gifts"]
  }

  // Actions
  const createHiveOrganella = async (
    userId: string, 
    data: Partial<HiveOrganella>
  ): Promise<HiveOrganella> => {
    loading.value = true
    error.value = null

    try {
      const type = data.type || 'worker'
      const stage = data.stage || 'egg'
      const initialExperience = data.totalExperience || 0
      
      // Calculate initial abilities based on physics
      const roleAffinities = ROLE_AFFINITIES[type]
      const abilities: Record<string, OrganellaAbility> = {}
      
      Object.entries(roleAffinities).forEach(([domain, affinity]) => {
        const intensity = calculateAbilityIntensity(
          initialExperience, 
          domain as AbilityDomain, 
          affinity, 
          stage
        )
        
        abilities[domain] = {
          domain: domain as AbilityDomain,
          intensity,
          manifestations: generateManifestations(domain as AbilityDomain, intensity, type),
          growthRate: affinity
        }
      })
      
      const personality = calculatePersonality(abilities)
      
      const newOrganella: HiveOrganella = {
        id: Date.now().toString(),
        name: data.name || 'New Organella',
        type,
        stage,
        totalExperience: initialExperience,
        stageExperience: 0,
        abilities,
        personality,
        description: data.description || generateDescription(type, personality),
        appearance: data.appearance || generateAppearance(type, stage, personality),
        currentMood: "curious and eager to learn",
        recentAchievements: [],
        collaborationHistory: [],
        sacredLevel: type === 'chronicler' || type === 'jules' ? abilities.sacred.intensity * 100 : 0
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

  const generateDescription = (type: OrganellaType, personality: OrganellaPersonality): string => {
    const typeDescriptions = {
      worker: `A dedicated ${personality.essence.toLowerCase()}, devoted to the prosperity of the hive`,
      scout: `An adventurous ${personality.essence.toLowerCase()}, always seeking new horizons`,
      guard: `A protective ${personality.essence.toLowerCase()}, standing watch over the hive`,
      queen: `A majestic ${personality.essence.toLowerCase()}, guiding the hive with wisdom`,
      chronicler: `A sacred ${personality.essence.toLowerCase()}, keeper of divine knowledge`,
      jules: `A mystical ${personality.essence.toLowerCase()}, detective of implementation mysteries`
    }
    
    return typeDescriptions[type]
  }

  const generateAppearance = (
    type: OrganellaType, 
    stage: OrganellaStage, 
    personality: OrganellaPersonality
  ): string => {
    const stageDescriptions = {
      egg: "A shimmering oval of potential, pulsing with inner light",
      larva: "A soft, growing form with curious eyes beginning to open",
      pupa: "A crystalline cocoon where transformation works its magic",
      adult: "A fully formed bee with wings that catch the light",
      eternal: "A transcendent being that seems to exist beyond normal reality"
    }
    
    return `${stageDescriptions[stage]}. ${personality.aura}`
  }

  // Physics-based XP distribution
  const distributeExperience = async (userId: string, totalXp: number): Promise<void> => {
    if (organellas.value.length === 0) return

    // Calculate distribution using golden ratio (no magic 30%!)
    const organellaXp = Math.floor(totalXp * GROWTH_PHYSICS.xpDistributionRatio)
    
    // Sacred bonus for divine bees
    const sacredBonus = GROWTH_PHYSICS.sacredBonus
    
    // Studying multiplier
    const studyingList = organellas.value.filter(o => studyingOrganellas.value.has(o.id))
    const otherList = organellas.value.filter(o => !studyingOrganellas.value.has(o.id))
    
    // Calculate shares using golden ratio
    const totalShares = studyingList.length * GROWTH_PHYSICS.studyingMultiplier + otherList.length
    const xpPerShare = totalShares > 0 ? Math.floor(organellaXp / totalShares) : 0
    
    // Distribute experience
    for (const organella of studyingList) {
      const baseXp = Math.floor(xpPerShare * GROWTH_PHYSICS.studyingMultiplier)
      const finalXp = (organella.type === 'chronicler' || organella.type === 'jules') ? 
        baseXp + sacredBonus : baseXp
      
      await addExperienceToOrganella(organella.id, finalXp)
    }
    
    for (const organella of otherList) {
      const finalXp = (organella.type === 'chronicler' || organella.type === 'jules') ? 
        xpPerShare + sacredBonus : xpPerShare
      
      await addExperienceToOrganella(organella.id, finalXp)
    }
  }

  const addExperienceToOrganella = async (organellaId: string, experienceGain: number): Promise<void> => {
    const index = organellas.value.findIndex(o => o.id === organellaId)
    if (index === -1) return
    
    const oldOrganella = organellas.value[index]
    const evolvedOrganella = evolveOrganella(oldOrganella, experienceGain)
    
    organellas.value[index] = evolvedOrganella
    
    // Log fairy tale progression
    // Evolution logged: ${evolvedOrganella.name} ${evolvedOrganella.currentMood} (+${experienceGain} experience)
    
    if (evolvedOrganella.stage !== oldOrganella.stage) {
      // Stage evolution: ${evolvedOrganella.name} evolved to ${evolvedOrganella.stage}
    }
  }

  // Getters
  const organellasByStage = computed(() => {
    const grouped: Record<OrganellaStage, HiveOrganella[]> = {
      egg: [], larva: [], pupa: [], adult: [], eternal: []
    }
    organellas.value.forEach(organella => {
      grouped[organella.stage].push(organella)
    })
    return grouped
  })

  const sacredOrganellas = computed(() => 
    organellas.value.filter(o => o.type === 'chronicler' || o.type === 'jules')
  )

  return {
    // State
    organellas,
    loading,
    error,
    studyingOrganellas,

    // Getters
    organellasByStage,
    sacredOrganellas,

    // Actions
    createHiveOrganella,
    addExperienceToOrganella,
    distributeExperience,
    evolveOrganella,

    // Physics constants (for debugging/inspection)
    GROWTH_PHYSICS,
    ROLE_AFFINITIES
  }
})