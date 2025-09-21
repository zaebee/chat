/**
 * T (Transformation) Components - Data Processing & Logic
 * 
 * Components that handle data transformation, processing, and business logic.
 * These components embody the "T" principle of ATCG architecture.
 */

import type { ATCGComponent } from '../index'

// Transformation component implementations
export * from './RectValidator'
export * from './HexaProcessor'
export * from './TransformHub'
export * from './DataPipeline'

// Type definitions for transformation components
export interface TransformationComponent extends ATCGComponent {
  readonly type: 'transformation'
  readonly purpose: string
  readonly id: string
  transform(input: any): any
  process(data: any): any
  initialize(): Promise<void>
  destroy(): Promise<void>
  getStatus(): Record<string, any>
}

// Transformation component factory
export async function createTransformationComponent(type: string, config: any): Promise<TransformationComponent> {
  switch (type) {
    case 'rect_validator':
      return new (await import('./RectValidator')).RectValidator(config.id || 'rect_validator')
    case 'hexa_processor':
      return new (await import('./HexaProcessor')).HexaProcessor(config.id || 'hexa_processor')
    case 'transform_hub':
      return new (await import('./TransformHub')).TransformHub(config.id || 'transform_hub')
    case 'data_pipeline':
      return new (await import('./DataPipeline')).DataPipeline(config.id || 'data_pipeline')
    default:
      throw new Error(`Unknown transformation component type: ${type}`)
  }
}