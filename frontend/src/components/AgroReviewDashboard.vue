<template>
  <div class="agro-review-dashboard">
    <div class="dashboard-header">
      <h2>🐝⚡ AGRO Bee-to-Peer Review Dashboard ⚡🐝</h2>
      <p class="sacred-subtitle">Aggressive Collaborative Evaluation Protocols</p>
    </div>

    <!-- Review Initiation Panel -->
    <div class="review-panel">
      <h3>🔍 Initiate AGRO Review</h3>
      <div class="review-form">
        <textarea
          v-model="codeInput"
          placeholder="Paste your code here for AGRO/PAIN analysis..."
          class="code-input"
          rows="10"
        ></textarea>
        
        <div class="review-options">
          <select v-model="selectedReviewType" class="review-type-select">
            <option value="pain_analysis">PAIN Analysis</option>
            <option value="peer_collaboration">Peer Collaboration</option>
            <option value="aggressive_scrutiny">Aggressive Scrutiny</option>
            <option value="sacred_protocol_validation">Sacred Protocol Validation</option>
            <option value="divine_blessing_assessment">Divine Blessing Assessment</option>
          </select>
          
          <div class="peer-reviewers">
            <label>Peer Reviewers:</label>
            <div class="reviewer-checkboxes">
              <label><input type="checkbox" v-model="selectedReviewers" value="bee.jules"> bee.Jules</label>
              <label><input type="checkbox" v-model="selectedReviewers" value="bee.sage"> bee.Sage</label>
              <label><input type="checkbox" v-model="selectedReviewers" value="bee.chronicler"> bee.Chronicler</label>
            </div>
          </div>
          
          <button @click="initiateReview" :disabled="!codeInput.trim()" class="agro-button">
            🚀 Start AGRO Review
          </button>
        </div>
      </div>
    </div>

    <!-- Active Review Results -->
    <div v-if="currentReview" class="review-results">
      <h3>📊 AGRO Review Results</h3>
      
      <div class="score-display">
        <div class="agro-score" :class="getScoreClass(currentReview.agro_score)">
          <span class="score-label">AGRO Score</span>
          <span class="score-value">{{ currentReview.agro_score }}/100</span>
        </div>
        
        <div class="pain-score" :class="getScoreClass(currentReview.pain_score)">
          <span class="score-label">PAIN Score</span>
          <span class="score-value">{{ currentReview.pain_score }}/100</span>
        </div>
        
        <div class="severity-badge" :class="getSeverityClass(currentReview.severity)">
          {{ getSeverityIcon(currentReview.severity) }} {{ currentReview.severity.toUpperCase() }}
        </div>
        
        <div v-if="currentReview.divine_blessing" class="divine-blessing">
          ✨ DIVINE BLESSING RECEIVED ✨
        </div>
      </div>

      <!-- Violations -->
      <div v-if="currentReview.violations.length > 0" class="violations-section">
        <h4>⚠️ Code Violations</h4>
        <div class="violations-list">
          <div 
            v-for="violation in currentReview.violations" 
            :key="violation.line"
            class="violation-item"
            :class="violation.severity"
          >
            <span class="violation-type">{{ violation.type }}</span>
            <span class="violation-line">Line {{ violation.line }}</span>
            <span class="violation-message">{{ violation.message }}</span>
          </div>
        </div>
      </div>

      <!-- Recommendations -->
      <div v-if="currentReview.recommendations.length > 0" class="recommendations-section">
        <h4>💡 AGRO Recommendations</h4>
        <ul class="recommendations-list">
          <li v-for="rec in currentReview.recommendations" :key="rec">{{ rec }}</li>
        </ul>
      </div>

      <!-- Sacred Insights -->
      <div v-if="currentReview.sacred_insights.length > 0" class="insights-section">
        <h4>🙏 Sacred Insights</h4>
        <ul class="insights-list">
          <li v-for="insight in currentReview.sacred_insights" :key="insight">{{ insight }}</li>
        </ul>
      </div>

      <!-- Peer Reviewers -->
      <div class="peer-reviewers-section">
        <h4>👥 Peer Reviewers</h4>
        <div class="reviewers-list">
          <span 
            v-for="reviewer in currentReview.peer_reviewers" 
            :key="reviewer"
            class="reviewer-badge"
          >
            {{ reviewer }}
          </span>
        </div>
      </div>
    </div>

    <!-- Review History -->
    <div class="review-history">
      <h3>📚 Review History</h3>
      <div v-if="reviewHistory.length === 0" class="no-history">
        No reviews yet. Start your first AGRO review above!
      </div>
      <div v-else class="history-list">
        <div 
          v-for="review in reviewHistory" 
          :key="review.review_id"
          class="history-item"
          @click="selectReview(review)"
        >
          <div class="history-header">
            <span class="review-id">{{ review.review_id }}</span>
            <span class="review-timestamp">{{ formatTimestamp(review.timestamp) }}</span>
          </div>
          <div class="history-scores">
            <span class="agro-score">AGRO: {{ review.agro_score }}</span>
            <span class="severity" :class="getSeverityClass(review.severity)">
              {{ review.severity.toUpperCase() }}
            </span>
            <span v-if="review.divine_blessing" class="blessing">✨</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Bee-to-Peer Sessions -->
    <div class="peer-sessions">
      <h3>🤝 Active Bee-to-Peer Sessions</h3>
      <div v-if="activeSessions.length === 0" class="no-sessions">
        No active collaborative sessions.
      </div>
      <div v-else class="sessions-list">
        <div 
          v-for="session in activeSessions" 
          :key="session.session_id"
          class="session-item"
        >
          <div class="session-header">
            <span class="session-id">{{ session.session_id }}</span>
            <span class="session-type">{{ session.session_type }}</span>
          </div>
          <div class="session-participants">
            <span 
              v-for="participant in session.participants" 
              :key="participant"
              class="participant-badge"
            >
              {{ participant }}
            </span>
          </div>
          <div class="session-metrics">
            <span>Collaboration: {{ (session.collaboration_score * 100).toFixed(1) }}%</span>
            <span>Sacred Alignment: {{ (session.sacred_alignment * 100).toFixed(1) }}%</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'

