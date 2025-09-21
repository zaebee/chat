/**
 * C (Connector) Components - Communication & Interfaces
 * 
 * Components that handle communication, APIs, protocols, and external interfaces.
 * These components embody the "C" principle of ATCG architecture.
 */

// Re-export all connector components
export * from './APIConnector'
export * from './WebSocketHandler'
export * from './ProtocolManager'

// Type definitions for connector components
export interface ConnectorComponent {
  readonly type: 'connector'
  readonly purpose: string
  connect(): Promise<void>
  disconnect(): Promise<void>
  send(data: any): Promise<any>
  receive(): Promise<any>
}

// Connector component factory
export function createConnectorComponent(type: string, config: any): ConnectorComponent {
  switch (type) {
    case 'api':
      return new APIConnector(config)
    case 'websocket':
      return new WebSocketHandler(config)
    case 'protocol':
      return new ProtocolManager(config)
    default:
      throw new Error(`Unknown connector component type: ${type}`)
  }
}