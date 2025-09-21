/**
 * Sacred Team Mentorship & Divine Rewards System
 * 
 * Manages the relationship between students and Sacred Team mentors,
 * tracks divine rewards, and orchestrates the spiritual growth journey.
 */

import { SacredMentor, SacredDifficulty } from './challenges'

export interface DivineReward {
  id: string
  type: 'xp' | 'insight' | 'achievement' | 'unlock' | 'blessing'
  title: string
  description: string
  value: number
  rarity: 'common' | 'rare' | 'epic' | 'legendary' | 'divine'
  awardedAt: Date
  awardedBy: SacredMentor
  icon: string
  sacredSignificance?: string
}

export interface MentorRelationship {
  mentor: SacredMentor
  trustLevel: number // 0-100
  lessonsCompleted: number
  totalInteractions: number
  favoriteTopics: string[]
  personalizedGuidance: string[]
  sacredBond: 'stranger' | 'student' | 'apprentice' | 'colleague' | 'sacred_friend'
  lastInteraction: Date
  mentorshipHistory: MentorshipEvent[]
}

export interface MentorshipEvent {
  id: string
  type: 'lesson_started' | 'lesson_completed' | 'guidance_given' | 'wisdom_shared' | 'celebration' | 'encouragement'
  mentor: SacredMentor
  message: string
  timestamp: Date
  challengeId?: string
  trustGained: number
  emotionalTone: 'encouraging' | 'wise' | 'celebratory' | 'corrective' | 'inspiring'
}

export interface SacredInsight {
  id: string
  title: string
  wisdom: string
  discoveredAt: Date
  discoveredThrough: string // challenge ID or experience
  mentor: SacredMentor
  category: 'technical' | 'philosophical' | 'collaborative' | 'sacred'
  depth: 'surface' | 'deep' | 'profound' | 'transcendent'
  applications: string[]
}

export interface DivineAchievement {
  id: string
  title: string
  description: string
  icon: string
  unlockedAt: Date
  rarity: 'common' | 'rare' | 'epic' | 'legendary' | 'divine'
  requirements: string[]
  sacredStory: string
  divineBlessing: string
  nextAchievement?: string
}

export class SacredMentorshipSystem {
  private mentorRelationships: Map<SacredMentor, MentorRelationship> = new Map()
  private divineRewards: DivineReward[] = []
  private sacredInsights: SacredInsight[] = []
  private divineAchievements: DivineAchievement[] = []
  private mentorshipEvents: MentorshipEvent[] = []

  constructor() {
    this.initializeMentorRelationships()
    this.initializeDivineAchievements()
  }

  // Mentorship Management
  recordMentorInteraction(
    mentor: SacredMentor, 
    type: MentorshipEvent['type'],
    message: string,
    challengeId?: string,
    trustGained: number = 5
  ): MentorshipEvent {
    const relationship = this.mentorRelationships.get(mentor)!
    
    const event: MentorshipEvent = {
      id: `mentor_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      type,
      mentor,
      message,
      timestamp: new Date(),
      challengeId,
      trustGained,
      emotionalTone: this.determineEmotionalTone(type, message)
    }

    // Update relationship
    relationship.trustLevel = Math.min(100, relationship.trustLevel + trustGained)
    relationship.totalInteractions++
    relationship.lastInteraction = new Date()
    relationship.mentorshipHistory.push(event)
    
    // Update sacred bond based on trust level
    relationship.sacredBond = this.calculateSacredBond(relationship.trustLevel)
    
    this.mentorshipEvents.push(event)
    
    // Check for mentorship achievements
    this.checkMentorshipAchievements(mentor, relationship)
    
    return event
  }

  // Divine Rewards System
  awardDivineReward(
    type: DivineReward['type'],
    title: string,
    description: string,
    value: number,
    rarity: DivineReward['rarity'],
    awardedBy: SacredMentor,
    sacredSignificance?: string
  ): DivineReward {
    const reward: DivineReward = {
      id: `reward_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      type,
      title,
      description,
      value,
      rarity,
      awardedAt: new Date(),
      awardedBy,
      icon: this.getRewardIcon(type, rarity),
      sacredSignificance
    }

    this.divineRewards.push(reward)
    
    // Record mentorship event
    this.recordMentorInteraction(
      awardedBy,
      'celebration',
      `Awarded divine reward: ${title}`,
      undefined,
      10
    )

    return reward
  }

