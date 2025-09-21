/**
 * DataPipeline - End-to-End Data Processing System
 * 
 * Comprehensive pipeline system that orchestrates data flow through
 * rect↔hexa transformations with monitoring, validation, and optimization.
 * Embodies AlgoGenesis principles for complete data lifecycle management.
 */

import type { TransformationComponent } from './index'
import { TransformHub, type TransformationPipeline, type PipelineResult } from './TransformHub'
import { RectValidator, type RectConstraint } from './RectValidator'
import { HexaProcessor, type HexaNode } from './HexaProcessor'

export interface PipelineStage {
  readonly id: string
  readonly name: string
  readonly type: 'validation' | 'transformation' | 'merge' | 'output'
  readonly componentId: string
  readonly config: Record<string, any>
  readonly dependencies: string[]
  readonly optional: boolean
}

export interface PipelineMetrics {
  readonly totalProcessingTime: number
  readonly stagesExecuted: number
  readonly validationsPassed: number
  readonly transformationsApplied: number
  readonly dataSize: {
    input: number
    output: number
    growth: number
  }
  readonly performance: {
    throughput: number
    latency: number
    efficiency: number
  }
}

export interface PipelineExecution {
  readonly id: string
  readonly startTime: Date
  endTime?: Date
  status: 'running' | 'completed' | 'failed' | 'cancelled'
  readonly stages: Array<{
    stage: PipelineStage
    status: 'pending' | 'running' | 'completed' | 'failed' | 'skipped'
    startTime?: Date
    endTime?: Date
    result?: any
    error?: string
  }>
  metrics?: PipelineMetrics
  result?: any
}

export interface DataQualityReport {
  readonly score: number
  readonly issues: Array<{
    type: 'validation' | 'transformation' | 'compliance' | 'performance'
    severity: 'low' | 'medium' | 'high' | 'critical'
    message: string
    stage?: string
    suggestion?: string
  }>
  readonly recommendations: string[]
  readonly compliance: {
    rect: boolean
    hexa: boolean
    overall: boolean
  }
}

/**
 * DataPipeline orchestrates complete data processing workflows
 */
export class DataPipeline implements TransformationComponent {
  readonly type = 'transformation' as const
  readonly purpose = 'End-to-end data processing pipeline'
  readonly id: string

  private stages = new Map<string, PipelineStage>()
  private transformHub: TransformHub
  private executions = new Map<string, PipelineExecution>()
  private qualityThresholds = {
    minScore: 0.8,
    maxLatency: 5000, // ms
    maxDataGrowth: 3.0 // 3x original size
  }

  constructor(id: string) {
    this.id = id
    this.transformHub = new TransformHub(`${id}_hub`)
  }

  /**
   * Add processing stage to pipeline
   */
  addStage(stage: PipelineStage): void {
    this.stages.set(stage.id, stage)
  }

  /**
   * Remove processing stage from pipeline
   */
  removeStage(stageId: string): void {
    this.stages.delete(stageId)
  }

  /**
   * Configure pipeline with stages and components
   */
  async configurePipeline(config: {
    stages: PipelineStage[]
    rectConstraints?: RectConstraint[]
    hexaNodes?: HexaNode[]
    transformationPipeline?: TransformationPipeline
  }): Promise<void> {
    // Add stages
    for (const stage of config.stages) {
      this.addStage(stage)
    }

    // Configure rect validators
    if (config.rectConstraints) {
      const rectValidator = new RectValidator('pipeline_rect_validator')
      for (const constraint of config.rectConstraints) {
        rectValidator.addConstraint(constraint)
      }
      this.transformHub.registerRectValidator('pipeline_validator', rectValidator)
    }

    // Configure hexa processors
    if (config.hexaNodes) {
      const hexaProcessor = new HexaProcessor('pipeline_hexa_processor')
      for (const node of config.hexaNodes) {
        hexaProcessor.addNode(node)
      }
      this.transformHub.registerHexaProcessor('pipeline_processor', hexaProcessor)
    }

    // Configure transformation pipeline
    if (config.transformationPipeline) {
      this.transformHub.createPipeline(config.transformationPipeline)
    }

    await this.transformHub.initialize()
  }

