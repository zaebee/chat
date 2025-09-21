<script setup lang="ts">
import { ref, watch, nextTick } from "vue";

const props = defineProps<{ 
  modelValue: string; 
  replyToMessageId: string | null; 
}>();

const emit = defineEmits<{ 
  (e: 'update:modelValue', value: string): void; 
  (e: 'sendMessage'): void; 
  (e: 'cancelReply'): void; 
}>();

const chatInputRef = ref<HTMLTextAreaElement | null>(null);

const localNewMessage = ref(props.modelValue);

watch(
  () => props.modelValue,
  (newValue) => {
    localNewMessage.value = newValue;
  }
);

watch(localNewMessage, (newValue) => {
  emit('update:modelValue', newValue);
});

function handleKeydown(e: KeyboardEvent) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    emit('sendMessage');
  }
}

function cancelReply() {
  emit('cancelReply');
}

// Auto-resize textarea
watch(localNewMessage, async () => {
  const el = chatInputRef.value;
  if (el) {
    el.style.height = "auto";
    await nextTick();
    el.style.height = `${el.scrollHeight}px`;
  }
});

// Focus input when reply state changes
watch(
  () => props.replyToMessageId,
  (newVal) => {
    if (newVal) {
      nextTick(() => {
        chatInputRef.value?.focus();
      });
    }
  }
);
</script>

<template>
  <div class="chat-input-area">
    <div v-if="replyToMessageId" class="reply-indicator">
      Replying to message...
      <button @click="cancelReply" class="cancel-reply-btn">x</button>
    </div>
    <textarea
      v-model="localNewMessage"
      @keydown="handleKeydown"
      placeholder="Message #general"
      rows="1"
      ref="chatInputRef"
    ></textarea>
    <button class="send-btn" @click="emit('sendMessage')" :disabled="!localNewMessage.trim()">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
        <path
          fill="currentColor"
          d="M3.478 2.405c.126-.138.29-.22.468-.245l16.204 2.315c.28.04.51.238.594.512c.084.274.01.57-.184.764L13.3 12l7.387 6.26c.194.194.268.49.184.764c-.084.274-.314.472-.594.512l-16.204 2.315c-.178.025-.342-.057-.468-.245c-.126-.188-.15-.43-.063-.642l4.5-9.5l-4.5-9.5c-.087-.212-.063-.454.063-.642z"
        />
      </svg>
    </button>
  </div>
</template>

<style scoped>
.reply-indicator {
  position: absolute;
  bottom: 100%;
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
  position: relative;
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
  overflow-y: hidden;
  line-height: 1.5;
  max-height: 150px;
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
