/**
 * 🐝✨ Sacred Reaction Manager Tests - Phase 1.1 Validation ✨🐝
 * 
 * Tests for divine protection mechanisms and computational safety
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { BoundedReactionManager, PROTECTION_LIMITS, ReactionManagerError } from '../BoundedReactionManager';

// Mock localStorage for testing
const localStorageMock = (() => {
  let store: Record<string, string> = {};
  
  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => { store[key] = value; },
    removeItem: (key: string) => { delete store[key]; },
    clear: () => { store = {}; },
    get length() { return Object.keys(store).length; },
    key: (index: number) => Object.keys(store)[index] || null
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock
});

describe('Sacred Reaction Manager', () => {
  let manager: BoundedReactionManager;
  
  beforeEach(() => {
    // Clear localStorage before each test
    localStorage.clear();
    
    // Create fresh manager instance
    manager = new BoundedReactionManager();
  });
  
  afterEach(() => {
    localStorage.clear();
  });

  describe('Basic Reaction Operations', () => {
    it('should toggle reactions correctly', async () => {
      const messageId = 'test-message-1';
      const emoji = '👍';
      const userId = 'user-1';
      const userName = 'TestUser';

      // Add reaction
      const result1 = await manager.toggleReaction(messageId, emoji, userId, userName);
      expect(result1).toBe(true);

      // Verify reaction was added
      const reactions = await manager.getReactionsForMessage(messageId);
      expect(reactions).toBeTruthy();
      expect(reactions![emoji]).toBeTruthy();
      expect(reactions![emoji].count).toBe(1);
      expect(reactions![emoji].users).toContain(userName);

      // Remove reaction
      const result2 = await manager.toggleReaction(messageId, emoji, userId, userName);
      expect(result2).toBe(true);

      // Verify reaction was removed
      const reactionsAfter = await manager.getReactionsForMessage(messageId);
      expect(reactionsAfter).toBeNull();
    });

    it('should handle multiple users reacting', async () => {
      const messageId = 'test-message-2';
      const emoji = '❤️';

      // Add reactions from multiple users
      await manager.toggleReaction(messageId, emoji, 'user-1', 'User1');
      await manager.toggleReaction(messageId, emoji, 'user-2', 'User2');
      await manager.toggleReaction(messageId, emoji, 'user-3', 'User3');

      const reactions = await manager.getReactionsForMessage(messageId);
      expect(reactions![emoji].count).toBe(3);
      expect(reactions![emoji].users).toHaveLength(3);
      expect(reactions![emoji].users).toContain('User1');
      expect(reactions![emoji].users).toContain('User2');
      expect(reactions![emoji].users).toContain('User3');
    });
  });

  describe('Sacred Bounds Protection', () => {
    it('should enforce maximum users per reaction', async () => {
      const messageId = 'test-message-bounds';
      const emoji = '🎉';

      // Add reactions up to the limit
      for (let i = 0; i < PROTECTION_LIMITS.MAX_USERS_PER_REACTION; i++) {
        const result = await manager.toggleReaction(messageId, emoji, `user-${i}`, `User${i}`);
        expect(result).toBe(true);
      }

      // Try to add one more (should fail)
      const result = await manager.toggleReaction(
        messageId, 
        emoji, 
        `user-${PROTECTION_LIMITS.MAX_USERS_PER_REACTION}`, 
        `User${PROTECTION_LIMITS.MAX_USERS_PER_REACTION}`
      );
      expect(result).toBe(false);

      // Verify count is still at limit
      const reactions = await manager.getReactionsForMessage(messageId);
      expect(reactions![emoji].count).toBe(PROTECTION_LIMITS.MAX_USERS_PER_REACTION);
    });

    it('should perform sacred cleanup when reaction limit exceeded', async () => {
      const messageId = 'test-message-cleanup';

      // Add reactions beyond cleanup threshold
      const reactionCount = Math.floor(PROTECTION_LIMITS.MAX_REACTIONS_PER_MESSAGE * PROTECTION_LIMITS.CLEANUP_THRESHOLD) + 5;
      
      for (let i = 0; i < reactionCount; i++) {
        const emoji = String.fromCodePoint(0x1F600 + i); // Different emojis
        await manager.toggleReaction(messageId, emoji, 'user-1', 'User1');
      }

      // Add one more reaction to trigger cleanup
      await manager.toggleReaction(messageId, '🚀', 'user-1', 'User1');

      const reactions = await manager.getReactionsForMessage(messageId);
      const finalCount = Object.keys(reactions || {}).length;
      
      // Should have fewer reactions after cleanup
      expect(finalCount).toBeLessThan(reactionCount);
      expect(finalCount).toBeLessThanOrEqual(Math.floor(PROTECTION_LIMITS.MAX_REACTIONS_PER_MESSAGE * 0.4));
    });
  });

  describe('Sacred Metrics and Monitoring', () => {
    it('should track reaction metrics correctly', async () => {
      const messageId1 = 'metrics-test-1';
      const messageId2 = 'metrics-test-2';

      // Add some reactions
      await manager.toggleReaction(messageId1, '👍', 'user-1', 'User1');
      await manager.toggleReaction(messageId1, '❤️', 'user-2', 'User2');
      await manager.toggleReaction(messageId2, '😄', 'user-1', 'User1');

      // Allow metrics to update
      await new Promise(resolve => setTimeout(resolve, 10));

      const metrics = manager.getMetrics();
      
      expect(metrics.totalReactions).toBe(3);
      expect(metrics.totalMessages).toBe(2);
      expect(metrics.circuitBreakerState).toBe('CLOSED');
    });

    it('should calculate popularity correctly', async () => {
      const messageId = 'popularity-test';
      const emoji = '🔥';

      // Add multiple reactions to increase popularity
      await manager.toggleReaction(messageId, emoji, 'user-1', 'User1');
      await manager.toggleReaction(messageId, emoji, 'user-2', 'User2');
      await manager.toggleReaction(messageId, emoji, 'user-3', 'User3');

      const reactions = await manager.getReactionsForMessage(messageId);
      expect(reactions![emoji].popularity).toBeGreaterThan(0);
      expect(reactions![emoji].popularity).toBeLessThanOrEqual(1);
    });
  });

  describe('Error Handling and Circuit Breaker', () => {
    it('should handle localStorage errors gracefully', async () => {
      // Mock localStorage to throw error
      const originalSetItem = localStorage.setItem;
      localStorage.setItem = vi.fn(() => {
        throw new Error('Storage quota exceeded');
      });

      try {
        await expect(
          manager.toggleReaction('test', '👍', 'user', 'User')
        ).rejects.toThrow();
      } finally {
        localStorage.setItem = originalSetItem;
      }
    });

    it('should provide health status correctly', async () => {
      // Allow initialization to complete
      await new Promise(resolve => setTimeout(resolve, 10));
      
      expect(manager.isHealthy.value).toBe(true);
      expect(manager.statusMessage.value).toBe('Sacred Protection: All systems operational');
    });
  });

  describe('Memory Management', () => {
    it('should perform global cleanup when needed', async () => {
      // Create many messages with reactions to simulate memory pressure
      const messageCount = 20;
      
      for (let i = 0; i < messageCount; i++) {
        await manager.toggleReaction(`message-${i}`, '👍', 'user-1', 'User1');
        
        // Add some delay to create different timestamps
        await new Promise(resolve => setTimeout(resolve, 1));
      }

      // Trigger global cleanup manually
      await manager.performManualCleanup();

      const metrics = manager.getMetrics();
      
      // Should have fewer messages after cleanup
      expect(metrics.totalMessages).toBeLessThan(messageCount);
    });
  });
});

describe('Sacred Protection Integration', () => {
  it('should integrate with Vue reactivity', async () => {
    const manager = new BoundedReactionManager();
    
    // Allow initialization to complete
    await new Promise(resolve => setTimeout(resolve, 10));
    
    // Test reactive properties
    expect(manager.metrics.value).toBeDefined();
    expect(manager.isHealthy.value).toBe(true);
    expect(manager.statusMessage.value).toBe('Sacred Protection: All systems operational');
  });

  it('should provide comprehensive metrics', () => {
    const manager = new BoundedReactionManager();
    const metrics = manager.getMetrics();
    
    expect(metrics).toHaveProperty('totalReactions');
    expect(metrics).toHaveProperty('totalMessages');
    expect(metrics).toHaveProperty('memoryUsage');
    expect(metrics).toHaveProperty('circuitBreakerState');
    expect(metrics).toHaveProperty('memory');
    expect(metrics).toHaveProperty('circuitBreaker');
  });
});