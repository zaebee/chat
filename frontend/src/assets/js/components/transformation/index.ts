/**
 * T (Transformation) Components - Data Processing & Logic
 * 
 * Components that handle data transformation, processing, and business logic.
 * These components embody the "T" principle of ATCG architecture.
 */

// Re-export all transformation components
export * from './DataTransformer'
export * from './StateProcessor'
export * from './ContentFormatter'

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
    case 'data':
      return new DataTransformer(config)
    case 'state':
      return new StateProcessor(config)
    case 'content':
      return new ContentFormatter(config)
    default:
      throw new Error(`Unknown transformation component type: ${type}`)
  }
}