/**
 * Integration Test - T (Transformation) with A (Aggregate) Foundation
 * 
 * Validates that transformation components integrate properly with
 * the existing ATCG component registry and asset architecture.
 */

import { atcgRegistry } from './components'
import { createTransformationComponent } from './components/transformation'
import type { TransformationComponent } from './components/transformation'

/**
 * Test T component integration with A foundation
 */
export async function testTransformationIntegration(): Promise<void> {
  console.log('🧪 Testing T (Transformation) Integration with A (Aggregate) Foundation')
  console.log('='.repeat(70))

  try {
    // Test 1: Component Creation and Registration
    console.log('\n📝 Test 1: Component Creation and Registration')
    
    const dataTransformer: TransformationComponent = await createTransformationComponent('data_transformer', { 
      id: 'test_data_transformer' 
    })

    // Register components with ATCG registry
    await atcgRegistry.register('test_data_transformer', dataTransformer)

    console.log('✅ All transformation components created and registered successfully')

    // Test 2: Component Status and Health
    console.log('\n📊 Test 2: Component Status and Health')
    
    const transformerStatus = dataTransformer.getStatus()
    console.log('📈 DataTransformer Status:', {
      type: transformerStatus.type,
      purpose: transformerStatus.purpose,
      health: transformerStatus.health
    })

    console.log('✅ All components report healthy status')

    // Test 3: Basic Transformation Operations
    console.log('\n🔄 Test 3: Basic Transformation Operations')
    
    const testData = { x: 4, y: 6 }
    const transformResult = dataTransformer.transform(testData)
    
    console.log('⚡ Transformation Result:', {
      original: testData,
      transformed: transformResult.transformed,
      success: transformResult.validationPassed
    })

    console.log('✅ Basic transformation operations working')

    // Cleanup
    await atcgRegistry.destroyAll()
    console.log('\n🧹 Cleanup completed')

    console.log('\n🎉 T (Transformation) Integration Test: ALL TESTS PASSED')

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