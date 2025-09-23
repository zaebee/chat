<script setup lang="ts">
import { ref } from 'vue';

const props = defineProps<{
  textareaRef: HTMLTextAreaElement | null;
}>();

const emit = defineEmits<{
  (e: 'format', format: string): void;
}>();

const showToolbar = ref(false);

const formatText = (format: string) => {
  if (!props.textareaRef) return;
  
  const textarea = props.textareaRef;
  const start = textarea.selectionStart;
  const end = textarea.selectionEnd;
  const selectedText = textarea.value.substring(start, end);
  
  let formattedText = '';
  let cursorOffset = 0;
  
  switch (format) {
    case 'bold':
      formattedText = `**${selectedText}**`;
      cursorOffset = selectedText ? 0 : 2;
      break;
    case 'italic':
      formattedText = `*${selectedText}*`;
      cursorOffset = selectedText ? 0 : 1;
      break;
    case 'code':
      formattedText = `\`${selectedText}\``;
      cursorOffset = selectedText ? 0 : 1;
      break;
    case 'codeblock':
      formattedText = `\`\`\`\n${selectedText}\n\`\`\``;
      cursorOffset = selectedText ? 0 : 4;
      break;
    case 'quote':
      formattedText = `> ${selectedText}`;
      cursorOffset = selectedText ? 0 : 2;
      break;
  }
  
  // Replace selected text with formatted text
  const newValue = textarea.value.substring(0, start) + formattedText + textarea.value.substring(end);
  textarea.value = newValue;
  
  // Set cursor position
  const newCursorPos = selectedText ? end + formattedText.length - selectedText.length : start + formattedText.length - cursorOffset;
  textarea.setSelectionRange(newCursorPos, newCursorPos);
  
  // Trigger input event to update v-model
  textarea.dispatchEvent(new Event('input', { bubbles: true }));
  
  // Focus back to textarea
  textarea.focus();
  
  emit('format', format);
};

const toggleToolbar = () => {
  showToolbar.value = !showToolbar.value;
};
</script>

<template>
  <div class="formatting-toolbar">
    <button 
      class="toolbar-toggle"
      @click="toggleToolbar"
      :class="{ active: showToolbar }"
      title="Formatting options"
    >
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
        <path d="M9 4v3h5v12h3V7h5V4H9zm-6 8h3v7h3v-7h3V9H3v3z"/>
      </svg>
    </button>
    
    <div v-if="showToolbar" class="toolbar-buttons">
      <button 
        @click="formatText('bold')" 
        class="format-btn"
        title="Bold (**text**)"
      >
        <strong>B</strong>
      </button>
      
      <button 
        @click="formatText('italic')" 
        class="format-btn"
        title="Italic (*text*)"
      >
        <em>I</em>
      </button>
      
      <button 
        @click="formatText('code')" 
        class="format-btn"
        title="Inline code (`code`)"
      >
        <code>&lt;/&gt;</code>
      </button>
      
      <button 
        @click="formatText('codeblock')" 
        class="format-btn"
        title="Code block (```)"
      >
        <span class="code-block-icon">{ }</span>
      </button>
      
      <button 
        @click="formatText('quote')" 
        class="format-btn"
        title="Quote (> text)"
      >
        <span>"</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.formatting-toolbar {
  position: relative;
  display: flex;
  align-items: center;
  gap: 4px;
}

.toolbar-toggle {
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

.toolbar-toggle:hover,
.toolbar-toggle.active {
  background: var(--color-background-soft);
  border-color: var(--vt-c-blue);
  color: var(--vt-c-blue);
}

.toolbar-buttons {
  position: absolute;
  bottom: 100%;
  left: 0;
  display: flex;
  gap: 2px;
  padding: 4px;
  background: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin-bottom: 4px;
  z-index: 10;
}

.format-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border: none;
  border-radius: 4px;
  background: transparent;
  color: var(--color-text-2);
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 12px;
}

.format-btn:hover {
  background: var(--color-background-soft);
  color: var(--color-text);
}

.format-btn strong {
  font-weight: 700;
}

.format-btn em {
  font-style: italic;
}

.format-btn code {
  font-family: monospace;
  font-size: 10px;
}

.code-block-icon {
  font-family: monospace;
  font-weight: bold;
}

/* Dark mode adjustments */
@media (prefers-color-scheme: dark) {
  .toolbar-buttons {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }
}
</style>