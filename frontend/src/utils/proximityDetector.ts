/**
 * Proximity Detection System
 * 
 * Tracks bee positions and calculates spatial relationships for emotional contagion.
 * Uses efficient spatial indexing for real-time proximity queries.
 */

export interface BeePosition {
  beeId: string
  x: number
  y: number
  role: string
  emotionalState: string
  timestamp: number
}

export interface ProximityInfluence {
  sourceBee: string
  targetBee: string
  distance: number
  influenceStrength: number
  emotionalVector: string
  decayFactor: number
}

export interface ProximityMetrics {
  totalBees: number
  activeInfluences: number
  averageDistance: number
  clusteredBees: number
  isolatedBees: number
}

// Configuration constants - extracted for easy tuning
const DEFAULT_CONFIG = {
  maxInfluenceDistance: 150, // pixels - range of emotional influence
  updateInterval: 100, // ms - frequency of proximity calculations
  roleModifiers: {
    queen: 2.0,      // Queens have strong influence
    chronicler: 1.8, // Sacred bees have enhanced influence
    jules: 1.5,      // Divine debugging influence
    guard: 1.2,      // Guards have moderate influence
    scout: 1.0,      // Scouts have normal influence
    worker: 0.8      // Workers have slightly less influence
  },
  emotionalModifiers: {
    divine: 1.5,     // Divine state has strong influence
    excited: 1.3,    // Excitement is contagious
    protective: 1.2, // Protective state spreads
    focused: 1.0,    // Focused state is neutral
    calm: 0.8        // Calm state has gentle influence
  }
}

export class ProximityDetector {
  private beePositions: Map<string, BeePosition> = new Map()
  private influences: Map<string, ProximityInfluence[]> = new Map()
  private maxInfluenceDistance = DEFAULT_CONFIG.maxInfluenceDistance
  private updateInterval = DEFAULT_CONFIG.updateInterval
  private lastUpdate = 0

  /**
   * Register or update a bee's position
   */
  updateBeePosition(position: BeePosition): void {
    this.beePositions.set(position.beeId, {
      ...position,
      timestamp: Date.now()
    })
    
    // Trigger influence recalculation if enough time has passed
    const now = Date.now()
    if (now - this.lastUpdate > this.updateInterval) {
      this.calculateInfluences()
      this.lastUpdate = now
    }
  }

  /**
   * Remove a bee from tracking
   */
  removeBee(beeId: string): void {
    this.beePositions.delete(beeId)
    this.influences.delete(beeId)
    
    // Remove this bee from other bees' influence lists
    for (const [targetId, influenceList] of this.influences.entries()) {
      this.influences.set(
        targetId,
        influenceList.filter(inf => inf.sourceBee !== beeId)
      )
    }
  }

  /**
   * Get all bees within influence range of a target bee
   */
  getInfluencesForBee(beeId: string): ProximityInfluence[] {
    return this.influences.get(beeId) || []
  }

  /**
   * Get all current bee positions
   */
  getAllPositions(): BeePosition[] {
    return Array.from(this.beePositions.values())
  }

  /**
   * Calculate distance between two points
   */
  private calculateDistance(pos1: BeePosition, pos2: BeePosition): number {
    const dx = pos1.x - pos2.x
    const dy = pos1.y - pos2.y
    return Math.sqrt(dx * dx + dy * dy)
  }

  /**
   * Calculate influence strength based on distance and roles
   */
  private calculateInfluenceStrength(
    source: BeePosition, 
    target: BeePosition, 
    distance: number
  ): number {
    // Base influence decreases with distance (inverse square law)
    const baseInfluence = Math.max(0, 1 - (distance / this.maxInfluenceDistance) ** 2)
    
    const sourceModifier = DEFAULT_CONFIG.roleModifiers[source.role as keyof typeof DEFAULT_CONFIG.roleModifiers] || 1.0
    const emotionalModifier = DEFAULT_CONFIG.emotionalModifiers[source.emotionalState as keyof typeof DEFAULT_CONFIG.emotionalModifiers] || 1.0
    
    return baseInfluence * sourceModifier * emotionalModifier
  }

