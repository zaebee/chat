/**
 * Organellas Store - Manages bee companions in the Hive ecosystem
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface Organella {
  id: string
  name: string
  type: string
  level: number
  userId: string
  traits: string[]
  createdAt: string
  lastActive: string
  experience: number
  specialization: string
}

export interface OrganellaCreationData {
  name: string
  type: string
  level: number
  traits: string[]
  specialization: string
}

export const useOrganellasStore = defineStore('organellas', () => {
  // State
  const organellas = ref<Organella[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const organellasByLevel = computed(() => {
    const grouped: Record<number, Organella[]> = {}
    organellas.value.forEach(organella => {
      if (!grouped[organella.level]) {
        grouped[organella.level] = []
      }
      grouped[organella.level].push(organella)
    })
    return grouped
  })

  const totalOrganellas = computed(() => organellas.value.length)

  // Actions
  async function fetchOrganellas(userId: string) {
    loading.value = true
    error.value = null
    
    try {
      // For POC, return mock data
      // In real implementation, this would fetch from API
      organellas.value = [
        {
          id: '1',
          name: 'Buzzy',
          type: 'Worker Bee',
          level: 1,
          userId,
          traits: ['Curious', 'Helpful'],
          createdAt: new Date().toISOString(),
          lastActive: new Date().toISOString(),
          experience: 100,
          specialization: 'Python Basics'
        },
        {
          id: '2',
          name: 'Honey',
          type: 'Scout Bee',
          level: 2,
          userId,
          traits: ['Adventurous', 'Quick'],
          createdAt: new Date().toISOString(),
          lastActive: new Date().toISOString(),
          experience: 250,
          specialization: 'Code Review'
        }
      ]
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch organellas'
      console.error('Error fetching organellas:', err)
    } finally {
      loading.value = false
    }
  }

  async function createOrganella(userId: string, data: OrganellaCreationData): Promise<Organella> {
    loading.value = true
    error.value = null
    
    try {
      // For POC, create mock organella
      // In real implementation, this would POST to API
      const newOrganella: Organella = {
        id: Date.now().toString(),
        userId,
        createdAt: new Date().toISOString(),
        lastActive: new Date().toISOString(),
        experience: 0,
        ...data
      }
      
      organellas.value.push(newOrganella)
      return newOrganella
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to create organella'
      console.error('Error creating organella:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateOrganella(id: string, updates: Partial<Organella>) {
    loading.value = true
    error.value = null
    
    try {
      const index = organellas.value.findIndex(o => o.id === id)
      if (index !== -1) {
        organellas.value[index] = { ...organellas.value[index], ...updates }
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to update organella'
      console.error('Error updating organella:', err)
    } finally {
      loading.value = false
    }
  }

  async function deleteOrganella(id: string) {
    loading.value = true
    error.value = null
    
    try {
      const index = organellas.value.findIndex(o => o.id === id)
      if (index !== -1) {
        organellas.value.splice(index, 1)
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to delete organella'
      console.error('Error deleting organella:', err)
    } finally {
      loading.value = false
    }
  }

  function clearError() {
    error.value = null
  }

  return {
    // State
    organellas,
    loading,
    error,
    
    // Getters
    organellasByLevel,
    totalOrganellas,
    
    // Actions
    fetchOrganellas,
    createOrganella,
    updateOrganella,
    deleteOrganella,
    clearError
  }
})