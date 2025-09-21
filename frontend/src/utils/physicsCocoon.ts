/**
 * Physics Cocoon System - Sacred Validation for Bee Morphology
 * 
 * Ensures all bee manifestations follow divine mathematical principles
 * and golden ratio proportions before rendering to the sacred realm.
 */

import { hivePhysics, type BeeMorphology, type MorphologyConstraints } from './hivePhysics'
import { pollenBus, BeeEventTypes } from './pollenProtocol'
import { validateGoldenRatioCompliance } from './validationRules/goldenRatio.rule.ts'
import { validateDivineTranscendence } from './validationRules/divineTranscendence.rule.ts'
import { validateAnatomicalHarmony } from './validationRules/anatomicalHarmony.rule.ts'
import { validatePhysicsConstraints } from './validationRules/physicsConstraints.rule.ts'
import { validateVisualQuality } from './validationRules/visualQuality.rule.ts'

// Sacred constants for validation
const GOLDEN_RATIO = 1.618033988749
const VALIDATION_TIMEOUT = 5000 // 5 seconds max cocoon time
const DIVINE_TOLERANCE = 0.001  // Acceptable deviation from divine ratios

export interface PhysicsConstraint {
  name: string
  description: string
  validator: (morphology: BeeMorphology) => ValidationResult
  severity: 'warning' | 'error' | 'critical'
  divineRequirement: boolean
}

export interface ValidationResult {
  passed: boolean
  score: number // 0-1, higher is better
  message: string
  details?: any
}

export interface PhysicsCocoon {
  stage: 'calculation' | 'validation' | 'manifestation'
  beeId: string
  role: string
  
  // Calculation stage
  inputConstraints: MorphologyConstraints
  rawCalculations: BeeMorphology | null
  
  // Validation stage
  validationRules: PhysicsConstraint[]
  validationResults: ValidationResult[]
  emergenceThreshold: number
  
  // Manifestation stage
  validatedMorphology: BeeMorphology | null
  renderingInstructions: SVGInstructions | null
  
  // Cocoon metadata
  entryTimestamp: number
  stageTransitions: StageTransition[]
  divineBlessing: boolean
  
  // Progress tracking
  calculationProgress: number // 0-1
  validationProgress: number  // 0-1
  manifestationProgress: number // 0-1
}

export interface SVGInstructions {
  viewBox: string
  elements: SVGElement[]
  animations: AnimationInstruction[]
  divineEffects: DivineEffect[]
}

export interface SVGElement {
  type: 'ellipse' | 'circle' | 'polygon' | 'line' | 'rect'
  attributes: Record<string, any>
  classes: string[]
  divineEnhancement?: boolean
}

export interface AnimationInstruction {
  target: string
  property: string
  keyframes: any[]
  duration: number
  easing: string
}

export interface DivineEffect {
  type: 'aura' | 'glow' | 'emanation' | 'transcendence'
  intensity: number
  color: string
  pattern: string
}

export interface StageTransition {
  fromStage: PhysicsCocoon['stage']
  toStage: PhysicsCocoon['stage']
  timestamp: number
  duration: number
  success: boolean
  reason?: string
}

// Sacred validation rules
const DIVINE_CONSTRAINTS: PhysicsConstraint[] = [
  {
    name: 'golden_ratio_compliance',
    description: 'All proportions must follow golden ratio mathematics',
    validator: (morphology: BeeMorphology) => validateGoldenRatioCompliance(morphology, GOLDEN_RATIO, DIVINE_TOLERANCE),
    severity: 'critical',
    divineRequirement: true
  },
  {
    name: 'sacred_bee_transcendence',
    description: 'Divine bees must exceed normal physical limitations',
    validator: (morphology: BeeMorphology) => validateDivineTranscendence(morphology),
    severity: 'error',
    divineRequirement: true
  },
  {
    name: 'morphology_coherence',
    description: 'All body parts must maintain anatomical harmony',
    validator: (morphology: BeeMorphology) => validateAnatomicalHarmony(morphology, GOLDEN_RATIO),
    severity: 'warning',
    divineRequirement: false
  },
  {
    name: 'physics_constraints',
    description: 'Morphology must respect physical laws and constraints',
    validator: (morphology: BeeMorphology) => validatePhysicsConstraints(morphology),
    severity: 'error',
    divineRequirement: false
  },
  {
    name: 'visual_quality',
    description: 'Rendered output must meet aesthetic standards',
    validator: (morphology: BeeMorphology) => validateVisualQuality(morphology, GOLDEN_RATIO),
    severity: 'warning',
    divineRequirement: false
  }
]

