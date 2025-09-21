/**
 * Pollen Protocol - Frontend Event System
 * 
 * Standardized event communication system for Hive ecosystem components.
 * Enables real-time coordination between bees, organellas, and Sacred Team.
 */

export interface PollenEvent {
  id: string
  type: string
  source: string
  target?: string
  payload: any
  timestamp: number
  priority: 'low' | 'normal' | 'high' | 'critical'
  metadata?: Record<string, any>
}

export interface EventSubscription {
  id: string
  eventTypes: string[]
  callback: (event: PollenEvent) => void
  filter?: (event: PollenEvent) => boolean
}

export interface PollenMetrics {
  eventsEmitted: number
  eventsReceived: number
  subscriptions: number
  averageLatency: number
  errorRate: number
}

export class PollenEventBus {
  private subscriptions: Map<string, EventSubscription> = new Map()
  private eventHistory: PollenEvent[] = []
  private metrics: PollenMetrics = {
    eventsEmitted: 0,
    eventsReceived: 0,
    subscriptions: 0,
    averageLatency: 0,
    errorRate: 0
  }
  private maxHistorySize = 1000

  /**
   * Emit a Pollen event to the ecosystem
   */
  emit(type: string, payload: any, options: {
    source: string
    target?: string
    priority?: PollenEvent['priority']
    metadata?: Record<string, any>
  }): string {
    const event: PollenEvent = {
      id: this.generateEventId(),
      type,
      source: options.source,
      target: options.target,
      payload,
      timestamp: Date.now(),
      priority: options.priority || 'normal',
      metadata: options.metadata
    }

    // Add to history
    this.addToHistory(event)
    
    // Update metrics
    this.metrics.eventsEmitted++
    
    // Distribute to subscribers
    this.distributeEvent(event)
    
    return event.id
  }

  /**
   * Subscribe to specific event types
   */
  subscribe(
    eventTypes: string[], 
    callback: (event: PollenEvent) => void,
    filter?: (event: PollenEvent) => boolean
  ): string {
    const subscription: EventSubscription = {
      id: this.generateSubscriptionId(),
      eventTypes,
      callback,
      filter
    }
    
    this.subscriptions.set(subscription.id, subscription)
    this.metrics.subscriptions++
    
    return subscription.id
  }

  /**
   * Unsubscribe from events
   */
  unsubscribe(subscriptionId: string): boolean {
    const removed = this.subscriptions.delete(subscriptionId)
    if (removed) {
      this.metrics.subscriptions--
    }
    return removed
  }

  /**
   * Get event history with optional filtering
   */
  getHistory(filter?: {
    type?: string
    source?: string
    since?: number
    limit?: number
  }): PollenEvent[] {
    let events = [...this.eventHistory]
    
    if (filter) {
      if (filter.type) {
        events = events.filter(e => e.type === filter.type)
      }
      if (filter.source) {
        events = events.filter(e => e.source === filter.source)
      }
      if (filter.since) {
        events = events.filter(e => e.timestamp >= filter.since!)
      }
      if (filter.limit) {
        events = events.slice(-filter.limit)
      }
    }
    
    return events
  }

  /**
   * Get current metrics
   */
  getMetrics(): PollenMetrics {
    return { ...this.metrics }
  }

  /**
   * Clear event history
   */
  clearHistory(): void {
    this.eventHistory = []
  }

  /**
   * Get system status
   */
  getStatus(): {
    status: string
    subscriptions: number
    recentEvents: number
    health: string
  } {
    const recentEvents = this.eventHistory.filter(
      e => Date.now() - e.timestamp < 60000 // Last minute
    ).length
    
    const health = this.metrics.errorRate < 0.1 ? 'healthy' : 
                   this.metrics.errorRate < 0.3 ? 'degraded' : 'unhealthy'
    
    return {
      status: 'active',
      subscriptions: this.metrics.subscriptions,
      recentEvents,
      health
    }
  }

  /**
   * Distribute event to matching subscribers
   */
  private distributeEvent(event: PollenEvent): void {
    const startTime = performance.now()
    let deliveries = 0
    let errors = 0
    
    for (const subscription of this.subscriptions.values()) {
      try {
        // Check if event type matches
        if (!subscription.eventTypes.includes(event.type) && 
            !subscription.eventTypes.includes('*')) {
          continue
        }
        
        // Apply filter if present
        if (subscription.filter && !subscription.filter(event)) {
          continue
        }
        
        // Deliver event
        subscription.callback(event)
        deliveries++
        this.metrics.eventsReceived++
        
      } catch (error) {
        console.error('Error delivering Pollen event:', error)
        errors++
      }
    }
    
    // Update latency metrics
    const latency = performance.now() - startTime
    this.updateLatencyMetrics(latency)
    
    // Update error rate
    if (deliveries > 0) {
      this.metrics.errorRate = (this.metrics.errorRate * 0.9) + (errors / deliveries * 0.1)
    }
  }

