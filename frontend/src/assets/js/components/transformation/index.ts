/**
 * T (Transformation) Components - Data Processing & Logic
 * 
 * Components that handle data transformation, processing, and business logic.
 * These components embody the "T" principle of ATCG architecture.
 */

// Transformation component implementations
export * from './RectValidator'
export * from './HexaProcessor'
export * from './TransformHub'

// Type definitions for transformation components
export interface TransformationComponent {
  readonly type: 'transformation'
  readonly purpose: string
  transform(input: any): any
  process(data: any): any
}

// Transformation component factory
export function createTransformationComponent(type: string, config: any): TransformationComponent {
  switch (type) {
    case 'rect_validator':
      return new (await import('./RectValidator')).RectValidator(config.id || 'rect_validator')
    case 'hexa_processor':
      return new (await import('./HexaProcessor')).HexaProcessor(config.id || 'hexa_processor')
    case 'transform_hub':
      return new (await import('./TransformHub')).TransformHub(config.id || 'transform_hub')
    default:
      throw new Error(`Unknown transformation component type: ${type}`)
  }
}