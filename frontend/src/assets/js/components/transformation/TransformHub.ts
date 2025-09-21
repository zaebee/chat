/**
 * TransformHub - Rect↔Hexa Transformation System
 * 
 * Central orchestration system that bridges rectangular (strict) and 
 * hexagonal (adaptive) paradigms through sacred soft merge patterns.
 * Embodies the complete constitutional wisdom from prototype analysis.
 */

import type { TransformationComponent } from './index'
import { RectValidator, type RectConstraint, type ValidationResult } from './RectValidator'
import { HexaProcessor, type HexaNode, type ProcessingResult } from './HexaProcessor'

export interface MergePoint {
  readonly rectStage: string
  readonly hexaNodes: string[]
  readonly mergeStrategy: 'enhance_rect' | 'hexa_override' | 'balanced_merge'
  readonly compliancePreserved: boolean
}

export interface SoftMergeConfig {
  readonly preserveRectCompliance: boolean
  readonly enableHexaAdaptation: boolean
  readonly mergeStrategy: 'rect_first' | 'hexa_first' | 'parallel'
  readonly validationLevel: 'strict' | 'moderate' | 'flexible'
}

export interface TransformationPipeline {
  readonly id: string
  readonly rectValidators: string[]
  readonly hexaProcessors: string[]
  readonly mergePoints: MergePoint[]
  readonly config: SoftMergeConfig
}

export interface PipelineResult {
  readonly data: any
  readonly rectValidation: ValidationResult
  readonly hexaProcessing: ProcessingResult
  readonly mergeResults: Array<{
    point: MergePoint
    success: boolean
    data: any
    compliance: boolean
  }>
  readonly finalCompliance: boolean
  readonly processingTime: number
}

/**
 * TransformHub orchestrates rect↔hexa transformations
 */
export class TransformHub implements TransformationComponent {
  readonly type = 'transformation' as const
  readonly purpose = 'Rect↔Hexa transformation orchestration'
  readonly id: string

  private rectValidators = new Map<string, RectValidator>()
  private hexaProcessors = new Map<string, HexaProcessor>()
  private mergePoints = new Map<string, MergePoint>()
  private pipelines = new Map<string, TransformationPipeline>()

  constructor(id: string) {
    this.id = id
  }

  /**
   * Register rectangular validator
   */
  registerRectValidator(id: string, validator: RectValidator): void {
    this.rectValidators.set(id, validator)
  }

  /**
   * Register hexagonal processor
   */
  registerHexaProcessor(id: string, processor: HexaProcessor): void {
    this.hexaProcessors.set(id, processor)
  }

  /**
   * Create merge point between rect and hexa paradigms
   */
  createMergePoint(id: string, mergePoint: MergePoint): void {
    this.mergePoints.set(id, mergePoint)
  }

  /**
   * Create transformation pipeline
   */
  createPipeline(pipeline: TransformationPipeline): void {
    this.pipelines.set(pipeline.id, pipeline)
  }

  /**
   * Transform data through rect↔hexa system
   */
  async transform(input: any): Promise<any> {
    // Use default pipeline if available
    const defaultPipeline = this.pipelines.get('default')
    if (defaultPipeline) {
      const result = await this.processPipeline(input, defaultPipeline)
      return result.data
    }

    // Fallback to simple rect→hexa transformation
    return this.processSimpleTransformation(input)
  }

