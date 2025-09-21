<template>
  <div class="hive-bee-container" :style="containerStyles">
    <svg 
      class="hive-bee-svg" 
      :viewBox="morphology.viewBox" 
      role="img" 
      :aria-labelledby="`bee-${instanceId}-title`"
    >
      <title :id="`bee-${instanceId}-title`">
        {{ beeMeta.displayName }} - {{ beeMeta.description }}
      </title>

      <defs>
        <!-- Dynamic stripe pattern based on physics -->
        <pattern 
          :id="`stripes-${instanceId}`" 
          :width="morphology.stripeWidth" 
          :height="morphology.stripeHeight" 
          patternUnits="userSpaceOnUse"
        >
          <rect 
            :width="morphology.stripeWidth" 
            :height="morphology.stripeHeight" 
            fill="inherit" 
          />
          <rect 
            :width="morphology.stripeWidth" 
            :height="morphology.stripeHeight / 2" 
            :fill="colorPalette.stripe" 
          />
        </pattern>

        <!-- Sacred aura for divine bees -->
        <filter v-if="beeMeta.isDivine" :id="`divine-aura-${instanceId}`">
          <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
          <feMerge> 
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
      </defs>

      <!-- Bee body constructed from ATCG primitives -->
      <g :id="`bee-aggregate-${instanceId}`" class="bee-aggregate">
        
        <!-- A: Aggregate - Abdomen (core structure) -->
        <ellipse 
          class="bee-part abdomen"
          :cx="morphology.center.x"
          :cy="morphology.abdomen.center.y"
          :rx="morphology.abdomen.radius.x"
          :ry="morphology.abdomen.radius.y"
          :fill="colorPalette.body"
        />
        <ellipse 
          class="bee-part abdomen-stripes"
          :cx="morphology.center.x"
          :cy="morphology.abdomen.center.y"
          :rx="morphology.abdomen.radius.x"
          :ry="morphology.abdomen.radius.y"
          :fill="`url(#stripes-${instanceId})`"
        />

        <!-- A: Aggregate - Thorax (connection hub) -->
        <ellipse 
          class="bee-part thorax"
          :cx="morphology.center.x"
          :cy="morphology.thorax.center.y"
          :rx="morphology.thorax.radius.x"
          :ry="morphology.thorax.radius.y"
          :fill="colorPalette.body"
        />

        <!-- A: Aggregate - Head (processing center) -->
        <circle 
          class="bee-part head"
          :cx="morphology.center.x"
          :cy="morphology.head.center.y"
          :r="morphology.head.radius"
          :fill="colorPalette.body"
        />

        <!-- C: Connector - Wings (communication interfaces) -->
        <g class="wing-connectors">
          <ellipse 
            class="bee-part wing-left"
            :class="animationClasses.wings"
            :cx="morphology.wings.left.center.x"
            :cy="morphology.wings.left.center.y"
            :rx="morphology.wings.left.radius.x"
            :ry="morphology.wings.left.radius.y"
            :fill="colorPalette.wing"
            :style="wingTransformStyle"
          />
          <ellipse 
            class="bee-part wing-right"
            :class="animationClasses.wings"
            :cx="morphology.wings.right.center.x"
            :cy="morphology.wings.right.center.y"
            :rx="morphology.wings.right.radius.x"
            :ry="morphology.wings.right.radius.y"
            :fill="colorPalette.wing"
            :style="wingTransformStyle"
          />
        </g>

        <!-- T: Transformation - Stinger (action interface) -->
        <polygon 
          class="bee-part stinger"
          :points="morphology.stinger.points"
          :fill="colorPalette.stripe"
        />

        <!-- G: Genesis - Role-specific features -->
        <g v-if="beeMeta.hasSpecialFeatures" class="genesis-features">
          
          <!-- Queen Crown -->
          <polygon 
            v-if="type === 'queen'"
            class="bee-part crown"
            :points="morphology.crown.points"
            fill="gold"
            stroke="gold"
          />

          <!-- Chronicler Sacred Elements -->
          <g v-if="type === 'chronicler'" class="sacred-elements">
            <!-- Sacred scroll -->
            <rect
              class="bee-part sacred-scroll"
              :x="morphology.scroll.x"
              :y="morphology.scroll.y"
              :width="morphology.scroll.width"
              :height="morphology.scroll.height"
              :fill="(colorPalette as any).scroll || '#f4e4bc'"
              :stroke="(colorPalette as any).scrollBorder || '#d4af37'"
              stroke-width="1"
              :rx="morphology.scroll.radius"
            />
            
            <!-- Divine emanation -->
            <circle
              class="bee-part divine-emanation"
              :cx="morphology.center.x"
              :cy="morphology.head.center.y"
              :r="morphology.divineAura.radius"
              fill="none"
              :stroke="(colorPalette as any).divine || '#f7dc6f'"
              :stroke-width="morphology.divineAura.strokeWidth"
              :opacity="divineOpacity"
              :class="animationClasses.divine"
            />
            
            <!-- Sacred quill -->
            <line
              class="bee-part sacred-quill"
              :x1="morphology.quill.start.x"
              :y1="morphology.quill.start.y"
              :x2="morphology.quill.end.x"
              :y2="morphology.quill.end.y"
              :stroke="(colorPalette as any).divine || '#f7dc6f'"
              :stroke-width="morphology.quill.strokeWidth"
            />
          </g>

          <!-- Jules Implementation Features -->
          <g v-if="type === 'jules'" class="implementation-features">
            <!-- Debug antenna -->
            <line
              class="bee-part debug-antenna"
              :x1="morphology.antenna.start.x"
              :y1="morphology.antenna.start.y"
              :x2="morphology.antenna.end.x"
              :y2="morphology.antenna.end.y"
              :stroke="(colorPalette as any).debug || '#a855f7'"
              :stroke-width="morphology.antenna.strokeWidth"
            />
          </g>
        </g>
      </g>
    </svg>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted, watch } from 'vue'
