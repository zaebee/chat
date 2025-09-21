<template>
  <div class="quest-panel">
    <div class="panel-header">
      <h3>📜 Quests in {{ room.name }}</h3>
      <button @click="$emit('back')" class="back-btn">← Back</button>
    </div>
    <div class="panel-content">
      <div v-if="quests.length === 0" class="no-quests">
        <p>No quests in this chamber.</p>
      </div>
      <div v-else class="quests-list">
        <div
          v-for="quest in quests"
          :key="quest.id"
          class="quest-card"
          :class="`status-${quest.status}`"
        >
          <div class="quest-header">
            <h4>{{ quest.title }}</h4>
            <span class="quest-status">{{ quest.status }}</span>
          </div>
          <p class="quest-description">{{ quest.description }}</p>
          <button class="start-quest-btn" v-if="quest.status === 'available'">Start Quest</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import type { Room } from "@/stores/game";

interface Props {
  room: Room;
}

interface Quest {
  id: string;
  title: string;
  description: string;
  status: "available" | "in-progress" | "completed";
}

defineProps<Props>();

const quests = ref<Quest[]>([
  {
    id: "1",
    title: "The First Journey",
    description: "Learn the basics of the Hive and create your first organella.",
    status: "available",
  },
  {
    id: "2",
    title: "The Pollen Collector",
    description: "Help a worker bee collect pollen from the nearby flowers.",
    status: "in-progress",
  },
  {
    id: "3",
    title: "The Guardian's Trial",
    description: "Prove your worth to the Hive's guardians by completing a series of challenges.",
    status: "completed",
  },
  {
    id: "4",
    title: "The Beetle's Riddle",
    description: "Find the beetle in the forest and solve its riddle.",
    status: "available",
  },
]);
</script>

<style scoped>
.quest-panel {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin: 1rem 0;
  overflow: hidden;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: linear-gradient(135deg, #3b82f6, #60a5fa);
  color: white;
}

.panel-header h3 {
  margin: 0;
  font-size: 1.2rem;
}

.back-btn {
  background: rgba(255, 255, 255, 0.8);
  border: none;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  cursor: pointer;
  font-size: 1.2rem;
  transition: all 0.3s ease;
}

.back-btn:hover {
  background: white;
  transform: scale(1.1);
}

.panel-content {
  padding: 1rem;
}

.no-quests {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.quests-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.quest-card {
  background: white;
  border-radius: 12px;
  padding: 1rem;
  border-left: 4px solid #e5e7eb;
  transition: all 0.3s ease;
}

.quest-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.quest-card.status-available {
  border-left-color: #4ade80;
}

.quest-card.status-in-progress {
  border-left-color: #fbbf24;
}

.quest-card.status-completed {
  border-left-color: #a855f7;
}

.quest-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.quest-header h4 {
  margin: 0;
  color: #333;
  font-size: 1.1rem;
}

.quest-status {
  background: rgba(59, 130, 246, 0.1);
  color: #1d4ed8;
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  font-size: 0.8rem;
  text-transform: capitalize;
}

.quest-description {
  color: #555;
  line-height: 1.5;
  margin: 0.5rem 0;
}

.start-quest-btn {
  background: linear-gradient(135deg, #4ade80, #22c55e);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  margin-top: 1rem;
  transition: all 0.3s ease;
}

.start-quest-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
}
</style>