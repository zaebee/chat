/**
 * A (Aggregate) Components - File Organization & Structure
 * 
 * Components that manage structural organization, layout, and file management.
 * These components embody the "A" principle of ATCG architecture.
 */

// Re-export all aggregate components
export * from './NavigationAggregator'
export * from './LayoutManager'
export * from './AssetOrganizer'

// Type definitions for aggregate components
export interface AggregateComponent {
  readonly type: 'aggregate'
  readonly purpose: string
  organize(): void
  getStructure(): Record<string, any>
}

// Aggregate component factory
export function createAggregateComponent(type: string, config: any): AggregateComponent {
  switch (type) {
    case 'navigation':
      return new NavigationAggregator(config)
    case 'layout':
      return new LayoutManager(config)
    case 'asset':
      return new AssetOrganizer(config)
    default:
      throw new Error(`Unknown aggregate component type: ${type}`)
  }
}