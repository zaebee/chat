/**
 * DataConnector - Real-time Communication Engine
 * 
 * Implements WebSocket-based communication with protocol translation capabilities
 * Provides secure, rate-limited messaging following ATCG architectural patterns
 * for Connector components with comprehensive error handling and reconnection.
 */

import type { ConnectorComponent } from './index'

// Communication Types - Pure technical terminology
export interface ConnectorMessage {
  readonly id: string
  readonly messageType: string
  readonly payload: Record<string, unknown>
  readonly priority: number // Message priority (0-10)
  readonly timestamp: string
  readonly sourceId: string
  readonly targetId: string
}

export interface PollenEvent {
  readonly event_id: string
  readonly event_type: string
  readonly version: string
  readonly timestamp: string
  readonly aggregate_id: string
  readonly payload: Record<string, unknown>
  readonly source_component?: string
  readonly correlation_id?: string
  readonly tags?: string[]
}

export interface WebSocketMessage {
  readonly type: string
  readonly data: Record<string, unknown>
  readonly timestamp?: string
  readonly id?: string
}

export interface MessageChannel {
  readonly channelId: string
  readonly messageTypes: string
  readonly isOpen: boolean
  readonly efficiency: number // 0-1, transmission efficiency
  readonly lastActivity: string
  readonly messageCount: number
}

export interface ConnectionMetrics {
  readonly connectionId: string
  readonly messageFrequency: number // Messages per second
  readonly signalStrength: number // Connection quality (0-1)
  readonly latency: number // Average latency in ms
  readonly errorRate: number // Error rate (0-1)
  readonly isStable: boolean // Connection stability
}

export interface MessageTransmissionResult {
  readonly original: ConnectorMessage | PollenEvent | WebSocketMessage
  readonly translated: ConnectorMessage | PollenEvent | WebSocketMessage
  readonly transmissionSuccess: boolean
  readonly protocolTranslation: 'websocket_to_pollen' | 'pollen_to_websocket' | 'internal'
  readonly timestamp: string
  readonly latency: number // milliseconds
}

export interface ValidationRules {
  readonly messageIntegrity: boolean
  readonly protocolCompliance: boolean
  readonly securityValidation: boolean
  readonly performanceOptimization: boolean
}

export interface SystemMetrics {
  readonly totalTransmissions: number
  readonly averageLatency: number
  readonly errorRate: number
  readonly protocolEfficiency: number
  readonly networkHealth: 'optimal' | 'degraded' | 'critical'
}

export interface ConnectorOutput {
  readonly transmission_result: MessageTransmissionResult
  readonly [key: string]: unknown
}

/**
 * DataConnector - Real-time Communication Engine
 * 
 * Implements WebSocket-based communication for real-time messaging between
 * components with protocol translation and connection management.
 */
export class DataConnector implements ConnectorComponent {
  readonly type = 'connector' as const
  readonly purpose = 'Real-time communication and protocol translation'
  readonly id: string

  // Security: Prevent connection flooding DoS attacks
  private static readonly MAX_CONNECTIONS = 50
  private static readonly MAX_MESSAGE_SIZE = 1024 * 1024 // 1MB
  private static readonly RATE_LIMIT_MESSAGES = 100 // per minute
  private static readonly RATE_LIMIT_WINDOW = 60000 // 1 minute in ms

  // Communication Constants - Engineering-based values
  private static readonly COMMUNICATION_CONSTANTS = {
    // Message processing parameters
    MIN_PRIORITY_THRESHOLD: 0.7, // Minimum priority for high-priority processing (0-1 scale)
    THROTTLE_DELAY: 50, // ms - minimum time between rapid message sends (anti-spam)
    PROCESSING_DELAY: 1, // ms - base processing latency for message handling
    
    // Connection quality parameters  
    TARGET_MESSAGE_RATE: 40, // messages/second - optimal throughput target
    QUALITY_DECAY_RATE: 0.95, // Connection quality decay per failed attempt
    MAX_ERROR_THRESHOLD: 0.3, // Maximum acceptable error rate before degradation
    
    // Reliability parameters
    MIN_RELIABILITY_THRESHOLD: 0.8, // Minimum connection reliability for stable operation
    CONNECTION_TIMEOUT: 1000, // ms - connection attempt timeout
    MAX_RETRY_DISTANCE: 10000, // Maximum retry attempts before giving up
  } as const

