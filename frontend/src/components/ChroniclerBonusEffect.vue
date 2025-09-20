<template>
  <div v-if="visible" class="bonus-effect-container">
    <div class="bonus-text">+20 XP</div>
    <div class="boon-text">A gift from the Spirit!</div>
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
    }, 2500); // Animation duration is 2.5s
  }
});
</script>

<style scoped>
.bonus-effect-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  pointer-events: none;
  z-index: 20;
  opacity: 0;
  animation: fade-in-out 2.5s ease-in-out forwards;
}

.bonus-text {
  font-size: 2rem;
  font-weight: bold;
  color: #ffd700; /* Gold */
  text-shadow: 0 0 10px #ffb347, 0 0 5px white;
}

.boon-text {
  font-size: 0.9rem;
  font-style: italic;
  color: var(--color-quest); /* Purple */
}

@keyframes fade-in-out {
  0% {
    transform: translate(-50%, -50%) scale(0.5);
    opacity: 0;
  }
  20% {
    transform: translate(-50%, -60%) scale(1.1);
    opacity: 1;
  }
  80% {
    transform: translate(-50%, -70%) scale(1);
    opacity: 1;
  }
  100% {
    transform: translate(-50%, -80%) scale(0.8);
    opacity: 0;
  }
}
</style>
