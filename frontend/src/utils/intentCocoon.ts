/**
 * Intent Cocoon - Simple Transition Validation
 * 
 * Provides smooth intent transitions to prevent jarring bee behavior changes.
 * Keeps it simple: just smooth interpolation and basic validation.
 */

import type { HiveIntent } from './hiveIntent'
import { pollenBus, BeeEventTypes } from './pollenProtocol'

export interface IntentTransition {
  beeId: string
  from: HiveIntent
  to: HiveIntent
  progress: number // 0-1
  duration: number // milliseconds
  startTime: number
  isValid: boolean
}

export interface TransitionOptions {
  duration?: number // Default 1000ms
  easing?: 'linear' | 'ease-out' | 'divine' // Default 'divine'
  validateTransition?: boolean // Default true
}

/**
 * Simple validation: prevent extreme jumps in intent values
 */
export function validateTransition(from: HiveIntent, to: HiveIntent): boolean {
  // Simple rule: no extreme jumps (>0.5 change in core values)
  const activityJump = Math.abs(to.activityLevel - from.activityLevel)
  const focusJump = Math.abs(to.focusIntensity - from.focusIntensity)
  const socialJump = Math.abs(to.socialAlignment - from.socialAlignment)
  
  // Allow larger jumps for sacred collaboration mode (divine transcendence)
  const maxJump = to.collaborationMode === 'sacred' || from.collaborationMode === 'sacred' ? 0.7 : 0.5
  
  return activityJump <= maxJump && focusJump <= maxJump && socialJump <= maxJump
}

/**
 * Divine easing function using golden ratio
 */
function divineEasing(progress: number): number {
  // Golden ratio-based easing for natural feel
  const φ = 1.618033988749
  return 1 - Math.pow(1 - progress, φ / 2)
}

/**
 * Apply easing function based on type
 */
function applyEasing(progress: number, easing: TransitionOptions['easing']): number {
  switch (easing) {
    case 'linear':
      return progress
    case 'ease-out':
      return 1 - Math.pow(1 - progress, 2)
    case 'divine':
    default:
      return divineEasing(progress)
  }
}

/**
 * Smooth interpolation between two intent states
 */
export function interpolateIntent(
  from: HiveIntent, 
  to: HiveIntent, 
  progress: number,
  easing: TransitionOptions['easing'] = 'divine'
): HiveIntent {
  const easedProgress = applyEasing(progress, easing)
  
  return {
    activityLevel: from.activityLevel + (to.activityLevel - from.activityLevel) * easedProgress,
    focusIntensity: from.focusIntensity + (to.focusIntensity - from.focusIntensity) * easedProgress,
    socialAlignment: from.socialAlignment + (to.socialAlignment - from.socialAlignment) * easedProgress,
    
    // Discrete properties change at midpoint
    collaborationMode: easedProgress < 0.5 ? from.collaborationMode : to.collaborationMode,
    purpose: easedProgress < 0.3 ? from.purpose : to.purpose,
    emotionalState: easedProgress < 0.5 ? from.emotionalState : to.emotionalState
  }
}

/**
 * Simple Intent Transition Manager
 */
export class IntentTransitionManager {
  private activeTransitions: Map<string, IntentTransition> = new Map()
  private animationFrames: Map<string, number> = new Map()

