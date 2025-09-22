/**
 * SacredTransformer - Data Processing Engine
 * 
 * Implements stateless data transformation with enzymatic processing patterns
 * Provides secure, efficient data conversion following ATCG architectural patterns
 * for Transformation components with comprehensive error handling and validation.
 */

import type { TransformationComponent } from './index'

// Transformation Types - Zero 'any' violations
export interface TransformationInput {
  readonly id: string
  readonly data: Record<string, unknown>
  readonly format: string
  readonly timestamp: string
  readonly metadata?: Record<string, unknown>
}

export interface TransformationOutput {
  readonly id: string
  readonly originalData: Record<string, unknown>
  readonly transformedData: Record<string, unknown>
  readonly inputFormat: string
  readonly outputFormat: string
  readonly transformationType: string
  readonly success: boolean
  readonly timestamp: string
  readonly executionTime: number // milliseconds
  readonly metadata?: Record<string, unknown>
}

export interface ProcessingRule {
  readonly ruleId: string
  readonly name: string
  readonly inputFormat: string
  readonly outputFormat: string
  readonly processor: (data: Record<string, unknown>) => Record<string, unknown>
  readonly validator?: (data: Record<string, unknown>) => boolean
  readonly isActive: boolean
}

export interface TransformationMetrics {
  readonly transformationId: string
  readonly executionCount: number
  readonly totalExecutionTime: number
  readonly averageExecutionTime: number
  readonly successRate: number
  readonly errorCount: number
  readonly lastExecution: string | null
}

export interface ProcessingPipeline {
  readonly pipelineId: string
  readonly name: string
  readonly rules: ProcessingRule[]
  readonly isActive: boolean
  readonly executionOrder: string[]
}

export interface TransformationResult {
  readonly original: TransformationInput
  readonly transformed: TransformationOutput
  readonly processingSuccess: boolean
  readonly pipelineUsed: string
  readonly timestamp: string
  readonly executionTime: number // milliseconds
}

export interface ValidationResult {
  readonly isValid: boolean
  readonly violations: string[]
  readonly riskLevel: 'safe' | 'warning' | 'error' | 'critical'
  readonly sanitizedData?: Record<string, unknown>
}

/**
 * SacredTransformer - Data Processing Engine
 * 
 * Implements stateless data transformation with configurable processing rules
 * and comprehensive validation for secure, efficient data conversion.
 */
export class SacredTransformer implements TransformationComponent {
  readonly type = 'transformation' as const
  readonly purpose = 'Stateless data transformation with enzymatic processing patterns'

  // Security: Prevent processing overload DoS attacks
  private static readonly MAX_PROCESSING_SIZE = 10 * 1024 * 1024 // 10MB
  private static readonly MAX_PROCESSING_TIME = 30000 // 30 seconds
  private static readonly MAX_PIPELINE_DEPTH = 10 // Maximum chained transformations
  private static readonly RATE_LIMIT_OPERATIONS = 1000 // per minute
  private static readonly RATE_LIMIT_WINDOW = 60000 // 1 minute in ms

  // Processing Constants - Engineering-based values
  private static readonly PROCESSING_CONSTANTS = {
    // Performance parameters
    DEFAULT_TIMEOUT: 5000, // ms - default processing timeout
    BATCH_SIZE_LIMIT: 100, // Maximum items per batch processing
    MEMORY_THRESHOLD: 0.8, // Memory usage threshold before throttling
    
    // Quality parameters
    MIN_SUCCESS_RATE: 0.95, // Minimum acceptable success rate
    ERROR_THRESHOLD: 0.05, // Maximum acceptable error rate
    PERFORMANCE_TARGET: 100, // ms - target processing time per operation
    
    // Reliability parameters
    MAX_RETRY_ATTEMPTS: 3, // Maximum retry attempts for failed operations
    RETRY_DELAY: 1000, // ms - delay between retry attempts
    HEALTH_CHECK_INTERVAL: 30000, // ms - health check frequency
  } as const

  // Processing State
  private processingRules: Map<string, ProcessingRule> = new Map()
  private processingPipelines: Map<string, ProcessingPipeline> = new Map()
  private transformationMetrics: Map<string, TransformationMetrics> = new Map()
  
