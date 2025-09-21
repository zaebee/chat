<script setup lang="ts">
import { ref } from 'vue'

const username = ref('')

const emit = defineEmits<{ (e: 'login', username: string): void }>()

function handleLogin() {
  if (username.value.trim()) {
    emit('login', username.value.trim())
  }
}
</script>

<template>
  <div class="login-overlay">
    <div class="login-box">
      <h2>Welcome to Hive Chat</h2>
      <p>Please choose a username to join</p>
      <form @submit.prevent="handleLogin">
        <input
          type="text"
          v-model="username"
          placeholder="Enter your username"
          autofocus
        />
        <button type="submit">Join Chat</button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.login-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.login-box {
  background-color: var(--color-background-soft);
  padding: 2rem 3rem;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.login-box h2 {
  color: var(--color-heading);
  margin-top: 0;
}

.login-box p {
  color: var(--color-text-mute);
  margin-bottom: 1.5rem;
}

.login-box input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background-color: var(--color-background-mute);
  color: var(--color-text);
  font-size: 1rem;
  text-align: center;
  margin-bottom: 1rem;
}

.login-box button {
  width: 100%;
  padding: 0.75rem;
  border: none;
  border-radius: 8px;
  background-color: #007bff;
  color: white;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.login-box button:hover {
  background-color: #0056b3;
}
</style>
