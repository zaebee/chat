/**
 * Influence Visualizer
 * 
 * Creates visual effects for emotional contagion including ripples, gradients,
 * connection lines, and particle effects to show emotional influence flow.
 */

export interface VisualEffect {
  id: string
  type: 'ripple' | 'connection' | 'aura' | 'particle'
  sourceX: number
  sourceY: number
  targetX?: number
  targetY?: number
  emotion: string
  intensity: number
  startTime: number
  duration: number
  color: string
}

export interface VisualizationConfig {
  enabled: boolean
  showRipples: boolean
  showConnections: boolean
  showAuras: boolean
  showParticles: boolean
  effectIntensity: number // 0-1
  animationSpeed: number // 0-1
}

export class InfluenceVisualizer {
  private activeEffects: Map<string, VisualEffect> = new Map()
  private animationFrame: number | null = null
  private canvas: HTMLCanvasElement | null = null
  private ctx: CanvasRenderingContext2D | null = null

  private config: VisualizationConfig = {
    enabled: true,
    showRipples: true,
    showConnections: true,
    showAuras: true,
    showParticles: false, // Disabled by default for performance
    effectIntensity: 0.7,
    animationSpeed: 1.0
  }

  private emotionColors = {
    calm: '#87CEEB',      // Sky blue
    excited: '#FF6347',   // Tomato red
    focused: '#228B22',   // Forest green
    protective: '#DC143C', // Crimson
    divine: '#FFD700'     // Gold
  }

  /**
   * Initialize visualizer with canvas element
   */
  initialize(canvas: HTMLCanvasElement): void {
    this.canvas = canvas
    this.ctx = canvas.getContext('2d')
    
    if (this.ctx) {
      this.startAnimation()
    }
  }

  /**
   * Create ripple effect from emotional influence
   */
  createRipple(
    x: number, 
    y: number, 
    emotion: string, 
    intensity: number = 1.0
  ): string {
    if (!this.config.enabled || !this.config.showRipples) return ''

    const effectId = `ripple_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    
    const effect: VisualEffect = {
      id: effectId,
      type: 'ripple',
      sourceX: x,
      sourceY: y,
      emotion,
      intensity: intensity * this.config.effectIntensity,
      startTime: Date.now(),
      duration: 2000 / this.config.animationSpeed, // 2 seconds base duration
      color: this.emotionColors[emotion as keyof typeof this.emotionColors] || '#87CEEB'
    }

    this.activeEffects.set(effectId, effect)
    return effectId
  }

  /**
   * Create connection line between two bees showing influence
   */
  createConnection(
    sourceX: number,
    sourceY: number,
    targetX: number,
    targetY: number,
    emotion: string,
    intensity: number = 1.0
  ): string {
    if (!this.config.enabled || !this.config.showConnections) return ''

    const effectId = `connection_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    
    const effect: VisualEffect = {
      id: effectId,
      type: 'connection',
      sourceX,
      sourceY,
      targetX,
      targetY,
      emotion,
      intensity: intensity * this.config.effectIntensity,
      startTime: Date.now(),
      duration: 1500 / this.config.animationSpeed,
      color: this.emotionColors[emotion as keyof typeof this.emotionColors] || '#87CEEB'
    }

    this.activeEffects.set(effectId, effect)
    return effectId
  }