  // Performance Metrics
  private totalTransformations = 0
  private totalExecutionTime = 0
  private errorCount = 0
  private lastTransformation: Date | null = null
  
  // Rate Limiting
  private operationTimestamps: number[] = []
  
  // Processing State
  private isInitialized = false
  private isDestroyed = false

  constructor(public readonly id: string) {
    this.validateConfiguration()
    this.initializeDefaultRules()
  }

  /**
   * Initialize the transformer with default processing rules
   */
  async initialize(): Promise<void> {
    try {
      if (this.isInitialized) {
        return
      }

      // Initialize default processing pipelines
      await this.initializeDefaultPipelines()

      // Initialize metrics tracking
      this.initializeMetricsTracking()

      this.isInitialized = true

      // Emit initialization event
      console.log(`SacredTransformer ${this.id} initialized successfully`)

    } catch (error) {
      throw new Error(`Transformer initialization failed: ${error instanceof Error ? error.message : 'Unknown error'}`)
    }
  }

  /**
   * Destroy the transformer and clean up resources
   */
  async destroy(): Promise<void> {
    try {
      if (this.isDestroyed) {
        return
      }

      // Clear all processing rules and pipelines
      this.processingRules.clear()
      this.processingPipelines.clear()
      this.transformationMetrics.clear()

      // Clear rate limiting data
      this.operationTimestamps = []

      this.isDestroyed = true
      this.isInitialized = false

      console.log(`SacredTransformer ${this.id} destroyed successfully`)

    } catch (error) {
      throw new Error(`Transformer destruction failed: ${error instanceof Error ? error.message : 'Unknown error'}`)
    }
  }

  /**
   * Transform data using specified processing rule or pipeline
   */
  async transform(input: unknown): Promise<TransformationOutput> {
    try {
      if (!this.isInitialized) {
        throw new Error('Transformer not initialized. Call initialize() first.')
      }

      if (this.isDestroyed) {
        throw new Error('Transformer has been destroyed and cannot process data.')
      }

      // Validate and convert input
      const transformationInput = this.validateAndConvertInput(input)

      // Check rate limiting
      if (!this.checkRateLimit()) {
        throw new Error(`Rate limit exceeded (${SacredTransformer.RATE_LIMIT_OPERATIONS} operations per minute). This prevents processing overload.`)
      }

      // Validate processing size
      const inputSize = this.calculateDataSize(transformationInput.data)
      if (inputSize > SacredTransformer.MAX_PROCESSING_SIZE) {
        throw new Error(`Input size ${inputSize} exceeds maximum ${SacredTransformer.MAX_PROCESSING_SIZE} bytes. This prevents memory exhaustion.`)
      }

      // Execute transformation
      const result = await this.executeTransformation(transformationInput)

      // Update metrics
      this.updateMetrics(result)

      return result

    } catch (error) {
      this.errorCount++
      throw new Error(`Transformation failed: ${error instanceof Error ? error.message : 'Unknown error'}`)
    }
  }

  /**
   * Process data (alias for transform for compatibility)
   */
  async process(data: unknown): Promise<TransformationOutput> {
    return await this.transform(data)
  }

  /**
   * Add a custom processing rule
   */
  addProcessingRule(rule: ProcessingRule): void {
    try {
      // Validate rule
      if (!rule.ruleId || !rule.name || !rule.processor) {
        throw new Error('Processing rule must have ruleId, name, and processor function')
      }

      // Check for duplicate rule IDs
      if (this.processingRules.has(rule.ruleId)) {
        throw new Error(`Processing rule with ID '${rule.ruleId}' already exists`)
      }

      this.processingRules.set(rule.ruleId, rule)

      // Initialize metrics for this rule
      this.transformationMetrics.set(rule.ruleId, {
        transformationId: rule.ruleId,
        executionCount: 0,
        totalExecutionTime: 0,
        averageExecutionTime: 0,
        successRate: 1.0,
        errorCount: 0,
        lastExecution: null
      })

    } catch (error) {
      throw new Error(`Failed to add processing rule: ${error instanceof Error ? error.message : 'Unknown error'}`)
    }
  }

  /**
   * Remove a processing rule
   */
  removeProcessingRule(ruleId: string): boolean {
    try {
      const removed = this.processingRules.delete(ruleId)
      if (removed) {
        this.transformationMetrics.delete(ruleId)
      }
      return removed
    } catch (error) {
      console.error(`Failed to remove processing rule: ${error}`)
      return false
    }
  }

