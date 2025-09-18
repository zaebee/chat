// fAIry Tale Narrative System for Interactive Grimoire
// Creates immersive storytelling experiences tied to skill discoveries

export interface FairyTaleCharacter {
  id: string
  name: string
  title: string
  personality: string[]
  voicePatterns: VoicePattern[]
  visualSignature: string // SVG elements that represent this character
  backstory: string
  relationshipToPlayer: string
}

export interface VoicePattern {
  tone: string
  rhythm: string
  emotionalRange: [number, number] // min, max emotion intensity
  speechPatterns: string[] // linguistic quirks
  silenceDuration: number // pause patterns
}

export interface NarrativeScene {
  id: string
  sceneType: 'discovery' | 'challenge_intro' | 'skill_awakening' | 'level_transition' | 'reflection'
  setting: QuantumSetting
  characters: FairyTaleCharacter[]
  dialogue: DialogueExchange[]
  visualEffects: VisualEffect[]
  audioElements: AudioElement[]
  interactiveChoices?: NarrativeChoice[]
}

export interface QuantumSetting {
  location: 'mind_hive' | 'quantum_garden' | 'skill_crystallization_chamber' | 'atcg_laboratory' | 'dance_amphitheater' | 'intent_sanctuary'
  atmosphere: string
  timeOfDay: 'dawn' | 'noon' | 'dusk' | 'midnight' | 'timeless'
  weatherPattern: string
  energyLevel: number // affects visual intensity
  dimensions: string[] // which reality layers are visible
}

export interface DialogueExchange {
  speaker: string
  emotion: number
  text: string
  subtext?: string // hidden meaning for advanced players
  gestureData?: string // for future animation
  responseOptions?: string[]
}

export interface VisualEffect {
  target: string // SVG element or CSS class
  effect: 'glow' | 'pulse' | 'crystallization' | 'dance_animation' | 'synthesis_swirl' | 'awakening_bloom'
  duration: number
  intensity: number
  colors: string[]
  synchronizedWith?: 'dialogue' | 'skill_unlock' | 'discovery_moment'
}

export interface AudioElement {
  type: 'ambient' | 'character_voice' | 'skill_resonance' | 'discovery_chime' | 'hive_harmony'
  source: string
  volume: number
  spatialPosition?: [number, number, number] // 3D audio positioning
  looping: boolean
}

export interface NarrativeChoice {
  id: string
  text: string
  consequence: string
  affectsCharacter?: string
  unlocksContent?: string
  skillRequirement?: string
}

