<script setup lang="ts">
import CodeEditor from '@/components/CodeEditor.vue'
import { challenges } from '@/challenges'
import { useChatStore } from '@/stores/chat'
import { storeToRefs } from 'pinia'

const chatStore = useChatStore()
const { language } = storeToRefs(chatStore)

// For now, we'll just use the first challenge.
const currentChallenge = challenges[0]
</script>

<template>
  <div class="playground-view">
    <div class="challenge-description">
      <h1>{{ currentChallenge.content[language]?.title || currentChallenge.content.en.title }}</h1>
      <p>{{ currentChallenge.content[language]?.description || currentChallenge.content.en.description }}</p>
    </div>
    <CodeEditor :challenge="currentChallenge" />
  </div>
</template>

<style scoped>
.playground-view {
  padding: 1rem;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.challenge-description {
  padding: 0 1rem 1rem 1rem;
  border-bottom: 1px solid var(--color-border);
  margin-bottom: 1rem;
}

.challenge-description h1 {
  color: var(--color-heading);
  margin: 0 0 0.5rem 0;
}

.challenge-description p {
  color: var(--color-text);
  margin: 0;
}
</style>
