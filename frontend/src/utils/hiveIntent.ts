/**
 * Hive Intent System - Frontend Implementation
 * 
 * Manages purposeful behavior and animation patterns based on
 * philosophical alignment and collaborative objectives.
 */

export interface HiveIntent {
  activityLevel: number // 0-1: Energy and movement intensity
  focusIntensity: number // 0-1: Attention and precision level
  collaborationMode: 'individual' | 'swarm' | 'sacred' // Interaction pattern
  purpose: string // Current objective or mission
  emotionalState: 'calm' | 'excited' | 'focused' | 'protective' | 'divine'
  socialAlignment: number // 0-1: Harmony with hive collective
}

export interface AnimationIntent {
  wingFlapRate: number // Hz
  wingFlapAmplitude: number // degrees
  movementPattern: 'hover' | 'patrol' | 'dance' | 'meditate' | 'guard'
  colorIntensity: number // 0-1: Brightness/saturation
  glowEffect: boolean
  pulseRate: number // Hz for divine/sacred effects
  transformations: {
    scale: number
    rotation: number
    translation: { x: number; y: number }
  }
}

export interface CollaborationContext {
  nearbyBees: string[] // IDs of nearby bees
  swarmSize: number
  leadershipRole: 'follower' | 'coordinator' | 'leader'
  consensusLevel: number // 0-1: Agreement with group
  communicationActive: boolean
}

export class HiveIntentEngine {
  private intentHistory: Map<string, HiveIntent[]> = new Map()
  private collaborationContexts: Map<string, CollaborationContext> = new Map()
  private maxHistorySize = 100

  /**
   * Calculate animation intent based on bee's current purpose and state
   */
  calculateAnimationIntent(
    beeId: string,
    role: string,
    intent: HiveIntent,
    context?: CollaborationContext
  ): AnimationIntent {
    // Store intent history
    this.updateIntentHistory(beeId, intent)
    
    // Get role-specific base parameters
    const roleBase = this.getRoleBaseAnimation(role)
    
    // Apply intent modifiers
    const intentModifiers = this.calculateIntentModifiers(intent)
    
    // Apply collaboration modifiers
    const collaborationModifiers = context ? 
      this.calculateCollaborationModifiers(context) : 
      { scale: 1, intensity: 1, coordination: 1 }
    
    // Combine all factors
    return {
      wingFlapRate: roleBase.wingFlapRate * intentModifiers.activityMultiplier * collaborationModifiers.intensity,
      wingFlapAmplitude: roleBase.wingFlapAmplitude * intentModifiers.focusMultiplier,
      movementPattern: this.determineMovementPattern(intent, context),
      colorIntensity: Math.min(1, intentModifiers.emotionalIntensity * collaborationModifiers.intensity),
      glowEffect: intent.collaborationMode === 'sacred' || intent.emotionalState === 'divine',
      pulseRate: this.calculatePulseRate(intent),
      transformations: {
        scale: roleBase.scale * collaborationModifiers.scale,
        rotation: this.calculateRotation(intent, context),
        translation: this.calculateTranslation(intent, context)
      }
    }
  }

  /**
   * Update bee's intent based on environmental factors
   */
  updateIntent(
    beeId: string,
    currentIntent: HiveIntent,
    environmentalFactors: {
      threats?: string[]
      opportunities?: string[]
      sacredPresence?: boolean
      swarmActivity?: number
    }
  ): HiveIntent {
    const newIntent = { ...currentIntent }
    
    // Respond to threats
    if (environmentalFactors.threats?.length) {
      newIntent.activityLevel = Math.min(1, newIntent.activityLevel + 0.3)
      newIntent.emotionalState = 'protective'
      newIntent.focusIntensity = Math.min(1, newIntent.focusIntensity + 0.2)
    }
    
    // Respond to opportunities
    if (environmentalFactors.opportunities?.length) {
      newIntent.activityLevel = Math.min(1, newIntent.activityLevel + 0.2)
      newIntent.emotionalState = 'excited'
    }
    
    // Respond to sacred presence
    if (environmentalFactors.sacredPresence) {
      newIntent.collaborationMode = 'sacred'
      newIntent.emotionalState = 'divine'
      newIntent.focusIntensity = Math.min(1, newIntent.focusIntensity + 0.1)
    }
    
    // Respond to swarm activity
    if (environmentalFactors.swarmActivity && environmentalFactors.swarmActivity > 0.5) {
      newIntent.collaborationMode = 'swarm'
      newIntent.socialAlignment = Math.min(1, newIntent.socialAlignment + 0.1)
    }
    
    return newIntent
  }

