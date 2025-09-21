/**
 * Hive Physics Engine - Frontend Implementation
 * 
 * Provides physics-based calculations for Organella morphology,
 * eliminating magic numbers through mathematical relationships.
 */

export interface HivePhysicsConfig {
  baseUnit: number
  scaleFactor: number
  aspectRatio: number
  energyLevel: number
  gravityConstant: number
  fluidDensity: number
}

export interface MorphologyConstraints {
  minSize: number
  maxSize: number
  aspectRatioRange: [number, number]
  energyEfficiency: number
}

export interface Point2D {
  x: number
  y: number
}

export interface Ellipse {
  center: Point2D
  radius: { x: number; y: number }
}

export interface BeeMorphology {
  viewBox: string
  center: Point2D
  abdomen: Ellipse
  thorax: Ellipse
  head: { center: Point2D; radius: number }
  wings: {
    left: Ellipse
    right: Ellipse
  }
  stinger: { points: string }
  specialFeatures: Record<string, any>
}

export class HivePhysicsEngine {
  private config: HivePhysicsConfig
  
  constructor(config: Partial<HivePhysicsConfig> = {}) {
    this.config = {
      baseUnit: 20,
      scaleFactor: 1,
      aspectRatio: 1.2,
      energyLevel: 0.8,
      gravityConstant: 9.81,
      fluidDensity: 1.225, // Air density
      ...config
    }
  }

  /**
   * Calculate optimal bee morphology based on role and physics
   */
  calculateMorphology(
    role: string, 
    constraints: Partial<MorphologyConstraints> = {}
  ): BeeMorphology {
    const { baseUnit, scaleFactor, aspectRatio } = this.config
    const unit = baseUnit * scaleFactor
    
    // Role-specific biomechanical modifiers
    const rolePhysics = this.getRolePhysics(role)
    
    // Apply constraints
    const finalConstraints: MorphologyConstraints = {
      minSize: unit * 0.5,
      maxSize: unit * 3,
      aspectRatioRange: [1.0, 2.0],
      energyEfficiency: 0.8,
      ...constraints
    }
    
    // Calculate canvas dimensions
    const viewBoxSize = this.clamp(unit * 10, finalConstraints.minSize * 10, finalConstraints.maxSize * 10)
    const viewBoxHeight = viewBoxSize * this.clamp(aspectRatio, ...finalConstraints.aspectRatioRange)
    
    const center: Point2D = { 
      x: viewBoxSize / 2, 
      y: viewBoxHeight / 2 
    }
    
    // Golden ratio proportions for natural aesthetics
    const goldenRatio = 1.618
    const bodySegmentRatio = 1 / goldenRatio
    
    return {
      viewBox: `0 0 ${viewBoxSize} ${viewBoxHeight}`,
      center,
      
      // Abdomen: Primary mass center
      abdomen: {
        center: { 
          x: center.x, 
          y: viewBoxHeight * (0.5 + bodySegmentRatio * 0.3) 
        },
        radius: { 
          x: unit * 1.2 * rolePhysics.abdomenScale, 
          y: unit * 1.7 * rolePhysics.abdomenScale 
        }
      },
      
      // Thorax: Power center
      thorax: {
        center: { 
          x: center.x, 
          y: viewBoxHeight * (0.5 - bodySegmentRatio * 0.2) 
        },
        radius: { 
          x: unit * 0.9 * rolePhysics.thoraxScale, 
          y: unit * 1.0 * rolePhysics.thoraxScale 
        }
      },
      
      // Head: Processing center
      head: {
        center: { 
          x: center.x, 
          y: viewBoxHeight * (0.5 - bodySegmentRatio * 0.6) 
        },
        radius: unit * 0.7 * rolePhysics.headScale
      },
      
      // Wings: Aerodynamic surfaces
      wings: this.calculateWingGeometry(center, unit, rolePhysics, viewBoxHeight),
      
      // Stinger: Defense mechanism
      stinger: this.calculateStingerGeometry(center, unit, rolePhysics, viewBoxHeight),
      
      // Role-specific features
      specialFeatures: this.calculateSpecialFeatures(center, unit, role, viewBoxSize, viewBoxHeight)
    }
  }

  /**
   * Calculate wing geometry based on aerodynamics
   */
  private calculateWingGeometry(
    center: Point2D, 
    unit: number, 
    rolePhysics: any, 
    viewBoxHeight: number
  ) {
    const wingSpan = unit * 1.0
    const wingChord = unit * 1.5 * rolePhysics.wingScale
    const wingThickness = unit * 0.7 * rolePhysics.wingScale
    
    // Wing positioning based on thorax location
    const wingY = viewBoxHeight * (0.5 - 1.618 * 0.2) // Golden ratio positioning
    
    return {
      left: {
        center: { x: center.x - wingSpan, y: wingY },
        radius: { x: wingChord, y: wingThickness }
      },
      right: {
        center: { x: center.x + wingSpan, y: wingY },
        radius: { x: wingChord, y: wingThickness }
      }
    }
  }

  /**
   * Calculate stinger geometry based on role requirements
   */
  private calculateStingerGeometry(
    center: Point2D, 
    unit: number, 
    rolePhysics: any, 
    viewBoxHeight: number
  ) {
    const stingerLength = unit * 0.4 * rolePhysics.stingerScale
    const stingerWidth = unit * 0.2 * rolePhysics.stingerScale
    const stingerY = viewBoxHeight * 0.8
    
    return {
      points: `${center.x},${stingerY} ${center.x - stingerWidth},${stingerY + stingerLength} ${center.x + stingerWidth},${stingerY + stingerLength}`
    }
  }