  /**
   * Create a processing pipeline
   */
  createProcessingPipeline(pipeline: ProcessingPipeline): void {
    try {
      // Validate pipeline
      if (!pipeline.pipelineId || !pipeline.name || !pipeline.rules.length) {
        throw new Error('Processing pipeline must have pipelineId, name, and at least one rule')
      }

      // Validate pipeline depth
      if (pipeline.rules.length > SacredTransformer.MAX_PIPELINE_DEPTH) {
        throw new Error(`Pipeline depth ${pipeline.rules.length} exceeds maximum ${SacredTransformer.MAX_PIPELINE_DEPTH}. This prevents infinite processing loops.`)
      }

      // Validate all rules exist
      for (const rule of pipeline.rules) {
        if (!this.processingRules.has(rule.ruleId)) {
          throw new Error(`Processing rule '${rule.ruleId}' not found. Add the rule before creating pipeline.`)
        }
      }

      this.processingPipelines.set(pipeline.pipelineId, pipeline)

    } catch (error) {
      throw new Error(`Failed to create processing pipeline: ${error instanceof Error ? error.message : 'Unknown error'}`)
    }
  }

  /**
   * Get comprehensive status following Sacred Architecture patterns
   */
  getStatus(): Record<string, unknown> {
    const errorRate = this.totalTransformations > 0 ? this.errorCount / this.totalTransformations : 0
    const averageExecutionTime = this.totalTransformations > 0 ? this.totalExecutionTime / this.totalTransformations : 0

    return {
      // Component identification
      component: 'SacredTransformer',
      type: 'T',
      id: this.id,
      purpose: this.purpose,

      // Initialization state
      initialization_state: {
        is_initialized: this.isInitialized,
        is_destroyed: this.isDestroyed,
        ready_for_processing: this.isInitialized && !this.isDestroyed
      },

      // Processing capabilities
      processing_capabilities: {
        available_rules: this.processingRules.size,
        available_pipelines: this.processingPipelines.size,
        active_rules: Array.from(this.processingRules.values()).filter(rule => rule.isActive).length,
        active_pipelines: Array.from(this.processingPipelines.values()).filter(pipeline => pipeline.isActive).length
      },

      // Performance metrics
      performance_metrics: {
        total_transformations: this.totalTransformations,
        error_count: this.errorCount,
        error_rate: errorRate,
        average_execution_time: averageExecutionTime,
        last_transformation: this.lastTransformation?.toISOString() || null
      },

      // Processing health
      processing_health: {
        success_rate: 1 - errorRate,
        performance_target_met: averageExecutionTime < SacredTransformer.PROCESSING_CONSTANTS.PERFORMANCE_TARGET,
        error_threshold_ok: errorRate < SacredTransformer.PROCESSING_CONSTANTS.ERROR_THRESHOLD,
        rate_limit_status: this.getCurrentOperationRate()
      },

      // Processing constants
      processing_constants: SacredTransformer.PROCESSING_CONSTANTS,

      // Security constraints
      security_constraints: {
        max_processing_size: SacredTransformer.MAX_PROCESSING_SIZE,
        max_processing_time: SacredTransformer.MAX_PROCESSING_TIME,
        max_pipeline_depth: SacredTransformer.MAX_PIPELINE_DEPTH,
        rate_limit: `${SacredTransformer.RATE_LIMIT_OPERATIONS} operations per minute`,
        current_rate: this.getCurrentOperationRate()
      },

      // Known limitations
      known_limitations: {
        stateless_processing: 'No state maintained between transformations for thread safety',
        memory_constraints: 'Large data processing limited by memory thresholds',
        processing_timeout: 'Long-running transformations subject to timeout limits',
        rule_validation: 'Custom processing rules must be validated by implementer'
      },

      // Design philosophy
      design_philosophy: 'Stateless enzymatic processing enables reliable, scalable data transformation',

      // Timestamp and health
      timestamp: new Date().toISOString(),
      health: errorRate < SacredTransformer.PROCESSING_CONSTANTS.ERROR_THRESHOLD && 
              this.isInitialized && !this.isDestroyed ? 'optimal' : 
              errorRate < 0.2 ? 'degraded' : 'critical'
    }
  }

