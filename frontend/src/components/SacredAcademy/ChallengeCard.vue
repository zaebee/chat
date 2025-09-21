<template>
  <div 
    :class="[
      'challenge-card',
      `difficulty-${challenge.difficulty.replace('.', '-')}`,
      { 'recommended': isRecommended, 'locked': isLocked }
    ]"
  >
    <!-- Challenge Header -->
    <div class="challenge-header">
      <div class="challenge-meta">
        <span class="difficulty-badge">{{ getDifficultyIcon(challenge.difficulty) }} {{ challenge.difficulty }}</span>
        <span class="atcg-badge">{{ getATCGIcon(challenge.atcgClassification) }} {{ challenge.atcgClassification }}</span>
      </div>
      <div class="issue-link">
        <a :href="getIssueUrl(challenge.issueNumber)" target="_blank" class="issue-badge">
          #{{ challenge.issueNumber }}
        </a>
      </div>
    </div>

    <!-- Challenge Title -->
    <h3 class="challenge-title">{{ challenge.title }}</h3>
    
    <!-- Challenge Description -->
    <p class="challenge-description">{{ challenge.description }}</p>

    <!-- Mentor Info -->
    <div class="mentor-info">
      <span class="mentor-avatar">{{ getMentorIcon(challenge.mentor) }}</span>
      <span class="mentor-name">{{ challenge.mentor }}</span>
      <span class="mentor-role">{{ getMentorRole(challenge.mentor) }}</span>
    </div>

    <!-- Sacred Principles -->
    <div class="sacred-principles">
      <span class="principles-label">Sacred Principles:</span>
      <div class="principles-tags">
        <span 
          v-for="principle in challenge.sacredPrinciples" 
          :key="principle"
          class="principle-tag"
        >
          {{ principle }}
        </span>
      </div>
    </div>

    <!-- Challenge Stats -->
    <div class="challenge-stats">
      <div class="stat">
        <span class="stat-icon">⏱️</span>
        <span class="stat-value">{{ challenge.estimatedTime }}</span>
      </div>
      <div class="stat">
        <span class="stat-icon">⭐</span>
        <span class="stat-value">{{ challenge.divineRewards.xp }} XP</span>
      </div>
      <div class="stat">
        <span class="stat-icon">📁</span>
        <span class="stat-value">{{ challenge.files.length }} files</span>
      </div>
    </div>

    <!-- Prerequisites (if any) -->
    <div v-if="challenge.prerequisites && challenge.prerequisites.length > 0" class="prerequisites">
      <span class="prerequisites-label">Prerequisites:</span>
      <div class="prerequisites-list">
        <span 
          v-for="prereq in challenge.prerequisites" 
          :key="prereq"
          :class="['prerequisite-tag', { 'completed': isPrerequisiteCompleted(prereq) }]"
        >
          {{ getPrerequisiteTitle(prereq) }}
          <span class="prerequisite-status">
            {{ isPrerequisiteCompleted(prereq) ? '✅' : '🔒' }}
          </span>
        </span>
      </div>
    </div>

    <!-- Learning Objectives Preview -->
    <div class="learning-objectives">
      <span class="objectives-label">You'll learn:</span>
      <ul class="objectives-list">
        <li v-for="objective in challenge.learningObjectives.slice(0, 2)" :key="objective">
          {{ objective }}
        </li>
        <li v-if="challenge.learningObjectives.length > 2" class="more-objectives">
          +{{ challenge.learningObjectives.length - 2 }} more...
        </li>
      </ul>
    </div>

    <!-- Divine Rewards Preview -->
    <div class="divine-rewards">
      <span class="rewards-label">Divine Rewards:</span>
      <div class="rewards-preview">
        <div class="xp-reward">
          <span class="reward-icon">✨</span>
          <span class="reward-text">{{ challenge.divineRewards.xp }} Sacred XP</span>
        </div>
        <div v-if="challenge.divineRewards.sacredInsights.length > 0" class="insights-reward">
          <span class="reward-icon">🧠</span>
          <span class="reward-text">{{ challenge.divineRewards.sacredInsights.length }} Sacred Insights</span>
        </div>
        <div v-if="challenge.divineRewards.unlocks" class="unlocks-reward">
          <span class="reward-icon">🔓</span>
          <span class="reward-text">Unlocks new challenges</span>
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="challenge-actions">
      <button 
        v-if="!isLocked"
        @click="$emit('start-challenge', challenge.id)"
        :class="['start-btn', { 'recommended': isRecommended }]"
      >
        <span class="btn-icon">🚀</span>
        {{ isRecommended ? 'Start Recommended' : 'Start Challenge' }}
      </button>
      
      <button 
        v-else
        class="locked-btn"
        disabled
      >
        <span class="btn-icon">🔒</span>
        Prerequisites Required
      </button>
      
      <button 
        @click="$emit('view-details', challenge)"
        class="details-btn"
      >
        <span class="btn-icon">👁️</span>
        View Details
      </button>
    </div>

    <!-- Recommended Badge -->
    <div v-if="isRecommended" class="recommended-badge">
      <span class="badge-icon">🎯</span>
      <span class="badge-text">Recommended</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { SacredChallenge, StudentProgress, SacredDifficulty, SacredMentor, ATCGClassification } from '@/utils/sacredAcademy/challenges'

