<script setup lang="ts">
import { useChatStore } from '@/stores/chat'
import { onMounted, ref, watch, nextTick } from 'vue'
import { storeToRefs } from 'pinia'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import hljs from 'highlight.js'

// Import highlight.js themes
import 'highlight.js/styles/github.css'
import 'highlight.js/styles/github-dark.css'

const chatStore = useChatStore()
const { messages, isConnected, currentUser, theme } = storeToRefs(chatStore)

const newMessage = ref('')
const chatMessagesEl = ref<HTMLElement | null>(null)

const renderer = new marked.Renderer();

// Custom link renderer for images and new tabs
renderer.link = (token) => {
  const { href, title, text } = token;
  // Guard against null or undefined href
  if (!href) {
    return text;
  }

  const imageExtensions = ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'];
  const isImage = imageExtensions.some(ext => href.toLowerCase().endsWith(ext));

  if (isImage) {
    return `<img src="${href}" alt="${text}" class="chat-image" />`;
  }
  
  const linkTitle = title || text;
  return `<a href="${href}" title="${linkTitle}" target="_blank" rel="noopener noreferrer">${text}</a>`;
};

// Global function for copying code (called from dynamically rendered HTML)
declare global {
  interface Window {
    copyCodeToClipboardAndProvideFeedback: (codeId: string, buttonEl: HTMLElement) => void;
  }
}

window.copyCodeToClipboardAndProvideFeedback = (codeId: string, buttonEl: HTMLElement) => {
  const codeElement = document.getElementById(codeId);
  if (codeElement) {
    navigator.clipboard.writeText(codeElement.innerText).then(() => {
      const originalText = buttonEl.innerHTML;
      buttonEl.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16"><path fill="currentColor" d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/></svg> Copied!';
      setTimeout(() => {
        buttonEl.innerHTML = originalText;
      }, 2000);
    }).catch(err => {
      console.error('Failed to copy text: ', err);
    });
  }
};

// Custom code block renderer with a copy button
renderer.code = (token) => {
  const { text: code, lang } = token;
  const language = hljs.getLanguage(lang || '') ? lang : 'plaintext';
  
  // Ensure code is a string before highlighting
  const highlightedCode = hljs.highlight(code || '', { language: language || 'plaintext' }).value;

  // Use a unique ID to connect the button to the code
  const codeId = `code-${Math.random().toString(36).substring(2, 9)}`;

  return `
    <div class="code-block-wrapper">
      <button onclick="window.copyCodeToClipboardAndProvideFeedback('${codeId}', this)" class="copy-code-btn">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16"><path fill="currentColor" d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg> Copy
      </button>
      <pre><code id="${codeId}" class="language-${language}">${highlightedCode}</code></pre>
    </div>
  `;
};

marked.use({ renderer });

// Configure marked to use highlight.js for code blocks
marked.setOptions({
  gfm: true,
  breaks: true,
});

// Watch for new messages and scroll to the bottom
watch(
  messages,
  async () => {
    await nextTick()
    if (chatMessagesEl.value) {
      // Apply highlighting to any new code blocks
      chatMessagesEl.value.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightElement(block as HTMLElement)
      })
      chatMessagesEl.value.scrollTop = chatMessagesEl.value.scrollHeight
    }
  },
  { deep: true }
)

function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    handleSendMessage()
  }
}

function handleSendMessage() {
  if (newMessage.value.trim()) {
    chatStore.sendMessage(newMessage.value.trim())
    newMessage.value = ''
  }
}

function renderMarkdown(text: string) {
  const rawHtml = marked.parse(text, { gfm: true, breaks: true }) as string
  return DOMPurify.sanitize(rawHtml, { ADD_ATTR: ['target'] })
}

// Auto-resize textarea
watch(newMessage, async (val) => {
  // Reset height to shrink if text is deleted
  const el = document.querySelector('.chat-input-area textarea') as HTMLTextAreaElement
  if (el) {
    el.style.height = 'auto'
    await nextTick()
    el.style.height = `${el.scrollHeight}px`
  }
})
</script>