export class PhysicsCocoonEngine {
  private cocoons: Map<string, PhysicsCocoon> = new Map()
  private validationRules: PhysicsConstraint[] = [...DIVINE_CONSTRAINTS]
  
  /**
   * Enter a bee into the physics cocoon for validation
   */
  async enterCocoon(
    beeId: string, 
    role: string, 
    constraints: MorphologyConstraints
  ): Promise<PhysicsCocoon> {
    // Create cocoon with calculation stage
    const cocoon: PhysicsCocoon = {
      stage: 'calculation',
      beeId,
      role,
      inputConstraints: constraints,
      rawCalculations: null,
      validationRules: this.getValidationRulesForRole(role),
      validationResults: [],
      emergenceThreshold: this.calculateEmergenceThreshold(role),
      validatedMorphology: null,
      renderingInstructions: null,
      entryTimestamp: Date.now(),
      stageTransitions: [],
      divineBlessing: false,
      calculationProgress: 0,
      validationProgress: 0,
      manifestationProgress: 0
    }
    
    this.cocoons.set(beeId, cocoon)
    
    // Emit cocoon entry event
    pollenBus.emit(BeeEventTypes.COCOON_ENTERED, {
      beeId,
      role,
      stage: 'calculation',
      timestamp: Date.now()
    }, {
      source: 'physics-cocoon-engine'
    })
    
    // Begin calculation stage
    return this.progressCocoon(beeId)
  }
  
  /**
   * Progress cocoon through stages
   */
  private async progressCocoon(beeId: string): Promise<PhysicsCocoon> {
    const cocoon = this.cocoons.get(beeId)
    if (!cocoon) throw new Error(`Cocoon not found for bee ${beeId}`)
    
    switch (cocoon.stage) {
      case 'calculation':
        return this.calculateMorphology(cocoon)
      case 'validation':
        return this.validateMorphology(cocoon)
      case 'manifestation':
        return this.manifestBee(cocoon)
    }
  }
  
  /**
   * Calculate morphology stage
   */
  private async calculateMorphology(cocoon: PhysicsCocoon): Promise<PhysicsCocoon> {
    cocoon.calculationProgress = 0.1
    
    try {
      // Use hive physics engine to calculate morphology
      cocoon.rawCalculations = hivePhysics.calculateMorphology(
        cocoon.role, 
        cocoon.inputConstraints
      )
      
      cocoon.calculationProgress = 1.0
      
      // Transition to validation stage
      this.transitionStage(cocoon, 'validation')
      
      return this.progressCocoon(cocoon.beeId)
      
    } catch (error) {
      // Calculation failed
      pollenBus.emit(BeeEventTypes.COCOON_FAILED, {
        beeId: cocoon.beeId,
        stage: 'calculation',
        error: error instanceof Error ? error.message : 'Unknown error',
        timestamp: Date.now()
      }, {
        source: 'physics-cocoon-engine'
      })
      
      throw error
    }
  }
  
