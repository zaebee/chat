<template>
  <div class="sacred-academy-selector">
    <!-- Header -->
    <div class="academy-header">
      <h1 class="sacred-title">
        🏛️ Sacred Team Academy
      </h1>
      <p class="sacred-subtitle">
        Transform GitHub Issues into Learning Adventures
      </p>
    </div>

    <!-- Student Progress Overview -->
    <div class="progress-overview">
      <div class="progress-card">
        <div class="progress-stat">
          <span class="stat-value">{{ studentProgress.totalXP }}</span>
          <span class="stat-label">Sacred XP</span>
        </div>
        <div class="progress-stat">
          <span class="stat-value">{{ studentProgress.completedChallenges.length }}</span>
          <span class="stat-label">Challenges Completed</span>
        </div>
        <div class="progress-stat">
          <span class="stat-value">{{ studentProgress.sacredLevel }}</span>
          <span class="stat-label">Sacred Level</span>
        </div>
      </div>
    </div>

    <!-- Filter Controls -->
    <div class="filter-controls">
      <div class="filter-group">
        <label>Sacred Difficulty:</label>
        <select v-model="selectedDifficulty" @change="filterChallenges">
          <option value="">All Levels</option>
          <option value="bee.larva">🐛 bee.larva (Beginner)</option>
          <option value="bee.pupa">🛡️ bee.pupa (Intermediate)</option>
          <option value="bee.adult">🐝 bee.adult (Advanced)</option>
          <option value="bee.sacred">👑 bee.sacred (Master)</option>
        </select>
      </div>

      <div class="filter-group">
        <label>Sacred Mentor:</label>
        <select v-model="selectedMentor" @change="filterChallenges">
          <option value="">All Mentors</option>
          <option value="bee.jules">🔧 bee.Jules (Technical Guide)</option>
          <option value="bee.chronicler">📜 bee.chronicler (Sacred Keeper)</option>
          <option value="bee.sage">🧙 bee.Sage (Wise Synthesizer)</option>
        </select>
      </div>

      <div class="filter-group">
        <label>ATCG Classification:</label>
        <select v-model="selectedATCG" @change="filterChallenges">
          <option value="">All Classifications</option>
          <option value="A">🏗️ A (Aggregate) - Structure & State</option>
          <option value="T">⚡ T (Transformation) - Processing & Logic</option>
          <option value="C">🔗 C (Connector) - Communication & Integration</option>
          <option value="G">🌟 G (Genesis) - Events & Generation</option>
        </select>
      </div>
    </div>

    <!-- Recommended Challenge -->
    <div v-if="recommendedChallenge" class="recommended-challenge">
      <h3>🎯 Recommended for You</h3>
      <ChallengeCard 
        :challenge="recommendedChallenge" 
        :is-recommended="true"
        @start-challenge="startChallenge"
      />
    </div>

    <!-- Learning Paths -->
    <div class="learning-paths">
      <h3>🛤️ Sacred Learning Paths</h3>
      <div class="paths-grid">
        <div 
          v-for="path in learningPaths" 
          :key="path.id"
          class="learning-path-card"
          @click="selectLearningPath(path)"
        >
          <h4>{{ path.name }}</h4>
          <p>{{ path.description }}</p>
          <div class="path-progress">
            <div class="progress-bar">
              <div 
                class="progress-fill" 
                :style="{ width: `${getPathProgress(path)}%` }"
              ></div>
            </div>
            <span class="progress-text">
              {{ getCompletedChallengesInPath(path) }}/{{ path.challenges.length }} completed
            </span>
          </div>
          <div class="path-reward">
            <span class="xp-reward">{{ path.totalXP }} XP</span>
            <span class="mastery-reward">{{ path.sacredMastery }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Challenge Grid -->
    <div class="challenges-section">
      <h3>🎓 Available Challenges</h3>
      
      <!-- ATCG Classification Tabs -->
      <div class="atcg-tabs">
        <button 
          v-for="classification in atcgClassifications"
          :key="classification.type"
          :class="['atcg-tab', { active: selectedATCG === classification.type }]"
          @click="selectATCGTab(classification.type)"
        >
          {{ classification.icon }} {{ classification.type }}
          <span class="tab-count">({{ getChallengesByATCG(classification.type).length }})</span>
        </button>
      </div>

      <!-- Challenges Grid -->
      <div class="challenges-grid">
        <ChallengeCard
          v-for="challenge in filteredChallenges"
          :key="challenge.id"
          :challenge="challenge"
          :student-progress="studentProgress"
          @start-challenge="startChallenge"
          @view-details="viewChallengeDetails"
        />
      </div>

      <!-- Empty State -->
      <div v-if="filteredChallenges.length === 0" class="empty-state">
        <div class="empty-icon">🔍</div>
        <h3>No challenges match your filters</h3>
        <p>Try adjusting your filters or check back later for new challenges!</p>
        <button @click="clearFilters" class="clear-filters-btn">
          Clear All Filters
        </button>
      </div>
    </div>

    <!-- Challenge Details Modal -->
    <ChallengeDetailsModal
      v-if="selectedChallengeForDetails"
      :challenge="selectedChallengeForDetails"
      :student-progress="studentProgress"
      @close="selectedChallengeForDetails = null"
      @start-challenge="startChallenge"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { 
  SACRED_CHALLENGES, 
  LEARNING_PATHS,
  SacredChallenge, 
  StudentProgress,
  SacredDifficulty,
  SacredMentor,
  ATCGClassification,
  LearningPath
} from '@/utils/sacredAcademy/challenges'
import { sacredAcademy } from '@/utils/sacredAcademy/academy'
import ChallengeCard from './ChallengeCard.vue'
import ChallengeDetailsModal from './ChallengeDetailsModal.vue'

// Reactive state
const selectedDifficulty = ref<SacredDifficulty | ''>('')
const selectedMentor = ref<SacredMentor | ''>('')
const selectedATCG = ref<ATCGClassification | ''>('')
const selectedChallengeForDetails = ref<SacredChallenge | null>(null)
const studentProgress = ref<StudentProgress>(sacredAcademy.getProgress())

// ATCG Classifications for tabs
const atcgClassifications = [
  { type: 'A' as ATCGClassification, icon: '🏗️', name: 'Aggregate', description: 'Structure & State Management' },
  { type: 'T' as ATCGClassification, icon: '⚡', name: 'Transformation', description: 'Processing & Logic' },
  { type: 'C' as ATCGClassification, icon: '🔗', name: 'Connector', description: 'Communication & Integration' },
  { type: 'G' as ATCGClassification, icon: '🌟', name: 'Genesis', description: 'Events & Generation' }
]

// Computed properties
const recommendedChallenge = computed(() => {
  return sacredAcademy.getRecommendedChallenge()
})

const learningPaths = computed(() => LEARNING_PATHS)

const filteredChallenges = computed(() => {
  let challenges = SACRED_CHALLENGES.filter(challenge => {
    // Filter by availability (not completed, prerequisites met)
    if (studentProgress.value.completedChallenges.includes(challenge.id)) return false
    
    if (challenge.prerequisites) {
      const prerequisitesMet = challenge.prerequisites.every(prereq => 
        studentProgress.value.completedChallenges.includes(prereq)
      )
      if (!prerequisitesMet) return false
    }
    
    return true
  })

  // Apply filters
  if (selectedDifficulty.value) {
    challenges = challenges.filter(c => c.difficulty === selectedDifficulty.value)
  }
  
  if (selectedMentor.value) {
    challenges = challenges.filter(c => c.mentor === selectedMentor.value)
  }
  
  if (selectedATCG.value) {
    challenges = challenges.filter(c => c.atcgClassification === selectedATCG.value)
  }

  return challenges
})

// Methods
const filterChallenges = () => {
  // Reactive filtering happens automatically through computed property
}

const selectATCGTab = (classification: ATCGClassification) => {
  selectedATCG.value = selectedATCG.value === classification ? '' : classification
}

const getChallengesByATCG = (classification: ATCGClassification) => {
  return SACRED_CHALLENGES.filter(c => c.atcgClassification === classification)
}

const clearFilters = () => {
  selectedDifficulty.value = ''
  selectedMentor.value = ''
  selectedATCG.value = ''
}

const startChallenge = (challengeId: string) => {
  // Start the challenge through the academy system
  const attempt = sacredAcademy.startChallenge(challengeId)
  
  // Navigate to challenge interface (would be implemented)
  console.log('Starting challenge:', challengeId, attempt)
  
  // Emit event to parent or use router
  // router.push(`/academy/challenge/${challengeId}`)
}

const viewChallengeDetails = (challenge: SacredChallenge) => {
  selectedChallengeForDetails.value = challenge
}

const selectLearningPath = (path: LearningPath) => {
  // Find first incomplete challenge in path
  const nextChallenge = path.challenges.find(challengeId => 
    !studentProgress.value.completedChallenges.includes(challengeId)
  )
  
  if (nextChallenge) {
    startChallenge(nextChallenge)
  }
}

const getPathProgress = (path: LearningPath): number => {
  const completed = getCompletedChallengesInPath(path)
  return (completed / path.challenges.length) * 100
}

const getCompletedChallengesInPath = (path: LearningPath): number => {
  return path.challenges.filter(challengeId => 
    studentProgress.value.completedChallenges.includes(challengeId)
  ).length
}

// Lifecycle
onMounted(() => {
  // Update progress from academy
  studentProgress.value = sacredAcademy.getProgress()
})
</script>

<style scoped>
.sacred-academy-selector {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  font-family: 'Inter', sans-serif;
}

.academy-header {
  text-align: center;
  margin-bottom: 2rem;
}

.sacred-title {
  font-size: 2.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.5rem;
}

.sacred-subtitle {
  font-size: 1.2rem;
  color: #6b7280;
  margin: 0;
}

.progress-overview {
  margin-bottom: 2rem;
}

.progress-card {
  display: flex;
  justify-content: center;
  gap: 2rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.progress-stat {
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
}

.stat-label {
  font-size: 0.875rem;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.filter-controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-group label {
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
}

.filter-group select {
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: white;
  font-size: 0.875rem;
  min-width: 200px;
}

.recommended-challenge {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border-radius: 12px;
  border: 1px solid #f59e0b;
}

.recommended-challenge h3 {
  margin: 0 0 1rem 0;
  color: #92400e;
  font-weight: 700;
}

.learning-paths {
  margin-bottom: 2rem;
}

.learning-paths h3 {
  margin-bottom: 1rem;
  color: #1e293b;
  font-weight: 700;
}

.paths-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}

.learning-path-card {
  padding: 1.5rem;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.learning-path-card:hover {
  border-color: #667eea;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
  transform: translateY(-2px);
}

.learning-path-card h4 {
  margin: 0 0 0.5rem 0;
  color: #1e293b;
  font-weight: 600;
}

.learning-path-card p {
  margin: 0 0 1rem 0;
  color: #64748b;
  font-size: 0.875rem;
}

.path-progress {
  margin-bottom: 1rem;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 0.75rem;
  color: #64748b;
}

.path-reward {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.75rem;
}

.xp-reward {
  color: #059669;
  font-weight: 600;
}

.mastery-reward {
  color: #7c3aed;
  font-style: italic;
}

.challenges-section h3 {
  margin-bottom: 1rem;
  color: #1e293b;
  font-weight: 700;
}

.atcg-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.atcg-tab {
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
  font-weight: 500;
}

.atcg-tab:hover {
  border-color: #667eea;
  background: #f8fafc;
}

.atcg-tab.active {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.tab-count {
  margin-left: 0.5rem;
  opacity: 0.7;
}

.challenges-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #64748b;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  margin: 0 0 0.5rem 0;
  color: #374151;
}

.empty-state p {
  margin: 0 0 1.5rem 0;
}

.clear-filters-btn {
  padding: 0.75rem 1.5rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.2s ease;
}

.clear-filters-btn:hover {
  background: #5a67d8;
}

@media (max-width: 768px) {
  .sacred-academy-selector {
    padding: 1rem;
  }
  
  .progress-card {
    flex-direction: column;
    gap: 1rem;
  }
  
  .filter-controls {
    flex-direction: column;
  }
  
  .filter-group select {
    min-width: auto;
  }
  
  .atcg-tabs {
    justify-content: center;
  }
  
  .challenges-grid {
    grid-template-columns: 1fr;
  }
}
</style>