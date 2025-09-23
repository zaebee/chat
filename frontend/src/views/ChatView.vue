<script setup lang="ts">
import { useChatStore } from "@/stores/chat";
import { useMessagesStore, type Message } from "@/stores/messages";
import { useUserStore } from "@/stores/user";
import { useTeammatesStore } from "@/stores/teammates";
import { useGameStore } from "@/stores/game";
import { useSettingsStore } from "@/stores/settings";
import { onMounted, onUnmounted, ref, watch, nextTick, computed } from "vue";
import { storeToRefs } from "pinia";

import MessageList from "@/components/MessageList.vue";
import ChatInput from "@/components/ChatInput.vue";
import TypingIndicator from "@/components/TypingIndicator.vue";

import TeammatePresence from "@/components/TeammatePresence.vue";
import RoomNavigation from "@/components/RoomNavigation.vue";
import HexagonalRoomNavigation from "@/components/HexagonalRoomNavigation.vue";
import OrganellaPanel from "@/components/OrganellaPanel.vue";

const chatStore = useChatStore();
const messagesStore = useMessagesStore();
const userStore = useUserStore();
const teammatesStore = useTeammatesStore();
const gameStore = useGameStore();
const settingsStore = useSettingsStore();

const { messages, isAiThinking, replyToMessageId } = storeToRefs(messagesStore);
const { isConnected, typingUsers } = storeToRefs(chatStore);
const { currentUser } = storeToRefs(userStore);
const { teammates } = storeToRefs(teammatesStore);
const { rooms, currentRoom } = storeToRefs(gameStore);
const { theme } = storeToRefs(settingsStore); // Added

// Toggle between hexagonal and traditional room layout
const useHexagonalLayout = ref(true); // Default to hexagonal layout

const newMessage = ref("");
const chatMessagesEl = ref<HTMLElement | null>(null);

const threadedMessages = computed(() => {
  const messageMap = new Map<string, Message & { replies: Message[] }>();
  const rootMessages: (Message & { replies: Message[] })[] = [];

  messages.value.forEach((msg: Message) => {
    messageMap.set(msg.id, { ...msg, replies: [] });
  });

  messages.value.forEach((msg: Message) => {
    if (msg.parent_id && messageMap.has(msg.parent_id)) {
      messageMap.get(msg.parent_id)?.replies.push(messageMap.get(msg.id)!);
    } else {
      rootMessages.push(messageMap.get(msg.id)!);
    }
  });

  // Sort root messages and their replies by timestamp
  rootMessages.sort(
    (a: Message, b: Message) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime(),
  );
  rootMessages.forEach((rootMsg) => {
    rootMsg.replies.sort(
      (a: Message, b: Message) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime(),
    );
  });

  return rootMessages;
});

function handleSendMessage() {
  const messageText = newMessage.value.trim();
  if (!messageText) return;

  if (messageText.startsWith("/")) {
    // It's a command
    const command = messageText.substring(1);
    messagesStore.processCommand(command);
  } else {
    // It's a regular message
    messagesStore.sendMessage(messageText, replyToMessageId.value);
  }

  newMessage.value = "";
  messagesStore.setReplyToMessageId(null); // Clear reply state after sending
}

function handleReply(senderName: string, messageId: string) {
  newMessage.value = `@${senderName} `;
  messagesStore.setReplyToMessageId(messageId);
}

function cancelReply() {
  messagesStore.setReplyToMessageId(null);
  newMessage.value = "";
}

function handleRoomSwitch(roomId: string) {
  chatStore.switchRoom(roomId);
}

// Initialize teammates and rooms on mount and refresh periodically
onMounted(() => {
  // Initial fetch
  teammatesStore.fetchTeammates();
  gameStore.fetchRooms();

  // Cleanup interval on unmount
  onUnmounted(() => {
    // No interval to clear, but keeping the hook for future use
  });
});
</script>

