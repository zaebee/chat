/**
 * ChatProtocolTranslator - Sacred WebSocket to Pollen Protocol Translation
 * 
 * Specialized translator for chat application messages between WebSocket
 * and Pollen Protocol formats, enabling Sacred Aggregator integration
 */

import type { PollenEvent, WebSocketMessage, SynapticMessage } from './SacredConnector'

// Chat-specific message types
export interface ChatMessage {
  readonly id: string
  readonly type: 'user_message' | 'system_message' | 'ai_response' | 'status_update'
  readonly content: string
  readonly userId: string
  readonly username?: string
  readonly timestamp: string
  readonly metadata?: Record<string, unknown>
}

export interface ChatEvent {
  readonly type: 'user_joined' | 'user_left' | 'message_sent' | 'typing_started' | 'typing_stopped'
  readonly userId: string
  readonly username?: string
  readonly roomId?: string
  readonly timestamp: string
  readonly data?: Record<string, unknown>
}

export interface AggregatorUpdate {
  readonly aggregatorId: string
  readonly action: 'aggregate' | 'update' | 'validate' | 'reset'
  readonly elements: unknown[]
  readonly result?: Record<string, unknown>
  readonly timestamp: string
}

/**
 * Sacred Chat Protocol Translator
 * 
 * Translates between WebSocket chat messages and Pollen Protocol events
 * with special handling for Sacred Aggregator integration
 */
export class ChatProtocolTranslator {
  private static readonly CHAT_EVENT_TYPES = {
    // WebSocket to Pollen mappings
    user_message: 'chat_message_received',
    system_message: 'system_notification_received',
    ai_response: 'ai_response_received',
    status_update: 'status_update_received',
    user_joined: 'user_joined_chat',
    user_left: 'user_left_chat',
    typing_started: 'user_typing_started',
    typing_stopped: 'user_typing_stopped',
    
    // Sacred Aggregator specific
    aggregator_update: 'sacred_aggregator_updated',
    aggregator_result: 'sacred_aggregator_completed',
    ionic_bond_formed: 'ionic_bond_established',
    lattice_energy_calculated: 'lattice_energy_computed'
  } as const

  /**
   * Translate WebSocket chat message to Pollen Protocol event
   */
  static translateChatMessageToPollen(message: ChatMessage): PollenEvent {
    const eventType = ChatProtocolTranslator.CHAT_EVENT_TYPES[message.type] || 'unknown_chat_event'
    
    return {
      event_id: message.id,
      event_type: eventType,
      version: '1.0',
      timestamp: message.timestamp,
      aggregate_id: `chat:${message.userId}`,
      payload: {
        message_id: message.id,
        content: message.content,
        user_id: message.userId,
        username: message.username,
        message_type: message.type,
        metadata: message.metadata || {}
      },
      source_component: 'chat_frontend',
      correlation_id: `chat_${message.id}`,
      tags: ['chat', 'message', message.type]
    }
  }

  /**
   * Translate WebSocket chat event to Pollen Protocol event
   */
  static translateChatEventToPollen(event: ChatEvent): PollenEvent {
    const eventType = ChatProtocolTranslator.CHAT_EVENT_TYPES[event.type] || 'unknown_chat_event'
    
    return {
      event_id: `evt_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      event_type: eventType,
      version: '1.0',
      timestamp: event.timestamp,
      aggregate_id: event.roomId ? `room:${event.roomId}` : `user:${event.userId}`,
      payload: {
        user_id: event.userId,
        username: event.username,
        room_id: event.roomId,
        event_type: event.type,
        event_data: event.data || {}
      },
      source_component: 'chat_frontend',
      correlation_id: `chat_event_${event.userId}`,
      tags: ['chat', 'event', event.type]
    }
  }

  /**
   * Translate Sacred Aggregator update to Pollen Protocol event
   */
  static translateAggregatorUpdateToPollen(update: AggregatorUpdate): PollenEvent {
    const eventType = update.action === 'aggregate' 
      ? 'sacred_aggregator_completed'
      : `sacred_aggregator_${update.action}d`
    
    return {
      event_id: `agg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      event_type: eventType,
      version: '1.0',
      timestamp: update.timestamp,
      aggregate_id: update.aggregatorId,
      payload: {
        aggregator_id: update.aggregatorId,
        action: update.action,
        elements: update.elements,
        result: update.result || {},
        ionic_bonds: update.result?.bonds || [],
        lattice_energy: update.result?.latticeEnergy || 0,
        structure_type: update.result?.structureType || 'unknown',
        structural_integrity: update.result?.structuralIntegrity || false
      },
      source_component: 'sacred_aggregator',
      correlation_id: `aggregator_${update.aggregatorId}`,
      tags: ['aggregator', 'sacred', 'ionic', update.action]
    }
  }

  /**
   * Translate Pollen Protocol event to WebSocket chat message
   */
  static translatePollenToChatMessage(event: PollenEvent): ChatMessage | null {
    // Only translate chat-related events
    if (!event.tags?.includes('chat') || !event.tags?.includes('message')) {
      return null
    }

    const messageType = this.extractChatMessageType(event.event_type)
    if (!messageType) {
      return null
    }

    return {
      id: event.event_id,
      type: messageType,
      content: event.payload.content as string || '',
      userId: event.payload.user_id as string || '',
      username: event.payload.username as string,
      timestamp: event.timestamp,
      metadata: event.payload.metadata as Record<string, unknown>
    }
  }