  /**
   * Process data through complete pipeline
   */
  async processPipeline(data: any, pipeline: TransformationPipeline): Promise<PipelineResult> {
    const startTime = performance.now()
    let currentData = { ...data }
    const mergeResults: Array<{
      point: MergePoint
      success: boolean
      data: any
      compliance: boolean
    }> = []

    // Phase 1: Rectangular validation
    let rectValidation: ValidationResult = { valid: true, errors: [], warnings: [], constraintsChecked: 0 }
    
    if (pipeline.config.mergeStrategy === 'rect_first' || pipeline.config.mergeStrategy === 'parallel') {
      for (const validatorId of pipeline.rectValidators) {
        const validator = this.rectValidators.get(validatorId)
        if (validator) {
          currentData = await validator.process(currentData)
          // Extract validation result from processed data
          if (currentData.rect_validation) {
            rectValidation = {
              valid: currentData.rect_validation.validated,
              errors: [],
              warnings: [],
              constraintsChecked: currentData.rect_validation.constraints_applied
            }
          }
        }
      }
    }

    // Phase 2: Hexagonal processing
    let hexaProcessing: ProcessingResult = {
      data: currentData,
      nodesVisited: [],
      transformationsApplied: 0,
      processingTime: 0,
      networkPath: []
    }

    if (pipeline.config.mergeStrategy === 'hexa_first' || pipeline.config.mergeStrategy === 'parallel') {
      for (const processorId of pipeline.hexaProcessors) {
        const processor = this.hexaProcessors.get(processorId)
        if (processor) {
          const result = await processor.processFromNode(currentData, 'entry')
          currentData = result.data
          hexaProcessing = result
        }
      }
    }

    // Phase 3: Soft merge at merge points
    for (const mergePoint of pipeline.mergePoints) {
      try {
        const mergeResult = await this.executeSoftMerge(currentData, mergePoint, pipeline.config)
        mergeResults.push({
          point: mergePoint,
          success: true,
          data: mergeResult.data,
          compliance: mergeResult.compliance
        })
        currentData = mergeResult.data
      } catch (error) {
        mergeResults.push({
          point: mergePoint,
          success: false,
          data: currentData,
          compliance: false
        })
      }
    }

    // Phase 4: Final compliance check
    const finalCompliance = this.checkFinalCompliance(currentData, pipeline.config)

    const endTime = performance.now()

    return {
      data: currentData,
      rectValidation,
      hexaProcessing,
      mergeResults,
      finalCompliance,
      processingTime: endTime - startTime
    }
  }

  /**
   * Execute soft merge at merge point
   */
  private async executeSoftMerge(
    data: any, 
    mergePoint: MergePoint, 
    config: SoftMergeConfig
  ): Promise<{ data: any; compliance: boolean }> {
    let mergedData = { ...data }
    let compliance = true

    switch (mergePoint.mergeStrategy) {
      case 'enhance_rect':
        // Enhance rectangular data with hexagonal insights
        mergedData = await this.enhanceRectWithHexa(data, mergePoint)
        compliance = mergePoint.compliancePreserved
        break

      case 'hexa_override':
        // Allow hexagonal processing to override rectangular constraints
        mergedData = await this.hexaOverrideRect(data, mergePoint)
        compliance = false // Compliance may be compromised
        break

      case 'balanced_merge':
        // Balance between rect compliance and hexa adaptation
        mergedData = await this.balancedMerge(data, mergePoint)
        compliance = this.validateBalancedCompliance(mergedData, config)
        break
    }

    return { data: mergedData, compliance }
  }

  /**
   * Enhance rectangular data with hexagonal insights
   */
  private async enhanceRectWithHexa(data: any, mergePoint: MergePoint): Promise<any> {
    const enhanced = { ...data }

    // Add hexagonal enhancements while preserving rect structure
    enhanced.hexa_enhancements = {
      merge_point: mergePoint.rectStage,
      nodes_involved: mergePoint.hexaNodes,
      enhancement_type: 'rect_preserving',
      timestamp: new Date().toISOString()
    }

    // Apply adaptive enhancements based on hexa nodes
    for (const nodeId of mergePoint.hexaNodes) {
      const processor = this.findProcessorWithNode(nodeId)
      if (processor) {
        const nodeResult = await processor.processFromNode(data, nodeId)
        enhanced[`hexa_${nodeId}_insights`] = {
          transformations: nodeResult.transformationsApplied,
          path: nodeResult.networkPath,
          processing_time: nodeResult.processingTime
        }
      }
    }

    return enhanced
  }

  /**
   * Allow hexagonal override of rectangular constraints
   */
  private async hexaOverrideRect(data: any, mergePoint: MergePoint): Promise<any> {
    let overridden = { ...data }

    // Process through hexa nodes with override capability
    for (const nodeId of mergePoint.hexaNodes) {
      const processor = this.findProcessorWithNode(nodeId)
      if (processor) {
        const result = await processor.processFromNode(overridden, nodeId)
        overridden = result.data
      }
    }

    overridden.hexa_override = {
      original_rect_stage: mergePoint.rectStage,
      override_nodes: mergePoint.hexaNodes,
      compliance_preserved: false,
      timestamp: new Date().toISOString()
    }

    return overridden
  }

  /**
   * Balanced merge between rect and hexa paradigms
   */
  private async balancedMerge(data: any, mergePoint: MergePoint): Promise<any> {
    const rectData = { ...data }
    let hexaData = { ...data }

    // Process through hexa nodes
    for (const nodeId of mergePoint.hexaNodes) {
      const processor = this.findProcessorWithNode(nodeId)
      if (processor) {
        const result = await processor.processFromNode(hexaData, nodeId)
        hexaData = result.data
      }
    }

    // Merge results with balance
    const balanced = {
      ...rectData,
      hexa_balanced_merge: {
        rect_preserved: this.extractRectFields(rectData),
        hexa_adaptations: this.extractHexaFields(hexaData),
        merge_strategy: 'balanced',
        compliance_level: 'partial',
        timestamp: new Date().toISOString()
      }
    }

    // Selectively merge hexa enhancements that don't violate rect constraints
    const safeHexaFields = this.filterSafeHexaFields(hexaData, rectData)
    Object.assign(balanced, safeHexaFields)

    return balanced
  }