interface Props {
  challenge: SacredChallenge
  studentProgress?: StudentProgress
  isRecommended?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  isRecommended: false
})

const emit = defineEmits<{
  'start-challenge': [challengeId: string]
  'view-details': [challenge: SacredChallenge]
}>()

// Computed properties
const isLocked = computed(() => {
  if (!props.challenge.prerequisites || !props.studentProgress) return false
  
  return !props.challenge.prerequisites.every(prereq => 
    props.studentProgress!.completedChallenges.includes(prereq)
  )
})

// Helper methods
const getDifficultyIcon = (difficulty: SacredDifficulty): string => {
  const icons = {
    'bee.larva': '🐛',
    'bee.pupa': '🛡️', 
    'bee.adult': '🐝',
    'bee.sacred': '👑'
  }
  return icons[difficulty]
}

const getATCGIcon = (classification: ATCGClassification): string => {
  const icons = {
    'A': '🏗️',
    'T': '⚡',
    'C': '🔗',
    'G': '🌟'
  }
  return icons[classification]
}

const getMentorIcon = (mentor: SacredMentor): string => {
  const icons = {
    'bee.jules': '🔧',
    'bee.chronicler': '📜',
    'bee.sage': '🧙'
  }
  return icons[mentor]
}

const getMentorRole = (mentor: SacredMentor): string => {
  const roles = {
    'bee.jules': 'Technical Guide',
    'bee.chronicler': 'Sacred Keeper',
    'bee.sage': 'Wise Synthesizer'
  }
  return roles[mentor]
}

const getIssueUrl = (issueNumber: number): string => {
  return `https://github.com/zaebee/chat/issues/${issueNumber}`
}

const isPrerequisiteCompleted = (prereqId: string): boolean => {
  return props.studentProgress?.completedChallenges.includes(prereqId) || false
}

const getPrerequisiteTitle = (prereqId: string): string => {
  // In a real implementation, this would look up the challenge title
  return prereqId.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
}
</script>

<style scoped>
.challenge-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 1.5rem;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.challenge-card:hover {
  border-color: #667eea;
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
  transform: translateY(-4px);
}

.challenge-card.recommended {
  border-color: #f59e0b;
  background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
}

.challenge-card.locked {
  opacity: 0.6;
  background: #f8fafc;
}

