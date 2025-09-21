<template>
  <g class="hexa-room" @click="selectRoom">
    <polygon :class="roomClass" :points="points" />
    <text :x="x" :y="y - 10" class="room-label name">
      {{ room.name }}
    </text>
    <text :x="x" :y="y + 10" class="room-label type">
      {{ room.type }}
    </text>
    <circle v-if="isActive" :cx="x + 35" :cy="y - 35" r="6" class="active-indicator" />
  </g>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { Room } from "@/stores/game";

interface Props {
  room: Room;
  isActive: boolean;
  points: string;
  x: number;
  y: number;
}

interface Emits {
  (e: "select-room", room: Room): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const roomClass = computed(() => {
  let classes = "hex-room";

  if (props.isActive) {
    classes += " active-room";
  }

  // Add type-specific styling
  classes += ` room-type-${props.room.type}`;

  return classes;
});

const selectRoom = () => {
  emit("select-room", props.room);
};
</script>

<style scoped>
.hex-room {
  fill: var(--color-background-soft);
  stroke: var(--color-border);
  stroke-width: 2;
  cursor: pointer;
  transition: all 0.3s ease;
}

.hex-room:hover {
  fill: var(--color-background-mute);
  stroke: var(--color-border-hover);
  stroke-width: 3;
}

.hex-room.active-room {
  fill: #007bff;
  stroke: #0056b3;
  stroke-width: 3;
}

.hex-room.room-type-public {
  stroke: #4caf50;
}

.hex-room.room-type-private {
  stroke: #ff9800;
}

.hex-room.room-type-ai {
  stroke: #677eea;
}

.room-label {
  fill: var(--color-text);
  text-anchor: middle;
  font-family: monospace;
  pointer-events: none;
}

.room-label.name {
  font-size: 11px;
  font-weight: 600;
}

.room-label.type {
  font-size: 8px;
  text-transform: uppercase;
  fill: var(--color-text-mute);
}

.active-room .room-label {
  fill: white;
}

.active-indicator {
  fill: #ffd700;
  stroke: #fff;
  stroke-width: 2;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.2);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
