<template>
  <form class="create-room-form" @submit.prevent="submitForm">
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
</template>

<script setup lang="ts">
import { reactive } from "vue";
import { useGameStore } from "@/stores/game";

const emit = defineEmits(["cancel"]);

const gameStore = useGameStore();

const newRoom = reactive({
  name: "",
  description: "",
  type: "public",
  metadata: {
    theme: "forest",
  },
});

const submitForm = () => {
  if (!newRoom.name) return;
  gameStore.createRoom(newRoom);
  cancelCreation();
};

const cancelCreation = () => {
  emit("cancel");
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
.create-room-form .form-group {
  margin-bottom: 0.75rem;
}

.create-room-form input,
.create-room-form textarea,
.create-room-form select {
  width: 100%;
  padding: 0.5rem;
  border-radius: 6px;
  border: 1px solid var(--color-border);
  background-color: var(--color-background);
  color: var(--color-text);
  font-size: 0.9rem;
}

.create-room-form textarea {
  min-height: 80px;
  resize: vertical;
}

.create-room-form .form-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: 1rem;
}

.create-room-form button {
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  border: 1px solid transparent;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.create-room-form button[type="submit"] {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}

.create-room-form button[type="submit"]:hover {
  background-color: #0056b3;
}

.create-room-form button[type="button"] {
  background-color: var(--color-background-mute);
  color: var(--color-text);
  border-color: var(--color-border);
}

.create-room-form button[type="button"]:hover {
  background-color: var(--color-background-soft);
}
</style>