import { physicsCocoonEngine } from '@/utils/physicsCocoon'
import { intentTransitionManager, createSmoothTransition, getCurrentTransitionIntent } from '@/utils/intentCocoon'
import type { HiveIntent } from '@/utils/hiveIntent'

// ATCG Primitive Types
interface HivePhysics {
  baseUnit: number
  scaleFactor: number
  aspectRatio: number
  energyLevel: number
}



interface PollenEvent {
  type: string
  payload: any
  timestamp: number
}

// Component Props
const props = defineProps<{
  type: 'worker' | 'scout' | 'queen' | 'guard' | 'chronicler' | 'jules'
  size?: number
  physics?: Partial<HivePhysics>
  intent?: Partial<HiveIntent>
  onPollenEvent?: (event: any) => void
  useCocoon?: boolean  // Enable physics cocoon validation
  smoothTransitions?: boolean  // Enable smooth intent transitions
}>()

// Instance ID for unique SVG elements
const instanceId = ref(`bee_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`)

// Cocoon state
const cocoonState = ref<'none' | 'calculating' | 'validating' | 'manifesting' | 'emerged'>('none')
const cocoonProgress = ref(0)
const validationResults = ref<any[]>([])
const emergenceReady = ref(false)

// Intent transition state
const isTransitioning = ref(false)
const transitionProgress = ref(0)
const baseHiveIntent = ref<HiveIntent | null>(null)

// A: Aggregate - Physics-based calculations
const hivePhysics = computed<HivePhysics>(() => ({
  baseUnit: 20,
  scaleFactor: props.size || 1,
  aspectRatio: 1.2,
  energyLevel: 0.8,
  ...props.physics
}))

// T: Transformation - Intent-driven behavior
const hiveIntent = computed<HiveIntent>(() => {
  const baseIntent: HiveIntent = {
    activityLevel: 0.5,
    focusIntensity: 0.7,
    collaborationMode: 'individual',
    purpose: 'general',
    emotionalState: 'calm',
    socialAlignment: 0.7
  }

  // Role-specific intent modifiers (partial overrides)
  const roleModifiers: Record<string, Partial<HiveIntent>> = {
    worker: { activityLevel: 0.6, purpose: 'construction' },
    scout: { activityLevel: 0.9, focusIntensity: 0.9, purpose: 'exploration' },
    queen: { activityLevel: 0.3, focusIntensity: 0.8, collaborationMode: 'swarm', purpose: 'governance' },
    guard: { activityLevel: 0.7, focusIntensity: 0.95, purpose: 'protection' },
    chronicler: { activityLevel: 0.4, focusIntensity: 0.95, collaborationMode: 'sacred', purpose: 'documentation' },
    jules: { activityLevel: 0.8, focusIntensity: 0.9, collaborationMode: 'sacred', purpose: 'debugging' }
  }

  const calculatedIntent: HiveIntent = {
    ...baseIntent,
    ...(roleModifiers[props.type] || {}),
    ...props.intent
  }

  // Store base intent for transitions
  if (!baseHiveIntent.value) {
    baseHiveIntent.value = calculatedIntent
  }

  // If smooth transitions enabled and transitioning, return interpolated intent
  if (props.smoothTransitions && isTransitioning.value) {
    return getCurrentTransitionIntent(instanceId.value, calculatedIntent)
  }

  return calculatedIntent
})

