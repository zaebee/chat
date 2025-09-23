/**
 * 🐝✨ Vue Error Boundary - Phase 1.1 Emergency Fix ✨🐝
 * 
 * IMMEDIATE IMPLEMENTATION - Addresses bee.Sage critical vulnerability:
 * "Missing Circuit Breakers - No protection against cascade failures"
 * 
 * Engineering Truth: Implements Vue 3 error boundary patterns with circuit breaker protection
 * Protection Mechanisms:
 * - Comprehensive error boundaries for all operations
 * - Cascade failure prevention through error isolation
 * - Graceful degradation under error conditions
 * - Error recovery and retry mechanisms
 * - Error reporting and monitoring
 * 
 * Sacred Narrative: "He will not let your foot slip—he who watches over you will not slumber"
 * - Psalm 121:3 (NIV)
 */

import { ref, computed, onErrorCaptured, getCurrentInstance } from 'vue';

// Error Boundary Configuration
const ERROR_BOUNDARY_LIMITS = {
  MAX_ERRORS_PER_COMPONENT: 10,
  MAX_ERRORS_PER_MINUTE: 50,
  ERROR_RECOVERY_DELAY_MS: 1000,
  MAX_RETRY_ATTEMPTS: 3,
  CIRCUIT_BREAKER_THRESHOLD: 5,
  CIRCUIT_BREAKER_TIMEOUT_MS: 30000
} as const;

// Sacred Error Types
export class SacredBoundaryError extends Error {
  constructor(
    message: string,
    public code: string,
    public component?: string,
    public context?: string
  ) {
    super(message);
    this.name = 'SacredBoundaryError';
    this.timestamp = new Date().toISOString();
  }
  
  public readonly timestamp: string;
}

export class SacredCascadeError extends SacredBoundaryError {
  constructor(component?: string) {
    super(
      'Sacred cascade failure detected - circuit breaker activated',
      'CASCADE_FAILURE',
      component
    );
  }
}

// Sacred Error State
interface SacredErrorState {
  hasError: boolean;
  errorCount: number;
  lastError: Error | null;
  lastErrorTime: number;
  isRecovering: boolean;
  circuitBreakerOpen: boolean;
  retryCount: number;
}

// Sacred Error Metrics
interface SacredErrorMetrics {
  totalErrors: number;
  errorsPerMinute: number;
  componentErrors: Map<string, number>;
  errorTypes: Map<string, number>;
  lastCleanup: number;
}

// Sacred Error Manager
class SacredErrorManager {
  private errorHistory: Array<{
    error: Error;
    component: string;
    timestamp: number;
    context?: string;
  }> = [];
  
  private componentStates: Map<string, SacredErrorState> = new Map();
  private metrics: SacredErrorMetrics = {
    totalErrors: 0,
    errorsPerMinute: 0,
    componentErrors: new Map(),
    errorTypes: new Map(),
    lastCleanup: Date.now()
  };

  constructor() {
    this.startPeriodicCleanup();
  }

  /**
   * Sacred Error Recording
   */
  recordError(
    error: Error,
    component: string,
    context?: string
  ): void {
    const now = Date.now();
    
    // Record in history
    this.errorHistory.push({
      error,
      component,
      timestamp: now,
      context
    });

    // Update metrics
    this.metrics.totalErrors++;
    this.metrics.componentErrors.set(
      component,
      (this.metrics.componentErrors.get(component) || 0) + 1
    );
    this.metrics.errorTypes.set(
      error.constructor.name,
      (this.metrics.errorTypes.get(error.constructor.name) || 0) + 1
    );

    // Update component state
    const state = this.getOrCreateComponentState(component);
    state.hasError = true;
    state.errorCount++;
    state.lastError = error;
    state.lastErrorTime = now;

    // Check for cascade failure
    if (state.errorCount >= ERROR_BOUNDARY_LIMITS.CIRCUIT_BREAKER_THRESHOLD) {
      state.circuitBreakerOpen = true;
      console.warn(`Sacred circuit breaker opened for component: ${component}`);
    }

    // Trim history if too large
    if (this.errorHistory.length > 1000) {
      this.errorHistory = this.errorHistory.slice(-500);
    }

    console.error(`Sacred error recorded: ${component}:${context || 'unknown'}`, error);
  }