  /**
   * Start a smooth transition for a bee
   */
  async startTransition(
    beeId: string,
    from: HiveIntent,
    to: HiveIntent,
    options: TransitionOptions = {}
  ): Promise<void> {
    const {
      duration = 1000,
      easing = 'divine',
      validateTransition: shouldValidate = true
    } = options

    // Validate transition if requested
    if (shouldValidate && !validateTransition(from, to)) {
      // Emit validation failed event
      pollenBus.emit(BeeEventTypes.VALIDATION_FAILED, {
        beeId,
        reason: 'Intent transition too extreme',
        from,
        to,
        timestamp: Date.now()
      }, {
        source: 'intent-transition-manager'
      })
      
      throw new Error(`Intent transition validation failed for bee ${beeId}: transition too extreme`)
    }

    // Cancel any existing transition for this bee
    this.cancelTransition(beeId)

    // Create new transition
    const transition: IntentTransition = {
      beeId,
      from: { ...from },
      to: { ...to },
      progress: 0,
      duration,
      startTime: Date.now(),
      isValid: true
    }

    this.activeTransitions.set(beeId, transition)

    // Emit transition started event
    pollenBus.emit(BeeEventTypes.INTENT_TRANSITION_STARTED, {
      beeId,
      from,
      to,
      duration,
      timestamp: Date.now()
    }, {
      source: 'intent-transition-manager'
    })

    // Start animation
    return new Promise((resolve) => {
      const animate = () => {
        const currentTransition = this.activeTransitions.get(beeId)
        if (!currentTransition) {
          resolve()
          return
        }

        const elapsed = Date.now() - currentTransition.startTime
        const progress = Math.min(elapsed / currentTransition.duration, 1)
        
        currentTransition.progress = progress

        // Emit progress event
        pollenBus.emit(BeeEventTypes.INTENT_TRANSITION_PROGRESS, {
          beeId,
          progress,
          currentIntent: interpolateIntent(from, to, progress, easing),
          timestamp: Date.now()
        }, {
          source: 'intent-transition-manager'
        })

        if (progress >= 1) {
          // Transition complete
          this.completeTransition(beeId)
          resolve()
        } else {
          // Continue animation
          const frameId = requestAnimationFrame(animate)
          this.animationFrames.set(beeId, frameId)
        }
      }

      animate()
    })
  }

  /**
   * Get current interpolated intent for a bee
   */
  getCurrentIntent(beeId: string, baseIntent: HiveIntent): HiveIntent {
    const transition = this.activeTransitions.get(beeId)
    if (!transition) {
      return baseIntent
    }

    return interpolateIntent(transition.from, transition.to, transition.progress)
  }

  /**
   * Check if a bee is currently transitioning
   */
  isTransitioning(beeId: string): boolean {
    return this.activeTransitions.has(beeId)
  }

  /**
   * Cancel an active transition
   */
  cancelTransition(beeId: string): void {
    const frameId = this.animationFrames.get(beeId)
    if (frameId) {
      cancelAnimationFrame(frameId)
      this.animationFrames.delete(beeId)
    }

    const transition = this.activeTransitions.get(beeId)
    if (transition) {
      this.activeTransitions.delete(beeId)
      
      // Emit cancellation event
      pollenBus.emit(BeeEventTypes.INTENT_TRANSITION_PROGRESS, {
        beeId,
        cancelled: true,
        timestamp: Date.now()
      }, {
        source: 'intent-transition-manager'
      })
    }
  }

  /**
   * Complete a transition
   */
  private completeTransition(beeId: string): void {
    const transition = this.activeTransitions.get(beeId)
    if (!transition) return

    // Clean up
    this.cancelTransition(beeId)

    // Emit completion event
    pollenBus.emit(BeeEventTypes.INTENT_EMERGENCE_READY, {
      beeId,
      finalIntent: transition.to,
      transitionDuration: Date.now() - transition.startTime,
      timestamp: Date.now()
    }, {
      source: 'intent-transition-manager'
    })
  }

  /**
   * Get all active transitions
   */
  getActiveTransitions(): IntentTransition[] {
    return Array.from(this.activeTransitions.values())
  }

  /**
   * Get transition status
   */
  getStatus(): {
    activeTransitions: number
    totalTransitions: number
  } {
    return {
      activeTransitions: this.activeTransitions.size,
      totalTransitions: 0 // TODO: Add metrics tracking
    }
  }

  /**
   * Clean up all transitions (for component unmount)
   */
  cleanup(): void {
    for (const beeId of this.activeTransitions.keys()) {
      this.cancelTransition(beeId)
    }
  }
}

// Export singleton instance
export const intentTransitionManager = new IntentTransitionManager()

// Utility functions
export const createSmoothTransition = (
  beeId: string,
  from: HiveIntent,
  to: HiveIntent,
  options?: TransitionOptions
) => {
  return intentTransitionManager.startTransition(beeId, from, to, options)
}

export const isIntentTransitioning = (beeId: string): boolean => {
  return intentTransitionManager.isTransitioning(beeId)
}

export const getCurrentTransitionIntent = (beeId: string, baseIntent: HiveIntent): HiveIntent => {
  return intentTransitionManager.getCurrentIntent(beeId, baseIntent)
}