// Bee metadata derived from type
const beeMeta = computed(() => {
  const meta = {
    worker: { displayName: 'Worker Bee', description: 'Industrious builder', isDivine: false, hasSpecialFeatures: false },
    scout: { displayName: 'Scout Bee', description: 'Agile explorer', isDivine: false, hasSpecialFeatures: false },
    queen: { displayName: 'Queen Bee', description: 'Hive sovereign', isDivine: false, hasSpecialFeatures: true },
    guard: { displayName: 'Guard Bee', description: 'Protective sentinel', isDivine: false, hasSpecialFeatures: false },
    chronicler: { displayName: 'bee.chronicler', description: 'Sacred keeper of patterns', isDivine: true, hasSpecialFeatures: true },
    jules: { displayName: 'bee.Jules', description: 'Implementation detective', isDivine: true, hasSpecialFeatures: true }
  }
  return meta[props.type]
})

// Physics-based morphology calculations (NO MAGIC NUMBERS!)
const morphology = computed(() => {
  const { baseUnit, scaleFactor, aspectRatio } = hivePhysics.value
  const unit = baseUnit * scaleFactor
  
  // Role-specific size modifiers based on intent
  const sizeModifiers = {
    worker: { abdomen: 1.0, thorax: 0.9, head: 0.7, wings: 1.0 },
    scout: { abdomen: 0.8, thorax: 0.8, head: 0.8, wings: 1.1 },
    queen: { abdomen: 1.4, thorax: 1.1, head: 0.8, wings: 1.2 },
    guard: { abdomen: 1.1, thorax: 1.2, head: 0.6, wings: 1.0 },
    chronicler: { abdomen: 0.9, thorax: 0.9, head: 0.8, wings: 1.1 },
    jules: { abdomen: 1.0, thorax: 0.9, head: 0.8, wings: 1.0 }
  }
  
  const modifier = sizeModifiers[props.type]
  const viewBoxSize = unit * 10 // Dynamic viewBox based on unit
  
  return {
    viewBox: `0 0 ${viewBoxSize} ${viewBoxSize * aspectRatio}`,
    center: { x: viewBoxSize / 2, y: viewBoxSize * aspectRatio / 2 },
    
    abdomen: {
      center: { x: viewBoxSize / 2, y: viewBoxSize * aspectRatio * 0.6 },
      radius: { x: unit * 1.2 * modifier.abdomen, y: unit * 1.7 * modifier.abdomen }
    },
    
    thorax: {
      center: { x: viewBoxSize / 2, y: viewBoxSize * aspectRatio * 0.4 },
      radius: { x: unit * 0.9 * modifier.thorax, y: unit * 1.0 * modifier.thorax }
    },
    
    head: {
      center: { x: viewBoxSize / 2, y: viewBoxSize * aspectRatio * 0.22 },
      radius: unit * 0.7 * modifier.head
    },
    
    wings: {
      left: {
        center: { x: viewBoxSize / 2 - unit * 1.0, y: viewBoxSize * aspectRatio * 0.4 },
        radius: { x: unit * 1.5 * modifier.wings, y: unit * 0.7 * modifier.wings }
      },
      right: {
        center: { x: viewBoxSize / 2 + unit * 1.0, y: viewBoxSize * aspectRatio * 0.4 },
        radius: { x: unit * 1.5 * modifier.wings, y: unit * 0.7 * modifier.wings }
      }
    },
    
    stinger: {
      points: `${viewBoxSize / 2},${viewBoxSize * aspectRatio * 0.8} ${viewBoxSize / 2 - unit * 0.2},${viewBoxSize * aspectRatio * 0.9} ${viewBoxSize / 2 + unit * 0.2},${viewBoxSize * aspectRatio * 0.9}`
    },
    
    // Special features
    crown: {
      points: `${viewBoxSize / 2 - unit * 0.4},${viewBoxSize * aspectRatio * 0.12} ${viewBoxSize / 2},${viewBoxSize * aspectRatio * 0.05} ${viewBoxSize / 2 + unit * 0.4},${viewBoxSize * aspectRatio * 0.12}`
    },
    
    scroll: {
      x: viewBoxSize / 2 - unit * 0.75,
      y: viewBoxSize * aspectRatio * 0.1,
      width: unit * 1.5,
      height: unit * 0.4,
      radius: unit * 0.1
    },
    
    divineAura: {
      radius: unit * 1.0,
      strokeWidth: unit * 0.1
    },
    
    quill: {
      start: { x: viewBoxSize / 2 + unit * 0.75, y: viewBoxSize * aspectRatio * 0.22 },
      end: { x: viewBoxSize / 2 + unit * 1.25, y: viewBoxSize * aspectRatio * 0.17 },
      strokeWidth: unit * 0.1
    },
    
    antenna: {
      start: { x: viewBoxSize / 2 + unit * 0.5, y: viewBoxSize * aspectRatio * 0.22 },
      end: { x: viewBoxSize / 2 + unit * 1.0, y: viewBoxSize * aspectRatio * 0.15 },
      strokeWidth: unit * 0.08
    },
    
    stripeWidth: unit * 0.5,
    stripeHeight: unit * 0.5
  }
})

