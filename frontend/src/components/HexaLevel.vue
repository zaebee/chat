<template>
  <g class="hexa-level" @click="selectLevel">
    <polygon :class="hexClass" :points="points" />
    <text :x="x" :y="y - 15" class="label title">{{ title }}</text>
    <text :x="x" :y="y + 10" class="label cap">{{ subtitle }}</text>
    <g v-if="organellas.length > 0" class="organellas">
      <image
        v-for="(organella, index) in organellas"
        :key="organella.id"
        :x="x - 20 + index * 20"
        :y="y + 20"
        width="20"
        height="20"
        :href="getOrganellaIcon(organella.type, organella.stage)"
      />
    </g>
  </g>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useChatStore, type Organella, type OrganellaType, type OrganellaStage } from '@/stores/chat'

const props = defineProps<{
  level: number
  title: string
  subtitle: string
  points: string
  x: number
  y: number
  organellas: Organella[]
}>()

const chatStore = useChatStore()

const hexClass = computed(() => {
  let classes = 'hex'
  if (props.level === chatStore.level) {
    classes += ' current-level'
  } else if (props.level < chatStore.level) {
    classes += ' solved-level'
  } else {
    classes += ' locked-level'
  }
  return classes
})

const selectLevel = () => {
  // TODO: Implement level selection logic
  console.log(`Selected level ${props.level}`)
}

const getOrganellaIcon = (type: OrganellaType, stage: OrganellaStage) => {
  const icons: Record<OrganellaType, Record<OrganellaStage, string>> = {
    worker: { egg: '🥚', larva: '🐛', pupa: '🛡️', adult: '🐝' },
    scout: { egg: '🥚', larva: '🐛', pupa: '🛡️', adult: '🔍' },
    guard: { egg: '🥚', larva: '🐛', pupa: '🛡️', adult: '🛡️' },
    queen: { egg: '🥚', larva: '🐛', pupa: '🛡️', adult: '👑' },
  }
  return `data:image/svg+xml,${encodeURIComponent(
    `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20"><text x="0" y="15">${
      icons[type]?.[stage] || '🐝'
    }</text></svg>`
  )}`
}
</script>

<style scoped>
.hexa-level {
  cursor: pointer;
  transition: all 0.3s ease;
}

.hexa-level:hover {
  transform: scale(1.05);
}
</style>
