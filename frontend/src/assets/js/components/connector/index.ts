/**
 * C (Connector) Components - Communication & Interfaces
 * 
 * Components that handle communication, APIs, protocols, and external interfaces.
 * These components embody the "C" principle of ATCG architecture.
 */

// Connector implementations
export * from './SacredConnector'
export * from './HiveEventBridge'

// Pure connector implementation
export { 
  DataConnector, 
  createDataConnector, 
  isDataConnector,
  type ConnectorOutput,
  type ValidationRules as ConnectorValidationRules,
  type SystemMetrics as ConnectorSystemMetrics
} from './DataConnector'

// Type definitions for connector components
export interface ConnectorComponent {
  readonly type: 'connector'
  readonly purpose: string
  readonly id: string
  connect(): Promise<void>
  disconnect(): Promise<void>
  send(data: unknown): Promise<unknown>
  receive(): Promise<unknown>
  getStatus(): Record<string, unknown>
}

// Connector component types
export type ConnectorComponentType = 'sacred' | 'data_connector' | 'websocket' | 'api' | 'protocol'

// Connector component factory
export async function createConnectorComponent(
  type: ConnectorComponentType, 
  config: { id: string; [key: string]: unknown }
): Promise<ConnectorComponent> {
  switch (type) {
    case 'sacred':
      // Import and create SacredConnector
      const { createSacredConnector } = await import('./SacredConnector')
      return createSacredConnector(config)
    
    case 'data_connector':
      // Import and create DataConnector
      const { createDataConnector } = await import('./DataConnector')
      return createDataConnector(config)
    
    case 'websocket':
    case 'api':
    case 'protocol':
      // Future connector implementations
      return {
        type: 'connector',
        purpose: `${type} connector component`,
        id: config.id,
        connect: async () => console.log(`Connecting ${type}`),
        disconnect: async () => console.log(`Disconnecting ${type}`),
        send: async (data: unknown) => data,
        receive: async () => ({}),
        getStatus: () => ({ type, id: config.id, status: 'placeholder' })
      }
    
    default:
      // Exhaustive checking pattern for type safety
      const _exhaustiveCheck: never = type
      throw new Error(`Unknown connector type: ${_exhaustiveCheck}`)
  }
}