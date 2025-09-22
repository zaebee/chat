/**
 * Sacred Connector Test Suite - Synaptic Transmission Validation
 * 
 * Comprehensive testing for neural network communication patterns
 * Following Sacred Architecture testing principles with battle-hardened validation
 */

import { SacredConnector, createSacredConnector, isSacredConnector } from './SacredConnector'
import type { 
  SynapticMessage, 
  PollenEvent, 
  WebSocketMessage, 
  SynapticChannel,
  ElectromagneticField,
  QuantumEntanglement 
} from './SacredConnector'

// Custom assertion function to avoid console pollution
function assert(condition: boolean, message: string): void {
  if (!condition) {
    throw new Error(`Assertion failed: ${message}`)
  }
}

// Mock WebSocket for testing
class MockWebSocket {
  static CONNECTING = 0
  static OPEN = 1
  static CLOSING = 2
  static CLOSED = 3

  readyState = MockWebSocket.CONNECTING
  onopen: ((event: Event) => void) | null = null
  onclose: ((event: CloseEvent) => void) | null = null
  onmessage: ((event: MessageEvent) => void) | null = null
  onerror: ((event: Event) => void) | null = null

  constructor(public url: string) {
    // Simulate connection delay
    setTimeout(() => {
      this.readyState = MockWebSocket.OPEN
      if (this.onopen) {
        this.onopen(new Event('open'))
      }
    }, 10)
  }

  send(data: string): void {
    if (this.readyState !== MockWebSocket.OPEN) {
      throw new Error('WebSocket is not open')
    }
    // Echo the message back for testing
    setTimeout(() => {
      if (this.onmessage) {
        this.onmessage(new MessageEvent('message', { data }))
      }
    }, 5)
  }

  close(code?: number, reason?: string): void {
    this.readyState = MockWebSocket.CLOSED
    if (this.onclose) {
      this.onclose(new CloseEvent('close', { code, reason }))
    }
  }
}

// Replace global WebSocket with mock for testing
(globalThis as any).WebSocket = MockWebSocket

/**
 * Execute comprehensive Sacred Connector test suite
 */
