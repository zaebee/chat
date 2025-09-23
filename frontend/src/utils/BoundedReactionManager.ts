/**
 * 🐝✨ Bounded Reaction Manager - Phase 1.1 Emergency Fix ✨🐝
 * 
 * IMMEDIATE IMPLEMENTATION - Addresses bee.Sage critical vulnerability:
 * "Unbounded Reaction Storage - Memory exhaustion through infinite reaction accumulation"
 * 
 * Engineering Truth: Implements bounded collection patterns with circuit breaker protection
 * Protection Mechanisms:
 * - Bounded collections with automatic cleanup
 * - Circuit breaker patterns for failure isolation
 * - Memory monitoring and quota enforcement
 * - Graceful degradation under stress
 * 
 * Sacred Narrative: "For everything there is a season, and a time for every matter under heaven"
 * - Ecclesiastes 3:1 (ESV)
 */

import { ref, computed } from 'vue';
import type { Message } from '@/stores/messages';

// Protection Configuration Constants
const PROTECTION_LIMITS = {
  MAX_REACTIONS_PER_MESSAGE: 50,
  MAX_USERS_PER_REACTION: 100,
  CLEANUP_THRESHOLD: 0.8,
  STORAGE_QUOTA_MB: 10,
  CIRCUIT_BREAKER_THRESHOLD: 5,
  RECOVERY_TIMEOUT_MS: 30000,
  GLOBAL_CLEANUP_THRESHOLD: 0.9
} as const;

// Reaction Management Error Types
export class ReactionManagerError extends Error {
  constructor(message: string, public code: string) {
    super(message);
    this.name = 'SacredReactionError';
  }
}

export class SacredCircuitBreakerError extends SacredReactionError {
  constructor() {
    super('Sacred Circuit Breaker is OPEN - protecting system from cascade failures', 'CIRCUIT_BREAKER_OPEN');
  }
}

export class SacredMemoryQuotaError extends SacredReactionError {
  constructor() {
    super('Sacred Memory Quota exceeded - performing divine cleanup', 'MEMORY_QUOTA_EXCEEDED');
  }
}

// Sacred Circuit Breaker Implementation
class SacredCircuitBreaker {
  private state: 'CLOSED' | 'OPEN' | 'HALF_OPEN' = 'CLOSED';
  private failureCount = 0;
  private lastFailureTime = 0;
  private successCount = 0;

  constructor(
    private failureThreshold: number = PROTECTION_LIMITS.CIRCUIT_BREAKER_THRESHOLD,
    private recoveryTimeout: number = PROTECTION_LIMITS.RECOVERY_TIMEOUT_MS,
    private successThreshold: number = 3
  ) {}

  async execute<T>(operation: () => Promise<T>): Promise<T> {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailureTime > this.recoveryTimeout) {
        this.state = 'HALF_OPEN';
        this.successCount = 0;
      } else {
        throw new SacredCircuitBreakerError();
      }
    }

    try {
      const result = await operation();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess(): void {
    this.failureCount = 0;
    
    if (this.state === 'HALF_OPEN') {
      this.successCount++;
      if (this.successCount >= this.successThreshold) {
        this.state = 'CLOSED';
      }
    }
  }

  private onFailure(): void {
    this.failureCount++;
    this.lastFailureTime = Date.now();
    
    if (this.failureCount >= this.failureThreshold) {
      this.state = 'OPEN';
    }
  }

  getState(): string {
    return this.state;
  }

  getMetrics() {
    return {
      state: this.state,
      failureCount: this.failureCount,
      successCount: this.successCount,
      lastFailureTime: this.lastFailureTime
    };
  }
}

// Sacred Memory Monitor Implementation
class SacredMemoryMonitor {
  private readonly maxStorageSize: number;
  private readonly warningThreshold: number;

  constructor(maxStorageMB: number = PROTECTION_LIMITS.STORAGE_QUOTA_MB) {
    this.maxStorageSize = maxStorageMB * 1024 * 1024;
    this.warningThreshold = this.maxStorageSize * 0.8;
  }

  getCurrentUsage(): number {
    try {
      let totalSize = 0;
      for (let key in localStorage) {
        if (localStorage.hasOwnProperty(key)) {
          totalSize += localStorage[key].length + key.length;
        }
      }
      return totalSize;
    } catch (error) {
      console.warn('Sacred Memory Monitor: Unable to calculate storage usage', error);
      return 0;
    }
  }

