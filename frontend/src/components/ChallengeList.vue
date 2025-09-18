<script setup lang="ts">
import { challenges } from '@/challenges'
import { useChatStore } from '@/stores/chat'
import { storeToRefs } from 'pinia'

const chatStore = useChatStore()
const { language, solvedChallenges } = storeToRefs(chatStore)

const emit = defineEmits<{
  (e: 'select-challenge', id: string): void
}>()

function selectChallenge(id: string) {
  emit('select-challenge', id)
}

function isChallengeSolved(id: string): boolean {
  return solvedChallenges.value.includes(id)
}
</script>

<template>
  <div class="challenge-list-container">
    <h2>Challenges</h2>
    <ul>
      <li v-for="challenge in challenges" :key="challenge.id">
        <button @click="selectChallenge(challenge.id)">
          {{ challenge.content[language]?.title || challenge.content.en.title }}
          <span v-if="isChallengeSolved(challenge.id)" class="solved-badge">✔ Solved</span>
        </button>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.challenge-list-container {
  padding: 1rem;
  border-right: 1px solid var(--color-border);
  overflow-y: auto;
}

.challenge-list-container h2 {
  color: var(--color-heading);
  margin-top: 0;
  margin-bottom: 1rem;
}

.challenge-list-container ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.challenge-list-container li button {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  text-align: left;
  padding: 0.75rem 1rem;
  margin-bottom: 0.5rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background-color: var(--color-background-soft);
  color: var(--color-text);
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.challenge-list-container li button:hover {
  background-color: var(--color-background-mute);
  border-color: var(--color-border-hover);
}

.challenge-list-container li button.active {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}

.solved-badge {
  background-color: #4caf50;
  color: white;
  padding: 0.2em 0.6em;
  border-radius: 12px;
  font-size: 0.75rem;
  margin-left: 0.5rem;
}
</style>
