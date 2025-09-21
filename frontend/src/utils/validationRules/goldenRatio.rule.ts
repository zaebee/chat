import type { BeeMorphology } from "@/utils/hivePhysics";
import type { ValidationResult } from "@/utils/physicsCocoon";

export function validateGoldenRatioCompliance(morphology: BeeMorphology, GOLDEN_RATIO: number, DIVINE_TOLERANCE: number): ValidationResult {
  const { abdomen, thorax, head, wings } = morphology
  
  // Check abdomen proportions
  const abdomenRatio = abdomen.radius.x / abdomen.radius.y
  const abdomenDeviation = Math.abs(abdomenRatio - (1 / GOLDEN_RATIO))
  
  // Check thorax proportions
  const thoraxRatio = thorax.radius.x / thorax.radius.y
  const thoraxDeviation = Math.abs(thoraxRatio - (1 / GOLDEN_RATIO))
  
  // Check wing proportions
  const wingRatio = wings.left.radius.x / wings.left.radius.y
  const wingDeviation = Math.abs(wingRatio - GOLDEN_RATIO)
  
  const totalDeviation = (abdomenDeviation + thoraxDeviation + wingDeviation) / 3
  const passed = totalDeviation < DIVINE_TOLERANCE
  const score = Math.max(0, 1 - (totalDeviation / DIVINE_TOLERANCE))
  
  return {
    passed,
    score,
    message: passed 
      ? '✨ Divine golden ratio proportions achieved'
      : `⚠️ Golden ratio deviation: ${(totalDeviation * 100).toFixed(2)}%`,
    details: {
      abdomenDeviation,
      thoraxDeviation,
      wingDeviation,
      totalDeviation
    }
  }
}