  /**
   * Translate Pollen Protocol event to WebSocket chat event
   */
  static translatePollenToChatEvent(event: PollenEvent): ChatEvent | null {
    // Only translate chat event-related events
    if (!event.tags?.includes('chat') || !event.tags?.includes('event')) {
      return null
    }

    const eventType = this.extractChatEventType(event.event_type)
    if (!eventType) {
      return null
    }

    return {
      type: eventType,
      userId: event.payload.user_id as string || '',
      username: event.payload.username as string,
      roomId: event.payload.room_id as string,
      timestamp: event.timestamp,
      data: event.payload.event_data as Record<string, unknown>
    }
  }

  /**
   * Translate generic WebSocket message to Pollen Protocol event
   */
  static translateWebSocketToPollen(message: WebSocketMessage): PollenEvent {
    return {
      event_id: message.id || `ws_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      event_type: `websocket_${message.type}_received`,
      version: '1.0',
      timestamp: message.timestamp || new Date().toISOString(),
      aggregate_id: 'websocket_bridge',
      payload: message.data,
      source_component: 'websocket_connector',
      correlation_id: `ws_${message.id || Date.now()}`,
      tags: ['websocket', 'bridge', message.type]
    }
  }

  /**
   * Translate Pollen Protocol event to generic WebSocket message
   */
  static translatePollenToWebSocket(event: PollenEvent): WebSocketMessage {
    const messageType = event.event_type
      .replace('_received', '')
      .replace('websocket_', '')
      .replace('chat_', '')
      .replace('sacred_aggregator_', 'aggregator_')

    return {
      type: messageType,
      data: event.payload,
      timestamp: event.timestamp,
      id: event.event_id
    }
  }

  /**
   * Create synaptic message for neural network transmission
   */
  static createSynapticMessage(
    neurotransmitter: string,
    payload: Record<string, unknown>,
    voltage: number = 8.0,
    sourceNeuron: string = 'chat_translator',
    targetNeuron: string = 'hive_network'
  ): SynapticMessage {
    return {
      id: `syn_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      neurotransmitter,
      payload,
      voltage,
      timestamp: new Date().toISOString(),
      sourceNeuron,
      targetNeuron
    }
  }

  /**
   * Batch translate multiple WebSocket messages to Pollen events
   */
  static batchTranslateWebSocketToPollen(messages: WebSocketMessage[]): PollenEvent[] {
    return messages.map(message => this.translateWebSocketToPollen(message))
  }

  /**
   * Batch translate multiple Pollen events to WebSocket messages
   */
  static batchTranslatePollenToWebSocket(events: PollenEvent[]): WebSocketMessage[] {
    return events.map(event => this.translatePollenToWebSocket(event))
  }

  /**
   * Validate Pollen Protocol event structure
   */
  static validatePollenEvent(event: PollenEvent): boolean {
    const requiredFields = ['event_id', 'event_type', 'version', 'timestamp', 'aggregate_id', 'payload']
    
    for (const field of requiredFields) {
      if (!(field in event) || event[field as keyof PollenEvent] === undefined) {
        return false
      }
    }

    // Validate event_type is past-tense
    if (!event.event_type.endsWith('ed') && 
        !event.event_type.endsWith('en') && 
        !event.event_type.endsWith('ted') &&
        !event.event_type.endsWith('ied') &&
        !event.event_type.endsWith('ued')) {
      console.warn(`Event type '${event.event_type}' should be past-tense`)
    }

    return true
  }

  /**
   * Validate WebSocket message structure
   */
  static validateWebSocketMessage(message: WebSocketMessage): boolean {
    return typeof message.type === 'string' && 
           typeof message.data === 'object' && 
           message.data !== null
  }

  /**
   * Get translation statistics
   */
  static getTranslationStats(): Record<string, unknown> {
    return {
      supported_chat_message_types: Object.keys(this.CHAT_EVENT_TYPES).filter(key => 
        key.includes('message') || key.includes('response')
      ),
      supported_chat_event_types: Object.keys(this.CHAT_EVENT_TYPES).filter(key => 
        key.includes('joined') || key.includes('left') || key.includes('typing')
      ),
      supported_aggregator_types: Object.keys(this.CHAT_EVENT_TYPES).filter(key => 
        key.includes('aggregator') || key.includes('ionic') || key.includes('lattice')
      ),
      total_supported_translations: Object.keys(this.CHAT_EVENT_TYPES).length,
      pollen_protocol_version: '1.0',
      websocket_compatibility: 'full'
    }
  }

  // Private helper methods

  private static extractChatMessageType(eventType: string): ChatMessage['type'] | null {
    if (eventType.includes('chat_message')) return 'user_message'
    if (eventType.includes('system_notification')) return 'system_message'
    if (eventType.includes('ai_response')) return 'ai_response'
    if (eventType.includes('status_update')) return 'status_update'
    return null
  }

  private static extractChatEventType(eventType: string): ChatEvent['type'] | null {
    if (eventType.includes('user_joined')) return 'user_joined'
    if (eventType.includes('user_left')) return 'user_left'
    if (eventType.includes('typing_started')) return 'typing_started'
    if (eventType.includes('typing_stopped')) return 'typing_stopped'
    return null
  }
}

/**
 * Factory function for creating chat protocol translator instances
 */
export function createChatProtocolTranslator(): ChatProtocolTranslator {
  return new ChatProtocolTranslator()
}

/**
 * Type guards for chat protocol types
 */
export function isChatMessage(data: unknown): data is ChatMessage {
  return typeof data === 'object' && 
         data !== null && 
         'id' in data && 
         'type' in data && 
         'content' in data && 
         'userId' in data
}

export function isChatEvent(data: unknown): data is ChatEvent {
  return typeof data === 'object' && 
         data !== null && 
         'type' in data && 
         'userId' in data && 
         'timestamp' in data
}

export function isAggregatorUpdate(data: unknown): data is AggregatorUpdate {
  return typeof data === 'object' && 
         data !== null && 
         'aggregatorId' in data && 
         'action' in data && 
         'elements' in data
}