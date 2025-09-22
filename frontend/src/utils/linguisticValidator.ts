/**
 * Linguistic Validator for Pollen Protocol Events (TypeScript)
 *
 * This module provides comprehensive linguistic analysis for validating
 * past-tense event types in the Pollen Protocol, maintaining consistency
 * with the Python backend validation.
 *
 * Following the Hive Constitution requirement that all events use
 * clear past-tense verbs to describe completed actions.
 */

export interface ValidationResult {
  isValid: boolean
  confidence: number // 0.0 to 1.0
  detectedTense: string
  suggestions: string[]
  reason: string
}

export class LinguisticValidator {
  private irregularPastTense: Record<string, string> = {}
  private pastTenseForms: Set<string> = new Set()
  private pastParticiples: Set<string> = new Set()
  private commonEventTypes: Set<string> = new Set()
  private pastTensePatterns: Array<{ pattern: RegExp; type: string }> = []

  constructor() {
    this.loadIrregularVerbs()
    this.loadPastTensePatterns()
    this.loadCommonEventTypes()
  }

  private loadIrregularVerbs(): void {
    this.irregularPastTense = {
      begin: 'began',
      break: 'broke',
      bring: 'brought',
      build: 'built',
      catch: 'caught',
      choose: 'chose',
      come: 'came',
      cut: 'cut',
      do: 'did',
      draw: 'drew',
      drink: 'drank',
      drive: 'drove',
      eat: 'ate',
      fall: 'fell',
      feel: 'felt',
      find: 'found',
      fly: 'flew',
      forget: 'forgot',
      get: 'got',
      give: 'gave',
      go: 'went',
      grow: 'grew',
      have: 'had',
      hear: 'heard',
      keep: 'kept',
      know: 'knew',
      leave: 'left',
      lose: 'lost',
      make: 'made',
      mean: 'meant',
      meet: 'met',
      put: 'put',
      read: 'read',
      run: 'ran',
      say: 'said',
      see: 'saw',
      sell: 'sold',
      send: 'sent',
      set: 'set',
      show: 'showed',
      shut: 'shut',
      sing: 'sang',
      sit: 'sat',
      sleep: 'slept',
      speak: 'spoke',
      spend: 'spent',
      stand: 'stood',
      take: 'took',
      teach: 'taught',
      tell: 'told',
      think: 'thought',
      understand: 'understood',
      wake: 'woke',
      wear: 'wore',
      win: 'won',
      write: 'wrote'
    }

    this.pastTenseForms = new Set(Object.values(this.irregularPastTense))

    this.pastParticiples = new Set([
      'broken', 'built', 'caught', 'chosen', 'cut', 'done', 'drawn',
      'eaten', 'fallen', 'felt', 'found', 'forgotten', 'given', 'gone',
      'grown', 'heard', 'kept', 'known', 'left', 'lost', 'made', 'meant',
      'put', 'read', 'run', 'said', 'seen', 'sent', 'shown', 'shut',
      'sung', 'slept', 'spoken', 'spent', 'stood', 'taken', 'taught',
      'told', 'thought', 'understood', 'woken', 'worn', 'won', 'written'
    ])
  }

  private loadPastTensePatterns(): void {
    this.pastTensePatterns = [
      // Regular past tense endings
      { pattern: /\w+ed$/, type: 'regular_past' },
      { pattern: /\w+ied$/, type: 'regular_past_y_to_i' },
      { pattern: /\w+ued$/, type: 'regular_past_ue' },
      { pattern: /\w+pped$/, type: 'regular_past_double' },
      { pattern: /\w+tted$/, type: 'regular_past_double' },
      { pattern: /\w+nned$/, type: 'regular_past_double' },

      // Past participle forms
      { pattern: /\w+en$/, type: 'past_participle' },
      { pattern: /\w+n$/, type: 'past_participle_short' },

      // Special cases
      { pattern: /\w+ought$/, type: 'irregular_ought' },
      { pattern: /\w+aught$/, type: 'irregular_aught' }
    ]
  }

  private loadCommonEventTypes(): void {
    this.commonEventTypes = new Set([
      // User actions
      'user_registered', 'user_logged_in', 'user_logged_out', 'user_updated',
      'user_deleted', 'user_activated', 'user_deactivated',

      // Data events
      'data_created', 'data_updated', 'data_deleted', 'data_synchronized',
      'data_exported', 'data_imported', 'data_backed_up', 'data_restored',

      // System events
      'system_started', 'system_stopped', 'system_restarted', 'system_configured',
      'error_occurred', 'warning_issued', 'alert_triggered', 'notification_sent',

      // Process events
      'task_completed', 'task_failed', 'task_started', 'task_cancelled',
      'job_queued', 'job_executed', 'job_finished', 'job_retried',

      // Communication events
      'message_sent', 'message_received', 'message_delivered', 'message_read',
      'email_sent', 'notification_pushed', 'alert_broadcasted',

      // File operations
      'file_uploaded', 'file_downloaded', 'file_deleted', 'file_moved',
      'file_copied', 'file_renamed', 'file_compressed', 'file_extracted',

      // API events
      'request_received', 'response_sent', 'api_called', 'webhook_triggered',
      'endpoint_accessed', 'rate_limit_exceeded', 'authentication_failed',

      // Business events
      'order_placed', 'order_shipped', 'order_delivered', 'order_cancelled',
      'payment_processed', 'payment_failed', 'payment_refunded',
      'invoice_generated', 'invoice_paid', 'subscription_created',

      // AI/Hive specific events
      'agent_spawned', 'agent_terminated', 'model_trained', 'prediction_made',
      'analysis_completed', 'report_generated', 'decision_reached',
      'collaboration_initiated', 'teammate_joined', 'teammate_left'
    ])
  }