  /**
   * Calculate decay factor for influence over time
   */
  private calculateDecayFactor(source: BeePosition, target: BeePosition): number {
    // Emotional compatibility affects decay
    const compatibility = this.getEmotionalCompatibility(
      source.emotionalState, 
      target.emotionalState
    )
    
    // Compatible emotions decay slower, incompatible ones decay faster
    return compatibility > 0.5 ? 0.95 : 0.85
  }

  /**
   * Calculate emotional compatibility between two states
   */
  private getEmotionalCompatibility(state1: string, state2: string): number {
    // Compatibility matrix (0 = incompatible, 1 = highly compatible)
    const compatibilityMatrix: Record<string, Record<string, number>> = {
      calm: { calm: 1.0, focused: 0.8, divine: 0.7, excited: 0.3, protective: 0.4 },
      excited: { excited: 1.0, focused: 0.6, protective: 0.7, calm: 0.3, divine: 0.5 },
      focused: { focused: 1.0, calm: 0.8, divine: 0.9, excited: 0.6, protective: 0.7 },
      protective: { protective: 1.0, excited: 0.7, focused: 0.7, calm: 0.4, divine: 0.6 },
      divine: { divine: 1.0, focused: 0.9, calm: 0.7, protective: 0.6, excited: 0.5 }
    }
    
    return compatibilityMatrix[state1]?.[state2] || 0.5
  }

  /**
   * Recalculate all proximity influences
   * 
   * Performance Note: This is O(n²) complexity where n = number of bees.
   * This is acceptable for the target range of 6-12 bees but would need
   * spatial indexing (quadtree/grid) for larger swarms.
   */
  private calculateInfluences(): void {
    // Clear existing influences
    this.influences.clear()
    
    const positions = Array.from(this.beePositions.values())
    
    // Calculate influences for each bee
    for (const targetBee of positions) {
      const influences: ProximityInfluence[] = []
      
      for (const sourceBee of positions) {
        if (sourceBee.beeId === targetBee.beeId) continue
        
        const distance = this.calculateDistance(sourceBee, targetBee)
        
        // Only consider bees within influence range
        if (distance <= this.maxInfluenceDistance) {
          const influenceStrength = this.calculateInfluenceStrength(
            sourceBee, 
            targetBee, 
            distance
          )
          
          // Only add significant influences
          if (influenceStrength > 0.1) {
            influences.push({
              sourceBee: sourceBee.beeId,
              targetBee: targetBee.beeId,
              distance,
              influenceStrength,
              emotionalVector: sourceBee.emotionalState,
              decayFactor: this.calculateDecayFactor(sourceBee, targetBee)
            })
          }
        }
      }
      
      // Sort by influence strength (strongest first)
      influences.sort((a, b) => b.influenceStrength - a.influenceStrength)
      
      this.influences.set(targetBee.beeId, influences)
    }
  }

  /**
   * Get proximity metrics for monitoring
   */
  getMetrics(): ProximityMetrics {
    const positions = Array.from(this.beePositions.values())
    const totalBees = positions.length
    
    let totalInfluences = 0
    let totalDistance = 0
    let distanceCount = 0
    let clusteredBees = 0
    
    for (const influences of this.influences.values()) {
      totalInfluences += influences.length
      
      if (influences.length > 0) {
        clusteredBees++
      }
      
      for (const influence of influences) {
        totalDistance += influence.distance
        distanceCount++
      }
    }
    
    return {
      totalBees,
      activeInfluences: totalInfluences,
      averageDistance: distanceCount > 0 ? totalDistance / distanceCount : 0,
      clusteredBees,
      isolatedBees: totalBees - clusteredBees
    }
  }

  /**
   * Get system status for debugging
   */
  getStatus(): {
    status: string
    beesTracked: number
    influencesActive: number
    lastUpdate: number
  } {
    return {
      status: 'active',
      beesTracked: this.beePositions.size,
      influencesActive: Array.from(this.influences.values()).reduce(
        (sum, influences) => sum + influences.length, 0
      ),
      lastUpdate: this.lastUpdate
    }
  }

  /**
   * Configure proximity detection parameters
   */
  configure(options: {
    maxInfluenceDistance?: number
    updateInterval?: number
  }): void {
    if (options.maxInfluenceDistance !== undefined) {
      this.maxInfluenceDistance = options.maxInfluenceDistance
    }
    if (options.updateInterval !== undefined) {
      this.updateInterval = options.updateInterval
    }
  }
}

// Export singleton instance
export const proximityDetector = new ProximityDetector()