.challenge-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.challenge-meta {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.difficulty-badge, .atcg-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.difficulty-badge {
  background: #e0e7ff;
  color: #3730a3;
}

.difficulty-bee-larva .difficulty-badge {
  background: #dcfce7;
  color: #166534;
}

.difficulty-bee-pupa .difficulty-badge {
  background: #fef3c7;
  color: #92400e;
}

.difficulty-bee-adult .difficulty-badge {
  background: #dbeafe;
  color: #1e40af;
}

.difficulty-bee-sacred .difficulty-badge {
  background: #fae8ff;
  color: #86198f;
}

.atcg-badge {
  background: #f1f5f9;
  color: #475569;
}

.issue-badge {
  padding: 0.25rem 0.5rem;
  background: #374151;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  transition: background 0.2s ease;
}

.issue-badge:hover {
  background: #111827;
}

.challenge-title {
  margin: 0 0 0.75rem 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  line-height: 1.3;
}

.challenge-description {
  margin: 0 0 1rem 0;
  color: #64748b;
  font-size: 0.875rem;
  line-height: 1.5;
}

.mentor-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  padding: 0.75rem;
  background: #f8fafc;
  border-radius: 8px;
}

.mentor-avatar {
  font-size: 1.25rem;
}

.mentor-name {
  font-weight: 600;
  color: #374151;
}

.mentor-role {
  font-size: 0.75rem;
  color: #6b7280;
}

.sacred-principles {
  margin-bottom: 1rem;
}

.principles-label {
  display: block;
  font-size: 0.75rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.principles-tags {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.principle-tag {
  padding: 0.25rem 0.5rem;
  background: #e0e7ff;
  color: #3730a3;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 500;
}

.challenge-stats {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  padding: 0.75rem;
  background: #f8fafc;
  border-radius: 8px;
}

.stat {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.75rem;
  color: #64748b;
}

.stat-icon {
  font-size: 1rem;
}

.stat-value {
  font-weight: 600;
  color: #374151;
}

.prerequisites {
  margin-bottom: 1rem;
}

.prerequisites-label {
  display: block;
  font-size: 0.75rem;
  font-weight: 600;
  color: #dc2626;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.prerequisites-list {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.prerequisite-tag {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.5rem;
  background: #fef2f2;
  color: #dc2626;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 500;
}

.prerequisite-tag.completed {
  background: #dcfce7;
  color: #166534;
}

.learning-objectives {
  margin-bottom: 1rem;
}

.objectives-label {
  display: block;
  font-size: 0.75rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.objectives-list {
  margin: 0;
  padding-left: 1rem;
  font-size: 0.875rem;
  color: #64748b;
}

.objectives-list li {
  margin-bottom: 0.25rem;
}

.more-objectives {
  font-style: italic;
  color: #9ca3af;
}

.divine-rewards {
  margin-bottom: 1.5rem;
}

.rewards-label {
  display: block;
  font-size: 0.75rem;
  font-weight: 600;
  color: #7c3aed;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.rewards-preview {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.xp-reward, .insights-reward, .unlocks-reward {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
}

.reward-icon {
  font-size: 1rem;
}

.reward-text {
  color: #64748b;
  font-weight: 500;
}

.challenge-actions {
  display: flex;
  gap: 0.75rem;
}

.start-btn, .locked-btn, .details-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.start-btn {
  background: #667eea;
  color: white;
}

.start-btn:hover {
  background: #5a67d8;
  transform: translateY(-1px);
}

.start-btn.recommended {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.start-btn.recommended:hover {
  background: linear-gradient(135deg, #d97706 0%, #b45309 100%);
}

.locked-btn {
  background: #f1f5f9;
  color: #64748b;
  cursor: not-allowed;
}

.details-btn {
  background: #f8fafc;
  color: #64748b;
  border: 1px solid #e2e8f0;
}

.details-btn:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
}

.recommended-badge {
  position: absolute;
  top: -1px;
  right: -1px;
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0 16px 0 16px;
  font-size: 0.75rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.badge-icon {
  font-size: 1rem;
}

@media (max-width: 768px) {
  .challenge-card {
    padding: 1rem;
  }
  
  .challenge-header {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .challenge-stats {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .challenge-actions {
    flex-direction: column;
  }
}
</style>