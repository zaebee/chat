<template>
  <div v-if="visible" class="ceremony-overlay">
    <div class="ceremony-container">
      <div class="sparkle" v-for="i in 30" :key="i" :style="sparkleStyle(i)"></div>
      <div class="glow"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';

const props = defineProps<{
  start: boolean;
}>();

const visible = ref(false);

watch(() => props.start, (newVal) => {
  if (newVal) {
    visible.value = true;
    setTimeout(() => {
      visible.value = false;
    }, 1500); // Animation duration is 1.5s
  }
});

const sparkleStyle = (i: number) => {
  const angle = (i / 30) * 360;
  return {
    transform: `rotate(${angle}deg) translateY(50px)`,
    animationDelay: `${Math.random() * 0.5}s`,
  };
};
</script>

<style scoped>
.ceremony-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  pointer-events: none;
  z-index: 10;
  border-radius: 12px; /* Match the card */
  overflow: hidden;
}

.ceremony-container {
  position: relative;
  width: 100px;
  height: 100px;
}

.glow {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background-color: rgba(255, 215, 0, 0.8); /* Gold */
  animation: glow-anim 1.5s ease-out forwards;
}

.sparkle {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 4px;
  height: 10px;
  background-color: #ffd700;
  border-radius: 2px;
  opacity: 0;
  animation: sparkle-anim 1.5s ease-out forwards;
}

@keyframes glow-anim {
  0% {
    transform: translate(-50%, -50%) scale(0);
    opacity: 0.3;
  }
  50% {
    opacity: 0.8;
  }
  100% {
    transform: translate(-50%, -50%) scale(2.5);
    opacity: 0;
  }
}

@keyframes sparkle-anim {
  0% {
    transform: translate(-50%, -50%) scale(0);
    opacity: 0;
  }
  50% {
    transform: translate(-50%, -50%) scale(1.5);
    opacity: 1;
  }
  100% {
    transform: translate(-50%, -50%) scale(0);
    opacity: 0;
  }
}
</style>
