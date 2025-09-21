<template>
  <div class="interactive-code-block">
    <div class="code-header">
      <span class="language-label">{{ language }}</span>
      <button @click="copyCode" class="copy-button" :class="{ copied: isCopied }">
        {{ isCopied ? 'Copied!' : 'Copy' }}
      </button>
    </div>
    <div class="code-content">
      <pre><code :class="`language-${language}`" v-html="highlightedCode"></code></pre>
    </div>
    <div v-if="showRunButton" class="code-actions">
      <button @click="runCode" class="run-button" :disabled="isRunning">
        {{ isRunning ? 'Running...' : 'Run Code' }}
      </button>
    </div>
    <div v-if="output" class="code-output">
      <div class="output-header">Output:</div>
      <pre class="output-content">{{ output }}</pre>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import hljs from 'highlight.js'

interface Props {
  code: string
  language?: string
  showRunButton?: boolean
  editable?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  language: 'python',
  showRunButton: false,
  editable: false
})

const emit = defineEmits<{
  run: [code: string]
  codeChange: [code: string]
}>()

const isCopied = ref(false)
const isRunning = ref(false)
const output = ref('')

const highlightedCode = computed(() => {
  try {
    return hljs.highlight(props.code, { language: props.language }).value
  } catch (error) {
    console.warn('Highlighting failed:', error)
    return props.code
  }
})

async function copyCode() {
  try {
    await navigator.clipboard.writeText(props.code)
    isCopied.value = true
    setTimeout(() => {
      isCopied.value = false
    }, 2000)
  } catch (error) {
    console.error('Failed to copy code:', error)
  }
}

async function runCode() {
  if (isRunning.value) return
  
  isRunning.value = true
  output.value = ''
  
  try {
    // Emit run event for parent to handle
    emit('run', props.code)
    
    // For demo purposes, simulate code execution
    if (props.language === 'python') {
      await new Promise(resolve => setTimeout(resolve, 1000))
      output.value = 'Code executed successfully!\n(This is a demo output)'
    }
  } catch (error) {
    output.value = `Error: ${error}`
  } finally {
    isRunning.value = false
  }
}

onMounted(() => {
  // Initialize highlight.js if needed
  hljs.configure({ ignoreUnescapedHTML: true })
})
</script>

<style scoped>
.interactive-code-block {
  border: 1px solid #e1e5e9;
  border-radius: 8px;
  overflow: hidden;
  margin: 16px 0;
  background: #f8f9fa;
}

.code-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 16px;
  background: #e9ecef;
  border-bottom: 1px solid #dee2e6;
}

.language-label {
  font-size: 12px;
  font-weight: 600;
  color: #6c757d;
  text-transform: uppercase;
}

.copy-button {
  padding: 4px 12px;
  font-size: 12px;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  background: white;
  color: #495057;
  cursor: pointer;
  transition: all 0.2s;
}

.copy-button:hover {
  background: #f8f9fa;
  border-color: #adb5bd;
}

.copy-button.copied {
  background: #d4edda;
  border-color: #c3e6cb;
  color: #155724;
}

.code-content {
  padding: 16px;
  background: #ffffff;
  overflow-x: auto;
}

.code-content pre {
  margin: 0;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 14px;
  line-height: 1.5;
}

.code-content code {
  background: none;
  padding: 0;
  border-radius: 0;
}

.code-actions {
  padding: 12px 16px;
  background: #f8f9fa;
  border-top: 1px solid #dee2e6;
}

.run-button {
  padding: 8px 16px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.run-button:hover:not(:disabled) {
  background: #0056b3;
}

.run-button:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.code-output {
  border-top: 1px solid #dee2e6;
}

.output-header {
  padding: 8px 16px;
  background: #e9ecef;
  font-size: 12px;
  font-weight: 600;
  color: #495057;
}

.output-content {
  padding: 12px 16px;
  background: #f8f9fa;
  margin: 0;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 13px;
  line-height: 1.4;
  color: #495057;
  white-space: pre-wrap;
  word-wrap: break-word;
}

/* Dark theme support */
@media (prefers-color-scheme: dark) {
  .interactive-code-block {
    background: #2d3748;
    border-color: #4a5568;
  }
  
  .code-header {
    background: #4a5568;
    border-color: #718096;
  }
  
  .language-label {
    color: #a0aec0;
  }
  
  .copy-button {
    background: #2d3748;
    border-color: #718096;
    color: #e2e8f0;
  }
  
  .copy-button:hover {
    background: #4a5568;
  }
  
  .code-content {
    background: #1a202c;
  }
  
  .code-actions {
    background: #2d3748;
    border-color: #4a5568;
  }
  
  .output-header {
    background: #4a5568;
    color: #e2e8f0;
  }
  
  .output-content {
    background: #2d3748;
    color: #e2e8f0;
  }
}
</style>