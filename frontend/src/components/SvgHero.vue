<template>
  <div class="svg-hero-container">
    <svg class="svg-hero" viewBox="0 0 200 260" role="img" aria-labelledby="heroTitle heroDesc">
      <title id="heroTitle">Player hero holding sword in left hand</title>
      <desc id="heroDesc">
        Stylized vector hero made of paths; sword attached to left wrist group.
      </desc>                                                                                                                                               
      <!-- torso -->
      <g id="body">
        <path
          class="hero-part"
          fill="var(--shirt)"
          d="M86 70 C86 100 114 100 114 70 L114 140 L86 140 Z"
        />
      </g>

      <!-- head -->
      <circle class="hero-part" cx="100" cy="44" r="18" fill="var(--skin)" />

      <!-- right arm (simple stroked limb) -->
      <path class="hero-part" fill="none" d="M114 82 Q140 96 152 118" stroke-width="6" />

      <!-- left arm + sword group: the group is transformable around wrist anchor near (60,120) -->
      <g id="left-arm-sword">
        <!-- left arm as a filled limb (from shoulder to wrist) -->
        <path
          class="hero-part"
          fill="var(--skin)"
          d="M86 82 C76 98 68 110 60 120 L66 128 C74 118 82 104 90 90 Z"
          stroke-width="2"
        />
        <!-- small wrist anchor (invisible but clarifies origin) -->
        <circle cx="60" cy="120" r="0.5" fill="transparent" />

        <!-- sword (local coords: blade goes up) -->
        <g id="sword" transform="translate(60,120) rotate(-10)">
          <!-- blade -->
          <rect
            x="-2"
            y="-70"
            width="4"
            height="70"
            class="hero-part"
            fill="var(--sword-blade)"
            stroke-width="1"
          />
          <!-- guard -->
          <rect
            x="-8"
            y="-62"
            width="16"
            height="6"
            fill="var(--sword-guard)"
            class="hero-part"
            stroke-width="1"
          />
          <!-- pommel -->
          <circle
            cx="0"
            cy="-54"
            r="3"
            fill="var(--sword-guard)"
            class="hero-part"
            stroke-width="1"
          />
        </g>
      </g>

      <!-- legs -->
      <path class="hero-part" fill="var(--shirt)" d="M88 140 L92 200 L104 200 L108 140 Z" />
    </svg>
  </div>
</template>
<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{
  skinColor?: string;
  shirtColor?: string;
  swordBladeColor?: string;
  swordGuardColor?: string;
  strokeColor?: string;
  size?: number; // Scale factor
  animateSwing?: boolean; // Control animation
}>();

const skin = computed(() => props.skinColor || "#f0cfb0");
const shirt = computed(() => props.shirtColor || "#2b6cb0");
const swordBlade = computed(() => props.swordBladeColor || "#e6eef6");
const swordGuard = computed(() => props.swordGuardColor || "#b8860b");
const stroke = computed(() => props.strokeColor || "#222");

const heroSize = computed(() => props.size || 1);
const swingAnimation = computed(() =>
  props.animateSwing !== false ? "swing 1.2s ease-in-out infinite" : "none",
);
</script>

<style scoped>
.svg-hero-container {
  display: inline-block;
  width: 100px; /* Base size */
  height: 130px;
  overflow: visible;
  /* Initial animation for born effect */
  animation: born-fade-in 0.5s ease-out forwards;
}

.svg-hero {
  width: 100%;
  height: 100%;
  display: block;
}
.hero-part {
  stroke: v-bind(stroke);
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  fill-rule: evenodd;
  vector-effect: non-scaling-stroke;
}

/* Custom properties for colors */
.svg-hero-container {
  --skin: v-bind(skin);
  --shirt: v-bind(shirt);
  --stroke: v-bind(stroke);
  --sword-blade: v-bind(swordBlade);
  --sword-guard: v-bind(swordGuard);
}

/* Transform origin is wrist coordinate (60px,120px in SVG user coords below) */
#left-arm-sword {
  transform-box: fill-box;
  transform-origin: 60px 120px;
  animation: v-bind(swingAnimation);
}

@keyframes swing {
  0% {
    transform: rotate(-8deg);
  }

  50% {
    transform: rotate(12deg);
  }

  100% {
    transform: rotate(-8deg);
  }
}
@keyframes born-fade-in {
  from {
    opacity: 0;
    transform: scale(0.5);
  }
  to {
    opacity: 1;
    transform: scale(v-bind(heroSize));
  }
}
                                                                                                                                                            @media (prefers-reduced-motion: reduce) {
  #left-arm-sword {
    animation: none;
  }
}
</style>