  /**
   * Create aura effect around a bee
   */
  createAura(
    x: number,
    y: number,
    emotion: string,
    intensity: number = 1.0
  ): string {
    if (!this.config.enabled || !this.config.showAuras) return ''

    const effectId = `aura_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    
    const effect: VisualEffect = {
      id: effectId,
      type: 'aura',
      sourceX: x,
      sourceY: y,
      emotion,
      intensity: intensity * this.config.effectIntensity,
      startTime: Date.now(),
      duration: 3000 / this.config.animationSpeed,
      color: this.emotionColors[emotion as keyof typeof this.emotionColors] || '#87CEEB'
    }

    this.activeEffects.set(effectId, effect)
    return effectId
  }

  /**
   * Create particle effect between bees
   */
  createParticles(
    sourceX: number,
    sourceY: number,
    targetX: number,
    targetY: number,
    emotion: string,
    intensity: number = 1.0
  ): string {
    if (!this.config.enabled || !this.config.showParticles) return ''

    const effectId = `particles_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    
    const effect: VisualEffect = {
      id: effectId,
      type: 'particle',
      sourceX,
      sourceY,
      targetX,
      targetY,
      emotion,
      intensity: intensity * this.config.effectIntensity,
      startTime: Date.now(),
      duration: 2500 / this.config.animationSpeed,
      color: this.emotionColors[emotion as keyof typeof this.emotionColors] || '#87CEEB'
    }

    this.activeEffects.set(effectId, effect)
    return effectId
  }

  /**
   * Start animation loop
   */
  private startAnimation(): void {
    if (this.animationFrame) return

    const animate = () => {
      this.render()
      this.cleanupExpiredEffects()
      this.animationFrame = requestAnimationFrame(animate)
    }

    animate()
  }

  /**
   * Stop animation loop
   */
  stopAnimation(): void {
    if (this.animationFrame) {
      cancelAnimationFrame(this.animationFrame)
      this.animationFrame = null
    }
  }

  /**
   * Render all active effects
   */
  private render(): void {
    if (!this.ctx || !this.canvas) return

    // Clear canvas
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height)

    const now = Date.now()

