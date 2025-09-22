/**
 * HiveEventBridge - Sacred Connector Integration with Backend Event Bus
 * 
 * Bridges the Sacred Connector frontend with the HiveEventBus backend
 * Implements bidirectional Pollen Protocol communication over WebSocket
 */

import { SacredConnector } from './SacredConnector'
import type { PollenEvent, SynapticMessage } from './SacredConnector'

// Backend HiveEventBus API types
export interface HiveEventBusAPI {
  readonly endpoint: string
  readonly websocketUrl: string
  readonly pollenProtocolVersion: string
}

export interface EventSubscription {
  readonly subscriptionId: string
  readonly eventTypes: string[]
  readonly aggregateIds: string[]
  readonly tags: string[]
  readonly callback: (event: PollenEvent) => Promise<void>
}

export interface HiveBridgeConfig {
  readonly connectorId: string
  readonly hiveEventBusUrl: string
  readonly websocketUrl: string
  readonly enableAutoReconnect?: boolean
  readonly maxReconnectAttempts?: number
  readonly reconnectDelay?: number
}

/**
 * Sacred Event Bridge for Hive Integration
 * 
 * Connects Sacred Connector to the backend HiveEventBus using WebSocket
 * and Pollen Protocol for seamless frontend-backend communication.
 */
export class HiveEventBridge {
  private connector: SacredConnector
  private subscriptions: Map<string, EventSubscription> = new Map()
  private isConnected = false
  private reconnectAttempts = 0
  private reconnectTimer: number | null = null

  constructor(private readonly config: HiveBridgeConfig) {
    this.connector = new SacredConnector({
      id: config.connectorId,
      webSocketUrl: config.websocketUrl,
      enableQuantumEntanglement: true
    })
  }

  /**
   * Establish connection to Hive Event Bus
   */
  async connect(): Promise<void> {
    try {
      // Connect the Sacred Connector
      await this.connector.connect()

      // Register with Hive Event Bus
      await this.registerWithHiveEventBus()

      this.isConnected = true
      this.reconnectAttempts = 0

      // Emit bridge connection event
      await this.publishEvent({
        event_type: 'hive_bridge_connected',
        aggregate_id: this.config.connectorId,
        payload: {
          bridge_id: this.config.connectorId,
          websocket_url: this.config.websocketUrl,
          pollen_protocol_version: '1.0'
        },
        source_component: 'hive_event_bridge',
        tags: ['bridge', 'connection', 'hive']
      })

    } catch (error) {
      if (this.config.enableAutoReconnect && 
          this.reconnectAttempts < (this.config.maxReconnectAttempts || 5)) {
        await this.scheduleReconnect()
      } else {
        throw new Error(`Hive Event Bridge connection failed: ${error instanceof Error ? error.message : 'Unknown error'}`)
      }
    }
  }

  /**
   * Disconnect from Hive Event Bus
   */
  async disconnect(): Promise<void> {
    try {
      // Clear reconnect timer
      if (this.reconnectTimer) {
        clearTimeout(this.reconnectTimer)
        this.reconnectTimer = null
      }

      // Emit bridge disconnection event
      if (this.isConnected) {
        await this.publishEvent({
          event_type: 'hive_bridge_disconnected',
          aggregate_id: this.config.connectorId,
          payload: {
            bridge_id: this.config.connectorId,
            disconnect_reason: 'manual_disconnect'
          },
          source_component: 'hive_event_bridge',
          tags: ['bridge', 'disconnection', 'hive']
        })
      }

      // Disconnect the Sacred Connector
      await this.connector.disconnect()

      // Clear subscriptions
      this.subscriptions.clear()
      this.isConnected = false

    } catch (error) {
      throw new Error(`Hive Event Bridge disconnection failed: ${error instanceof Error ? error.message : 'Unknown error'}`)
    }
  }

  /**
   * Publish event to Hive Event Bus
   */
  async publishEvent(eventData: Partial<PollenEvent>): Promise<boolean> {
    try {
      if (!this.isConnected) {
        throw new Error('Hive Event Bridge not connected')
      }

      // Create complete Pollen Protocol event
      const pollenEvent: PollenEvent = {
        event_id: eventData.event_id || this.generateEventId(),
        event_type: eventData.event_type || 'unknown_event',
        version: eventData.version || '1.0',
        timestamp: eventData.timestamp || new Date().toISOString(),
        aggregate_id: eventData.aggregate_id || this.config.connectorId,
        payload: eventData.payload || {},
        source_component: eventData.source_component || 'hive_event_bridge',
        correlation_id: eventData.correlation_id || this.generateEventId(),
        tags: eventData.tags || []
      }

      // Send through Sacred Connector
      const result = await this.connector.send({
        type: 'pollen_event',
        action: 'publish',
        event: pollenEvent
      })

      return true

    } catch (error) {
      console.error('Failed to publish event to Hive Event Bus:', error)
      return false
    }
  }

  /**
   * Subscribe to events from Hive Event Bus
   */
  async subscribeToEvents(
    eventTypes: string[] = [],
    aggregateIds: string[] = [],
    tags: string[] = [],
    callback: (event: PollenEvent) => Promise<void>
  ): Promise<string> {
    try {
      if (!this.isConnected) {
        throw new Error('Hive Event Bridge not connected')
      }

      const subscriptionId = this.generateEventId()
      
      const subscription: EventSubscription = {
        subscriptionId,
        eventTypes,
        aggregateIds,
        tags,
        callback
      }

      // Store subscription
      this.subscriptions.set(subscriptionId, subscription)

      // Send subscription request to backend
      await this.connector.send({
        type: 'pollen_subscription',
        action: 'subscribe',
        subscription: {
          subscription_id: subscriptionId,
          event_types: eventTypes,
          aggregate_ids: aggregateIds,
          tags: tags
        }
      })

      return subscriptionId

    } catch (error) {
      throw new Error(`Failed to subscribe to Hive events: ${error instanceof Error ? error.message : 'Unknown error'}`)
    }
  }