  isQuotaExceeded(): boolean {
    return this.getCurrentUsage() > this.maxStorageSize;
  }

  isWarningThresholdExceeded(): boolean {
    return this.getCurrentUsage() > this.warningThreshold;
  }

  getUsagePercentage(): number {
    return (this.getCurrentUsage() / this.maxStorageSize) * 100;
  }

  getMetrics() {
    const usage = this.getCurrentUsage();
    return {
      currentUsage: usage,
      maxStorage: this.maxStorageSize,
      usagePercentage: (usage / this.maxStorageSize) * 100,
      isQuotaExceeded: usage > this.maxStorageSize,
      isWarningExceeded: usage > this.warningThreshold
    };
  }
}

// Sacred Reaction Data Types
export interface SacredReaction {
  emoji: string;
  users: string[];
  count: number;
  lastUpdated: number;
  popularity: number; // For cleanup prioritization
}

export interface BoundedMessageReactions {
  [emoji: string]: SacredReaction;
}

export interface SacredReactionMetrics {
  totalReactions: number;
  totalMessages: number;
  memoryUsage: number;
  circuitBreakerState: string;
  lastCleanup: number;
}

// Main Sacred Reaction Manager Class
export class BoundedReactionManager {
  private circuitBreaker: SacredCircuitBreaker;
  private memoryMonitor: SacredMemoryMonitor;
  private lastGlobalCleanup = 0;
  private readonly globalCleanupInterval = 300000; // 5 minutes

  // Reactive state for Vue integration
  public readonly metrics = ref<SacredReactionMetrics>({
    totalReactions: 0,
    totalMessages: 0,
    memoryUsage: 0,
    circuitBreakerState: 'CLOSED',
    lastCleanup: 0
  });

  constructor() {
    this.circuitBreaker = new SacredCircuitBreaker();
    this.memoryMonitor = new SacredMemoryMonitor();
    
    // Initialize metrics immediately
    this.updateMetrics();
    
    // Set up periodic monitoring
    this.startPeriodicMonitoring();
    
    // Ensure reactive properties are properly initialized
    setTimeout(() => this.updateMetrics(), 0);
  }

  /**
   * Sacred Toggle Reaction - Main entry point with divine protection
   */
  async toggleReaction(
    messageId: string, 
    emoji: string, 
    userId: string, 
    userName: string
  ): Promise<boolean> {
    return this.circuitBreaker.execute(async () => {
      // Sacred bounds checking
      if (await this.exceedsReactionLimits(messageId)) {
        await this.performSacredCleanup(messageId);
      }

      // Sacred memory monitoring
      if (this.memoryMonitor.isQuotaExceeded()) {
        await this.performGlobalCleanup();
      }

      // Perform the actual reaction toggle
      return this.performReactionToggle(messageId, emoji, userId, userName);
    });
  }

  /**
   * Sacred Reaction Limits Check
   */
  private async exceedsReactionLimits(messageId: string): Promise<boolean> {
    const reactions = await this.getMessageReactions(messageId);
    if (!reactions) return false;

    const reactionCount = Object.keys(reactions).length;
    return reactionCount > PROTECTION_LIMITS.MAX_REACTIONS_PER_MESSAGE * PROTECTION_LIMITS.CLEANUP_THRESHOLD;
  }

  /**
   * Sacred Message-Level Cleanup
   */
  private async performSacredCleanup(messageId: string): Promise<void> {
    try {
      const reactions = await this.getMessageReactions(messageId);
      if (!reactions) return;

      // Calculate popularity scores for divine preservation
      const reactionEntries = Object.entries(reactions).map(([emoji, reaction]) => ({
        emoji,
        reaction,
        popularity: this.calculatePopularity(reaction)
      }));

      // Sort by popularity (divine wisdom - preserve what humans value most)
      reactionEntries.sort((a, b) => b.popularity - a.popularity);

      // Keep only the most sacred (popular) reactions
      const keepCount = Math.floor(PROTECTION_LIMITS.MAX_REACTIONS_PER_MESSAGE * 0.4); // More aggressive cleanup
      const preservedReactions: BoundedMessageReactions = {};

      for (let i = 0; i < Math.min(keepCount, reactionEntries.length); i++) {
        const { emoji, reaction } = reactionEntries[i];
        preservedReactions[emoji] = reaction;
      }

      // Sacred preservation
      await this.setMessageReactions(messageId, preservedReactions);
      
      console.log(`Sacred Cleanup: Preserved ${Object.keys(preservedReactions).length} most popular reactions for message ${messageId}`);
    } catch (error) {
      console.error('Sacred Cleanup Error:', error);
      throw new SacredReactionError('Failed to perform sacred cleanup', 'CLEANUP_FAILED');
    }
  }