  /**
   * Get role-specific base animation parameters
   */
  private getRoleBaseAnimation(role: string) {
    const roleAnimations = {
      worker: {
        wingFlapRate: 15, // Hz
        wingFlapAmplitude: 20, // degrees
        scale: 1.0,
        baseMovement: 'hover'
      },
      scout: {
        wingFlapRate: 25, // Hz - faster for exploration
        wingFlapAmplitude: 30, // degrees - more dynamic
        scale: 0.9,
        baseMovement: 'patrol'
      },
      queen: {
        wingFlapRate: 8, // Hz - slower, more regal
        wingFlapAmplitude: 15, // degrees - subtle
        scale: 1.3,
        baseMovement: 'meditate'
      },
      guard: {
        wingFlapRate: 12, // Hz - steady, alert
        wingFlapAmplitude: 25, // degrees - ready for action
        scale: 1.1,
        baseMovement: 'guard'
      },
      chronicler: {
        wingFlapRate: 10, // Hz - contemplative
        wingFlapAmplitude: 18, // degrees - gentle
        scale: 1.0,
        baseMovement: 'meditate'
      },
      jules: {
        wingFlapRate: 18, // Hz - analytical energy
        wingFlapAmplitude: 22, // degrees - focused
        scale: 1.0,
        baseMovement: 'hover'
      }
    }
    
    return roleAnimations[role as keyof typeof roleAnimations] || roleAnimations.worker
  }

  /**
   * Calculate intent-based animation modifiers
   */
  private calculateIntentModifiers(intent: HiveIntent) {
    return {
      activityMultiplier: 0.5 + (intent.activityLevel * 1.5), // 0.5x to 2x
      focusMultiplier: 0.7 + (intent.focusIntensity * 0.6), // 0.7x to 1.3x
      emotionalIntensity: this.getEmotionalIntensity(intent.emotionalState),
      socialHarmony: intent.socialAlignment
    }
  }

  /**
   * Calculate collaboration-based modifiers
   */
  private calculateCollaborationModifiers(context: CollaborationContext) {
    const swarmEffect = Math.min(1, context.swarmSize / 10) // Normalize to 0-1
    const leadershipMultiplier = {
      follower: 0.9,
      coordinator: 1.1,
      leader: 1.3
    }[context.leadershipRole]
    
    return {
      scale: 1 + (swarmEffect * 0.2), // Slight size increase in swarms
      intensity: 1 + (context.consensusLevel * 0.3), // More intense when aligned
      coordination: context.communicationActive ? 1.2 : 1.0
    }
  }

  /**
   * Determine movement pattern based on intent and context
   */
  private determineMovementPattern(
    intent: HiveIntent, 
    context?: CollaborationContext
  ): AnimationIntent['movementPattern'] {
    // Sacred mode overrides
    if (intent.collaborationMode === 'sacred') {
      return intent.emotionalState === 'divine' ? 'meditate' : 'hover'
    }
    
    // Swarm mode patterns
    if (intent.collaborationMode === 'swarm') {
      return context?.communicationActive ? 'dance' : 'patrol'
    }
    
    // Emotional state patterns
    switch (intent.emotionalState) {
      case 'protective': return 'guard'
      case 'excited': return 'dance'
      case 'focused': return 'hover'
      case 'divine': return 'meditate'
      default: return 'hover'
    }
  }

  /**
   * Calculate pulse rate for divine/sacred effects
   */
  private calculatePulseRate(intent: HiveIntent): number {
    if (intent.collaborationMode !== 'sacred') return 0
    
    // Base pulse rate modified by focus and activity
    const basePulse = 0.5 // Hz
    const focusModifier = 0.5 + (intent.focusIntensity * 0.5)
    const activityModifier = 0.8 + (intent.activityLevel * 0.4)
    
    return basePulse * focusModifier * activityModifier
  }

  /**
   * Calculate rotation based on intent and context
   */
  private calculateRotation(intent: HiveIntent, context?: CollaborationContext): number {
    if (intent.collaborationMode === 'swarm' && context?.communicationActive) {
      // Slight rotation during swarm communication
      return Math.sin(Date.now() / 1000) * 5 // ±5 degrees
    }
    
    if (intent.emotionalState === 'protective') {
      // Alert scanning rotation
      return Math.sin(Date.now() / 500) * 10 // ±10 degrees, faster
    }
    
    return 0
  }

