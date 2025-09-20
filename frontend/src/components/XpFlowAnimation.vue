<template>
  <div v-if="visible" class="xp-flow-container">
    <div v-for="i in particleCount" :key="i" class="xp-particle" :style="particleStyle(i)"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';

const props = defineProps<{
  start: boolean;
}>();

const visible = ref(false);
const particleCount = 15; // Number of XP particles

watch(() => props.start, (newVal) => {
  if (newVal) {
    visible.value = true;
    // Hide the animation container after it completes
    setTimeout(() => {
      visible.value = false;
    }, 2000); // Animation duration is 2s
  }
});

// Randomize particle animation delays and paths
const particleStyle = (i: number) => ({
  animationDelay: `${(i * 0.1).toFixed(2)}s`,
  left: `${Math.random() * 100}%`,
});
</script>

<style scoped>
.xp-flow-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none; /* Allow clicks to pass through */
  z-index: 2000; /* Appear on top of everything */
  overflow: hidden;
}

.xp-particle {
  position: absolute;
  bottom: 10%; /* Start from the bottom area */
  width: 10px;
  height: 10px;
  background-color: #ffd700; /* Golden XP color */
  border-radius: 50%;
  opacity: 0;
  animation: flow 2s ease-out forwards;
  box-shadow: 0 0 5px #ffd700, 0 0 10px #ffb347;
}

@keyframes flow {
  0% {
    transform: translateY(0) scale(1);
    opacity: 1;
  }
  100% {
    transform: translateY(-80vh) scale(0.5); /* Flow upwards towards top of screen */
    opacity: 0;
  }
}
</style>
