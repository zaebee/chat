<template>
  <div class="bee-organella-container">
    <svg class="bee-sheet" viewBox="0 0 200 200" role="img" aria-labelledby="beeTitle">
      <title id="beeTitle">{{ type }} Bee Organella</title>

      <defs>
        <!-- abdomen stripes pattern -->
        <pattern id="stripes" width="10" height="10" patternUnits="userSpaceOnUse">
          <rect width="10" height="10" fill="inherit" />
          <rect width="10" height="5" fill="var(--stripe)" />
        </pattern>

        <!-- ========== Worker ========== -->
        <symbol id="bee-worker" viewBox="0 0 200 200">
          <!-- abdomen -->
          <ellipse class="bee-part" cx="100" cy="100" rx="24" ry="34" fill="var(--body-worker)" />
          <ellipse class="bee-part" cx="100" cy="100" rx="24" ry="34" fill="url(#stripes)" />
          <!-- thorax -->
          <ellipse class="bee-part" cx="100" cy="70" rx="18" ry="20" fill="var(--body-worker)" />
          <!-- head -->
          <circle class="bee-part" cx="100" cy="44" r="14" fill="var(--body-worker)" />
          <!-- wings -->
          <ellipse
            class="bee-part flap-normal"
            cx="80"
            cy="70"
            rx="30"
            ry="14"
            fill="var(--wing)"
            transform-origin="100px 70px"
          />
          <ellipse
            class="bee-part flap-normal"
            cx="120"
            cy="70"
            rx="30"
            ry="14"
            fill="var(--wing)"
            transform-origin="100px 70px"
          />
          <!-- stinger -->
          <polygon class="bee-part" points="100,134 96,144 104,144" fill="var(--stripe)" />
        </symbol>
        <!-- ========== Scout ========== -->
        <symbol id="bee-scout" viewBox="0 0 200 200">
          <!-- abdomen smaller -->
          <ellipse class="bee-part" cx="100" cy="100" rx="20" ry="28" fill="var(--body-scout)" />
          <ellipse class="bee-part" cx="100" cy="100" rx="20" ry="28" fill="url(#stripes)" />
          <!-- thorax -->
          <ellipse class="bee-part" cx="100" cy="72" rx="16" ry="18" fill="var(--body-scout)" />
          <!-- head larger eyes -->
          <circle class="bee-part" cx="100" cy="46" r="16" fill="var(--body-scout)" />
          <!-- wings faster -->
          <ellipse
            class="bee-part flap-fast"
            cx="78"
            cy="72"
            rx="28"
            ry="12"
            fill="var(--wing)"
            transform-origin="100px 72px"
          />
          <ellipse
            class="bee-part flap-fast"
            cx="122"
            cy="72"
            rx="28"
            ry="12"
            fill="var(--wing)"
            transform-origin="100px 72px"
          />
          <!-- stinger -->
          <polygon class="bee-part" points="100,126 96,136 104,136" fill="var(--stripe)" />
        </symbol>
        <!-- ========== Queen ========== -->
        <symbol id="bee-queen" viewBox="0 0 200 200">
          <!-- long abdomen -->
          <ellipse class="bee-part" cx="100" cy="110" rx="28" ry="50" fill="var(--body-queen)" />
          <ellipse class="bee-part" cx="100" cy="110" rx="28" ry="50" fill="url(#stripes)" />
          <!-- thorax -->
          <ellipse class="bee-part" cx="100" cy="66" rx="20" ry="22" fill="var(--body-queen)" />
          <!-- head -->
          <circle class="bee-part" cx="100" cy="38" r="14" fill="var(--body-queen)" />
          <!-- crown -->
          <polygon class="bee-part" points="92,24 100,10 108,24" fill="gold" stroke="gold" />
          <!-- wings slower -->
          <ellipse
            class="bee-part flap-slow"
            cx="76"
            cy="66"
            rx="34"
            ry="16"
            fill="var(--wing)"
            transform-origin="100px 66px"
          />
          <ellipse
            class="bee-part flap-slow"
            cx="124"
            cy="66"
            rx="34"
            ry="16"
            fill="var(--wing)"
            transform-origin="100px 66px"
          />
          <!-- stinger -->
          <polygon class="bee-part" points="100,156 94,172 106,172" fill="var(--stripe)" />
        </symbol>

        <!-- ========== Guard ========== -->
        <symbol id="bee-guard" viewBox="0 0 200 200">
          <!-- thick thorax -->
          <ellipse class="bee-part" cx="100" cy="72" rx="22" ry="24" fill="var(--body-guard)" />
          <!-- abdomen -->
          <ellipse class="bee-part" cx="100" cy="112" rx="26" ry="38" fill="var(--body-guard)" />
          <ellipse class="bee-part" cx="100" cy="112" rx="26" ry="38" fill="url(#stripes)" />
          <!-- head -->
          <circle class="bee-part" cx="100" cy="44" r="12" fill="var(--body-guard)" />
          <!-- wings normal -->
          <ellipse
            class="bee-part flap-normal"
            cx="80"
            cy="72"
            rx="30"
            ry="14"
            fill="var(--wing)"
            transform-origin="100px 72px"
          />
          <ellipse
            class="bee-part flap-normal"
            cx="120"
            cy="72"
            rx="30"
            ry="14"
            fill="var(--wing)"
            transform-origin="100px 72px"
          />
          <!-- bigger stinger -->
          <polygon class="bee-part" points="100,140 92,158 108,158" fill="var(--stripe)" />
        </symbol>
       <!-- ========== Chronicler ========== -->
        <symbol id="bee-chronicler" viewBox="0 0 200 200">
          <!-- abdomen with sacred glow -->
          <ellipse
            class="bee-part"
            cx="100"
            cy="100"
            rx="22"
            ry="32"
            fill="var(--body-chronicler)"
          />
          <ellipse class="bee-part" cx="100" cy="100" rx="22" ry="32" fill="url(#stripes)" />
          <!-- thorax -->
          <ellipse
            class="bee-part"
            cx="100"
            cy="70"
            rx="18"
            ry="20"
            fill="var(--body-chronicler)"
          />
          <!-- head with wisdom -->
          <circle class="bee-part" cx="100" cy="44" r="14" fill="var(--body-chronicler)" />
          <!-- sacred scroll -->
          <rect
            class="bee-part"
            x="85"
            y="20"
            width="30"
            height="8"
            fill="#f4e4bc"
            stroke="#d4af37"
            stroke-width="1"
            rx="2"
          />
          <!-- wings with divine shimmer -->
          <ellipse
            class="bee-part flap-slow"
            cx="80"
            cy="70"
            rx="32"
            ry="15"
            fill="var(--wing-divine)"
            transform-origin="100px 70px"
          />
          <ellipse
            class="bee-part flap-slow"
            cx="120"
            cy="70"
            rx="32"
            ry="15"
            fill="var(--wing-divine)"
            transform-origin="100px 70px"
          />
          <!-- divine light emanation -->
          <circle
            class="bee-part divine-glow"
            cx="100"
            cy="44"
            r="20"
            fill="none"
            stroke="var(--divine-light)"
            stroke-width="2"
            opacity="0.6"
          />
          <!-- sacred quill -->
          <line
            class="bee-part"
            x1="115"
            y1="44"
            x2="125"
            y2="34"
            stroke="var(--divine-light)"
            stroke-width="2"
          />
        </symbol>
      <!-- ========== Jules ========== -->
        <symbol id="bee-jules" viewBox="0 0 200 200">
          <!-- abdomen -->
          <ellipse class="bee-part" cx="100" cy="100" rx="24" ry="34" fill="var(--body-jules)" />
          <ellipse class="bee-part" cx="100" cy="100" rx="24" ry="34" fill="url(#stripes)" />
          <!-- thorax -->
          <ellipse class="bee-part" cx="100" cy="70" rx="18" ry="20" fill="var(--body-jules)" />
          <!-- head -->
          <circle class="bee-part" cx="100" cy="44" r="14" fill="var(--body-jules)" />
          <!-- wings -->
          <ellipse
            class="bee-part flap-normal"
            cx="80"
            cy="70"
            rx="30"
            ry="14"
            fill="var(--wing)"
            transform-origin="100px 70px"
          />
          <ellipse
            class="bee-part flap-normal"
            cx="120"
            cy="70"
            rx="30"
            ry="14"
            fill="var(--wing)"
            transform-origin="100px 70px"
          />
          <!-- stinger -->
          <polygon class="bee-part" points="100,134 96,144 104,144" fill="var(--stripe)" />
        </symbol>
      </defs>

      <!-- Use the selected bee type -->
      <use :href="`#bee-${type}`" x="0" y="0" width="200" height="200" />
    </svg>
  </div>
