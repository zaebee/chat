/**
 * Sacred Asset Library - Main Entry Point
 * 
 * Centralized export for all ATCG assets and components.
 * Provides clean imports and maintains sacred separation.
 */

// Export ATCG component library
export * from './components'

// Export individual assets (to be properly typed in future PRs)
// export { default as HiveNavigationEnhancer } from './hive-interactive-navigation.js'
// export * from './tales_v2_implementation'

// Asset metadata and configuration
export const ASSET_METADATA = {
  version: '2.0.0',
  architecture: 'ATCG',
  principles: ['Sacred Separation', 'Component Purity', 'Architectural Independence'],
  location: 'frontend/src/assets/js/',
  buildSystem: 'Vite + TypeScript'
} as const

// Asset initialization function
export async function initializeAssets(): Promise<void> {
  console.log('🍯 Initializing Sacred Asset Library')
  console.log('📊 Metadata:', ASSET_METADATA)
  
  // Initialize ATCG component registry
  const { atcgRegistry } = await import('./components')
  await atcgRegistry.initializeAll()
  
  console.log('✅ Sacred Asset Library initialized')
}

// Asset cleanup function
export async function cleanupAssets(): Promise<void> {
  console.log('🧹 Cleaning up Sacred Asset Library')
  
  const { atcgRegistry } = await import('./components')
  await atcgRegistry.destroyAll()
  
  console.log('✅ Sacred Asset Library cleaned up')
}