  /**
   * Sacred Global Cleanup - Divine memory management
   */
  private async performGlobalCleanup(): Promise<void> {
    try {
      const now = Date.now();
      
      // Prevent too frequent global cleanups
      if (now - this.lastGlobalCleanup < this.globalCleanupInterval) {
        return;
      }

      const allMessages = await this.getAllMessagesWithReactions();
      
      // Sort by last activity (divine wisdom - preserve recent interactions)
      const sortedMessages = allMessages.sort((a, b) => 
        (b.lastReactionTime || 0) - (a.lastReactionTime || 0)
      );

      // Keep only the most recent 80% of messages with reactions
      const keepCount = Math.floor(sortedMessages.length * 0.8);
      const messagesToClean = sortedMessages.slice(keepCount);

      // Sacred cleanup of old messages
      for (const message of messagesToClean) {
        await this.clearMessageReactions(message.id);
      }

      this.lastGlobalCleanup = now;
      this.metrics.value.lastCleanup = now;
      
      console.log(`Sacred Global Cleanup: Cleaned ${messagesToClean.length} old messages, preserved ${keepCount} recent messages`);
    } catch (error) {
      console.error('Sacred Global Cleanup Error:', error);
      throw new SacredMemoryQuotaError();
    }
  }

  /**
   * Sacred Reaction Toggle Implementation
   */
  private async performReactionToggle(
    messageId: string, 
    emoji: string, 
    userId: string, 
    userName: string
  ): Promise<boolean> {
    try {
      const reactions = await this.getMessageReactions(messageId) || {};
      
      if (!reactions[emoji]) {
        // Create new reaction
        reactions[emoji] = {
          emoji,
          users: [userName],
          count: 1,
          lastUpdated: Date.now(),
          popularity: 1
        };
      } else {
        // Toggle existing reaction
        const reaction = reactions[emoji];
        const userIndex = reaction.users.indexOf(userName);
        
        if (userIndex === -1) {
          // Add user reaction (with sacred bounds checking)
          if (reaction.users.length < PROTECTION_LIMITS.MAX_USERS_PER_REACTION) {
            reaction.users.push(userName);
            reaction.count++;
          } else {
            console.warn(`Protection Limit: Maximum users per reaction (${PROTECTION_LIMITS.MAX_USERS_PER_REACTION}) reached for ${emoji}`);
            return false;
          }
        } else {
          // Remove user reaction
          reaction.users.splice(userIndex, 1);
          reaction.count--;
          
          // Remove reaction if no users left
          if (reaction.count === 0) {
            delete reactions[emoji];
            await this.setMessageReactions(messageId, reactions);
            return true;
          }
        }
        
        reaction.lastUpdated = Date.now();
        reaction.popularity = this.calculatePopularity(reaction);
      }

      await this.setMessageReactions(messageId, reactions);
      return true;
    } catch (error) {
      console.error('Sacred Reaction Toggle Error:', error);
      throw new SacredReactionError('Failed to toggle reaction', 'TOGGLE_FAILED');
    }
  }

  /**
   * Sacred Popularity Calculation (Divine Algorithm)
   */
  private calculatePopularity(reaction: SacredReaction): number {
    const recencyWeight = 0.3;
    const countWeight = 0.7;
    
    // Recency score (more recent = higher score)
    const hoursSinceUpdate = (Date.now() - reaction.lastUpdated) / (1000 * 60 * 60);
    const recencyScore = Math.max(0, 1 - (hoursSinceUpdate / 24)); // Decay over 24 hours
    
    // Count score (normalized)
    const countScore = Math.min(1, reaction.count / 10); // Max score at 10 reactions
    
    return (recencyScore * recencyWeight) + (countScore * countWeight);
  }

  /**
   * Sacred Storage Operations
   */
  private async getMessageReactions(messageId: string): Promise<BoundedMessageReactions | null> {
    try {
      const stored = localStorage.getItem(`sacred_reactions_${messageId}`);
      return stored ? JSON.parse(stored) : null;
    } catch (error) {
      console.error('Sacred Storage Read Error:', error);
      return null;
    }
  }

