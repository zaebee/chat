<script setup lang="ts">
import { useChatStore } from '@/stores/chat'
import { onMounted, ref, watch, nextTick } from 'vue'
import { storeToRefs } from 'pinia'

const chatStore = useChatStore()
const { messages, isConnected, currentUser } = storeToRefs(chatStore)

const newMessage = ref('')
const chatMessagesEl = ref<HTMLElement | null>(null)

// Connect to the WebSocket when the component is mounted
onMounted(() => {
  // chatStore.connect('VueUser') // This is now handled by App.vue
})

// Watch for new messages and scroll to the bottom
watch(
  messages,
  async () => {
    await nextTick()
    if (chatMessagesEl.value) {
      chatMessagesEl.value.scrollTop = chatMessagesEl.value.scrollHeight
    }
  },
  { deep: true }
)

function handleSendMessage() {
  if (newMessage.value.trim()) {
    chatStore.sendMessage(newMessage.value.trim())
    newMessage.value = ''
  }
}
</script>

<template>
  <div class="chat-view">
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
        <div class="message-content">
          <p>{{ message.text }}</p>
        </div>
        <div class="message-timestamp">{{ new Date(message.timestamp).toLocaleTimeString() }}</div>
      </div>
    </div>
    <div class="chat-input-area">
      <input
        type="text"
        v-model="newMessage"
        @keyup.enter="handleSendMessage"
        placeholder="Message #general"
      />
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

.message-content p {
  margin: 0;
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
}

.chat-input-area input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background-color: var(--color-background-mute);
  color: var(--color-text);
  font-size: 1rem;
}

.chat-input-area input:focus {
  outline: none;
  border-color: var(--color-border-hover);
}
</style>
