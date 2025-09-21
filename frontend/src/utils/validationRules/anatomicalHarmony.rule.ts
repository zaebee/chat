export function validateAnatomicalHarmony(morphology: BeeMorphology, GOLDEN_RATIO: number): ValidationResult {
  const { abdomen, thorax, head } = morphology
  
  // Check size progression: head < thorax < abdomen
  const headSize = head.radius
  const thoraxSize = Math.sqrt(thorax.radius.x * thorax.radius.y)
  const abdomenSize = Math.sqrt(abdomen.radius.x * abdomen.radius.y)
  
  const properProgression = headSize < thoraxSize && thoraxSize < abdomenSize
  const sizeRatio = abdomenSize / headSize
  const idealRatio = GOLDEN_RATIO * GOLDEN_RATIO // φ²
  const ratioDeviation = Math.abs(sizeRatio - idealRatio) / idealRatio
  
  const passed = properProgression && ratioDeviation < 0.2
  const score = properProgression ? Math.max(0, 1 - ratioDeviation) : 0
  
  return {
    passed,
    score,
    message: passed
      ? '✅ Anatomical harmony achieved'
      : '⚠️ Body part proportions lack harmony',
    details: {
      headSize,
      thoraxSize,
      abdomenSize,
      sizeRatio,
      idealRatio,
      ratioDeviation,
      properProgression
    }
  }
}
