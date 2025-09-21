<script setup lang="ts">
import type { Message } from "@/stores/messages";
import MessageItem from "./MessageItem.vue";

const props = defineProps<{ 
  messages: (Message & { replies: Message[] })[] 
}>();

const emit = defineEmits<{ 
  (e: 'reply', senderName: string, messageId: string): void 
}>();

function handleReply(senderName: string, messageId: string) {
  emit('reply', senderName, messageId);
}
</script>

<template>
  <div class="chat-messages">
    <template v-for="message in messages" :key="message.id">
      <MessageItem :message="message" @reply="handleReply" />
    </template>
  </div>
</template>

<style scoped>
.chat-messages {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
</style>