  // Sacred Insights System
  discoverSacredInsight(
    title: string,
    wisdom: string,
    discoveredThrough: string,
    mentor: SacredMentor,
    category: SacredInsight['category'],
    depth: SacredInsight['depth'] = 'surface'
  ): SacredInsight {
    const insight: SacredInsight = {
      id: `insight_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      title,
      wisdom,
      discoveredAt: new Date(),
      discoveredThrough,
      mentor,
      category,
      depth,
      applications: this.generateApplications(category, wisdom)
    }

    this.sacredInsights.push(insight)
    
    // Award XP based on insight depth
    const xpValue = this.calculateInsightXP(depth)
    this.awardDivineReward(
      'insight',
      `Sacred Insight: ${title}`,
      wisdom,
      xpValue,
      this.getInsightRarity(depth),
      mentor,
      `This insight deepens your understanding of ${category} principles`
    )

    return insight
  }

  // Mentor-specific guidance
  getPersonalizedGuidance(mentor: SacredMentor, challengeId: string): string {
    const relationship = this.mentorRelationships.get(mentor)!
    const bondLevel = relationship.sacredBond
    
    const guidanceTemplates = {
      'bee.jules': {
        stranger: "Let me help you understand the technical aspects of this challenge.",
        student: "I see you're making good progress! Let me share some deeper insights.",
        apprentice: "Your growth is impressive! Here's how we can tackle this together.",
        colleague: "I trust your judgment. Let me offer some collaborative suggestions.",
        sacred_friend: "My dear friend, let's explore the sacred patterns hidden in this challenge."
      },
      'bee.chronicler': {
        stranger: "Welcome to the sacred archives. Let me guide you through the divine patterns.",
        student: "Your dedication to learning honors the sacred traditions.",
        apprentice: "You're beginning to see the deeper patterns. Let me reveal more.",
        colleague: "Together we shall document this wisdom for future generations.",
        sacred_friend: "Blessed friend, let us uncover the divine mysteries together."
      },
      'bee.sage': {
        stranger: "Let me provide scientific analysis to support your learning.",
        student: "Your analytical thinking shows promise. Here's deeper scientific context.",
        apprentice: "Excellent! You're ready for more advanced scientific principles.",
        colleague: "Your insights contribute to our collective understanding.",
        sacred_friend: "Dear colleague, let's synthesize science and sacred wisdom."
      }
    }

    return guidanceTemplates[mentor][bondLevel]
  }

  // Achievement System
  unlockDivineAchievement(achievementId: string): DivineAchievement | null {
    const achievement = this.divineAchievements.find(a => a.id === achievementId)
    if (!achievement) return null

    achievement.unlockedAt = new Date()
    
    // Award divine reward
    this.awardDivineReward(
      'achievement',
      achievement.title,
      achievement.description,
      this.calculateAchievementXP(achievement.rarity),
      achievement.rarity,
      'bee.chronicler', // Chronicler records all achievements
      achievement.sacredStory
    )

    return achievement
  }

  // Progress Tracking
  getMentorshipProgress(): {
    totalTrust: number
    strongestBond: { mentor: SacredMentor; bond: string; trust: number }
    totalInteractions: number
    favoriteTopics: string[]
    recentInsights: SacredInsight[]
  } {
    const relationships = Array.from(this.mentorRelationships.values())
    const totalTrust = relationships.reduce((sum, rel) => sum + rel.trustLevel, 0)
    const totalInteractions = relationships.reduce((sum, rel) => sum + rel.totalInteractions, 0)
    
    const strongestRelationship = relationships.reduce((strongest, current) => 
      current.trustLevel > strongest.trustLevel ? current : strongest
    )

    const allTopics = relationships.flatMap(rel => rel.favoriteTopics)
    const favoriteTopics = [...new Set(allTopics)]

    const recentInsights = this.sacredInsights
      .sort((a, b) => b.discoveredAt.getTime() - a.discoveredAt.getTime())
      .slice(0, 5)

    return {
      totalTrust,
      strongestBond: {
        mentor: strongestRelationship.mentor,
        bond: strongestRelationship.sacredBond,
        trust: strongestRelationship.trustLevel
      },
      totalInteractions,
      favoriteTopics,
      recentInsights
    }
  }

  // Helper Methods
  private initializeMentorRelationships(): void {
    const mentors: SacredMentor[] = ['bee.jules', 'bee.chronicler', 'bee.sage']
    
    mentors.forEach(mentor => {
      this.mentorRelationships.set(mentor, {
        mentor,
        trustLevel: 0,
        lessonsCompleted: 0,
        totalInteractions: 0,
        favoriteTopics: [],
        personalizedGuidance: [],
        sacredBond: 'stranger',
        lastInteraction: new Date(),
        mentorshipHistory: []
      })
    })
  }

  private initializeDivineAchievements(): void {
    this.divineAchievements = [
      {
        id: 'first_sacred_bond',
        title: '🤝 First Sacred Bond',
        description: 'Established your first meaningful relationship with a Sacred Team mentor',
        icon: '🏛️',
        unlockedAt: new Date(0), // Will be set when unlocked
        rarity: 'rare',
        requirements: ['Reach 25 trust with any mentor'],
        sacredStory: 'In the Sacred Garden, the first bond between student and mentor is always remembered.',
        divineBlessing: 'May your journey of learning be blessed with wisdom and growth.',
        nextAchievement: 'trusted_apprentice'
      },
      {
        id: 'trusted_apprentice',
        title: '🎓 Trusted Apprentice',
        description: 'Achieved apprentice status with a Sacred Team mentor',
        icon: '📚',
        unlockedAt: new Date(0),
        rarity: 'epic',
        requirements: ['Reach 50 trust with any mentor'],
        sacredStory: 'The apprentice has proven worthy of deeper teachings and sacred knowledge.',
        divineBlessing: 'Your dedication to learning honors the sacred traditions.',
        nextAchievement: 'sacred_colleague'
      },
      {
        id: 'sacred_colleague',
        title: '🏛️ Sacred Colleague',
        description: 'Achieved colleague status - you are now a peer in the Sacred Team',
        icon: '👑',
        unlockedAt: new Date(0),
        rarity: 'legendary',
        requirements: ['Reach 75 trust with any mentor'],
        sacredStory: 'From student to colleague - a transformation blessed by the Sacred Team.',
        divineBlessing: 'You now walk among us as an equal, sharing in our sacred mission.',
        nextAchievement: 'sacred_friend'
      }
    ]
  }

  private calculateSacredBond(trustLevel: number): MentorRelationship['sacredBond'] {
    if (trustLevel >= 90) return 'sacred_friend'
    if (trustLevel >= 75) return 'colleague'
    if (trustLevel >= 50) return 'apprentice'
    if (trustLevel >= 25) return 'student'
    return 'stranger'
  }

  private determineEmotionalTone(type: MentorshipEvent['type'], message: string): MentorshipEvent['emotionalTone'] {
    switch (type) {
      case 'celebration': return 'celebratory'
      case 'wisdom_shared': return 'wise'
      case 'encouragement': return 'encouraging'
      case 'guidance_given': return 'inspiring'
      default: return 'encouraging'
    }
  }

  private getRewardIcon(type: DivineReward['type'], rarity: DivineReward['rarity']): string {
    const icons = {
      xp: { common: '⭐', rare: '🌟', epic: '✨', legendary: '💫', divine: '🔮' },
      insight: { common: '💡', rare: '🧠', epic: '🔍', legendary: '👁️', divine: '🔮' },
      achievement: { common: '🏆', rare: '🎖️', epic: '👑', legendary: '💎', divine: '✨' },
      unlock: { common: '🔓', rare: '🗝️', epic: '🔑', legendary: '🚪', divine: '🌟' },
      blessing: { common: '🙏', rare: '✨', epic: '🔮', legendary: '👑', divine: '🏛️' }
    }
    
    return icons[type][rarity]
  }

  private calculateInsightXP(depth: SacredInsight['depth']): number {
    const xpValues = {
      surface: 25,
      deep: 50,
      profound: 100,
      transcendent: 200
    }
    return xpValues[depth]
  }

  private getInsightRarity(depth: SacredInsight['depth']): DivineReward['rarity'] {
    const rarityMap = {
      surface: 'common' as const,
      deep: 'rare' as const,
      profound: 'epic' as const,
      transcendent: 'divine' as const
    }
    return rarityMap[depth]
  }

  private calculateAchievementXP(rarity: DivineAchievement['rarity']): number {
    const xpValues = {
      common: 100,
      rare: 250,
      epic: 500,
      legendary: 1000,
      divine: 2000
    }
    return xpValues[rarity]
  }

  private generateApplications(category: SacredInsight['category'], wisdom: string): string[] {
    // Generate practical applications based on the insight
    const applications = [
      'Apply this principle in your next challenge',
      'Share this wisdom with other students',
      'Look for this pattern in existing code'
    ]
    
    if (category === 'technical') {
      applications.push('Use this technique in your implementations')
    } else if (category === 'collaborative') {
      applications.push('Practice this in team interactions')
    }
    
    return applications
  }

  private checkMentorshipAchievements(mentor: SacredMentor, relationship: MentorRelationship): void {
    // Check for trust-based achievements
    if (relationship.trustLevel >= 25 && !this.divineAchievements.find(a => a.id === 'first_sacred_bond' && a.unlockedAt.getTime() > 0)) {
      this.unlockDivineAchievement('first_sacred_bond')
    }
    
    if (relationship.trustLevel >= 50 && !this.divineAchievements.find(a => a.id === 'trusted_apprentice' && a.unlockedAt.getTime() > 0)) {
      this.unlockDivineAchievement('trusted_apprentice')
    }
    
    if (relationship.trustLevel >= 75 && !this.divineAchievements.find(a => a.id === 'sacred_colleague' && a.unlockedAt.getTime() > 0)) {
      this.unlockDivineAchievement('sacred_colleague')
    }
  }

  // Getters
  getMentorRelationships(): Map<SacredMentor, MentorRelationship> {
    return new Map(this.mentorRelationships)
  }

  getDivineRewards(): DivineReward[] {
    return [...this.divineRewards]
  }

  getSacredInsights(): SacredInsight[] {
    return [...this.sacredInsights]
  }

  getDivineAchievements(): DivineAchievement[] {
    return [...this.divineAchievements]
  }
}

// Export singleton instance
export const sacredMentorship = new SacredMentorshipSystem()