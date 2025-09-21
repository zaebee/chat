import type { BeeMorphology } from "@/utils/hivePhysics";
import type { ValidationResult } from "@/utils/physicsCocoon";

export function validateDivineTranscendence(morphology: BeeMorphology): ValidationResult {
  // Check if this is a divine bee based on special features
  const hasDivineFeatures = Object.keys(morphology.specialFeatures).length > 0
  
  if (!hasDivineFeatures) {
    return {
      passed: true,
      score: 1,
      message: '✅ Non-divine bee - transcendence not required'
    }
  }
  
  // For divine bees, check transcendent properties
  const hasAura = 'divineAura' in morphology.specialFeatures
  const hasScroll = 'scroll' in morphology.specialFeatures
  const hasAntenna = 'antenna' in morphology.specialFeatures
  const hasCrown = 'crown' in morphology.specialFeatures
  
  const transcendentFeatures = [hasAura, hasScroll, hasAntenna, hasCrown].filter(Boolean).length
  const passed = transcendentFeatures > 0
  const score = transcendentFeatures / 4 // Max 4 possible features
  
  return {
    passed,
    score,
    message: passed
      ? `✨ Divine transcendence manifested (${transcendentFeatures} features)`
      : '❌ Divine bee lacks transcendent features',
    details: {
      hasAura,
      hasScroll,
      hasAntenna,
      hasCrown,
      transcendentFeatures
    }
  }
}
