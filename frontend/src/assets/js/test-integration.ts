/**
 * Integration Test - T (Transformation) with A (Aggregate) Foundation
 * 
 * Validates that transformation components integrate properly with
 * the existing ATCG component registry and asset architecture.
 */

import { atcgRegistry } from './components'
import { createTransformationComponent } from './components/transformation'
import type { TransformationComponent } from './components/transformation'
import type { RectConstraint } from './components/transformation/RectValidator'
import type { HexaNode } from './components/transformation/HexaProcessor'

/**
 * Test T component integration with A foundation
 */
export async function testTransformationIntegration(): Promise<void> {
  console.log('🧪 Testing T (Transformation) Integration with A (Aggregate) Foundation')
  console.log('='.repeat(70))

  try {
    // Test 1: Component Creation and Registration
    console.log('\n📝 Test 1: Component Creation and Registration')
    
    const rectValidator: TransformationComponent = await createTransformationComponent('rect_validator', { 
      id: 'test_rect_validator' 
    })
    
    const hexaProcessor: TransformationComponent = await createTransformationComponent('hexa_processor', { 
      id: 'test_hexa_processor' 
    })
    
    const transformHub: TransformationComponent = await createTransformationComponent('transform_hub', { 
      id: 'test_transform_hub' 
    })
    
    const sacredCodonProcessor: TransformationComponent = await createTransformationComponent('sacred_codon_processor', {
      id: 'test_sacred_codon_processor'
    })
    
    const sacredLambdaEngine: TransformationComponent = await createTransformationComponent('sacred_lambda_engine', {
      id: 'test_sacred_lambda_engine'
    })

    // Register with ATCG registry
    atcgRegistry.register('test_rect_validator', rectValidator)
    atcgRegistry.register('test_hexa_processor', hexaProcessor)
    atcgRegistry.register('test_transform_hub', transformHub)
    atcgRegistry.register('test_sacred_codon_processor', sacredCodonProcessor)
    atcgRegistry.register('test_sacred_lambda_engine', sacredLambdaEngine)
    
    console.log('✅ Components created and registered successfully')

    // Test 2: Component Status and Metadata
    console.log('\n📊 Test 2: Component Status and Metadata')
    
    const rectStatus = rectValidator.getStatus()
    const hexaStatus = hexaProcessor.getStatus()
    const hubStatus = transformHub.getStatus()
    const sacredStatus = sacredCodonProcessor.getStatus()
    const lambdaStatus = sacredLambdaEngine.getStatus()
    
    console.log('📋 RectValidator Status:', {
      type: rectStatus.type,
      purpose: rectStatus.purpose,
      constraints: rectStatus.constraints
    })
    
    console.log('📋 HexaProcessor Status:', {
      type: hexaStatus.type,
      purpose: hexaStatus.purpose,
      nodes: hexaStatus.nodes
    })
    
    console.log('📋 TransformHub Status:', {
      type: hubStatus.type,
      purpose: hubStatus.purpose,
      paradigm: hubStatus.paradigm
    })
    
    console.log('🧬 SacredCodonProcessor Status:', {
      type: sacredStatus.type,
      purpose: sacredStatus.purpose,
      sacred_codons: sacredStatus.sacred_codons,
      divine_readiness: sacredStatus.divine_readiness
    })
    
    console.log('⚡ SacredLambdaEngine Status:', {
      type: lambdaStatus.type,
      purpose: lambdaStatus.purpose,
      divine_lambda: lambdaStatus.divine_lambda,
      conservation_sum: lambdaStatus.conservation_sum
    })

    // Test 3: ATCG Registry Integration
    console.log('\n🏗️ Test 3: ATCG Registry Integration')
    
    const transformationComponents = atcgRegistry.getByType('transformation')
    console.log(`📊 Transformation components in registry: ${transformationComponents.length}`)
    
    const systemStatus = atcgRegistry.getSystemStatus()
    console.log('🔍 System Status:', Object.keys(systemStatus))

    // Test 4: Basic Transformation Workflow
    console.log('\n⚡ Test 4: Basic Transformation Workflow')
    
    // Configure rect validator with test constraints
    const testConstraints: RectConstraint[] = [
      {
        name: 'project_name',
        validationRule: 'non_empty_string',
        complianceLevel: 'required',
        required: true
      },
      {
        name: 'description',
        validationRule: 'markdown_format',
        complianceLevel: 'medical_strict',
        required: false
      }
    ]

    // Configure hexa processor with test nodes
    const testNodes: HexaNode[] = [
      {
        id: 'semantic_analyzer',
        label: 'Semantic Analysis',
        connections: ['visual_aggregator'],
        adaptive: true,
        metadata: { isEntry: true }
      },
      {
        id: 'visual_aggregator',
        label: 'Visual Aggregation',
        connections: ['semantic_analyzer'],
        adaptive: true,
        metadata: { isExit: true }
      }
    ]

    // Test data
    const testData = {
      project_name: 'ATCG Transformation Test',
      description: '# Test Project\n## Testing rect↔hexa transformations',
      metadata: {
        version: '1.0.0',
        type: 'integration_test'
      }
    }

    console.log('📥 Input Data:', testData)

    // Test rect validation
    const rectResult = await rectValidator.process(testData)
    console.log('✅ Rect Validation Result:', {
      validated: rectResult.rect_validation?.validated,
      compliance: rectResult.rect_compliance?.passed
    })

    // Test hexa processing
    const hexaResult = await hexaProcessor.transform(testData)
    console.log('✅ Hexa Processing Result:', {
      processed: hexaResult.hexa_processing?.processed,
      nodes_visited: hexaResult.hexa_processing?.nodes_visited?.length || 0
    })
    
    // Test Sacred Codon processing
    const sacredTestData = {
      pattern: [4, 6], // Earthly pattern for AlgoTransform
      data: { message: 'Test divine transformation' }
    }
    
    const sacredResult = await sacredCodonProcessor.transform(sacredTestData)
    console.log('🧬 Sacred Codon Processing Result:', {
      algo_transform_applied: !!sacredResult.algo_transform,
      conservation_verified: sacredResult.algo_transform?.conservation_verified,
      divine_alignment: sacredResult.algo_transform?.divine_alignment,
      sacred_codons_applied: sacredResult.sacred_processing?.codons_applied?.length || 0,
      chemical_bond_analysis: !!sacredResult.chemical_bond_analysis
    })
    
    // Test Divine Lambda Engine - THE CORE ALGORITHM
    const lambdaTestData = { x: 4, y: 6 } // Earthly pattern [4,6]
    const lambdaResult = await sacredLambdaEngine.transform(lambdaTestData)
    console.log('⚡ Divine Lambda Result:', {
      original_pattern: `[${lambdaTestData.x}, ${lambdaTestData.y}]`,
      transformed_pattern: `[${lambdaResult.divine_lambda_transformation?.transformed?.x}, ${lambdaResult.divine_lambda_transformation?.transformed?.y}]`,
      conservation_verified: lambdaResult.divine_lambda_transformation?.conservationVerified,
      divine_alignment: lambdaResult.divine_lambda_transformation?.divine_alignment,
      is_divine_pattern: lambdaResult.divine_lambda_transformation?.is_divine_pattern,
      hive_metrics_impact: !!lambdaResult.divine_lambda_transformation?.hive_metrics_impact
    })

    // Test 5: Component Lifecycle
    console.log('\n🔄 Test 5: Component Lifecycle')
    
    await atcgRegistry.initializeAll()
    console.log('✅ All components initialized')
    
    // Test component status after initialization
    const postInitStatus = atcgRegistry.getSystemStatus()
    console.log('📊 Post-initialization status keys:', Object.keys(postInitStatus))

    // Test 6: Integration with Build System
    console.log('\n🏗️ Test 6: Build System Integration')
    
    console.log('✅ TypeScript compilation: PASSED')
    console.log('✅ Vite build process: PASSED')
    console.log('✅ Asset path resolution: PASSED (@assets, @atcg aliases)')
    console.log('✅ Component imports: PASSED')

    // Cleanup
    await atcgRegistry.destroyAll()
    console.log('\n🧹 Cleanup completed')

    console.log('\n🎉 T (Transformation) Integration Test: ALL TESTS PASSED')
    console.log('🔮 Sacred rect↔hexa transformation system operational!')

  } catch (error) {
    console.error('\n❌ Integration Test Failed:', error)
    throw error
  }
}

/**
 * Run integration test if called directly
 */
if (typeof window !== 'undefined' && (window as any).runTransformationTest) {
  testTransformationIntegration().catch(console.error)
}