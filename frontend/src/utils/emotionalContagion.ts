/**
 * Emotional Contagion System
 * 
 * Manages emotional influence between bees based on proximity and social dynamics.
 * Creates cascading emotional waves that demonstrate emergent collective behavior.
 */

import { proximityDetector, type ProximityInfluence, type BeePosition } from './proximityDetector'
import { pollenBus, BeeEventTypes } from './pollenProtocol'
import type { HiveIntent } from './hiveIntent'

export interface EmotionalInfluence {
  targetBeeId: string
  sourceEmotions: string[]
  influenceStrength: number
  targetEmotion: string
  transitionSpeed: number
  timestamp: number
}

export interface ContagionMetrics {
  activeInfluences: number
  emotionalWaves: number
  averageInfluenceStrength: number
  dominantEmotion: string
  emotionalDiversity: number
  contagionEvents: number
}

export interface ContagionConfig {
  enabled: boolean
  influenceStrength: number // 0-1 multiplier
  propagationSpeed: number // 0-1 speed multiplier
  resistanceFactors: Record<string, number> // role-based resistance
  emotionalMomentum: number // 0-1 how much bees resist change
}

// Configuration constants - extracted for easy tuning
const DEFAULT_CONTAGION_CONFIG: ContagionConfig = {
  enabled: true,
  influenceStrength: 0.7,
  propagationSpeed: 0.5,
  resistanceFactors: {
    queen: 0.3,      // Queens resist emotional change
    chronicler: 0.2, // Sacred bees are emotionally stable
    jules: 0.4,      // Debugging requires emotional control
    guard: 0.5,      // Guards have moderate resistance
    scout: 0.8,      // Scouts are emotionally flexible
    worker: 0.7      // Workers are moderately influenced
  },
  emotionalMomentum: 0.6
}

const EMOTIONAL_HISTORY_LENGTH = 10 // Maximum emotional states to remember
const RECENT_HISTORY_SAMPLE = 5 // Recent states used for momentum calculation

export class EmotionalContagionEngine {
  private activeInfluences: Map<string, EmotionalInfluence[]> = new Map()
  private emotionalHistory: Map<string, string[]> = new Map()
  private contagionEvents = 0
  private lastUpdate = 0
  private updateInterval = 200 // ms

  private config: ContagionConfig = { ...DEFAULT_CONTAGION_CONFIG }

  /**
   * Process emotional influences for all bees
   */
  processContagion(): void {
    if (!this.config.enabled) return

    const now = Date.now()
    if (now - this.lastUpdate < this.updateInterval) return

    this.lastUpdate = now
    this.activeInfluences.clear()

    const allPositions = proximityDetector.getAllPositions()
    
    for (const targetBee of allPositions) {
      const influences = proximityDetector.getInfluencesForBee(targetBee.beeId)
      
      if (influences.length > 0) {
        const emotionalInfluence = this.calculateEmotionalInfluence(
          targetBee, 
          influences
        )
        
        if (emotionalInfluence) {
          this.activeInfluences.set(targetBee.beeId, [emotionalInfluence])
          
          // Emit contagion event
          this.emitContagionEvent(emotionalInfluence)
        }
      }
    }
  }

  /**
   * Calculate emotional influence for a target bee
   */
  private calculateEmotionalInfluence(
    targetBee: BeePosition,
    proximityInfluences: ProximityInfluence[]
  ): EmotionalInfluence | null {
    // Group influences by emotional state
    const emotionalGroups = new Map<string, ProximityInfluence[]>()
    
    for (const influence of proximityInfluences) {
      const emotion = influence.emotionalVector
      if (!emotionalGroups.has(emotion)) {
        emotionalGroups.set(emotion, [])
      }
      emotionalGroups.get(emotion)!.push(influence)
    }

    // Calculate combined influence for each emotion
    const emotionalStrengths = new Map<string, number>()
    
    for (const [emotion, influences] of emotionalGroups.entries()) {
      const totalStrength = influences.reduce((sum, inf) => {
        return sum + (inf.influenceStrength * this.config.influenceStrength)
      }, 0)
      
      emotionalStrengths.set(emotion, totalStrength)
    }

    // Find the strongest emotional influence
    let strongestEmotion = ''
    let strongestStrength = 0
    
    for (const [emotion, strength] of emotionalStrengths.entries()) {
      if (strength > strongestStrength) {
        strongestEmotion = emotion
        strongestStrength = strength
      }
    }

    // Check if influence is strong enough to cause change
    const resistance = this.config.resistanceFactors[targetBee.role] || 0.5
    const momentum = this.getEmotionalMomentum(targetBee.beeId, targetBee.emotionalState)
    const threshold = resistance + momentum

    if (strongestStrength > threshold && strongestEmotion !== targetBee.emotionalState) {
      return {
        targetBeeId: targetBee.beeId,
        sourceEmotions: Array.from(emotionalStrengths.keys()),
        influenceStrength: strongestStrength,
        targetEmotion: strongestEmotion,
        transitionSpeed: this.calculateTransitionSpeed(strongestStrength),
        timestamp: Date.now()
      }
    }

    return null
  }

  /**
   * Calculate emotional momentum (resistance to change based on history)
   */
  private getEmotionalMomentum(beeId: string, currentEmotion: string): number {
    const history = this.emotionalHistory.get(beeId) || []
    
    if (history.length === 0) return 0
    
    // Count recent occurrences of current emotion
    const recentHistory = history.slice(-RECENT_HISTORY_SAMPLE) // Last N states for momentum
    const sameEmotionCount = recentHistory.filter(e => e === currentEmotion).length
    
    // More consistent emotions create more momentum
    return (sameEmotionCount / recentHistory.length) * this.config.emotionalMomentum
  }

