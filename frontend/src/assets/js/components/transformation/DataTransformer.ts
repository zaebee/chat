/**
 * DataTransformer - Pure Data Transformation Component
 * 
 * Implements core data transformation functions for processing operations
 * Following the ATCG architectural pattern for Transform components
 * with pure software terminology and no metaphorical contamination.
 */

import type { TransformationComponent } from './index'

// Pure data types - no metaphorical contamination
export interface DataVector {
  readonly x: number
  readonly y: number
}

export interface TransformationResult {
  readonly original: DataVector
  readonly transformed: DataVector
  readonly validationPassed: boolean
  readonly transformationType: 'data_transform'
  readonly timestamp: string
}

export interface ValidationRules {
  readonly sumConservation: boolean
  readonly dataIntegrity: boolean
  readonly informationPreservation: boolean
  readonly operationConsistency: boolean
}

export interface SystemMetrics {
  readonly complexity_reduction: number     // System complexity reduction
  readonly quality_enhancement: number      // Quality enhancement  
  readonly optimization_improvement: number // Optimization improvement
}

export interface ComponentMapping {
  readonly aggregate_support: number        // A - Aggregate support (0.1-0.3)
  readonly transformation_dominance: number // T - Transform dominance (0.8-1.0)
  readonly connector_flexibility: number    // C - Connection flexibility (0.05-0.15)
  readonly generator_emergence: number      // G - Generation emergence (0.01-0.05)
}

export interface DataTransformationResult {
  readonly original: DataVector
  readonly transformed: DataVector
  readonly validationPassed: boolean
  readonly transformationType: 'data_transform'
  readonly timestamp: string
  readonly validation_rules: ValidationRules
  readonly system_metrics: SystemMetrics
  readonly component_mapping: ComponentMapping
  readonly optimization_score: number
  readonly is_valid_transformation: boolean
}

export interface TransformationOutput {
  readonly vectors?: DataVector[]
  readonly transformation_result: DataTransformationResult
  readonly [key: string]: unknown
}

/**
 * DataTransformer - Pure data transformation implementation
 */
export class DataTransformer implements TransformationComponent {
  readonly type = 'transformation' as const
  readonly purpose = 'Data transformation for processing operations'
  readonly id: string

  // Configuration constants
  private static readonly OPTIMIZATION_RATIO = 1.618 // Golden ratio for optimization
  private static readonly MIN_VALUE = -1000 // Minimum value for safety
  private static readonly MAX_VALUE = 1000 // Maximum value for safety
  private static readonly PRECISION_THRESHOLD = 0.001 // Precision threshold
  private static readonly OPTIMIZATION_PATTERNS = [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16] // Optimization patterns
  
  // Performance constraints
  private static readonly MAX_ITERATIONS = 1000 // Maximum iterations to prevent infinite loops
  private static readonly PERFORMANCE_THRESHOLD = 0.8 // Performance threshold
  private static readonly VALIDATION_TOLERANCE = 0.01 // Validation tolerance

  // Execution metrics
  private executionCount = 0
  private totalExecutionTime = 0
  private lastExecution: Date | null = null

  constructor(id: string) {
    this.id = id
  }

  /**
   * Apply core data transformation: (x, y) => (x - 1, y + 1)
   */
  transformData(vector: DataVector): TransformationResult {
    const startTime = performance.now()
    
    try {
      // Apply core transformation algorithm
      const transformed = this.applyCoreTransformation(vector)
      
      // Validate transformation
      const validationPassed = this.validateTransformation(vector, transformed)
      
      // Update execution metrics
      const executionTime = performance.now() - startTime
      this.updateExecutionMetrics(executionTime)
      
      return {
        original: vector,
        transformed,
        validationPassed,
        transformationType: 'data_transform',
        timestamp: new Date().toISOString()
      }
    } catch (error) {
      // Handle transformation errors
      const executionTime = performance.now() - startTime
      this.updateExecutionMetrics(executionTime)
      
      return {
        original: vector,
        transformed: vector, // Return original on error
        validationPassed: false,
        transformationType: 'data_transform',
        timestamp: new Date().toISOString()
      }
    }
  }

  /**
   * Apply core transformation algorithm
   */
  private applyCoreTransformation(vector: DataVector): DataVector {
    // Core transformation: (x, y) => (x - 1, y + 1)
    const transformedX = this.clampValue(vector.x - 1)
    const transformedY = this.clampValue(vector.y + 1)
    
    return {
      x: transformedX,
      y: transformedY
    }
  }

  /**
   * Clamp value to safe range
   */
  private clampValue(value: number): number {
    return Math.max(
      DataTransformer.MIN_VALUE,
      Math.min(DataTransformer.MAX_VALUE, value)
    )
  }

