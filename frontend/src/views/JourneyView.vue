<script setup lang="ts">
import { useOrganellasStore, type Organella } from "@/stores/organellas";
import { useUserStore } from "@/stores/user";
import { storeToRefs } from "pinia";
import { computed, onMounted, ref } from "vue";
import HexaLevel from "@/components/HexaLevel.vue";
import QuestPanel from "@/components/QuestPanel.vue";
import SimpleProjectGraph from "@/components/SimpleProjectGraph.vue";
import type { Room } from "@/stores/game";

const organellasStore = useOrganellasStore();
const userStore = useUserStore();
const { organellas } = storeToRefs(organellasStore);
const { currentUser } = storeToRefs(userStore);

const isGenesisQuestVisible = ref(false);
const isProjectDetailExpanded = ref(false);
const selectedProjectLevel = ref<number | null>(null);

// Mock room for QuestPanel
const genesisRoom: Room = {
  id: "genesis",
  name: "Genesis Chamber",
  description: "The birthplace of new organellas",
  type: "journey",
  created_by: "system",
  created_at: new Date().toISOString(),
  is_archived: false,
  level: 1,
  unlocked: true,
  completed: false,
  organellas: [],
  quests: [],
};

onMounted(() => {
  // Fetch organellas for the current user
  if (currentUser.value?.id) {
    organellasStore.fetchOrganellas(currentUser.value.id);
  }
});

const organellasByLevel = computed(() => {
  const result: { [key: number]: Organella[] } = {};
  // Add defensive check to ensure organellas.value is an array
  const organellaArray = organellas.value || [];
  for (const organella of organellaArray) {
    // Additional defensive check for organella validity
    if (organella && organella.id && typeof organella.level === 'number') {
      if (!result[organella.level]) {
        result[organella.level] = [];
      }
      result[organella.level].push(organella);
    }
  }
  return result;
});

// Project detail functions
const toggleProjectDetail = (level: number) => {
  if (isProjectDetailExpanded.value && selectedProjectLevel.value === level) {
    // Clicking the same level closes the detail
    isProjectDetailExpanded.value = false;
    selectedProjectLevel.value = null;
  } else {
    // Clicking a different level or expanding for the first time
    selectedProjectLevel.value = level;
    isProjectDetailExpanded.value = true;
  }
};

const getProjectIdForLevel = (level: number): string => {
  const projectMap: { [key: number]: string } = {
    7: "intent-level",
    6: "physics-level",
    5: "implementation-level",
    4: "atcg-primitives",
    3: "codons-level",
    2: "cell-level",
    1: "organism-level",
    0: "master-architecture",
  };
  return projectMap[level] || "unknown-project";
};

const getLevelTitle = (level: number): string => {
  const titleMap: { [key: number]: string } = {
    7: "Intent (Дух улья • смысл • цель)",
    6: "Physics (OS • Network • CPU)",
    5: "Implementation (Codeons • tests • clarity)",
    4: "ATCG (A • T • C • G primitives)",
    3: "Codons (C→A→G • C→T→C • G→C→A→G)",
    2: "Cell (Bounded Context / API wall)",
    1: "Organism (All Hives • whole system)",
  };
  return titleMap[level] || "Unknown Level";
};
</script>