  /**
   * Validate morphology stage
   */
  private async validateMorphology(cocoon: PhysicsCocoon): Promise<PhysicsCocoon> {
    if (!cocoon.rawCalculations) {
      throw new Error('No morphology to validate')
    }
    
    cocoon.validationProgress = 0.1
    cocoon.validationResults = []
    
    // Run all validation rules
    for (let i = 0; i < cocoon.validationRules.length; i++) {
      const rule = cocoon.validationRules[i]
      const result = rule.validator(cocoon.rawCalculations)
      
      cocoon.validationResults.push(result)
      cocoon.validationProgress = (i + 1) / cocoon.validationRules.length
      
      // Emit validation progress
      pollenBus.emit(BeeEventTypes.VALIDATION_PROGRESS, {
        beeId: cocoon.beeId,
        rule: rule.name,
        result,
        progress: cocoon.validationProgress,
        timestamp: Date.now()
      }, {
        source: 'physics-cocoon-engine'
      })
    }
    
    // Calculate overall validation score
    const totalScore = cocoon.validationResults.reduce((sum, result) => sum + result.score, 0)
    const averageScore = totalScore / cocoon.validationResults.length
    const criticalFailures = cocoon.validationResults.filter(
      (result, index) => !result.passed && cocoon.validationRules[index].severity === 'critical'
    )
    
    // Check if validation passed
    const validationPassed = averageScore >= cocoon.emergenceThreshold && criticalFailures.length === 0
    
    if (validationPassed) {
      // Validation successful - proceed to manifestation
      cocoon.validatedMorphology = cocoon.rawCalculations
      cocoon.divineBlessing = averageScore >= 0.9 // Divine blessing for high scores
      
      this.transitionStage(cocoon, 'manifestation')
      return this.progressCocoon(cocoon.beeId)
      
    } else {
      // Validation failed
      pollenBus.emit(BeeEventTypes.VALIDATION_FAILED, {
        beeId: cocoon.beeId,
        averageScore,
        threshold: cocoon.emergenceThreshold,
        criticalFailures: criticalFailures.length,
        results: cocoon.validationResults,
        timestamp: Date.now()
      }, {
        source: 'physics-cocoon-engine'
      })
      
      throw new Error(`Validation failed: score ${averageScore.toFixed(3)} < threshold ${cocoon.emergenceThreshold}`)
    }
  }
  
  /**
   * Manifest bee stage
   */
  private async manifestBee(cocoon: PhysicsCocoon): Promise<PhysicsCocoon> {
    if (!cocoon.validatedMorphology) {
      throw new Error('No validated morphology to manifest')
    }
    
    cocoon.manifestationProgress = 0.1
    
    // Generate SVG rendering instructions
    cocoon.renderingInstructions = this.generateSVGInstructions(
      cocoon.validatedMorphology,
      cocoon.divineBlessing
    )
    
    cocoon.manifestationProgress = 1.0
    
    // Emit successful emergence
    pollenBus.emit(BeeEventTypes.BEE_EMERGED, {
      beeId: cocoon.beeId,
      role: cocoon.role,
      morphology: cocoon.validatedMorphology,
      renderingInstructions: cocoon.renderingInstructions,
      divineBlessing: cocoon.divineBlessing,
      validationScore: cocoon.validationResults.reduce((sum, r) => sum + r.score, 0) / cocoon.validationResults.length,
      timestamp: Date.now()
    }, {
      source: 'physics-cocoon-engine'
    })
    
    return cocoon
  }
  