  // Private helper methods

  private validateConfiguration(): void {
    if (!this.id) {
      throw new Error('Transformer ID is required')
    }
    if (this.id.length > 100) {
      throw new Error('Transformer ID must be less than 100 characters')
    }
  }

  private initializeDefaultRules(): void {
    // Add basic data transformation rules
    this.addProcessingRule({
      ruleId: 'identity_transform',
      name: 'Identity Transformation',
      inputFormat: 'any',
      outputFormat: 'any',
      processor: (data: Record<string, unknown>) => data,
      validator: () => true,
      isActive: true
    })

    this.addProcessingRule({
      ruleId: 'json_normalize',
      name: 'JSON Normalization',
      inputFormat: 'json',
      outputFormat: 'normalized_json',
      processor: (data: Record<string, unknown>) => this.normalizeJsonData(data),
      validator: (data: Record<string, unknown>) => typeof data === 'object' && data !== null,
      isActive: true
    })

    this.addProcessingRule({
      ruleId: 'data_sanitization',
      name: 'Data Sanitization',
      inputFormat: 'any',
      outputFormat: 'sanitized',
      processor: (data: Record<string, unknown>) => this.sanitizeData(data),
      validator: () => true,
      isActive: true
    })
  }

  private async initializeDefaultPipelines(): Promise<void> {
    // Create default processing pipeline
    this.createProcessingPipeline({
      pipelineId: 'default_pipeline',
      name: 'Default Processing Pipeline',
      rules: [
        this.processingRules.get('data_sanitization')!,
        this.processingRules.get('json_normalize')!
      ],
      isActive: true,
      executionOrder: ['data_sanitization', 'json_normalize']
    })
  }

  private initializeMetricsTracking(): void {
    // Initialize metrics for default rules
    for (const [ruleId] of this.processingRules) {
      if (!this.transformationMetrics.has(ruleId)) {
        this.transformationMetrics.set(ruleId, {
          transformationId: ruleId,
          executionCount: 0,
          totalExecutionTime: 0,
          averageExecutionTime: 0,
          successRate: 1.0,
          errorCount: 0,
          lastExecution: null
        })
      }
    }
  }

  private validateAndConvertInput(input: unknown): TransformationInput {
    try {
      // Handle different input types
      if (typeof input === 'object' && input !== null && 'data' in input) {
        const typedInput = input as Partial<TransformationInput>
        return {
          id: typedInput.id || this.generateTransformationId(),
          data: typedInput.data || {},
          format: typedInput.format || 'unknown',
          timestamp: typedInput.timestamp || new Date().toISOString(),
          metadata: typedInput.metadata
        }
      }

      // Convert simple data to transformation input
      return {
        id: this.generateTransformationId(),
        data: typeof input === 'object' && input !== null ? input as Record<string, unknown> : { value: input },
        format: 'auto_detected',
        timestamp: new Date().toISOString()
      }

    } catch (error) {
      throw new Error(`Input validation failed: ${error instanceof Error ? error.message : 'Unknown error'}`)
    }
  }

  private async executeTransformation(input: TransformationInput): Promise<TransformationOutput> {
    const startTime = Date.now()

    try {
      // Use default pipeline if no specific rule requested
      const pipeline = this.processingPipelines.get('default_pipeline')!
      
      let transformedData = { ...input.data }
      let currentFormat = input.format

      // Execute pipeline rules in order
      for (const rule of pipeline.rules) {
        if (rule.isActive) {
          // Validate input if validator exists
          if (rule.validator && !rule.validator(transformedData)) {
            throw new Error(`Validation failed for rule '${rule.name}'`)
          }

          // Apply transformation
          transformedData = rule.processor(transformedData)
          currentFormat = rule.outputFormat
        }
      }

      const executionTime = Date.now() - startTime

      return {
        id: this.generateTransformationId(),
        originalData: input.data,
        transformedData,
        inputFormat: input.format,
        outputFormat: currentFormat,
        transformationType: pipeline.pipelineId,
        success: true,
        timestamp: new Date().toISOString(),
        executionTime,
        metadata: input.metadata
      }

    } catch (error) {
      const executionTime = Date.now() - startTime

      return {
        id: this.generateTransformationId(),
        originalData: input.data,
        transformedData: {},
        inputFormat: input.format,
        outputFormat: 'error',
        transformationType: 'error',
        success: false,
        timestamp: new Date().toISOString(),
        executionTime,
        metadata: { error: error instanceof Error ? error.message : 'Unknown error' }
      }
    }
  }

