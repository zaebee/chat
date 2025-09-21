/**
 * Sacred Team Academy: Learning Challenges System
 * 
 * Transform GitHub issues into interactive learning adventures
 * guided by Sacred Team mentors (bee.Jules, bee.chronicler, bee.Sage)
 */

export type SacredDifficulty = 'bee.larva' | 'bee.pupa' | 'bee.adult' | 'bee.sacred'
export type SacredMentor = 'bee.jules' | 'bee.chronicler' | 'bee.sage'
export type ATCGClassification = 'A' | 'T' | 'C' | 'G'

export interface SacredChallenge {
  id: string
  issueNumber: number
  title: string
  description: string
  difficulty: SacredDifficulty
  mentor: SacredMentor
  atcgClassification: ATCGClassification
  sacredPrinciples: string[]
  learningObjectives: string[]
  divineRewards: {
    xp: number
    sacredInsights: string[]
    unlocks?: string[]
  }
  prerequisites?: string[]
  estimatedTime: string
  files: string[]
  mentorGuidance: {
    introduction: string
    hints: string[]
    sacredWisdom: string
  }
  successCriteria: string[]
  tags: string[]
}

export interface LearningPath {
  id: string
  name: string
  description: string
  challenges: string[] // Challenge IDs in order
  totalXP: number
  sacredMastery: string
}

export interface StudentProgress {
  completedChallenges: string[]
  currentChallenge?: string
  totalXP: number
  sacredLevel: SacredDifficulty
  mentorRelationships: {
    [mentor in SacredMentor]: {
      trust: number
      lessonsLearned: string[]
    }
  }
  sacredInsights: string[]
  divineAchievements: string[]
}