<template>
  <div class="chat-view" :class="theme === 'dark' ? 'hljs-dark-theme' : 'hljs-light-theme'">
    <div class="chat-header">
      <h2>#general</h2>
      <span class="connection-status" :class="{ connected: isConnected }">
        {{ isConnected ? 'Connected' : 'Disconnected' }}
      </span>
    </div>
    <div class="chat-messages" ref="chatMessagesEl">
      <div
        v-for="message in messages"
        :key="message.id"
        class="message"
        :class="{ 'own-message': message.sender_id === currentUser?.id }"
      >
        <div class="message-sender">{{ message.sender_name }}</div>
        <div class="message-content" v-html="renderMarkdown(message.text)"></div>
        <div class="message-timestamp">{{ new Date(message.timestamp).toLocaleTimeString() }}</div>
      </div>
    </div>
    <div class="chat-input-area">
      <textarea
        v-model="newMessage"
        @keydown="handleKeydown"
        placeholder="Message #general"
        rows="1"
      ></textarea>
      <button class="send-btn" @click="handleSendMessage" :disabled="!newMessage.trim()">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
          <path fill="currentColor" d="M3.478 2.405c.126-.138.29-.22.468-.245l16.204 2.315c.28.04.51.238.594.512c.084.274.01.57-.184.764L13.3 12l7.387 6.26c.194.194.268.49.184.764c-.084.274-.314.472-.594.512l-16.204 2.315c-.178.025-.342-.057-.468-.245c-.126-.188-.15-.43-.063-.642l4.5-9.5l-4.5-9.5c-.087-.212-.063-.454.063-.642z"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<style scoped>
.chat-view {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid var(--color-border);
}

.chat-header h2 {
  margin: 0;
  font-size: 1.2rem;
  color: var(--color-heading);
}

.connection-status {
  font-size: 0.8rem;
  padding: 4px 8px;
  border-radius: 12px;
  background-color: #f44336;
  color: white;
}

.connection-status.connected {
  background-color: #4caf50;
}

.chat-messages {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.message {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  max-width: 80%;
  align-self: flex-start;
}

.own-message {
  align-self: flex-end;
}

.message-sender {
  font-weight: bold;
  font-size: 0.9rem;
  color: var(--color-heading);
}

.own-message .message-sender {
  align-self: flex-end;
}

.message-content {
  background-color: var(--color-background-soft);
  padding: 0.5rem 1rem;
  border-radius: 12px;
  color: var(--color-text);
  word-wrap: break-word;
}

.own-message .message-content {
  background-color: #007bff;
  color: white;
}

.message-timestamp {
  font-size: 0.75rem;
  color: var(--color-text-mute);
}

.own-message .message-timestamp {
  align-self: flex-end;
}

.chat-input-area {
  padding: 1rem;
  border-top: 1px solid var(--color-border);
  display: flex;
  align-items: flex-end;
  gap: 0.5rem;
}

.chat-input-area textarea {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background-color: var(--color-background-mute);
  color: var(--color-text);
  font-size: 1rem;
  font-family: inherit;
  resize: none;
  overflow-y: hidden; /* Hide scrollbar as it grows */
  line-height: 1.5;
  max-height: 150px; /* Prevent infinite growth */
}

.send-btn {
  background-color: #007bff;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  color: white;
  flex-shrink: 0;
  transition: background-color 0.2s ease;
}

.send-btn:hover {
  background-color: #0056b3;
}

.send-btn:disabled {
  background-color: #aaa;
  cursor: not-allowed;
}

.chat-input-area textarea:focus {
  outline: none;
  border-color: var(--color-border-hover);
}
</style>

<style>
:deep(.message-content p:first-child) {
  margin-top: 0;
}
:deep(.message-content p:last-child) {
  margin-bottom: 0;
}

:deep(.message-content a) {
  color: #007bff;
}

.own-message :deep(.message-content a) {
  color: #cce5ff;
}

:deep(.message-content pre) {
  background-color: var(--color-background-mute);
  padding: 0.75rem;
  border-radius: 6px;
  white-space: pre-wrap;
}

.own-message :deep(.message-content pre) {
  background-color: rgba(0, 0, 0, 0.2);
}

:deep(.message-content code) {
  background-color: var(--color-background-mute);
  padding: 0.2em 0.4em;
  margin: 0;
  font-size: 85%;
  border-radius: 3px;
}

.own-message :deep(.message-content code) {
  background-color: rgba(0, 0, 0, 0.2);
}

:deep(.chat-image) {
  max-width: 100%;
  max-height: 300px;
  border-radius: 8px;
  margin-top: 0.5rem;
}

:deep(.code-block-wrapper) {
  position: relative;
}

:deep(.copy-code-btn) {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background-color: var(--color-background);
  border: 1px solid var(--color-border);
  color: var(--color-text);
  border-radius: 6px;
  padding: 0.25rem 0.5rem;
  font-size: 0.8rem;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s ease;
}

:deep(.code-block-wrapper:hover .copy-code-btn) {
  opacity: 1;
}

/* Use the correct highlight.js theme based on the parent class */
.hljs-light-theme :deep(.message-content pre code) {
  @import 'highlight.js/styles/github.css';
}
.hljs-dark-theme :deep(.message-content pre code) {
  @import 'highlight.js/styles/github-dark.css';
}
</style>