<template>
  <div class="journey-view">
    <!-- 4D Project Analysis Controls -->
    <div class="project-controls">
      <h2 class="controls-title">🧬 Sacred Architecture Analysis</h2>
      <p class="controls-subtitle">4D→3D Dimensional Bridge Navigation</p>
      <div class="level-buttons">
        <button
          v-for="level in [7, 6, 5, 4, 3, 2, 1]"
          :key="level"
          @click="toggleProjectDetail(level)"
          :class="['level-btn', `level-${level}`]"
        >
          🎯 Level {{ level }} Detail
        </button>
      </div>
      <button class="master-analysis-btn" @click="toggleProjectDetail(0)">
        🧬 Master Architecture Analysis
      </button>
    </div>

    <div class="journey-map">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 800 700"
        width="800"
        height="700"
        font-family="monospace"
      >
        <title>Hive of Seven Levels — Hex Honeyprint</title>

        <HexaLevel
          :level="7"
          title="Level 7: Intent"
          subtitle="Дух улья • смысл • цель"
          points="310,350 355,272 445,272 490,350 445,428 355,428"
          :x="400"
          :y="350"
          :organellas="organellasByLevel[7] || []"
          @click="toggleProjectDetail(7)"
        />

        <HexaLevel
          :level="6"
          title="Level 6: Physics"
          subtitle="OS • Network • CPU"
          points="310,200 355,122 445,122 490,200 445,278 355,278"
          :x="400"
          :y="200"
          :organellas="organellasByLevel[6] || []"
          @click="toggleProjectDetail(6)"
        />

        <HexaLevel
          :level="5"
          title="Level 5: Implementation"
          subtitle="Codeons • tests • clarity"
          points="430,275 475,197 565,197 610,275 565,353 475,353"
          :x="520"
          :y="275"
          :organellas="organellasByLevel[5] || []"
          @click="toggleProjectDetail(5)"
        />

        <HexaLevel
          :level="4"
          title="Level 4: ATCG"
          subtitle="A • T • C • G primitives"
          points="430,425 475,347 565,347 610,425 565,503 475,503"
          :x="520"
          :y="425"
          :organellas="organellasByLevel[4] || []"
          @click="toggleProjectDetail(4)"
        />

        <HexaLevel
          :level="3"
          title="Level 3: Codons"
          subtitle="C→A→G • C→T→C • G→C→A→G"
          points="310,500 355,422 445,422 490,500 445,578 355,578"
          :x="400"
          :y="500"
          :organellas="organellasByLevel[3] || []"
          @click="toggleProjectDetail(3)"
        />

        <HexaLevel
          :level="2"
          title="Level 2: Cell"
          subtitle="Bounded Context / API wall"
          points="190,425 235,347 325,347 370,425 325,503 235,503"
          :x="280"
          :y="425"
          :organellas="organellasByLevel[2] || []"
          @click="toggleProjectDetail(2)"
        />

        <HexaLevel
          :level="1"
          title="Level 1: Organism"
          subtitle="All Hives • whole system"
          points="190,275 235,197 325,197 370,275 325,353 235,353"
          :x="280"
          :y="275"
          :organellas="organellasByLevel[1] || []"
          @click="toggleProjectDetail(1)"
        />

        <!-- Quest marker: GENESIS:x:y -->
        <g
          class="pulse"
          transform="translate(500,220)"
          @click="isGenesisQuestVisible = !isGenesisQuestVisible"
        >
          <circle r="18" fill="var(--color-quest)" />
          <text x="0" y="4" font-size="20" text-anchor="middle" fill="#fff">
            ?
          </text>
        </g>
      </svg>
    </div>

    <!-- Project Detail Graph Inline Section -->
    <div v-if="isProjectDetailExpanded" class="project-detail-section">
      <div class="project-detail-header">
        <h2 v-if="selectedProjectLevel === 0">
          🧬 Master Architecture Analysis
        </h2>
        <h2 v-else>
          🎯 Level {{ selectedProjectLevel }} -
          {{ getLevelTitle(selectedProjectLevel) }}
        </h2>
        <button
          class="collapse-btn"
          @click="isProjectDetailExpanded = false"
          title="Collapse"
        >
          ▲
        </button>
      </div>
      <div class="project-detail-content">
        <SimpleProjectGraph
          :project-id="getProjectIdForLevel(selectedProjectLevel || 0)"
          :show-metrics="true"
          :enable-interaction="true"
        />
      </div>
    </div>

    <QuestPanel
      v-if="isGenesisQuestVisible"
      :room="genesisRoom"
      @close="isGenesisQuestVisible = false"
    />
  </div>