  /**
   * Process simple rect→hexa transformation
   */
  private async processSimpleTransformation(data: any): Promise<any> {
    let result = { ...data }

    // Apply first available rect validator
    const firstValidator = Array.from(this.rectValidators.values())[0]
    if (firstValidator) {
      result = await firstValidator.process(result)
    }

    // Apply first available hexa processor
    const firstProcessor = Array.from(this.hexaProcessors.values())[0]
    if (firstProcessor) {
      result = await firstProcessor.transform(result)
    }

    return result
  }

  /**
   * Process data through transformation system
   */
  async process(data: any): Promise<any> {
    const transformed = await this.transform(data)
    
    return {
      ...transformed,
      transform_hub_meta: {
        hub_id: this.id,
        rect_validators: this.rectValidators.size,
        hexa_processors: this.hexaProcessors.size,
        merge_points: this.mergePoints.size,
        pipelines: this.pipelines.size,
        processing_timestamp: new Date().toISOString()
      }
    }
  }

  // Helper methods
  private findProcessorWithNode(nodeId: string): HexaProcessor | undefined {
    for (const processor of this.hexaProcessors.values()) {
      if (processor.getStatus().topology?.nodes[nodeId]) {
        return processor
      }
    }
    return undefined
  }

  private checkFinalCompliance(data: any, config: SoftMergeConfig): boolean {
    if (!config.preserveRectCompliance) return true
    
    // Check if rect validation markers are present and valid
    return data.rect_validation?.validated === true || 
           data.rect_compliance?.passed === true
  }

  private validateBalancedCompliance(data: any, config: SoftMergeConfig): boolean {
    if (config.validationLevel === 'flexible') return true
    if (config.validationLevel === 'strict') return data.rect_validation?.validated === true
    
    // Moderate validation
    return data.hexa_balanced_merge?.compliance_level !== 'failed'
  }

  private extractRectFields(data: any): Record<string, any> {
    const rectFields: Record<string, any> = {}
    for (const [key, value] of Object.entries(data)) {
      if (!key.startsWith('hexa_') && !key.includes('processing')) {
        rectFields[key] = value
      }
    }
    return rectFields
  }

  private extractHexaFields(data: any): Record<string, any> {
    const hexaFields: Record<string, any> = {}
    for (const [key, value] of Object.entries(data)) {
      if (key.startsWith('hexa_') || key.includes('processing')) {
        hexaFields[key] = value
      }
    }
    return hexaFields
  }

  private filterSafeHexaFields(hexaData: any, rectData: any): Record<string, any> {
    const safeFields: Record<string, any> = {}
    
    for (const [key, value] of Object.entries(hexaData)) {
      // Only include hexa fields that don't conflict with rect structure
      if (key.startsWith('hexa_') && !(key in rectData)) {
        safeFields[key] = value
      }
    }
    
    return safeFields
  }

  /**
   * Component lifecycle methods
   */
  async initialize(): Promise<void> {
    // Initialize all registered components
    for (const validator of this.rectValidators.values()) {
      await validator.initialize()
    }
    
    for (const processor of this.hexaProcessors.values()) {
      await processor.initialize()
    }
    
    console.log(`🔧 TransformHub ${this.id} initialized with rect↔hexa system`)
  }

  async destroy(): Promise<void> {
    // Destroy all registered components
    for (const validator of this.rectValidators.values()) {
      await validator.destroy()
    }
    
    for (const processor of this.hexaProcessors.values()) {
      await processor.destroy()
    }
    
    this.rectValidators.clear()
    this.hexaProcessors.clear()
    this.mergePoints.clear()
    this.pipelines.clear()
    
    console.log(`🧹 TransformHub ${this.id} destroyed`)
  }

  getStatus(): Record<string, any> {
    return {
      type: this.type,
      purpose: this.purpose,
      id: this.id,
      rect_validators: this.rectValidators.size,
      hexa_processors: this.hexaProcessors.size,
      merge_points: this.mergePoints.size,
      pipelines: this.pipelines.size,
      paradigm: 'rect↔hexa',
      system_status: 'operational'
    }
  }
}