<template>
  <div class="chat-view" :class="theme === 'dark' ? 'hljs-dark-theme' : 'hljs-light-theme'">
    <div class="chat-header">
      <h2>{{ rooms?.find((r) => r.id === currentRoom)?.name || "#general" }}</h2>
      <span class="connection-status" :class="{ connected: isConnected }">
        {{ isConnected ? "Connected" : "Disconnected" }}
      </span>
    </div>
    <div class="chat-main">
      <div class="chat-rooms">
        <div class="room-layout-toggle">
          <button
            @click="useHexagonalLayout = !useHexagonalLayout"
            class="layout-toggle-btn"
            :title="useHexagonalLayout ? 'Switch to list view' : 'Switch to hexagonal view'"
          >
            {{ useHexagonalLayout ? '📋' : '⬢' }}
          </button>
        </div>

        <HexagonalRoomNavigation
          v-if="useHexagonalLayout"
          :rooms="rooms"
          :current-room="currentRoom"
          @switch-room="handleRoomSwitch"
        />
        <RoomNavigation
          v-else
          :rooms="rooms"
          :current-room="currentRoom"
          @switch-room="handleRoomSwitch"
        />
      </div>
      <div class="chat-content">
        <MessageList :messages="threadedMessages" @reply="handleReply" />
        
        <!-- Typing Indicator -->
        <TypingIndicator :typing-users="typingUsers" />

        <div v-if="isAiThinking" class="ai-thinking-indicator message ai-message">
          <div class="message-sender">
            <svg
              class="ai-icon"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              width="16"
              height="16"
            >
              <path
                fill="currentColor"
                d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-2-9h4v2h-4v-2zm0-4h4v2h-4V7z"
              />
            </svg>
            AI Teammate
          </div>
          <div class="message-content">
            <span>Thinking</span><span class="dot-animation">...</span>
          </div>
        </div>
        <DigitalBee
          :size="1.5"
          body-color="#FFA500"
          wing-color="#ADD8E6"
          has-sword
          animation-speed="fast"
        />

        <ChatInput
          v-model="newMessage"
          :reply-to-message-id="replyToMessageId"
          @send-message="handleSendMessage"
          @cancel-reply="cancelReply"
        />
      </div>

      <div class="chat-sidebar">
        <OrganellaPanel />
        <div v-for="teammate in teammates" :key="teammate.id">
          <TeammatePresence 
            :name="teammate.name" 
            :status="teammate.status as 'online' | 'away' | 'busy' | 'offline'" 
          />
        </div>
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

.chat-rooms {
  width: 280px;
  flex-shrink: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.room-layout-toggle {
  padding: 0.5rem;
  border-bottom: 1px solid var(--color-border);
  background: var(--color-background);
  display: flex;
  justify-content: center;
}

.layout-toggle-btn {
  background: none;
  border: 1px solid var(--color-border);
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 1.2rem;
  transition: all 0.2s ease;
  color: var(--color-text);
}

.layout-toggle-btn:hover {
  background-color: var(--color-background-mute);
  border-color: var(--color-border-hover);
  transform: scale(1.05);
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

@media (max-width: 1024px) {
  .chat-rooms {
    width: 220px;
  }
}

@media (max-width: 768px) {
  .chat-rooms {
    display: none; /* Hide room navigation on mobile */
  }
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
  padding: 0.25rem 1rem;
  border-radius: 8px;
  color: var(--color-text);
  word-wrap: break-word;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.own-message .message-content {
  background-color: var(--color-border-hover);
  color: var(--color-heading);
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
  from {
    box-shadow: 0 0 4px var(--color-ai-accent);
  }
  to {
    box-shadow: 0 0 12px var(--color-ai-accent);
  }
}

.message.decaying-message {
  opacity: 0.6;
  filter: grayscale(50%);
  font-size: 0.9em;
  transition:
    opacity 0.5s ease-out,
    filter 0.5s ease-out,
    font-size 0.5s ease-out;
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
  transition:
    background-color 0.2s ease,
    color 0.2s ease;
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
</style>