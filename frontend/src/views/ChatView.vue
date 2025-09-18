<script setup lang="ts">
import { useChatStore, type Message } from '@/stores/chat'
import { onMounted, onUnmounted, ref, watch, nextTick, computed } from 'vue'
import { storeToRefs } from 'pinia'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import hljs from 'highlight.js'
import InteractiveCodeBlock from '@/components/InteractiveCodeBlock.vue'
import DigitalBee from '@/components/DigitalBee.vue'
import HeroMessage from '@/components/HeroMessage.vue'
import BeeOrganella from '@/components/BeeOrganella.vue'
import TeammatePresence from '@/components/TeammatePresence.vue'
import RoomNavigation from '@/components/RoomNavigation.vue'


const chatStore = useChatStore()
const { messages, isConnected, currentUser, theme, isAiThinking, replyToMessageId, teammates, rooms, currentRoom } = storeToRefs(chatStore)

const newMessage = ref('')
const chatMessagesEl = ref<HTMLElement | null>(null)
const chatInputRef = ref<HTMLTextAreaElement | null>(null)
const expandedImages = ref(new Map<string, boolean>())
const imageCollapseTimers = ref(new Map<string, number>())

const threadedMessages = computed(() => {
  const messageMap = new Map<string, Message & { replies: Message[] }>()
  const rootMessages: (Message & { replies: Message[] })[] = []

  messages.value.forEach((msg: Message) => {
    messageMap.set(msg.id, { ...msg, replies: [] })
  })

  messages.value.forEach((msg: Message) => {
    if (msg.parent_id && messageMap.has(msg.parent_id)) {
      messageMap.get(msg.parent_id)?.replies.push(messageMap.get(msg.id)!)
    } else {
      rootMessages.push(messageMap.get(msg.id)!)
    }
  })

  // Sort root messages and their replies by timestamp
  rootMessages.sort((a: Message, b: Message) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime())
  rootMessages.forEach(rootMsg => {
    rootMsg.replies.sort((a: Message, b: Message) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime())
  })

  return rootMessages
})

function renderMarkdown(text: string) {
  const localMarked = new marked.Marked();
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
      const imageId = `img-wrapper-${Math.random().toString(36).substring(2, 9)}`;
      return `
        <div id="${imageId}" class="chat-image-wrapper collapsed">
          <img src="${href}" alt="${text}" title="${title || text}" class="chat-image" onclick="window.toggleImageExpansion('${imageId}')" />
          <button class="expand-image-btn" onclick="window.toggleImageExpansion('${imageId}')">Expand</button>
        </div>
      `;
    }

    const linkTitle = title || text;
    return `<a href="${href}" title="${linkTitle}" target="_blank" rel="noopener noreferrer">${text}</a>`;
  };

  // Custom code block renderer with a copy button
  renderer.code = (token) => {
    const { text: code, lang } = token;
    const language = hljs.getLanguage(lang || '') ? lang : 'plaintext';
    
    // Ensure code is a string before highlighting
    const highlightedCode = hljs.highlight(code || '', { language: language || 'plaintext' }).value;

    // Use a unique ID to connect the button to the code
    const codeId = `code-${Math.random().toString(36).substring(2, 9)}`;
    const codeWrapperId = `code-wrapper-${Math.random().toString(36).substring(2, 9)}`;

    return `
      <div id="${codeWrapperId}" class="code-block-wrapper collapsed">
        <button onclick="window.copyCodeToClipboardAndProvideFeedback('${codeId}', this)" class="copy-code-btn">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16"><path fill="currentColor" d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg> Copy
        </button>
        <pre><code id="${codeId}" class="language-${language}">${highlightedCode}</code></pre>
        <button class="expand-code-btn" onclick="window.toggleCodeExpansion('${codeWrapperId}')">Expand</button>
      </div>
    `;
  };

  localMarked.use({ renderer });
  localMarked.setOptions({
    gfm: true,
    breaks: true,
  });

  const rawHtml = localMarked.parse(text) as string;
  const sanitizedHtml = DOMPurify.sanitize(rawHtml, { ADD_ATTR: ['target'] });
  return sanitizedHtml;
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

