/**
 * TransformerSecurity - Sacred Transformer Security Framework
 * 
 * Implements comprehensive security measures for data transformation processing
 * Following Sacred Architecture security principles with battle-hardened protection
 */

// Security constraint types
export interface TransformerSecurityConstraints {
  readonly maxProcessingSize: number
  readonly maxProcessingTime: number
  readonly maxPipelineDepth: number
  readonly rateLimitOperations: number
  readonly rateLimitWindow: number
  readonly maxConcurrentOperations: number
  readonly memoryThreshold: number
}

export interface SecurityViolation {
  readonly violationType: 'rate_limit' | 'size_limit' | 'time_limit' | 'depth_limit' | 'memory_limit' | 'malicious_input'
  readonly timestamp: string
  readonly details: Record<string, unknown>
  readonly severity: 'low' | 'medium' | 'high' | 'critical'
  readonly blocked: boolean
}

export interface InputValidationResult {
  readonly isValid: boolean
  readonly violations: string[]
  readonly sanitizedData?: unknown
  readonly riskLevel: 'safe' | 'suspicious' | 'dangerous' | 'malicious'
}

export interface PerformanceMetrics {
  readonly operationId: string
  readonly startTime: number
  readonly endTime: number
  readonly memoryUsage: number
  readonly cpuUsage: number
  readonly operationType: string
}

/**
 * Sacred Transformer Security Guardian
 * 
 * Implements multi-layered security protection for Sacred Transformer
 * using performance monitoring and threat detection principles
 */
export class TransformerSecurity {
  // Security Constants - Battle-tested limits
  private static readonly DEFAULT_CONSTRAINTS: TransformerSecurityConstraints = {
    maxProcessingSize: 10 * 1024 * 1024, // 10MB
    maxProcessingTime: 30000, // 30 seconds
    maxPipelineDepth: 10, // Maximum chained transformations
    rateLimitOperations: 1000, // per minute
    rateLimitWindow: 60000, // 1 minute in ms
    maxConcurrentOperations: 50, // Maximum parallel operations
    memoryThreshold: 0.8 // 80% memory usage threshold
  }