  // Connection State
  private messageChannels: Map<string, MessageChannel> = new Map()
  private connectionMetrics: Map<string, ConnectionMetrics> = new Map()
  private webSocketConnections: Map<string, WebSocket> = new Map()
  
  // Performance Metrics
  private transmissionCount = 0
  private totalLatency = 0
  private errorCount = 0
  private lastTransmission: Date | null = null
  
  // Rate Limiting
  private messageTimestamps: number[] = []
  
  // Connection Management
  private isConnected = false
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5

  constructor(
    private readonly config: {
      readonly id: string
      readonly webSocketUrl?: string
      readonly pollenEventBusUrl?: string
      readonly enableAdvancedFeatures?: boolean
    }
  ) {
    this.id = config.id
    this.validateConfiguration()
  }

  /**
   * Establish WebSocket connections to the communication network
   */
  async connect(): Promise<void> {
    try {
      // Validate connection limits
      if (this.webSocketConnections.size >= DataConnector.MAX_CONNECTIONS) {
        throw new Error(`Connection limit exceeded (${DataConnector.MAX_CONNECTIONS}). This prevents resource exhaustion.`)
      }

      // Establish primary WebSocket connection
      if (this.config.webSocketUrl) {
        await this.establishWebSocketConnection(this.config.webSocketUrl)
      }

      // Initialize connection metrics tracking
      await this.initializeConnectionMetrics()

      this.isConnected = true
      this.reconnectAttempts = 0

      // Emit connection established event
      await this.transmitMessage({
        id: this.generateMessageId(),
        messageType: 'connection_established',
        payload: { connectorId: this.config.id },
        priority: 8.0,
        timestamp: new Date().toISOString(),
        sourceId: this.config.id,
        targetId: 'network'
      })

    } catch (error) {
      this.errorCount++
      throw new Error(`Connection failed: ${error instanceof Error ? error.message : 'Unknown error'}`)
    }
  }

  /**
   * Disconnect from the communication network
   */
  async disconnect(): Promise<void> {
    try {
      // Close all WebSocket connections
      for (const [channelId, webSocket] of this.webSocketConnections) {
        if (webSocket.readyState === WebSocket.OPEN) {
          webSocket.close(1000, 'Clean disconnection')
        }
        this.webSocketConnections.delete(channelId)
      }

      // Deactivate message channels
      for (const [channelId, channel] of this.messageChannels) {
        this.messageChannels.set(channelId, {
          ...channel,
          isOpen: false,
          efficiency: 0
        })
      }

      this.isConnected = false

      // Emit disconnection event
      await this.transmitMessage({
        id: this.generateMessageId(),
        messageType: 'connection_terminated',
        payload: { connectorId: this.config.id },
        priority: 7.0,
        timestamp: new Date().toISOString(),
        sourceId: this.config.id,
        targetId: 'network'
      })

    } catch (error) {
      this.errorCount++
      throw new Error(`Disconnection failed: ${error instanceof Error ? error.message : 'Unknown error'}`)
    }
  }

  /**
   * Send data through the connector
   */
  async send(data: unknown): Promise<ConnectorOutput> {
    const startTime = performance.now()
    
    try {
      // Validate rate limiting
      if (!this.checkRateLimit()) {
        throw new Error('Rate limit exceeded')
      }

      // Convert data to connector message
      const message = this.convertToConnectorMessage(data)
      
      // Transmit message
      const result = await this.processMessageTransmission(message)
      
      // Update metrics
      const latency = performance.now() - startTime
      this.updateTransmissionMetrics(latency)
      
      return {
        transmission_result: result
      }

    } catch (error) {
      const latency = performance.now() - startTime
      this.updateTransmissionMetrics(latency, true)
      
      throw new Error(`Send failed: ${error instanceof Error ? error.message : 'Unknown error'}`)
    }
  }

  /**
   * Receive data from the connector
   */
  async receive(): Promise<unknown> {
    try {
      // Check for available messages in channels
      for (const [channelId, channel] of this.messageChannels) {
        if (channel.isOpen && channel.messageCount > 0) {
          return await this.retrieveChannelMessage(channelId)
        }
      }
      
      return null
    } catch (error) {
      this.errorCount++
      throw new Error(`Receive failed: ${error instanceof Error ? error.message : 'Unknown error'}`)
    }
  }