  /**
   * Validate transformation correctness
   */
  private validateTransformation(original: DataVector, transformed: DataVector): boolean {
    // Check if transformation follows expected pattern
    const expectedX = this.clampValue(original.x - 1)
    const expectedY = this.clampValue(original.y + 1)
    
    const xValid = Math.abs(transformed.x - expectedX) < DataTransformer.PRECISION_THRESHOLD
    const yValid = Math.abs(transformed.y - expectedY) < DataTransformer.PRECISION_THRESHOLD
    
    return xValid && yValid
  }

  /**
   * Apply batch transformation
   */
  transformBatch(vectors: DataVector[]): TransformationResult[] {
    return vectors.map(vector => this.transformData(vector))
  }

  /**
   * Apply inverse transformation: (x, y) => (x + 1, y - 1)
   */
  inverseTransform(vector: DataVector): TransformationResult {
    const startTime = performance.now()
    
    try {
      // Apply inverse transformation
      const transformed = {
        x: this.clampValue(vector.x + 1),
        y: this.clampValue(vector.y - 1)
      }
      
      // Validate inverse transformation
      const validationPassed = this.validateInverseTransformation(vector, transformed)
      
      // Update execution metrics
      const executionTime = performance.now() - startTime
      this.updateExecutionMetrics(executionTime)
      
      return {
        original: vector,
        transformed,
        validationPassed,
        transformationType: 'data_transform',
        timestamp: new Date().toISOString()
      }
    } catch (error) {
      const executionTime = performance.now() - startTime
      this.updateExecutionMetrics(executionTime)
      
      return {
        original: vector,
        transformed: vector,
        validationPassed: false,
        transformationType: 'data_transform',
        timestamp: new Date().toISOString()
      }
    }
  }

  /**
   * Validate inverse transformation
   */
  private validateInverseTransformation(original: DataVector, transformed: DataVector): boolean {
    const expectedX = this.clampValue(original.x + 1)
    const expectedY = this.clampValue(original.y - 1)
    
    const xValid = Math.abs(transformed.x - expectedX) < DataTransformer.PRECISION_THRESHOLD
    const yValid = Math.abs(transformed.y - expectedY) < DataTransformer.PRECISION_THRESHOLD
    
    return xValid && yValid
  }

  /**
   * Calculate comprehensive validation rules
   */
  calculateValidationRules(transformation: TransformationResult): ValidationRules {
    const sumConservation = this.validateSumConservation(transformation.original, transformation.transformed)
    const dataIntegrity = this.validateDataIntegrity(transformation.transformed)
    const informationPreservation = this.validateInformationPreservation(transformation.original, transformation.transformed)
    const operationConsistency = transformation.validationPassed

    return {
      sumConservation,
      dataIntegrity,
      informationPreservation,
      operationConsistency
    }
  }

  /**
   * Validate sum conservation (x + y should remain constant)
   */
  private validateSumConservation(original: DataVector, transformed: DataVector): boolean {
    const originalSum = original.x + original.y
    const transformedSum = transformed.x + transformed.y
    return Math.abs(originalSum - transformedSum) < DataTransformer.VALIDATION_TOLERANCE
  }

  /**
   * Validate data integrity
   */
  private validateDataIntegrity(vector: DataVector): boolean {
    // Check for valid numbers
    return !isNaN(vector.x) && !isNaN(vector.y) && 
           isFinite(vector.x) && isFinite(vector.y)
  }

  /**
   * Validate information preservation
   */
  private validateInformationPreservation(original: DataVector, transformed: DataVector): boolean {
    // Information is preserved if transformation is reversible
    const inverse = {
      x: this.clampValue(transformed.x + 1),
      y: this.clampValue(transformed.y - 1)
    }
    
    const xPreserved = Math.abs(original.x - inverse.x) < DataTransformer.PRECISION_THRESHOLD
    const yPreserved = Math.abs(original.y - inverse.y) < DataTransformer.PRECISION_THRESHOLD
    
    return xPreserved && yPreserved
  }

  /**
   * Calculate system metrics impact
   */
  calculateSystemMetrics(transformation: TransformationResult): SystemMetrics {
    const complexityReduction = this.calculateComplexityReduction(transformation)
    const qualityEnhancement = this.calculateQualityEnhancement(transformation)
    const optimizationImprovement = this.calculateOptimizationImprovement(transformation)

    return {
      complexity_reduction: complexityReduction,
      quality_enhancement: qualityEnhancement,
      optimization_improvement: optimizationImprovement
    }
  }