  /**
   * Generate SVG rendering instructions
   */
  private generateSVGInstructions(
    morphology: BeeMorphology, 
    divineBlessing: boolean
  ): SVGInstructions {
    const elements: SVGElement[] = []
    const animations: AnimationInstruction[] = []
    const divineEffects: DivineEffect[] = []
    
    // Generate basic bee elements
    elements.push(
      {
        type: 'ellipse',
        attributes: {
          cx: morphology.abdomen.center.x,
          cy: morphology.abdomen.center.y,
          rx: morphology.abdomen.radius.x,
          ry: morphology.abdomen.radius.y
        },
        classes: ['bee-part', 'abdomen']
      },
      {
        type: 'ellipse',
        attributes: {
          cx: morphology.thorax.center.x,
          cy: morphology.thorax.center.y,
          rx: morphology.thorax.radius.x,
          ry: morphology.thorax.radius.y
        },
        classes: ['bee-part', 'thorax']
      },
      {
        type: 'circle',
        attributes: {
          cx: morphology.head.center.x,
          cy: morphology.head.center.y,
          r: morphology.head.radius
        },
        classes: ['bee-part', 'head']
      }
    )
    
    // Add wings
    elements.push(
      {
        type: 'ellipse',
        attributes: {
          cx: morphology.wings.left.center.x,
          cy: morphology.wings.left.center.y,
          rx: morphology.wings.left.radius.x,
          ry: morphology.wings.left.radius.y
        },
        classes: ['bee-part', 'wing', 'wing-left']
      },
      {
        type: 'ellipse',
        attributes: {
          cx: morphology.wings.right.center.x,
          cy: morphology.wings.right.center.y,
          rx: morphology.wings.right.radius.x,
          ry: morphology.wings.right.radius.y
        },
        classes: ['bee-part', 'wing', 'wing-right']
      }
    )
    
    // Add divine effects if blessed
    if (divineBlessing) {
      divineEffects.push({
        type: 'aura',
        intensity: 0.8,
        color: '#f7dc6f',
        pattern: 'radial-gradient'
      })
      
      // Add divine glow animation
      animations.push({
        target: '.divine-aura',
        property: 'opacity',
        keyframes: [0.3, 0.8, 0.3],
        duration: 3000,
        easing: 'ease-in-out'
      })
    }
    
    return {
      viewBox: morphology.viewBox,
      elements,
      animations,
      divineEffects
    }
  }
  
  /**
   * Transition between cocoon stages
   */
  private transitionStage(
    cocoon: PhysicsCocoon, 
    newStage: PhysicsCocoon['stage']
  ): void {
    const transition: StageTransition = {
      fromStage: cocoon.stage,
      toStage: newStage,
      timestamp: Date.now(),
      duration: Date.now() - cocoon.entryTimestamp,
      success: true
    }
    
    cocoon.stageTransitions.push(transition)
    cocoon.stage = newStage
    
    pollenBus.emit(BeeEventTypes.STAGE_TRANSITION, {
      beeId: cocoon.beeId,
      transition,
      timestamp: Date.now()
    }, {
      source: 'physics-cocoon-engine'
    })
  }
  
  /**
   * Get validation rules for specific role
   */
  private getValidationRulesForRole(role: string): PhysicsConstraint[] {
    // Divine bees get all rules including divine requirements
    if (role === 'chronicler' || role === 'jules') {
      return [...this.validationRules]
    }
    
    // Regular bees skip divine-specific validations
    return this.validationRules.filter(rule => !rule.divineRequirement)
  }
  
  /**
   * Calculate emergence threshold based on role
   */
  private calculateEmergenceThreshold(role: string): number {
    const baseThreshold = 0.7
    
    // Divine bees require higher standards
    if (role === 'chronicler' || role === 'jules') {
      return 0.85
    }
    
    // Queen requires high quality
    if (role === 'queen') {
      return 0.8
    }
    
    return baseThreshold
  }
  
  /**
   * Get cocoon status
   */
  getCocoonStatus(beeId: string): PhysicsCocoon | null {
    return this.cocoons.get(beeId) || null
  }
  
  /**
   * Get all active cocoons
   */
  getActiveCocoons(): PhysicsCocoon[] {
    return Array.from(this.cocoons.values())
  }
  
  /**
   * Remove completed cocoon
   */
  releaseCocoon(beeId: string): void {
    this.cocoons.delete(beeId)
  }
  
  /**
   * Get engine status
   */
  getStatus(): {
    activeCocoons: number
    totalProcessed: number
    averageProcessingTime: number
    successRate: number
  } {
    const active = this.cocoons.size
    // TODO: Implement metrics tracking
    return {
      activeCocoons: active,
      totalProcessed: 0,
      averageProcessingTime: 0,
      successRate: 1.0
    }
  }
}

// Export singleton instance
export const physicsCocoonEngine = new PhysicsCocoonEngine()
