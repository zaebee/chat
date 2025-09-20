/**
 * User Store - Manages user authentication and profile
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface User {
  id: string
  username: string
  email?: string
  color: string
  level: number
  experience: number
  joinedAt: string
  lastActive: string
  preferences: {
    theme: 'light' | 'dark'
    language: string
    notifications: boolean
  }
  stats: {
    challengesCompleted: number
    totalXP: number
    streak: number
    organellasCreated: number
  }
}

export const useUserStore = defineStore('user', () => {
  // State
  const currentUser = ref<User | null>(null)
  const isAuthenticated = ref(false)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const userLevel = computed(() => currentUser.value?.level || 1)
  const userExperience = computed(() => currentUser.value?.experience || 0)
  const userStats = computed(() => currentUser.value?.stats || {
    challengesCompleted: 0,
    totalXP: 0,
    streak: 0,
    organellasCreated: 0
  })

  // Actions
  async function login(username: string, password?: string) {
    loading.value = true
    error.value = null
    
    try {
      // For POC, create a mock user
      // In real implementation, this would authenticate with API
      const mockUser: User = {
        id: Date.now().toString(),
        username,
        color: `#${Math.floor(Math.random()*16777215).toString(16)}`,
        level: 1,
        experience: 0,
        joinedAt: new Date().toISOString(),
        lastActive: new Date().toISOString(),
        preferences: {
          theme: 'light',
          language: 'en',
          notifications: true
        },
        stats: {
          challengesCompleted: 0,
          totalXP: 0,
          streak: 0,
          organellasCreated: 0
        }
      }
      
      currentUser.value = mockUser
      isAuthenticated.value = true
      
      // Store in localStorage for persistence
      localStorage.setItem('hive_user', JSON.stringify(mockUser))
      
      return mockUser
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Login failed'
      console.error('Login error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    currentUser.value = null
    isAuthenticated.value = false
    localStorage.removeItem('hive_user')
  }

  async function loadUserFromStorage() {
    try {
      const stored = localStorage.getItem('hive_user')
      if (stored) {
        const user = JSON.parse(stored)
        currentUser.value = user
        isAuthenticated.value = true
      }
    } catch (err) {
      console.error('Error loading user from storage:', err)
      localStorage.removeItem('hive_user')
    }
  }

  async function updateUser(updates: Partial<User>) {
    if (!currentUser.value) return
    
    loading.value = true
    error.value = null
    
    try {
      currentUser.value = { ...currentUser.value, ...updates }
      
      // Update localStorage
      localStorage.setItem('hive_user', JSON.stringify(currentUser.value))
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to update user'
      console.error('Error updating user:', err)
    } finally {
      loading.value = false
    }
  }

  async function addExperience(xp: number) {
    if (!currentUser.value) return
    
    const newXP = currentUser.value.experience + xp
    const newLevel = Math.floor(newXP / 100) + 1
    
    await updateUser({
      experience: newXP,
      level: newLevel,
      stats: {
        ...currentUser.value.stats,
        totalXP: newXP
      }
    })
  }

  async function completeChallenge(xp: number = 50) {
    if (!currentUser.value) return
    
    await addExperience(xp)
    await updateUser({
      stats: {
        ...currentUser.value.stats,
        challengesCompleted: currentUser.value.stats.challengesCompleted + 1
      }
    })
  }

  function clearError() {
    error.value = null
  }

  // Initialize user from storage on store creation
  loadUserFromStorage()

  return {
    // State
    currentUser,
    isAuthenticated,
    loading,
    error,
    
    // Getters
    userLevel,
    userExperience,
    userStats,
    
    // Actions
    login,
    logout,
    loadUserFromStorage,
    updateUser,
    addExperience,
    completeChallenge,
    clearError
  }
})