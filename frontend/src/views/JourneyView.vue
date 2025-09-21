<script setup lang="ts">
import { useOrganellasStore, type Organella } from "@/stores/organellas";
import { useUserStore } from "@/stores/user";
import { storeToRefs } from "pinia";
import { computed, onMounted, ref } from "vue";
import HexaLevel from "@/components/HexaLevel.vue";
import QuestPanel from "@/components/QuestPanel.vue";
import type { Room } from "@/stores/game";

const organellasStore = useOrganellasStore();
const userStore = useUserStore();
const { organellas } = storeToRefs(organellasStore);
const { currentUser } = storeToRefs(userStore);

const isGenesisQuestVisible = ref(false);

// Mock room for QuestPanel
const genesisRoom: Room = {
  id: 'genesis',
  name: 'Genesis Chamber',
  description: 'The birthplace of new organellas',
  type: 'journey',
  created_by: 'system',
  created_at: new Date().toISOString(),
  is_archived: false,
  level: 1,
  unlocked: true,
  completed: false,
  organellas: [],
  quests: []
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
    if (!result[organella.level]) {
      result[organella.level] = [];
    }
    result[organella.level].push(organella);
  }
  return result;
});
</script>

<template>
  <div class="journey-view">
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
        />

        <HexaLevel
          :level="6"
          title="Level 6: Physics"
          subtitle="OS • Network • CPU"
          points="310,200 355,122 445,122 490,200 445,278 355,278"
          :x="400"
          :y="200"
          :organellas="organellasByLevel[6] || []"
        />

        <HexaLevel
          :level="5"
          title="Level 5: Implementation"
          subtitle="Codeons • tests • clarity"
          points="430,275 475,197 565,197 610,275 565,353 475,353"
          :x="520"
          :y="275"
          :organellas="organellasByLevel[5] || []"
        />

        <HexaLevel
          :level="4"
          title="Level 4: ATCG"
          subtitle="A • T • C • G primitives"
          points="430,425 475,347 565,347 610,425 565,503 475,503"
          :x="520"
          :y="425"
          :organellas="organellasByLevel[4] || []"
        />

        <HexaLevel
          :level="3"
          title="Level 3: Codons"
          subtitle="C→A→G • C→T→C • G→C→A→G"
          points="310,500 355,422 445,422 490,500 445,578 355,578"
          :x="400"
          :y="500"
          :organellas="organellasByLevel[3] || []"
        />

        <HexaLevel
          :level="2"
          title="Level 2: Cell"
          subtitle="Bounded Context / API wall"
          points="190,425 235,347 325,347 370,425 325,503 235,503"
          :x="280"
          :y="425"
          :organellas="organellasByLevel[2] || []"
        />

        <HexaLevel
          :level="1"
          title="Level 1: Organism"
          subtitle="All Hives • whole system"
          points="190,275 235,197 325,197 370,275 325,353 235,353"
          :x="280"
          :y="275"
          :organellas="organellasByLevel[1] || []"
        />

        <!-- Quest marker: GENESIS:x:y -->
        <g class="pulse" transform="translate(500,220)" @click="isGenesisQuestVisible = !isGenesisQuestVisible">
          <circle r="18" fill="var(--color-quest)" />
          <text x="0" y="4" font-size="20" text-anchor="middle" fill="#fff">?</text>
        </g>
      </svg>
    </div>
    <QuestPanel v-if="isGenesisQuestVisible" :room="genesisRoom" @close="isGenesisQuestVisible = false" />
  </div>
</template>

<style scoped>
.journey-view {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
  overflow: auto;
  background-color: var(--color-background);
}

.journey-map {
  max-width: 100%;
  max-height: 100%;
  display: block; /* Remove extra space below SVG */
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