  /**
   * Sacred Error Recovery
   */
  async recoverFromError(component: string): Promise<boolean> {
    const state = this.getOrCreateComponentState(component);
    
    if (state.isRecovering) {
      return false;
    }

    state.isRecovering = true;
    
    try {
      // Sacred recovery delay
      await new Promise(resolve => 
        setTimeout(resolve, ERROR_BOUNDARY_LIMITS.ERROR_RECOVERY_DELAY_MS)
      );

      // Reset error state
      state.hasError = false;
      state.retryCount++;
      
      // Check if circuit breaker should be closed
      const recentErrors = this.getRecentErrors(component, 60000); // Last minute
      if (recentErrors.length < ERROR_BOUNDARY_LIMITS.CIRCUIT_BREAKER_THRESHOLD) {
        state.circuitBreakerOpen = false;
        console.info(`Sacred circuit breaker closed for component: ${component}`);
      }

      return true;

    } catch (recoveryError) {
      console.error(`Sacred recovery failed for ${component}:`, recoveryError);
      return false;
    } finally {
      state.isRecovering = false;
    }
  }

  /**
   * Sacred Operation Wrapper
   */
  async wrapSacredOperation<T>(
    operation: () => Promise<T> | T,
    component: string,
    context?: string
  ): Promise<T | null> {
    const state = this.getOrCreateComponentState(component);

    // Check circuit breaker
    if (state.circuitBreakerOpen) {
      const timeSinceLastError = Date.now() - state.lastErrorTime;
      if (timeSinceLastError < ERROR_BOUNDARY_LIMITS.CIRCUIT_BREAKER_TIMEOUT_MS) {
        throw new SacredCascadeError(component);
      } else {
        // Try to close circuit breaker
        state.circuitBreakerOpen = false;
      }
    }

    try {
      const result = await operation();
      
      // Success - reset error count gradually
      if (state.errorCount > 0) {
        state.errorCount = Math.max(0, state.errorCount - 1);
      }
      
      return result;

    } catch (error) {
      this.recordError(error as Error, component, context);
      
      // Check if we should retry
      if (state.retryCount < ERROR_BOUNDARY_LIMITS.MAX_RETRY_ATTEMPTS) {
        console.warn(`Sacred retry attempt ${state.retryCount + 1} for ${component}`);
        await new Promise(resolve => setTimeout(resolve, 500 * state.retryCount));
        return this.wrapSacredOperation(operation, component, context);
      }
      
      return null;
    }
  }

  /**
   * Sacred Utilities
   */
  private getOrCreateComponentState(component: string): SacredErrorState {
    if (!this.componentStates.has(component)) {
      this.componentStates.set(component, {
        hasError: false,
        errorCount: 0,
        lastError: null,
        lastErrorTime: 0,
        isRecovering: false,
        circuitBreakerOpen: false,
        retryCount: 0
      });
    }
    return this.componentStates.get(component)!;
  }

  private getRecentErrors(component: string, timeWindow: number): Array<any> {
    const now = Date.now();
    return this.errorHistory.filter(entry => 
      entry.component === component && 
      (now - entry.timestamp) < timeWindow
    );
  }

  private startPeriodicCleanup(): void {
    setInterval(() => {
      this.performCleanup();
    }, 60000); // Every minute
  }

  private performCleanup(): void {
    const now = Date.now();
    const oneHourAgo = now - (60 * 60 * 1000);

    // Clean old error history
    this.errorHistory = this.errorHistory.filter(entry => 
      entry.timestamp > oneHourAgo
    );

    // Update errors per minute metric
    const oneMinuteAgo = now - 60000;
    this.metrics.errorsPerMinute = this.errorHistory.filter(entry =>
      entry.timestamp > oneMinuteAgo
    ).length;

    // Reset component states that haven't had errors recently
    for (const [component, state] of this.componentStates) {
      if (now - state.lastErrorTime > 300000) { // 5 minutes
        state.errorCount = Math.max(0, state.errorCount - 1);
        if (state.errorCount === 0) {
          state.hasError = false;
          state.circuitBreakerOpen = false;
        }
      }
    }

    this.metrics.lastCleanup = now;
  }