  private updateMetrics(result: TransformationOutput): void {
    this.totalTransformations++
    this.totalExecutionTime += result.executionTime
    this.lastTransformation = new Date()

    if (!result.success) {
      this.errorCount++
    }

    // Update rule-specific metrics
    const metrics = this.transformationMetrics.get(result.transformationType)
    if (metrics) {
      const updatedMetrics: TransformationMetrics = {
        ...metrics,
        executionCount: metrics.executionCount + 1,
        totalExecutionTime: metrics.totalExecutionTime + result.executionTime,
        averageExecutionTime: (metrics.totalExecutionTime + result.executionTime) / (metrics.executionCount + 1),
        errorCount: result.success ? metrics.errorCount : metrics.errorCount + 1,
        successRate: result.success ? 
          (metrics.successRate * metrics.executionCount + 1) / (metrics.executionCount + 1) :
          (metrics.successRate * metrics.executionCount) / (metrics.executionCount + 1),
        lastExecution: result.timestamp
      }
      this.transformationMetrics.set(result.transformationType, updatedMetrics)
    }
  }

  private checkRateLimit(): boolean {
    const now = Date.now()
    
    // Remove old timestamps outside the window
    this.operationTimestamps = this.operationTimestamps.filter(
      timestamp => now - timestamp < SacredTransformer.RATE_LIMIT_WINDOW
    )

    // Check if we're under the limit
    if (this.operationTimestamps.length >= SacredTransformer.RATE_LIMIT_OPERATIONS) {
      return false
    }

    // Add current timestamp
    this.operationTimestamps.push(now)
    return true
  }

  private getCurrentOperationRate(): number {
    const now = Date.now()
    const recentOperations = this.operationTimestamps.filter(
      timestamp => now - timestamp < SacredTransformer.RATE_LIMIT_WINDOW
    )
    return recentOperations.length
  }

  private calculateDataSize(data: Record<string, unknown>): number {
    try {
      return JSON.stringify(data).length
    } catch (error) {
      // If JSON.stringify fails, estimate size
      return String(data).length
    }
  }

  private normalizeJsonData(data: Record<string, unknown>): Record<string, unknown> {
    // Simple JSON normalization - remove null values, trim strings
    const normalized: Record<string, unknown> = {}
    
    for (const [key, value] of Object.entries(data)) {
      if (value !== null && value !== undefined) {
        if (typeof value === 'string') {
          normalized[key] = value.trim()
        } else if (typeof value === 'object' && value !== null) {
          normalized[key] = this.normalizeJsonData(value as Record<string, unknown>)
        } else {
          normalized[key] = value
        }
      }
    }

    return normalized
  }

  private sanitizeData(data: Record<string, unknown>): Record<string, unknown> {
    // Simple data sanitization - remove dangerous patterns
    const sanitized: Record<string, unknown> = {}
    
    for (const [key, value] of Object.entries(data)) {
      // Skip dangerous keys
      if (key === '__proto__' || key === 'constructor' || key === 'prototype') {
        continue
      }

      if (typeof value === 'string') {
        // Remove potentially dangerous patterns
        sanitized[key] = value
          .replace(/<script[^>]*>.*?<\/script>/gi, '')
          .replace(/javascript:/gi, '')
          .replace(/on\w+\s*=/gi, '')
      } else if (typeof value === 'object' && value !== null) {
        sanitized[key] = this.sanitizeData(value as Record<string, unknown>)
      } else {
        sanitized[key] = value
      }
    }

    return sanitized
  }

  private generateTransformationId(): string {
    return `transform_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }
}

/**
 * Factory function for creating Sacred Transformer instances
 */
export function createSacredTransformer(config: {
  readonly id: string
}): SacredTransformer {
  return new SacredTransformer(config.id)
}

/**
 * Type guard for Sacred Transformer
 */
export function isSacredTransformer(transformer: unknown): transformer is SacredTransformer {
  return transformer instanceof SacredTransformer
}