</template>

<style scoped>
.journey-view {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  overflow: auto;
  background-color: var(--color-background);
  padding: 1rem;
  gap: 1.5rem;
}

.journey-map {
  max-width: 100%;
  max-height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Project Controls Styles */
.project-controls {
  background: linear-gradient(
    135deg,
    rgba(139, 92, 246, 0.05),
    rgba(255, 255, 255, 0.95)
  );
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 0.75rem;
  padding: 1.5rem;
  text-align: center;
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.1);
}

.controls-title {
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: #8b5cf6;
}

.controls-subtitle {
  margin: 0 0 1.5rem 0;
  font-size: 0.9rem;
  color: var(--color-text-secondary, #6b7280);
  font-style: italic;
}

.level-buttons {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  justify-content: center;
}

.level-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
  color: white;
  min-width: 120px;
}

.level-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* Level-specific colors matching Sacred ATCG */
.level-7 {
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
} /* Intent - Purple */
.level-6 {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
} /* Physics - Blue */
.level-5 {
  background: linear-gradient(135deg, #10b981, #059669);
} /* Implementation - Green */
.level-4 {
  background: linear-gradient(135deg, #f59e0b, #d97706);
} /* ATCG - Orange */
.level-3 {
  background: linear-gradient(135deg, #ef4444, #dc2626);
} /* Codons - Red */
.level-2 {
  background: linear-gradient(135deg, #06b6d4, #0891b2);
} /* Cell - Cyan */
.level-1 {
  background: linear-gradient(135deg, #84cc16, #65a30d);
} /* Organism - Lime */

.master-analysis-btn {
  padding: 0.75rem 2rem;
  background: linear-gradient(135deg, #ffd700, #fbbf24);
  border: none;
  border-radius: 0.5rem;
  color: #92400e;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(255, 215, 0, 0.3);
}

.master-analysis-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(255, 215, 0, 0.4);
}

/* Project Detail Inline Section Styles */
.project-detail-section {
  margin: 2rem 0;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  border: 2px solid #e5e7eb;
  overflow: hidden;
  animation: expandIn 0.3s ease-out;
}

@keyframes expandIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.project-detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  background: linear-gradient(
    135deg,
    rgba(139, 92, 246, 0.05),
    rgba(255, 255, 255, 0.95)
  );
}

.project-detail-header h2 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 700;
  color: #8b5cf6;
}

.collapse-btn {
  padding: 0.5rem;
  background: #6b7280;
  color: white;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: bold;
  transition: all 0.2s ease;
  width: 2.5rem;
  height: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.collapse-btn:hover {
  background: #4b5563;
  transform: translateY(-1px);
}

.project-detail-content {
  height: 700px;
  overflow: auto;
  padding: 0;
}

.hex {
  fill: #f9e79f;
  stroke: #a87400;
  stroke-width: 3;
}
.center {
  fill: #f4d03f;
  stroke: #a87400;
  stroke-width: 4;
}
.label {
  font-size: 16px;
  fill: #3b2f00;
  text-anchor: middle;
  dominant-baseline: middle;
}
.title {
  font-weight: 700;
  font-size: 18px;
}
.subtitle {
  font-size: 14px;
  opacity: 0.9;
}
.cap {
  font-size: 13px;
  opacity: 0.85;
}

/* New styles for journey progression */
.hex.current-level {
  fill: #4caf50; /* Green for current level */
  stroke: #388e3c;
  stroke-width: 5;
}

.hex.solved-level {
  fill: #8bc34a; /* Lighter green for solved levels */
  stroke: #689f38;
  stroke-width: 3;
}

.hex.past-level {
  fill: #bdbdbd; /* Grey for past, unsolved levels */
  stroke: #757575;
}

.hex.locked-level {
  fill: #e0e0e0; /* Very light grey for future levels */
  stroke: #9e9e9e;
}
</style>