  public validatePastTense(eventType: string): ValidationResult {
    if (!eventType || typeof eventType !== 'string') {
      return {
        isValid: false,
        confidence: 1.0,
        detectedTense: 'invalid',
        suggestions: [],
        reason: 'Event type must be a non-empty string'
      }
    }

    const normalized = eventType.toLowerCase().trim()

    // Check if it's a known valid event type
    if (this.commonEventTypes.has(normalized)) {
      return {
        isValid: true,
        confidence: 1.0,
        detectedTense: 'past',
        suggestions: [],
        reason: 'Recognized valid past-tense event type'
      }
    }

    // Extract the main verb from compound event types
    const mainVerb = this.extractMainVerb(normalized)

    // Check irregular past tense forms
    if (this.pastTenseForms.has(mainVerb)) {
      return {
        isValid: true,
        confidence: 0.95,
        detectedTense: 'past_irregular',
        suggestions: [],
        reason: `Irregular past tense form: ${mainVerb}`
      }
    }

    // Check past participles
    if (this.pastParticiples.has(mainVerb)) {
      return {
        isValid: true,
        confidence: 0.90,
        detectedTense: 'past_participle',
        suggestions: [],
        reason: `Past participle form: ${mainVerb}`
      }
    }

    // Check against regex patterns
    for (const { pattern, type } of this.pastTensePatterns) {
      if (pattern.test(normalized)) {
        const confidence = this.calculatePatternConfidence(type, normalized)
        return {
          isValid: true,
          confidence,
          detectedTense: type,
          suggestions: [],
          reason: `Matches ${type} pattern`
        }
      }
    }

    // If no past-tense pattern found, generate suggestions
    const suggestions = this.generateSuggestions(normalized)

    return {
      isValid: false,
      confidence: 0.0,
      detectedTense: 'present_or_other',
      suggestions,
      reason: 'Does not match any recognized past-tense pattern'
    }
  }

  private extractMainVerb(eventType: string): string {
    const parts = eventType.split('_')
    if (parts.length >= 2) {
      return parts[parts.length - 1]
    }
    return eventType
  }

  private calculatePatternConfidence(patternType: string, word: string): number {
    const baseConfidence: Record<string, number> = {
      regular_past: 0.90,
      regular_past_y_to_i: 0.95,
      regular_past_ue: 0.95,
      regular_past_double: 0.90,
      past_participle: 0.85,
      past_participle_short: 0.80,
      irregular_ought: 0.95,
      irregular_aught: 0.95
    }

    let confidence = baseConfidence[patternType] || 0.70

    // Adjust confidence based on word characteristics
    if (word.length < 3) {
      confidence *= 0.7
    } else if (word.length > 15) {
      confidence *= 0.8
    }

    return Math.min(confidence, 1.0)
  }

  private generateSuggestions(eventType: string): string[] {
    const suggestions: string[] = []

    // Simple transformations
    if (eventType.endsWith('e')) {
      suggestions.push(eventType + 'd')
    } else if (eventType.endsWith('y') && eventType.length > 2) {
      suggestions.push(eventType.slice(0, -1) + 'ied')
    } else if (/[ptn]$/.test(eventType) && eventType.length > 2) {
      suggestions.push(eventType + eventType.slice(-1) + 'ed')
    } else {
      suggestions.push(eventType + 'ed')
    }

    // Check for irregular verb base forms
    if (this.irregularPastTense[eventType]) {
      suggestions.push(this.irregularPastTense[eventType])
    }

    // Add compound suggestions
    const prefixes = ['user_', 'data_', 'system_', 'task_', 'message_', 'file_']
    for (const prefix of prefixes) {
      if (!eventType.startsWith(prefix)) {
        suggestions.push(prefix + eventType + 'ed')
      }
    }

    return suggestions.slice(0, 5)
  }

  public validateEventNameStyle(eventType: string): ValidationResult {
    if (!eventType) {
      return {
        isValid: false,
        confidence: 1.0,
        detectedTense: 'invalid',
        suggestions: [],
        reason: 'Event type cannot be empty'
      }
    }

    const issues: string[] = []
    const suggestions: string[] = []

    // Check snake_case convention
    if (!/^[a-z][a-z0-9_]*[a-z0-9]$/.test(eventType)) {
      issues.push('Should use snake_case (lowercase with underscores)')
      suggestions.push(eventType.replace(/[A-Z]/g, (match) => '_' + match.toLowerCase()).replace(/^_/, ''))
    }

    // Check length
    if (eventType.length < 3) {
      issues.push('Event type too short (minimum 3 characters)')
    } else if (eventType.length > 50) {
      issues.push('Event type too long (maximum 50 characters)')
    }

    // Check for descriptive content
    if (eventType.replace(/_/g, '').length < 5) {
      issues.push('Event type should be more descriptive')
    }

    // Check for reserved words
    const reservedPatterns = ['test', 'temp', 'debug', 'tmp']
    if (reservedPatterns.some(pattern => eventType.toLowerCase().includes(pattern))) {
      issues.push('Avoid using temporary/debug terms in production events')
    }

    const isValid = issues.length === 0
    const confidence = isValid ? 1.0 : Math.max(0.3, 1.0 - issues.length * 0.2)

    return {
      isValid,
      confidence,
      detectedTense: 'style_check',
      suggestions,
      reason: issues.length > 0 ? issues.join('; ') : 'Event naming style is compliant'
    }
  }
}

// Create a singleton instance for convenience
export const linguisticValidator = new LinguisticValidator()

// Utility function for quick validation
export function validatePollenEventType(eventType: string): ValidationResult {
  return linguisticValidator.validatePastTense(eventType)
}

export default LinguisticValidator