  /**
   * Calculate transition speed based on influence strength
   */
  private calculateTransitionSpeed(influenceStrength: number): number {
    // Stronger influences cause faster transitions
    const baseSpeed = this.config.propagationSpeed
    const strengthMultiplier = Math.min(influenceStrength * 2, 2.0)
    
    return baseSpeed * strengthMultiplier
  }

  /**
   * Update emotional history for a bee
   */
  updateEmotionalHistory(beeId: string, emotion: string): void {
    if (!this.emotionalHistory.has(beeId)) {
      this.emotionalHistory.set(beeId, [])
    }
    
    const history = this.emotionalHistory.get(beeId)!
    history.push(emotion)
    
    // Keep only recent history
    if (history.length > EMOTIONAL_HISTORY_LENGTH) {
      history.shift()
    }
  }

  /**
   * Get emotional influence for a specific bee
   */
  getInfluenceForBee(beeId: string): EmotionalInfluence | null {
    const influences = this.activeInfluences.get(beeId)
    return influences && influences.length > 0 ? influences[0] : null
  }

  /**
   * Get all active emotional influences
   */
  getAllInfluences(): Map<string, EmotionalInfluence[]> {
    return new Map(this.activeInfluences)
  }

  /**
   * Emit contagion event for monitoring
   */
  private emitContagionEvent(influence: EmotionalInfluence): void {
    this.contagionEvents++
    
    pollenBus.emit(BeeEventTypes.EMOTIONAL_CONTAGION, {
      targetBeeId: influence.targetBeeId,
      sourceEmotions: influence.sourceEmotions,
      targetEmotion: influence.targetEmotion,
      influenceStrength: influence.influenceStrength,
      transitionSpeed: influence.transitionSpeed
    }, {
      source: 'emotional-contagion-engine',
      priority: 'normal'
    })
  }

  /**
   * Trigger emotional wave from a specific bee
   */
  triggerEmotionalWave(
    sourceBeeId: string, 
    emotion: string, 
    intensity: number = 1.0
  ): void {
    // Find the source bee position
    const allPositions = proximityDetector.getAllPositions()
    const sourceBee = allPositions.find(pos => pos.beeId === sourceBeeId)
    
    if (!sourceBee) {
      console.warn(`EmotionalContagion: Source bee '${sourceBeeId}' not found for emotional wave. Available bees:`, 
        allPositions.map(p => p.beeId))
      return
    }

    // Create artificial strong influence
    const waveInfluences = proximityDetector.getInfluencesForBee(sourceBeeId)
    
    for (const influence of waveInfluences) {
      const targetInfluence: EmotionalInfluence = {
        targetBeeId: influence.targetBee,
        sourceEmotions: [emotion],
        influenceStrength: intensity * 2.0, // Amplified for wave effect
        targetEmotion: emotion,
        transitionSpeed: this.config.propagationSpeed * 1.5,
        timestamp: Date.now()
      }
      
      this.activeInfluences.set(influence.targetBee, [targetInfluence])
      this.emitContagionEvent(targetInfluence)
    }

    // Emit wave event
    pollenBus.emit(BeeEventTypes.EMOTIONAL_WAVE_TRIGGERED, {
      sourceBeeId,
      emotion,
      intensity,
      affectedBees: waveInfluences.length
    }, {
      source: 'emotional-contagion-engine',
      priority: 'high'
    })
  }

  /**
   * Get contagion metrics for monitoring
   */
  getMetrics(): ContagionMetrics {
    const allInfluences = Array.from(this.activeInfluences.values()).flat()
    const emotionCounts = new Map<string, number>()
    let totalStrength = 0

    for (const influence of allInfluences) {
      const emotion = influence.targetEmotion
      emotionCounts.set(emotion, (emotionCounts.get(emotion) || 0) + 1)
      totalStrength += influence.influenceStrength
    }

    // Find dominant emotion
    let dominantEmotion = 'calm'
    let maxCount = 0
    for (const [emotion, count] of emotionCounts.entries()) {
      if (count > maxCount) {
        dominantEmotion = emotion
        maxCount = count
      }
    }

    // Calculate emotional diversity (Shannon entropy)
    const totalEmotions = Array.from(emotionCounts.values()).reduce((a, b) => a + b, 0)
    let diversity = 0
    if (totalEmotions > 0) {
      for (const count of emotionCounts.values()) {
        const p = count / totalEmotions
        if (p > 0) {
          diversity -= p * Math.log2(p)
        }
      }
    }

    return {
      activeInfluences: allInfluences.length,
      emotionalWaves: this.contagionEvents,
      averageInfluenceStrength: allInfluences.length > 0 ? totalStrength / allInfluences.length : 0,
      dominantEmotion,
      emotionalDiversity: diversity,
      contagionEvents: this.contagionEvents
    }
  }

  /**
   * Configure contagion parameters
   */
  configure(newConfig: Partial<ContagionConfig>): void {
    this.config = { ...this.config, ...newConfig }
  }

  /**
   * Get current configuration
   */
  getConfig(): ContagionConfig {
    return { ...this.config }
  }

  /**
   * Get system status
   */
  getStatus(): {
    status: string
    enabled: boolean
    activeInfluences: number
    lastUpdate: number
  } {
    return {
      status: 'active',
      enabled: this.config.enabled,
      activeInfluences: Array.from(this.activeInfluences.values()).flat().length,
      lastUpdate: this.lastUpdate
    }
  }

  /**
   * Reset contagion state
   */
  reset(): void {
    this.activeInfluences.clear()
    this.emotionalHistory.clear()
    this.contagionEvents = 0
  }
}

// Export singleton instance
export const emotionalContagionEngine = new EmotionalContagionEngine()