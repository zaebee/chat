/**
 * ATCGIntegration - Sacred Component Pipeline Integration
 * 
 * Integrates Sacred Transformer with Sacred Aggregator and Sacred Connector
 * to create complete A→T→C data processing pipelines with type-safe interfaces
 */

import type { SacredTransformer, TransformationInput, TransformationOutput } from './SacredTransformer'
import type { SacredStructure, AggregationResult } from '../aggregate/SacredAggregator'
import type { ConnectorMessage, PollenEvent } from '../connector/SacredConnector'

// Integration Types - Zero 'any' violations
export interface ATCGPipelineConfig {
  readonly pipelineId: string
  readonly name: string
  readonly aggregatorId: string
  readonly transformerId: string
  readonly connectorId: string
  readonly enableAutoProcessing: boolean
  readonly processingTimeout: number
}

export interface AggregatorToTransformerMapping {
  readonly mappingId: string
  readonly aggregatorOutputFormat: string
  readonly transformerInputFormat: string
  readonly conversionRules: Record<string, string>
}

export interface TransformerToConnectorMapping {
  readonly mappingId: string
  readonly transformerOutputFormat: string
  readonly connectorInputFormat: string
  readonly protocolTranslation: 'websocket' | 'pollen' | 'internal'
}

export interface PipelineExecutionResult {
  readonly pipelineId: string
  readonly executionId: string
  readonly aggregationResult: AggregationResult | null
  readonly transformationResult: TransformationOutput | null
  readonly connectorResult: unknown | null
  readonly overallSuccess: boolean
  readonly totalExecutionTime: number
  readonly timestamp: string
  readonly errors: string[]
}

export interface PipelineMetrics {
  readonly pipelineId: string
  readonly executionCount: number
  readonly successCount: number
  readonly errorCount: number
  readonly averageExecutionTime: number
  readonly lastExecution: string | null
  readonly throughput: number // operations per second
}

/**
 * ATCG Pipeline Orchestrator
 * 
 * Orchestrates data flow between Sacred Aggregator, Transformer, and Connector
 * components with comprehensive error handling and performance monitoring.
 */
export class ATCGPipelineOrchestrator {
  private pipelines: Map<string, ATCGPipelineConfig> = new Map()
  private pipelineMetrics: Map<string, PipelineMetrics> = new Map()
  private aggregatorMappings: Map<string, AggregatorToTransformerMapping> = new Map()
  private connectorMappings: Map<string, TransformerToConnectorMapping> = new Map()
  
  // Performance tracking
  private totalExecutions = 0
  private totalExecutionTime = 0
  private errorCount = 0

  constructor(private readonly orchestratorId: string) {}

  /**
   * Register an ATCG processing pipeline
   */
  registerPipeline(config: ATCGPipelineConfig): void {
    try {
      // Validate pipeline configuration
      if (!config.pipelineId || !config.aggregatorId || !config.transformerId || !config.connectorId) {
        throw new Error('Pipeline configuration must include all component IDs')
      }

      // Check for duplicate pipeline IDs
      if (this.pipelines.has(config.pipelineId)) {
        throw new Error(`Pipeline with ID '${config.pipelineId}' already exists`)
      }

      this.pipelines.set(config.pipelineId, config)

      // Initialize metrics for this pipeline
      this.pipelineMetrics.set(config.pipelineId, {
        pipelineId: config.pipelineId,
        executionCount: 0,
        successCount: 0,
        errorCount: 0,
        averageExecutionTime: 0,
        lastExecution: null,
        throughput: 0
      })

    } catch (error) {
      throw new Error(`Failed to register pipeline: ${error instanceof Error ? error.message : 'Unknown error'}`)
    }
  }

  /**
   * Add aggregator to transformer mapping
   */
  addAggregatorMapping(mapping: AggregatorToTransformerMapping): void {
    this.aggregatorMappings.set(mapping.mappingId, mapping)
  }

  /**
   * Add transformer to connector mapping
   */
  addConnectorMapping(mapping: TransformerToConnectorMapping): void {
    this.connectorMappings.set(mapping.mappingId, mapping)
  }

