import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// Helper to generate a UUID
function generateUUID(): string {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
    const r = (Math.random() * 16) | 0,
      v = c === 'x' ? r : (r & 0x3) | 0x8
    return v.toString(16)
  })
}

// Define the types for our state
export interface User {
  id: string
  username: string
  color: string
}

export interface HiveTeammate {
  id: string
  name: string
  type: string
  status: string
  capabilities: string[]
  active_tasks: number
  health: string
}

export interface Room {
  id: string
  name: string
  description: string
  type: string
  created_by: string
  created_at: string
  is_archived: boolean
}

export type OrganellaType = 'worker' | 'scout' | 'guard' | 'queen'
export type OrganellaStage = 'egg' | 'larva' | 'pupa' | 'adult'

export interface Organella {
  id: string
  name: string
  type: OrganellaType
  stage: OrganellaStage
  level: number
  experience_points: number
  skills: {
    [key: string]: {
      name: string
      level: number
      max_level: number
    }
  }
  personality_traits: {
    [key: string]: number
  }
  description: string
  mystical_appearance: string
  sacred_skills: Record<string, string>
  unlocked_sections: string[]
}

export interface TaleChapter {
  id: string
  chapter_number: number
  title: string
  content: string
  organella_involved: string | null
  challenge_trigger: string | null
  unlocked_at: string
  chapter_type: 'birth' | 'milestone' | 'evolution' | 'discovery' | 'triumph' | 'collaboration'
  mood: string
}

export interface Message {
  id: string
  text: string
  sender_id: string
  sender_name: string
  timestamp: string
  room_id?: string
  parent_id?: string
  is_bot?: boolean
  code_content?: string
  code_language?: string
  editor_id?: string
  hero_properties?: {
    skinColor?: string
    shirtColor?: string
    swordBladeColor?: string
    swordGuardColor?: string
    strokeColor?: string
    size?: number
    animateSwing?: boolean
  }
  dialogue_text?: string
  isPeaking?: boolean // Temporary for testing "Peak" effect
  isDecaying?: boolean // Temporary for testing "Decay" effect
  bee_organella_type?: 'worker' | 'scout' | 'queen' | 'guard'
}