  /**
   * Unsubscribe from events
   */
  async unsubscribeFromEvents(subscriptionId: string): Promise<boolean> {
    try {
      if (!this.subscriptions.has(subscriptionId)) {
        return false
      }

      // Remove local subscription
      this.subscriptions.delete(subscriptionId)

      // Send unsubscription request to backend
      await this.connector.send({
        type: 'pollen_subscription',
        action: 'unsubscribe',
        subscription_id: subscriptionId
      })

      return true

    } catch (error) {
      console.error('Failed to unsubscribe from Hive events:', error)
      return false
    }
  }

  /**
   * Publish Sacred Aggregator events to Hive
   */
  async publishAggregatorEvent(
    aggregatorId: string,
    eventType: string,
    aggregationData: Record<string, unknown>
  ): Promise<boolean> {
    return await this.publishEvent({
      event_type: `sacred_aggregator_${eventType}`,
      aggregate_id: aggregatorId,
      payload: {
        aggregator_id: aggregatorId,
        aggregation_data: aggregationData,
        ionic_bonds: aggregationData.bonds || [],
        lattice_energy: aggregationData.latticeEnergy || 0,
        structure_type: aggregationData.structureType || 'unknown'
      },
      source_component: 'sacred_aggregator',
      tags: ['aggregator', 'ionic', 'sacred', eventType]
    })
  }

  /**
   * Subscribe to Sacred Aggregator events from other components
   */
  async subscribeToAggregatorEvents(
    callback: (event: PollenEvent) => Promise<void>
  ): Promise<string> {
    return await this.subscribeToEvents(
      ['sacred_aggregator_aggregated', 'sacred_aggregator_updated', 'sacred_aggregator_validated'],
      [],
      ['aggregator', 'sacred'],
      callback
    )
  }

  /**
   * Get bridge status and health
   */
  getStatus(): Record<string, unknown> {
    const connectorStatus = this.connector.getStatus() as Record<string, unknown>
    
    return {
      component: 'HiveEventBridge',
      type: 'Bridge',
      bridge_id: this.config.connectorId,
      
      // Connection state
      connection_state: {
        is_connected: this.isConnected,
        reconnect_attempts: this.reconnectAttempts,
        max_reconnect_attempts: this.config.maxReconnectAttempts || 5,
        auto_reconnect_enabled: this.config.enableAutoReconnect || false
      },

      // Subscription management
      subscription_state: {
        active_subscriptions: this.subscriptions.size,
        subscription_ids: Array.from(this.subscriptions.keys())
      },

      // Backend integration
      backend_integration: {
        hive_event_bus_url: this.config.hiveEventBusUrl,
        websocket_url: this.config.websocketUrl,
        pollen_protocol_version: '1.0'
      },

      // Underlying connector status
      connector_status: connectorStatus,

      // Health assessment
      health: this.isConnected && 
              (connectorStatus.health === 'optimal' || connectorStatus.health === 'degraded') 
              ? 'connected' : 'disconnected',

      timestamp: new Date().toISOString()
    }
  }

  // Private helper methods

  private async registerWithHiveEventBus(): Promise<void> {
    // Send registration message to backend HiveEventBus
    await this.connector.send({
      type: 'hive_registration',
      action: 'register_bridge',
      bridge_info: {
        bridge_id: this.config.connectorId,
        bridge_type: 'sacred_connector',
        capabilities: ['pollen_protocol', 'websocket', 'aggregator_integration'],
        version: '1.0'
      }
    })
  }

  private async scheduleReconnect(): Promise<void> {
    this.reconnectAttempts++
    const delay = (this.config.reconnectDelay || 1000) * Math.pow(2, this.reconnectAttempts - 1)
    
    this.reconnectTimer = setTimeout(async () => {
      try {
        await this.connect()
      } catch (error) {
        console.error('Reconnection attempt failed:', error)
      }
    }, delay) as unknown as number
  }

  private generateEventId(): string {
    return `hive_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }

  private async handleIncomingEvent(event: PollenEvent): Promise<void> {
    // Route incoming events to matching subscriptions
    for (const [subscriptionId, subscription] of this.subscriptions) {
      if (this.eventMatchesSubscription(event, subscription)) {
        try {
          await subscription.callback(event)
        } catch (error) {
          console.error(`Error in subscription callback ${subscriptionId}:`, error)
        }
      }
    }
  }

  private eventMatchesSubscription(event: PollenEvent, subscription: EventSubscription): boolean {
    // Match event types (empty array means match all)
    if (subscription.eventTypes.length > 0 && 
        !subscription.eventTypes.includes(event.event_type)) {
      return false
    }

    // Match aggregate IDs (empty array means match all)
    if (subscription.aggregateIds.length > 0 && 
        !subscription.aggregateIds.includes(event.aggregate_id)) {
      return false
    }

    // Match tags (empty array means match all)
    if (subscription.tags.length > 0 && 
        !subscription.tags.some(tag => event.tags?.includes(tag))) {
      return false
    }

    return true
  }
}

/**
 * Factory function for creating Hive Event Bridge instances
 */
export function createHiveEventBridge(config: HiveBridgeConfig): HiveEventBridge {
  return new HiveEventBridge(config)
}

/**
 * Type guard for Hive Event Bridge
 */
export function isHiveEventBridge(bridge: unknown): bridge is HiveEventBridge {
  return bridge instanceof HiveEventBridge
}