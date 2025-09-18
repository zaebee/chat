<script setup lang="ts">
import { ref, computed } from 'vue'
import CodeEditor from '@/components/CodeEditor.vue'
import ChallengeList from '@/components/ChallengeList.vue'
import { challenges } from '@/challenges'
import { useChatStore } from '@/stores/chat'
import { storeToRefs } from 'pinia'

const chatStore = useChatStore()
const { language } = storeToRefs(chatStore)

const selectedChallengeId = ref(challenges[0]?.id || null)

const currentChallenge = computed(() => {
  return challenges.find((c) => c.id === selectedChallengeId.value)
})

function handleSelectChallenge(id: string) {
  selectedChallengeId.value = id
}
</script>

<template>
  <div class="playground-layout">
    <ChallengeList @select-challenge="handleSelectChallenge" />

    <div class="playground-content">
      <div v-if="currentChallenge" class="challenge-description">
        <h1>{{ currentChallenge.content[language]?.title || currentChallenge.content.en.title }}</h1>
        <p>{{ currentChallenge.content[language]?.description || currentChallenge.content.en.description }}</p>
      </div>
      <div v-else class="challenge-description">
        <h1>No Challenge Selected</h1>
        <p>Please select a challenge from the list.</p>
      </div>

      <CodeEditor v-if="currentChallenge" :challenge="currentChallenge" />
      <div v-else class="no-challenge-editor">
        <p>Select a challenge to start coding!</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.playground-layout {
  display: flex;
  height: 100%;
}

.playground-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 1rem;
}

.challenge-description {
  padding: 0 0 1rem 0;
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

.no-challenge-editor {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: var(--color-background-soft);
  border-radius: 8px;
  color: var(--color-text-mute);
}
</style>