  /**
   * Calculate role-specific special features
   */
  private calculateSpecialFeatures(
    center: Point2D, 
    unit: number, 
    role: string, 
    viewBoxSize: number, 
    viewBoxHeight: number
  ): Record<string, any> {
    const features: Record<string, any> = {}
    
    switch (role) {
      case 'queen':
        features.crown = {
          points: `${center.x - unit * 0.4},${viewBoxHeight * 0.12} ${center.x},${viewBoxHeight * 0.05} ${center.x + unit * 0.4},${viewBoxHeight * 0.12}`
        }
        break
        
      case 'chronicler':
        features.scroll = {
          x: center.x - unit * 0.75,
          y: viewBoxHeight * 0.1,
          width: unit * 1.5,
          height: unit * 0.4,
          radius: unit * 0.1
        }
        features.divineAura = {
          radius: unit * 1.0,
          strokeWidth: unit * 0.1
        }
        features.quill = {
          start: { x: center.x + unit * 0.75, y: viewBoxHeight * 0.22 },
          end: { x: center.x + unit * 1.25, y: viewBoxHeight * 0.17 },
          strokeWidth: unit * 0.1
        }
        break
        
      case 'jules':
        features.antenna = {
          start: { x: center.x + unit * 0.5, y: viewBoxHeight * 0.22 },
          end: { x: center.x + unit * 1.0, y: viewBoxHeight * 0.15 },
          strokeWidth: unit * 0.08
        }
        break
    }
    
    return features
  }

  /**
   * Get role-specific physics parameters
   */
  private getRolePhysics(role: string) {
    const rolePhysicsMap = {
      worker: { 
        abdomenScale: 1.0, 
        thoraxScale: 0.9, 
        headScale: 0.7, 
        wingScale: 1.0, 
        stingerScale: 0.8,
        massDistribution: 'balanced'
      },
      scout: { 
        abdomenScale: 0.8, 
        thoraxScale: 0.8, 
        headScale: 0.8, 
        wingScale: 1.1, 
        stingerScale: 0.7,
        massDistribution: 'wing-heavy'
      },
      queen: { 
        abdomenScale: 1.4, 
        thoraxScale: 1.1, 
        headScale: 0.8, 
        wingScale: 1.2, 
        stingerScale: 1.2,
        massDistribution: 'abdomen-heavy'
      },
      guard: { 
        abdomenScale: 1.1, 
        thoraxScale: 1.2, 
        headScale: 0.6, 
        wingScale: 1.0, 
        stingerScale: 1.4,
        massDistribution: 'thorax-heavy'
      },
      chronicler: { 
        abdomenScale: 0.9, 
        thoraxScale: 0.9, 
        headScale: 0.8, 
        wingScale: 1.1, 
        stingerScale: 0.6,
        massDistribution: 'head-heavy'
      },
      jules: { 
        abdomenScale: 1.0, 
        thoraxScale: 0.9, 
        headScale: 0.8, 
        wingScale: 1.0, 
        stingerScale: 0.8,
        massDistribution: 'balanced'
      }
    }
    
    return rolePhysicsMap[role as keyof typeof rolePhysicsMap] || rolePhysicsMap.worker
  }

  /**
   * Calculate animation timing based on physics
   */
  calculateAnimationTiming(role: string, activityLevel: number): {
    wingFlapPeriod: number
    wingFlapAmplitude: number
    divineGlowPeriod: number
  } {
    const rolePhysics = this.getRolePhysics(role)
    const { energyLevel } = this.config
    
    // Wing flap frequency based on wing loading and energy
    const wingLoading = rolePhysics.wingScale / (rolePhysics.abdomenScale + rolePhysics.thoraxScale)
    const baseFlapPeriod = 0.15 // seconds
    const wingFlapPeriod = baseFlapPeriod / (wingLoading * activityLevel * energyLevel)
    
    // Wing flap amplitude based on role requirements
    const wingFlapAmplitude = 25 * activityLevel // degrees
    
    // Divine glow period for sacred bees
    const divineGlowPeriod = 3.0 / (activityLevel * 0.5 + 0.5)
    
    return {
      wingFlapPeriod,
      wingFlapAmplitude,
      divineGlowPeriod
    }
  }

  /**
   * Utility: Clamp value between min and max
   */
  private clamp(value: number, min: number, max: number): number {
    return Math.min(Math.max(value, min), max)
  }

  /**
   * Update physics configuration
   */
  updateConfig(newConfig: Partial<HivePhysicsConfig>): void {
    this.config = { ...this.config, ...newConfig }
  }

  /**
   * Get current physics status
   */
  getStatus(): { status: string; config: HivePhysicsConfig } {
    return {
      status: 'active',
      config: { ...this.config }
    }
  }
}

// Export singleton instance
export const hivePhysics = new HivePhysicsEngine()

// Export utility functions
export const calculateOptimalSize = (role: string, constraints: any) => {
  return hivePhysics.calculateMorphology(role, constraints)
}

export const getAnimationTiming = (role: string, activity: number) => {
  return hivePhysics.calculateAnimationTiming(role, activity)
}