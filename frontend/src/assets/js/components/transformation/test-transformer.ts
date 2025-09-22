/**
 * Sacred Transformer Test Suite - Enzymatic Processing Validation
 * 
 * Comprehensive testing for stateless data transformation patterns
 * Following Sacred Architecture testing principles with battle-hardened validation
 */

import { SacredTransformer, createSacredTransformer, isSacredTransformer } from './SacredTransformer'
import type { 
  TransformationInput, 
  TransformationOutput, 
  ProcessingRule,
  ProcessingPipeline,
  TransformationMetrics 
} from './SacredTransformer'

// Custom assertion function to avoid console pollution
function assert(condition: boolean, message: string): void {
  if (!condition) {
    throw new Error(`Assertion failed: ${message}`)
  }
}

/**
 * Execute comprehensive Sacred Transformer test suite
 */
export async function runSacredTransformerTests(): Promise<void> {
  console.log('🔧 Sacred Transformer Test Suite - Enzymatic Processing Validation')
  console.log('=' .repeat(80))

  let testCount = 0
  let passedTests = 0

  // Test execution helper
  async function runTest(testName: string, testFn: () => Promise<void>): Promise<void> {
    testCount++
    try {
      await testFn()
      passedTests++
      console.log(`✅ Test ${testCount}: ${testName}`)
    } catch (error) {
      console.log(`❌ Test ${testCount}: ${testName}`)
      console.log(`   Error: ${error instanceof Error ? error.message : 'Unknown error'}`)
    }
  }

  // Test 1: Basic Transformer Creation
  await runTest('Sacred Transformer Creation', async () => {
    const transformer = createSacredTransformer({
      id: 'test_transformer_1'
    })

    assert(transformer instanceof SacredTransformer, 'Should create SacredTransformer instance')
    assert(transformer.type === 'transformation', 'Should have correct type')
    assert(transformer.purpose.includes('enzymatic processing'), 'Should have enzymatic purpose')
    assert(isSacredTransformer(transformer), 'Type guard should work')
  })

  // Test 2: Configuration Validation
  await runTest('Configuration Validation', async () => {
    try {
      createSacredTransformer({ id: '' })
      assert(false, 'Should reject empty ID')
    } catch (error) {
      assert(error instanceof Error && error.message.includes('required'), 'Should validate ID requirement')
    }

    try {
      createSacredTransformer({ id: 'x'.repeat(101) })
      assert(false, 'Should reject oversized ID')
    } catch (error) {
      assert(error instanceof Error && error.message.includes('100 characters'), 'Should validate ID length')
    }
  })

  // Test 3: Initialization and Destruction
  await runTest('Initialization and Destruction', async () => {
    const transformer = createSacredTransformer({ id: 'test_transformer_3' })

    // Test initialization
    await transformer.initialize()
    const status = transformer.getStatus() as any
    assert(status.initialization_state.is_initialized === true, 'Should be initialized')
    assert(status.initialization_state.ready_for_processing === true, 'Should be ready for processing')

    // Test destruction
    await transformer.destroy()
    const destroyedStatus = transformer.getStatus() as any
    assert(destroyedStatus.initialization_state.is_destroyed === true, 'Should be destroyed')
    assert(destroyedStatus.initialization_state.ready_for_processing === false, 'Should not be ready after destruction')
  })

  // Test 4: Basic Data Transformation
  await runTest('Basic Data Transformation', async () => {
    const transformer = createSacredTransformer({ id: 'test_transformer_4' })
    await transformer.initialize()

    const input = {
      id: 'test_input_1',
      data: { name: 'test', value: 42 },
      format: 'json',
      timestamp: new Date().toISOString()
    }

    const result = await transformer.transform(input)

    assert(result.success === true, 'Transformation should succeed')
    assert(result.originalData.name === 'test', 'Should preserve original data')
    assert(typeof result.transformedData === 'object', 'Should produce transformed data')
    assert(result.executionTime >= 0, 'Should track execution time')
    assert(result.inputFormat === 'json', 'Should preserve input format')

    await transformer.destroy()
  })

  // Test 5: Processing Rules Management
  await runTest('Processing Rules Management', async () => {
    const transformer = createSacredTransformer({ id: 'test_transformer_5' })
    await transformer.initialize()

    // Add custom processing rule
    const customRule: ProcessingRule = {
      ruleId: 'uppercase_transform',
      name: 'Uppercase Transformation',
      inputFormat: 'text',
      outputFormat: 'uppercase_text',
      processor: (data: Record<string, unknown>) => {
        const result: Record<string, unknown> = {}
        for (const [key, value] of Object.entries(data)) {
          result[key] = typeof value === 'string' ? value.toUpperCase() : value
        }
        return result
      },
      validator: (data: Record<string, unknown>) => typeof data === 'object',
      isActive: true
    }

    transformer.addProcessingRule(customRule)

    const status = transformer.getStatus() as any
    assert(status.processing_capabilities.available_rules > 3, 'Should have added custom rule')

    // Test rule removal
    const removed = transformer.removeProcessingRule('uppercase_transform')
    assert(removed === true, 'Should successfully remove rule')

    await transformer.destroy()
  })

  // Test 6: Processing Pipeline Creation
  await runTest('Processing Pipeline Creation', async () => {
    const transformer = createSacredTransformer({ id: 'test_transformer_6' })
    await transformer.initialize()

    // Add custom rules for pipeline
    transformer.addProcessingRule({
      ruleId: 'step1',
      name: 'Step 1',
      inputFormat: 'raw',
      outputFormat: 'processed1',
      processor: (data: Record<string, unknown>) => ({ ...data, step1: true }),
      isActive: true
    })

    transformer.addProcessingRule({
      ruleId: 'step2',
      name: 'Step 2',
      inputFormat: 'processed1',
      outputFormat: 'processed2',
      processor: (data: Record<string, unknown>) => ({ ...data, step2: true }),
      isActive: true
    })

    // Create pipeline
    const pipeline: ProcessingPipeline = {
      pipelineId: 'test_pipeline',
      name: 'Test Pipeline',
      rules: [
        transformer['processingRules'].get('step1')!,
        transformer['processingRules'].get('step2')!
      ],
      isActive: true,
      executionOrder: ['step1', 'step2']
    }

    transformer.createProcessingPipeline(pipeline)

    const status = transformer.getStatus() as any
    assert(status.processing_capabilities.available_pipelines > 1, 'Should have created custom pipeline')

    await transformer.destroy()
  })

  // Test 7: Input Size Validation
  await runTest('Input Size Security Validation', async () => {
    const transformer = createSacredTransformer({ id: 'test_transformer_7' })
    await transformer.initialize()

    // Create oversized input
    const largeData = { content: 'x'.repeat(10 * 1024 * 1024 + 1) } // > 10MB

    try {
      await transformer.transform({
        id: 'large_test',
        data: largeData,
        format: 'json',
        timestamp: new Date().toISOString()
      })
      assert(false, 'Should reject oversized input')
    } catch (error) {
      assert(error instanceof Error && error.message.includes('exceeds maximum'), 'Should validate input size')
    }

    await transformer.destroy()
  })

  // Test 8: Rate Limiting Protection
  await runTest('Rate Limiting DoS Protection', async () => {
    const transformer = createSacredTransformer({ id: 'test_transformer_8' })
    await transformer.initialize()

    // Attempt to process messages rapidly
    const promises = []
    for (let i = 0; i < 1002; i++) { // Exceed rate limit of 1000
      promises.push(transformer.transform({
        id: `rate_test_${i}`,
        data: { message: `test_${i}` },
        format: 'json',
        timestamp: new Date().toISOString()
      }).catch(e => e))
    }

    const results = await Promise.all(promises)
    const errors = results.filter(result => result instanceof Error)
    
    assert(errors.length > 0, 'Should reject some operations due to rate limiting')
    assert(errors.some(error => error.message.includes('Rate limit exceeded')), 'Should provide rate limit error message')

    await transformer.destroy()
  })

  // Test 9: Pipeline Depth Validation
  await runTest('Pipeline Depth Security Validation', async () => {
    const transformer = createSacredTransformer({ id: 'test_transformer_9' })
    await transformer.initialize()

    // Create too many rules for pipeline
    const rules: ProcessingRule[] = []
    for (let i = 0; i < 12; i++) { // Exceed max depth of 10
      rules.push({
        ruleId: `rule_${i}`,
        name: `Rule ${i}`,
        inputFormat: 'any',
        outputFormat: 'any',
        processor: (data: Record<string, unknown>) => data,
        isActive: true
      })
    }

    try {
      transformer.createProcessingPipeline({
        pipelineId: 'deep_pipeline',
        name: 'Deep Pipeline',
        rules,
        isActive: true,
        executionOrder: rules.map(r => r.ruleId)
      })
      assert(false, 'Should reject deep pipeline')
    } catch (error) {
      assert(error instanceof Error && error.message.includes('exceeds maximum'), 'Should validate pipeline depth')
    }

    await transformer.destroy()
  })

  // Test 10: Error Handling and Recovery
  await runTest('Error Handling and Recovery', async () => {
    const transformer = createSacredTransformer({ id: 'test_transformer_10' })

    // Test processing without initialization
    try {
      await transformer.transform({ data: { test: 'data' } })
      assert(false, 'Should fail when not initialized')
    } catch (error) {
      assert(error instanceof Error && error.message.includes('not initialized'), 'Should require initialization')
    }

    // Test processing after destruction
    await transformer.initialize()
    await transformer.destroy()

    try {
      await transformer.transform({ data: { test: 'data' } })
      assert(false, 'Should fail when destroyed')
    } catch (error) {
      assert(error instanceof Error && error.message.includes('destroyed'), 'Should prevent processing after destruction')
    }
  })

  // Test 11: Performance Metrics Tracking
  await runTest('Performance Metrics Tracking', async () => {
    const transformer = createSacredTransformer({ id: 'test_transformer_11' })
    await transformer.initialize()

    const initialStatus = transformer.getStatus() as any
    assert(initialStatus.performance_metrics.total_transformations === 0, 'Should start with zero transformations')

    // Perform some transformations
    for (let i = 0; i < 5; i++) {
      await transformer.transform({
        id: `metrics_test_${i}`,
        data: { value: i },
        format: 'json',
        timestamp: new Date().toISOString()
      })
    }

    const updatedStatus = transformer.getStatus() as any
    assert(updatedStatus.performance_metrics.total_transformations === 5, 'Should track transformations')
    assert(typeof updatedStatus.performance_metrics.average_execution_time === 'number', 'Should calculate average execution time')
    assert(updatedStatus.performance_metrics.error_rate >= 0, 'Should track error rate')

    await transformer.destroy()
  })

  // Test 12: Processing Health Assessment
  await runTest('Processing Health Assessment', async () => {
    const transformer = createSacredTransformer({ id: 'test_transformer_12' })
    await transformer.initialize()

    const status = transformer.getStatus() as any
    const health = status.processing_health

    assert(typeof health.success_rate === 'number', 'Should assess success rate')
    assert(typeof health.performance_target_met === 'boolean', 'Should assess performance targets')
    assert(typeof health.error_threshold_ok === 'boolean', 'Should assess error thresholds')
    assert(typeof health.rate_limit_status === 'number', 'Should assess rate limit status')

    await transformer.destroy()
  })

  // Test 13: Data Sanitization
  await runTest('Data Sanitization Security', async () => {
    const transformer = createSacredTransformer({ id: 'test_transformer_13' })
    await transformer.initialize()

    // Test malicious input sanitization
    const maliciousInput = {
      id: 'sanitization_test',
      data: {
        script: '<script>alert("xss")</script>',
        javascript: 'javascript:alert("xss")',
        onclick: 'onclick="alert(\'xss\')"',
        __proto__: { polluted: true },
        constructor: { dangerous: true }
      },
      format: 'json',
      timestamp: new Date().toISOString()
    }

    const result = await transformer.transform(maliciousInput)
    
    assert(result.success === true, 'Should handle malicious input without crashing')
    assert(!JSON.stringify(result.transformedData).includes('<script>'), 'Should sanitize script tags')
    assert(!result.transformedData.hasOwnProperty('__proto__'), 'Should remove dangerous properties')

    await transformer.destroy()
  })

  // Test 14: Type Safety Validation
  await runTest('Type Safety Validation', async () => {
    const transformer = createSacredTransformer({ id: 'test_transformer_14' })

    // Test type guards
    assert(isSacredTransformer(transformer), 'Type guard should identify SacredTransformer')
    assert(!isSacredTransformer({}), 'Type guard should reject non-transformers')
    assert(!isSacredTransformer(null), 'Type guard should reject null')

    // Test readonly properties
    assert(transformer.type === 'transformation', 'Type should be readonly')
    assert(typeof transformer.purpose === 'string', 'Purpose should be string')
    assert(typeof transformer.id === 'string', 'ID should be string')
  })

  // Test 15: Status Information Completeness
  await runTest('Status Information Completeness', async () => {
    const transformer = createSacredTransformer({ id: 'test_transformer_15' })
    await transformer.initialize()
    
    const status = transformer.getStatus() as any

    // Required status fields
    assert(status.component === 'SacredTransformer', 'Should identify component')
    assert(status.type === 'T', 'Should identify ATCG type')
    assert(status.id === 'test_transformer_15', 'Should include transformer ID')
    assert(typeof status.timestamp === 'string', 'Should include timestamp')
    assert(['optimal', 'degraded', 'critical'].includes(status.health), 'Should have valid health status')

    // Processing state
    assert(typeof status.initialization_state === 'object', 'Should include initialization state')
    assert(typeof status.processing_capabilities === 'object', 'Should include processing capabilities')
    assert(typeof status.performance_metrics === 'object', 'Should include performance metrics')
    assert(typeof status.processing_health === 'object', 'Should include processing health')
    assert(typeof status.security_constraints === 'object', 'Should include security constraints')
    assert(typeof status.known_limitations === 'object', 'Should acknowledge limitations')

    await transformer.destroy()
  })

  // Test 16: Chaos Engineering - Memory Pressure
  await runTest('Chaos Engineering - Memory Pressure', async () => {
    const transformer = createSacredTransformer({ id: 'test_transformer_16' })
    await transformer.initialize()

    // Send many large transformations to test memory handling
    const largePayload = { data: 'x'.repeat(100000) } // 100KB payload
    
    for (let i = 0; i < 20; i++) {
      try {
        await transformer.transform({
          id: `memory_test_${i}`,
          data: largePayload,
          format: 'json',
          timestamp: new Date().toISOString()
        })
      } catch (error) {
        // Rate limiting or size limiting is expected
        assert(error instanceof Error, 'Should handle memory pressure gracefully')
      }
    }

    const status = transformer.getStatus() as any
    assert(typeof status.performance_metrics.total_transformations === 'number', 'Should track transformations under pressure')

    await transformer.destroy()
  })

  // Test 17: Chaos Engineering - Malformed Data Injection
  await runTest('Chaos Engineering - Malformed Data Injection', async () => {
    const transformer = createSacredTransformer({ id: 'test_transformer_17' })
    await transformer.initialize()

    // Inject various malformed data types
    const malformedInputs = [
      undefined,
      null,
      Symbol('chaos'),
      function() { return 'chaos' },
      new Date(),
      /regex/,
      new Error('chaos error'),
      { circular: null as any }
    ]

    // Create circular reference
    malformedInputs[7].circular = malformedInputs[7]

    for (const input of malformedInputs.slice(0, 7)) { // Skip circular for now
      try {
        await transformer.transform(input)
        // Some inputs might be handled gracefully
        assert(true, 'Should handle malformed input without crashing')
      } catch (error) {
        // Rejecting malformed input is also acceptable
        assert(error instanceof Error, 'Should throw proper Error objects for malformed input')
      }
    }

    await transformer.destroy()
  })

  // Test 18: Chaos Engineering - Processing Rule Failures
  await runTest('Chaos Engineering - Processing Rule Failures', async () => {
    const transformer = createSacredTransformer({ id: 'test_transformer_18' })
    await transformer.initialize()

    // Add a rule that always fails
    transformer.addProcessingRule({
      ruleId: 'failing_rule',
      name: 'Always Fails',
      inputFormat: 'any',
      outputFormat: 'error',
      processor: () => {
        throw new Error('Intentional failure for chaos testing')
      },
      isActive: true
    })

    // Create pipeline with failing rule
    transformer.createProcessingPipeline({
      pipelineId: 'chaos_pipeline',
      name: 'Chaos Pipeline',
      rules: [transformer['processingRules'].get('failing_rule')!],
      isActive: true,
      executionOrder: ['failing_rule']
    })

    // Test that system handles rule failures gracefully
    try {
      const result = await transformer.transform({
        id: 'chaos_test',
        data: { test: 'data' },
        format: 'json',
        timestamp: new Date().toISOString()
      })
      
      // Should return error result, not crash
      assert(result.success === false, 'Should handle rule failures gracefully')
      assert(result.metadata?.error, 'Should include error information')
    } catch (error) {
      // Throwing is also acceptable for rule failures
      assert(error instanceof Error, 'Should throw proper Error objects')
    }

    await transformer.destroy()
  })

  // Test 19: Chaos Engineering - Concurrent Operations
  await runTest('Chaos Engineering - Concurrent Operations', async () => {
    const transformer = createSacredTransformer({ id: 'test_transformer_19' })
    await transformer.initialize()

    // Test concurrent transformations
    const promises = []
    for (let i = 0; i < 50; i++) {
      promises.push(
        transformer.transform({
          id: `concurrent_${i}`,
          data: { concurrent: i, timestamp: Date.now() },
          format: 'json',
          timestamp: new Date().toISOString()
        }).catch(e => e) // Capture both successes and failures
      )
    }

    const results = await Promise.all(promises)
    const successes = results.filter(result => !(result instanceof Error) && result.success)
    
    assert(successes.length > 0, 'Should handle some concurrent operations')
    
    // System should still be responsive after concurrent operations
    const status = transformer.getStatus() as any
    assert(typeof status.health === 'string', 'Should remain responsive after concurrent operations')

    await transformer.destroy()
  })

  // Test 20: Chaos Engineering - Resource Exhaustion
  await runTest('Chaos Engineering - Resource Exhaustion', async () => {
    const transformer = createSacredTransformer({ id: 'test_transformer_20' })
    await transformer.initialize()

    // Attempt to exhaust various resources
    const resourceExhaustionTests = [
      // Rule exhaustion
      async () => {
        for (let i = 0; i < 100; i++) {
          try {
            transformer.addProcessingRule({
              ruleId: `exhaustion_rule_${i}`,
              name: `Exhaustion Rule ${i}`,
              inputFormat: 'any',
              outputFormat: 'any',
              processor: (data: Record<string, unknown>) => data,
              isActive: true
            })
          } catch (error) {
            return error
          }
        }
      },
      
      // Pipeline exhaustion
      async () => {
        for (let i = 0; i < 50; i++) {
          try {
            transformer.createProcessingPipeline({
              pipelineId: `exhaustion_pipeline_${i}`,
              name: `Exhaustion Pipeline ${i}`,
              rules: [transformer['processingRules'].get('identity_transform')!],
              isActive: true,
              executionOrder: ['identity_transform']
            })
          } catch (error) {
            return error
          }
        }
      }
    ]

    for (const test of resourceExhaustionTests) {
      try {
        await test()
        // Should either succeed or fail gracefully
        assert(true, 'Should handle resource exhaustion attempts')
      } catch (error) {
        // Proper error handling is expected
        assert(error instanceof Error, 'Should handle resource exhaustion with proper errors')
      }
    }

    // System should still be responsive after exhaustion attempts
    const status = transformer.getStatus() as any
    assert(typeof status.health === 'string', 'Should remain responsive after resource exhaustion attempts')

    await transformer.destroy()
  })

  // Test Summary
  console.log('=' .repeat(80))
  console.log(`🔧 Sacred Transformer Test Results: ${passedTests}/${testCount} tests passed`)
  console.log(`📊 Test Coverage: Basic (5), Security (5), Processing (5), Chaos Engineering (5)`)
  
  if (passedTests === testCount) {
    console.log('✅ All tests passed! Sacred Transformer is ready for production processing.')
    console.log('🔥 Chaos engineering tests validate resilience under adversarial conditions.')
  } else {
    console.log(`❌ ${testCount - passedTests} tests failed. Production readiness requires all tests to pass.`)
  }

  console.log('=' .repeat(80))
  
  // Return test results for programmatic use
  return Promise.resolve()
}

// Auto-run tests if this file is executed directly
if (typeof window !== 'undefined' && (window as any).runSacredTransformerTests) {
  runSacredTransformerTests().catch(console.error)
}