import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useSettingsStore = defineStore('settings', () => {
  // --- STATE ---
  const theme = ref<'light' | 'dark'>('light');
  const language = ref<'en' | 'ru'>('en');

  // --- ACTIONS ---

  /**
   * Sets the application language.
   */
  const setLanguage = (lang: 'en' | 'ru') => {
    language.value = lang;
    localStorage.setItem('hive-chat-language', lang);
  };

  /**
   * Toggles the color theme between light and dark.
   */
  const toggleTheme = () => {
    theme.value = theme.value === 'light' ? 'dark' : 'light';
    localStorage.setItem('hive-chat-theme', theme.value);
  };

  /**
   * Initializes settings from localStorage.
   */
  const initSettings = () => {
    const savedLang = localStorage.getItem('hive-chat-language');
    if (savedLang === 'en' || savedLang === 'ru') {
      language.value = savedLang;
    }

    const savedTheme = localStorage.getItem('hive-chat-theme');
    if (savedTheme === 'light' || savedTheme === 'dark') {
      theme.value = savedTheme;
    }
  };

  return {
    theme,
    language,
    setLanguage,
    toggleTheme,
    initSettings,
  };
});