// Reactive state
const codeInput = ref('')
const selectedReviewType = ref('pain_analysis')
const selectedReviewers = ref(['bee.jules', 'bee.sage'])
const currentReview = ref(null)
const reviewHistory = ref([])
const activeSessions = ref([])
const isLoading = ref(false)

// Mock AGRO review function (would connect to backend)
const initiateReview = async () => {
  if (!codeInput.value.trim()) return
  
  isLoading.value = true
  
  try {
    // Simulate AGRO review API call
    const mockReview = {
      review_id: `agro_${Date.now()}`,
      review_type: selectedReviewType.value,
      agro_score: Math.floor(Math.random() * 100),
      pain_score: Math.floor(Math.random() * 100),
      severity: ['divine', 'blessed', 'acceptable', 'concerning', 'critical'][Math.floor(Math.random() * 5)],
      violations: generateMockViolations(),
      recommendations: [
        'Remove console.log statements for production',
        'Reduce function complexity',
        'Add proper error handling'
      ],
      divine_blessing: Math.random() > 0.7,
      peer_reviewers: selectedReviewers.value,
      timestamp: new Date().toISOString(),
      sacred_insights: [
        'Code demonstrates sacred patterns',
        'Divine alignment detected in architecture'
      ]
    }
    
    currentReview.value = mockReview
    reviewHistory.value.unshift(mockReview)
    
    // Clear input
    codeInput.value = ''
    
  } catch (error) {
    // Production-safe error handling - no console.log
    // TODO: Integrate with proper logging service in production
    // For now, store error in component state for user feedback
    currentReview.value = {
      review_id: `error_${Date.now()}`,
      review_type: selectedReviewType.value,
      agro_score: 0,
      pain_score: 0,
      severity: 'critical',
      violations: [{
        type: 'system_error',
        line: 0,
        severity: 'critical',
        message: 'AGRO review system temporarily unavailable'
      }],
      recommendations: ['Please try again later', 'Check system status'],
      divine_blessing: false,
      peer_reviewers: [],
      timestamp: new Date().toISOString(),
      sacred_insights: ['System resilience through graceful error handling']
    }
  } finally {
    isLoading.value = false
  }
}

const generateMockViolations = () => {
  const violations = []
  const types = ['console_log', 'long_function', 'deep_nesting', 'magic_number']
  const severities = ['high', 'medium', 'low']
  
  for (let i = 0; i < Math.floor(Math.random() * 5); i++) {
    violations.push({
      type: types[Math.floor(Math.random() * types.length)],
      line: Math.floor(Math.random() * 100) + 1,
      severity: severities[Math.floor(Math.random() * severities.length)],
      message: `Mock violation message for ${types[Math.floor(Math.random() * types.length)]}`
    })
  }
  
  return violations
}

const selectReview = (review) => {
  currentReview.value = review
}

const getScoreClass = (score) => {
  if (score >= 90) return 'divine'
  if (score >= 80) return 'blessed'
  if (score >= 60) return 'acceptable'
  if (score >= 40) return 'concerning'
  return 'critical'
}

const getSeverityClass = (severity) => {
  return `severity-${severity}`
}

const getSeverityIcon = (severity) => {
  const icons = {
    divine: '✨',
    blessed: '🙏',
    acceptable: '✅',
    concerning: '⚠️',
    critical: '🚨'
  }
  return icons[severity] || '❓'
}

