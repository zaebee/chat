/**
 * HexaProcessor - Hexagonal Paradigm Processing System
 * 
 * Implements flexible transformation network following
 * the hexagonal (adaptive) paradigm from the prototype wisdom.
 * Embodies AlgoGenesis 1:7 (Layer Abstraction) principles.
 */

import type { TransformationComponent } from './index'

export interface HexaNode {
  readonly id: string
  readonly label: string
  readonly connections: string[]
  readonly transformFunc?: (data: any) => Promise<any>
  readonly adaptive: boolean
  readonly metadata: Record<string, any>
}

export interface ProcessingResult {
  readonly data: any
  readonly nodesVisited: string[]
  readonly transformationsApplied: number
  readonly processingTime: number
  readonly networkPath: string[]
}

export interface NetworkTopology {
  readonly nodes: Record<string, HexaNode>
  readonly connections: Array<[string, string]>
  readonly entryPoints: string[]
  readonly exitPoints: string[]
}

/**
 * HexaProcessor implements flexible transformation following hexagonal paradigm
 */
export class HexaProcessor implements TransformationComponent {
  readonly type = 'transformation' as const
  readonly purpose = 'Hexagonal paradigm adaptive processing'
  readonly id: string

  private nodes = new Map<string, HexaNode>()
  private activeConnections = new Set<string>()
  private transformationFunctions = new Map<string, (data: any) => Promise<any>>()

  constructor(id: string) {
    this.id = id
    this.initializeBuiltInTransformations()
  }

  /**
   * Add node to hexagonal network
   */
  addNode(node: HexaNode): void {
    this.nodes.set(node.id, node)
    
    // Register transformation function if provided
    if (node.transformFunc) {
      this.transformationFunctions.set(node.id, node.transformFunc)
    }
  }

  /**
   * Create bidirectional connection between nodes
   */
  connectNodes(node1Id: string, node2Id: string): void {
    if (this.nodes.has(node1Id) && this.nodes.has(node2Id)) {
      const connectionKey = [node1Id, node2Id].sort().join('↔')
      this.activeConnections.add(connectionKey)
      
      // Update node connections
      const node1 = this.nodes.get(node1Id)!
      const node2 = this.nodes.get(node2Id)!
      
      if (!node1.connections.includes(node2Id)) {
        node1.connections.push(node2Id)
      }
      if (!node2.connections.includes(node1Id)) {
        node2.connections.push(node1Id)
      }
    }
  }

  /**
   * Transform data through hexagonal network
   */
  async transform(input: any): Promise<any> {
    const entryNodes = this.getEntryNodes()
    
    if (entryNodes.length === 0) {
      return input
    }

    // Process through first available entry node
    const result = await this.processFromNode(input, entryNodes[0])
    
    return {
      ...result.data,
      hexa_processing: {
        processed: true,
        timestamp: new Date().toISOString(),
        nodes_visited: result.nodesVisited,
        transformations_applied: result.transformationsApplied,
        processing_time_ms: result.processingTime,
        network_path: result.networkPath
      }
    }
  }

  /**
   * Process data starting from specific node
   */
  async processFromNode(data: any, entryNodeId: string): Promise<ProcessingResult> {
    const startTime = performance.now()
    const visited = new Set<string>()
    const networkPath: string[] = []
    let transformationsApplied = 0
    let currentData = { ...data }

    const processNode = async (nodeId: string): Promise<void> => {
      if (visited.has(nodeId)) return

      visited.add(nodeId)
      networkPath.push(nodeId)

      const node = this.nodes.get(nodeId)
      if (!node) return

      // Apply transformation if available
      const transformFunc = this.transformationFunctions.get(nodeId)
      if (transformFunc) {
        currentData = await transformFunc(currentData)
        transformationsApplied++
      }

      // Process connected nodes if adaptive
      if (node.adaptive) {
        for (const connectedId of node.connections) {
          if (!visited.has(connectedId)) {
            await processNode(connectedId)
          }
        }
      }
    }

    await processNode(entryNodeId)

    const endTime = performance.now()

    return {
      data: currentData,
      nodesVisited: Array.from(visited),
      transformationsApplied,
      processingTime: endTime - startTime,
      networkPath
    }
  }