// Initialize teammates on mount and refresh periodically
onMounted(() => {
  // Initial fetch
  chatStore.fetchTeammates()

  // Refresh teammates every 30 seconds
  const interval = setInterval(() => {
    chatStore.fetchTeammates()
  }, 30000)

  // Cleanup interval on unmount
  onUnmounted(() => {
    clearInterval(interval)
  })
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
    <div class="chat-main">
      <div class="chat-content">
    <div class="chat-messages" ref="chatMessagesEl">
      <template v-for="message in threadedMessages" :key="message.id">
        <div
          class="message"
          :class="{ 'own-message': message.sender_id === currentUser?.id, 'ai-message': message.is_bot, 'peaking-message': message.isPeaking, 'decaying-message': message.isDecaying }"
        >
          <div class="message-sender">
            <svg v-if="message.is_bot" class="ai-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16"><path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-2-9h4v2h-4v-2zm0-4h4v2h-4V7z"/></svg>
            {{ message.sender_name }}
          </div>
          <BeeOrganella
            v-if="message.bee_organella_type"
            :type="message.bee_organella_type"
            :size="1.5"
          />
          <HeroMessage
            v-else-if="message.hero_properties && message.dialogue_text"
            :hero-properties="message.hero_properties"
            :dialogue-text="message.dialogue_text"
          />
          <InteractiveCodeBlock
            v-else-if="message.code_content"
            :code-content="message.code_content"
            :code-language="message.code_language"
            :editor-id="`editor-${message.id}`"
          />
          <div v-else class="message-content" v-html="renderMarkdown(message.text)"></div>
          <div class="message-timestamp">{{ new Date(message.timestamp).toLocaleTimeString() }}</div>
          <button class="reply-btn" @click="handleReply(message.sender_name, message.id)">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="14" height="14" fill="currentColor" class="reply-icon"><path d="M10 9V5l-7 7 7 7v-4.1c5 0 8.5 1.6 11 5.1-1-5-4-10-11-11z"/></svg>
            <span>Reply</span>
          </button>
        </div>
        <div
          v-for="reply in message.replies"
          :key="reply.id"
          class="message reply-message"
          :class="{ 'own-message': reply.sender_id === currentUser?.id, 'ai-message': reply.is_bot, 'peaking-message': reply.isPeaking, 'decaying-message': reply.isDecaying }"
        >
          <div class="message-sender">
            <svg v-if="reply.is_bot" class="ai-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16"><path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-2-9h4v2h-4v-2zm0-4h4v2h-4V7z"/></svg>
            {{ reply.sender_name }}
          </div>
          <InteractiveCodeBlock
            v-if="reply.code_content"
            :code-content="reply.code_content"
            :code-language="reply.code_language"
            :editor-id="`editor-${reply.id}`"
          />
          <div v-else class="message-content" v-html="renderMarkdown(reply.text)"></div>
          <div class="message-timestamp">{{ new Date(reply.timestamp).toLocaleTimeString() }}</div>
          <button class="reply-btn" @click="handleReply(reply.sender_name, reply.id)">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="14" height="14" fill="currentColor" class="reply-icon"><path d="M10 9V5l-7 7 7 7v-4.1c5 0 8.5 1.6 11 5.1-1-5-4-10-11-11z"/></svg>
            <span>Reply</span>
          </button>
        </div>
      </template>
      <div v-if="isAiThinking" class="ai-thinking-indicator message ai-message">
        <div class="message-sender">
          <svg class="ai-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16"><path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-2-9h4v2h-4v-2zm0-4h4v2h-4V7z"/></svg>
          AI Teammate
        </div>
        <div class="message-content">
          <span>Thinking</span><span class="dot-animation">...</span>
        </div>
      </div>
      <DigitalBee :size="1.5" body-color="#FFA500" wing-color="#ADD8E6" has-sword animation-speed="fast" />
    </div>
        <div class="chat-input-area">
          <div v-if="replyToMessageId" class="reply-indicator">
            Replying to message...
            <button @click="cancelReply" class="cancel-reply-btn">x</button>
          </div>
          <textarea
            v-model="newMessage"
            @keydown="handleKeydown"
            placeholder="Message #general"
            rows="1"
            ref="chatInputRef"
          ></textarea>
          <button class="send-btn" @click="handleSendMessage" :disabled="!newMessage.trim()">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
              <path fill="currentColor" d="M3.478 2.405c.126-.138.29-.22.468-.245l16.204 2.315c.28.04.51.238.594.512c.084.274.01.57-.184.764L13.3 12l7.387 6.26c.194.194.268.49.184.764c-.084.274-.314.472-.594.512l-16.204 2.315c-.178.025-.342-.057-.468-.245c-.126-.188-.15-.43-.063-.642l4.5-9.5l-4.5-9.5c-.087-.212-.063-.454.063-.642z"/>
            </svg>
          </button>
        </div>
      </div>

      <div class="chat-sidebar">
        <TeammatePresence :teammates="teammates" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-view {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-main {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.chat-content {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
}

.chat-sidebar {
  width: 300px;
  flex-shrink: 0;
  border-left: 1px solid var(--color-border);
  background-color: var(--color-background-soft);
  padding: 1rem;
  overflow-y: auto;
}

@media (max-width: 768px) {
  .chat-sidebar {
    display: none; /* Hide sidebar on mobile */
  }
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

@keyframes message-born {
  from {
    opacity: 0;
    transform: translateY(10px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.message {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  max-width: 80%;
  align-self: flex-start;
  animation: message-born 0.3s ease-out forwards; /* Apply animation */
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

.message.ai-message .message-content {
  background-color: var(--color-background-ai);
  border-left: 4px solid var(--color-ai-accent);
}

.ai-icon {
  margin-right: 0.5rem;
  color: var(--color-ai-accent);
  vertical-align: middle;
}

.message.ai-message .message-sender {
  display: flex;
  align-items: center;
}

.message.ai-message {
  align-self: flex-start;
}

.message.ai-message .message-timestamp {
  align-self: flex-start;
}

.reply-message {
  margin-left: 2rem;
  border-left: 2px solid var(--color-border);
  padding-left: 0.5rem;
}

.message.peaking-message {
  animation: peaking-glow 1.5s ease-in-out infinite alternate;
  border: 2px solid var(--color-ai-accent); /* Example: a subtle border */
  box-shadow: 0 0 8px var(--color-ai-accent); /* Example: a subtle glow */
}

@keyframes peaking-glow {
  from { box-shadow: 0 0 4px var(--color-ai-accent); }
  to { box-shadow: 0 0 12px var(--color-ai-accent); }
}

.message.decaying-message {
  opacity: 0.6;
  filter: grayscale(50%);
  font-size: 0.9em;
  transition: opacity 0.5s ease-out, filter 0.5s ease-out, font-size 0.5s ease-out;
}

.reply-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  background: none;
  border: none;
  color: var(--color-text-mute);
  font-size: 0.8rem;
  cursor: pointer;
  padding: 0.2rem 0.5rem;
  border-radius: 12px;
  transition: background-color 0.2s ease, color 0.2s ease;
}

.reply-btn:hover {
  background-color: var(--color-background-mute);
  color: var(--color-text);
}

.reply-icon {
  transform: scaleX(-1); /* Flip horizontally */
}

.reply-indicator {
  position: absolute;
  bottom: 100%; /* Position above the textarea */
  left: 0;
  right: 0;
  background-color: var(--color-background-soft);
  padding: 0.5rem 1rem;
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
  border: 1px solid var(--color-border);
  border-bottom: none;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: var(--color-text);
  font-size: 0.9rem;
}

.cancel-reply-btn {
  background: none;
  border: none;
  color: var(--color-text-mute);
  font-size: 1rem;
  cursor: pointer;
  padding: 0.2rem;
  border-radius: 4px;
}

.cancel-reply-btn:hover {
  background-color: var(--color-background-mute);
}

.chat-input-area {
  padding: 1rem;
  border-top: 1px solid var(--color-border);
  display: flex;
  align-items: flex-end;
  gap: 0.5rem;
  position: relative; /* Needed for absolute positioning of reply-indicator */
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
  transition: max-height 0.3s ease-out;
}

:deep(.chat-image-wrapper) {
  position: relative;
  display: inline-block;
  max-width: 100%;
  overflow: hidden;
  border-radius: 8px;
  margin-top: 0.5rem;
}

:deep(.chat-image-wrapper.collapsed .chat-image) {
  max-height: 100px; /* Default thumbnail height */
  width: auto; /* Allow width to adjust */
  object-fit: contain; /* Ensure image fits within bounds without cropping */
  cursor: pointer;
}

:deep(.chat-image-wrapper.expanded .chat-image) {
  max-height: none; /* Full height */
  width: 100%; /* Take full width */
  object-fit: contain;
}

:deep(.expand-image-btn) {
  position: absolute;
  bottom: 0.5rem;
  right: 0.5rem;
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s ease;
}

:deep(.chat-image-wrapper.collapsed:hover .expand-image-btn) {
  opacity: 1;
}

:deep(.code-block-wrapper) {
  position: relative;
  max-height: 200px; /* Default collapsed height */
  overflow: hidden;
  transition: max-height 0.3s ease-out;
  border-radius: 6px;
  margin-top: 0.5rem;
}

:deep(.code-block-wrapper.expanded) {
  max-height: none; /* Full height when expanded */
}

:deep(.code-block-wrapper.collapsed::after) {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 50px; /* Gradient height */
  background: linear-gradient(to top, var(--color-background-soft), transparent);
  pointer-events: none; /* Allow clicks to pass through */
}

:deep(.expand-code-btn) {
  position: absolute;
  bottom: 0.5rem;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s ease;
  z-index: 10; /* Ensure button is above gradient */
}

:deep(.code-block-wrapper.collapsed:hover .expand-code-btn) {
  opacity: 1;
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

/* Highlight.js themes are now imported globally in main.ts */
</style>