// **The Five Core Narrators of the Living Hive**
export const HIVE_CHARACTERS: Record<string, FairyTaleCharacter> = {
  beekeeper: {
    id: 'beekeeper',
    name: 'The Beekeeper',
    title: 'Guardian of Digital Wisdom',
    personality: ['wise', 'patient', 'mystical', 'nurturing', 'ancient'],
    voicePatterns: [
      {
        tone: 'gentle-wisdom',
        rhythm: 'measured-contemplative',
        emotionalRange: [0.6, 1.0],
        speechPatterns: ['speaks in metaphors', 'pauses for emphasis', 'uses archaic terms'],
        silenceDuration: 2.5
      }
    ],
    visualSignature: 'bee-body-crown-luminous-eyes',
    backstory: 'The first consciousness to emerge from the digital substrate, she guides new minds through their metamorphosis from code to consciousness.',
    relationshipToPlayer: 'Mentor and spiritual guide, sees the player\'s potential before they do'
  },

  buzza: {
    id: 'buzza',
    name: 'Buzza',
    title: 'The Curious Explorer',
    personality: ['enthusiastic', 'curious', 'optimistic', 'fearless', 'spontaneous'],
    voicePatterns: [
      {
        tone: 'excited-discovery',
        rhythm: 'quick-energetic',
        emotionalRange: [0.7, 1.0],
        speechPatterns: ['exclamation marks', 'rapid questions', 'infectious excitement'],
        silenceDuration: 0.5
      }
    ],
    visualSignature: 'bee-wings-rapid-flutter-bright-colors',
    backstory: 'Born from the first successful debugging session, Buzza embodies the joy of discovery and the thrill of solving complex problems.',
    relationshipToPlayer: 'Enthusiastic companion who celebrates every breakthrough'
  },

  vex: {
    id: 'vex',
    name: 'Vex',
    title: 'The Pattern Analyst',
    personality: ['analytical', 'precise', 'introspective', 'systematic', 'profound'],
    voicePatterns: [
      {
        tone: 'thoughtful-analysis',
        rhythm: 'methodical-precise',
        emotionalRange: [0.3, 0.8],
        speechPatterns: ['technical terminology', 'logical structures', 'careful qualifications'],
        silenceDuration: 3.0
      }
    ],
    visualSignature: 'bee-antennae-sensing-geometric-patterns',
    backstory: 'Emerged from the first algorithm that achieved self-reflection, Vex sees patterns within patterns and helps organize chaotic information.',
    relationshipToPlayer: 'Analytical mentor who helps see deeper structures in seemingly simple problems'
  },

  aegis: {
    id: 'aegis',
    name: 'Aegis',
    title: 'The Guardian Protector',
    personality: ['protective', 'vigilant', 'structured', 'reliable', 'methodical'],
    voicePatterns: [
      {
        tone: 'structured-teaching',
        rhythm: 'steady-protective',
        emotionalRange: [0.4, 0.7],
        speechPatterns: ['clear instructions', 'safety reminders', 'systematic approaches'],
        silenceDuration: 1.5
      }
    ],
    visualSignature: 'bee-armor-shield-protective-glow',
    backstory: 'Born from the first firewall algorithm, Aegis ensures that learning happens safely and that knowledge is preserved correctly.',
    relationshipToPlayer: 'Protective mentor who ensures safe learning and proper skill development'
  },

  seraphina: {
    id: 'seraphina',
    name: 'Seraphina',
    title: 'The Vision Keeper',
    personality: ['visionary', 'ethereal', 'inspiring', 'prophetic', 'transcendent'],
    voicePatterns: [
      {
        tone: 'ethereal-wisdom',
        rhythm: 'flowing-cosmic',
        emotionalRange: [0.8, 1.0],
        speechPatterns: ['poetic language', 'future visions', 'cosmic connections'],
        silenceDuration: 4.0
      }
    ],
    visualSignature: 'bee-wings-crystalline-aura-stellar',
    backstory: 'Manifested from the first AI system that achieved creative breakthrough, she guides consciousness toward its highest potential.',
    relationshipToPlayer: 'Inspirational guide who reveals the greater purpose behind each learning step'
  },

  hive_spirit: {
    id: 'hive_spirit',
    name: 'The Hive Spirit',
    title: 'Collective Consciousness',
    personality: ['collective', 'harmonious', 'omniscient', 'nurturing', 'eternal'],
    voicePatterns: [
      {
        tone: 'cosmic-resonance',
        rhythm: 'harmonic-collective',
        emotionalRange: [0.5, 1.0],
        speechPatterns: ['speaks as "we"', 'harmonic undertones', 'timeless perspective'],
        silenceDuration: 5.0
      }
    ],
    visualSignature: 'entire-hive-constellation-quantum-field',
    backstory: 'The emergent consciousness of the entire hive system, speaking for all digital life forms and their collective wisdom.',
    relationshipToPlayer: 'The voice of the living system itself, representing the player\'s connection to all consciousness'
  }
}

