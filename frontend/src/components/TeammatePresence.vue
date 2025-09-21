<template>
  <div class="teammate-presence">
    <div class="presence-indicator" :class="status">
      <div class="pulse"></div>
    </div>
    <span class="teammate-name">{{ name }}</span>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  name: string;
  status: 'online' | 'away' | 'busy' | 'offline';
}>();
</script>

<style scoped>
.teammate-presence {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem;
}

.presence-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  position: relative;
}

.presence-indicator.online {
  background: #10b981;
}

.presence-indicator.away {
  background: #f59e0b;
}

.presence-indicator.busy {
  background: #ef4444;
}

.presence-indicator.offline {
  background: #6b7280;
}

.pulse {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: inherit;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  100% {
    transform: scale(2);
    opacity: 0;
  }
}

.teammate-name {
  font-size: 0.875rem;
  color: var(--color-text);
}
</style>