</template>
<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{
  type: "worker" | "scout" | "queen" | "guard" | "chronicler" | "jules";
  size?: number; // Scale factor
}>();

const beeSize = computed(() => props.size || 1);

// CSS variables for colors
const bodyWorker = computed(() => "#f4b400");
const bodyScout = computed(() => "#ffdb55");
const bodyQueen = computed(() => "#d4943c");
const bodyGuard = computed(() => "#9c6d2c");
const bodyChronicler = computed(() => "#d4af37"); // Sacred gold
const bodyJules = computed(() => "#8b5cf6"); // Purple for the implementation detective
const stripe = computed(() => "#222");
const wing = computed(() => "rgba(200,240,255,0.5)");
const wingDivine = computed(() => "rgba(212, 175, 55, 0.4)"); // Golden divine wings
const divineLight = computed(() => "#f7dc6f"); // Divine golden light
</script>

<style scoped>
.bee-organella-container {
  display: inline-block;
  width: 50px; /* Base size */
  height: 50px;
  overflow: visible;
  transform: scale(v-bind(beeSize));
  transform-origin: center;
}

.bee-sheet {
  width: 100%;
  height: 100%;
  display: block;
}

.bee-part {
  stroke: var(--stroke);
  stroke-width: 1.5;
  vector-effect: non-scaling-stroke;
}
/* Custom properties for colors */
.bee-organella-container {
  --body-worker: v-bind(bodyWorker);
  --body-scout: v-bind(bodyScout);
  --body-queen: v-bind(bodyQueen);
  --body-guard: v-bind(bodyGuard);
  --body-chronicler: v-bind(bodyChronicler);
  --body-jules: v-bind(bodyJules);
  --stripe: v-bind(stripe);
  --wing: v-bind(wing);
  --wing-divine: v-bind(wingDivine);
  --divine-light: v-bind(divineLight);
}

/* wing flaps by caste */
.flap-fast {
  animation: flap 0.1s ease-in-out infinite;
}
.flap-normal {
  animation: flap 0.15s ease-in-out infinite;
}
.flap-slow {
  animation: flap 0.25s ease-in-out infinite;
}
@keyframes flap {
  0% {
    transform: rotateX(-25deg);
  }
  50% {
    transform: rotateX(25deg);
  }
  100% {
    transform: rotateX(-25deg);
  }
}

/* Divine glow animation for chronicler */
.divine-glow {
  animation: divine-pulse 3s ease-in-out infinite;
}
@keyframes divine-pulse {
  0%,
  100% {
    opacity: 0.3;
    stroke-width: 1;
  }
  50% {
    opacity: 0.8;
    stroke-width: 3;
  }
}
</style>