<script setup lang="ts">
import type { Message } from "@/stores/messages";
import { useUserStore } from "@/stores/user";
import { useMarkdownRenderer } from "@/composables/useMarkdownRenderer";
import InteractiveCodeBlock from "@/components/InteractiveCodeBlock.vue";
import BeeOrganella from "@/components/BeeOrganella.vue";
import ChroniclerOrganella from "@/components/ChroniclerOrganella.vue";
import HeroMessage from "@/components/HeroMessage.vue";

const props = defineProps<{
  message: Message & { children?: Message[] }
}>();

const emit = defineEmits<{ 
  (e: 'reply', senderName: string, messageId: string): void 
}>();

const userStore = useUserStore();
const { currentUser } = userStore;
const { renderMarkdown } = useMarkdownRenderer();

function handleReply(senderName: string, messageId: string) {
  emit('reply', senderName, messageId);
}
</script>

<template>
  <div
    class="message"
    :class="{
      'own-message': message.sender_id === currentUser?.id,
      'ai-message': message.is_bot,
      'peaking-message': message.isPeaking,
      'decaying-message': message.isDecaying,
    }"
  >
    <div class="message-sender">
      <svg
        v-if="message.is_bot"
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
      {{ message.sender_name }}
    </div>
    <ChroniclerOrganella
      v-if="message.bee_organella_type === 'chronicler'"
      :is-recording="message.divine_action_type === 'pattern_recording'"
    />
    <BeeOrganella
      v-else-if="message.bee_organella_type"
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
      :code="message.code_content"
      :language="message.code_language"
      :editor-id="`editor-${message.id}`"
    />
    <div v-else class="message-content" v-html="renderMarkdown(message.text)"></div>
    <div class="message-timestamp">
      {{ new Date(message.timestamp).toLocaleTimeString() }}
    </div>
    <button class="reply-btn" @click="handleReply(message.sender_name, message.id)">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        width="14"
        height="14"
        fill="currentColor"
        class="reply-icon"
      >
        <path d="M10 9V5l-7 7 7 7v-4.1c5 0 8.5 1.6 11 5.1-1-5-4-10-11-11z" />
      </svg>
      <span>Reply</span>
    </button>
  </div>
  <!-- Render Children (replies) -->
  <div v-if="message.children && message.children.length > 0" class="replies-container">
    <MessageItem
      v-for="child in message.children"
      :key="child.id"
      :message="child"
      @reply="handleReply"
      class="reply-message"
    />
  </div>
</template>

<style scoped>
/* Scoped styles from ChatView.vue related to a single message will be moved here */
.message {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  max-width: 80%;
  align-self: flex-start;
  animation: message-born 0.3s ease-out forwards;
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

.message-timestamp {
  font-size: 0.75rem;
  color: var(--color-text-mute);
  align-self: flex-start;
}

.own-message .message-timestamp {
  align-self: flex-end;
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
  align-self: flex-start;
  margin-top: 4px;
}

.own-message .reply-btn {
  align-self: flex-end;
}

.reply-btn:hover {
  background-color: var(--color-background-mute);
  color: var(--color-text);
}

.reply-icon {
  transform: scaleX(-1);
}

.replies-container {
  margin-left: 2rem;
  border-left: 2px solid var(--color-border);
  padding-left: 1rem;
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
</style>
