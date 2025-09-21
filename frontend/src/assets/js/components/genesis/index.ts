/**
 * G (Genesis) Components - Generation & Creation
 * 
 * Components that generate, create, and build new content or functionality.
 * These components embody the "G" principle of ATCG architecture.
 */

// Re-export all genesis components
export * from './ContentGenerator'
export * from './ComponentBuilder'
export * from './WorkflowCreator'

// Type definitions for genesis components
export interface GenesisComponent {
  readonly type: 'genesis'
  readonly purpose: string
  generate(template: any): any
  create(specification: any): any
  build(config: any): any
}

// Genesis component factory
export function createGenesisComponent(type: string, config: any): GenesisComponent {
  switch (type) {
    case 'content':
      return new ContentGenerator(config)
    case 'component':
      return new ComponentBuilder(config)
    case 'workflow':
      return new WorkflowCreator(config)
    default:
      throw new Error(`Unknown genesis component type: ${type}`)
  }
}