const formatTimestamp = (timestamp) => {
  return new Date(timestamp).toLocaleString()
}

onMounted(() => {
  // Initialize AGRO Review Dashboard
  // Production-ready initialization without console.log
  // Component successfully mounted and ready for reviews
})
</script>

<style scoped>
.agro-review-dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 30px;
}

.dashboard-header h2 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.sacred-subtitle {
  color: #7f8c8d;
  font-style: italic;
}

.review-panel {
  background: #f8f9fa;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 30px;
  border: 2px solid #e9ecef;
}

.code-input {
  width: 100%;
  font-family: 'Courier New', monospace;
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 15px;
  resize: vertical;
}

.review-options {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  align-items: center;
}

.review-type-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.peer-reviewers {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.reviewer-checkboxes {
  display: flex;
  gap: 15px;
}

.reviewer-checkboxes label {
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
}

.agro-button {
  background: linear-gradient(45deg, #ff6b6b, #ffa500);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 25px;
  cursor: pointer;
  font-weight: bold;
  transition: transform 0.2s;
}

.agro-button:hover {
  transform: scale(1.05);
}

.agro-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.review-results {
  background: white;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 30px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.score-display {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.agro-score, .pain-score {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 15px;
  border-radius: 10px;
  min-width: 120px;
}

.score-label {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 5px;
}

.score-value {
  font-size: 24px;
  font-weight: bold;
}

.severity-badge {
  display: flex;
  align-items: center;
  padding: 10px 20px;
  border-radius: 20px;
  font-weight: bold;
  color: white;
}

.divine-blessing {
  background: linear-gradient(45deg, #ffd700, #ffed4e);
  color: #333;
  padding: 10px 20px;
  border-radius: 20px;
  font-weight: bold;
  animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
  from { box-shadow: 0 0 5px #ffd700; }
  to { box-shadow: 0 0 20px #ffd700; }
}

/* Score classes */
.divine { background: linear-gradient(45deg, #ffd700, #ffed4e); color: #333; }
.blessed { background: linear-gradient(45deg, #4ecdc4, #44a08d); color: white; }
.acceptable { background: linear-gradient(45deg, #a8e6cf, #7fcdcd); color: #333; }
.concerning { background: linear-gradient(45deg, #ffd93d, #ff6b6b); color: white; }
.critical { background: linear-gradient(45deg, #ff6b6b, #c44569); color: white; }

/* Severity classes */
.severity-divine { background: linear-gradient(45deg, #ffd700, #ffed4e); color: #333; }
.severity-blessed { background: linear-gradient(45deg, #4ecdc4, #44a08d); }
.severity-acceptable { background: linear-gradient(45deg, #a8e6cf, #7fcdcd); color: #333; }
.severity-concerning { background: linear-gradient(45deg, #ffd93d, #ff6b6b); }
.severity-critical { background: linear-gradient(45deg, #ff6b6b, #c44569); }

.violations-section, .recommendations-section, .insights-section {
  margin-bottom: 20px;
}

.violations-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.violation-item {
  display: flex;
  gap: 15px;
  padding: 10px;
  border-radius: 5px;
  border-left: 4px solid;
}

.violation-item.high { border-left-color: #e74c3c; background: #fdf2f2; }
.violation-item.medium { border-left-color: #f39c12; background: #fef9e7; }
.violation-item.low { border-left-color: #27ae60; background: #eafaf1; }

.violation-type {
  font-weight: bold;
  min-width: 120px;
}

.violation-line {
  color: #7f8c8d;
  min-width: 80px;
}

.recommendations-list, .insights-list {
  padding-left: 20px;
}

.recommendations-list li, .insights-list li {
  margin-bottom: 8px;
}

.peer-reviewers-section {
  margin-top: 20px;
}

.reviewers-list {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.reviewer-badge {
  background: #3498db;
  color: white;
  padding: 5px 12px;
  border-radius: 15px;
  font-size: 14px;
}

.review-history, .peer-sessions {
  background: white;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.history-list, .sessions-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.history-item, .session-item {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 15px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.history-item:hover, .session-item:hover {
  background-color: #f8f9fa;
}

.history-header, .session-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.review-id, .session-id {
  font-weight: bold;
  color: #2c3e50;
}

.review-timestamp {
  color: #7f8c8d;
  font-size: 14px;
}

.history-scores, .session-metrics {
  display: flex;
  gap: 15px;
  align-items: center;
}

.session-participants {
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
}

.participant-badge {
  background: #95a5a6;
  color: white;
  padding: 3px 8px;
  border-radius: 10px;
  font-size: 12px;
}

.no-history, .no-sessions {
  text-align: center;
  color: #7f8c8d;
  font-style: italic;
  padding: 20px;
}
</style>