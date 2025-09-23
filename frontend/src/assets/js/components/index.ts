/**
 * ATCG Component Library - Main Entry Point
 * 
 * Pure component library following ATCG architectural principles.
 * Provides organized, reusable components for the Hive ecosystem.
 */

// Export all ATCG component categories
export * from './aggregate'
export * from './transformation'
export * from './connector'
export * from './genesis'

// Main ATCG component types
export type ATCGComponentType = 'aggregate' | 'transformation' | 'connector' | 'genesis'

// Universal component interface
export interface ATCGComponent {
  readonly type: ATCGComponentType
  readonly purpose: string
  readonly id: string
  initialize(): Promise<void>
  destroy(): Promise<void>
  getStatus(): Record<string, any>
}

// Component registry for managing ATCG components
export class ATCGComponentRegistry {
  private components = new Map<string, ATCGComponent>()

  register(id: string, component: ATCGComponent): void {
    this.components.set(id, component)
  }

  unregister(id: string): void {
    this.components.delete(id)
  }

  get(id: string): ATCGComponent | undefined {
    return this.components.get(id)
  }

  getByType(type: ATCGComponentType): ATCGComponent[] {
    return Array.from(this.components.values()).filter(c => c.type === type)
  }

  async initializeAll(): Promise<void> {
    await Promise.all(
      Array.from(this.components.values()).map(c => c.initialize())
    )
  }

  async destroyAll(): Promise<void> {
    await Promise.all(
      Array.from(this.components.values()).map(c => c.destroy())
    )
  }

  getSystemStatus(): Record<string, any> {
    const status: Record<string, any> = {}
    for (const [id, component] of this.components) {
      status[id] = component.getStatus()
    }
    return status
  }
}

// Global registry instance
export const atcgRegistry = new ATCGComponentRegistry()