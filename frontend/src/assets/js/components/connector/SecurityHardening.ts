/**
 * SecurityHardening - Sacred Connector Security Framework
 * 
 * Implements comprehensive security measures for synaptic communication
 * Following Sacred Architecture security principles with battle-hardened protection
 */

// Security constraint types
export interface SecurityConstraints {
  readonly maxConnections: number
  readonly maxMessageSize: number
  readonly rateLimitMessages: number
  readonly rateLimitWindow: number
  readonly maxReconnectAttempts: number
  readonly connectionTimeout: number
  readonly messageTimeout: number
}

export interface RateLimitState {
  readonly messageTimestamps: number[]
  readonly connectionAttempts: number[]
  readonly lastReset: number
  readonly currentRate: number
  readonly isLimited: boolean
}

export interface SecurityViolation {
  readonly violationType: 'rate_limit' | 'size_limit' | 'connection_limit' | 'timeout' | 'malicious_input'
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

/**
 * Sacred Security Guardian
 * 
 * Implements multi-layered security protection for Sacred Connector
 * using electromagnetic field theory and quantum security principles
 */
export class SecurityHardening {
  // Security Constants - Battle-tested limits
  private static readonly DEFAULT_CONSTRAINTS: SecurityConstraints = {
    maxConnections: 50,
    maxMessageSize: 1024 * 1024, // 1MB
    rateLimitMessages: 100, // per minute
    rateLimitWindow: 60000, // 1 minute in ms
    maxReconnectAttempts: 5,
    connectionTimeout: 30000, // 30 seconds
    messageTimeout: 10000 // 10 seconds
  }

