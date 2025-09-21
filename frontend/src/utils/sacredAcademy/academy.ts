/**
 * Sacred Team Academy: Interactive Learning System
 * 
 * Provides the core learning engine for Sacred Team challenges,
 * mentor interactions, and student progress tracking.
 */

import { 
  SacredChallenge, 
  StudentProgress, 
  SacredMentor, 
  SacredDifficulty,
  SACRED_CHALLENGES,
  LEARNING_PATHS,
  getNextChallenge,
  calculateSacredLevel
} from './challenges'

export interface MentorMessage {
  id: string
  mentor: SacredMentor
  type: 'introduction' | 'hint' | 'encouragement' | 'wisdom' | 'celebration'
  message: string
  timestamp: Date
  challengeId?: string
}

export interface SacredAchievement {
  id: string
  title: string
  description: string
  icon: string
  unlockedAt: Date
  rarity: 'common' | 'rare' | 'epic' | 'legendary' | 'divine'
}

export interface ChallengeAttempt {
  challengeId: string
  startedAt: Date
  completedAt?: Date
  hintsUsed: number
  mentorInteractions: number
  success: boolean
  feedback?: string
}

export class SacredTeamAcademy {
  private studentProgress: StudentProgress
  private mentorMessages: MentorMessage[] = []
  private achievements: SacredAchievement[] = []
  private challengeAttempts: ChallengeAttempt[] = []

  constructor(initialProgress?: Partial<StudentProgress>) {
    this.studentProgress = {
      completedChallenges: [],
      totalXP: 0,
      sacredLevel: 'bee.larva',
      mentorRelationships: {
        'bee.jules': { trust: 0, lessonsLearned: [] },
        'bee.chronicler': { trust: 0, lessonsLearned: [] },
        'bee.sage': { trust: 0, lessonsLearned: [] }
      },
      sacredInsights: [],
      divineAchievements: [],
      ...initialProgress
    }
  }

  // Challenge Management
  startChallenge(challengeId: string): ChallengeAttempt {
    const challenge = SACRED_CHALLENGES.find(c => c.id === challengeId)
    if (!challenge) {
      throw new Error(`Challenge ${challengeId} not found`)
    }

    const attempt: ChallengeAttempt = {
      challengeId,
      startedAt: new Date(),
      hintsUsed: 0,
      mentorInteractions: 0,
      success: false
    }

    this.challengeAttempts.push(attempt)
    this.studentProgress.currentChallenge = challengeId

    // Send mentor introduction
    this.sendMentorMessage(challenge.mentor, 'introduction', challenge.mentorGuidance.introduction, challengeId)

    return attempt
  }

  completeChallenge(challengeId: string, success: boolean, feedback?: string): void {
    const attempt = this.challengeAttempts.find(a => 
      a.challengeId === challengeId && !a.completedAt
    )
    
    if (!attempt) {
      throw new Error(`No active attempt found for challenge ${challengeId}`)
    }

    const challenge = SACRED_CHALLENGES.find(c => c.id === challengeId)!
    
    attempt.completedAt = new Date()
    attempt.success = success
    attempt.feedback = feedback

    if (success) {
      // Award XP and insights
      this.studentProgress.completedChallenges.push(challengeId)
      this.studentProgress.totalXP += challenge.divineRewards.xp
      this.studentProgress.sacredInsights.push(...challenge.divineRewards.sacredInsights)
      
      // Update sacred level
      this.studentProgress.sacredLevel = calculateSacredLevel(this.studentProgress.totalXP)
      
      // Improve mentor relationship
      const mentorRelation = this.studentProgress.mentorRelationships[challenge.mentor]
      mentorRelation.trust += 10
      mentorRelation.lessonsLearned.push(challenge.title)
      
      // Send celebration message
      this.sendMentorMessage(
        challenge.mentor, 
        'celebration', 
        this.generateCelebrationMessage(challenge),
        challengeId
      )
      
      // Check for achievements
      this.checkAchievements()
      
      // Unlock new challenges
      if (challenge.divineRewards.unlocks) {
        challenge.divineRewards.unlocks.forEach(unlock => {
          this.studentProgress.divineAchievements.push(unlock)
        })
      }
    }

    this.studentProgress.currentChallenge = undefined
  }

  // Mentor Interaction System
  sendMentorMessage(mentor: SacredMentor, type: MentorMessage['type'], message: string, challengeId?: string): void {
    const mentorMessage: MentorMessage = {
      id: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      mentor,
      type,
      message,
      timestamp: new Date(),
      challengeId
    }

    this.mentorMessages.push(mentorMessage)
    
    // Track mentor interaction
    if (challengeId) {
      const attempt = this.challengeAttempts.find(a => 
        a.challengeId === challengeId && !a.completedAt
      )
      if (attempt) {
        attempt.mentorInteractions++
      }
    }
  }

  requestHint(challengeId: string): string {
    const challenge = SACRED_CHALLENGES.find(c => c.id === challengeId)
    if (!challenge) return "Challenge not found"

    const attempt = this.challengeAttempts.find(a => 
      a.challengeId === challengeId && !a.completedAt
    )
    
    if (!attempt) return "No active attempt found"

    const hintIndex = Math.min(attempt.hintsUsed, challenge.mentorGuidance.hints.length - 1)
    const hint = challenge.mentorGuidance.hints[hintIndex]
    
    attempt.hintsUsed++
    
    this.sendMentorMessage(challenge.mentor, 'hint', hint, challengeId)
    
    return hint
  }