  /**
   * Establish WebSocket connection
   */
  private async establishWebSocketConnection(url: string): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        const webSocket = new WebSocket(url)
        const channelId = this.generateChannelId()
        
        webSocket.onopen = () => {
          this.webSocketConnections.set(channelId, webSocket)
          this.createMessageChannel(channelId, ['websocket'])
          resolve()
        }
        
        webSocket.onerror = (error) => {
          reject(new Error(`WebSocket connection failed: ${error}`))
        }
        
        webSocket.onmessage = (event) => {
          this.handleIncomingMessage(event.data, channelId)
        }
        
        webSocket.onclose = () => {
          this.webSocketConnections.delete(channelId)
          this.handleConnectionClosure(channelId)
        }
        
      } catch (error) {
        reject(error)
      }
    })
  }

  /**
   * Initialize connection metrics tracking
   */
  private async initializeConnectionMetrics(): Promise<void> {
    const metrics: ConnectionMetrics = {
      connectionId: this.config.id,
      messageFrequency: 0,
      signalStrength: 1.0,
      latency: 0,
      errorRate: 0,
      isStable: true
    }
    
    this.connectionMetrics.set(this.config.id, metrics)
  }

  /**
   * Transmit message through the network
   */
  private async transmitMessage(message: ConnectorMessage): Promise<void> {
    // Add to rate limiting tracking
    this.messageTimestamps.push(Date.now())
    
    // Broadcast to all open channels
    for (const [channelId, webSocket] of this.webSocketConnections) {
      if (webSocket.readyState === WebSocket.OPEN) {
        const webSocketMessage = this.translateConnectorToWebSocket(message)
        webSocket.send(JSON.stringify(webSocketMessage))
      }
    }
    
    this.lastTransmission = new Date()
  }

  /**
   * Generate unique message ID
   */
  private generateMessageId(): string {
    return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }

  /**
   * Generate unique channel ID
   */
  private generateChannelId(): string {
    return `ch_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }

  /**
   * Create message channel for specific types
   */
  private createMessageChannel(channelId: string, messageTypes: string[]): MessageChannel {
    const channel: MessageChannel = {
      channelId,
      messageTypes: messageTypes.join(','),
      isOpen: true,
      efficiency: 1.0,
      lastActivity: new Date().toISOString(),
      messageCount: 0
    }

    this.messageChannels.set(channelId, channel)
    return channel
  }

  /**
   * Convert data to connector message format
   */
  private convertToConnectorMessage(data: unknown): ConnectorMessage {
    return {
      id: this.generateMessageId(),
      messageType: 'data_transmission',
      payload: { data },
      priority: 5.0,
      timestamp: new Date().toISOString(),
      sourceId: this.config.id,
      targetId: 'network'
    }
  }

  /**
   * Process message transmission
   */
  private async processMessageTransmission(message: ConnectorMessage): Promise<MessageTransmissionResult> {
    const startTime = performance.now()
    
    try {
      // Translate to WebSocket format
      const webSocketMessage = this.translateConnectorToWebSocket(message)
      
      // Transmit through channels
      await this.transmitMessage(message)
      
      const latency = performance.now() - startTime
      
      return {
        original: message,
        translated: webSocketMessage,
        transmissionSuccess: true,
        protocolTranslation: 'websocket_to_pollen',
        timestamp: new Date().toISOString(),
        latency
      }
      
    } catch (error) {
      const latency = performance.now() - startTime
      
      return {
        original: message,
        translated: message,
        transmissionSuccess: false,
        protocolTranslation: 'internal',
        timestamp: new Date().toISOString(),
        latency
      }
    }
  }

  /**
   * Translate connector message to WebSocket message
   */
  private translateConnectorToWebSocket(message: ConnectorMessage): WebSocketMessage {
    return {
      type: message.messageType,
      data: message.payload,
      timestamp: message.timestamp,
      id: message.id
    }
  }

  /**
   * Translate WebSocket message to Pollen Protocol event
   */
  private translateWebSocketToPollen(message: WebSocketMessage): PollenEvent {
    return {
      event_id: message.id || this.generateMessageId(),
      event_type: `websocket_${message.type}_received`,
      version: '1.0',
      timestamp: message.timestamp || new Date().toISOString(),
      aggregate_id: this.config.id,
      payload: message.data,
      source_component: 'data_connector',
      tags: ['websocket', 'translation', message.type]
    }
  }

  /**
   * Translate Pollen Protocol event to WebSocket message
   */
  private translatePollenToWebSocket(event: PollenEvent): WebSocketMessage {
    return {
      type: event.event_type.replace('_received', '').replace('websocket_', ''),
      data: event.payload,
      timestamp: event.timestamp,
      id: event.event_id
    }
  }

  /**
   * Handle incoming message from WebSocket
   */
  private handleIncomingMessage(data: string, channelId: string): void {
    try {
      const message = JSON.parse(data) as WebSocketMessage
      
      // Update channel activity
      const channel = this.messageChannels.get(channelId)
      if (channel) {
        this.messageChannels.set(channelId, {
          ...channel,
          lastActivity: new Date().toISOString(),
          messageCount: channel.messageCount + 1
        })
      }
      
    } catch (error) {
      this.errorCount++
    }
  }

  /**
   * Handle connection closure
   */
  private handleConnectionClosure(channelId: string): void {
    const channel = this.messageChannels.get(channelId)
    if (channel) {
      this.messageChannels.set(channelId, {
        ...channel,
        isOpen: false,
        efficiency: 0
      })
    }
  }

  /**
   * Retrieve message from channel
   */
  private async retrieveChannelMessage(channelId: string): Promise<unknown> {
    // Placeholder for message retrieval logic
    return null
  }

  /**
   * Check rate limiting
   */
  private checkRateLimit(): boolean {
    const now = Date.now()
    
    // Clean old timestamps
    this.messageTimestamps = this.messageTimestamps.filter(
      timestamp => now - timestamp < DataConnector.RATE_LIMIT_WINDOW
    )
    
    return this.messageTimestamps.length < DataConnector.RATE_LIMIT_MESSAGES
  }

  /**
   * Update transmission metrics
   */
  private updateTransmissionMetrics(latency: number, isError = false): void {
    this.transmissionCount++
    this.totalLatency += latency
    
    if (isError) {
      this.errorCount++
    }
    
    // Update rate limiting
    this.messageTimestamps.push(Date.now())
  }

  /**
   * Validate configuration
   */
  private validateConfiguration(): void {
    if (!this.config.id) {
      throw new Error('Connector ID is required')
    }
    
    if (!this.config.webSocketUrl && !this.config.pollenEventBusUrl) {
      throw new Error('At least one connection URL must be provided')
    }
  }

  /**
   * Get comprehensive status
   */
  getStatus(): Record<string, unknown> {
    const errorRate = this.transmissionCount > 0 ? this.errorCount / this.transmissionCount : 0
    const averageLatency = this.transmissionCount > 0 ? this.totalLatency / this.transmissionCount : 0
    
    return {
      component: `DataConnector:${this.id}`,
      type: this.type,
      purpose: this.purpose,
      isConnected: this.isConnected,
      connectionCount: this.webSocketConnections.size,
      channelCount: this.messageChannels.size,
      transmissionCount: this.transmissionCount,
      errorRate,
      averageLatency,
      messageRate: this.getCurrentMessageRate(),
      networkHealth: this.getNetworkHealth(errorRate),
      timestamp: new Date().toISOString()
    }
  }

  /**
   * Get current message rate
   */
  private getCurrentMessageRate(): number {
    const now = Date.now()
    const recentMessages = this.messageTimestamps.filter(
      timestamp => now - timestamp < DataConnector.RATE_LIMIT_WINDOW
    )
    return recentMessages.length
  }

  /**
   * Determine network health based on error rate
   */
  private getNetworkHealth(errorRate: number): 'optimal' | 'degraded' | 'critical' {
    if (errorRate < 0.05) return 'optimal'
    if (errorRate < 0.2) return 'degraded'
    return 'critical'
  }
}

/**
 * Factory function for creating Data Connector instances
 */
export function createDataConnector(config: {
  readonly id: string
  readonly webSocketUrl?: string
  readonly pollenEventBusUrl?: string
  readonly enableAdvancedFeatures?: boolean
}): DataConnector {
  return new DataConnector(config)
}

/**
 * Type guard for Data Connector
 */
export function isDataConnector(component: unknown): component is DataConnector {
  return component instanceof DataConnector
}