  /**
   * Process data with enhanced network analysis
   */
  async process(data: any): Promise<any> {
    const topology = this.getNetworkTopology()
    const results: ProcessingResult[] = []

    // Process through all entry points for comprehensive transformation
    for (const entryPoint of topology.entryPoints) {
      const result = await this.processFromNode(data, entryPoint)
      results.push(result)
    }

    // Merge results from all processing paths
    const mergedData = this.mergeProcessingResults(data, results)

    return {
      ...mergedData,
      hexa_network_analysis: {
        topology,
        processing_results: results.map(r => ({
          entry_point: r.networkPath[0],
          nodes_visited: r.nodesVisited.length,
          transformations: r.transformationsApplied,
          processing_time: r.processingTime
        }))
      }
    }
  }

  /**
   * Get network topology information
   */
  private getNetworkTopology(): NetworkTopology {
    const connections: Array<[string, string]> = []
    
    for (const connectionKey of this.activeConnections) {
      const [node1, node2] = connectionKey.split('↔')
      connections.push([node1, node2])
    }

    return {
      nodes: Object.fromEntries(this.nodes),
      connections,
      entryPoints: this.getEntryNodes(),
      exitPoints: this.getExitNodes()
    }
  }

  /**
   * Get entry nodes (nodes with no incoming connections or marked as entry)
   */
  private getEntryNodes(): string[] {
    const allNodes = Array.from(this.nodes.keys())
    const hasIncoming = new Set<string>()

    // Find nodes with incoming connections
    for (const [node1, node2] of this.getConnectionPairs()) {
      hasIncoming.add(node2)
    }

    // Entry nodes are those without incoming connections or explicitly marked
    return allNodes.filter(nodeId => {
      const node = this.nodes.get(nodeId)!
      return !hasIncoming.has(nodeId) || node.metadata.isEntry === true
    })
  }

  /**
   * Get exit nodes (nodes with no outgoing connections or marked as exit)
   */
  private getExitNodes(): string[] {
    const allNodes = Array.from(this.nodes.keys())
    const hasOutgoing = new Set<string>()

    // Find nodes with outgoing connections
    for (const [node1, node2] of this.getConnectionPairs()) {
      hasOutgoing.add(node1)
    }

    // Exit nodes are those without outgoing connections or explicitly marked
    return allNodes.filter(nodeId => {
      const node = this.nodes.get(nodeId)!
      return !hasOutgoing.has(nodeId) || node.metadata.isExit === true
    })
  }

  /**
   * Get connection pairs from active connections
   */
  private getConnectionPairs(): Array<[string, string]> {
    return Array.from(this.activeConnections).map(key => {
      const [node1, node2] = key.split('↔')
      return [node1, node2] as [string, string]
    })
  }

  /**
   * Merge results from multiple processing paths
   */
  private mergeProcessingResults(originalData: any, results: ProcessingResult[]): any {
    let mergedData = { ...originalData }

    // Apply transformations from all paths
    for (const result of results) {
      mergedData = { ...mergedData, ...result.data }
    }

    return mergedData
  }

  /**
   * Initialize built-in transformation functions
   */
  private initializeBuiltInTransformations(): void {
    this.transformationFunctions.set('semantic_analyzer', async (data: any) => ({
      ...data,
      semantic_analysis: {
        keywords: this.extractKeywords(data),
        entities: this.extractEntities(data),
        sentiment: this.analyzeSentiment(data)
      }
    }))

    this.transformationFunctions.set('visual_aggregator', async (data: any) => ({
      ...data,
      visual_aggregation: {
        structure: this.analyzeStructure(data),
        hierarchy: this.buildHierarchy(data),
        relationships: this.mapRelationships(data)
      }
    }))

    this.transformationFunctions.set('interconnect_mapper', async (data: any) => ({
      ...data,
      interconnect_mapping: {
        connections: this.mapConnections(data),
        dependencies: this.analyzeDependencies(data),
        flow_patterns: this.identifyFlowPatterns(data)
      }
    }))
  }