    for (const effect of this.activeEffects.values()) {
      const elapsed = now - effect.startTime
      const progress = Math.min(elapsed / effect.duration, 1)

      switch (effect.type) {
        case 'ripple':
          this.renderRipple(effect, progress)
          break
        case 'connection':
          this.renderConnection(effect, progress)
          break
        case 'aura':
          this.renderAura(effect, progress)
          break
        case 'particle':
          this.renderParticles(effect, progress)
          break
      }
    }
  }

  /**
   * Render ripple effect
   */
  private renderRipple(effect: VisualEffect, progress: number): void {
    if (!this.ctx) return

    const maxRadius = 80 * effect.intensity
    const radius = maxRadius * progress
    const opacity = (1 - progress) * effect.intensity * 0.6

    this.ctx.save()
    this.ctx.globalAlpha = opacity
    this.ctx.strokeStyle = effect.color
    this.ctx.lineWidth = 2
    this.ctx.setLineDash([5, 5])
    this.ctx.beginPath()
    this.ctx.arc(effect.sourceX, effect.sourceY, radius, 0, Math.PI * 2)
    this.ctx.stroke()
    this.ctx.restore()
  }

  /**
   * Render connection line
   */
  private renderConnection(effect: VisualEffect, progress: number): void {
    if (!this.ctx || !effect.targetX || !effect.targetY) return

    const opacity = Math.sin(progress * Math.PI) * effect.intensity * 0.8
    const lineWidth = 2 * effect.intensity

    this.ctx.save()
    this.ctx.globalAlpha = opacity
    this.ctx.strokeStyle = effect.color
    this.ctx.lineWidth = lineWidth
    this.ctx.setLineDash([10, 5])
    this.ctx.lineDashOffset = -progress * 20 // Animated dash movement
    
    this.ctx.beginPath()
    this.ctx.moveTo(effect.sourceX, effect.sourceY)
    this.ctx.lineTo(effect.targetX, effect.targetY)
    this.ctx.stroke()
    this.ctx.restore()
  }

  /**
   * Render aura effect
   */
  private renderAura(effect: VisualEffect, progress: number): void {
    if (!this.ctx) return

    const pulseRadius = 30 + Math.sin(progress * Math.PI * 4) * 10
    const opacity = (1 - progress * 0.5) * effect.intensity * 0.4

    // Create radial gradient
    const gradient = this.ctx.createRadialGradient(
      effect.sourceX, effect.sourceY, 0,
      effect.sourceX, effect.sourceY, pulseRadius
    )
    gradient.addColorStop(0, effect.color + '80') // Semi-transparent center
    gradient.addColorStop(1, effect.color + '00') // Transparent edge

    this.ctx.save()
    this.ctx.globalAlpha = opacity
    this.ctx.fillStyle = gradient
    this.ctx.beginPath()
    this.ctx.arc(effect.sourceX, effect.sourceY, pulseRadius, 0, Math.PI * 2)
    this.ctx.fill()
    this.ctx.restore()
  }

  /**
   * Render particle effect
   */
  private renderParticles(effect: VisualEffect, progress: number): void {
    if (!this.ctx || !effect.targetX || !effect.targetY) return

    const particleCount = Math.floor(5 * effect.intensity)
    
    for (let i = 0; i < particleCount; i++) {
      const particleProgress = (progress + i * 0.1) % 1
      const x = effect.sourceX + (effect.targetX - effect.sourceX) * particleProgress
      const y = effect.sourceY + (effect.targetY - effect.sourceY) * particleProgress
      
      // Add some randomness to particle movement
      const wobble = Math.sin(particleProgress * Math.PI * 4 + i) * 5
      const finalX = x + wobble
      const finalY = y + wobble * 0.5

      const opacity = Math.sin(particleProgress * Math.PI) * effect.intensity * 0.8
      const size = 3 * effect.intensity

      this.ctx.save()
      this.ctx.globalAlpha = opacity
      this.ctx.fillStyle = effect.color
      this.ctx.beginPath()
      this.ctx.arc(finalX, finalY, size, 0, Math.PI * 2)
      this.ctx.fill()
      this.ctx.restore()
    }
  }

  /**
   * Remove expired effects
   */
  private cleanupExpiredEffects(): void {
    const now = Date.now()
    
    for (const [id, effect] of this.activeEffects.entries()) {
      if (now - effect.startTime > effect.duration) {
        this.activeEffects.delete(id)
      }
    }
  }

  /**
   * Remove specific effect
   */
  removeEffect(effectId: string): void {
    this.activeEffects.delete(effectId)
  }

  /**
   * Clear all effects
   */
  clearAllEffects(): void {
    this.activeEffects.clear()
  }

  /**
   * Configure visualization settings
   */
  configure(newConfig: Partial<VisualizationConfig>): void {
    this.config = { ...this.config, ...newConfig }
  }

  /**
   * Get current configuration
   */
  getConfig(): VisualizationConfig {
    return { ...this.config }
  }

  /**
   * Get visualization metrics
   */
  getMetrics(): {
    activeEffects: number
    effectsByType: Record<string, number>
    averageIntensity: number
  } {
    const effects = Array.from(this.activeEffects.values())
    const effectsByType: Record<string, number> = {}
    let totalIntensity = 0

    for (const effect of effects) {
      effectsByType[effect.type] = (effectsByType[effect.type] || 0) + 1
      totalIntensity += effect.intensity
    }

    return {
      activeEffects: effects.length,
      effectsByType,
      averageIntensity: effects.length > 0 ? totalIntensity / effects.length : 0
    }
  }

  /**
   * Get system status
   */
  getStatus(): {
    status: string
    enabled: boolean
    activeEffects: number
    canvasReady: boolean
  } {
    return {
      status: 'active',
      enabled: this.config.enabled,
      activeEffects: this.activeEffects.size,
      canvasReady: !!(this.canvas && this.ctx)
    }
  }

  /**
   * Cleanup resources
   */
  destroy(): void {
    this.stopAnimation()
    this.clearAllEffects()
    this.canvas = null
    this.ctx = null
  }
}

// Export singleton instance
export const influenceVisualizer = new InfluenceVisualizer()