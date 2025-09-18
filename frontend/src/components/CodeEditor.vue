<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { EditorView } from '@codemirror/view'
import { basicSetup } from 'codemirror'
import { python } from '@codemirror/lang-python'
import { oneDark } from '@codemirror/theme-one-dark'
import { pythonRunner } from '@/services/pythonRunner'
import { useChatStore } from '@/stores/chat'
import { storeToRefs } from 'pinia'
import type { Challenge } from '@/challenges'

const props = defineProps<{
  challenge: Challenge
}>()

const chatStore = useChatStore()
const { theme, language } = storeToRefs(chatStore)

const editorEl = ref<HTMLElement | null>(null)
const output = ref('')
const svgOutput = ref<string | null>(null)
const isRunning = ref(false)
const solutionResult = ref<'correct' | 'incorrect' | 'none'>('none')

let view: EditorView | null = null

// Function to create or reconfigure the editor
function createEditor(themeExtension: any[]) {
  // Destroy existing view if it exists
  if (view) {
    view.destroy()
    view = null
  }

  if (editorEl.value) {
    view = new EditorView({
      doc: props.challenge.startingCode,
      extensions: [basicSetup, python(), ...themeExtension],
      parent: editorEl.value,
    })
  }
}

// Create the editor when the component is mounted
onMounted(() => {
  const themeExtension = theme.value === 'dark' ? [oneDark] : []
  createEditor(themeExtension)
})

// Watch for theme changes and re-create the editor
watch(theme, (newTheme) => {
  const themeExtension = newTheme === 'dark' ? [oneDark] : []
  createEditor(themeExtension)
})

// Watch for challenge changes and update the editor content
watch(
  () => props.challenge.id,
  (newChallengeId, oldChallengeId) => {
    if (newChallengeId !== oldChallengeId && view) {
      view.dispatch({
        changes: { from: 0, to: view.state.doc.length, insert: props.challenge.startingCode },
      })
    }
  }
)

async function submitSolution() {
  if (isRunning.value) return

  isRunning.value = true
  solutionResult.value = 'none'
  output.value = 'Running tests...'

  const userCode = view.state.doc.toString()
  const currentLang = language.value || 'en'
  const challengeContent = props.challenge.content[currentLang] || props.challenge.content.en

  const result = await pythonRunner.runChallenge(
    userCode,
    challengeContent.testCases,
    props.challenge.functionName,
    challengeContent.successMessage,
    props.challenge.visualOutput
  )

  output.value = result.output
  svgOutput.value = result.svgOutput || null
  solutionResult.value = result.success ? 'correct' : 'incorrect'

  if (result.success) {
    chatStore.recordChallengeSolved(props.challenge.id)
  }

  isRunning.value = false
}
</script>

<template>
  <div class="code-editor-container">
    <div class="editor-panel">
      <div class="editor-header">
        <span>Python Code</span>
        <button @click="submitSolution" :disabled="isRunning">
          {{ isRunning ? 'Submitting...' : 'Submit Solution' }}
        </button>
      </div>
      <div ref="editorEl" class="editor"></div>
    </div>
    <div class="output-panel">
      <div class="output-header">
        <span>Output</span>
        <span v-if="solutionResult !== 'none'" :class="`result-badge ${solutionResult}`">
          {{ solutionResult === 'correct' ? '✔ Correct' : '❌ Incorrect' }}
        </span>
      </div>
      <div v-if="svgOutput" class="visual-output" v-html="svgOutput"></div>
      <pre class="output-content" v-else>{{ output }}</pre>
    </div>
  </div>
</template>

<style scoped>
.code-editor-container {
  display: flex;
  flex-direction: column;
  height: calc(100% - 4rem); /* Adjust based on parent padding */
  gap: 1rem;
}

.editor-panel, .output-panel {
  display: flex;
  flex-direction: column;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  overflow: hidden;
}

.editor-panel {
  flex: 3; /* Takes up more space */
}

.output-panel {
  flex: 2; /* Takes up less space */
}

.editor-header, .output-header {
  padding: 0.5rem 1rem;
  background-color: var(--color-background-soft);
  border-bottom: 1px solid var(--color-border);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}

.editor-header button {
  padding: 0.25rem 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  background-color: #007bff;
  color: white;
  cursor: pointer;
}

.editor-header button:disabled {
  background-color: #aaa;
  cursor: not-allowed;
}

.result-badge {
  font-size: 0.8rem;
  padding: 4px 8px;
  border-radius: 12px;
  color: white;
}

.result-badge.correct {
  background-color: #4caf50; /* Green */
}

.result-badge.incorrect {
  background-color: #f44336; /* Red */
}

.editor {
  flex: 1;
  overflow: auto;
}

.output-content {
  flex: 1;
  padding: 1rem;
  margin: 0;
  background-color: var(--color-background-mute);
  color: var(--color-text);
  white-space: pre-wrap;
  word-wrap: break-word;
  overflow-y: auto;
}

.visual-output {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: var(--color-background-mute);
  overflow: hidden;
}

.visual-output :deep(svg) {
  max-width: 100%;
  max-height: 100%;
  display: block;
}

/* Basic styling for the CodeMirror editor itself */
:deep(.cm-editor) {
  height: 100%;
}
</style>
