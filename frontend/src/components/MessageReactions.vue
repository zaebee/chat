<script setup lang="ts">
import { ref, computed } from 'vue';
import { useUserStore } from '@/stores/user';
import { useMessagesStore } from '@/stores/messages';
import type { Message } from '@/stores/messages';

const props = defineProps<{
  message: Message;
}>();

const userStore = useUserStore();
const messagesStore = useMessagesStore();

const showReactionPicker = ref(false);
const reactionPickerRef = ref<HTMLElement | null>(null);

// Common emoji reactions
const commonEmojis = ['👍', '❤️', '😄', '😮', '😢', '😡', '🎉', '🚀'];

const reactions = computed(() => {
  if (!props.message.reactions) return [];
  
  return Object.entries(props.message.reactions)
    .filter(([_, reaction]) => reaction.count > 0)
    .map(([emoji, reaction]) => ({
      emoji,
      count: reaction.count,
      users: reaction.users,
      hasUserReacted: reaction.users.includes(userStore.currentUser?.id || '')
    }));
});

const toggleReaction = (emoji: string) => {
  if (!userStore.currentUser) return;
  
  messagesStore.toggleReaction(
    props.message.id,
    emoji,
    userStore.currentUser.id,
    userStore.currentUser.username
  );
  
  showReactionPicker.value = false;
};

const openReactionPicker = () => {
  showReactionPicker.value = !showReactionPicker.value;
};

// Close picker when clicking outside
const handleClickOutside = (event: Event) => {
  if (reactionPickerRef.value && !reactionPickerRef.value.contains(event.target as Node)) {
    showReactionPicker.value = false;
  }
};

// Add/remove event listener for clicking outside
import { onMounted, onUnmounted } from 'vue';

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<template>
  <div class="message-reactions">
    <!-- Existing Reactions -->
    <div v-if="reactions.length > 0" class="reactions-list">
      <button
        v-for="reaction in reactions"
        :key="reaction.emoji"
        class="reaction-button"
        :class="{ 'user-reacted': reaction.hasUserReacted }"
        @click="toggleReaction(reaction.emoji)"
        :title="`${reaction.users.length} reaction${reaction.users.length !== 1 ? 's' : ''}`"
      >
        <span class="reaction-emoji">{{ reaction.emoji }}</span>
        <span class="reaction-count">{{ reaction.count }}</span>
      </button>
    </div>

    <!-- Add Reaction Button -->
    <div class="reaction-picker-container" ref="reactionPickerRef">
      <button
        class="add-reaction-button"
        @click="openReactionPicker"
        title="Add reaction"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          width="16"
          height="16"
          fill="currentColor"
        >
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
        </svg>
        <span class="add-reaction-text">😊</span>
      </button>

      <!-- Reaction Picker -->
      <div v-if="showReactionPicker" class="reaction-picker">
        <button
          v-for="emoji in commonEmojis"
          :key="emoji"
          class="emoji-option"
          @click="toggleReaction(emoji)"
          :title="`React with ${emoji}`"
        >
          {{ emoji }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.message-reactions {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 4px;
  flex-wrap: wrap;
}

.reactions-list {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.reaction-button {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 2px 6px;
  border: 1px solid var(--color-border);
  border-radius: 12px;
  background: var(--color-background-soft);
  color: var(--color-text);
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.reaction-button:hover {
  background: var(--color-background-mute);
  border-color: var(--color-border-hover);
}

.reaction-button.user-reacted {
  background: var(--vt-c-blue-soft);
  border-color: var(--vt-c-blue);
  color: var(--vt-c-blue-dark);
}

.reaction-emoji {
  font-size: 14px;
  line-height: 1;
}

.reaction-count {
  font-weight: 500;
  min-width: 12px;
  text-align: center;
}

.reaction-picker-container {
  position: relative;
}

.add-reaction-button {
  display: flex;
  align-items: center;
  gap: 2px;
  padding: 2px 6px;
  border: 1px dashed var(--color-border);
  border-radius: 12px;
  background: transparent;
  color: var(--color-text-2);
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  opacity: 0.7;
}

.add-reaction-button:hover {
  opacity: 1;
  background: var(--color-background-soft);
  border-style: solid;
}

.add-reaction-text {
  font-size: 14px;
  line-height: 1;
}

.reaction-picker {
  position: absolute;
  top: 100%;
  left: 0;
  z-index: 100;
  display: flex;
  gap: 4px;
  padding: 8px;
  background: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin-top: 4px;
}

.emoji-option {
  padding: 4px;
  border: none;
  border-radius: 4px;
  background: transparent;
  font-size: 18px;
  cursor: pointer;
  transition: background 0.2s ease;
  line-height: 1;
}

.emoji-option:hover {
  background: var(--color-background-soft);
}

/* Dark mode adjustments */
@media (prefers-color-scheme: dark) {
  .reaction-picker {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }
}
</style>