  private async setMessageReactions(messageId: string, reactions: BoundedMessageReactions): Promise<void> {
    try {
      if (Object.keys(reactions).length === 0) {
        localStorage.removeItem(`sacred_reactions_${messageId}`);
      } else {
        localStorage.setItem(`sacred_reactions_${messageId}`, JSON.stringify(reactions));
      }
    } catch (error) {
      console.error('Sacred Storage Write Error:', error);
      throw new SacredReactionError('Failed to save reactions', 'STORAGE_FAILED');
    }
  }

  private async clearMessageReactions(messageId: string): Promise<void> {
    localStorage.removeItem(`sacred_reactions_${messageId}`);
  }

  private async getAllMessagesWithReactions(): Promise<Array<{id: string, lastReactionTime?: number}>> {
    const messages: Array<{id: string, lastReactionTime?: number}> = [];
    
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key?.startsWith('sacred_reactions_')) {
        const messageId = key.replace('sacred_reactions_', '');
        const reactions = await this.getMessageReactions(messageId);
        
        if (reactions) {
          const lastReactionTime = Math.max(
            ...Object.values(reactions).map(r => r.lastUpdated)
          );
          messages.push({ id: messageId, lastReactionTime });
        }
      }
    }
    
    return messages;
  }

  /**
   * Sacred Metrics and Monitoring
   */
  private updateMetrics(): void {
    try {
      const memoryMetrics = this.memoryMonitor.getMetrics();
      const circuitMetrics = this.circuitBreaker.getMetrics();
      
      this.metrics.value = {
        totalReactions: this.getTotalReactionCount(),
        totalMessages: this.getTotalMessageCount(),
        memoryUsage: memoryMetrics.usagePercentage,
        circuitBreakerState: circuitMetrics.state,
        lastCleanup: this.lastGlobalCleanup
      };
    } catch (error) {
      console.warn('Sacred Metrics Update Error:', error);
    }
  }

  private getTotalReactionCount(): number {
    let total = 0;
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key?.startsWith('sacred_reactions_')) {
        try {
          const reactions = JSON.parse(localStorage.getItem(key) || '{}');
          total += Object.values(reactions).reduce((sum: number, reaction: any) => sum + reaction.count, 0);
        } catch (error) {
          // Ignore corrupted entries
        }
      }
    }
    return total;
  }

  private getTotalMessageCount(): number {
    let count = 0;
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key?.startsWith('sacred_reactions_')) {
        count++;
      }
    }
    return count;
  }

  private startPeriodicMonitoring(): void {
    // Update metrics every 30 seconds
    setInterval(() => {
      this.updateMetrics();
      
      // Check for automatic global cleanup
      if (this.memoryMonitor.isWarningThresholdExceeded()) {
        console.warn('Sacred Memory Warning: Approaching storage quota');
      }
    }, 30000);
  }

  /**
   * Public API for component integration
   */
  public getReactionsForMessage(messageId: string): Promise<BoundedMessageReactions | null> {
    return this.getMessageReactions(messageId);
  }

  public getMetrics() {
    return {
      ...this.metrics.value,
      memory: this.memoryMonitor.getMetrics(),
      circuitBreaker: this.circuitBreaker.getMetrics()
    };
  }

  public async performManualCleanup(): Promise<void> {
    await this.performGlobalCleanup();
  }

  // Computed properties for Vue reactivity
  public readonly isHealthy = computed(() => {
    const currentMetrics = this.metrics.value;
    return currentMetrics.circuitBreakerState === 'CLOSED' && 
           currentMetrics.memoryUsage < 90;
  });

  public readonly statusMessage = computed(() => {
    const currentMetrics = this.metrics.value;
    if (currentMetrics.circuitBreakerState === 'OPEN') {
      return 'Sacred Protection: Circuit breaker active';
    }
    if (currentMetrics.memoryUsage > 90) {
      return 'Sacred Protection: Memory cleanup in progress';
    }
    return 'Sacred Protection: All systems operational';
  });
}

// Sacred Singleton Instance
let sacredReactionManagerInstance: SacredReactionManager | null = null;

export function useBoundedReactionManager(): SacredReactionManager {
  if (!sacredReactionManagerInstance) {
    sacredReactionManagerInstance = new SacredReactionManager();
  }
  return sacredReactionManagerInstance;
}

// Export for testing and debugging
export { PROTECTION_LIMITS };