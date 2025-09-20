<template>
  <div class="organella-panel">
    <ChroniclerBonusEffect :start="showBoonAnimation" />
    <div class="panel-header">
      <h3>🐝 My Organellas</h3>
      <button @click="toggleExpanded" class="toggle-btn">
        {{ isExpanded ? "−" : "+" }}
      </button>
    </div>

    <div v-if="isExpanded" class="panel-content">
      <div v-if="organellas.length === 0" class="no-organellas">
        <p>No organellas yet! Complete challenges to attract your first bee companion.</p>
        <button @click="createNewOrganella" class="create-btn">Create First Organella</button>
      </div>

      <div v-else class="organellas-list">
        <div
          v-for="organella in organellas"
          :key="organella.id"
          class="organella-card"
          :class="`type-${organella.type} stage-${organella.stage}`"
        >
          <OrganellaEvolutionCeremony :start="evolvingOrganellaId === organella.id" />
          <div class="organella-header">
            <div class="organella-icon">
              <DigitalBee :bodyColor="getOrganellaColor(organella.type)" />
            </div>
            <div class="organella-info">
              <h4>{{ organella.name }}</h4>
              <span class="organella-type">{{ organella.type }} {{ organella.stage }}</span>
            </div>
            <div class="organella-level">
              <span class="level">Lv. {{ organella.level }}</span>
              <div class="xp-bar">
                <div class="xp-fill" :style="{ width: `${getXpProgress(organella)}%` }"></div>
              </div>
              <span class="xp-text">{{ organella.experience_points }} XP</span>
            </div>
          </div>
          <em class="organella-description">"{{ organella.description }}"</em>

          <div class="organella-body">
            <div class="organella-details">
              <div class="organella-appearance">
                <h5>Professional Appearance</h5>
                <p v-if="isSectionVisible(organella.id, 'appearance')">
                  {{ organella.professional_appearance }}
                </p>
                <div v-else>
                  <button @click="startStudy(organella.id, 'appearance')" class="study-btn">
                    Study
                  </button>
                  <p v-if="isStudying(organella.id, 'appearance')" class="studying-message">
                    Studying... this section will be revealed for 3 minutes.
                  </p>
                </div>
              </div>

              <div class="organella-experience">
                <h5>Experience</h5>
                <div v-if="isSectionVisible(organella.id, 'experience')">
                  <p><strong>Experience Points:</strong> {{ organella.experience_points }}</p>
                  <p><strong>Level:</strong> {{ organella.level }}</p>
                </div>
                <div v-else>
                  <button @click="startStudy(organella.id, 'experience')" class="study-btn">
                    Study
                  </button>
                  <p v-if="isStudying(organella.id, 'experience')" class="studying-message">
                    Studying... this section will be revealed for 3 minutes.
                  </p>
                </div>
              </div>
            </div>

            <div class="organella-skills">
              <h5>Skills:</h5>
              <div class="skills-grid">
              <div
                v-for="(skill, skillName) in organella.skills"
                :key="skillName"
                class="skill-item"
              >
                <span class="skill-name">{{ skill.name }}</span>
                <div class="skill-level-bar-wrapper">
                  <div class="skill-level-bar">
                    <div class="skill-level-fill" :style="{ width: `${(skill.level / skill.max_level) * 100}%` }"></div>
                  </div>
                  <span class="skill-level-text">{{ skill.level }} / {{ skill.max_level }}</span>
                </div>
              </div>              </div>
            </div>

            <div class="organella-personality">
              <h5>Personality:</h5>
              <div v-if="organella.personality_traits && Object.keys(organella.personality_traits).length > 0" class="personality-traits">
                <span
                  v-for="(value, trait) in organella.personality_traits"
                  :key="trait"
                  class="trait"
                  :style="{ opacity: 0.5 + value * 0.5 }"
                >
                  {{ trait }}
                </span>
              </div>
              <div v-else class="no-personality">
                <p>Personality not yet defined.</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Tales Section -->
      <div v-if="tales.length > 0" class="tales-section">
        <h3>📖 fAIry Tales</h3>
        <div class="tales-list">
          <div
            v-for="tale in tales.slice(-3)"
            :key="tale.id"
            class="tale-card"
            :class="`mood-${tale.mood} type-${tale.chapter_type}`"
          >
            <div class="tale-header">
              <h4>{{ tale.title }}</h4>
              <span class="tale-type">{{ tale.chapter_type }}</span>
            </div>
            <p class="tale-content">{{ tale.content }}</p>
            <div class="tale-meta">
              <span class="tale-date">{{ formatDate(tale.unlocked_at) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from "vue";
import {
  useOrganellasStore,
  type Organella,
  type OrganellaType,
  type OrganellaStage,
} from "@/stores/organellas";
import { useTalesStore } from "@/stores/tales";
import { useUserStore } from "@/stores/user";
import { useGameStore } from "@/stores/game";
import { storeToRefs } from "pinia";
import OrganellaEvolutionCeremony from "./OrganellaEvolutionCeremony.vue";
import ChroniclerBonusEffect from "./ChroniclerBonusEffect.vue";
import DigitalBee from "./DigitalBee.vue";

const organellasStore = useOrganellasStore();
const talesStore = useTalesStore();
const userStore = useUserStore();
const gameStore = useGameStore();
const isExpanded = ref(true);

const organellas = computed(() => organellasStore.organellas);
const tales = computed(() => talesStore.tales);
const { totalXp } = storeToRefs(gameStore);

const evolvingOrganellaId = ref<string | null>(null);
const showBoonAnimation = ref(false);

watch(organellas, (newOrganellas, oldOrganellas) => {
  if (!oldOrganellas || oldOrganellas.length === 0) return;

  for (const newOrganella of newOrganellas) {
    const oldOrganella = oldOrganellas.find(o => o.id === newOrganella.id);
    if (oldOrganella && newOrganella.level > oldOrganella.level) {
      evolvingOrganellaId.value = newOrganella.id;
      // Reset after the animation duration to allow re-triggering
      setTimeout(() => {
        if (evolvingOrganellaId.value === newOrganella.id) {
          evolvingOrganellaId.value = null;
        }
      }, 2000);
    }
  }
}, { deep: true });

watch(totalXp, (newXp, oldXp) => {
  if (newXp > oldXp && (newXp - oldXp) === 20) {
    showBoonAnimation.value = true;
    setTimeout(() => {
      showBoonAnimation.value = false;
    }, 2500); // Duration of the boon animation
  }
});

const studying_sections = ref(new Map<string, number>());
const studying_sections_message = ref(new Set<string>());

const startStudy = (organellaId: string, section: string) => {
  const key = `${organellaId}-${section}`;

  // Show studying message
  studying_sections_message.value.add(key);

  // Clear any existing timer for this section
  if (studying_sections.value.has(key)) {
    clearTimeout(studying_sections.value.get(key));
  }

  // Set a new timer to hide the section after 3 minutes
  const timerId = setTimeout(() => {
    studying_sections.value.delete(key);
    studying_sections_message.value.delete(key);
  }, 180000); // 3 minutes

  // Add the section to the studying map
  studying_sections.value.set(key, timerId);
};

const isStudying = (organellaId: string, section: string) => {
  const key = `${organellaId}-${section}`;
  return studying_sections_message.value.has(key) && !studying_sections.value.has(key);
};

const isSectionVisible = (organellaId: string, section: string) => {
  const key = `${organellaId}-${section}`;
  return studying_sections.value.has(key);
};

const toggleExpanded = () => {
  isExpanded.value = !isExpanded.value;
};

const createNewOrganella = async () => {
  if (userStore.currentUser) {
    await organellasStore.createOrganella(userStore.currentUser.id, {
      type: "worker",
      name: `${userStore.currentUser.username}'s Worker`,
    });
  }
};

const getOrganellaColor = (type: OrganellaType) => {
  const colors: Record<OrganellaType, string> = {
    worker: "#fbbf24",
    scout: "#06b6d4",
    guard: "#ef4444",
    queen: "#a855f7",
    chronicler: "#3b82f6",
  };
  return colors[type] || "#6b7280";
};

const getXpProgress = (organella: Organella) => {
  const currentLevelXp = organella.experience_points % 100;
  return (currentLevelXp / 100) * 100;
};

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString();
};
</script>

<style scoped>
.organella-panel {
  position: relative; /* For the bonus effect overlay */
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin: 1rem 0;
  overflow: hidden;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: linear-gradient(135deg, #ffd700, #ffb347);
  color: #333;
}

.panel-header h3 {
  margin: 0;
  font-size: 1.2rem;
}

.toggle-btn {
  background: rgba(255, 255, 255, 0.8);
  border: none;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  cursor: pointer;
  font-size: 1.2rem;
  transition: all 0.3s ease;
}

.toggle-btn:hover {
  background: white;
  transform: scale(1.1);
}

.panel-content {
  padding: 1rem;
}

.no-organellas {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.create-btn {
  background: linear-gradient(135deg, #4ade80, #22c55e);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  margin-top: 1rem;
  transition: all 0.3s ease;
}

.create-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
}

.study-btn {
  background: #4a5568;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  margin-top: 1rem;
  transition: all 0.3s ease;
}

.study-btn:hover {
  background: #2d3748;
}

.studying-message {
  font-size: 0.8rem;
  color: #666;
  margin-top: 0.5rem;
}

.organellas-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

@keyframes organella-born {
  from {
    opacity: 0;
    transform: translateY(10px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.organella-card {
  position: relative; /* Container for the ceremony overlay */
  background: white;
  border-radius: 12px;
  padding: 1rem;
  border: 2px solid #e5e7eb;
  transition: all 0.3s ease;
  animation: organella-born 0.5s ease-out forwards;
}

.organella-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.organella-card.type-worker {
  border-color: #fbbf24;
}
.organella-card.type-scout {
  border-color: #06b6d4;
}
.organella-card.type-guard {
  border-color: #ef4444;
}
.organella-card.type-queen {
  border-color: #a855f7;
}

.organella-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.organella-icon {
  font-size: 2rem;
}

.organella-info h4 {
  margin: 0;
  font-size: 1.1rem;
  color: #333;
}

.organella-type {
  color: #666;
  font-size: 0.9rem;
  text-transform: capitalize;
}

.organella-level {
  margin-left: auto;
  text-align: right;
}

.organella-description {
  font-size: 0.8rem;
  color: #666;
  font-style: italic;
  margin-bottom: 1rem;
}

.organella-body {
  display: grid;
  grid-template-areas:
    "details skills"
    "details personality";
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.organella-details {
  grid-area: details;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.organella-skills {
  grid-area: skills;
}

.organella-personality {
  grid-area: personality;
}

.organella-appearance h5,
.organella-sacred-skills h5 {
  margin: 0.5rem 0;
  font-size: 0.9rem;
  color: #555;
}

.organella-appearance p {
  font-size: 0.9rem;
  color: #666;
}

.organella-sacred-skills ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.organella-sacred-skills li {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.level {
  font-weight: bold;
  color: #333;
  display: block;
}

.xp-bar {
  width: 60px;
  height: 6px;
  background: #e5e7eb;
  border-radius: 3px;
  overflow: hidden;
  margin: 0.25rem 0;
}

.xp-fill {
  height: 100%;
  background: linear-gradient(90deg, #4ade80, #22c55e);
  transition: width 0.3s ease;
}

.xp-text {
  font-size: 0.8rem;
  color: #666;
}

.organella-skills h5,
.organella-personality h5 {
  margin: 0.5rem 0;
  font-size: 0.9rem;
  color: #555;
}

.skills-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.25rem;
}

.skill-item {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.25rem;
}

.skill-level-bar-wrapper {
  display: grid;
  grid-template-columns: 1fr auto;
  align-items: center;
  gap: 0.5rem;
}

.skill-name {
  grid-column: 1 / 3;
}

.skill-level-bar {
  width: 100%;
}

.skill-level-text {
  justify-self: end;

.skill-name {
  font-size: 0.8rem;
  color: #666;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.skill-level-bar {
  width: 100px;
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
}

.skill-level-fill {
  height: 100%;
  background: #4ade80;
  transition: width 0.3s ease;
}

.skill-level-text {
  font-size: 0.7rem;
  color: #666;
  min-width: 50px;
  text-align: right;
}

.personality-traits {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.trait {
  background: rgba(59, 130, 246, 0.1);
  color: #1d4ed8;
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  font-size: 0.8rem;
  text-transform: capitalize;
}

.tales-section {
  margin-top: 2rem;
  border-top: 2px solid #e5e7eb;
  padding-top: 1rem;
}

.tales-section h3 {
  margin: 0 0 1rem 0;
  color: #333;
}

.tales-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.tale-card {
  background: linear-gradient(135deg, #f8fafc, #e2e8f0);
  border-radius: 12px;
  padding: 1rem;
  border-left: 4px solid #3b82f6;
}

.tale-card.mood-mystical {
  border-left-color: #8b5cf6;
}
.tale-card.mood-triumphant {
  border-left-color: #f59e0b;
}
.tale-card.mood-transformative {
  border-left-color: #10b981;
}

.tale-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.tale-header h4 {
  margin: 0;
  color: #333;
  font-size: 1rem;
}

.tale-type {
  background: rgba(59, 130, 246, 0.1);
  color: #1d4ed8;
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  font-size: 0.7rem;
  text-transform: capitalize;
}

.tale-content {
  color: #555;
  font-style: italic;
  line-height: 1.5;
  margin: 0.5rem 0;
}

.tale-meta {
  text-align: right;
}

.tale-date {
  color: #888;
  font-size: 0.8rem;
}

/* Dark theme support */
[data-theme="dark"] .organella-panel {
  background: rgba(17, 24, 39, 0.95);
}

[data-theme="dark"] .organella-card {
  background: #1f2937;
  border-color: #374151;
}

[data-theme="dark"] .organella-info h4,
[data-theme="dark"] .level {
  color: #f3f4f6;
}

[data-theme="dark"] .tale-card {
  background: linear-gradient(135deg, #1f2937, #111827);
}

[data-theme="dark"] .tale-header h4 {
  color: #f3f4f6;
}
</style>
