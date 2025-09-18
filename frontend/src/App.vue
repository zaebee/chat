<script setup lang="ts">
import { onMounted, ref, watchEffect } from 'vue'
import { RouterView, RouterLink } from 'vue-router'
import { useChatStore } from '@/stores/chat'
import { storeToRefs } from 'pinia'
import LoginModal from '@/components/LoginModal.vue'

const isCollapsed = ref(false)
const chatStore = useChatStore()
const { currentUser, theme, language, totalXp, level } = storeToRefs(chatStore)

// On startup, check for saved username and theme
onMounted(() => {
  chatStore.init()
})

// Watch for theme changes and apply them to the document
watchEffect(() => {
  document.documentElement.className = theme.value === 'dark' ? 'dark-theme' : ''
})

function toggleSidebar() {
  isCollapsed.value = !isCollapsed.value
}

function handleLogin(username: string) {
  chatStore.login(username)
}
</script>

<template>
  <LoginModal v-if="!currentUser" @login="handleLogin" />
  <div v-else class="app-container">
    <aside class="sidebar" :class="{ 'is-collapsed': isCollapsed }">
      <div class="sidebar-header">
        <h2 v-if="!isCollapsed">Hive Chat</h2>
        <button @click="toggleSidebar" class="toggle-btn collapse-btn">‹</button>
      </div>
      <div class="user-profile-summary">
        <span class="username">{{ currentUser?.username }}</span>
        <span class="xp-level">XP: {{ totalXp }} | Level: {{ level }}</span>
      </div>
      <nav class="user-list">
        <h3>Users ({{ chatStore.users.length }})</h3>
        <ul>
          <li v-for="user in chatStore.users" :key="user.id" class="user-item">
            <span class="user-color-dot" :style="{ backgroundColor: user.color }"></span>
            <span :style="{ fontWeight: user.id === currentUser?.id ? 'bold' : 'normal' }">
              {{ user.username }}
            </span>
          </li>
        </ul>
      </nav>
      <nav class="main-nav">
        <RouterLink to="/">Chat</RouterLink>
        <RouterLink to="/playground">Playground</RouterLink>
        <RouterLink to="/journey">Journey</RouterLink>
      </nav>
      <div class="sidebar-footer">
        <div class="lang-switcher">
          <button @click="chatStore.setLanguage('en')" :class="{ active: language === 'en' }">EN</button>
          <button @click="chatStore.setLanguage('ru')" :class="{ active: language === 'ru' }">RU</button>
        </div>
        <button @click="chatStore.toggleTheme" class="theme-toggle-btn">
          {{ theme === 'light' ? 'Dark' : 'Light' }} Mode
        </button>
      </div>
    </aside>
    <main class="main-content">
      <button @click="toggleSidebar" class="toggle-btn open-btn" v-if="isCollapsed">›</button>
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  height: 100vh;
  background-color: var(--color-background);
}

.sidebar {
  width: 250px;
  background-color: var(--color-background-soft);
  padding: 1.5rem;
  border-right: 1px solid var(--color-border);
  transition: all 0.3s ease;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.sidebar.is-collapsed {
  width: 0;
  padding-left: 0;
  padding-right: 0;
}

.sidebar.is-collapsed .sidebar-header,
.sidebar.is-collapsed nav {
  visibility: hidden;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  transition: all 0.3s ease;
}

.sidebar h2 {
  color: var(--color-heading);
  margin: 0;
  white-space: nowrap; /* Prevent title from wrapping during collapse */
}

.user-profile-summary {
  background-color: var(--color-background-mute);
  padding: 0.75rem 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.user-profile-summary .username {
  font-weight: bold;
  color: var(--color-heading);
}

.user-profile-summary .xp-level {
  font-size: 0.8rem;
  color: var(--color-text-mute);
}

.user-list h3 {
  margin-top: 1rem;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: var(--color-text-mute);
  text-transform: uppercase;
}

.user-list ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.user-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1rem;
  white-space: nowrap;
}

.user-color-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
}

.main-nav {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 1.5rem;
}

.main-nav a {
  color: var(--color-text);
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  transition: background-color 0.2s ease;
}

.main-nav a:hover {
  background-color: var(--color-background-mute);
}

.main-nav a.router-link-exact-active {
  background-color: #007bff;
  color: white;
}

.sidebar-footer {
  margin-top: auto; /* Pushes the footer to the bottom */
  padding-top: 1rem;
  border-top: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.lang-switcher {
  display: flex;
  width: 100%;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  overflow: hidden;
}

.lang-switcher button {
  flex: 1;
  padding: 0.5rem;
  border: none;
  background-color: var(--color-background-mute);
  color: var(--color-text-mute);
  cursor: pointer;
  transition: all 0.2s ease;
}

.lang-switcher button:hover {
  background-color: var(--color-background-soft);
}

.lang-switcher button.active {
  background-color: #007bff;
  color: white;
}

.theme-toggle-btn {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background-color: var(--color-background-mute);
  color: var(--color-text);
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.theme-toggle-btn:hover {
  border-color: var(--color-border-hover);
  background-color: var(--color-background-soft);
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  position: relative;
}

.toggle-btn {
  background: var(--color-background-mute);
  border: 1px solid var(--color-border);
  color: var(--color-text);
  border-radius: 50%;
  width: 32px;
  height: 32px;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.5rem;
  line-height: 1;
  flex-shrink: 0;
}

.toggle-btn:hover {
  background: var(--color-background-soft);
  border-color: var(--color-border-hover);
}

.collapse-btn {
  /* Hide the collapse button when sidebar is collapsed */
  transition: opacity 0.1s ease;
}

.sidebar.is-collapsed .collapse-btn {
  opacity: 0;
  z-index: -1; /* Force the button behind other content during transition */
}

.open-btn {
  position: absolute;
  top: 1.5rem;
  left: 1.5rem;
  z-index: 10;
}
</style>
