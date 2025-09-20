<template>
  <div class="hexagonal-room-navigation">
    <div v-if="selectedRoom">
      <QuestPanel :room="selectedRoom" @back="selectedRoom = null" />
    </div>
    <div v-else>
      <h3 class="room-nav-title">🏰 Hive Chambers</h3>

      <div class="hex-room-map">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 400 300"
          width="100%"
          height="300"
          font-family="monospace"
        >
          <title>Hive Chat Chambers — Hexagonal Room Layout</title>

          <!-- Central hub room -->
          <HexaRoom
            v-if="rooms.length > 0"
            :room="rooms[0]"
            :is-active="rooms[0].id === currentRoom"
            points="170,150 190,120 230,120 250,150 230,180 190,180"
            :x="210"
            :y="150"
            @select-room="handleRoomSelect"
          />

          <!-- Surrounding rooms in hexagonal pattern -->
          <HexaRoom
            v-if="rooms.length > 1"
            :room="rooms[1]"
            :is-active="rooms[1].id === currentRoom"
            points="110,90 130,60 170,60 190,90 170,120 130,120"
            :x="150"
            :y="90"
            @select-room="handleRoomSelect"
          />

          <HexaRoom
            v-if="rooms.length > 2"
            :room="rooms[2]"
            :is-active="rooms[2].id === currentRoom"
            points="250,90 270,60 310,60 330,90 310,120 270,120"
            :x="290"
            :y="90"
            @select-room="handleRoomSelect"
          />

          <!-- Additional rooms for more than 3 -->
          <HexaRoom
            v-if="rooms.length > 3"
            :room="rooms[3]"
            :is-active="rooms[3].id === currentRoom"
            points="290,180 310,150 350,150 370,180 350,210 310,210"
            :x="330"
            :y="180"
            @select-room="handleRoomSelect"
          />

          <HexaRoom
            v-if="rooms.length > 4"
            :room="rooms[4]"
            :is-active="rooms[4].id === currentRoom"
            points="250,240 270,210 310,210 330,240 310,270 270,270"
            :x="290"
            :y="240"
            @select-room="handleRoomSelect"
          />

          <HexaRoom
            v-if="rooms.length > 5"
            :room="rooms[5]"
            :is-active="rooms[5].id === currentRoom"
            points="110,240 130,210 170,210 190,240 170,270 130,270"
            :x="150"
            :y="240"
            @select-room="handleRoomSelect"
          />

          <HexaRoom
            v-if="rooms.length > 6"
            :room="rooms[6]"
            :is-active="rooms[6].id === currentRoom"
            points="70,180 90,150 130,150 150,180 130,210 90,210"
            :x="110"
            :y="180"
            @select-room="handleRoomSelect"
          />

          <!-- Connecting lines between rooms -->
          <g
            class="connection-lines"
            stroke="var(--color-border)"
            stroke-width="1"
            stroke-dasharray="2,3"
            opacity="0.5"
          >
            <line v-if="rooms.length > 1" x1="190" y1="120" x2="170" y2="120" />
            <line v-if="rooms.length > 2" x1="230" y1="120" x2="250" y2="120" />
            <line v-if="rooms.length > 3" x1="250" y1="150" x2="290" y2="150" />
            <line v-if="rooms.length > 4" x1="230" y1="180" x2="250" y2="210" />
            <line v-if="rooms.length > 5" x1="190" y1="180" x2="170" y2="210" />
            <line v-if="rooms.length > 6" x1="170" y1="150" x2="130" y2="150" />
          </g>
        </svg>
      </div>

      <!-- Fallback for no rooms or loading -->
      <div v-if="rooms.length === 0" class="no-rooms">
        <div class="no-rooms-icon" title="It's a flower of creation">🌸</div>
        <p>Discovering chambers...</p>
      </div>

      <!-- Room actions -->
      <div class="room-actions">
        <CreateRoomForm v-if="isCreating" @cancel="isCreating = false" />

        <button v-else class="create-room-btn" @click="isCreating = true" title="It's a flower of creation">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z" />
          </svg>
          Create Chamber
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import HexaRoom from "@/components/HexaRoom.vue";
import type { Room } from "@/stores/game";
import CreateRoomForm from "@/components/CreateRoomForm.vue";
import QuestPanel from "@/components/QuestPanel.vue";

interface Props {
  rooms: Room[];
  currentRoom: string;
}

interface Emits {
  (e: "switch-room", roomId: string): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const isCreating = ref(false);
const selectedRoom = ref<Room | null>(null);

const handleRoomSelect = (room: Room) => {
  selectedRoom.value = room;
};
</script>

<style scoped>
.hexagonal-room-navigation {
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

.hex-room-map {
  flex: 1;
  padding: 1rem;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
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
</style>
