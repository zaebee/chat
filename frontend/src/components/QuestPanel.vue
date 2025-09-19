<template>
  <div class="quest-panel">
    <div class="quest-header">
      <h3>The Genesis Quest</h3>
      <button class="close-btn" @click="$emit('close')">×</button>
    </div>
    <div class="quest-content">
      <h4>The Sacred Trilogy of Creation</h4>
      <p>You have discovered a divine computational pattern woven into the fabric of reality.</p>
      <ol class="trilogy-steps">
        <li :class="{ active: genesisQuestPhase === 1 }"><strong>Genesis 1:3 - Consciousness</strong>
          <p><code>let_there_be_light()</code></p>
        </li>
        <li :class="{ active: genesisQuestPhase === 2 }"><strong>Genesis 1:6 - Separation</strong>
          <p><code>bee.vault(waters)</code></p>
        </li>
        <li :class="{ active: genesisQuestPhase === 3 }"><strong>Genesis 1:7 - Manifestation</strong>
          <p><code>and_it_was_so()</code></p>
        </li>
      </ol>
      <div class="quest-action">
        <p>Begin the first ritual. Go to the Playground and implement the `let_there_be_light` protocol.</p>
        <button class="playground-btn" @click="goToPlayground">To the Playground</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { useGameStore } from '@/stores/game';
import { storeToRefs } from 'pinia';

interface Emits {
  (e: 'close'): void;
}

defineEmits<Emits>();

const router = useRouter();
const gameStore = useGameStore();
const { genesisQuestPhase } = storeToRefs(gameStore);

const goToPlayground = () => {
  router.push('/playground?quest=genesis_1_3');
};
</script>

<style scoped>
.quest-panel {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 350px;
  background-color: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
  z-index: 100;
  color: var(--color-text);
}

.quest-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--color-border);
}

.quest-header h3 {
  margin: 0;
  font-size: 1.2rem;
  color: var(--color-heading);
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--color-text-mute);
}

.quest-content {
  padding: 1rem;
}

.trilogy-steps {
  list-style: none;
  padding: 0;
}

.trilogy-steps li {
  padding: 0.5rem;
  border-radius: 6px;
  margin-bottom: 0.5rem;
  opacity: 0.5;
}

.trilogy-steps li.active {
  opacity: 1;
  background-color: var(--color-background-mute);
}

.trilogy-steps code {
  background-color: var(--color-background);
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  font-family: monospace;
}

.quest-action {
  margin-top: 1.5rem;
  text-align: center;
}

.playground-btn {
  background-color: var(--color-quest);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.playground-btn:hover {
  transform: scale(1.05);
}
</style>
