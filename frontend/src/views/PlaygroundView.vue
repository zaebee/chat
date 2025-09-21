<script setup lang="ts">
import { ref, computed } from "vue";
import { useRoute } from "vue-router";
import CodeEditor from "@/components/CodeEditor.vue";
import ChallengeList from "@/components/ChallengeList.vue";
import { challenges, type Challenge, SkillDomain, ATCGPhase } from "@/challenges";
import { useSettingsStore } from "@/stores/settings";
import { storeToRefs } from "pinia";

const settingsStore = useSettingsStore();
const { language } = storeToRefs(settingsStore);
const route = useRoute();

const selectedChallengeId = ref(challenges[0]?.id || null);

const isQuestMode = computed(() => !!route.query.quest);

const questChallenge = computed((): Challenge | null => {
  if (isQuestMode.value && route.query.quest === "genesis_1_3") {
    return {
      id: "genesis_1_3",
      functionName: "let_there_be_light",
      content: {
        en: {
          title: "Genesis 1:3 - The First Ritual",
          description: "Write a function `let_there_be_light` that prints the sacred words: Fiat Lux",
          successMessage: "A divine light fills the cosmos!",
          testCases: [],
        },
      },
      startingCode: "def let_there_be_light():\n  # Your implementation here\n\nlet_there_be_light()",
      visualOutput: false,
      skillDomains: [SkillDomain.FUNCTION],
      skillUnlocks: [],
      atcgSequence: [ATCGPhase.GENESIS],
      difficultyTier: 1,
    };
  }
  return null;
});

const currentChallenge = computed(() => {
  if (isQuestMode.value) {
    return questChallenge.value;
  }
  return challenges.find((c) => c.id === selectedChallengeId.value);
});

function handleSelectChallenge(id: string) {
  selectedChallengeId.value = id;
}
</script>

<template>
  <div class="playground-layout">
        <ChallengeList v-if="!isQuestMode" @select-challenge="handleSelectChallenge" />
    
        <div class="playground-content">
      <div v-if="currentChallenge" class="challenge-description">
        <h1>
          {{ currentChallenge.content[language]?.title || currentChallenge.content.en.title }}
        </h1>
        <p>{{ currentChallenge.content[language]?.description || currentChallenge.content.en.description }}</p>
      </div>
      <div v-else class="challenge-description">
        <h1>No Challenge Selected</h1>
        <p>Please select a challenge from the list.</p>
      </div>

      <CodeEditor v-if="currentChallenge" :challenge="currentChallenge" :is-quest-mode="isQuestMode" />
      <div v-else class="no-challenge-editor">
        <p>Select a challenge to start coding!</p>
      </div>
    </div>  </div>
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