  /**
   * Execute pipeline with data
   */
  async executePipeline(data: any, executionId?: string): Promise<PipelineExecution> {
    const execId = executionId || `exec_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    
    const execution: PipelineExecution = {
      id: execId,
      startTime: new Date(),
      status: 'running',
      stages: Array.from(this.stages.values()).map(stage => ({
        stage,
        status: 'pending'
      }))
    }

    this.executions.set(execId, execution)

    try {
      let currentData = { ...data }
      const inputSize = this.calculateDataSize(data)
      const stageResults: any[] = []

      // Execute stages in dependency order
      const orderedStages = this.getStagesInExecutionOrder()
      
      for (const stage of orderedStages) {
        const stageExecution = execution.stages.find(s => s.stage.id === stage.id)!
        stageExecution.status = 'running'
        stageExecution.startTime = new Date()

        try {
          const stageResult = await this.executeStage(stage, currentData)
          currentData = stageResult
          stageResults.push(stageResult)
          
          stageExecution.status = 'completed'
          stageExecution.endTime = new Date()
          stageExecution.result = stageResult
        } catch (error) {
          stageExecution.status = 'failed'
          stageExecution.endTime = new Date()
          stageExecution.error = error instanceof Error ? error.message : String(error)
          
          if (!stage.optional) {
            throw error
          }
        }
      }

      // Calculate metrics
      const outputSize = this.calculateDataSize(currentData)
      const totalTime = Date.now() - execution.startTime.getTime()
      
      const metrics: PipelineMetrics = {
        totalProcessingTime: totalTime,
        stagesExecuted: execution.stages.filter(s => s.status === 'completed').length,
        validationsPassed: this.countValidationStages(execution.stages),
        transformationsApplied: this.countTransformationStages(execution.stages),
        dataSize: {
          input: inputSize,
          output: outputSize,
          growth: outputSize / inputSize
        },
        performance: {
          throughput: outputSize / (totalTime / 1000), // bytes per second
          latency: totalTime,
          efficiency: this.calculateEfficiency(execution.stages)
        }
      }

      execution.status = 'completed'
      execution.endTime = new Date()
      execution.result = currentData
      execution.metrics = metrics

    } catch (error) {
      execution.status = 'failed'
      execution.endTime = new Date()
      console.error(`Pipeline execution ${execId} failed:`, error)
    }

    return execution
  }

  /**
   * Execute individual stage
   */
  private async executeStage(stage: PipelineStage, data: any): Promise<any> {
    switch (stage.type) {
      case 'validation':
        return this.executeValidationStage(stage, data)
      
      case 'transformation':
        return this.executeTransformationStage(stage, data)
      
      case 'merge':
        return this.executeMergeStage(stage, data)
      
      case 'output':
        return this.executeOutputStage(stage, data)
      
      default:
        throw new Error(`Unknown stage type: ${stage.type}`)
    }
  }

  /**
   * Execute validation stage
   */
  private async executeValidationStage(stage: PipelineStage, data: any): Promise<any> {
    // Use transform hub for validation
    const result = await this.transformHub.process(data)
    
    return {
      ...result,
      stage_execution: {
        stage_id: stage.id,
        stage_name: stage.name,
        stage_type: 'validation',
        timestamp: new Date().toISOString()
      }
    }
  }

  /**
   * Execute transformation stage
   */
  private async executeTransformationStage(stage: PipelineStage, data: any): Promise<any> {
    // Apply transformation through hub
    const result = await this.transformHub.transform(data)
    
    return {
      ...result,
      stage_execution: {
        stage_id: stage.id,
        stage_name: stage.name,
        stage_type: 'transformation',
        timestamp: new Date().toISOString()
      }
    }
  }

  /**
   * Execute merge stage
   */
  private async executeMergeStage(stage: PipelineStage, data: any): Promise<any> {
    // Execute soft merge through transform hub
    const result = await this.transformHub.process(data)
    
    return {
      ...result,
      stage_execution: {
        stage_id: stage.id,
        stage_name: stage.name,
        stage_type: 'merge',
        merge_strategy: stage.config.mergeStrategy || 'balanced_merge',
        timestamp: new Date().toISOString()
      }
    }
  }

  /**
   * Execute output stage
   */
  private async executeOutputStage(stage: PipelineStage, data: any): Promise<any> {
    // Apply output formatting and finalization
    const output = {
      ...data,
      pipeline_output: {
        pipeline_id: this.id,
        stage_id: stage.id,
        stage_name: stage.name,
        output_format: stage.config.format || 'json',
        finalized: true,
        timestamp: new Date().toISOString()
      }
    }

    // Apply output transformations if specified
    if (stage.config.transformations) {
      for (const transformation of stage.config.transformations) {
        // Apply transformation logic based on config
        if (transformation === 'minify') {
          output.pipeline_output.minified = true
        } else if (transformation === 'compress') {
          output.pipeline_output.compressed = true
        }
      }
    }

    return output
  }

  /**
   * Generate data quality report
   */
  async generateQualityReport(execution: PipelineExecution): Promise<DataQualityReport> {
    const issues: DataQualityReport['issues'] = []
    const recommendations: string[] = []
    let score = 1.0

    if (!execution.metrics) {
      return {
        score: 0,
        issues: [{ type: 'performance', severity: 'critical', message: 'No metrics available' }],
        recommendations: ['Re-run pipeline with metrics enabled'],
        compliance: { rect: false, hexa: false, overall: false }
      }
    }

    // Check performance issues
    if (execution.metrics.performance.latency > this.qualityThresholds.maxLatency) {
      issues.push({
        type: 'performance',
        severity: 'high',
        message: `High latency: ${execution.metrics.performance.latency}ms`,
        suggestion: 'Consider optimizing transformation stages'
      })
      score -= 0.2
    }

    // Check data growth
    if (execution.metrics.dataSize.growth > this.qualityThresholds.maxDataGrowth) {
      issues.push({
        type: 'performance',
        severity: 'medium',
        message: `Excessive data growth: ${execution.metrics.dataSize.growth.toFixed(2)}x`,
        suggestion: 'Review transformation efficiency'
      })
      score -= 0.1
    }

    // Check failed stages
    const failedStages = execution.stages.filter(s => s.status === 'failed')
    for (const failedStage of failedStages) {
      issues.push({
        type: 'validation',
        severity: failedStage.stage.optional ? 'medium' : 'high',
        message: `Stage failed: ${failedStage.stage.name}`,
        stage: failedStage.stage.id,
        suggestion: 'Check stage configuration and input data'
      })
      score -= failedStage.stage.optional ? 0.05 : 0.15
    }

    // Generate recommendations
    if (execution.metrics.performance.efficiency < 0.7) {
      recommendations.push('Consider reducing number of transformation stages')
    }
    
    if (execution.metrics.validationsPassed === 0) {
      recommendations.push('Add validation stages to ensure data quality')
    }

    // Check compliance
    const compliance = {
      rect: execution.result?.rect_validation?.validated === true,
      hexa: execution.result?.hexa_processing?.processed === true,
      overall: score >= this.qualityThresholds.minScore
    }

    return {
      score: Math.max(0, score),
      issues,
      recommendations,
      compliance
    }
  }

  /**
   * Transform data through pipeline
   */
  async transform(input: any): Promise<any> {
    const execution = await this.executePipeline(input)
    return execution.result || input
  }

  /**
   * Process data with quality reporting
   */
  async process(data: any): Promise<any> {
    const execution = await this.executePipeline(data)
    const qualityReport = await this.generateQualityReport(execution)
    
    return {
      ...execution.result,
      pipeline_execution: {
        execution_id: execution.id,
        status: execution.status,
        metrics: execution.metrics,
        quality_report: qualityReport
      }
    }
  }

  // Helper methods
  private getStagesInExecutionOrder(): PipelineStage[] {
    const stages = Array.from(this.stages.values())
    const ordered: PipelineStage[] = []
    const visited = new Set<string>()

    const visit = (stage: PipelineStage) => {
      if (visited.has(stage.id)) return
      
      // Visit dependencies first
      for (const depId of stage.dependencies) {
        const depStage = this.stages.get(depId)
        if (depStage) {
          visit(depStage)
        }
      }
      
      visited.add(stage.id)
      ordered.push(stage)
    }

    for (const stage of stages) {
      visit(stage)
    }

    return ordered
  }

  private calculateDataSize(data: any): number {
    return JSON.stringify(data).length
  }

  private countValidationStages(stages: PipelineExecution['stages']): number {
    return stages.filter(s => 
      s.stage.type === 'validation' && s.status === 'completed'
    ).length
  }

  private countTransformationStages(stages: PipelineExecution['stages']): number {
    return stages.filter(s => 
      s.stage.type === 'transformation' && s.status === 'completed'
    ).length
  }

  private calculateEfficiency(stages: PipelineExecution['stages']): number {
    const completed = stages.filter(s => s.status === 'completed').length
    const total = stages.length
    return total > 0 ? completed / total : 0
  }

  /**
   * Component lifecycle methods
   */
  async initialize(): Promise<void> {
    await this.transformHub.initialize()
    console.log(`🔧 DataPipeline ${this.id} initialized with ${this.stages.size} stages`)
  }

  async destroy(): Promise<void> {
    await this.transformHub.destroy()
    this.stages.clear()
    this.executions.clear()
    console.log(`🧹 DataPipeline ${this.id} destroyed`)
  }

  getStatus(): Record<string, any> {
    return {
      type: this.type,
      purpose: this.purpose,
      id: this.id,
      stages: this.stages.size,
      executions: this.executions.size,
      transform_hub: this.transformHub.getStatus(),
      quality_thresholds: this.qualityThresholds
    }
  }
}