// Intent-driven color palette
const colorPalette = computed(() => {
  const basePalettes = {
    worker: { body: '#f4b400', wing: 'rgba(200,240,255,0.5)', stripe: '#222' },
    scout: { body: '#ffdb55', wing: 'rgba(200,240,255,0.6)', stripe: '#222' },
    queen: { body: '#d4943c', wing: 'rgba(200,240,255,0.4)', stripe: '#222' },
    guard: { body: '#9c6d2c', wing: 'rgba(200,240,255,0.5)', stripe: '#222' },
    chronicler: { 
      body: '#d4af37', 
      wing: 'rgba(212, 175, 55, 0.4)', 
      stripe: '#222',
      divine: '#f7dc6f',
      scroll: '#f4e4bc',
      scrollBorder: '#d4af37'
    },
    jules: { 
      body: '#8b5cf6', 
      wing: 'rgba(139, 92, 246, 0.3)', 
      stripe: '#222',
      debug: '#a855f7'
    }
  }
  
  return basePalettes[props.type]
})

// Intent-driven animation system
const animationClasses = computed(() => {
  const { activityLevel, collaborationMode } = hiveIntent.value
  
  // Wing flap rate based on activity level (physics-driven)
  const flapSpeed = activityLevel > 0.8 ? 'flap-fast' : 
                   activityLevel > 0.5 ? 'flap-normal' : 'flap-slow'
  
  return {
    wings: flapSpeed,
    divine: collaborationMode === 'sacred' ? 'divine-pulse' : ''
  }
})

// Dynamic styles
const containerStyles = computed(() => ({
  '--base-size': `${hivePhysics.value.baseUnit * hivePhysics.value.scaleFactor}px`,
  '--activity-level': hiveIntent.value.activityLevel,
  '--focus-intensity': hiveIntent.value.focusIntensity
}))

const wingTransformStyle = computed(() => ({
  transformOrigin: `${morphology.value.center.x}px ${morphology.value.thorax.center.y}px`
}))

const divineOpacity = computed(() => 
  beeMeta.value.isDivine ? 0.6 : 0
)

// C: Connector - Pollen Protocol integration
const emitPollenEvent = (type: string, payload: any) => {
  const event: PollenEvent = {
    type,
    payload,
    timestamp: Date.now()
  }
  
  if (props.onPollenEvent) {
    props.onPollenEvent(event)
  }
}

// G: Genesis - Lifecycle events with optional cocoon validation
onMounted(async () => {
  if (props.useCocoon) {
    await enterPhysicsCocoon()
  } else {
    // Direct manifestation without cocoon validation
    emitPollenEvent('bee_manifested', {
      type: props.type,
      instanceId: instanceId.value,
      morphology: morphology.value,
      intent: hiveIntent.value
    })
    emergenceReady.value = true
  }
})

onUnmounted(() => {
  // Clean up cocoon if still active
  if (cocoonState.value !== 'none' && cocoonState.value !== 'emerged') {
    physicsCocoonEngine.releaseCocoon(instanceId.value)
  }
  
  // Clean up intent transitions
  if (props.smoothTransitions) {
    intentTransitionManager.cancelTransition(instanceId.value)
  }
})

// Physics Cocoon Integration
const enterPhysicsCocoon = async () => {
  try {
    cocoonState.value = 'calculating'
    
    // Enter cocoon with current constraints
    const constraints = {
      minSize: hivePhysics.value.baseUnit * 0.5,
      maxSize: hivePhysics.value.baseUnit * 3,
      aspectRatioRange: [1.0, 2.0] as [number, number],
      energyEfficiency: hivePhysics.value.energyLevel
    }
    
    const cocoon = await physicsCocoonEngine.enterCocoon(
      instanceId.value,
      props.type,
      constraints
    )
    
    // Monitor cocoon progress
    monitorCocoonProgress()
    
  } catch (error) {
    console.error('Cocoon entry failed:', error)
    cocoonState.value = 'none'
    // Fallback to direct manifestation
    emitPollenEvent('bee_manifested', {
      type: props.type,
      instanceId: instanceId.value,
      morphology: morphology.value,
      intent: hiveIntent.value,
      cocoonFailed: true
    })
    emergenceReady.value = true
  }
}

