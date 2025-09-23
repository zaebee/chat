<script setup lang="ts">
/**
 * 🐝✨ MessageReactions Component - Phase 1.1 Sacred Protection ✨🐝
 * 
 * UPDATED: Sacred Reaction Manager with divine protection mechanisms
 * Addresses bee.Sage critical vulnerability: "Unbounded Memory Growth"
 * 
 * Sacred Protection Features:
 * - Bounded collections with automatic cleanup
 * - Circuit breaker patterns for failure isolation
 * - Memory monitoring and quota enforcement
 * - Graceful degradation under stress
 * 
 * Phase 1.1 Implementation:
 * - Sacred memory bounds and cleanup
 * - Divine protection against infinite growth
 * - Circuit breaker for cascade failure prevention
 * - Real-time metrics and monitoring
 * 
 * Future Phase 2: Backend integration with sacred protection maintained
 */
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useUserStore } from '@/stores/user';
import { useMessagesStore } from '@/stores/messages';
import { useSacredReactionManager, type SacredMessageReactions } from '@/utils/SacredReactionManager';
import type { Message } from '@/stores/messages';

const props = defineProps<{
  message: Message;
}>();

const userStore = useUserStore();
const messagesStore = useMessagesStore();

// Sacred Reaction Manager Integration
const sacredReactionManager = useSacredReactionManager();

const showReactionPicker = ref(false);
const reactionPickerRef = ref<HTMLElement | null>(null);
const isLoading = ref(false);
const errorMessage = ref<string | null>(null);

// Sacred reaction state
const sacredReactions = ref<SacredMessageReactions | null>(null);

// Common emoji reactions
const commonEmojis = ['👍', '❤️', '😄', '😮', '😢', '😡', '🎉', '🚀'];

// Sacred reactions computed property
const reactions = computed(() => {
  if (!sacredReactions.value) return [];
  
  return Object.entries(sacredReactions.value)
    .filter(([_, reaction]) => reaction.count > 0)
    .map(([emoji, reaction]) => ({
      emoji,
      count: reaction.count,
      users: reaction.users,
      hasUserReacted: reaction.users.includes(userStore.currentUser?.username || ''),
      lastUpdated: reaction.lastUpdated,
      popularity: reaction.popularity
    }))
    .sort((a, b) => b.popularity - a.popularity); // Sort by divine popularity
});

// Sacred metrics for monitoring
const sacredMetrics = computed(() => sacredReactionManager.getMetrics());
const isSystemHealthy = computed(() => sacredReactionManager.isHealthy.value);
const statusMessage = computed(() => sacredReactionManager.statusMessage.value);

// Sacred toggle reaction with divine protection
const toggleReaction = async (emoji: string) => {
  if (!userStore.currentUser) {
    errorMessage.value = 'Please log in to react to messages';
    return;
  }
  
  if (isLoading.value) return; // Prevent double-clicks
  
  isLoading.value = true;
  errorMessage.value = null;
  
  try {
    const success = await sacredReactionManager.toggleReaction(
      props.message.id,
      emoji,
      userStore.currentUser.id,
      userStore.currentUser.username
    );
    
    if (success) {
      // Reload reactions to reflect changes
      await loadSacredReactions();
      showReactionPicker.value = false;
    } else {
      errorMessage.value = 'Unable to add reaction - limit reached';
    }
  } catch (error: any) {
    console.error('Sacred Reaction Error:', error);
    
    if (error.code === 'CIRCUIT_BREAKER_OPEN') {
      errorMessage.value = 'System protection active - please try again in a moment';
    } else if (error.code === 'MEMORY_QUOTA_EXCEEDED') {
      errorMessage.value = 'Storage limit reached - cleaning up old reactions';
    } else {
      errorMessage.value = 'Unable to process reaction - please try again';
    }
    
    // Auto-clear error message after 5 seconds
    setTimeout(() => {
      errorMessage.value = null;
    }, 5000);
  } finally {
    isLoading.value = false;
  }
};