  /**
   * Execute complete A→T→C pipeline
   */
  async executePipeline(
    pipelineId: string,
    aggregator: any, // SacredAggregator instance
    transformer: SacredTransformer,
    connector: any, // SacredConnector instance
    inputData: unknown[]
  ): Promise<PipelineExecutionResult> {
    const startTime = Date.now()
    const executionId = this.generateExecutionId()
    const errors: string[] = []

    let aggregationResult: AggregationResult | null = null
    let transformationResult: TransformationOutput | null = null
    let connectorResult: unknown | null = null

    try {
      const pipeline = this.pipelines.get(pipelineId)
      if (!pipeline) {
        throw new Error(`Pipeline '${pipelineId}' not found`)
      }

      // Step 1: Aggregate data using Sacred Aggregator
      try {
        aggregationResult = await aggregator.aggregate(inputData)
        if (!aggregationResult.structuralIntegrity) {
          errors.push('Aggregation failed: structural integrity check failed')
        }
      } catch (error) {
        errors.push(`Aggregation error: ${error instanceof Error ? error.message : 'Unknown error'}`)
      }

      // Step 2: Transform aggregated data using Sacred Transformer
      if (aggregationResult && aggregationResult.structuralIntegrity) {
        try {
          const transformationInput = this.convertAggregationToTransformation(aggregationResult)
          transformationResult = await transformer.transform(transformationInput)
          
          if (!transformationResult.success) {
            errors.push('Transformation failed: processing error')
          }
        } catch (error) {
          errors.push(`Transformation error: ${error instanceof Error ? error.message : 'Unknown error'}`)
        }
      }

      // Step 3: Send transformed data through Sacred Connector
      if (transformationResult && transformationResult.success) {
        try {
          const connectorMessage = this.convertTransformationToConnector(transformationResult)
          connectorResult = await connector.send(connectorMessage)
        } catch (error) {
          errors.push(`Connector error: ${error instanceof Error ? error.message : 'Unknown error'}`)
        }
      }

      const executionTime = Date.now() - startTime
      const overallSuccess = errors.length === 0

      // Update metrics
      this.updatePipelineMetrics(pipelineId, executionTime, overallSuccess)

      return {
        pipelineId,
        executionId,
        aggregationResult,
        transformationResult,
        connectorResult,
        overallSuccess,
        totalExecutionTime: executionTime,
        timestamp: new Date().toISOString(),
        errors
      }

    } catch (error) {
      const executionTime = Date.now() - startTime
      errors.push(`Pipeline execution error: ${error instanceof Error ? error.message : 'Unknown error'}`)
      
      this.updatePipelineMetrics(pipelineId, executionTime, false)

      return {
        pipelineId,
        executionId,
        aggregationResult,
        transformationResult,
        connectorResult,
        overallSuccess: false,
        totalExecutionTime: executionTime,
        timestamp: new Date().toISOString(),
        errors
      }
    }
  }

  /**
   * Execute batch processing through pipeline
   */
  async executeBatchPipeline(
    pipelineId: string,
    aggregator: any,
    transformer: SacredTransformer,
    connector: any,
    batchData: unknown[][]
  ): Promise<PipelineExecutionResult[]> {
    const results: PipelineExecutionResult[] = []

    for (const inputData of batchData) {
      try {
        const result = await this.executePipeline(pipelineId, aggregator, transformer, connector, inputData)
        results.push(result)
      } catch (error) {
        // Continue processing other batches even if one fails
        results.push({
          pipelineId,
          executionId: this.generateExecutionId(),
          aggregationResult: null,
          transformationResult: null,
          connectorResult: null,
          overallSuccess: false,
          totalExecutionTime: 0,
          timestamp: new Date().toISOString(),
          errors: [`Batch processing error: ${error instanceof Error ? error.message : 'Unknown error'}`]
        })
      }
    }

    return results
  }

  /**
   * Get pipeline status and metrics
   */
  getPipelineStatus(pipelineId: string): Record<string, unknown> {
    const pipeline = this.pipelines.get(pipelineId)
    const metrics = this.pipelineMetrics.get(pipelineId)

    if (!pipeline || !metrics) {
      throw new Error(`Pipeline '${pipelineId}' not found`)
    }

    return {
      pipeline_config: pipeline,
      pipeline_metrics: metrics,
      aggregator_mappings: Array.from(this.aggregatorMappings.values()),
      connector_mappings: Array.from(this.connectorMappings.values()),
      health: metrics.errorCount / Math.max(1, metrics.executionCount) < 0.1 ? 'healthy' : 'degraded'
    }
  }

  /**
   * Get orchestrator status
   */
  getOrchestratorStatus(): Record<string, unknown> {
    const errorRate = this.totalExecutions > 0 ? this.errorCount / this.totalExecutions : 0
    const averageExecutionTime = this.totalExecutions > 0 ? this.totalExecutionTime / this.totalExecutions : 0

    return {
      component: 'ATCGPipelineOrchestrator',
      orchestrator_id: this.orchestratorId,
      
      pipeline_summary: {
        total_pipelines: this.pipelines.size,
        total_executions: this.totalExecutions,
        error_count: this.errorCount,
        error_rate: errorRate,
        average_execution_time: averageExecutionTime
      },

      registered_pipelines: Array.from(this.pipelines.keys()),
      
      integration_mappings: {
        aggregator_mappings: this.aggregatorMappings.size,
        connector_mappings: this.connectorMappings.size
      },

      health: errorRate < 0.1 ? 'optimal' : errorRate < 0.3 ? 'degraded' : 'critical',
      timestamp: new Date().toISOString()
    }
  }