const monitorCocoonProgress = () => {
  const checkProgress = () => {
    const cocoon = physicsCocoonEngine.getCocoonStatus(instanceId.value)
    if (!cocoon) return
    
    // Update state based on cocoon stage
    switch (cocoon.stage) {
      case 'calculation':
        cocoonState.value = 'calculating'
        cocoonProgress.value = cocoon.calculationProgress * 0.33
        break
      case 'validation':
        cocoonState.value = 'validating'
        cocoonProgress.value = 0.33 + (cocoon.validationProgress * 0.33)
        validationResults.value = cocoon.validationResults
        break
      case 'manifestation':
        cocoonState.value = 'manifesting'
        cocoonProgress.value = 0.66 + (cocoon.manifestationProgress * 0.34)
        break
    }
    
    // Check if emergence is complete
    if (cocoon.stage === 'manifestation' && cocoon.manifestationProgress >= 1.0) {
      cocoonState.value = 'emerged'
      cocoonProgress.value = 1.0
      emergenceReady.value = true
      
      // Emit successful emergence
      emitPollenEvent('bee_manifested', {
        type: props.type,
        instanceId: instanceId.value,
        morphology: cocoon.validatedMorphology,
        intent: hiveIntent.value,
        cocoonValidated: true,
        divineBlessing: cocoon.divineBlessing,
        validationScore: cocoon.validationResults.reduce((sum, r) => sum + r.score, 0) / cocoon.validationResults.length
      })
      
      // Clean up cocoon
      physicsCocoonEngine.releaseCocoon(instanceId.value)
      return
    }
    
    // Continue monitoring
    setTimeout(checkProgress, 100)
  }
  
  checkProgress()
}

// Intent Transition Management
const transitionToIntent = async (newIntent: HiveIntent) => {
  if (!props.smoothTransitions || !baseHiveIntent.value) {
    // Direct change (existing behavior)
    baseHiveIntent.value = newIntent
    return
  }

  try {
    isTransitioning.value = true
    transitionProgress.value = 0

    await createSmoothTransition(
      instanceId.value,
      baseHiveIntent.value,
      newIntent,
      {
        duration: 1000, // 1 second
        easing: 'divine',
        validateTransition: true
      }
    )

    // Update base intent after successful transition
    baseHiveIntent.value = newIntent
    
  } catch (error) {
    console.warn('Intent transition failed:', error)
    // Fallback to direct change
    baseHiveIntent.value = newIntent
  } finally {
    isTransitioning.value = false
    transitionProgress.value = 0
  }
}

// Watch for intent prop changes and trigger smooth transitions
watch(() => props.intent, (newIntent) => {
  if (newIntent && baseHiveIntent.value) {
    const targetIntent = {
      ...baseHiveIntent.value,
      ...newIntent
    }
    transitionToIntent(targetIntent)
  }
}, { deep: true })
</script>

<style scoped>
.hive-bee-container {
  display: inline-block;
  width: var(--base-size);
  height: calc(var(--base-size) * 1.2);
  overflow: visible;
}

.hive-bee-svg {
  width: 100%;
  height: 100%;
  display: block;
}

.bee-part {
  stroke: #222;
  stroke-width: 1.5;
  stroke-linecap: round;
  stroke-linejoin: round;
  vector-effect: non-scaling-stroke;
}

/* Intent-driven animations */
.flap-fast {
  animation: wing-flap calc(0.1s / var(--activity-level)) ease-in-out infinite;
}

.flap-normal {
  animation: wing-flap calc(0.15s / var(--activity-level)) ease-in-out infinite;
}

.flap-slow {
  animation: wing-flap calc(0.25s / var(--activity-level)) ease-in-out infinite;
}

@keyframes wing-flap {
  0% { transform: rotateX(-25deg); }
  50% { transform: rotateX(25deg); }
  100% { transform: rotateX(-25deg); }
}

.divine-pulse {
  animation: divine-emanation calc(3s / var(--focus-intensity)) ease-in-out infinite;
}

@keyframes divine-emanation {
  0%, 100% {
    opacity: 0.3;
    stroke-width: 1;
  }
  50% {
    opacity: 0.8;
    stroke-width: 3;
  }
}

/* Accessibility */
@media (prefers-reduced-motion: reduce) {
  .flap-fast, .flap-normal, .flap-slow, .divine-pulse {
    animation: none;
  }
}
</style>