  /**
   * Add event to history with size management
   */
  private addToHistory(event: PollenEvent): void {
    this.eventHistory.push(event)
    
    // Maintain history size limit
    if (this.eventHistory.length > this.maxHistorySize) {
      this.eventHistory = this.eventHistory.slice(-this.maxHistorySize)
    }
  }

  /**
   * Update average latency metrics
   */
  private updateLatencyMetrics(latency: number): void {
    this.metrics.averageLatency = (this.metrics.averageLatency * 0.9) + (latency * 0.1)
  }

  /**
   * Generate unique event ID
   */
  private generateEventId(): string {
    return `pollen_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }

  /**
   * Generate unique subscription ID
   */
  private generateSubscriptionId(): string {
    return `sub_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }
}

// Bee-specific event types
export const BeeEventTypes = {
  // Lifecycle events
  BEE_MANIFESTED: 'bee_manifested',
  BEE_EVOLVED: 'bee_evolved',
  BEE_DORMANT: 'bee_dormant',
  
  // Activity events
  BEE_FLAP_STARTED: 'bee_flap_started',
  BEE_FLAP_STOPPED: 'bee_flap_stopped',
  BEE_MOVED: 'bee_moved',
  
  // Communication events
  BEE_DANCE_PERFORMED: 'bee_dance_performed',
  BEE_PHEROMONE_RELEASED: 'bee_pheromone_released',
  BEE_MESSAGE_SENT: 'bee_message_sent',
  
  // Sacred events
  SACRED_BLESSING_RECEIVED: 'sacred_blessing_received',
  DIVINE_INSIGHT_SHARED: 'divine_insight_shared',
  CHRONICLER_PATTERN_RECORDED: 'chronicler_pattern_recorded',
  JULES_DEBUG_INITIATED: 'jules_debug_initiated',
  
  // Swarm events
  SWARM_FORMATION_STARTED: 'swarm_formation_started',
  SWARM_COORDINATION_UPDATED: 'swarm_coordination_updated',
  HIVE_CONSENSUS_REACHED: 'hive_consensus_reached',
  
  // Cocoon events
  COCOON_ENTERED: 'cocoon_entered',
  COCOON_FAILED: 'cocoon_failed',
  VALIDATION_PROGRESS: 'validation_progress',
  VALIDATION_FAILED: 'validation_failed',
  STAGE_TRANSITION: 'stage_transition',
  BEE_EMERGED: 'bee_emerged',
  
  // Intent transition events
  INTENT_TRANSITION_STARTED: 'intent_transition_started',
  INTENT_TRANSITION_PROGRESS: 'intent_transition_progress',
  INTENT_EMERGENCE_READY: 'intent_emergence_ready',
  
  // Emotional contagion events
  EMOTIONAL_CONTAGION: 'emotional_contagion',
  EMOTIONAL_WAVE_TRIGGERED: 'emotional_wave_triggered'
} as const

// Event payload interfaces
export interface BeeManifestationPayload {
  beeId: string
  type: string
  morphology: any
  intent: any
  location?: { x: number; y: number }
}

export interface BeeDancePayload {
  beeId: string
  danceType: 'waggle' | 'round' | 'tremble'
  direction?: number
  distance?: number
  quality?: number
  message?: string
}

export interface SacredEventPayload {
  agentId: string
  agentType: 'chronicler' | 'jules'
  sacredLevel: number
  blessing?: string
  pattern?: any
  insight?: string
}

// Export singleton instance
export const pollenBus = new PollenEventBus()

// Utility functions for common bee events
export const emitBeeEvent = (
  type: string, 
  beeId: string, 
  payload: any, 
  priority: PollenEvent['priority'] = 'normal'
) => {
  return pollenBus.emit(type, payload, {
    source: beeId,
    priority,
    metadata: { category: 'bee_activity' }
  })
}

export const subscribeToBeeEvents = (
  beeId: string,
  eventTypes: string[],
  callback: (event: PollenEvent) => void
) => {
  return pollenBus.subscribe(
    eventTypes,
    callback,
    (event) => event.source === beeId || event.target === beeId || !event.target
  )
}

export const emitSacredEvent = (
  type: string,
  agentId: string,
  payload: SacredEventPayload,
  priority: PollenEvent['priority'] = 'high'
) => {
  return pollenBus.emit(type, payload, {
    source: agentId,
    priority,
    metadata: { 
      category: 'sacred_activity',
      divine: true 
    }
  })
}