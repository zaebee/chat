<script setup lang="ts">
import { useChatStore } from '@/stores/chat'
import { storeToRefs } from 'pinia'
import { computed } from 'vue'
import HexaLevel from '@/components/HexaLevel.vue'

const chatStore = useChatStore()
const { level, solvedChallenges, organellas } = storeToRefs(chatStore)

// Define the mapping of levels to challenge IDs (example, needs to be expanded)
// For now, we'll just map the first few levels to our existing challenges
const levelChallengeMap: { [key: number]: string[] } = {
  1: ['1', '2'], // Level 1: Add, Multiply
  2: ['3'], // Level 2: Check if Even
  3: ['4'], // Level 3: Draw a Square
  // ... more levels and challenges
}

const organellasByLevel = computed(() => {
  const result: { [key: number]: any[] } = {}
  for (const organella of organellas.value) {
    if (!result[organella.level]) {
      result[organella.level] = []
    }
    result[organella.level].push(organella)
  }
  return result
})

function getHexClass(hexLevel: number) {
  let classes = 'hex'
  if (hexLevel === level.value) {
    classes += ' current-level'
  } else if (hexLevel < level.value) {
    // Check if all challenges for this level are solved
    const challengesForLevel = levelChallengeMap[hexLevel] || []
    const allSolved = challengesForLevel.every((id) => solvedChallenges.value.includes(id))
    if (allSolved) {
      classes += ' solved-level'
    } else {
      classes += ' past-level'
    }
  } else {
    classes += ' locked-level'
  }
  return classes
}

function isLevelSolved(hexLevel: number) {
  const challengesForLevel = levelChallengeMap[hexLevel] || []
  return challengesForLevel.every((id) => solvedChallenges.value.includes(id))
}
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
      </svg>
    </div>
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