  // Private helper methods

  private convertAggregationToTransformation(aggregationResult: AggregationResult): TransformationInput {
    return {
      id: this.generateExecutionId(),
      data: {
        aggregated_structure: aggregationResult.aggregated,
        structural_integrity: aggregationResult.structuralIntegrity,
        aggregation_type: aggregationResult.aggregationType,
        original_elements: aggregationResult.original,
        bonds: aggregationResult.aggregated.bonds,
        lattice_energy: aggregationResult.aggregated.latticeEnergy,
        structure_type: aggregationResult.aggregated.structureType
      },
      format: 'aggregation_result',
      timestamp: aggregationResult.timestamp
    }
  }

  private convertTransformationToConnector(transformationResult: TransformationOutput): ConnectorMessage {
    return {
      id: transformationResult.id,
      messageType: 'transformation_result',
      payload: {
        transformed_data: transformationResult.transformedData,
        transformation_type: transformationResult.transformationType,
        execution_time: transformationResult.executionTime,
        input_format: transformationResult.inputFormat,
        output_format: transformationResult.outputFormat
      },
      priority: 7.0, // High priority for transformation results
      timestamp: transformationResult.timestamp,
      sourceId: 'sacred_transformer',
      targetId: 'hive_network'
    }
  }

  private updatePipelineMetrics(pipelineId: string, executionTime: number, success: boolean): void {
    const metrics = this.pipelineMetrics.get(pipelineId)
    if (!metrics) return

    const updatedMetrics: PipelineMetrics = {
      ...metrics,
      executionCount: metrics.executionCount + 1,
      successCount: success ? metrics.successCount + 1 : metrics.successCount,
      errorCount: success ? metrics.errorCount : metrics.errorCount + 1,
      averageExecutionTime: (metrics.averageExecutionTime * metrics.executionCount + executionTime) / (metrics.executionCount + 1),
      lastExecution: new Date().toISOString(),
      throughput: metrics.executionCount / Math.max(1, (Date.now() - new Date(metrics.lastExecution || Date.now()).getTime()) / 1000)
    }

    this.pipelineMetrics.set(pipelineId, updatedMetrics)

    // Update global metrics
    this.totalExecutions++
    this.totalExecutionTime += executionTime
    if (!success) {
      this.errorCount++
    }
  }

  private generateExecutionId(): string {
    return `exec_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }
}

/**
 * Factory function for creating ATCG Pipeline Orchestrator
 */
export function createATCGPipelineOrchestrator(orchestratorId: string): ATCGPipelineOrchestrator {
  return new ATCGPipelineOrchestrator(orchestratorId)
}

/**
 * Type guard for ATCG Pipeline Orchestrator
 */
export function isATCGPipelineOrchestrator(orchestrator: unknown): orchestrator is ATCGPipelineOrchestrator {
  return orchestrator instanceof ATCGPipelineOrchestrator
}

/**
 * Utility functions for common ATCG integrations
 */
export class ATCGIntegrationUtils {
  /**
   * Create standard aggregator to transformer mapping
   */
  static createStandardAggregatorMapping(mappingId: string): AggregatorToTransformerMapping {
    return {
      mappingId,
      aggregatorOutputFormat: 'ionic_structure',
      transformerInputFormat: 'aggregation_result',
      conversionRules: {
        'bonds': 'ionic_bonds',
        'latticeEnergy': 'lattice_energy',
        'structureType': 'structure_type',
        'stability': 'structural_stability'
      }
    }
  }

  /**
   * Create standard transformer to connector mapping
   */
  static createStandardConnectorMapping(mappingId: string, protocol: 'websocket' | 'pollen' | 'internal'): TransformerToConnectorMapping {
    return {
      mappingId,
      transformerOutputFormat: 'processed_data',
      connectorInputFormat: protocol === 'websocket' ? 'websocket_message' : 'pollen_event',
      protocolTranslation: protocol
    }
  }

  /**
   * Validate ATCG pipeline configuration
   */
  static validatePipelineConfig(config: ATCGPipelineConfig): string[] {
    const errors: string[] = []

    if (!config.pipelineId) errors.push('Pipeline ID is required')
    if (!config.name) errors.push('Pipeline name is required')
    if (!config.aggregatorId) errors.push('Aggregator ID is required')
    if (!config.transformerId) errors.push('Transformer ID is required')
    if (!config.connectorId) errors.push('Connector ID is required')
    if (config.processingTimeout <= 0) errors.push('Processing timeout must be positive')

    return errors
  }
}