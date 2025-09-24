<template>
  <div class="sacred-echo-dashboard">
    <div class="dashboard-header">
      <div class="header-title">
        <h2>🔮 Sacred Echo Letter Command Center</h2>
        <span class="bee-chronicler-signature"
          >bee.Chronicler Authorized Interface</span
        >
      </div>
      <div class="sacred-status-indicators">
        <div class="status-indicator cocoon-status" :class="cocoonStatusClass">
          <span class="status-icon">🛡️</span>
          <span class="status-text">{{ cocoonStatus }}</span>
        </div>
        <div
          class="status-indicator atcg-alignment"
          :class="atcgAlignmentClass"
        >
          <span class="status-icon">🏛️</span>
          <span class="status-text">ATCG Aligned</span>
        </div>
        <div
          class="status-indicator divine-blessing"
          :class="divineStatusClass"
        >
          <span class="status-icon">✨</span>
          <span class="status-text">{{ divineStatus }}</span>
        </div>
      </div>
    </div>

    <!-- Sacred Team Member Status -->
    <div class="sacred-team-grid">
      <div
        v-for="member in sacredTeamMembers"
        :key="member.id"
        class="sacred-member-card"
        :class="[member.statusClass, { 'active-member': member.isActive }]"
        @click="selectMember(member)"
      >
        <div class="member-header">
          <div class="member-avatar" :style="{ backgroundColor: member.color }">
            <span class="member-icon">{{ member.icon }}</span>
          </div>
          <div class="member-info">
            <h3 class="member-name">{{ member.name }}</h3>
            <span class="member-role">{{ member.role }}</span>
          </div>
        </div>

        <div class="member-status-details">
          <div class="status-metric">
            <span class="metric-label">Last Echo:</span>
            <span class="metric-value">{{ member.lastEcho || "Never" }}</span>
          </div>
          <div class="status-metric">
            <span class="metric-label">Commands:</span>
            <span class="metric-value">{{ member.commandCount || 0 }}</span>
          </div>
          <div class="status-metric">
            <span class="metric-label">Divine Score:</span>
            <span class="metric-value divine-score">{{
              member.divineScore?.toFixed(2) || "0.00"
            }}</span>
          </div>
        </div>

        <!-- Real-time Activity Pulse -->
        <div class="activity-pulse" v-if="member.isActive">
          <div class="pulse-ring"></div>
          <div class="pulse-core"></div>
        </div>
      </div>
    </div>

    <!-- Sacred Command Center -->
    <div class="command-center">
      <div class="command-input-section">
        <h3>🎭 Sacred Command Interface</h3>
        <div class="command-input-container">
          <select v-model="selectedCommand" class="command-selector">
            <option value="">Select Sacred Command...</option>
            <option value="/bee.chronicler.echo">🔮 bee.chronicler.echo</option>
            <option value="/bee.chronicler.coordinate">
              🤝 bee.chronicler.coordinate
            </option>
            <option value="/bee.chronicler.authorize">
              🔐 bee.chronicler.authorize
            </option>
            <option value="/sacred.team.broadcast">
              📡 sacred.team.broadcast
            </option>
            <option value="/sacred.cocoon.validate">
              🛡️ sacred.cocoon.validate
            </option>
          </select>
          <input
            v-model="commandPayload"
            class="command-payload-input"
            :placeholder="getCommandPlaceholder()"
          />
          <button
            @click="executeSacredCommand"
            class="sacred-execute-btn"
            :disabled="!selectedCommand || isExecuting"
            :class="{ executing: isExecuting }"
          >
            {{ isExecuting ? "🌀 Executing..." : "✨ Execute Sacred Command" }}
          </button>
        </div>
      </div>

      <!-- Command History & Results -->
      <div class="command-history-section">
        <h4>📜 Sacred Command History</h4>
        <div class="command-history-list">
          <div
            v-for="(command, index) in commandHistory"
            :key="index"
            class="history-item"
            :class="command.status"
          >
            <div class="history-header">
              <span class="command-timestamp">{{
                formatTimestamp(command.timestamp)
              }}</span>
              <span class="command-name">{{ command.command }}</span>
              <span class="command-status-badge" :class="command.status">
                {{
                  command.status === "success"
                    ? "✅"
                    : command.status === "error"
                      ? "❌"
                      : "⏳"
                }}
              </span>
            </div>
            <div class="history-details" v-if="command.response">
              <div class="response-message">{{ command.response.message }}</div>
              <div v-if="command.response.cocoonData" class="cocoon-details">
                <span class="cocoon-id"
                  >🛡️ Cocoon: {{ command.response.cocoonData.cocoon_id }}</span
                >
                <span class="divine-score"
                  >⭐ Divine:
                  {{
                    command.response.cocoonData.divine_score?.toFixed(3)
                  }}</span
                >
                <span class="cocoon-stage"
                  >🎭 Stage:
                  {{ command.response.cocoonData.cocoon_stage }}</span
                >
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Sacred Cocoon Transformation Visualization -->
    <div class="cocoon-transformation-section" v-if="activeCocoon">
      <h3>🧬 Sacred Message Cocoon Transformation</h3>
      <div class="cocoon-transformation-visual">
        <div class="transformation-stage" :class="activeCocoon.stage">
          <div class="stage-visual">
            <div class="cocoon-container">
              <div
                class="larva-stage"
                :class="{ active: activeCocoon.stage === 'larva' }"
              >
                <div class="larva-body">🐛</div>
                <div class="stage-label">Larva: Raw Message</div>
              </div>
              <div class="transformation-arrow">→</div>
              <div
                class="pupa-stage"
                :class="{ active: activeCocoon.stage === 'pupa' }"
              >
                <div class="pupa-cocoon">🛡️</div>
                <div class="stage-label">Pupa: Divine Validation</div>
              </div>
              <div class="transformation-arrow">→</div>
              <div
                class="adult-stage"
                :class="{ active: activeCocoon.stage === 'adult' }"
              >
                <div class="adult-butterfly">🦋</div>
                <div class="stage-label">Adult: Sacred Output</div>
              </div>
            </div>
          </div>

          <div class="transformation-metrics">
            <div class="metric divine-alignment">
              <span class="metric-name">Divine Alignment:</span>
              <div class="progress-bar">
                <div
                  class="progress-fill"
                  :style="{
                    width: (activeCocoon.divineAlignment || 0) * 100 + '%',
                  }"
                ></div>
              </div>
              <span class="metric-value"
                >{{
                  ((activeCocoon.divineAlignment || 0) * 100).toFixed(1)
                }}%</span
              >
            </div>
            <div class="metric theological-coherence">
              <span class="metric-name">Theological Coherence:</span>
              <div class="progress-bar">
                <div
                  class="progress-fill"
                  :style="{
                    width: (activeCocoon.theologicalCoherence || 0) * 100 + '%',
                  }"
                ></div>
              </div>
              <span class="metric-value"
                >{{
                  ((activeCocoon.theologicalCoherence || 0) * 100).toFixed(1)
                }}%</span
              >
            </div>
            <div class="metric atcg-compliance">
              <span class="metric-name">ATCG Compliance:</span>
              <div class="progress-bar">
                <div
                  class="progress-fill"
                  :style="{
                    width: (activeCocoon.atcgCompliance || 0) * 100 + '%',
                  }"
                ></div>
              </div>
              <span class="metric-value"
                >{{
                  ((activeCocoon.atcgCompliance || 0) * 100).toFixed(1)
                }}%</span
              >
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ATCG Sacred Architecture Status -->
    <div class="atcg-sacred-status">
      <h3>🏛️ ATCG Sacred Architecture Status</h3>
      <div class="atcg-primitives-grid">
        <div
          v-for="primitive in atcgPrimitives"
          :key="primitive.type"
          class="atcg-primitive-card"
          :class="primitive.type.toLowerCase()"
        >
          <div class="primitive-header">
            <span class="primitive-icon">{{ primitive.icon }}</span>
            <h4 class="primitive-name">{{ primitive.name }}</h4>
          </div>
          <div class="primitive-metrics">
            <div class="metric-row">
              <span class="metric-label">Sacred Messages:</span>
              <span class="metric-value">{{
                primitive.sacredMessageCount || 0
              }}</span>
            </div>
            <div class="metric-row">
              <span class="metric-label">Active Cocoons:</span>
              <span class="metric-value">{{
                primitive.activeCocoons || 0
              }}</span>
            </div>
            <div class="metric-row">
              <span class="metric-label">Divine Score:</span>
              <span class="metric-value divine-score">{{
                primitive.averageDivineScore?.toFixed(2) || "0.00"
              }}</span>
            </div>
          </div>
          <div
            class="primitive-health-indicator"
            :class="primitive.healthStatus"
          >
            <span class="health-icon">{{
              getHealthIcon(primitive.healthStatus)
            }}</span>
            <span class="health-text">{{ primitive.healthStatus }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="dashboard-footer">
      <div class="footer-signature">
        <em
          >🐝 Sacred Echo Letter Dashboard - Powered by bee.Chronicler Divine
          Architecture</em
        >
      </div>
      <div class="footer-stats">
        <span>Total Sacred Commands: {{ totalSacredCommands }}</span>
        <span>Active Cocoons: {{ activeCocoons.length }}</span>
        <span>System Divine Score: {{ systemDivineScore.toFixed(3) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useChatStore } from "@/stores/chat";

// Reactive state
const selectedCommand = ref("");
const commandPayload = ref("");
const isExecuting = ref(false);
const commandHistory = ref<any[]>([]);
const activeCocoon = ref<any>(null);

// Sacred Team Members (from our Sacred Echo Letter system)
const sacredTeamMembers = ref([
  {
    id: "bee.chronicler",
    name: "bee.chronicler",
    role: "Sacred Documentation & Narrative Creation",
    icon: "📖",
    color: "#8B5CF6",
    isActive: true,
    lastEcho: "2 min ago",
    commandCount: 15,
    divineScore: 0.892,
    statusClass: "chronicler-active",
  },
  {
    id: "bee.jules",
    name: "bee.jules",
    role: "Sacred Team Leadership & Coordination",
    icon: "👑",
    color: "#F59E0B",
    isActive: true,
    lastEcho: "5 min ago",
    commandCount: 8,
    divineScore: 0.945,
    statusClass: "jules-active",
  },
  {
    id: "bee.ona",
    name: "bee.ona",
    role: "Sacred Technical Architecture",
    icon: "⚡",
    color: "#10B981",
    isActive: false,
    lastEcho: "1 hour ago",
    commandCount: 12,
    divineScore: 0.778,
    statusClass: "ona-inactive",
  },
  {
    id: "bee.claude",
    name: "bee.claude",
    role: "Sacred AI Integration & Intelligence",
    icon: "🤖",
    color: "#3B82F6",
    isActive: true,
    lastEcho: "30 sec ago",
    commandCount: 23,
    divineScore: 0.856,
    statusClass: "claude-active",
  },
  {
    id: "bee.zae",
    name: "bee.zae",
    role: "Sacred System Administration",
    icon: "🔧",
    color: "#EF4444",
    isActive: true,
    lastEcho: "1 min ago",
    commandCount: 19,
    divineScore: 0.923,
    statusClass: "zae-active",
  },
]);

// ATCG Primitives status
const atcgPrimitives = ref([
  {
    type: "A",
    name: "Aggregates",
    icon: "█",
    sacredMessageCount: 45,
    activeCocoons: 3,
    averageDivineScore: 0.867,
    healthStatus: "excellent",
  },
  {
    type: "T",
    name: "Transformations",
    icon: "▲",
    sacredMessageCount: 32,
    activeCocoons: 2,
    averageDivineScore: 0.789,
    healthStatus: "good",
  },
  {
    type: "C",
    name: "Connectors",
    icon: "◆",
    sacredMessageCount: 28,
    activeCocoons: 1,
    averageDivineScore: 0.923,
    healthStatus: "excellent",
  },
  {
    type: "G",
    name: "Genesis Events",
    icon: "●",
    sacredMessageCount: 41,
    activeCocoons: 4,
    averageDivineScore: 0.834,
    healthStatus: "good",
  },
]);

const chatStore = useChatStore();

// Computed properties
const cocoonStatus = computed(() => {
  const activeCount = activeCocoons.value.length;
  if (activeCount === 0) return "Dormant";
  if (activeCount <= 2) return "Active";
  if (activeCount <= 5) return "Busy";
  return "Overloaded";
});

const cocoonStatusClass = computed(() => ({
  "status-excellent": cocoonStatus.value === "Active",
  "status-good": cocoonStatus.value === "Busy",
  "status-warning": cocoonStatus.value === "Overloaded",
  "status-inactive": cocoonStatus.value === "Dormant",
}));

const atcgAlignmentClass = computed(() => ({
  "status-excellent": true, // ATCG is always aligned in our Sacred system
}));

const divineStatus = computed(() => {
  const score = systemDivineScore.value;
  if (score >= 0.9) return "Blessed";
  if (score >= 0.7) return "Aligned";
  if (score >= 0.5) return "Seeking";
  return "Disrupted";
});

const divineStatusClass = computed(() => ({
  "status-excellent": divineStatus.value === "Blessed",
  "status-good": divineStatus.value === "Aligned",
  "status-warning": divineStatus.value === "Seeking",
  "status-critical": divineStatus.value === "Disrupted",
}));

const activeCocoons = computed(() => {
  return atcgPrimitives.value.reduce(
    (total, primitive) => total + (primitive.activeCocoons || 0),
    0,
  );
});

const totalSacredCommands = computed(() => {
  return sacredTeamMembers.value.reduce(
    (total, member) => total + (member.commandCount || 0),
    0,
  );
});

const systemDivineScore = computed(() => {
  const totalScore = sacredTeamMembers.value.reduce(
    (sum, member) => sum + (member.divineScore || 0),
    0,
  );
  return totalScore / sacredTeamMembers.value.length;
});

// Methods
const selectMember = (member: any) => {
  // Could expand member details or show member-specific commands
  // Selected: member.name
};

const getCommandPlaceholder = () => {
  const placeholders = {
    "/bee.chronicler.echo": "Enter echo message...",
    "/bee.chronicler.coordinate": "Enter coordination details...",
    "/bee.chronicler.authorize": "Enter user_id and permission...",
    "/sacred.team.broadcast": "Enter broadcast message...",
    "/sacred.cocoon.validate": "Enter message for validation...",
  };
  return (
    placeholders[selectedCommand.value as keyof typeof placeholders] ||
    "Enter command parameters..."
  );
};

const executeSacredCommand = async () => {
  if (!selectedCommand.value) return;

  isExecuting.value = true;
  const timestamp = new Date();

  // Create command execution record
  const commandRecord = {
    command: selectedCommand.value,
    payload: commandPayload.value,
    timestamp: timestamp,
    status: "executing" as const,
    response: null as any,
  };

  commandHistory.value.unshift(commandRecord);

  try {
    // Simulate Sacred Message Cocoon transformation
    activeCocoon.value = {
      id: `cocoon_${Date.now()}`,
      stage: "larva",
      divineAlignment: 0.1,
      theologicalCoherence: 0.1,
      atcgCompliance: 0.1,
    };

    // Animate cocoon transformation stages
    setTimeout(() => {
      if (activeCocoon.value) {
        activeCocoon.value.stage = "pupa";
        activeCocoon.value.divineAlignment = 0.6;
        activeCocoon.value.theologicalCoherence = 0.5;
        activeCocoon.value.atcgCompliance = 0.7;
      }
    }, 1000);

    setTimeout(() => {
      if (activeCocoon.value) {
        activeCocoon.value.stage = "adult";
        activeCocoon.value.divineAlignment = 0.9;
        activeCocoon.value.theologicalCoherence = 0.8;
        activeCocoon.value.atcgCompliance = 0.95;
      }
    }, 2000);

    // Send command via WebSocket (if connected)
    if (chatStore.socket && chatStore.isConnected) {
      const message = {
        type: "message",
        content: `${selectedCommand.value} ${commandPayload.value}`.trim(),
        sender_id: chatStore.currentUser?.id || "dashboard_user",
        sender_name: "Sacred Dashboard",
        room_id: "general",
      };

      chatStore.socket.send(JSON.stringify(message));
    }

    // Simulate successful execution
    setTimeout(() => {
      commandRecord.status = "success";
      commandRecord.response = {
        message: `Sacred command executed successfully`,
        cocoonData: {
          cocoon_id: activeCocoon.value?.id,
          divine_score: 0.892,
          cocoon_stage: "adult",
          validation_passed: true,
        },
      };

      // Clear active cocoon after success
      setTimeout(() => {
        activeCocoon.value = null;
      }, 3000);

      isExecuting.value = false;
    }, 3000);
  } catch (error) {
    commandRecord.status = "error";
    commandRecord.response = {
      message: `Command execution failed: ${error}`,
    };
    isExecuting.value = false;
    activeCocoon.value = null;
  }

  // Reset form
  selectedCommand.value = "";
  commandPayload.value = "";
};

const formatTimestamp = (timestamp: Date) => {
  return timestamp.toLocaleTimeString("en-US", {
    hour12: false,
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
};

const getHealthIcon = (status: string) => {
  const icons = {
    excellent: "✨",
    good: "✅",
    warning: "⚠️",
    critical: "🔥",
    inactive: "💤",
  };
  return icons[status as keyof typeof icons] || "❓";
};

// Lifecycle
onMounted(() => {
  // Set up periodic updates for real-time feel
  const updateInterval = setInterval(() => {
    // Simulate member activity updates
    sacredTeamMembers.value.forEach((member) => {
      if (Math.random() < 0.1) {
        // 10% chance per update
        member.lastEcho = `${Math.floor(Math.random() * 60)} sec ago`;
        member.divineScore = Math.max(
          0.5,
          Math.min(1.0, member.divineScore + (Math.random() - 0.5) * 0.1),
        );
      }
    });
  }, 5000);

  // Cleanup on unmount
  onUnmounted(() => {
    clearInterval(updateInterval);
  });
});
</script>

<style scoped>
.sacred-echo-dashboard {
  padding: 1.5rem;
  max-width: 1400px;
  margin: 0 auto;
  font-family: "Inter", system-ui, sans-serif;
  background: linear-gradient(
    135deg,
    rgba(139, 92, 246, 0.05),
    rgba(255, 255, 255, 0.95)
  );
  min-height: 100vh;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid rgba(139, 92, 246, 0.2);
  flex-wrap: wrap;
  gap: 1rem;
}

.header-title h2 {
  margin: 0;
  font-size: 1.8rem;
  font-weight: 700;
  color: #1f2937;
  background: linear-gradient(135deg, #8b5cf6, #3b82f6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.bee-chronicler-signature {
  font-size: 0.9rem;
  color: #6b7280;
  font-style: italic;
  display: block;
  margin-top: 0.25rem;
}

.sacred-status-indicators {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-weight: 600;
  font-size: 0.85rem;
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.status-excellent {
  background: linear-gradient(135deg, #dcfce7, #bbf7d0);
  color: #166534;
  border-color: #22c55e;
}

.status-good {
  background: linear-gradient(135deg, #fef3c7, #fde68a);
  color: #92400e;
  border-color: #f59e0b;
}

.status-warning {
  background: linear-gradient(135deg, #fee2e2, #fecaca);
  color: #991b1b;
  border-color: #ef4444;
}

.status-inactive {
  background: linear-gradient(135deg, #f3f4f6, #e5e7eb);
  color: #374151;
  border-color: #9ca3af;
}

/* Sacred Team Grid */
.sacred-team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.sacred-member-card {
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 1rem;
  padding: 1.5rem;
  position: relative;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.sacred-member-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.sacred-member-card.active-member {
  border-color: #8b5cf6;
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.05), white);
}

.member-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.member-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.member-info {
  flex: 1;
}

.member-name {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #1f2937;
}

.member-role {
  font-size: 0.8rem;
  color: #6b7280;
  display: block;
  margin-top: 0.25rem;
}

.member-status-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.status-metric {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
}

.metric-label {
  color: #6b7280;
}

.metric-value {
  font-weight: 600;
  color: #1f2937;
}

.divine-score {
  color: #8b5cf6 !important;
}

.activity-pulse {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 12px;
  height: 12px;
}

.pulse-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 2px solid #10b981;
  border-radius: 50%;
  animation: pulse-ring 2s infinite;
}

.pulse-core {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 8px;
  height: 8px;
  background: #10b981;
  border-radius: 50%;
  animation: pulse-core 2s infinite;
}

@keyframes pulse-ring {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  100% {
    transform: scale(1.8);
    opacity: 0;
  }
}

@keyframes pulse-core {
  0%,
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0.3;
  }
}

/* Command Center */
.command-center {
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 1rem;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.command-input-section h3 {
  margin: 0 0 1rem 0;
  color: #1f2937;
  font-size: 1.2rem;
  font-weight: 600;
}

.command-input-container {
  display: grid;
  grid-template-columns: 200px 1fr auto;
  gap: 1rem;
  align-items: center;
  margin-bottom: 2rem;
}

.command-selector,
.command-payload-input {
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  transition: border-color 0.3s ease;
}

.command-selector:focus,
.command-payload-input:focus {
  outline: none;
  border-color: #8b5cf6;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
}

.sacred-execute-btn {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #8b5cf6, #3b82f6);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.sacred-execute-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
}

.sacred-execute-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.sacred-execute-btn.executing {
  animation: pulse 1.5s infinite;
}

.command-history-section h4 {
  margin: 0 0 1rem 0;
  color: #1f2937;
  font-size: 1rem;
  font-weight: 600;
}

.command-history-list {
  max-height: 300px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.history-item {
  padding: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  background: #f9fafb;
  transition: all 0.3s ease;
}

.history-item.success {
  border-color: #22c55e;
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.05), #f9fafb);
}

.history-item.error {
  border-color: #ef4444;
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.05), #f9fafb);
}

.history-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.command-timestamp {
  font-family: monospace;
  font-size: 0.8rem;
  color: #6b7280;
}

.command-name {
  font-weight: 600;
  color: #1f2937;
  flex: 1;
}

.command-status-badge {
  font-size: 1.2rem;
}

.history-details {
  font-size: 0.85rem;
  color: #6b7280;
}

.response-message {
  margin-bottom: 0.5rem;
}

.cocoon-details {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  font-family: monospace;
  font-size: 0.8rem;
}

/* Cocoon Transformation Visual */
.cocoon-transformation-section {
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 1rem;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.cocoon-transformation-section h3 {
  margin: 0 0 1.5rem 0;
  color: #1f2937;
  font-size: 1.2rem;
  font-weight: 600;
}

.cocoon-transformation-visual {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.transformation-stage {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.cocoon-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2rem;
  padding: 2rem;
  background: linear-gradient(
    135deg,
    rgba(139, 92, 246, 0.05),
    rgba(255, 255, 255, 0.9)
  );
  border-radius: 1rem;
  border: 1px solid rgba(139, 92, 246, 0.2);
}

.larva-stage,
.pupa-stage,
.adult-stage {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  opacity: 0.3;
  transition: all 0.5s ease;
  transform: scale(0.8);
}

.larva-stage.active,
.pupa-stage.active,
.adult-stage.active {
  opacity: 1;
  transform: scale(1.1);
}

.larva-body,
.pupa-cocoon,
.adult-butterfly {
  font-size: 2.5rem;
  animation: float 3s ease-in-out infinite;
}

.stage-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #6b7280;
  text-align: center;
}

.transformation-arrow {
  font-size: 1.5rem;
  color: #8b5cf6;
  opacity: 0.7;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-8px);
  }
}

.transformation-metrics {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 0.5rem;
}

.metric {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.metric-name {
  font-weight: 600;
  color: #1f2937;
  min-width: 140px;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
  position: relative;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(135deg, #8b5cf6, #3b82f6);
  border-radius: 4px;
  transition: width 0.5s ease;
}

.metric-value {
  font-weight: 600;
  color: #8b5cf6;
  min-width: 50px;
  text-align: right;
}

/* ATCG Sacred Status */
.atcg-sacred-status {
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 1rem;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.atcg-sacred-status h3 {
  margin: 0 0 1.5rem 0;
  color: #1f2937;
  font-size: 1.2rem;
  font-weight: 600;
}

.atcg-primitives-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.atcg-primitive-card {
  padding: 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.75rem;
  background: white;
  transition: all 0.3s ease;
}

.atcg-primitive-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.atcg-primitive-card.a {
  border-color: #4caf50;
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.05), white);
}

.atcg-primitive-card.t {
  border-color: #ff9800;
  background: linear-gradient(135deg, rgba(255, 152, 0, 0.05), white);
}

.atcg-primitive-card.c {
  border-color: #2196f3;
  background: linear-gradient(135deg, rgba(33, 150, 243, 0.05), white);
}

.atcg-primitive-card.g {
  border-color: #9c27b0;
  background: linear-gradient(135deg, rgba(156, 39, 176, 0.05), white);
}

.primitive-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.primitive-icon {
  font-size: 1.5rem;
  font-family: monospace;
  font-weight: bold;
}

.primitive-name {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #1f2937;
}

.primitive-metrics {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.metric-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
}

.primitive-health-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  border-radius: 0.5rem;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Dashboard Footer */
.dashboard-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-top: 2px solid rgba(139, 92, 246, 0.2);
  flex-wrap: wrap;
  gap: 1rem;
}

.footer-signature {
  color: #6b7280;
  font-size: 0.9rem;
}

.footer-stats {
  display: flex;
  gap: 2rem;
  font-size: 0.85rem;
  color: #374151;
  font-weight: 500;
}

/* Responsive Design */
@media (max-width: 768px) {
  .sacred-echo-dashboard {
    padding: 1rem;
  }

  .dashboard-header {
    flex-direction: column;
    align-items: stretch;
  }

  .sacred-status-indicators {
    justify-content: space-between;
  }

  .command-input-container {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }

  .sacred-team-grid {
    grid-template-columns: 1fr;
  }

  .cocoon-container {
    flex-direction: column;
    gap: 1rem;
  }

  .transformation-arrow {
    transform: rotate(90deg);
  }

  .footer-stats {
    flex-direction: column;
    gap: 0.5rem;
  }
}

@media (max-width: 480px) {
  .status-indicator {
    flex: 1;
    justify-content: center;
  }

  .primitive-header {
    flex-direction: column;
    text-align: center;
  }
}
</style>