export const useChatStore = defineStore('chat', () => {
  // --- STATE ---
  const users = ref<User[]>([])
  const messages = ref<Message[]>([])
  const teammates = ref<HiveTeammate[]>([])
  const rooms = ref<Room[]>([])
  const organellas = ref<Organella[]>([])
  const tales = ref<TaleChapter[]>([])
  const currentRoom = ref<string>('general')
  const isConnected = ref(false)
  const currentUser = ref<User | null>(null)
  const theme = ref('light')
  const language = ref('en')
  const solvedChallenges = ref<string[]>([])
  const inputPrompt = ref<string | null>(null)
  const inputResolver = ref<((value: string) => void) | null>(null)
  const isAiThinking = ref(false)
  const replyToMessageId = ref<string | null>(null)

  // Gamification constants
  const XP_PER_CHALLENGE = 100
  const XP_FOR_LEVEL_UP = 500 // Example: 500 XP to level up

  // Computed properties for gamification
  const totalXp = computed(() => {
    return solvedChallenges.value.length * XP_PER_CHALLENGE
  })

  const level = computed(() => {
    return Math.floor(totalXp.value / XP_FOR_LEVEL_UP) + 1
  })

  let socket: WebSocket | null = null

  // --- ACTIONS ---

  /**
   * Sends input to a waiting Python script.
   */
  const sendPythonInput = (text: string) => {
    if (inputResolver.value) {
      inputResolver.value(text)
      inputPrompt.value = null
      inputResolver.value = null
    } else {
      console.warn('No Python input requested.')
    }
  }

  /**
   * Adds a Python output message to the chat.
   */
  const addPythonOutputMessage = (text: string) => {
    const message: Message = {
      id: generateUUID(),
      text: text,
      sender_id: 'python_runtime',
      sender_name: 'Python',
      timestamp: new Date().toISOString(),
      is_bot: true,
    }
    messages.value.push(message)
  }

  /**
   * Requests Python input from the user.
   */
  const requestPythonInput = (prompt: string, resolve: (value: string) => void) => {
    inputPrompt.value = prompt
    inputResolver.value = resolve
  }

  /**
   * Sets the application language.
   */
  const setLanguage = (lang: string) => {
    language.value = lang
    localStorage.setItem('hive-chat-language', lang)
  }

  /**
   * Toggles the color theme between light and dark.
   */
  const toggleTheme = () => {
    theme.value = theme.value === 'light' ? 'dark' : 'light'
    localStorage.setItem('hive-chat-theme', theme.value)
  }

  /**
   * Fetches solved challenges for the current user.
   */
  const fetchSolvedChallenges = async (userId: string) => {
    try {
      const response = await fetch(`/api/user_progress/${userId}`)
      if (response.ok) {
        const data = await response.json()
        solvedChallenges.value = data.solved_challenge_ids
      } else {
        console.error('Failed to fetch solved challenges', response.statusText)
      }
    } catch (error) {
      console.error('Error fetching solved challenges:', error)
    }
  }

  /**
   * Fetches user's organellas from the backend.
   */
  const fetchOrganellas = async (userId: string) => {
    try {
      const response = await fetch(`/api/organellas/${userId}`)
      if (response.ok) {
        const data = await response.json()
        organellas.value = data.organellas || []
      } else {
        console.error('Failed to fetch organellas', response.statusText)
      }
    } catch (error) {
      console.error('Error fetching organellas:', error)
    }
  }

  /**
   * Fetches user's tale chapters from the backend.
   */
  const fetchTales = async (userId: string) => {
    try {
      const response = await fetch(`/api/tales/${userId}`)
      if (response.ok) {
        const data = await response.json()
        tales.value = data.tales || []
      } else {
        console.error('Failed to fetch tales', response.statusText)
      }
    } catch (error) {
      console.error('Error fetching tales:', error)
    }
  }

  /**
   * Creates a new organella for the user.
   */
  const createOrganella = async (
    type: 'worker' | 'scout' | 'guard' | 'queen',
    userName: string,
  ) => {
    if (!currentUser.value) {
      console.error('Cannot create organella: user not logged in.')
      return
    }

    try {
      const response = await fetch(`/api/organellas/${currentUser.value.id}/create`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          type: type,
          user_name: userName,
        }),
      })

      if (response.ok) {
        const data = await response.json()
        console.log('Organella created:', data.organella)
        // Refresh organellas and tales
        await fetchOrganellas(currentUser.value.id)
        await fetchTales(currentUser.value.id)
        return data.organella
      } else {
        console.error('Failed to create organella', response.statusText)
      }
    } catch (error) {
      console.error('Error creating organella:', error)
    }
  }

  /**
   * Records a solved challenge for the current user.
   */
  const recordChallengeSolved = async (challengeId: string) => {
    if (!currentUser.value) {
      console.error('Cannot record solved challenge: user not logged in.')
      return
    }
    if (solvedChallenges.value.includes(challengeId)) {
      console.log(`Challenge ${challengeId} already solved by ${currentUser.value.username}`)
      return
    }

    try {
      const response = await fetch('/solve_challenge', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: currentUser.value.id,
          challenge_id: challengeId,
        }),
      })

      if (response.ok) {
        const data = await response.json()
        console.log(data.message)
        solvedChallenges.value.push(challengeId) // Optimistically update UI

        // Refresh organellas and tales after challenge completion
        if (currentUser.value) {
          await fetchOrganellas(currentUser.value.id)
          await fetchTales(currentUser.value.id)
        }
      } else {
        console.error('Failed to record challenge solution', response.statusText)
      }
    } catch (error) {
      console.error('Error recording challenge solution:', error)
    }
  }

  /**
   * Connects to the WebSocket server.
   */
  const connect = (username: string, userId: string) => {
    if (socket || isConnected.value) return

    // Clear old data
    messages.value = []
    users.value = []
    currentUser.value = null

    const url = `wss://${window.location.host}/ws?username=${encodeURIComponent(username)}&user_id=${encodeURIComponent(userId)}`
    socket = new WebSocket(url)

    socket.onopen = () => {
      isConnected.value = true
      console.log('WebSocket connected')
    }

    socket.onmessage = (event) => {
      const response = JSON.parse(event.data)
      const { type, data } = response

      switch (type) {
        case 'message':
          messages.value.push(data)
          break
        case 'user_list':
          users.value = data
          // Now that we have the user list, find the current user
          currentUser.value = data.find((user: User) => user.id === userId) || null
          // Fetch solved challenges, organellas, and tales for the current user
          if (currentUser.value) {
            fetchSolvedChallenges(currentUser.value.id)
            fetchOrganellas(currentUser.value.id)
            fetchTales(currentUser.value.id)
          }
          break
        case 'user_joined':
          users.value.push(data)
          break
        case 'user_departed':
          users.value = users.value.filter((user) => user.id !== data.id)
          break
        case 'rooms':
          rooms.value = data
          break
        case 'room_switched':
          currentRoom.value = data.room_id
          messages.value = data.messages || []
          break
      }
    }

    socket.onclose = () => {
      isConnected.value = false
      socket = null
      console.log('WebSocket disconnected')
    }

    socket.onerror = (error) => {
      console.error('WebSocket error:', error)
      isConnected.value = false
      socket = null
    }
  }

  /**
   * Saves username and connects.
   */
  const login = (username: string) => {
    let userId = localStorage.getItem('hive-chat-user-id')
    if (!userId) {
      userId = generateUUID()
      localStorage.setItem('hive-chat-user-id', userId)
    }
    localStorage.setItem('hive-chat-username', username)
    connect(username, userId)
  }

  /**
   * Checks localStorage for a username and connects if found.
   */
  const init = () => {
    // Check for saved language
    const savedLang = localStorage.getItem('hive-chat-language')
    if (savedLang) {
      language.value = savedLang
    }

    // Check for saved theme
    const savedTheme = localStorage.getItem('hive-chat-theme')
    if (savedTheme) {
      theme.value = savedTheme
    }

    // Check for saved username and user ID
    const savedUsername = localStorage.getItem('hive-chat-username')
    const savedUserId = localStorage.getItem('hive-chat-user-id')

    if (savedUsername && savedUserId) {
      connect(savedUsername, savedUserId)
    }
  }

  /**
   * Sends a message over the WebSocket.
   */
  const sendMessage = (text: string, parentId: string | null = null) => {
    if (socket && isConnected.value) {
      const message = {
        type: 'message',
        data: { text, parent_id: parentId },
      }
      socket.send(JSON.stringify(message))
    } else {
      console.error('Cannot send message, WebSocket is not connected.')
    }
  }

  const setReplyToMessageId = (id: string | null) => {
    replyToMessageId.value = id
  }

  const fetchTeammates = async () => {
    try {
      const response = await fetch('/api/hive/teammates')
      if (response.ok) {
        const data = await response.json()
        teammates.value = data.teammates || []
      } else {
        console.warn('Failed to fetch teammates:', response.statusText)
      }
    } catch (error) {
      console.error('Error fetching teammates:', error)
    }
  }

  const fetchRooms = async () => {
    try {
      const response = await fetch('/api/rooms')
      if (response.ok) {
        const data = await response.json()
        rooms.value = data.rooms || []
      } else {
        console.warn('Failed to fetch rooms:', response.statusText)
      }
    } catch (error) {
      console.error('Error fetching rooms:', error)
    }
  }

  const switchRoom = (roomId: string) => {
    if (socket && isConnected.value) {
      currentRoom.value = roomId
      messages.value = [] // Clear current messages

      // Send room switch message to server
      socket.send(
        JSON.stringify({
          type: 'switch_room',
          data: { room_id: roomId },
        }),
      )
    }
  }

  // const setBackgroundTheme = (themeName: string) => { backgroundTheme.value = backgroundTheme.value = themeName }

  const processCommand = (command: string) => {
    const parts = command.split('.')
    if (parts.length >= 2 && parts[0] === 'bee') {
      const beeType = parts[1] // e.g., 'queen', 'worker'
      // For now, let's just spawn a bee of that type
      messages.value.push({
        id: generateUUID(),
        text: '',
        sender_id: 'system',
        sender_name: 'System',
        timestamp: new Date().toISOString(),
        is_bot: true,
        bee_organella_type: beeType as any, // Cast to any for now, will refine type later
        dialogue_text: `A ${beeType} bee organella has been born!`,
      })
    } else {
      messages.value.push({
        id: generateUUID(),
        text: `Unknown command: ${command}`,
        sender_id: 'system',
        sender_name: 'System',
        timestamp: new Date().toISOString(),
        is_bot: true,
      })
    }
  }

  const loadScene = (sceneName: string) => {
    // Clear existing messages for a fresh scene
    messages.value = []

    switch (sceneName) {
      case 'forest_clearing':
        // Set background
        // setBackgroundTheme('forest');

        // Spawn a hero with dialogue
        messages.value.push({
          id: generateUUID(),
          text: '',
          sender_id: 'game_master',
          sender_name: 'Game Master',
          timestamp: new Date().toISOString(),
          is_bot: true,
          hero_properties: {
            skinColor: '#f0cfb0',
            shirtColor: '#2b6cb0',
            swordBladeColor: '#e6eef6',
            swordGuardColor: '#b8860b',
            strokeColor: '#222',
            size: 1.2,
            animateSwing: true,
          },
          dialogue_text:
            'Welcome, brave adventurer, to the Forest Clearing! A new quest awaits you.',
        })

        // Spawn some worker bees
        messages.value.push({
          id: generateUUID(),
          text: '',
          sender_id: 'worker_bee_1',
          sender_name: 'Worker Bee',
          timestamp: new Date().toISOString(),
          is_bot: true,
          bee_organella_type: 'worker',
          dialogue_text: 'Buzzing with energy, ready to work!',
        })
        messages.value.push({
          id: generateUUID(),
          text: '',
          sender_id: 'worker_bee_2',
          sender_name: 'Worker Bee',
          timestamp: new Date().toISOString(),
          is_bot: true,
          bee_organella_type: 'worker',
          dialogue_text: 'Collecting pollen for the Hive!',
        })
        break
      case 'mountain_pass':
        // Set background
        // setBackgroundTheme('mountains');

        // Spawn a scout bee with dialogue
        messages.value.push({
          id: generateUUID(),
          text: '',
          sender_id: 'scout_bee_1',
          sender_name: 'Scout Bee',
          timestamp: new Date().toISOString(),
          is_bot: true,
          bee_organella_type: 'scout',
          dialogue_text: 'The path ahead is treacherous, but the view is grand!',
        })
        break
      default:
        // Default scene (e.g., clear background, no special characters)
        // setBackgroundTheme('default');
        messages.value.push({
          id: generateUUID(),
          text: 'The ocean is calm. What will emerge next?',
          sender_id: 'system',
          sender_name: 'System',
          timestamp: new Date().toISOString(),
          is_bot: true,
        })
        break
    }
  }

  return {
    users,
    messages,
    teammates,
    rooms,
    organellas,
    tales,
    currentRoom,
    isConnected,
    currentUser,
    theme,
    language,
    solvedChallenges,
    connect,
    sendMessage,
    login,
    init,
    toggleTheme,
    setLanguage,
    recordChallengeSolved,
    fetchSolvedChallenges,
    fetchOrganellas,
    fetchTales,
    createOrganella,
    fetchTeammates,
    fetchRooms,
    switchRoom,
    totalXp,
    level,
    inputPrompt,
    sendPythonInput,
    addPythonOutputMessage,
    requestPythonInput,
    isAiThinking,
    replyToMessageId,
    setReplyToMessageId,
    // backgroundTheme,
    // setBackgroundTheme,
    processCommand,
    loadScene,
  }
})