  // Helper methods for built-in transformations
  private extractKeywords(data: any): string[] {
    const text = JSON.stringify(data).toLowerCase()
    return ['transformation', 'processing', 'network', 'adaptive'].filter(keyword => 
      text.includes(keyword)
    )
  }

  private extractEntities(data: any): string[] {
    return Object.keys(data).filter(key => typeof data[key] === 'object')
  }

  private analyzeSentiment(data: any): string {
    const text = JSON.stringify(data).toLowerCase()
    const positiveWords = ['success', 'complete', 'valid', 'approved']
    const negativeWords = ['error', 'failed', 'invalid', 'rejected']
    
    const positiveCount = positiveWords.filter(word => text.includes(word)).length
    const negativeCount = negativeWords.filter(word => text.includes(word)).length
    
    if (positiveCount > negativeCount) return 'positive'
    if (negativeCount > positiveCount) return 'negative'
    return 'neutral'
  }

  private analyzeStructure(data: any): Record<string, any> {
    return {
      depth: this.calculateDepth(data),
      breadth: Object.keys(data).length,
      types: this.getValueTypes(data)
    }
  }

  private buildHierarchy(data: any): Record<string, any> {
    const hierarchy: Record<string, any> = {}
    
    for (const [key, value] of Object.entries(data)) {
      if (typeof value === 'object' && value !== null) {
        hierarchy[key] = this.buildHierarchy(value)
      } else {
        hierarchy[key] = typeof value
      }
    }
    
    return hierarchy
  }

  private mapRelationships(data: any): Array<[string, string]> {
    const relationships: Array<[string, string]> = []
    const keys = Object.keys(data)
    
    for (let i = 0; i < keys.length; i++) {
      for (let j = i + 1; j < keys.length; j++) {
        relationships.push([keys[i], keys[j]])
      }
    }
    
    return relationships
  }

  private mapConnections(data: any): Record<string, string[]> {
    const connections: Record<string, string[]> = {}
    
    for (const [key, value] of Object.entries(data)) {
      if (typeof value === 'object' && value !== null) {
        connections[key] = Object.keys(value)
      }
    }
    
    return connections
  }

  private analyzeDependencies(data: any): string[] {
    return Object.keys(data).filter(key => 
      typeof data[key] === 'object' && data[key] !== null
    )
  }

  private identifyFlowPatterns(data: any): string[] {
    const patterns: string[] = []
    
    if ('input' in data && 'output' in data) patterns.push('input-output')
    if ('source' in data && 'target' in data) patterns.push('source-target')
    if ('request' in data && 'response' in data) patterns.push('request-response')
    
    return patterns
  }

  private calculateDepth(obj: any): number {
    if (typeof obj !== 'object' || obj === null) return 0
    
    let maxDepth = 0
    for (const value of Object.values(obj)) {
      maxDepth = Math.max(maxDepth, this.calculateDepth(value))
    }
    
    return maxDepth + 1
  }

  private getValueTypes(obj: any): Record<string, number> {
    const types: Record<string, number> = {}
    
    for (const value of Object.values(obj)) {
      const type = typeof value
      types[type] = (types[type] || 0) + 1
    }
    
    return types
  }

  /**
   * Component lifecycle methods
   */
  async initialize(): Promise<void> {
    console.log(`🔧 HexaProcessor ${this.id} initialized with ${this.nodes.size} nodes`)
  }

  async destroy(): Promise<void> {
    this.nodes.clear()
    this.activeConnections.clear()
    this.transformationFunctions.clear()
    console.log(`🧹 HexaProcessor ${this.id} destroyed`)
  }

  getStatus(): Record<string, any> {
    return {
      type: this.type,
      purpose: this.purpose,
      id: this.id,
      nodes: this.nodes.size,
      connections: this.activeConnections.size,
      transformationFunctions: this.transformationFunctions.size,
      topology: this.getNetworkTopology()
    }
  }
}