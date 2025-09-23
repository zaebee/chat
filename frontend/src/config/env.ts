/**
 * Environment Configuration for chat.zae.life
 * 
 * Configures API and WebSocket endpoints for HTTPS deployment
 */

interface EnvironmentConfig {
  API_BASE_URL: string;
  WS_BASE_URL: string;
  ENVIRONMENT: 'development' | 'production';
}

/**
 * Determines if we're in development mode based on hostname
 */
const isDevelopment = (): boolean => {
  if (typeof window === 'undefined') return false;
  
  const hostname = window.location.hostname;
  return hostname === 'localhost' || 
         hostname === '127.0.0.1' || 
         hostname.includes('gitpod.dev') ||
         hostname.includes('gitpod.io') ||
         hostname.includes('codespaces') ||
         hostname.startsWith('192.168.') ||
         hostname.startsWith('10.') ||
         hostname.startsWith('172.');
};

/**
 * Get environment configuration
 * 
 * Strategy:
 * - Check build-time environment variables first
 * - If VITE_API_HOST is set, use production mode with specified target
 * - Otherwise, fall back to runtime detection for development
 * 
 * Environment Variables:
 * - VITE_API_HOST: Target host for production (e.g., "chat.zae.life")
 * - VITE_API_PROTOCOL: Protocol for production (default: "https")
 * - VITE_FORCE_PRODUCTION: Force production mode even in dev environments
 */
const getEnvironmentConfig = (): EnvironmentConfig => {
  // Check if we have build-time configuration (production build)
  const buildTimeHost = import.meta.env.VITE_API_HOST;
  const buildTimeProtocol = import.meta.env.VITE_API_PROTOCOL;
  const forceProduction = import.meta.env.VITE_FORCE_PRODUCTION;
  
  // If we have build-time host configuration, use production mode
  if (buildTimeHost || forceProduction) {
    const targetHost = buildTimeHost || 'chat.zae.life';
    const targetProtocol = buildTimeProtocol || 'https';
    const wsProtocol = targetProtocol === 'https' ? 'wss' : 'ws';
    
    return {
      API_BASE_URL: `${targetProtocol}://${targetHost}`,
      WS_BASE_URL: `${wsProtocol}://${targetHost}`,
      ENVIRONMENT: 'production'
    };
  }
  
  // Fall back to runtime detection for development
  const isDevMode = isDevelopment();
  
  if (isDevMode) {
    // Development: Use backend port (8000) for API calls
    const protocol = window.location.protocol === 'https:' ? 'https:' : 'http:';
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const hostname = window.location.hostname;
    
    // In Gitpod, use the backend port URL pattern
    if (hostname.includes('gitpod.dev') || hostname.includes('gitpod.io')) {
      const backendHost = hostname.replace('5173--', '8000--');
      return {
        API_BASE_URL: `${protocol}//${backendHost}`,
        WS_BASE_URL: `${wsProtocol}//${backendHost}`,
        ENVIRONMENT: 'development'
      };
    }
    
    // For localhost, use port 8000
    return {
      API_BASE_URL: `${protocol}//${hostname}:8000`,
      WS_BASE_URL: `${wsProtocol}//${hostname}:8000`,
      ENVIRONMENT: 'development'
    };
  } else {
    // Production fallback
    return {
      API_BASE_URL: 'https://chat.zae.life',
      WS_BASE_URL: 'wss://chat.zae.life',
      ENVIRONMENT: 'production'
    };
  }
};

// Export the configuration
export const ENV_CONFIG = getEnvironmentConfig();

// Helper functions for common use cases
export const getApiUrl = (endpoint: string): string => {
  // Remove leading slash if present to avoid double slashes
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint.slice(1) : endpoint;
  return `${ENV_CONFIG.API_BASE_URL}/${cleanEndpoint}`;
};

export const getWebSocketUrl = (endpoint: string): string => {
  // Remove leading slash if present to avoid double slashes
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint.slice(1) : endpoint;
  return `${ENV_CONFIG.WS_BASE_URL}/${cleanEndpoint}`;
};

// Debug logging
console.log('🌿 Hive Environment Config:', {
  environment: ENV_CONFIG.ENVIRONMENT,
  apiBaseUrl: ENV_CONFIG.API_BASE_URL,
  wsBaseUrl: ENV_CONFIG.WS_BASE_URL,
  hostname: window.location.hostname,
  buildTimeVars: {
    VITE_API_HOST: import.meta.env.VITE_API_HOST || 'not set',
    VITE_API_PROTOCOL: import.meta.env.VITE_API_PROTOCOL || 'not set',
    VITE_FORCE_PRODUCTION: import.meta.env.VITE_FORCE_PRODUCTION || 'not set'
  }
});