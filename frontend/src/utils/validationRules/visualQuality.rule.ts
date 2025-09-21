import type { BeeMorphology } from "@/utils/hivePhysics";
import type { ValidationResult } from "@/utils/physicsCocoon";

export function validateVisualQuality(morphology: BeeMorphology, GOLDEN_RATIO: number): ValidationResult {
  // Check for visual coherence and aesthetic quality
  const { abdomen, thorax, head, wings } = morphology
  
  // Symmetry check
  const leftWing = wings.left
  const rightWing = wings.right
  const wingSymmetry = Math.abs(leftWing.radius.x - rightWing.radius.x) < 0.1 &&
                      Math.abs(leftWing.radius.y - rightWing.radius.y) < 0.1
  
  // Alignment check
  const centerAlignment = Math.abs(abdomen.center.x - thorax.center.x) < 1 &&
                         Math.abs(thorax.center.x - head.center.x) < 1
  
  // Proportion balance
  const totalArea = (abdomen.radius.x * abdomen.radius.y * Math.PI) +
                   (thorax.radius.x * thorax.radius.y * Math.PI) +
                   (head.radius * head.radius * Math.PI)
  const wingArea = (leftWing.radius.x * leftWing.radius.y * Math.PI * 2)
  const wingToBodyRatio = wingArea / totalArea
  const idealWingRatio = 1 / GOLDEN_RATIO // Wings should be φ⁻¹ of body
  const wingRatioDeviation = Math.abs(wingToBodyRatio - idealWingRatio) / idealWingRatio
  
  const qualityFactors = [wingSymmetry, centerAlignment, wingRatioDeviation < 0.2]
  const passed = qualityFactors.filter(Boolean).length >= 2
  const score = qualityFactors.filter(Boolean).length / qualityFactors.length
  
  return {
    passed,
    score,
    message: passed
      ? '✅ Visual quality standards met'
      : '⚠️ Visual quality could be improved',
    details: {
      wingSymmetry,
      centerAlignment,
      wingToBodyRatio,
      idealWingRatio,
      wingRatioDeviation,
      qualityScore: score
    }
  }
}