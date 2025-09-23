<script setup lang="ts">
import { computed } from 'vue';
import { useMarkdownRenderer } from '@/composables/useMarkdownRenderer';

const props = defineProps<{
  text: string;
}>();

const { renderMarkdown } = useMarkdownRenderer();

const renderedHtml = computed(() => {
  return renderMarkdown(props.text);
});
</script>

<template>
  <div class="markdown-preview" v-html="renderedHtml"></div>
</template>

<style scoped>
.markdown-preview {
  line-height: 1.6;
}

/* Basic markdown styling */
.markdown-preview :deep(strong) {
  font-weight: 600;
  color: var(--color-text);
}

.markdown-preview :deep(em) {
  font-style: italic;
  color: var(--color-text-2);
}

.markdown-preview :deep(code) {
  background: var(--color-background-soft);
  padding: 2px 4px;
  border-radius: 3px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.9em;
  color: var(--vt-c-blue-dark);
}

.markdown-preview :deep(pre) {
  background: var(--color-background-soft);
  padding: 12px;
  border-radius: 6px;
  overflow-x: auto;
  margin: 8px 0;
}

.markdown-preview :deep(pre code) {
  background: none;
  padding: 0;
  color: inherit;
}

.markdown-preview :deep(blockquote) {
  border-left: 4px solid var(--vt-c-blue);
  padding-left: 12px;
  margin: 8px 0;
  color: var(--color-text-2);
  font-style: italic;
}

.markdown-preview :deep(a) {
  color: var(--vt-c-blue);
  text-decoration: none;
}

.markdown-preview :deep(a:hover) {
  text-decoration: underline;
}

.markdown-preview :deep(ul), 
.markdown-preview :deep(ol) {
  padding-left: 20px;
  margin: 8px 0;
}

.markdown-preview :deep(li) {
  margin: 4px 0;
}

/* Mention styling */
.markdown-preview :deep(.mention) {
  background: var(--vt-c-blue-soft);
  color: var(--vt-c-blue-dark);
  padding: 2px 4px;
  border-radius: 3px;
  font-weight: 500;
}

/* Dark mode adjustments */
@media (prefers-color-scheme: dark) {
  .markdown-preview :deep(code) {
    color: var(--vt-c-blue-light);
  }
  
  .markdown-preview :deep(.mention) {
    background: var(--vt-c-blue-dark);
    color: var(--vt-c-blue-light);
  }
}
</style>