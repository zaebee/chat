<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{
  bodyColor?: string;
  wingColor?: string;
  eyeColor?: string;
  stingerColor?: string;
  swordColor?: string;
  size?: number; // Scale factor
  hasSword?: boolean;
  animationSpeed?: "slow" | "normal" | "fast";
}>();

const beeSize = computed(() => props.size || 1);

const bodyFill = computed(() => props.bodyColor || "#FFD700"); // Gold
const wingFill = computed(() => props.wingColor || "#FFFFFF"); // White
const eyeFill = computed(() => props.eyeColor || "#000000"); // Black
const stingerFill = computed(() => props.stingerColor || "#8B0000"); // Dark Red
const swordFill = computed(() => props.swordColor || "#A9A9A9"); // Dark Gray

const animationDuration = computed(() => {
  switch (props.animationSpeed) {
    case "slow":
      return "2s";
    case "fast":
      return "0.5s";
    default:
      return "1s";
  }
});
</script>

<template>
  <div class="digital-bee-container" :style="{ transform: `scale(${beeSize})` }">
    <svg viewBox="0 0 100 100" class="digital-bee-svg">
      <!-- Body -->
      <ellipse cx="50" cy="50" rx="25" ry="20" :fill="bodyFill" class="bee-body" />

      <!-- Wings -->
      <path d="M50 30 Q65 10 80 30 Q65 40 50 30 Z" :fill="wingFill" class="bee-wing left-wing" />
      <path d="M50 30 Q35 10 20 30 Q35 40 50 30 Z" :fill="wingFill" class="bee-wing right-wing" />

      <!-- Head -->
      <circle cx="50" cy="25" r="15" :fill="bodyFill" class="bee-head" />

      <!-- Eyes -->
      <circle cx="45" cy="22" r="3" :fill="eyeFill" class="bee-eye" />
      <circle cx="55" cy="22" r="3" :fill="eyeFill" class="bee-eye" />

      <!-- Stinger (optional) -->
      <polygon
        v-if="stingerColor"
        points="50,70 48,80 52,80"
        :fill="stingerFill"
        class="bee-stinger"
      />

      <!-- Sword (optional) -->
      <g v-if="hasSword" class="bee-sword">
        <rect x="60" y="55" width="5" height="20" :fill="swordFill" transform="rotate(45 60 55)" />
        <rect x="60" y="55" width="15" height="2" :fill="swordFill" transform="rotate(45 60 55)" />
      </g>
    </svg>
  </div>
</template>

<style scoped>
.digital-bee-container {
  display: inline-block;
  width: 50px; /* Base size */
  height: 50px;
  animation:
    born-fade-in 0.5s ease-out forwards,
    idle-hover 3s ease-in-out infinite alternate;
}

.digital-bee-svg {
  width: 100%;
  height: 100%;
  overflow: visible; /* Allow wings to go outside viewBox */
}

.bee-body,
.bee-head {
  transform-origin: center;
}

.bee-wing {
  transform-origin: 50% 30%; /* Pivot point for wings */
  animation: wing-flap v-bind(animationDuration) ease-in-out infinite alternate;
}

.left-wing {
  transform-origin: 50% 30%;
}

.right-wing {
  transform-origin: 50% 30%;
}

.bee-sword {
  transform-origin: 60px 55px; /* Pivot point for sword */
}

@keyframes born-fade-in {
  from {
    opacity: 0;
    transform: scale(0.5);
  }
  to {
    opacity: 1;
    transform: scale(v-bind(beeSize));
  }
}

@keyframes idle-hover {
  from {
    transform: translateY(0) scale(v-bind(beeSize));
  }
  to {
    transform: translateY(-5px) scale(v-bind(beeSize));
  }
}

@keyframes wing-flap {
  from {
    transform: rotateX(0deg);
  }
  to {
    transform: rotateX(45deg);
  }
}
</style>