// Load sacred reactions for this message
const loadSacredReactions = async () => {
  try {
    sacredReactions.value = await sacredReactionManager.getReactionsForMessage(props.message.id);
  } catch (error) {
    console.error('Failed to load sacred reactions:', error);
  }
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

// Sacred lifecycle management with divine protection
onMounted(async () => {
  // Load initial reactions
  await loadSacredReactions();
  
  // Sacred event listener management
  document.addEventListener('click', handleClickOutside);
  
  // Listen for sacred memory cleanup events
  window.addEventListener('sacred-memory-cleanup', handleSacredCleanup);
});

onUnmounted(() => {
  // Sacred cleanup - prevent memory leaks
  document.removeEventListener('click', handleClickOutside);
  window.removeEventListener('sacred-memory-cleanup', handleSacredCleanup);
});

// Sacred cleanup event handler
const handleSacredCleanup = async () => {
  console.log('Sacred Memory Cleanup triggered - reloading reactions');
  await loadSacredReactions();
};
</script>

<template>
  <div class="message-reactions">
    <!-- Sacred Protection Status (only show if unhealthy) -->
    <div v-if="!isSystemHealthy" class="sacred-status-warning">
      <span class="status-icon">⚠️</span>
      <span class="status-text">{{ statusMessage }}</span>
    </div>
    
    <!-- Error Message Display -->
    <div v-if="errorMessage" class="sacred-error-message">
      <span class="error-icon">❌</span>
      <span class="error-text">{{ errorMessage }}</span>
    </div>
    
    <!-- Existing Reactions -->
    <div v-if="reactions.length > 0" class="reactions-list">
      <button
        v-for="reaction in reactions"
        :key="reaction.emoji"
        class="reaction-button"
        :class="{ 
          'user-reacted': reaction.hasUserReacted,
          'loading': isLoading,
          'popular': reaction.popularity > 0.7
        }"
        @click="toggleReaction(reaction.emoji)"
        :disabled="isLoading || !isSystemHealthy"
        :title="`${reaction.users.join(', ')} (${reaction.count} reaction${reaction.count !== 1 ? 's' : ''})`"
      >
        <span class="reaction-emoji">{{ reaction.emoji }}</span>
        <span class="reaction-count">{{ reaction.count }}</span>
        <span v-if="reaction.popularity > 0.8" class="popularity-indicator">✨</span>
      </button>
    </div>

    <!-- Add Reaction Button -->
    <div class="reaction-picker-container" ref="reactionPickerRef">
      <button
        class="add-reaction-button"
        :class="{ 'loading': isLoading, 'disabled': !isSystemHealthy }"
        @click="openReactionPicker"
        :disabled="isLoading || !isSystemHealthy"
        :title="isSystemHealthy ? 'Add reaction' : 'Reactions temporarily unavailable'"
      >
        <span v-if="isLoading" class="loading-spinner">⏳</span>
        <svg
          v-else
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
      <div v-if="showReactionPicker && isSystemHealthy" class="reaction-picker">
        <div class="picker-header">
          <span class="picker-title">Choose reaction</span>
          <span v-if="sacredMetrics.memory.usagePercentage > 80" class="memory-warning">
            ⚠️ {{ Math.round(sacredMetrics.memory.usagePercentage) }}% storage used
          </span>
        </div>
        <div class="emoji-grid">
          <button
            v-for="emoji in commonEmojis"
            :key="emoji"
            class="emoji-option"
            :disabled="isLoading"
            @click="toggleReaction(emoji)"
            :title="`React with ${emoji}`"
          >
            {{ emoji }}
          </button>
        </div>
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

/* Sacred Protection Status Styles */
.sacred-status-warning {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 2px 6px;
  background: rgba(255, 193, 7, 0.1);
  border: 1px solid rgba(255, 193, 7, 0.3);
  border-radius: 4px;
  font-size: 11px;
  color: #856404;
  margin-bottom: 4px;
}

.sacred-error-message {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 2px 6px;
  background: rgba(220, 53, 69, 0.1);
  border: 1px solid rgba(220, 53, 69, 0.3);
  border-radius: 4px;
  font-size: 11px;
  color: #721c24;
  margin-bottom: 4px;
  animation: fadeIn 0.3s ease-in;
}

.status-icon, .error-icon {
  font-size: 10px;
}

.status-text, .error-text {
  font-weight: 500;
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
  position: relative;
}

.reaction-button:hover:not(:disabled) {
  background: var(--color-background-mute);
  border-color: var(--color-border-hover);
}

.reaction-button.user-reacted {
  background: var(--vt-c-blue-soft);
  border-color: var(--vt-c-blue);
  color: var(--vt-c-blue-dark);
}

.reaction-button.popular {
  border-color: var(--vt-c-yellow);
  box-shadow: 0 0 4px rgba(255, 193, 7, 0.3);
}

.reaction-button.loading {
  opacity: 0.6;
  cursor: not-allowed;
}

.reaction-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: var(--color-background-mute);
}

.popularity-indicator {
  position: absolute;
  top: -2px;
  right: -2px;
  font-size: 8px;
  animation: sparkle 2s infinite;
}

@keyframes sparkle {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.7; transform: scale(1.2); }
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

.add-reaction-button:hover:not(:disabled) {
  opacity: 1;
  background: var(--color-background-soft);
  border-style: solid;
}

.add-reaction-button.loading {
  opacity: 0.6;
  cursor: not-allowed;
}

.add-reaction-button.disabled {
  opacity: 0.3;
  cursor: not-allowed;
  border-color: var(--color-border-hover);
}

.loading-spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
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
  background: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin-top: 4px;
  min-width: 200px;
}

.picker-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 8px;
  border-bottom: 1px solid var(--color-border);
  background: var(--color-background-soft);
  border-radius: 8px 8px 0 0;
}

.picker-title {
  font-size: 11px;
  font-weight: 600;
  color: var(--color-text);
}

.memory-warning {
  font-size: 10px;
  color: #856404;
  background: rgba(255, 193, 7, 0.1);
  padding: 1px 4px;
  border-radius: 3px;
}

.emoji-grid {
  display: flex;
  gap: 4px;
  padding: 8px;
  flex-wrap: wrap;
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

.emoji-option:hover:not(:disabled) {
  background: var(--color-background-soft);
}

.emoji-option:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-4px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Dark mode adjustments */
@media (prefers-color-scheme: dark) {
  .reaction-picker {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }
}
</style>