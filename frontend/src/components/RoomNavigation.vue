<template>
  <div class="room-navigation">
    <h3 class="room-nav-title">💬 Rooms</h3>

    <div class="room-list">
      <div
        v-for="room in rooms"
        :key="room.id"
        class="room-item"
        :class="{ active: room.id === currentRoom }"
        @click="switchToRoom(room.id)"
      >
        <div class="room-info">
          <div class="room-name">
            {{ room.name }}
          </div>
          <div class="room-description">
            {{ room.description }}
          </div>
        </div>

        <div class="room-status">
          <div class="room-type" :class="`type-${room.type}`">
            {{ room.type }}
          </div>
        </div>
      </div>
    </div>

    <div v-if="rooms.length === 0 && !isCreating" class="no-rooms">
      <div class="no-rooms-icon">🌿</div>
      <p>Loading rooms...</p>
    </div>

    <div class="room-actions">
      <form v-if="isCreating" class="create-room-form" @submit.prevent="submitForm">
        <div class="form-group">
          <input v-model="newRoom.name" type="text" placeholder="Room Name" required />
        </div>
        <div class="form-group">
          <textarea v-model="newRoom.description" placeholder="Description"></textarea>
        </div>
        <div class="form-group">
          <select v-model="newRoom.type">
            <option value="public">Public</option>
            <option value="private">Private</option>
            <option value="ai">AI Teammate</option>
          </select>
        </div>
        <div class="form-group">
          <select v-model="newRoom.metadata.theme">
            <option value="forest">Forest</option>
            <option value="hive">Hive</option>
            <option value="minimal">Minimal</option>
          </select>
        </div>
        <div class="form-buttons">
          <button type="button" @click="cancelCreation">Cancel</button>
          <button type="submit">Create</button>
        </div>
      </form>

      <button v-else class="create-room-btn" @click="isCreating = true">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
          <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z" />
        </svg>
        Create Room
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";
import type { Room } from "@/stores/game";
import { useGameStore } from "@/stores/game";

interface Props {
  rooms: Room[];
  currentRoom: string;
}

interface Emits {
  (e: "switch-room", roomId: string): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const gameStore = useGameStore();
const isCreating = ref(false);

const newRoom = reactive({
  name: "",
  description: "",
  type: "public",
  metadata: {
    theme: "forest",
  },
});

const switchToRoom = (roomId: string) => {
  if (roomId !== props.currentRoom) {
    emit("switch-room", roomId);
  }
};

const submitForm = () => {
  if (!newRoom.name) return;
  gameStore.createRoom(newRoom);
  cancelCreation();
};

const cancelCreation = () => {
  isCreating.value = false;
  // Reset form
  Object.assign(newRoom, {
    name: "",
    description: "",
    type: "public",
    metadata: {
      theme: "forest",
    },
  });
};
</script>

<style scoped>
.room-navigation {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: var(--color-background-soft);
  border-right: 1px solid var(--color-border);
}

.room-nav-title {
  margin: 0;
  padding: 1rem;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-heading);
  border-bottom: 1px solid var(--color-border);
  background: var(--color-background);
}

.room-list {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem;
}

.room-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

.room-item:hover {
  background-color: var(--color-background-mute);
  border-color: var(--color-border-hover);
}

.room-item.active {
  background-color: #007bff;
  color: white;
  border-color: #0056b3;
}

.room-item.active .room-description {
  color: rgba(255, 255, 255, 0.8);
}

.room-item.active .room-type {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
}

.room-info {
  flex: 1;
  min-width: 0;
}

.room-name {
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.room-description {
  font-size: 0.75rem;
  color: var(--color-text-mute);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.room-status {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.25rem;
}

.room-type {
  background-color: var(--color-background-mute);
  color: var(--color-text-mute);
  font-size: 0.6rem;
  padding: 0.125rem 0.375rem;
  border-radius: 10px;
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.room-type.type-public {
  background-color: rgba(76, 175, 80, 0.1);
  color: #4caf50;
}

.room-type.type-private {
  background-color: rgba(255, 152, 0, 0.1);
  color: #ff9800;
}

.room-type.type-ai {
  background-color: rgba(103, 126, 234, 0.1);
  color: #677eea;
}

.no-rooms {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  color: var(--color-text-mute);
  text-align: center;
}

.no-rooms-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.room-actions {
  padding: 1rem;
  border-top: 1px solid var(--color-border);
}

.create-room-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.5rem;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  background-color: var(--color-background);
  color: var(--color-text);
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.create-room-btn:hover:not(:disabled) {
  background-color: var(--color-background-mute);
  border-color: var(--color-border-hover);
}

.create-room-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Scrollbar styling */
.room-list::-webkit-scrollbar {
  width: 4px;
}

.room-list::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 2px;
}

.room-list::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 2px;
}

.room-list::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}
</style>
