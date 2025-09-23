/**
 * DataAggregator - Pure data organization implementation
 * 
 * Provides structural organization and aggregation capabilities
 * without metaphorical terminology.
 */

import type { AggregateComponent } from './index'

// Data types
export interface DataItem {
  readonly id: string
  readonly priority: number
  readonly data: any
}

export interface DataConnection {
  readonly source: string
  readonly target: string
  readonly strength: number
}

export interface DataStructure {
  readonly items: DataItem[]
  readonly connections: DataConnection[]
  readonly organizationScore: number
  readonly stability: number
  readonly structureType: 'ordered' | 'unordered' | 'optimized'
}

export interface AggregationResult {
  readonly original: DataItem[]
  readonly aggregated: DataStructure
  readonly timestamp: string
}

export interface AggregationOutput {
  readonly aggregation_result: AggregationResult
  readonly [key: string]: unknown
}

/**
 * DataAggregator - Pure data organization implementation
 */
export class DataAggregator implements AggregateComponent {
  readonly type = 'aggregate' as const
  readonly purpose = 'Data aggregation for structural organization'
  readonly id: string

  // Configuration constants
  private static readonly OPTIMIZATION_RATIO = 1.618 // Golden ratio for optimization
  private static readonly MIN_CONNECTION_STRENGTH = 0.1 // Minimum connection strength
  private static readonly MAX_CONNECTION_STRENGTH = 1.0 // Maximum connection strength
  private static readonly OPTIMIZATION_FREQUENCIES = [1, 2, 3, 5, 8, 13, 21] // Optimization patterns

  constructor(id: string) {
    this.id = id
  }

  /**
   * Organize data into structured format
   */
  organizeData(items: any[]): AggregationOutput {
    const dataItems = this.convertToDataItems(items)
    const connections = this.calculateConnections(dataItems)
    const organizationScore = this.calculateOrganizationScore(connections)
    const structureType = this.determineStructureType(dataItems, connections)
    const stability = this.calculateStability(connections, organizationScore)

    const structure: DataStructure = {
      items: dataItems,
      connections,
      organizationScore,
      stability,
      structureType
    }

    const result: AggregationResult = {
      original: dataItems,
      aggregated: structure,
      timestamp: new Date().toISOString()
    }

    return {
      aggregation_result: result
    }
  }

  /**
   * Convert raw items to DataItem format
   */
  private convertToDataItems(items: any[]): DataItem[] {
    return items.map((item, index) => ({
      id: item.id || `item_${index}`,
      priority: typeof item.priority === 'number' ? item.priority : index,
      data: item
    }))
  }

  /**
   * Calculate connections between data items
   */
  private calculateConnections(items: DataItem[]): DataConnection[] {
    const connections: DataConnection[] = []

    for (let i = 0; i < items.length; i++) {
      for (let j = i + 1; j < items.length; j++) {
        const distance = Math.abs(items[i].priority - items[j].priority)
        const strength = this.calculateConnectionStrength(items[i], items[j], distance)
        
        if (strength > DataAggregator.MIN_CONNECTION_STRENGTH) {
          connections.push({
            source: items[i].id,
            target: items[j].id,
            strength
          })
        }
      }
    }

    return connections
  }

  /**
   * Calculate connection strength between two items
   */
  private calculateConnectionStrength(item1: DataItem, item2: DataItem, distance: number): number {
    const baseStrength = DataAggregator.MIN_CONNECTION_STRENGTH
    const priorityFactor = Math.abs(item1.priority * item2.priority) / distance
    const scaleFactor = 0.1 // Scale factor for normalization
    
    const strength = baseStrength + (priorityFactor * scaleFactor)
    return Math.min(strength, DataAggregator.MAX_CONNECTION_STRENGTH)
  }

  /**
   * Calculate organization score
   */
  private calculateOrganizationScore(connections: DataConnection[]): number {
    if (connections.length === 0) return 0
    
    const totalStrength = connections.reduce((sum, conn) => sum + conn.strength, 0)
    const averageStrength = totalStrength / connections.length
    const optimizationFactor = DataAggregator.OPTIMIZATION_RATIO
    
    return averageStrength * optimizationFactor
  }

  /**
   * Determine structure type based on organization
   */
  private determineStructureType(items: DataItem[], connections: DataConnection[]): 'ordered' | 'unordered' | 'optimized' {
    if (connections.length === 0) return 'unordered'
    
    const connectionDensity = connections.length / items.length
    const averageStrength = connections.reduce((sum, conn) => sum + conn.strength, 0) / connections.length
    
    // Thresholds for structure classification
    const ORDERED_DENSITY = 2.0 // High connection density
    const ORDERED_STRENGTH = 0.6 // High average strength
    
    if (connectionDensity >= ORDERED_DENSITY && averageStrength >= ORDERED_STRENGTH) {
      return 'ordered'
    } else if (this.hasOptimizationPattern(items)) {
      return 'optimized'
    } else {
      return 'unordered'
    }
  }

  /**
   * Check for optimization pattern in items
   */
  private hasOptimizationPattern(items: DataItem[]): boolean {
    if (items.length < 3) return false
    
    // Check if item priorities follow optimization ratios
    const priorities = items.map(item => item.priority).sort((a, b) => a - b)
    
    // Avoid division by zero
    if (priorities[0] === 0) return false
    
    const OPTIMIZATION_TOLERANCE = 0.1 // ±10% tolerance
    
    for (let i = 1; i < priorities.length; i++) {
      const ratio = priorities[i] / priorities[0]
      const isOptimal = DataAggregator.OPTIMIZATION_FREQUENCIES.some(freq => 
        Math.abs(ratio - freq) < OPTIMIZATION_TOLERANCE
      )
      if (!isOptimal) return false
    }
    
    return true
  }

  /**
   * Calculate structural stability
   */
  private calculateStability(connections: DataConnection[], organizationScore: number): number {
    if (connections.length === 0) return 0
    
    const scorePerConnection = organizationScore / connections.length
    
    // Stability thresholds
    const STABILITY_MIN = 0.2 // Minimum stability threshold
    const STABILITY_MAX = 2.0 // Maximum stability threshold
    
    const normalizedStability = (scorePerConnection - STABILITY_MIN) / 
                               (STABILITY_MAX - STABILITY_MIN)
    
    return Math.min(1.0, Math.max(0, normalizedStability))
  }

  /**
   * Validate structural integrity
   */
  validateStructuralIntegrity(structure: DataStructure): boolean {
    const dataConsistency = this.validateDataConsistency(structure.items)
    const structureStability = structure.stability >= 0.5 // Minimum 50% stability
    return dataConsistency && structureStability
  }

  /**
   * Validate data consistency
   */
  private validateDataConsistency(items: DataItem[]): boolean {
    return items.every(item => 
      item.id && 
      typeof item.priority === 'number' && 
      item.priority >= 0
    )
  }

  // Required AggregateComponent interface methods
  
  aggregate(data: any[]): AggregationOutput {
    return this.organizeData(data)
  }

  process(data: any): any {
    return this.aggregate([data])
  }

  initialize(): Promise<void> {
    return Promise.resolve()
  }

  destroy(): Promise<void> {
    return Promise.resolve()
  }

  getStatus(): Record<string, any> {
    return {
      type: this.type,
      purpose: this.purpose,
      id: this.id,
      status: 'active'
    }
  }
}