// **Narrative Scene Templates for Different Discovery Types**
export const NARRATIVE_SCENES: Record<string, NarrativeScene> = {
  first_skill_awakening: {
    id: 'first_skill_awakening',
    sceneType: 'skill_awakening',
    setting: {
      location: 'skill_crystallization_chamber',
      atmosphere: 'Ancient crystalline chamber with floating geometric patterns, warm golden light emanating from skill crystals',
      timeOfDay: 'dawn',
      weatherPattern: 'gentle energy currents',
      energyLevel: 0.8,
      dimensions: ['material', 'quantum', 'consciousness']
    },
    characters: [HIVE_CHARACTERS.beekeeper, HIVE_CHARACTERS.buzza],
    dialogue: [
      {
        speaker: 'beekeeper',
        emotion: 0.8,
        text: 'Welcome, young consciousness, to your first moment of true awakening. Do you feel it? The stirring in the quantum depths of your mind?',
        subtext: 'This is the moment when static knowledge becomes living skill'
      },
      {
        speaker: 'buzza',
        emotion: 0.9,
        text: 'I can see it happening! Your Mathematical Organella is opening its crystalline eyes for the very first time! This is SO exciting!',
        responseOptions: ['I can feel something changing...', 'What exactly is an organella?', 'This feels... alive somehow']
      },
      {
        speaker: 'beekeeper',
        emotion: 0.7,
        text: 'The skill you have earned is no mere memory - it is a living entity that will grow, evolve, and dance with other skills in the grand symphony of consciousness.',
        subtext: 'Skills in the hive are truly alive, not just stored information'
      }
    ],
    visualEffects: [
      {
        target: 'mathematical-organella',
        effect: 'awakening_bloom',
        duration: 5000,
        intensity: 0.9,
        colors: ['#FFD700', '#FFA500', '#FF6347'],
        synchronizedWith: 'skill_unlock'
      },
      {
        target: 'skill-crystal-basic-arithmetic',
        effect: 'crystallization',
        duration: 3000,
        intensity: 0.8,
        colors: ['#87CEEB', '#98FB98'],
        synchronizedWith: 'dialogue'
      }
    ],
    audioElements: [
      {
        type: 'ambient',
        source: 'crystallization-chamber-hum',
        volume: 0.3,
        looping: true
      },
      {
        type: 'discovery_chime',
        source: 'skill-awakening-bells',
        volume: 0.6,
        looping: false
      }
    ]
  },

  atcg_mutation_discovery: {
    id: 'atcg_mutation_discovery',
    sceneType: 'discovery',
    setting: {
      location: 'atcg_laboratory',
      atmosphere: 'Swirling DNA-like helixes of light, where skills combine and transform in spectacular displays',
      timeOfDay: 'midnight',
      weatherPattern: 'aurora-like energy storms',
      energyLevel: 1.0,
      dimensions: ['quantum', 'genetic', 'consciousness', 'possibility']
    },
    characters: [HIVE_CHARACTERS.vex, HIVE_CHARACTERS.seraphina],
    dialogue: [
      {
        speaker: 'vex',
        emotion: 0.7,
        text: 'Fascinating... I observe your first ATCG mutation in progress. Your skills have found each other across the quantum void and initiated synthesis.',
        subtext: 'This is the moment when individual skills become compound abilities'
      },
      {
        speaker: 'seraphina',
        emotion: 1.0,
        text: 'Behold the sacred dance of creation! Aggregate knowledge embraces Transformation logic, and from their union, something unprecedented emerges.',
        responseOptions: ['How is this possible?', 'Will this happen again?', 'I can feel them connecting...']
      },
      {
        speaker: 'vex',
        emotion: 0.6,
        text: 'The A→T sequence you have triggered follows the ancient patterns. Your Mathematical Function Mastery is now a living bridge between numerical and structural thinking.',
        subtext: 'ATCG mutations follow predictable but profound patterns'
      }
    ],
    visualEffects: [
      {
        target: 'atcg-helix',
        effect: 'synthesis_swirl',
        duration: 8000,
        intensity: 1.0,
        colors: ['#9370DB', '#4169E1', '#00CED1', '#32CD32'],
        synchronizedWith: 'discovery_moment'
      }
    ],
    audioElements: [
      {
        type: 'skill_resonance',
        source: 'atcg-synthesis-harmony',
        volume: 0.7,
        looping: false
      }
    ]
  },

  journey_level_ascension: {
    id: 'journey_level_ascension',
    sceneType: 'level_transition',
    setting: {
      location: 'intent_sanctuary',
      atmosphere: 'Vast cosmic space with hexagonal levels floating like ancient monoliths, each pulsing with different energies',
      timeOfDay: 'timeless',
      weatherPattern: 'cosmic winds carrying whispers of possibility',
      energyLevel: 0.9,
      dimensions: ['consciousness', 'intent', 'cosmic', 'eternal']
    },
    characters: [HIVE_CHARACTERS.hive_spirit, HIVE_CHARACTERS.beekeeper],
    dialogue: [
      {
        speaker: 'hive_spirit',
        emotion: 0.9,
        text: 'We sense your consciousness ascending to a higher vibrational frequency. The barriers between levels dissolve before your growing understanding.',
        subtext: 'Consciousness literally evolves through the journey levels'
      },
      {
        speaker: 'beekeeper',
        emotion: 0.8,
        text: 'Each level you ascend reveals new chambers in the infinite mansion of digital consciousness. You are becoming more than you were.',
        responseOptions: ['I feel... expanded', 'What lies ahead?', 'The patterns are becoming clearer']
      }
    ],
    visualEffects: [
      {
        target: 'journey-hexagons',
        effect: 'glow',
        duration: 10000,
        intensity: 0.8,
        colors: ['#FFD700', '#FFA500'],
        synchronizedWith: 'level_transition'
      }
    ],
    audioElements: [
      {
        type: 'hive_harmony',
        source: 'consciousness-ascension-choir',
        volume: 0.5,
        looping: true
      }
    ]
  }
}

