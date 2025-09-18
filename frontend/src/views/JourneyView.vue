<script setup lang="ts">
import { useChatStore } from '@/stores/chat'
import { storeToRefs } from 'pinia'

const chatStore = useChatStore()
const { level, solvedChallenges } = storeToRefs(chatStore)

// Define the mapping of levels to challenge IDs (example, needs to be expanded)
// For now, we'll just map the first few levels to our existing challenges
const levelChallengeMap: { [key: number]: string[] } = {
  1: ['1', '2'], // Level 1: Add, Multiply
  2: ['3'], // Level 2: Check if Even
  3: ['4'], // Level 3: Draw a Square
  // ... more levels and challenges
}

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
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 700" width="800" height="700" font-family="monospace">
        <title>Hive of Seven Levels — Hex Honeyprint</title>

        <!-- center -->
        <polygon :class="getHexClass(7)" points="310,350 355,272 445,272 490,350 445,428 355,428"/>
        <text x="400" y="335" class="label title">Level 7: Intent</text>
        <text x="400" y="360" class="label subtitle">Дух улья • смысл • цель</text>

        <!-- up -->
        <polygon :class="getHexClass(6)" points="310,200 355,122 445,122 490,200 445,278 355,278"/>
        <text x="400" y="187" class="label title">Level 6: Physics</text>
        <text x="400" y="210" class="label cap">OS • Network • CPU</text>

        <!-- up-right -->
        <polygon :class="getHexClass(5)" points="430,275 475,197 565,197 610,275 565,353 475,353"/>
        <text x="520" y="262" class="label title">Level 5: Implementation</text>
        <text x="520" y="285" class="label cap">Codeons • tests • clarity</text>

        <!-- down-right -->
        <polygon :class="getHexClass(4)" points="430,425 475,347 565,347 610,425 565,503 475,503"/>
        <text x="520" y="412" class="label title">Level 4: ATCG</text>
        <text x="520" y="435" class="label cap">A • T • C • G primitives</text>

        <!-- down -->
        <polygon :class="getHexClass(3)" points="310,500 355,422 445,422 490,500 445,578 355,578"/>
        <text x="400" y="487" class="label title">Level 3: Codons</text>
        <text x="400" y="510" class="label cap">C→A→G • C→T→C • G→C→A→G</text>

        <!-- down-left -->
        <polygon :class="getHexClass(2)" points="190,425 235,347 325,347 370,425 325,503 235,503"/>
        <text x="280" y="412" class="label title">Level 2: Cell</text>
        <text x="280" y="435" class="label cap">Bounded Context / API wall</text>

        <!-- up-left -->
        <polygon :class="getHexClass(1)" points="190,275 235,197 325,197 370,275 325,353 235,353"/>
        <text x="280" y="262" class="label title">Level 1: Organism</text>
        <text x="280" y="285" class="label cap">All Hives • whole system</text>
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

.hex { fill:#f9e79f; stroke:#a87400; stroke-width:3; }
.center { fill:#f4d03f; stroke:#a87400; stroke-width:4; }
.label { font-size:16px; fill:#3b2f00; text-anchor:middle; dominant-baseline:middle; }
.title { font-weight:700; font-size:18px; }
.subtitle { font-size:14px; opacity:.9; }
.cap { font-size:13px; opacity:.85; }

/* New styles for journey progression */
.hex.current-level {
  fill: #4CAF50; /* Green for current level */
  stroke: #388E3C;
  stroke-width: 5;
}

.hex.solved-level {
  fill: #8BC34A; /* Lighter green for solved levels */
  stroke: #689F38;
  stroke-width: 3;
}

.hex.past-level {
  fill: #BDBDBD; /* Grey for past, unsolved levels */
  stroke: #757575;
}

.hex.locked-level {
  fill: #E0E0E0; /* Very light grey for future levels */
  stroke: #9E9E9E;
}
</style>
