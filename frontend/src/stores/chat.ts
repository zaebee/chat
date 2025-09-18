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

export interface Message {
  id: string
  text: string
  sender_id: string
  sender_name: string
  timestamp: string
  is_bot?: boolean
}

export const useChatStore = defineStore('chat', () => {
  // --- STATE ---
  const users = ref<User[]>([])
  const messages = ref<Message[]>([])
  const isConnected = ref(false)
  const currentUser = ref<User | null>(null)
  const theme = ref('light')
  const language = ref('en')
  const solvedChallenges = ref<string[]>([])
  const inputPrompt = ref<string | null>(null)
  const inputResolver = ref<((value: string) => void) | null>(null)

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
      is_bot: true
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
          // Fetch solved challenges for the current user
          if (currentUser.value) {
            fetchSolvedChallenges(currentUser.value.id)
          }
          break
        case 'user_joined':
          users.value.push(data)
          break
        case 'user_left':
          users.value = users.value.filter((user) => user.id !== data.id)
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
  const sendMessage = (text: string) => {
    if (socket && isConnected.value) {
      const message = {
        type: 'message',
        data: { text },
      }
      socket.send(JSON.stringify(message))
    } else {
      console.error('Cannot send message, WebSocket is not connected.')
    }
  }

  return {
    users,
    messages,
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
    totalXp,
    level,
    inputPrompt,
    sendPythonInput,
    addPythonOutputMessage,
    requestPythonInput,
  }
})