  // Malicious pattern detection
  private static readonly MALICIOUS_PATTERNS = [
    // XSS patterns
    /<script[^>]*>.*?<\/script>/gi,
    /javascript:/gi,
    /on\w+\s*=/gi,
    
    // SQL injection patterns
    /('|(\\')|(;)|(\\;)|(--)|(\s*(union|select|insert|delete|update|drop|create|alter|exec|execute)\s+)/gi,
    
    // Command injection patterns
    /(\||&|;|\$\(|\`)/g,
    
    // Path traversal patterns
    /\.\.[\/\\]/g,
    
    // Prototype pollution patterns
    /__proto__|constructor\.prototype|prototype\./gi
  ]

  // Security state
  private constraints: SecurityConstraints
  private rateLimitState: RateLimitState
  private securityViolations: SecurityViolation[] = []
  private connectionCount = 0
  private isSecurityEnabled = true

  constructor(customConstraints?: Partial<SecurityConstraints>) {
    this.constraints = {
      ...SecurityHardening.DEFAULT_CONSTRAINTS,
      ...customConstraints
    }

    this.rateLimitState = {
      messageTimestamps: [],
      connectionAttempts: [],
      lastReset: Date.now(),
      currentRate: 0,
      isLimited: false
    }
  }

  /**
   * Validate connection attempt against security constraints
   */
  validateConnectionAttempt(connectionId: string): InputValidationResult {
    try {
      const violations: string[] = []

      // Check connection limit
      if (this.connectionCount >= this.constraints.maxConnections) {
        violations.push(`Connection limit exceeded (${this.constraints.maxConnections}). This prevents resource exhaustion.`)
        this.recordSecurityViolation('connection_limit', {
          connection_id: connectionId,
          current_connections: this.connectionCount,
          max_connections: this.constraints.maxConnections
        }, 'high', true)
      }

      // Check connection rate limiting
      const now = Date.now()
      this.rateLimitState.connectionAttempts = this.rateLimitState.connectionAttempts.filter(
        timestamp => now - timestamp < this.constraints.rateLimitWindow
      )

      if (this.rateLimitState.connectionAttempts.length >= this.constraints.rateLimitMessages) {
        violations.push(`Connection rate limit exceeded. This prevents connection flooding attacks.`)
        this.recordSecurityViolation('rate_limit', {
          connection_id: connectionId,
          attempts_in_window: this.rateLimitState.connectionAttempts.length,
          rate_limit: this.constraints.rateLimitMessages
        }, 'medium', true)
      }

      // Add current attempt to tracking
      this.rateLimitState.connectionAttempts.push(now)

      return {
        isValid: violations.length === 0,
        violations,
        riskLevel: violations.length > 0 ? 'dangerous' : 'safe'
      }

    } catch (error) {
      return {
        isValid: false,
        violations: [`Security validation failed: ${error instanceof Error ? error.message : 'Unknown error'}`],
        riskLevel: 'malicious'
      }
    }
  }

  /**
   * Validate message against security constraints
   */
  validateMessage(data: unknown, messageId?: string): InputValidationResult {
    try {
      const violations: string[] = []
      let riskLevel: InputValidationResult['riskLevel'] = 'safe'

      // Validate message size
      const messageSize = this.calculateMessageSize(data)
      if (messageSize > this.constraints.maxMessageSize) {
        violations.push(`Message size ${messageSize} exceeds maximum ${this.constraints.maxMessageSize} bytes. This prevents memory exhaustion.`)
        this.recordSecurityViolation('size_limit', {
          message_id: messageId,
          message_size: messageSize,
          max_size: this.constraints.maxMessageSize
        }, 'high', true)
        riskLevel = 'dangerous'
      }

      // Check rate limiting
      if (!this.checkRateLimit()) {
        violations.push(`Rate limit exceeded (${this.constraints.rateLimitMessages} messages per minute). This prevents network flooding.`)
        this.recordSecurityViolation('rate_limit', {
          message_id: messageId,
          current_rate: this.getCurrentMessageRate(),
          rate_limit: this.constraints.rateLimitMessages
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
        violations: [`Message validation failed: ${error instanceof Error ? error.message : 'Unknown error'}`],
        riskLevel: 'malicious'
      }
    }
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
      for (const pattern of SecurityHardening.MALICIOUS_PATTERNS) {
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
        // Remove potentially dangerous characters
        return data
          .replace(/<script[^>]*>.*?<\/script>/gi, '')
          .replace(/javascript:/gi, '')
          .replace(/on\w+\s*=/gi, '')
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
    this.rateLimitState.messageTimestamps = this.rateLimitState.messageTimestamps.filter(
      timestamp => now - timestamp < this.constraints.rateLimitWindow
    )

    // Check if we're under the limit
    if (this.rateLimitState.messageTimestamps.length >= this.constraints.rateLimitMessages) {
      this.rateLimitState.isLimited = true
      return false
    }

    // Add current timestamp
    this.rateLimitState.messageTimestamps.push(now)
    this.rateLimitState.currentRate = this.rateLimitState.messageTimestamps.length
    this.rateLimitState.isLimited = false
    return true
  }

  /**
   * Register new connection
   */
  registerConnection(connectionId: string): void {
    this.connectionCount++
  }

  /**
   * Unregister connection
   */
  unregisterConnection(connectionId: string): void {
    this.connectionCount = Math.max(0, this.connectionCount - 1)
  }

  /**
   * Get current message rate
   */
  getCurrentMessageRate(): number {
    const now = Date.now()
    const recentMessages = this.rateLimitState.messageTimestamps.filter(
      timestamp => now - timestamp < this.constraints.rateLimitWindow
    )
    return recentMessages.length
  }

  /**
   * Get security status
   */
  getSecurityStatus(): Record<string, unknown> {
    const now = Date.now()
    const recentViolations = this.securityViolations.filter(
      violation => now - new Date(violation.timestamp).getTime() < this.constraints.rateLimitWindow
    )

    return {
      component: 'SecurityHardening',
      type: 'Security',
      
      // Security state
      security_state: {
        is_enabled: this.isSecurityEnabled,
        connection_count: this.connectionCount,
        current_message_rate: this.getCurrentMessageRate(),
        is_rate_limited: this.rateLimitState.isLimited
      },

      // Security constraints
      constraints: this.constraints,

      // Rate limiting state
      rate_limiting: {
        messages_in_window: this.rateLimitState.messageTimestamps.length,
        connections_in_window: this.rateLimitState.connectionAttempts.length,
        window_size_ms: this.constraints.rateLimitWindow,
        last_reset: new Date(this.rateLimitState.lastReset).toISOString()
      },

      // Security violations
      security_violations: {
        total_violations: this.securityViolations.length,
        recent_violations: recentViolations.length,
        violation_types: this.getViolationTypeCounts(),
        severity_distribution: this.getSeverityDistribution()
      },

      // Security health
      security_health: {
        violation_rate: recentViolations.length / Math.max(1, this.getCurrentMessageRate()),
        connection_utilization: this.connectionCount / this.constraints.maxConnections,
        rate_limit_utilization: this.getCurrentMessageRate() / this.constraints.rateLimitMessages,
        overall_health: this.calculateSecurityHealth()
      },

      timestamp: new Date().toISOString()
    }
  }

  /**
   * Reset security state
   */
  resetSecurityState(): void {
    this.rateLimitState = {
      messageTimestamps: [],
      connectionAttempts: [],
      lastReset: Date.now(),
      currentRate: 0,
      isLimited: false
    }
    this.securityViolations = []
    this.connectionCount = 0
  }

  /**
   * Enable/disable security
   */
  setSecurityEnabled(enabled: boolean): void {
    this.isSecurityEnabled = enabled
  }

  // Private helper methods

  private calculateMessageSize(data: unknown): number {
    try {
      return JSON.stringify(data).length
    } catch (error) {
      // If JSON.stringify fails, estimate size
      return String(data).length
    }
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
    const MAX_DEPTH = 10

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
 * Factory function for creating security hardening instances
 */
export function createSecurityHardening(constraints?: Partial<SecurityConstraints>): SecurityHardening {
  return new SecurityHardening(constraints)
}

/**
 * Type guard for security hardening
 */
export function isSecurityHardening(security: unknown): security is SecurityHardening {
  return security instanceof SecurityHardening
}