<script setup lang="ts">
import { ref } from 'vue';

const showHelp = ref(false);

const toggleHelp = () => {
  showHelp.value = !showHelp.value;
};

const examples = [
  { format: '**bold text**', description: 'Bold text' },
  { format: '*italic text*', description: 'Italic text' },
  { format: '`inline code`', description: 'Inline code' },
  { format: '```\ncode block\n```', description: 'Code block' },
  { format: '> quoted text', description: 'Quote' },
  { format: '@username', description: 'Mention user' },
  { format: '[link text](url)', description: 'Link' },
  { format: '- list item', description: 'Bullet list' },
  { format: '1. numbered item', description: 'Numbered list' }
];
</script>

<template>
  <div class="formatting-help">
    <button 
      class="help-toggle"
      @click="toggleHelp"
      :class="{ active: showHelp }"
      title="Formatting help"
    >
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17h-2v-2h2v2zm2.07-7.75l-.9.92C13.45 12.9 13 13.5 13 15h-2v-.5c0-1.1.45-2.1 1.17-2.83l1.24-1.26c.37-.36.59-.86.59-1.41 0-1.1-.9-2-2-2s-2 .9-2 2H8c0-2.21 1.79-4 4-4s4 1.79 4 4c0 .88-.36 1.68-.93 2.25z"/>
      </svg>
    </button>
    
    <div v-if="showHelp" class="help-panel">
      <h4>Formatting Guide</h4>
      <div class="examples">
        <div v-for="example in examples" :key="example.format" class="example">
          <code class="format-code">{{ example.format }}</code>
          <span class="format-description">{{ example.description }}</span>
        </div>
      </div>
      <div class="help-footer">
        <small>Use the formatting toolbar or type markdown directly</small>
      </div>
    </div>
  </div>
</template>

<style scoped>
.formatting-help {
  position: relative;
}

.help-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  background: var(--color-background);
  color: var(--color-text-2);
  cursor: pointer;
  transition: all 0.2s ease;
}

.help-toggle:hover,
.help-toggle.active {
  background: var(--color-background-soft);
  border-color: var(--vt-c-blue);
  color: var(--vt-c-blue);
}

.help-panel {
  position: absolute;
  bottom: 100%;
  right: 0;
  width: 300px;
  padding: 16px;
  background: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin-bottom: 8px;
  z-index: 20;
}

.help-panel h4 {
  margin: 0 0 12px 0;
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text);
}

.examples {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.example {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.format-code {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 12px;
  background: var(--color-background-soft);
  padding: 2px 4px;
  border-radius: 3px;
  color: var(--vt-c-blue-dark);
}

.format-description {
  font-size: 12px;
  color: var(--color-text-2);
}

.help-footer {
  margin-top: 12px;
  padding-top: 8px;
  border-top: 1px solid var(--color-border);
}

.help-footer small {
  color: var(--color-text-2);
  font-size: 11px;
}

/* Dark mode adjustments */
@media (prefers-color-scheme: dark) {
  .help-panel {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }
  
  .format-code {
    color: var(--vt-c-blue-light);
  }
}
</style>