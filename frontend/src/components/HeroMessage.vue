<script setup lang="ts">
import SvgHero from "./SvgHero.vue";

const { heroProperties, dialogueText } = defineProps<{
  heroProperties: {
    skinColor?: string;
    shirtColor?: string;
    swordBladeColor?: string;
    swordGuardColor?: string;
    strokeColor?: string;
    size?: number;
    animateSwing?: boolean;
  };
  dialogueText: string;
}>();
</script>

<template>
  <div class="hero-message-container">
    <div class="hero-avatar">
      <SvgHero
        :skin-color="heroProperties.skinColor"
        :shirt-color="heroProperties.shirtColor"
        :sword-blade-color="heroProperties.swordBladeColor"
        :sword-guard-color="heroProperties.swordGuardColor"
        :stroke-color="heroProperties.strokeColor"
        :size="heroProperties.size"
        :animate-swing="heroProperties.animateSwing"
      />
    </div>
    <div class="hero-dialogue-bubble">
      <p>{{ dialogueText }}</p>
    </div>
  </div>
</template>

<style scoped>
.hero-message-container {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1rem;
}
.hero-avatar {
  flex-shrink: 0;
  width: 80px; /* Adjust size as needed */
  height: 104px; /* Adjust size as needed */
  overflow: hidden;
}

.hero-dialogue-bubble {
  background-color: var(--color-background-soft);
  padding: 0.75rem 1rem;
  border-radius: 12px;
  position: relative;
  flex-grow: 1;
  color: var(--color-text);
}

.hero-dialogue-bubble::before {
  content: "";
  position: absolute;
  left: -10px; /* Position the triangle */
  top: 15px;
  width: 0;
  height: 0;
  border-top: 10px solid transparent;
  border-bottom: 10px solid transparent;
  border-right: 10px solid var(--color-background-soft); /* Color of the bubble */
}

.hero-dialogue-bubble p {
  margin: 0;
}
</style>