  // Malicious pattern detection
  private static readonly MALICIOUS_PATTERNS = [
    // Code injection patterns
    /eval\s*\(/gi,
    /Function\s*\(/gi,
    /setTimeout\s*\(/gi,
    /setInterval\s*\(/gi,
    
    // XSS patterns
    /<script[^>]*>.*?<\/script>/gi,
    /javascript:/gi,
    /on\w+\s*=/gi,
    
    // SQL injection patterns
    /('|(\\')|(;)|(\\;)|(--)|(\s*(union|select|insert|delete|update|drop|create|alter|exec|execute)\s+))/gi,
    
    // Command injection patterns
    /(\||&|;|\$\(|\`)/g,
    
    // Path traversal patterns
    /\.\.[\/\\]/g,
    
    // Prototype pollution patterns
    /__proto__|constructor\.prototype|prototype\./gi,
    
    // ReDoS patterns (potentially dangerous regex)
    /(\(.*\+.*\)|\[.*\+.*\]|\{.*\+.*\})/g
  ]

  // Security state
  private constraints: TransformerSecurityConstraints
  private securityViolations: SecurityViolation[] = []
  private operationTimestamps: number[] = []
  private concurrentOperations = 0
  private performanceMetrics: PerformanceMetrics[] = []
  private isSecurityEnabled = true

  constructor(customConstraints?: Partial<TransformerSecurityConstraints>) {
    this.constraints = {
      ...TransformerSecurity.DEFAULT_CONSTRAINTS,
      ...customConstraints
    }
  }

  /**
   * Validate processing operation against security constraints
   */
  validateProcessingOperation(operationId: string, data: unknown): InputValidationResult {
    try {
      const violations: string[] = []
      let riskLevel: InputValidationResult['riskLevel'] = 'safe'

      // Check concurrent operations limit
      if (this.concurrentOperations >= this.constraints.maxConcurrentOperations) {
        violations.push(`Concurrent operations limit exceeded (${this.constraints.maxConcurrentOperations}). This prevents resource exhaustion.`)
        this.recordSecurityViolation('memory_limit', {
          operation_id: operationId,
          concurrent_operations: this.concurrentOperations,
          max_concurrent: this.constraints.maxConcurrentOperations
        }, 'high', true)
        riskLevel = 'dangerous'
      }

      // Check processing size
      const dataSize = this.calculateDataSize(data)
      if (dataSize > this.constraints.maxProcessingSize) {
        violations.push(`Processing size ${dataSize} exceeds maximum ${this.constraints.maxProcessingSize} bytes. This prevents memory exhaustion.`)
        this.recordSecurityViolation('size_limit', {
          operation_id: operationId,
          data_size: dataSize,
          max_size: this.constraints.maxProcessingSize
        }, 'high', true)
        riskLevel = 'dangerous'
      }

      // Check rate limiting
      if (!this.checkRateLimit()) {
        violations.push(`Rate limit exceeded (${this.constraints.rateLimitOperations} operations per minute). This prevents processing overload.`)
        this.recordSecurityViolation('rate_limit', {
          operation_id: operationId,
          current_rate: this.getCurrentOperationRate(),
          rate_limit: this.constraints.rateLimitOperations
        }, 'medium', true)
        riskLevel = 'dangerous'
      }

      // Validate input content
      const inputValidation = this.validateInputContent(data)
      if (!inputValidation.isValid) {
        violations.push(...inputValidation.violations)
        riskLevel = inputValidation.riskLevel
      }

      // Sanitize data if needed
      const sanitizedData = this.sanitizeInput(data)

      return {
        isValid: violations.length === 0,
        violations,
        sanitizedData,
        riskLevel
      }

    } catch (error) {
      return {
        isValid: false,
        violations: [`Processing validation failed: ${error instanceof Error ? error.message : 'Unknown error'}`],
        riskLevel: 'malicious'
      }
    }
  }

  /**
   * Start performance monitoring for an operation
   */
  startPerformanceMonitoring(operationId: string, operationType: string): void {
    const metrics: PerformanceMetrics = {
      operationId,
      startTime: Date.now(),
      endTime: 0,
      memoryUsage: this.getMemoryUsage(),
      cpuUsage: 0, // Would be implemented with actual CPU monitoring
      operationType
    }

    this.performanceMetrics.push(metrics)
    this.concurrentOperations++
  }

  /**
   * End performance monitoring for an operation
   */
  endPerformanceMonitoring(operationId: string): PerformanceMetrics | null {
    const metricsIndex = this.performanceMetrics.findIndex(m => m.operationId === operationId)
    if (metricsIndex === -1) {
      return null
    }

    const metrics = this.performanceMetrics[metricsIndex]
    metrics.endTime = Date.now()
    this.concurrentOperations = Math.max(0, this.concurrentOperations - 1)

    // Check for timeout violations
    const executionTime = metrics.endTime - metrics.startTime
    if (executionTime > this.constraints.maxProcessingTime) {
      this.recordSecurityViolation('time_limit', {
        operation_id: operationId,
        execution_time: executionTime,
        max_time: this.constraints.maxProcessingTime
      }, 'high', false) // Not blocked since operation completed
    }

    // Remove old metrics to prevent memory bloat
    if (this.performanceMetrics.length > 1000) {
      this.performanceMetrics.splice(0, 500) // Remove oldest 500 entries
    }

    return metrics
  }

  /**
   * Validate pipeline depth to prevent infinite loops
   */
  validatePipelineDepth(depth: number): boolean {
    if (depth > this.constraints.maxPipelineDepth) {
      this.recordSecurityViolation('depth_limit', {
        pipeline_depth: depth,
        max_depth: this.constraints.maxPipelineDepth
      }, 'critical', true)
      return false
    }
    return true
  }

  /**
   * Validate input content for malicious patterns
   */
  validateInputContent(data: unknown): InputValidationResult {
    const violations: string[] = []
    let riskLevel: InputValidationResult['riskLevel'] = 'safe'

    try {
      // Convert to string for pattern matching
      const dataString = JSON.stringify(data)

      // Check for malicious patterns
      for (const pattern of TransformerSecurity.MALICIOUS_PATTERNS) {
        if (pattern.test(dataString)) {
          violations.push(`Malicious pattern detected: ${pattern.source}`)
          riskLevel = 'malicious'
          
          this.recordSecurityViolation('malicious_input', {
            pattern: pattern.source,
            data_sample: dataString.substring(0, 100) + '...'
          }, 'critical', true)
        }
      }

      // Check for suspicious structures
      if (this.containsSuspiciousStructures(data)) {
        violations.push('Suspicious data structure detected (potential prototype pollution)')
        riskLevel = riskLevel === 'malicious' ? 'malicious' : 'suspicious'
      }

      // Check for excessive nesting
      if (this.hasExcessiveNesting(data)) {
        violations.push('Excessive object nesting detected (potential DoS attack)')
        riskLevel = riskLevel === 'malicious' ? 'malicious' : 'dangerous'
      }

      // Check for circular references
      if (this.hasCircularReferences(data)) {
        violations.push('Circular references detected (potential infinite loop)')
        riskLevel = riskLevel === 'malicious' ? 'malicious' : 'dangerous'
      }

      return {
        isValid: violations.length === 0,
        violations,
        riskLevel
      }

    } catch (error) {
      return {
        isValid: false,
        violations: [`Input content validation failed: ${error instanceof Error ? error.message : 'Unknown error'}`],
        riskLevel: 'malicious'
      }
    }
  }

  /**
   * Sanitize input data
   */
  sanitizeInput(data: unknown): unknown {
    try {
      if (typeof data === 'string') {
        // Remove potentially dangerous patterns
        return data
          .replace(/<script[^>]*>.*?<\/script>/gi, '')
          .replace(/javascript:/gi, '')
          .replace(/on\w+\s*=/gi, '')
          .replace(/eval\s*\(/gi, '')
          .replace(/Function\s*\(/gi, '')
          .trim()
      }

      if (typeof data === 'object' && data !== null) {
        // Deep clone and sanitize object
        return this.sanitizeObject(data)
      }

      return data

    } catch (error) {
      // If sanitization fails, return null for safety
      return null
    }
  }

  /**
   * Check rate limiting
   */
  checkRateLimit(): boolean {
    const now = Date.now()
    
    // Remove old timestamps outside the window
    this.operationTimestamps = this.operationTimestamps.filter(
      timestamp => now - timestamp < this.constraints.rateLimitWindow
    )

    // Check if we're under the limit
    if (this.operationTimestamps.length >= this.constraints.rateLimitOperations) {
      return false
    }

    // Add current timestamp
    this.operationTimestamps.push(now)
    return true
  }

  /**
   * Get current operation rate
   */
  getCurrentOperationRate(): number {
    const now = Date.now()
    const recentOperations = this.operationTimestamps.filter(
      timestamp => now - timestamp < this.constraints.rateLimitWindow
    )
    return recentOperations.length
  }

  /**
   * Get security status
   */
  getSecurityStatus(): Record<string, unknown> {
    const now = Date.now()
    const recentViolations = this.securityViolations.filter(
      violation => now - new Date(violation.timestamp).getTime() < this.constraints.rateLimitWindow
    )

    const recentMetrics = this.performanceMetrics.filter(
      metric => metric.endTime > 0 && now - metric.endTime < this.constraints.rateLimitWindow
    )

    return {
      component: 'TransformerSecurity',
      type: 'Security',
      
      // Security state
      security_state: {
        is_enabled: this.isSecurityEnabled,
        concurrent_operations: this.concurrentOperations,
        current_operation_rate: this.getCurrentOperationRate(),
        memory_usage: this.getMemoryUsage()
      },

      // Security constraints
      constraints: this.constraints,

      // Rate limiting state
      rate_limiting: {
        operations_in_window: this.operationTimestamps.length,
        window_size_ms: this.constraints.rateLimitWindow,
        utilization: this.getCurrentOperationRate() / this.constraints.rateLimitOperations
      },

      // Security violations
      security_violations: {
        total_violations: this.securityViolations.length,
        recent_violations: recentViolations.length,
        violation_types: this.getViolationTypeCounts(),
        severity_distribution: this.getSeverityDistribution()
      },

      // Performance monitoring
      performance_monitoring: {
        active_operations: this.concurrentOperations,
        recent_operations: recentMetrics.length,
        average_execution_time: this.calculateAverageExecutionTime(recentMetrics),
        memory_threshold_status: this.getMemoryUsage() < this.constraints.memoryThreshold
      },

      // Security health
      security_health: {
        violation_rate: recentViolations.length / Math.max(1, this.getCurrentOperationRate()),
        resource_utilization: this.concurrentOperations / this.constraints.maxConcurrentOperations,
        rate_limit_utilization: this.getCurrentOperationRate() / this.constraints.rateLimitOperations,
        overall_health: this.calculateSecurityHealth()
      },

      timestamp: new Date().toISOString()
    }
  }

  /**
   * Reset security state
   */
  resetSecurityState(): void {
    this.operationTimestamps = []
    this.securityViolations = []
    this.performanceMetrics = []
    this.concurrentOperations = 0
  }

  /**
   * Enable/disable security
   */
  setSecurityEnabled(enabled: boolean): void {
    this.isSecurityEnabled = enabled
  }

  // Private helper methods

  private calculateDataSize(data: unknown): number {
    try {
      return JSON.stringify(data).length
    } catch (error) {
      // If JSON.stringify fails, estimate size
      return String(data).length
    }
  }

  private getMemoryUsage(): number {
    // Simplified memory usage estimation
    // In a real implementation, this would use actual memory monitoring
    return Math.random() * 0.5 // Simulate 0-50% memory usage
  }

  private containsSuspiciousStructures(data: unknown): boolean {
    if (typeof data !== 'object' || data === null) {
      return false
    }

    const dataString = JSON.stringify(data)
    return dataString.includes('__proto__') || 
           dataString.includes('constructor') || 
           dataString.includes('prototype')
  }

  private hasExcessiveNesting(data: unknown, depth = 0): boolean {
    const MAX_DEPTH = 20

    if (depth > MAX_DEPTH) {
      return true
    }

    if (typeof data === 'object' && data !== null) {
      for (const value of Object.values(data)) {
        if (this.hasExcessiveNesting(value, depth + 1)) {
          return true
        }
      }
    }

    return false
  }

  private hasCircularReferences(data: unknown, seen = new WeakSet()): boolean {
    if (typeof data !== 'object' || data === null) {
      return false
    }

    if (seen.has(data)) {
      return true
    }

    seen.add(data)

    for (const value of Object.values(data)) {
      if (this.hasCircularReferences(value, seen)) {
        return true
      }
    }

    seen.delete(data)
    return false
  }

  private sanitizeObject(obj: unknown): unknown {
    if (typeof obj !== 'object' || obj === null) {
      return obj
    }

    const sanitized: Record<string, unknown> = {}
    
    for (const [key, value] of Object.entries(obj)) {
      // Skip dangerous keys
      if (key === '__proto__' || key === 'constructor' || key === 'prototype') {
        continue
      }

      // Recursively sanitize values
      if (typeof value === 'object' && value !== null) {
        sanitized[key] = this.sanitizeObject(value)
      } else if (typeof value === 'string') {
        sanitized[key] = this.sanitizeInput(value)
      } else {
        sanitized[key] = value
      }
    }

    return sanitized
  }

  private recordSecurityViolation(
    type: SecurityViolation['violationType'],
    details: Record<string, unknown>,
    severity: SecurityViolation['severity'],
    blocked: boolean
  ): void {
    const violation: SecurityViolation = {
      violationType: type,
      timestamp: new Date().toISOString(),
      details,
      severity,
      blocked
    }

    this.securityViolations.push(violation)

    // Keep only recent violations to prevent memory bloat
    const cutoff = Date.now() - (24 * 60 * 60 * 1000) // 24 hours
    this.securityViolations = this.securityViolations.filter(
      v => new Date(v.timestamp).getTime() > cutoff
    )
  }

  private getViolationTypeCounts(): Record<string, number> {
    const counts: Record<string, number> = {}
    
    for (const violation of this.securityViolations) {
      counts[violation.violationType] = (counts[violation.violationType] || 0) + 1
    }

    return counts
  }

  private getSeverityDistribution(): Record<string, number> {
    const distribution: Record<string, number> = {}
    
    for (const violation of this.securityViolations) {
      distribution[violation.severity] = (distribution[violation.severity] || 0) + 1
    }

    return distribution
  }

  private calculateAverageExecutionTime(metrics: PerformanceMetrics[]): number {
    if (metrics.length === 0) return 0

    const totalTime = metrics.reduce((sum, metric) => sum + (metric.endTime - metric.startTime), 0)
    return totalTime / metrics.length
  }

  private calculateSecurityHealth(): 'secure' | 'monitored' | 'threatened' | 'compromised' {
    const recentViolations = this.securityViolations.filter(
      violation => Date.now() - new Date(violation.timestamp).getTime() < this.constraints.rateLimitWindow
    )

    const criticalViolations = recentViolations.filter(v => v.severity === 'critical').length
    const highViolations = recentViolations.filter(v => v.severity === 'high').length
    const totalViolations = recentViolations.length

    if (criticalViolations > 0) {
      return 'compromised'
    }

    if (highViolations > 3 || totalViolations > 10) {
      return 'threatened'
    }

    if (totalViolations > 0) {
      return 'monitored'
    }

    return 'secure'
  }
}

/**
 * Factory function for creating transformer security instances
 */
export function createTransformerSecurity(constraints?: Partial<TransformerSecurityConstraints>): TransformerSecurity {
  return new TransformerSecurity(constraints)
}

/**
 * Type guard for transformer security
 */
export function isTransformerSecurity(security: unknown): security is TransformerSecurity {
  return security instanceof TransformerSecurity
}