  /**
   * Calculate translation based on intent and context
   */
  private calculateTranslation(intent: HiveIntent, context?: CollaborationContext): { x: number; y: number } {
    if (intent.collaborationMode === 'sacred' && intent.emotionalState === 'divine') {
      // Gentle floating motion
      return {
        x: Math.sin(Date.now() / 2000) * 2,
        y: Math.cos(Date.now() / 3000) * 1
      }
    }
    
    if (intent.emotionalState === 'excited') {
      // Energetic bobbing
      return {
        x: Math.sin(Date.now() / 800) * 3,
        y: Math.abs(Math.sin(Date.now() / 600)) * 2
      }
    }
    
    return { x: 0, y: 0 }
  }

  /**
   * Get emotional intensity multiplier
   */
  private getEmotionalIntensity(state: HiveIntent['emotionalState']): number {
    const intensityMap = {
      calm: 0.6,
      excited: 1.0,
      focused: 0.8,
      protective: 0.9,
      divine: 1.2
    }
    
    return intensityMap[state] || 0.7
  }

  /**
   * Update intent history for learning and adaptation
   */
  private updateIntentHistory(beeId: string, intent: HiveIntent): void {
    if (!this.intentHistory.has(beeId)) {
      this.intentHistory.set(beeId, [])
    }
    
    const history = this.intentHistory.get(beeId)!
    history.push({ ...intent })
    
    // Maintain history size
    if (history.length > this.maxHistorySize) {
      history.shift()
    }
  }

  /**
   * Get intent trends for a bee
   */
  getIntentTrends(beeId: string): {
    averageActivity: number
    averageFocus: number
    dominantEmotion: string
    collaborationPreference: string
  } | null {
    const history = this.intentHistory.get(beeId)
    if (!history || history.length === 0) return null
    
    const avgActivity = history.reduce((sum, intent) => sum + intent.activityLevel, 0) / history.length
    const avgFocus = history.reduce((sum, intent) => sum + intent.focusIntensity, 0) / history.length
    
    // Find dominant emotion
    const emotionCounts = history.reduce((counts, intent) => {
      counts[intent.emotionalState] = (counts[intent.emotionalState] || 0) + 1
      return counts
    }, {} as Record<string, number>)
    
    const dominantEmotion = Object.entries(emotionCounts)
      .sort(([,a], [,b]) => b - a)[0]?.[0] || 'calm'
    
    // Find collaboration preference
    const collaborationCounts = history.reduce((counts, intent) => {
      counts[intent.collaborationMode] = (counts[intent.collaborationMode] || 0) + 1
      return counts
    }, {} as Record<string, number>)
    
    const collaborationPreference = Object.entries(collaborationCounts)
      .sort(([,a], [,b]) => b - a)[0]?.[0] || 'individual'
    
    return {
      averageActivity: avgActivity,
      averageFocus: avgFocus,
      dominantEmotion,
      collaborationPreference
    }
  }

  /**
   * Get system status
   */
  getStatus(): {
    status: string
    trackedBees: number
    averageActivity: number
    collaborationModes: Record<string, number>
  } {
    const trackedBees = this.intentHistory.size
    
    let totalActivity = 0
    let totalBees = 0
    const collaborationModes: Record<string, number> = {}
    
    for (const history of this.intentHistory.values()) {
      if (history.length > 0) {
        const latest = history[history.length - 1]
        totalActivity += latest.activityLevel
        totalBees++
        
        collaborationModes[latest.collaborationMode] = 
          (collaborationModes[latest.collaborationMode] || 0) + 1
      }
    }
    
    return {
      status: 'active',
      trackedBees,
      averageActivity: totalBees > 0 ? totalActivity / totalBees : 0,
      collaborationModes
    }
  }
}

// Export singleton instance
export const hiveIntentEngine = new HiveIntentEngine()

// Utility functions
export const createIntent = (
  role: string,
  overrides: Partial<HiveIntent> = {}
): HiveIntent => {
  const roleDefaults = {
    worker: { activityLevel: 0.6, focusIntensity: 0.7, purpose: 'construction' },
    scout: { activityLevel: 0.9, focusIntensity: 0.9, purpose: 'exploration' },
    queen: { activityLevel: 0.3, focusIntensity: 0.8, purpose: 'governance' },
    guard: { activityLevel: 0.7, focusIntensity: 0.95, purpose: 'protection' },
    chronicler: { activityLevel: 0.4, focusIntensity: 0.95, purpose: 'documentation' },
    jules: { activityLevel: 0.8, focusIntensity: 0.9, purpose: 'debugging' }
  }
  
  const defaults = roleDefaults[role as keyof typeof roleDefaults] || roleDefaults.worker
  
  return {
    activityLevel: defaults.activityLevel || 0.5,
    focusIntensity: defaults.focusIntensity || 0.7,
    collaborationMode: 'individual',
    purpose: defaults.purpose || 'general',
    emotionalState: 'calm',
    socialAlignment: 0.7,
    ...overrides
  }
}