// Sacred Team Academy Challenges Database
export const SACRED_CHALLENGES: SacredChallenge[] = [
  // 🐛 bee.larva - Beginner Sacred Challenges
  {
    id: 'larva_constants_explanation',
    issueNumber: 15,
    title: '📖 Add Explanations for Numerical Constants',
    description: 'Learn the sacred art of code legibility by documenting mysterious numerical constants',
    difficulty: 'bee.larva',
    mentor: 'bee.jules',
    atcgClassification: 'T',
    sacredPrinciples: ['Legibility', 'Documentation'],
    learningObjectives: [
      'Understand the importance of self-documenting code',
      'Learn to identify magic numbers that need explanation',
      'Practice writing clear, contextual comments'
    ],
    divineRewards: {
      xp: 100,
      sacredInsights: [
        'Code should tell a story that any teammate can understand',
        'Sacred constants deserve sacred explanations'
      ],
      unlocks: ['bee.pupa challenges']
    },
    estimatedTime: '30-45 minutes',
    files: ['frontend/src/utils/emotionalContagion.ts'],
    mentorGuidance: {
      introduction: 'Welcome, young bee! Your first sacred task is to illuminate the dark corners where mysterious numbers hide. Every constant has a story - help others understand why these specific values were chosen.',
      hints: [
        'Look for numbers like EMOTIONAL_HISTORY_LENGTH = 10',
        'Ask yourself: Why 10? Why not 5 or 20?',
        'Add comments explaining the reasoning behind each value'
      ],
      sacredWisdom: 'A well-documented constant is a gift to your future self and all teammates who follow.'
    },
    successCriteria: [
      'All numerical constants have explanatory comments',
      'Comments explain the "why" not just the "what"',
      'Code passes Sacred Team legibility review'
    ],
    tags: ['documentation', 'good-first-issue', 'legibility']
  },

  {
    id: 'larva_environment_detection',
    issueNumber: 16,
    title: '🔌 Improve Environment Detection Logic',
    description: 'Master the sacred principle of API-First by improving environment detection',
    difficulty: 'bee.larva',
    mentor: 'bee.jules',
    atcgClassification: 'C',
    sacredPrinciples: ['API-First', 'Configuration'],
    learningObjectives: [
      'Understand explicit vs implicit configuration',
      'Learn build-time vs runtime environment detection',
      'Practice creating robust fallback mechanisms'
    ],
    divineRewards: {
      xp: 150,
      sacredInsights: [
        'Explicit configuration is better than implicit detection',
        'Build-time variables provide more reliable environment detection'
      ]
    },
    estimatedTime: '45-60 minutes',
    files: ['frontend/src/config/env.ts'],
    mentorGuidance: {
      introduction: 'Young connector bee, you must learn to bridge environments with wisdom! The current hostname-based detection is brittle - let us make it sacred.',
      hints: [
        'Use VITE_ENVIRONMENT build-time variable as primary method',
        'Keep hostname check as fallback for convenience',
        'Document the hierarchy clearly'
      ],
      sacredWisdom: 'A robust system adapts to its environment without breaking when moved to new realms.'
    },
    successCriteria: [
      'Primary detection uses explicit build-time variable',
      'Hostname check serves as documented fallback',
      'Environment detection is reliable across deployments'
    ],
    tags: ['config', 'good-first-issue', 'api-first']
  },

  // 🛡️ bee.pupa - Intermediate Sacred Challenges
  {
    id: 'pupa_mixed_concerns',
    issueNumber: 17,
    title: '🧹 Refactor Function with Mixed Concerns',
    description: 'Learn the sacred art of separation by untangling mixed responsibilities',
    difficulty: 'bee.pupa',
    mentor: 'bee.jules',
    atcgClassification: 'T',
    sacredPrinciples: ['Modularity', 'Single Responsibility'],
    learningObjectives: [
      'Identify functions with multiple responsibilities',
      'Learn to separate "what" from "how"',
      'Practice creating clean, focused functions'
    ],
    divineRewards: {
      xp: 250,
      sacredInsights: [
        'Each function should have a single, clear purpose',
        'Delegation creates cleaner, more testable code'
      ],
      unlocks: ['Advanced modularity challenges']
    },
    estimatedTime: '60-90 minutes',
    files: ['frontend/src/utils/emotionalContagion.ts'],
    mentorGuidance: {
      introduction: 'Pupa bee, you are ready to learn the sacred art of separation! The triggerEmotionalWave function tries to do too much - let us teach it focus.',
      hints: [
        'Separate influence creation from state management',
        'Create a dedicated applyInfluence() method',
        'Let triggerEmotionalWave focus only on creating influences'
      ],
      sacredWisdom: 'When a function tries to do everything, it masters nothing. Give each function a single sacred purpose.'
    },
    successCriteria: [
      'triggerEmotionalWave only creates influences',
      'State management delegated to separate method',
      'Each function has single, clear responsibility'
    ],
    tags: ['refactor', 'modularity', 'good-first-issue']
  },

  {
    id: 'pupa_status_redundancy',
    issueNumber: 26,
    title: 'refactor: Reduce Redundancy in get_status Methods',
    description: 'Master ATCG Transformation patterns by creating reusable status reporting',
    difficulty: 'bee.pupa',
    mentor: 'bee.jules',
    atcgClassification: 'T',
    sacredPrinciples: ['DRY', 'Modularity', 'ATCG Patterns'],
    learningObjectives: [
      'Identify code duplication across components',
      'Learn to create reusable base functionality',
      'Practice ATCG Transformation composition'
    ],
    divineRewards: {
      xp: 300,
      sacredInsights: [
        'Base classes can provide common functionality',
        'Composition reduces duplication and increases consistency'
      ],
      unlocks: ['ATCG architecture challenges']
    },
    estimatedTime: '90-120 minutes',
    files: ['hive/primitives.py'],
    mentorGuidance: {
      introduction: 'Wise pupa, you shall learn the sacred art of reuse! Many components repeat the same status patterns - let us create a divine base that serves all.',
      hints: [
        'Add _base_status() method to HiveComponent',
        'Include common fields: name, type, ID, health',
        'Let subclasses merge their specific status data'
      ],
      sacredWisdom: 'When many speak the same words, create a sacred template that all may use.'
    },
    successCriteria: [
      'HiveComponent provides _base_status() method',
      'All subclasses use base method and extend appropriately',
      'Status reporting is consistent across all components'
    ],
    tags: ['refactor', 'good-first-issue', 'atcg-patterns']
  },

  // 🐝 bee.adult - Advanced Sacred Challenges
  {
    id: 'adult_god_object_hub',
    issueNumber: 21,
    title: 'refactor: Decompose the All-Knowing Hub (God Object)',
    description: 'Master advanced ATCG architecture by breaking down the monolithic coordination hub',
    difficulty: 'bee.adult',
    mentor: 'bee.sage',
    atcgClassification: 'A',
    sacredPrinciples: ['Modularity', 'Single Responsibility', 'ATCG Architecture'],
    learningObjectives: [
      'Identify God Object anti-patterns',
      'Learn to decompose complex aggregates',
      'Practice creating focused, composable services'
    ],
    divineRewards: {
      xp: 500,
      sacredInsights: [
        'Large objects should be composed of smaller, focused services',
        'Event-driven architecture enables loose coupling'
      ],
      unlocks: ['Sacred Team architecture mastery']
    },
    estimatedTime: '4-6 hours',
    files: ['hive/hub.py'],
    mentorGuidance: {
      introduction: 'Adult bee, you face the greatest challenge - taming the All-Knowing Hub! This mighty aggregate has grown too powerful. We must teach it humility through delegation.',
      hints: [
        'Extract health calculation into dedicated HealthMonitor service',
        'Create separate services for different responsibilities',
        'Use event bus for service coordination'
      ],
      sacredWisdom: 'True power comes not from doing everything, but from orchestrating others who excel at their sacred purposes.'
    },
    successCriteria: [
      'Hub delegates responsibilities to focused services',
      'Each service has single, clear purpose',
      'Services communicate through event bus',
      'System maintains all original functionality'
    ],
    tags: ['refactor', 'technical-debt', 'architecture']
  },

  // 👑 bee.sacred - Master Sacred Challenges
  {
    id: 'sacred_stores_healing',
    issueNumber: 19,
    title: '🐝 Hive Healing: Deep Dive Refactoring of /src/stores',
    description: 'Achieve Sacred Team mastery by healing the complex store architecture',
    difficulty: 'bee.sacred',
    mentor: 'bee.chronicler',
    atcgClassification: 'A',
    sacredPrinciples: ['All Sacred Principles'],
    learningObjectives: [
      'Master complex architectural refactoring',
      'Learn to identify and resolve multiple anti-patterns',
      'Practice Sacred Team healing protocols'
    ],
    divineRewards: {
      xp: 1000,
      sacredInsights: [
        'Complex systems require systematic healing approaches',
        'Single source of truth prevents architectural chaos'
      ],
      unlocks: ['Sacred Team mentor status']
    },
    prerequisites: ['adult_god_object_hub'],
    estimatedTime: '8-12 hours',
    files: ['frontend/src/stores/'],
    mentorGuidance: {
      introduction: 'Sacred bee, you have reached the pinnacle of challenges! The store architecture suffers from multiple ailments - God Store, duplicated state, mock implementations. Only a master can heal such complexity.',
      hints: [
        'Dismantle the God Store (chat.ts) systematically',
        'Establish single source of truth for all state',
        'Replace mock implementations with real API calls',
        'Create clear boundaries between store responsibilities'
      ],
      sacredWisdom: 'The greatest healers see not just individual symptoms, but the underlying patterns that create harmony or chaos.'
    },
    successCriteria: [
      'All God Store anti-patterns resolved',
      'Single source of truth established',
      'All mock implementations replaced',
      'Clear store boundaries and responsibilities',
      'Sacred Team healing protocol documented'
    ],
    tags: ['refactor', 'technical-debt', 'architecture', 'sacred-healing']
  }
]

