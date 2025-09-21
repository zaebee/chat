<template>
  <div class="hive-bee-test">
    <h2>🐝 Hive-Aligned Bee Dancing Test</h2>
    
    <div class="test-controls">
      <div class="control-group">
        <label>Physics Scale:</label>
        <input 
          v-model.number="physicsConfig.scaleFactor" 
          type="range" 
          min="0.5" 
          max="2" 
          step="0.1"
        />
        <span>{{ physicsConfig.scaleFactor }}x</span>
      </div>
      
      <div class="control-group">
        <label>Activity Level:</label>
        <input 
          v-model.number="intentConfig.activityLevel" 
          type="range" 
          min="0" 
          max="1" 
          step="0.1"
        />
        <span>{{ Math.round(intentConfig.activityLevel * 100) }}%</span>
      </div>
      
      <div class="control-group">
        <label>Collaboration Mode:</label>
        <select v-model="intentConfig.collaborationMode">
          <option value="individual">Individual</option>
          <option value="swarm">Swarm</option>
          <option value="sacred">Sacred</option>
        </select>
      </div>
      
      <div class="control-group">
        <label>Emotional State:</label>
        <select v-model="intentConfig.emotionalState">
          <option value="calm">Calm</option>
          <option value="excited">Excited</option>
          <option value="focused">Focused</option>
          <option value="protective">Protective</option>
          <option value="divine">Divine</option>
        </select>
      </div>
      
      <!-- Smooth Transitions Controls -->
      <div class="control-group">
        <label>
          <input 
            v-model="smoothTransitions" 
            type="checkbox"
            class="smooth-checkbox"
          />
          Smooth Transitions
        </label>
        <span :class="smoothTransitions ? 'enabled' : 'disabled'">
          {{ smoothTransitions ? '✅ Enabled' : '❌ Disabled' }}
        </span>
      </div>
      
      <div class="control-group" v-if="smoothTransitions">
        <label>Transition Duration:</label>
        <input 
          v-model.number="transitionDuration" 
          type="range" 
          min="100" 
          max="2000" 
          step="100"
        />
        <span>{{ transitionDuration }}ms</span>
      </div>
      
      <!-- Test Buttons -->
      <div class="control-group">
        <button @click="testRapidChanges" class="test-button">
          🎯 Test Rapid Changes
        </button>
        <button @click="testExtremeTransitions" class="test-button">
          ⚡ Test Extreme Transitions
        </button>
        <button @click="testCollaborationModes" class="test-button">
          🤝 Test Collaboration Modes
        </button>
      </div>
    </div>

    <div class="bee-showcase">
      <div class="bee-row" v-for="role in beeRoles" :key="role">
        <div class="bee-info">
          <h3>{{ role }}</h3>
          <div class="bee-stats">
            <div>Morph: {{ getMorphologyInfo(role) }}</div>
            <div>Intent: {{ getIntentInfo(role) }}</div>
            <div>Events: {{ getEventCount(role) }}</div>
          </div>
        </div>
        
        <div class="bee-container">
          <!-- Original Magic Numbers Bee -->
          <div class="bee-comparison">
            <h4>Original (Magic Numbers)</h4>
            <BeeOrganella :type="role" :size="physicsConfig.scaleFactor" />
          </div>
          
          <!-- Hive-Aligned Bee -->
          <div class="bee-comparison">
            <h4>Hive-Aligned (Physics + Intent)</h4>
            <BeeOrganellaHive 
              :type="role"
              :physics="physicsConfig"
              :intent="getIntentForRole(role)"
              :smoothTransitions="smoothTransitions"
              @pollen-event="handlePollenEvent"
            />
          </div>
        </div>
      </div>
    </div>

    <div class="metrics-panel">
      <h3>🌿 Hive Metrics</h3>
      <div class="metrics-grid">
        <div class="metric">
          <label>Physics Status:</label>
          <span :class="physicsStatus.status">{{ physicsStatus.status }}</span>
        </div>
        <div class="metric">
          <label>Intent Engine:</label>
          <span :class="intentStatus.status">{{ intentStatus.status }}</span>
        </div>
        <div class="metric">
          <label>Pollen Events:</label>
          <span>{{ pollenMetrics.eventsEmitted }}</span>
        </div>
        <div class="metric">
          <label>Active Bees:</label>
          <span>{{ intentStatus.trackedBees }}</span>
        </div>
        <div class="metric">
          <label>Active Transitions:</label>
          <span>{{ transitionStatus.activeTransitions }}</span>
        </div>
        <div class="metric">
          <label>Smooth Transitions:</label>
          <span :class="smoothTransitions ? 'enabled' : 'disabled'">
            {{ smoothTransitions ? 'ON' : 'OFF' }}
          </span>
        </div>
      </div>
      
      <div class="event-log">
        <h4>Recent Pollen Events:</h4>
        <div class="events">
          <div 
            v-for="event in recentEvents" 
            :key="event.id"
            class="event"
            :class="event.priority"
          >
            <span class="event-type">{{ event.type }}</span>
            <span class="event-source">{{ event.source }}</span>
            <span class="event-time">{{ formatTime(event.timestamp) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import BeeOrganella from './BeeOrganella.vue'
import BeeOrganellaHive from './BeeOrganellaHive.vue'
import { hivePhysics } from '../utils/hivePhysics'
import { hiveIntentEngine, createIntent } from '../utils/hiveIntent'
import { pollenBus, BeeEventTypes, type PollenEvent } from '../utils/pollenProtocol'
import { intentTransitionManager } from '../utils/intentCocoon'

// Test configuration
const physicsConfig = ref({
  baseUnit: 20,
  scaleFactor: 1,
  aspectRatio: 1.2,
  energyLevel: 0.8
})

const intentConfig = ref({
  activityLevel: 0.7,
  focusIntensity: 0.8,
  collaborationMode: 'individual' as const,
  emotionalState: 'calm' as const
})

// Transition controls
const smoothTransitions = ref(true)
const transitionDuration = ref(1000)

const beeRoles = ['worker', 'scout', 'queen', 'guard', 'chronicler', 'jules'] as const

// Event tracking
const pollenEvents = ref<PollenEvent[]>([])
const eventCounts = ref<Record<string, number>>({})

// Status monitoring
const physicsStatus = computed(() => hivePhysics.getStatus())
const intentStatus = computed(() => hiveIntentEngine.getStatus())
const pollenMetrics = computed(() => pollenBus.getMetrics())
const transitionStatus = computed(() => intentTransitionManager.getStatus())

const recentEvents = computed(() => 
  pollenEvents.value.slice(-10).reverse()
)

// Get intent configuration for each role
const getIntentForRole = (role: string) => {
  return createIntent(role, intentConfig.value)
}

// Get morphology info for display
const getMorphologyInfo = (role: string) => {
  const morphology = hivePhysics.calculateMorphology(role)
  const abdomen = morphology.abdomen.radius
  return `${Math.round(abdomen.x)}×${Math.round(abdomen.y)}`
}

// Get intent info for display
const getIntentInfo = (role: string) => {
  const intent = getIntentForRole(role)
  return `${Math.round(intent.activityLevel * 100)}% / ${intent.emotionalState}`
}

// Get event count for role
const getEventCount = (role: string) => {
  return eventCounts.value[role] || 0
}

// Handle Pollen events
const handlePollenEvent = (event: PollenEvent) => {
  // Filter out high-frequency transition progress events to prevent loops
  if (event.type === 'intent_transition_progress') {
    return
  }
  
  // Validate event structure
  if (!event || typeof event !== 'object') {
    console.warn('Invalid pollen event received:', event)
    return
  }
  
  pollenEvents.value.push(event)
  
  // Update event counts with error handling
  try {
    if (event.source && typeof event.source === 'string') {
      const sourceRole = event.source.split('_')[0] // Extract role from bee ID
      if (sourceRole) {
        eventCounts.value[sourceRole] = (eventCounts.value[sourceRole] || 0) + 1
      }
    }
  } catch (error) {
    console.warn('Error processing event source:', event.source, error)
  }
  
  // Limit event history
  if (pollenEvents.value.length > 100) {
    pollenEvents.value = pollenEvents.value.slice(-100)
  }
}

// Format timestamp for display
const formatTime = (timestamp: number) => {
  const now = Date.now()
  const diff = now - timestamp
  
  if (diff < 1000) return 'now'
  if (diff < 60000) return `${Math.round(diff / 1000)}s ago`
  return `${Math.round(diff / 60000)}m ago`
}

// Update physics configuration
const updatePhysics = () => {
  hivePhysics.updateConfig(physicsConfig.value)
}

// Test rapid intent changes
const testRapidChanges = () => {
  const states = ['calm', 'excited', 'focused', 'protective', 'divine']
  states.forEach((state, index) => {
    setTimeout(() => {
      intentConfig.value.emotionalState = state as any
    }, index * 300) // 300ms between changes
  })
}

// Test extreme transitions
const testExtremeTransitions = () => {
  // Test extreme activity level changes
  setTimeout(() => {
    intentConfig.value.activityLevel = 0.1
  }, 100)
  setTimeout(() => {
    intentConfig.value.activityLevel = 0.9
  }, 600)
  setTimeout(() => {
    intentConfig.value.activityLevel = 0.5
  }, 1100)
}

// Test collaboration mode changes
const testCollaborationModes = () => {
  const modes = ['individual', 'swarm', 'sacred']
  modes.forEach((mode, index) => {
    setTimeout(() => {
      intentConfig.value.collaborationMode = mode as any
    }, index * 800)
  })
}

// Lifecycle
onMounted(() => {
  // Subscribe to all bee events
  pollenBus.subscribe(['*'], handlePollenEvent)
  
  // Update physics when config changes
  updatePhysics()
})

onUnmounted(() => {
  // Clean up subscriptions
  pollenBus.clearHistory()
})
</script>

<style scoped>
.hive-bee-test {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.test-controls {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.control-group label {
  font-weight: 600;
  color: #333;
}

.control-group input, .control-group select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.bee-showcase {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  margin-bottom: 2rem;
}

.bee-row {
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: 2rem;
  padding: 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: white;
}

.bee-info h3 {
  margin: 0 0 1rem 0;
  color: #333;
  text-transform: capitalize;
}

.bee-stats {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: #666;
}

.bee-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  align-items: center;
}

.bee-comparison {
  text-align: center;
  padding: 1rem;
  border: 1px solid #f0f0f0;
  border-radius: 6px;
}

.bee-comparison h4 {
  margin: 0 0 1rem 0;
  font-size: 0.9rem;
  color: #666;
}

.metrics-panel {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.metric {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem;
  background: white;
  border-radius: 4px;
}

.metric label {
  font-weight: 600;
  color: #333;
}

.metric span.active {
  color: #10b981;
}

.event-log {
  max-height: 200px;
  overflow-y: auto;
}

.events {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.event {
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 1rem;
  padding: 0.25rem 0.5rem;
  background: white;
  border-radius: 4px;
  font-size: 0.8rem;
}

.event.high {
  border-left: 3px solid #f59e0b;
}

.event.critical {
  border-left: 3px solid #ef4444;
}

.event-type {
  font-weight: 600;
  color: #333;
}

.event-source {
  color: #666;
}

.event-time {
  color: #999;
  font-size: 0.7rem;
}

/* Transition Controls */
.smooth-checkbox {
  margin-right: 0.5rem;
}

.enabled {
  color: #10b981;
  font-weight: 600;
}

.disabled {
  color: #ef4444;
  font-weight: 600;
}

.test-button {
  padding: 0.5rem 1rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.test-button:hover {
  background: #2563eb;
}

.test-button:active {
  background: #1d4ed8;
}
</style>