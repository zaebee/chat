<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useChatStore } from '@/stores/chat';

// Phase 1: Local-only typing indicator
// Future Phase 2: Will integrate with WebSocket for real-time multi-user typing
const props = defineProps<{
  typingUsers?: string[];
  showLocalTyping?: boolean;
}>();

const chatStore = useChatStore();

// Local typing simulation for Phase 1 demo
const localTypingUsers = ref<string[]>([]);

// Simulate typing activity based on local input
const simulateTyping = () => {
  if (props.showLocalTyping) {
    localTypingUsers.value = ['You'];
    setTimeout(() => {
      localTypingUsers.value = [];
    }, 2000);
  }
};

// Use provided typing users or local simulation
const activeTypingUsers = computed(() => {
  return props.typingUsers || localTypingUsers.value;
});

const typingText = computed(() => {
  const users = activeTypingUsers.value;
  if (users.length === 0) return '';
  
  if (users.length === 1) {
    return `${users[0]} is typing...`;
  } else if (users.length === 2) {
    return `${users[0]} and ${users[1]} are typing...`;
  } else {
    return `${users[0]} and ${users.length - 1} others are typing...`;
  }
});

const isVisible = computed(() => activeTypingUsers.value.length > 0);

// Expose simulation function for parent components
defineExpose({
  simulateTyping
});
</script>

<template>
  <div v-if="isVisible" class="typing-indicator">
    <div class="typing-content">
      <div class="typing-dots">
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="dot"></span>
      </div>
      <span class="typing-text">{{ typingText }}</span>
    </div>
  </div>
</template>

<style scoped>
.typing-indicator {
  padding: 8px 16px;
  margin: 4px 0;
  background: var(--color-background-soft);
  border-radius: 8px;
  border-left: 3px solid var(--vt-c-blue);
  opacity: 0.8;
  animation: fadeIn 0.3s ease-in;
}

.typing-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.typing-dots {
  display: flex;
  gap: 2px;
}

.dot {
  width: 4px;
  height: 4px;
  background: var(--vt-c-blue);
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out;
}

.dot:nth-child(1) {
  animation-delay: 0s;
}

.dot:nth-child(2) {
  animation-delay: 0.2s;
}

.dot:nth-child(3) {
  animation-delay: 0.4s;
}

.typing-text {
  font-size: 14px;
  color: var(--color-text-2);
  font-style: italic;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: scale(1);
    opacity: 0.5;
  }
  30% {
    transform: scale(1.2);
    opacity: 1;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 0.8;
    transform: translateY(0);
  }
}

/* Dark mode adjustments */
@media (prefers-color-scheme: dark) {
  .typing-indicator {
    background: var(--color-background-mute);
  }
}
</style>