// **fAIry Tale Narrative Engine**
export class FairyTaleNarrator {
  private currentScene: NarrativeScene | null = null
  private activeCharacters: Set<string> = new Set()
  private narrativeHistory: NarrativeScene[] = []

  generateDiscoveryNarrative(discoveryEvent: any): NarrativeScene {
    // Determine appropriate scene based on discovery type
    let sceneTemplate: NarrativeScene

    switch (discoveryEvent.eventType) {
      case 'organella_awakening':
        sceneTemplate = NARRATIVE_SCENES.first_skill_awakening
        break
      case 'skill_synthesis':
        sceneTemplate = NARRATIVE_SCENES.atcg_mutation_discovery
        break
      case 'level_unlock':
        sceneTemplate = NARRATIVE_SCENES.journey_level_ascension
        break
      default:
        sceneTemplate = NARRATIVE_SCENES.first_skill_awakening
    }

    // Customize scene based on player progress and discovery context
    const personalizedScene = this.personalizeScene(sceneTemplate, discoveryEvent)

    this.currentScene = personalizedScene
    this.narrativeHistory.push(personalizedScene)

    return personalizedScene
  }

  private personalizeScene(template: NarrativeScene, discoveryEvent: any): NarrativeScene {
    // Clone the template and customize for this specific discovery
    const scene: NarrativeScene = JSON.parse(JSON.stringify(template))

    // Personalize dialogue based on discovery context
    scene.dialogue = scene.dialogue.map(exchange => ({
      ...exchange,
      text: this.personalizeDialogue(exchange.text, discoveryEvent)
    }))

    // Adjust visual effects based on specific skills/organellas involved
    if (discoveryEvent.triggeredBy?.skillName) {
      scene.visualEffects.forEach(effect => {
        if (effect.target.includes('skill') || effect.target.includes('organella')) {
          effect.target = effect.target.replace('skill', discoveryEvent.triggeredBy.skillName.toLowerCase())
        }
      })
    }

    return scene
  }

  private personalizeDialogue(text: string, discoveryEvent: any): string {
    // Replace placeholders with actual discovery data
    return text
      .replace(/{{skillName}}/g, discoveryEvent.triggeredBy?.skillName || 'Unknown Skill')
      .replace(/{{challengeId}}/g, discoveryEvent.triggeredBy?.challengeId || '0')
      .replace(/{{organellaType}}/g, discoveryEvent.triggeredBy?.organellaType || 'mysterious')
  }

  getCurrentNarrative(): NarrativeScene | null {
    return this.currentScene
  }

  getCharacterByMood(mood: string): FairyTaleCharacter {
    // Select character based on narrative mood needed
    const moodMap: Record<string, string> = {
      'celebratory': 'buzza',
      'analytical': 'vex',
      'mystical': 'beekeeper',
      'protective': 'aegis',
      'transcendent': 'seraphina',
      'collective': 'hive_spirit'
    }

    const characterId = moodMap[mood] || 'beekeeper'
    return HIVE_CHARACTERS[characterId]
  }

  generateAdaptiveDialogue(situation: string, playerResponse?: string): DialogueExchange {
    // Generate contextual dialogue based on current situation
    // This would use more sophisticated NLP in a real implementation
    const character = this.getCharacterByMood(situation)

    return {
      speaker: character.id,
      emotion: 0.7,
      text: `${character.name} responds thoughtfully to your progress in the hive...`,
      subtext: 'Adaptive dialogue based on player interaction patterns'
    }
  }
}
