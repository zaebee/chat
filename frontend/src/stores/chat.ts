
import { defineStore } from 'pinia'
import { ref } from 'vue'

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

  let socket: WebSocket | null = null

  // --- ACTIONS ---

  /**
   * Sets the application language.
   */
  function setLanguage(lang: string) {
    language.value = lang
    localStorage.setItem('hive-chat-language', lang)
  }

  /**
   * Toggles the color theme between light and dark.
   */
  function toggleTheme() {
    theme.value = theme.value === 'light' ? 'dark' : 'light'
    localStorage.setItem('hive-chat-theme', theme.value)
  }

  /**
   * Connects to the WebSocket server.
   */
  function connect(username: string) {
    if (socket || isConnected.value) return

    // Clear old data
    messages.value = []
    users.value = []
    currentUser.value = null

    const url = `wss://${window.location.host}/ws?username=${encodeURIComponent(username)}`
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
          currentUser.value = data.find((user: User) => user.username === username) || null
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
  function login(username: string) {
    localStorage.setItem('hive-chat-username', username)
    connect(username)
  }

  /**
   * Checks localStorage for a username and connects if found.
   */
  function init() {
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

    // Check for saved username
    const savedUsername = localStorage.getItem('hive-chat-username')
    if (savedUsername) {
      connect(savedUsername)
    }
  }

  /**
   * Sends a message over the WebSocket.
   */
  function sendMessage(text: string) {
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
    connect,
    sendMessage,
    login,
    init,
    toggleTheme,
    setLanguage,
  }
})