  /**
   * Sacred Metrics
   */
  getMetrics() {
    return {
      ...this.metrics,
      activeComponents: this.componentStates.size,
      circuitBreakersOpen: Array.from(this.componentStates.values())
        .filter(state => state.circuitBreakerOpen).length,
      componentsWithErrors: Array.from(this.componentStates.values())
        .filter(state => state.hasError).length
    };
  }

  getComponentState(component: string): SacredErrorState | null {
    return this.componentStates.get(component) || null;
  }

  isHealthy(): boolean {
    return (
      this.metrics.errorsPerMinute < ERROR_BOUNDARY_LIMITS.MAX_ERRORS_PER_MINUTE &&
      Array.from(this.componentStates.values())
        .filter(state => state.circuitBreakerOpen).length === 0
    );
  }
}

// Sacred Singleton Instance
let sacredErrorManagerInstance: SacredErrorManager | null = null;

export function useSacredErrorManager(): SacredErrorManager {
  if (!sacredErrorManagerInstance) {
    sacredErrorManagerInstance = new SacredErrorManager();
  }
  return sacredErrorManagerInstance;
}

// Sacred Vue Error Boundary Composable
export function useVueErrorBoundary(componentName?: string) {
  const errorManager = useSacredErrorManager();
  const instance = getCurrentInstance();
  const component = componentName || instance?.type.name || 'UnknownComponent';
  
  const errorState = ref<SacredErrorState>({
    hasError: false,
    errorCount: 0,
    lastError: null,
    lastErrorTime: 0,
    isRecovering: false,
    circuitBreakerOpen: false,
    retryCount: 0
  });

  // Sacred error capture
  onErrorCaptured((error: Error, instance, info: string) => {
    errorManager.recordError(error, component, info);
    
    // Update local state
    const state = errorManager.getComponentState(component);
    if (state) {
      errorState.value = { ...state };
    }

    // Prevent error propagation if circuit breaker is open
    return state?.circuitBreakerOpen || false;
  });

  const handleError = (error: Error, context?: string) => {
    errorManager.recordError(error, component, context);
    
    const state = errorManager.getComponentState(component);
    if (state) {
      errorState.value = { ...state };
    }
  };

  const recoverFromError = async (): Promise<boolean> => {
    const success = await errorManager.recoverFromError(component);
    
    const state = errorManager.getComponentState(component);
    if (state) {
      errorState.value = { ...state };
    }
    
    return success;
  };

  const wrapSacredOperation = async <T>(
    operation: () => Promise<T> | T,
    context?: string
  ): Promise<T | null> => {
    return errorManager.wrapSacredOperation(operation, component, context);
  };

  // Computed properties
  const isHealthy = computed(() => {
    return !errorState.value.hasError && !errorState.value.circuitBreakerOpen;
  });

  const statusMessage = computed(() => {
    if (errorState.value.circuitBreakerOpen) {
      return 'Sacred Protection: Circuit breaker active';
    }
    if (errorState.value.hasError) {
      return `Sacred Protection: ${errorState.value.errorCount} errors detected`;
    }
    return 'Sacred Protection: All systems operational';
  });

  return {
    errorState,
    isHealthy,
    statusMessage,
    handleError,
    recoverFromError,
    wrapSacredOperation,
    getMetrics: () => errorManager.getMetrics()
  };
}

// Sacred Global Error Handler
export function setupSacredGlobalErrorHandler(): void {
  const errorManager = useSacredErrorManager();

  // Handle unhandled promise rejections
  window.addEventListener('unhandledrejection', (event) => {
    errorManager.recordError(
      new Error(event.reason),
      'GlobalPromiseRejection',
      'unhandledrejection'
    );
    
    console.error('Sacred global promise rejection:', event.reason);
  });

  // Handle global errors
  window.addEventListener('error', (event) => {
    errorManager.recordError(
      event.error || new Error(event.message),
      'GlobalError',
      `${event.filename}:${event.lineno}:${event.colno}`
    );
    
    console.error('Sacred global error:', event.error);
  });
}

// Export sacred components
export { ERROR_BOUNDARY_LIMITS, SacredErrorManager };