  /**
   * Calculate complexity reduction
   */
  private calculateComplexityReduction(transformation: TransformationResult): number {
    // Complexity reduction based on value normalization
    const originalComplexity = Math.abs(transformation.original.x) + Math.abs(transformation.original.y)
    const transformedComplexity = Math.abs(transformation.transformed.x) + Math.abs(transformation.transformed.y)
    
    if (originalComplexity === 0) return 0
    return Math.max(0, (originalComplexity - transformedComplexity) / originalComplexity)
  }

  /**
   * Calculate quality enhancement
   */
  private calculateQualityEnhancement(transformation: TransformationResult): number {
    // Quality enhancement based on validation success
    return transformation.validationPassed ? 0.2 : 0
  }

  /**
   * Calculate optimization improvement
   */
  private calculateOptimizationImprovement(transformation: TransformationResult): number {
    // Optimization improvement based on execution efficiency
    const avgExecutionTime = this.getAverageExecutionTime()
    const optimizationFactor = Math.max(0, (10 - avgExecutionTime) / 10) // Normalize to 0-1
    return optimizationFactor * 0.1
  }

  /**
   * Map transformation to component characteristics
   */
  mapToComponentCharacteristics(transformation: TransformationResult): ComponentMapping {
    return {
      aggregate_support: this.calculateAggregateSupport(transformation),
      transformation_dominance: this.calculateTransformationDominance(transformation),
      connector_flexibility: this.calculateConnectorFlexibility(transformation),
      generator_emergence: this.calculateGeneratorEmergence(transformation)
    }
  }

  /**
   * Calculate aggregate support
   */
  private calculateAggregateSupport(transformation: TransformationResult): number {
    const baseSupport = 0.1 // Minimum 10% aggregate support
    const validationBonus = transformation.validationPassed ? 0.2 : 0
    return Math.min(0.3, baseSupport + validationBonus)
  }

  /**
   * Calculate transformation dominance
   */
  private calculateTransformationDominance(transformation: TransformationResult): number {
    const baseDominance = 0.8 // Minimum 80% transformation character
    const qualityBonus = transformation.validationPassed ? 0.2 : 0
    return Math.min(1.0, baseDominance + qualityBonus)
  }

  /**
   * Calculate connector flexibility
   */
  private calculateConnectorFlexibility(transformation: TransformationResult): number {
    const baseFlexibility = 0.05 // Minimum 5% connector character
    const complexityFactor = Math.min(0.1, Math.abs(transformation.transformed.x + transformation.transformed.y) * 0.01)
    return Math.min(0.15, baseFlexibility + complexityFactor)
  }

  /**
   * Calculate generator emergence
   */
  private calculateGeneratorEmergence(transformation: TransformationResult): number {
    const baseEmergence = 0.01 // Minimum 1% generator character
    const innovationFactor = transformation.validationPassed ? 0.04 : 0
    return Math.min(0.05, baseEmergence + innovationFactor)
  }

  /**
   * Update execution metrics
   */
  private updateExecutionMetrics(executionTime: number): void {
    this.executionCount++
    this.totalExecutionTime += executionTime
    this.lastExecution = new Date()
  }

  /**
   * Get average execution time
   */
  getAverageExecutionTime(): number {
    if (this.executionCount === 0) return 0
    return this.totalExecutionTime / this.executionCount
  }

  /**
   * Get execution metrics
   */
  getExecutionMetrics(): Record<string, any> {
    return {
      execution_count: this.executionCount,
      total_execution_time: this.totalExecutionTime,
      average_execution_time: this.getAverageExecutionTime(),
      last_execution: this.lastExecution?.toISOString() || null,
      performance_score: this.calculatePerformanceScore()
    }
  }

  /**
   * Calculate performance score
   */
  private calculatePerformanceScore(): number {
    const avgTime = this.getAverageExecutionTime()
    if (avgTime === 0) return 1.0
    
    // Performance score based on execution time (lower is better)
    return Math.max(0, Math.min(1.0, (10 - avgTime) / 10))
  }

  // Required TransformationComponent interface methods
  
  transform(data: any): TransformationResult {
    return this.transformData(data)
  }

  process(data: any): any {
    return this.transform(data)
  }

  initialize(): Promise<void> {
    return Promise.resolve()
  }

  destroy(): Promise<void> {
    return Promise.resolve()
  }

  getStatus(): Record<string, any> {
    return {
      component: `DataTransformer:${this.id}`,
      type: this.type,
      purpose: this.purpose,
      execution_metrics: this.getExecutionMetrics(),
      timestamp: new Date().toISOString(),
      health: 'active'
    }
  }
}

/**
 * Factory function for creating Data Transformer instances
 */
export function createDataTransformer(id: string): DataTransformer {
  return new DataTransformer(id)
}

/**
 * Type guard for Data Transformer
 */
export function isDataTransformer(component: unknown): component is DataTransformer {
  return component instanceof DataTransformer
}