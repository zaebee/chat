/**
 * G (Genesis) Components - Generation & Creation
 * 
 * Components that generate, create, and build new content or functionality.
 * These components embody the "G" principle of ATCG architecture.
 */

// Genesis component implementations
export { 
  DataGenerator, 
  createDataGenerator, 
  isDataGenerator,
  type GeneratorOutput,
  type GenerationResult,
  type GenerationTemplate
} from './DataGenerator'

// Type definitions for genesis components
export interface GenesisComponent {
  readonly type: 'genesis'
  readonly purpose: string
  readonly id: string
  generate(template: any): any
  create(specification: any): any
  build(config: any): any
  getStatus(): Record<string, unknown>
}

// Genesis component types
export type GenesisComponentType = 'data_generator'

// Genesis component factory
export async function createGenesisComponent(
  type: GenesisComponentType, 
  config: { id: string }
): Promise<GenesisComponent> {
  switch (type) {
    case 'data_generator':
      const { createDataGenerator } = await import('./DataGenerator')
      return createDataGenerator(config.id)
    
    default:
      // Exhaustive checking pattern for type safety
      const _exhaustiveCheck: never = type
      throw new Error(`Unknown genesis component type: ${_exhaustiveCheck}`)
  }
}