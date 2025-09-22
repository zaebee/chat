/**
 * C (Connector) Components - Communication & Interfaces
 * 
 * Components that handle communication, APIs, protocols, and external interfaces.
 * These components embody the "C" principle of ATCG architecture.
 */

// Sacred Connector implementations
export * from './SacredConnector'
export * from './HiveEventBridge'

// Type definitions for connector components
export interface ConnectorComponent {
  readonly type: 'connector'
  readonly purpose: string
  connect(): Promise<void>
  disconnect(): Promise<void>
  send(data: unknown): Promise<unknown>
  receive(): Promise<unknown>
}

// Connector component types
export type ConnectorComponentType = 'sacred' | 'websocket' | 'api' | 'protocol'

// Connector component factory
export function createConnectorComponent(
  type: ConnectorComponentType, 
  config: { id: string; [key: string]: unknown }
): ConnectorComponent {
  switch (type) {
    case 'sacred':
      // Import and create SacredConnector
      const { createSacredConnector } = require('./SacredConnector')
      return createSacredConnector(config)
    
    case 'websocket':
    case 'api':
    case 'protocol':
      // Future connector implementations
      return {
        type: 'connector',
        purpose: `${type} connector component`,
        connect: async () => console.log(`Connecting ${type}`),
        disconnect: async () => console.log(`Disconnecting ${type}`),
        send: async (data: unknown) => data,
        receive: async () => ({})
      }
    
    default:
      // Exhaustive checking pattern for type safety
      const exhaustiveCheck: never = type
      throw new Error(`Unknown connector type: ${exhaustiveCheck}`)
  }
}