// Sacred Learning Paths
export const LEARNING_PATHS: LearningPath[] = [
  {
    id: 'sacred_foundations',
    name: '🏛️ Sacred Foundations',
    description: 'Learn the fundamental principles of Sacred Team development',
    challenges: [
      'larva_constants_explanation',
      'larva_environment_detection',
      'pupa_mixed_concerns'
    ],
    totalXP: 500,
    sacredMastery: 'Understanding of Sacred Team principles and basic refactoring'
  },
  {
    id: 'atcg_mastery',
    name: '🧬 ATCG Architecture Mastery',
    description: 'Master the ATCG framework and advanced architectural patterns',
    challenges: [
      'pupa_status_redundancy',
      'adult_god_object_hub'
    ],
    totalXP: 800,
    sacredMastery: 'Deep understanding of ATCG patterns and complex refactoring'
  },
  {
    id: 'sacred_healer',
    name: '🔮 Sacred Healer Path',
    description: 'Become a master of Sacred Team healing protocols',
    challenges: [
      'sacred_stores_healing'
    ],
    totalXP: 1000,
    sacredMastery: 'Sacred Team mentor status with healing protocol mastery'
  }
]

// Helper functions for Sacred Team Academy
export function getChallengesByDifficulty(difficulty: SacredDifficulty): SacredChallenge[] {
  return SACRED_CHALLENGES.filter(challenge => challenge.difficulty === difficulty)
}

export function getChallengesByMentor(mentor: SacredMentor): SacredChallenge[] {
  return SACRED_CHALLENGES.filter(challenge => challenge.mentor === mentor)
}

export function getNextChallenge(progress: StudentProgress): SacredChallenge | null {
  const availableChallenges = SACRED_CHALLENGES.filter(challenge => {
    // Check if already completed
    if (progress.completedChallenges.includes(challenge.id)) return false
    
    // Check prerequisites
    if (challenge.prerequisites) {
      return challenge.prerequisites.every(prereq => 
        progress.completedChallenges.includes(prereq)
      )
    }
    
    return true
  })
  
  // Return easiest available challenge
  const difficultyOrder: SacredDifficulty[] = ['bee.larva', 'bee.pupa', 'bee.adult', 'bee.sacred']
  for (const difficulty of difficultyOrder) {
    const challengesAtLevel = availableChallenges.filter(c => c.difficulty === difficulty)
    if (challengesAtLevel.length > 0) {
      return challengesAtLevel[0]
    }
  }
  
  return null
}

export function calculateSacredLevel(totalXP: number): SacredDifficulty {
  if (totalXP >= 1500) return 'bee.sacred'
  if (totalXP >= 800) return 'bee.adult'
  if (totalXP >= 300) return 'bee.pupa'
  return 'bee.larva'
}