<template>
  <div class="simple-project-graph">
    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner">⚡</div>
      <p>Loading project analysis...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <div class="error-icon">❌</div>
      <p>{{ error }}</p>
      <button @click="refreshData" class="retry-btn">🔄 Retry</button>
    </div>

    <!-- Main Content -->
    <div v-else class="graph-content">
      <!-- Project Overview -->
      <div class="project-overview">
        <h3>📊 Project: {{ projectData?.projectId || projectId }}</h3>
        <div class="overview-stats">
          <div class="stat-item">
            <span class="stat-label">Components:</span>
            <span class="stat-value">{{ projectData?.sacredMetrics?.total_components || 0 }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Quality (φ):</span>
            <span class="stat-value">{{ (projectData?.sacredMetrics?.phi || 0).toFixed(2) }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Complexity (τ):</span>
            <span class="stat-value">{{ (projectData?.sacredMetrics?.tau || 0).toFixed(2) }}</span>
          </div>
        </div>
      </div>

      <!-- ATCG Distribution -->
      <div class="atcg-distribution">
        <h4>🧬 ATCG Component Distribution</h4>
        <div class="atcg-bars">
          <div class="atcg-bar" v-if="distribution">
            <div class="bar-group">
              <div class="bar-label">A (Aggregates)</div>
              <div class="bar-container">
                <div
                  class="bar-fill atcg-a"
                  :style="{ width: (distribution.aggregates * 100) + '%' }"
                ></div>
              </div>
              <div class="bar-value">{{ (distribution.aggregates * 100).toFixed(0) }}%</div>
            </div>

            <div class="bar-group">
              <div class="bar-label">T (Transformations)</div>
              <div class="bar-container">
                <div
                  class="bar-fill atcg-t"
                  :style="{ width: (distribution.transformations * 100) + '%' }"
                ></div>
              </div>
              <div class="bar-value">{{ (distribution.transformations * 100).toFixed(0) }}%</div>
            </div>

            <div class="bar-group">
              <div class="bar-label">C (Connectors)</div>
              <div class="bar-container">
                <div
                  class="bar-fill atcg-c"
                  :style="{ width: (distribution.connectors * 100) + '%' }"
                ></div>
              </div>
              <div class="bar-value">{{ (distribution.connectors * 100).toFixed(0) }}%</div>
            </div>

            <div class="bar-group">
              <div class="bar-label">G (Genesis)</div>
              <div class="bar-container">
                <div
                  class="bar-fill atcg-g"
                  :style="{ width: (distribution.genesis * 100) + '%' }"
                ></div>
              </div>
              <div class="bar-value">{{ (distribution.genesis * 100).toFixed(0) }}%</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Component List -->
      <div class="component-list" v-if="projectData?.nodes?.length">
        <h4>🔗 Component Network</h4>
        <div class="component-grid">
          <div
            v-for="node in displayedNodes"
            :key="node.id"
            class="component-card"
            :class="'atcg-' + node.atcgType.toLowerCase()"
          >
            <div class="component-header">
              <span class="component-type">{{ node.atcgType }}</span>
              <span class="component-name">{{ node.name }}</span>
            </div>
            <div class="component-details">
              <div class="detail-row">
                <span>Components: {{ node.componentCount || 1 }}</span>
              </div>
              <div class="detail-row">
                <span>Complexity: {{ (node.complexity || 0).toFixed(1) }}</span>
              </div>
              <div class="detail-row" v-if="node.file_path">
                <span class="file-path">{{ node.file_path }}</span>
              </div>
            </div>
          </div>
        </div>

        <div v-if="hasMoreNodes" class="load-more">
          <button @click="showMoreNodes" class="load-more-btn">
            📂 Show More Components ({{ remainingNodeCount }} remaining)
          </button>
        </div>
      </div>

      <!-- No Data State -->
      <div v-else class="no-data">
        <div class="no-data-icon">📊</div>
        <p>No component data available for this project.</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { projectAnalysisAPI, type ProjectAnalysisResponse } from '@/services/projectAnalysisApi'

// Props
interface Props {
  projectId?: string
  showMetrics?: boolean
  enableInteraction?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  projectId: 'master-architecture',
  showMetrics: true,
  enableInteraction: true
})

// State
const loading = ref(true)
const error = ref('')
const projectData = ref<ProjectAnalysisResponse | null>(null)
const nodesToShow = ref(12) // Show 12 components initially

// Computed
const distribution = computed(() => {
  return projectData.value?.sacredMetrics?.componentDistribution
})

const displayedNodes = computed(() => {
  return projectData.value?.nodes?.slice(0, nodesToShow.value) || []
})

const hasMoreNodes = computed(() => {
  const totalNodes = projectData.value?.nodes?.length || 0
  return totalNodes > nodesToShow.value
})

const remainingNodeCount = computed(() => {
  const totalNodes = projectData.value?.nodes?.length || 0
  return Math.max(0, totalNodes - nodesToShow.value)
})

// Methods
const refreshData = async () => {
  loading.value = true
  error.value = ''

  try {
    const data = await projectAnalysisAPI.getProjectAnalysis(props.projectId)
    projectData.value = data
  } catch (err: any) {
    error.value = err.message || 'Failed to load project data'
    console.error('Project data loading error:', err)
  } finally {
    loading.value = false
  }
}

const showMoreNodes = () => {
  nodesToShow.value += 12
}

// Lifecycle
onMounted(() => {
  refreshData()
})
</script>

<style scoped>
.simple-project-graph {
  max-width: 100%;
  margin: 0 auto;
}

/* Loading & Error States */
.loading-state, .error-state, .no-data {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  text-align: center;
}

.loading-spinner {
  font-size: 3rem;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.error-icon, .no-data-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.retry-btn {
  padding: 0.5rem 1rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  margin-top: 1rem;
}

.retry-btn:hover {
  background: #2563eb;
}

/* Project Overview */
.project-overview {
  background: #f8fafc;
  border-radius: 0.75rem;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  border: 1px solid #e2e8f0;
}

.project-overview h3 {
  margin: 0 0 1rem 0;
  color: #1e293b;
}

.overview-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: white;
  border-radius: 0.5rem;
  border: 1px solid #e2e8f0;
}

.stat-label {
  font-weight: 500;
  color: #64748b;
}

.stat-value {
  font-weight: 700;
  color: #1e293b;
  font-family: monospace;
}

/* ATCG Distribution */
.atcg-distribution {
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  border: 1px solid #e2e8f0;
}

.atcg-distribution h4 {
  margin: 0 0 1rem 0;
  color: #1e293b;
}

.bar-group {
  display: grid;
  grid-template-columns: 140px 1fr 60px;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.bar-label {
  font-weight: 500;
  color: #475569;
  font-size: 0.9rem;
}

.bar-container {
  background: #f1f5f9;
  border-radius: 0.25rem;
  height: 1.5rem;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  border-radius: 0.25rem;
  transition: width 0.3s ease;
}

.bar-value {
  font-weight: 600;
  font-family: monospace;
  color: #1e293b;
  text-align: right;
}

/* ATCG Colors */
.atcg-a, .atcg-a .bar-fill { background: #ef4444; } /* Red - Aggregates */
.atcg-t, .atcg-t .bar-fill { background: #3b82f6; } /* Blue - Transformations */
.atcg-c, .atcg-c .bar-fill { background: #f59e0b; } /* Orange - Connectors */
.atcg-g, .atcg-g .bar-fill { background: #10b981; } /* Green - Genesis */

/* Component List */
.component-list {
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  border: 1px solid #e2e8f0;
}

.component-list h4 {
  margin: 0 0 1rem 0;
  color: #1e293b;
}

.component-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.component-card {
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  padding: 1rem;
  background: #fafafa;
  border-left: 4px solid #64748b;
}

.component-card.atcg-a { border-left-color: #ef4444; }
.component-card.atcg-t { border-left-color: #3b82f6; }
.component-card.atcg-c { border-left-color: #f59e0b; }
.component-card.atcg-g { border-left-color: #10b981; }

.component-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.component-type {
  background: #64748b;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 600;
  min-width: 1.5rem;
  text-align: center;
}

.component-card.atcg-a .component-type { background: #ef4444; }
.component-card.atcg-t .component-type { background: #3b82f6; }
.component-card.atcg-c .component-type { background: #f59e0b; }
.component-card.atcg-g .component-type { background: #10b981; }

.component-name {
  font-weight: 600;
  color: #1e293b;
  flex: 1;
}

.component-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.detail-row {
  font-size: 0.85rem;
  color: #64748b;
}

.file-path {
  font-family: monospace;
  background: #f1f5f9;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
}

/* Load More */
.load-more {
  text-align: center;
  margin-top: 1rem;
}

.load-more-btn {
  padding: 0.75rem 1.5rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  cursor: pointer;
  color: #475569;
  font-weight: 500;
}

.load-more-btn:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
}

/* Responsive Design */
@media (max-width: 768px) {
  .overview-stats {
    grid-template-columns: 1fr;
  }

  .component-grid {
    grid-template-columns: 1fr;
  }

  .bar-group {
    grid-template-columns: 120px 1fr 50px;
    gap: 0.5rem;
  }
}
</style>