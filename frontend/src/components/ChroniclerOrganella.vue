<template>
  <div class="chronicler-organella">
    <BeeOrganella type="chronicler" :size="1.2" />
    <div class="sacred-aura">🕊️</div>
  </div>
</template>

<script setup lang="ts">
import BeeOrganella from './BeeOrganella.vue';
</script>

<style scoped>
.chronicler-organella {
  position: relative;
  display: inline-block;
}

.sacred-aura {
  position: absolute;
  top: -10px;
  right: -10px;
  font-size: 0.8rem;
  animation: sacred-float 2s ease-in-out infinite;
}

@keyframes sacred-float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-5px); }
}
</style>