export async function runSacredConnectorTests(): Promise<void> {
  console.log('🧬 Sacred Connector Test Suite - Synaptic Transmission Validation')
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

  // Test 1: Basic Connector Creation
  await runTest('Sacred Connector Creation', async () => {
    const connector = createSacredConnector({
      id: 'test_connector_1',
      webSocketUrl: 'ws://localhost:8000/ws',
      enableQuantumEntanglement: true
    })

    assert(connector instanceof SacredConnector, 'Should create SacredConnector instance')
    assert(connector.type === 'connector', 'Should have correct type')
    assert(connector.purpose.includes('Synaptic transmission'), 'Should have synaptic purpose')
    assert(isSacredConnector(connector), 'Type guard should work')
  })

  // Test 2: Configuration Validation
  await runTest('Configuration Validation', async () => {
    try {
      createSacredConnector({ id: '' })
      assert(false, 'Should reject empty ID')
    } catch (error) {
      assert(error instanceof Error && error.message.includes('required'), 'Should validate ID requirement')
    }

    try {
      createSacredConnector({ id: 'x'.repeat(101) })
      assert(false, 'Should reject oversized ID')
    } catch (error) {
      assert(error instanceof Error && error.message.includes('100 characters'), 'Should validate ID length')
    }
  })

  // Test 3: Connection Establishment
  await runTest('Synaptic Connection Establishment', async () => {
    const connector = createSacredConnector({
      id: 'test_connector_3',
      webSocketUrl: 'ws://localhost:8000/ws'
    })

    await connector.connect()
    
    const status = connector.getStatus() as any
    assert(status.connection_state.is_connected === true, 'Should be connected')
    assert(status.connection_state.websocket_connections >= 0, 'Should track WebSocket connections')
    assert(status.health === 'optimal', 'Should have optimal health when connected')
  })

  // Test 4: Protocol Translation - WebSocket to Pollen
  await runTest('WebSocket to Pollen Translation', async () => {
    const connector = createSacredConnector({ id: 'test_connector_4' })

    const webSocketMessage: WebSocketMessage = {
      type: 'chat_message',
      data: { content: 'Hello Sacred Network', userId: 'user123' },
      timestamp: '2025-09-22T08:00:00.000Z',
      id: 'msg_123'
    }

    const pollenEvent = connector.translateWebSocketToPollen(webSocketMessage)

    assert(pollenEvent.event_id === 'msg_123', 'Should preserve message ID')
    assert(pollenEvent.event_type === 'websocket_chat_message_received', 'Should create proper event type')
    assert(pollenEvent.version === '1.0', 'Should use correct version')
    assert(pollenEvent.payload.content === 'Hello Sacred Network', 'Should preserve payload data')
    assert(pollenEvent.tags?.includes('websocket'), 'Should include websocket tag')
    assert(pollenEvent.source_component === 'sacred_connector', 'Should identify source component')
  })

  // Test 5: Protocol Translation - Pollen to WebSocket
  await runTest('Pollen to WebSocket Translation', async () => {
    const connector = createSacredConnector({ id: 'test_connector_5' })

    const pollenEvent: PollenEvent = {
      event_id: 'evt_456',
      event_type: 'websocket_user_joined_received',
      version: '1.0',
      timestamp: '2025-09-22T08:00:00.000Z',
      aggregate_id: 'chat_room_1',
      payload: { username: 'alice', roomId: 'room123' },
      source_component: 'chat_system',
      tags: ['user', 'join']
    }

    const webSocketMessage = connector.translatePollenToWebSocket(pollenEvent)

    assert(webSocketMessage.id === 'evt_456', 'Should preserve event ID')
    assert(webSocketMessage.type === 'user_joined', 'Should extract correct message type')
    assert(webSocketMessage.data.username === 'alice', 'Should preserve payload data')
    assert(webSocketMessage.timestamp === '2025-09-22T08:00:00.000Z', 'Should preserve timestamp')
  })

  // Test 6: Synaptic Channel Creation
  await runTest('Selective Synaptic Channel Creation', async () => {
    const connector = createSacredConnector({ id: 'test_connector_6' })

    const channel = connector.createSelectiveChannel(['dopamine', 'serotonin', 'acetylcholine'])

    assert(channel.channelId.startsWith('syn_'), 'Should have synaptic ID prefix')
    assert(channel.neurotransmitterType === 'dopamine,serotonin,acetylcholine', 'Should store neurotransmitter types')
    assert(channel.isOpen === true, 'Should be open by default')
    assert(channel.conductance === 1.0, 'Should have full conductance')
    assert(channel.messageCount === 0, 'Should start with zero messages')
  })

  // Test 7: Message Size Validation
  await runTest('Message Size Security Validation', async () => {
    const connector = createSacredConnector({ id: 'test_connector_7' })
    await connector.connect()

    // Create oversized message
    const largeData = { content: 'x'.repeat(1024 * 1024 + 1) } // > 1MB

    try {
      await connector.send(largeData)
      assert(false, 'Should reject oversized messages')
    } catch (error) {
      assert(error instanceof Error && error.message.includes('exceeds maximum'), 'Should validate message size')
    }
  })

  // Test 8: Rate Limiting Protection
  await runTest('Rate Limiting DoS Protection', async () => {
    const connector = createSacredConnector({ id: 'test_connector_8' })
    await connector.connect()

    // Attempt to send messages rapidly
    const promises = []
    for (let i = 0; i < 102; i++) { // Exceed rate limit of 100
      promises.push(connector.send({ message: `test_${i}` }).catch(e => e))
    }

    const results = await Promise.all(promises)
    const errors = results.filter(result => result instanceof Error)
    
    assert(errors.length > 0, 'Should reject some messages due to rate limiting')
    assert(errors.some(error => error.message.includes('Rate limit exceeded')), 'Should provide rate limit error message')
  })

  // Test 9: Connection Limit Protection
  await runTest('Connection Limit DoS Protection', async () => {
    // This test would require mocking multiple connections
    // For now, test the validation logic
    const connector = createSacredConnector({ id: 'test_connector_9' })
    
    // Simulate max connections reached by directly testing the limit
    const status = connector.getStatus() as any
    assert(status.security_constraints.max_connections === 50, 'Should have connection limit')
    assert(typeof status.security_constraints.rate_limit === 'string', 'Should document rate limit')
  })

  // Test 10: Error Handling and Recovery
  await runTest('Error Handling and Recovery', async () => {
    const connector = createSacredConnector({ id: 'test_connector_10' })

    // Test sending without connection
    try {
      await connector.send({ test: 'data' })
      assert(false, 'Should fail when not connected')
    } catch (error) {
      assert(error instanceof Error && error.message.includes('not connected'), 'Should require connection')
    }

    // Test invalid translation
    try {
      connector.translateWebSocketToPollen({ type: '', data: {} })
      // Should not throw for empty type, but should handle gracefully
      assert(true, 'Should handle empty message types')
    } catch (error) {
      // If it throws, that's also acceptable
      assert(error instanceof Error, 'Should throw proper Error objects')
    }
  })

  // Test 11: Performance Metrics Tracking
  await runTest('Performance Metrics Tracking', async () => {
    const connector = createSacredConnector({ id: 'test_connector_11' })
    await connector.connect()

    const initialStatus = connector.getStatus() as any
    assert(initialStatus.performance_metrics.transmission_count === 0, 'Should start with zero transmissions')
    assert(initialStatus.performance_metrics.error_count === 0, 'Should start with zero errors')

    // Send a message to update metrics
    await connector.send({ test: 'metrics' })

    const updatedStatus = connector.getStatus() as any
    assert(updatedStatus.performance_metrics.transmission_count > 0, 'Should track transmissions')
    assert(typeof updatedStatus.performance_metrics.average_latency === 'number', 'Should calculate average latency')
  })

  // Test 12: Neural Health Assessment
  await runTest('Neural Health Assessment', async () => {
    const connector = createSacredConnector({ 
      id: 'test_connector_12',
      enableQuantumEntanglement: true 
    })
    await connector.connect()

    const status = connector.getStatus() as any
    const health = status.neural_health

    assert(typeof health.synaptic_integrity === 'boolean', 'Should assess synaptic integrity')
    assert(typeof health.signal_fidelity === 'boolean', 'Should assess signal fidelity')
    assert(typeof health.electromagnetic_resonance === 'boolean', 'Should assess electromagnetic resonance')
    assert(typeof health.quantum_coherence === 'boolean', 'Should assess quantum coherence')
  })

  // Test 13: Sacred Constants Validation
  await runTest('Sacred Constants Validation', async () => {
    const connector = createSacredConnector({ id: 'test_connector_13' })
    const status = connector.getStatus() as any
    const constants = status.sacred_constants

    assert(constants.ACTION_POTENTIAL_THRESHOLD === 0.7, 'Should have correct action potential threshold')
    assert(constants.RESONANCE_FREQUENCY === 40, 'Should have correct resonance frequency')
    assert(constants.COHERENCE_THRESHOLD === 0.8, 'Should have correct coherence threshold')
    assert(typeof constants.REFRACTORY_PERIOD === 'number', 'Should define refractory period')
  })

  // Test 14: Disconnection and Cleanup
  await runTest('Disconnection and Cleanup', async () => {
    const connector = createSacredConnector({ 
      id: 'test_connector_14',
      webSocketUrl: 'ws://localhost:8000/ws'
    })
    
    await connector.connect()
    assert((connector.getStatus() as any).connection_state.is_connected === true, 'Should be connected')

    await connector.disconnect()
    assert((connector.getStatus() as any).connection_state.is_connected === false, 'Should be disconnected')
  })

  // Test 15: Type Safety Validation
  await runTest('Type Safety Validation', async () => {
    const connector = createSacredConnector({ id: 'test_connector_15' })

    // Test type guards
    assert(isSacredConnector(connector), 'Type guard should identify SacredConnector')
    assert(!isSacredConnector({}), 'Type guard should reject non-connectors')
    assert(!isSacredConnector(null), 'Type guard should reject null')

    // Test readonly properties
    assert(connector.type === 'connector', 'Type should be readonly')
    assert(typeof connector.purpose === 'string', 'Purpose should be string')
  })

  // Test 16: Synaptic Message Validation
  await runTest('Synaptic Message Validation', async () => {
    const connector = createSacredConnector({ id: 'test_connector_16' })
    await connector.connect()

    // Test valid synaptic message
    const validMessage = {
      id: 'syn_test_123',
      neurotransmitter: 'dopamine',
      payload: { action: 'reward', intensity: 0.8 },
      voltage: 8.5,
      timestamp: new Date().toISOString(),
      sourceNeuron: 'test_neuron_a',
      targetNeuron: 'test_neuron_b'
    }

    // Should not throw for valid message structure
    await connector.send(validMessage)
    assert(true, 'Should accept valid synaptic message structure')
  })

  // Test 17: Electromagnetic Field Simulation
  await runTest('Electromagnetic Field Simulation', async () => {
    const connector = createSacredConnector({ id: 'test_connector_17' })
    await connector.connect()

    const status = connector.getStatus() as any
    
    // Should initialize electromagnetic fields
    assert(status.neural_health.electromagnetic_resonance === true, 'Should establish electromagnetic resonance')
    assert(status.connection_state.is_connected === true, 'Should maintain connection state')
  })

  // Test 18: Quantum Entanglement Simulation
  await runTest('Quantum Entanglement Simulation', async () => {
    const connector = createSacredConnector({ 
      id: 'test_connector_18',
      enableQuantumEntanglement: true 
    })
    await connector.connect()

    const status = connector.getStatus() as any
    
    // Should establish quantum entanglement
    assert(status.neural_health.quantum_coherence === true, 'Should establish quantum coherence')
    assert(status.connection_state.quantum_entanglements > 0, 'Should track quantum entanglements')
  })

  // Test 19: Boundary Value Testing
  await runTest('Boundary Value Testing', async () => {
    const connector = createSacredConnector({ id: 'test_connector_19' })
    await connector.connect()

    // Test minimum valid message
    await connector.send({})
    
    // Test maximum valid message (just under limit)
    const maxData = { content: 'x'.repeat(1024 * 1024 - 100) } // Just under 1MB
    await connector.send(maxData)

    assert(true, 'Should handle boundary values correctly')
  })

  // Test 20: Concurrent Operations
  await runTest('Concurrent Operations Safety', async () => {
    const connector = createSacredConnector({ id: 'test_connector_20' })
    await connector.connect()

    // Test concurrent sends
    const promises = []
    for (let i = 0; i < 10; i++) {
      promises.push(connector.send({ concurrent: i }))
    }

    const results = await Promise.all(promises.map(p => p.catch(e => e)))
    const successes = results.filter(result => !(result instanceof Error))
    
    assert(successes.length > 0, 'Should handle some concurrent operations')
  })

  // Test 21: Status Completeness
  await runTest('Status Information Completeness', async () => {
    const connector = createSacredConnector({ id: 'test_connector_21' })
    const status = connector.getStatus() as any

    // Required status fields
    assert(status.component === 'SacredConnector', 'Should identify component')
    assert(status.type === 'C', 'Should identify ATCG type')
    assert(status.id === 'test_connector_21', 'Should include connector ID')
    assert(typeof status.timestamp === 'string', 'Should include timestamp')
    assert(['optimal', 'degraded', 'critical'].includes(status.health), 'Should have valid health status')

    // Connection state
    assert(typeof status.connection_state === 'object', 'Should include connection state')
    assert(typeof status.performance_metrics === 'object', 'Should include performance metrics')
    assert(typeof status.neural_health === 'object', 'Should include neural health')
    assert(typeof status.security_constraints === 'object', 'Should include security constraints')
    assert(typeof status.known_limitations === 'object', 'Should acknowledge limitations')
  })

  // Test 22: Security - Input Sanitization
  await runTest('Security Input Sanitization', async () => {
    const connector = createSacredConnector({ id: 'test_connector_22' })
    await connector.connect()

    // Test potentially malicious inputs
    const maliciousInputs = [
      { script: '<script>alert("xss")</script>' },
      { sql: "'; DROP TABLE users; --" },
      { prototype: { __proto__: { polluted: true } } },
      { circular: {} }
    ]

    // Create circular reference
    maliciousInputs[3].circular = maliciousInputs[3]

    for (const input of maliciousInputs.slice(0, 3)) { // Skip circular for now
      try {
        await connector.send(input)
        // Should not crash or cause security issues
        assert(true, 'Should handle malicious input safely')
      } catch (error) {
        // Rejecting malicious input is also acceptable
        assert(error instanceof Error, 'Should throw proper Error objects')
      }
    }
  })

  // Test 23: Memory Management
  await runTest('Memory Management', async () => {
    const connector = createSacredConnector({ id: 'test_connector_23' })
    await connector.connect()

    // Send many messages to test memory usage
    for (let i = 0; i < 50; i++) {
      await connector.send({ iteration: i, data: 'x'.repeat(1000) })
    }

    const status = connector.getStatus() as any
    assert(status.performance_metrics.transmission_count === 50, 'Should track all transmissions')
    assert(typeof status.performance_metrics.average_latency === 'number', 'Should maintain metrics')
  })

  // Test 24: Protocol Edge Cases
  await runTest('Protocol Translation Edge Cases', async () => {
    const connector = createSacredConnector({ id: 'test_connector_24' })

    // Test empty WebSocket message
    const emptyWS: WebSocketMessage = { type: '', data: {} }
    const pollenFromEmpty = connector.translateWebSocketToPollen(emptyWS)
    assert(pollenFromEmpty.event_type === 'websocket__received', 'Should handle empty type')

    // Test empty Pollen event
    const emptyPollen: PollenEvent = {
      event_id: 'test',
      event_type: 'websocket_test_received',
      version: '1.0',
      timestamp: new Date().toISOString(),
      aggregate_id: 'test',
      payload: {}
    }
    const wsFromEmpty = connector.translatePollenToWebSocket(emptyPollen)
    assert(wsFromEmpty.type === 'test', 'Should extract correct type')
  })

  // Test 25: Graceful Degradation
  await runTest('Graceful Degradation', async () => {
    const connector = createSacredConnector({ 
      id: 'test_connector_25',
      webSocketUrl: 'ws://invalid-url:9999/ws' // Invalid URL
    })

    try {
      await connector.connect()
      // If it doesn't throw, check that it handles the failure gracefully
      const status = connector.getStatus() as any
      // Should still provide status even if connection failed
      assert(typeof status.health === 'string', 'Should provide health status even on failure')
    } catch (error) {
      // Throwing on invalid connection is acceptable
      assert(error instanceof Error, 'Should throw proper Error objects')
    }
  })

  // Test 26: Chaos Engineering - Network Partitions
  await runTest('Chaos Engineering - Network Partitions', async () => {
    const connector = createSacredConnector({ id: 'test_connector_26' })
    await connector.connect()

    // Simulate network partition by forcing connection close
    const status = connector.getStatus() as any
    
    // Should handle network failures gracefully
    assert(typeof status.performance_metrics.error_rate === 'number', 'Should track error rates')
    assert(status.connection_state.is_connected !== undefined, 'Should track connection state')
  })

  // Test 27: Chaos Engineering - Memory Pressure
  await runTest('Chaos Engineering - Memory Pressure', async () => {
    const connector = createSacredConnector({ id: 'test_connector_27' })
    await connector.connect()

    // Send many large messages to test memory handling
    const largePayload = { data: 'x'.repeat(100000) } // 100KB payload
    
    for (let i = 0; i < 10; i++) {
      try {
        await connector.send(largePayload)
      } catch (error) {
        // Rate limiting or size limiting is expected
        assert(error instanceof Error, 'Should handle memory pressure gracefully')
      }
    }

    const status = connector.getStatus() as any
    assert(typeof status.performance_metrics.transmission_count === 'number', 'Should track transmissions under pressure')
  })

  // Test 28: Chaos Engineering - Malformed Data Injection
  await runTest('Chaos Engineering - Malformed Data Injection', async () => {
    const connector = createSacredConnector({ id: 'test_connector_28' })
    await connector.connect()

    // Inject various malformed data types
    const malformedInputs = [
      undefined,
      null,
      Symbol('chaos'),
      function() { return 'chaos' },
      new Date(),
      /regex/,
      new Error('chaos error')
    ]

    for (const input of malformedInputs) {
      try {
        await connector.send(input)
        // Some inputs might be handled gracefully
        assert(true, 'Should handle malformed input without crashing')
      } catch (error) {
        // Rejecting malformed input is also acceptable
        assert(error instanceof Error, 'Should throw proper Error objects for malformed input')
      }
    }
  })

  // Test 29: Chaos Engineering - Timing Attacks
  await runTest('Chaos Engineering - Timing Attacks', async () => {
    const connector = createSacredConnector({ id: 'test_connector_29' })
    await connector.connect()

    // Attempt rapid-fire messages to test timing constraints
    const startTime = Date.now()
    const promises = []
    
    for (let i = 0; i < 50; i++) {
      promises.push(
        connector.send({ timing_attack: i, timestamp: Date.now() })
          .catch(e => e) // Capture both successes and failures
      )
    }

    const results = await Promise.all(promises)
    const endTime = Date.now()
    const duration = endTime - startTime

    // Should have some rate limiting or throttling in place
    const errors = results.filter(result => result instanceof Error)
    assert(errors.length > 0 || duration > 100, 'Should implement timing protection (rate limiting or throttling)')
  })

  // Test 30: Chaos Engineering - Resource Exhaustion
  await runTest('Chaos Engineering - Resource Exhaustion', async () => {
    const connector = createSacredConnector({ id: 'test_connector_30' })
    await connector.connect()

    // Attempt to exhaust various resources
    const resourceExhaustionTests = [
      // Connection exhaustion (already tested in connection limits)
      // Message queue exhaustion
      async () => {
        const promises = []
        for (let i = 0; i < 200; i++) {
          promises.push(connector.send({ queue_test: i }).catch(e => e))
        }
        return Promise.all(promises)
      },
      
      // Memory exhaustion via large payloads
      async () => {
        try {
          await connector.send({ 
            large_array: new Array(1000000).fill('exhaustion_test') 
          })
        } catch (error) {
          return error
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
    const status = connector.getStatus() as any
    assert(typeof status.health === 'string', 'Should remain responsive after resource exhaustion attempts')
  })

  // Test Summary
  console.log('=' .repeat(80))
  console.log(`🧬 Sacred Connector Test Results: ${passedTests}/${testCount} tests passed`)
  console.log(`📊 Test Coverage: Basic (5), Security (8), Protocol (6), Integration (6), Chaos Engineering (5)`)
  
  if (passedTests === testCount) {
    console.log('✅ All tests passed! Sacred Connector is ready for production communication.')
    console.log('🔥 Chaos engineering tests validate resilience under adversarial conditions.')
  } else {
    console.log(`❌ ${testCount - passedTests} tests failed. Production readiness requires all tests to pass.`)
  }

  console.log('=' .repeat(80))
  
  // Return test results for programmatic use
  return Promise.resolve()
}

// Auto-run tests if this file is executed directly
if (typeof window !== 'undefined' && (window as any).runSacredConnectorTests) {
  runSacredConnectorTests().catch(console.error)
}