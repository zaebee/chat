/**
 * RectValidator - Rectangular Paradigm Validation System
 * 
 * Implements strict validation and compliance checking following
 * the rectangular (structured) paradigm from the prototype wisdom.
 * Embodies AlgoGenesis 1:3 (Boolean Separation) principles.
 */

import type { TransformationComponent } from './index'

export interface RectConstraint {
  readonly name: string
  readonly validationRule: string
  readonly complianceLevel: 'required' | 'medical_strict' | 'optional'
  readonly required: boolean
}

export interface ValidationResult {
  readonly valid: boolean
  readonly errors: string[]
  readonly warnings: string[]
  readonly constraintsChecked: number
}

export interface ComplianceReport {
  readonly level: string
  readonly passed: boolean
  readonly violations: string[]
  readonly score: number
}

/**
 * RectValidator implements strict validation following rectangular paradigm
 */
export class RectValidator implements TransformationComponent {
  readonly type = 'transformation' as const
  readonly purpose = 'Rectangular paradigm validation and compliance'
  readonly id: string

  private constraints = new Map<string, RectConstraint>()
  private validationRules = new Map<string, (value: any) => boolean>()

  constructor(id: string) {
    this.id = id
    this.initializeValidationRules()
  }

  /**
   * Add rectangular constraint for validation
   */
  addConstraint(constraint: RectConstraint): void {
    this.constraints.set(constraint.name, constraint)
  }

  /**
   * Transform data through rectangular validation
   */
  transform(input: any): any {
    const validationResult = this.validateInput(input)
    
    if (!validationResult.valid) {
      throw new Error(`Rect validation failed: ${validationResult.errors.join(', ')}`)
    }

    return {
      ...input,
      rect_validation: {
        validated: true,
        timestamp: new Date().toISOString(),
        constraints_applied: validationResult.constraintsChecked,
        compliance_level: this.getHighestComplianceLevel()
      }
    }
  }

  /**
   * Process data with compliance monitoring
   */
  process(data: any): any {
    const validated = this.transform(data)
    const compliance = this.checkCompliance(validated)
    
    return {
      ...validated,
      rect_compliance: compliance
    }
  }

  /**
   * Validate input against all rectangular constraints
   */
  private validateInput(data: any): ValidationResult {
    const errors: string[] = []
    const warnings: string[] = []
    let constraintsChecked = 0

    for (const [name, constraint] of this.constraints) {
      constraintsChecked++

      if (constraint.required && !(name in data)) {
        errors.push(`Required constraint '${name}' missing`)
        continue
      }

      if (name in data) {
        const isValid = this.applyValidationRule(data[name], constraint.validationRule)
        
        if (!isValid) {
          if (constraint.complianceLevel === 'required') {
            errors.push(`Constraint '${name}' validation failed`)
          } else {
            warnings.push(`Constraint '${name}' validation warning`)
          }
        }
      }
    }

    return {
      valid: errors.length === 0,
      errors,
      warnings,
      constraintsChecked
    }
  }

  /**
   * Check compliance against rectangular standards
   */
  private checkCompliance(data: any): ComplianceReport {
    const violations: string[] = []
    let score = 1.0

    // Check for required fields
    const requiredConstraints = Array.from(this.constraints.values())
      .filter(c => c.complianceLevel === 'required')

    for (const constraint of requiredConstraints) {
      if (!(constraint.name in data)) {
        violations.push(`Missing required field: ${constraint.name}`)
        score -= 0.2
      }
    }

    // Check medical strict compliance
    const medicalConstraints = Array.from(this.constraints.values())
      .filter(c => c.complianceLevel === 'medical_strict')

    for (const constraint of medicalConstraints) {
      if (constraint.name in data) {
        const isValid = this.applyValidationRule(data[constraint.name], constraint.validationRule)
        if (!isValid) {
          violations.push(`Medical strict violation: ${constraint.name}`)
          score -= 0.3
        }
      }
    }

    return {
      level: this.getHighestComplianceLevel(),
      passed: violations.length === 0,
      violations,
      score: Math.max(0, score)
    }
  }

  /**
   * Apply validation rule to value
   */
  private applyValidationRule(value: any, rule: string): boolean {
    const validator = this.validationRules.get(rule)
    return validator ? validator(value) : true
  }

  /**
   * Initialize built-in validation rules
   */
  private initializeValidationRules(): void {
    this.validationRules.set('non_empty_string', (value: any) => 
      typeof value === 'string' && value.trim().length > 0
    )

    this.validationRules.set('valid_json', (value: any) => {
      try {
        if (typeof value === 'string') {
          JSON.parse(value)
        } else {
          JSON.stringify(value)
        }
        return true
      } catch {
        return false
      }
    })

    this.validationRules.set('markdown_format', (value: any) =>
      typeof value === 'string' && (value.includes('#') || value.includes('##'))
    )

    this.validationRules.set('email_format', (value: any) =>
      typeof value === 'string' && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)
    )

    this.validationRules.set('url_format', (value: any) =>
      typeof value === 'string' && /^https?:\/\/.+/.test(value)
    )
  }

  /**
   * Get highest compliance level from constraints
   */
  private getHighestComplianceLevel(): string {
    const levels = Array.from(this.constraints.values()).map(c => c.complianceLevel)
    
    if (levels.includes('medical_strict')) return 'medical_strict'
    if (levels.includes('required')) return 'required'
    return 'optional'
  }

  /**
   * Component lifecycle methods
   */
  async initialize(): Promise<void> {
    console.log(`🔧 RectValidator ${this.id} initialized with ${this.constraints.size} constraints`)
  }

  async destroy(): Promise<void> {
    this.constraints.clear()
    this.validationRules.clear()
    console.log(`🧹 RectValidator ${this.id} destroyed`)
  }

  getStatus(): Record<string, any> {
    return {
      type: this.type,
      purpose: this.purpose,
      id: this.id,
      constraints: this.constraints.size,
      validationRules: this.validationRules.size,
      complianceLevel: this.getHighestComplianceLevel()
    }
  }
}