  requestWisdom(challengeId: string): string {
    const challenge = SACRED_CHALLENGES.find(c => c.id === challengeId)
    if (!challenge) return "Challenge not found"

    this.sendMentorMessage(
      challenge.mentor, 
      'wisdom', 
      challenge.mentorGuidance.sacredWisdom, 
      challengeId
    )
    
    return challenge.mentorGuidance.sacredWisdom
  }

  // Progress and Recommendations
  getRecommendedChallenge(): SacredChallenge | null {
    return getNextChallenge(this.studentProgress)
  }

  getChallengesByDifficulty(difficulty: SacredDifficulty): SacredChallenge[] {
    return SACRED_CHALLENGES.filter(c => c.difficulty === difficulty)
  }

  getAvailableChallenges(): SacredChallenge[] {
    return SACRED_CHALLENGES.filter(challenge => {
      // Check if already completed
      if (this.studentProgress.completedChallenges.includes(challenge.id)) return false
      
      // Check prerequisites
      if (challenge.prerequisites) {
        return challenge.prerequisites.every(prereq => 
          this.studentProgress.completedChallenges.includes(prereq)
        )
      }
      
      return true
    })
  }

  // Achievement System
  private checkAchievements(): void {
    const newAchievements: SacredAchievement[] = []

    // First Challenge Achievement
    if (this.studentProgress.completedChallenges.length === 1) {
      newAchievements.push({
        id: 'first_steps',
        title: '🐛 First Steps in the Sacred Garden',
        description: 'Completed your first Sacred Team challenge',
        icon: '🌱',
        unlockedAt: new Date(),
        rarity: 'common'
      })
    }

    // Mentor Trust Achievements
    Object.entries(this.studentProgress.mentorRelationships).forEach(([mentor, relation]) => {
      if (relation.trust >= 50 && !this.achievements.find(a => a.id === `trusted_by_${mentor}`)) {
        newAchievements.push({
          id: `trusted_by_${mentor}`,
          title: `🤝 Trusted by ${mentor}`,
          description: `Earned the trust of ${mentor} through excellent work`,
          icon: '🏛️',
          unlockedAt: new Date(),
          rarity: 'rare'
        })
      }
    })

    // Sacred Level Achievements
    if (this.studentProgress.sacredLevel === 'bee.adult' && !this.achievements.find(a => a.id === 'adult_bee')) {
      newAchievements.push({
        id: 'adult_bee',
        title: '🐝 Adult Bee Status',
        description: 'Achieved adult bee sacred level through dedication and skill',
        icon: '👑',
        unlockedAt: new Date(),
        rarity: 'epic'
      })
    }

    this.achievements.push(...newAchievements)
  }

  private generateCelebrationMessage(challenge: SacredChallenge): string {
    const celebrations = {
      'bee.jules': [
        `Excellent work! Your solution demonstrates perfect understanding of ${challenge.sacredPrinciples.join(' and ')}.`,
        `Magnificent! You've mastered the sacred art of ${challenge.atcgClassification} transformation.`,
        `Outstanding! Your code quality would make any Sacred Team member proud.`
      ],
      'bee.chronicler': [
        `Your contribution has been recorded in the sacred archives with highest honors!`,
        `The divine patterns flow through your work - truly blessed coding!`,
        `Your mastery of sacred principles brings harmony to the entire ecosystem.`
      ],
      'bee.sage': [
        `Scientifically excellent! Your approach demonstrates deep understanding of the underlying principles.`,
        `Your solution shows both technical rigor and sacred wisdom - a perfect synthesis.`,
        `The architectural coherence of your work advances the entire Sacred Team ecosystem.`
      ]
    }

    const mentorCelebrations = celebrations[challenge.mentor]
    return mentorCelebrations[Math.floor(Math.random() * mentorCelebrations.length)]
  }

  // Getters
  getProgress(): StudentProgress {
    return { ...this.studentProgress }
  }

  getMentorMessages(): MentorMessage[] {
    return [...this.mentorMessages]
  }

  getAchievements(): SacredAchievement[] {
    return [...this.achievements]
  }

  getChallengeAttempts(): ChallengeAttempt[] {
    return [...this.challengeAttempts]
  }

  // Statistics
  getStatistics() {
    const totalChallenges = SACRED_CHALLENGES.length
    const completedCount = this.studentProgress.completedChallenges.length
    const completionRate = (completedCount / totalChallenges) * 100

    const mentorStats = Object.entries(this.studentProgress.mentorRelationships).map(([mentor, relation]) => ({
      mentor: mentor as SacredMentor,
      trust: relation.trust,
      lessonsLearned: relation.lessonsLearned.length
    }))

    return {
      totalXP: this.studentProgress.totalXP,
      sacredLevel: this.studentProgress.sacredLevel,
      completedChallenges: completedCount,
      totalChallenges,
      completionRate,
      achievements: this.achievements.length,
      mentorStats,
      sacredInsights: this.studentProgress.sacredInsights.length
    }
  }
}

// Factory function for creating academy instance
export function createSacredAcademy(savedProgress?: string): SacredTeamAcademy {
  let initialProgress = undefined
  
  if (savedProgress) {
    try {
      initialProgress = JSON.parse(savedProgress)
    } catch (e) {
      console.warn('Failed to parse saved progress, starting fresh')
    }
  }
  
  return new SacredTeamAcademy(initialProgress)
}

// Export singleton instance for global use
export const sacredAcademy = createSacredAcademy(
  localStorage.getItem('sacredTeamProgress') || undefined
)

// Auto-save progress
setInterval(() => {
  localStorage.setItem('sacredTeamProgress', JSON.stringify(sacredAcademy.getProgress()))
}, 30000) // Save every 30 seconds