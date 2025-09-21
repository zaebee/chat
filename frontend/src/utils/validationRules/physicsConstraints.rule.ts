import type { BeeMorphology } from "@/utils/hivePhysics";
import type { ValidationResult } from "@/utils/physicsCocoon";

export function validatePhysicsConstraints(morphology: BeeMorphology): ValidationResult {
  // Check for impossible geometries
  const viewBoxDimensions = morphology.viewBox.split(' ').slice(2).map(Number)
  const [width, height] = viewBoxDimensions
  
  // Ensure all elements fit within viewBox
  const { abdomen, thorax, head, wings } = morphology
  
  const maxX = Math.max(
    abdomen.center.x + abdomen.radius.x,
    thorax.center.x + thorax.radius.x,
    head.center.x + head.radius,
    wings.left.center.x + wings.left.radius.x,
    wings.right.center.x + wings.right.radius.x
  )
  
  const maxY = Math.max(
    abdomen.center.y + abdomen.radius.y,
    thorax.center.y + thorax.radius.y,
    head.center.y + head.radius,
    wings.left.center.y + wings.left.radius.y,
    wings.right.center.y + wings.right.radius.y
  )
  
  const fitsInViewBox = maxX <= width && maxY <= height
  const utilizationRatio = (maxX * maxY) / (width * height)
  
  const passed = fitsInViewBox && utilizationRatio > 0.3 && utilizationRatio < 0.9
  const score = fitsInViewBox ? Math.max(0, 1 - Math.abs(utilizationRatio - 0.6) / 0.3) : 0
  
  return {
    passed,
    score,
    message: passed
      ? '✅ Physics constraints satisfied'
      : fitsInViewBox 
        ? '⚠️ Suboptimal space utilization'
        : '❌ Elements exceed viewBox boundaries',
    details: {
      viewBoxWidth: width,
      viewBoxHeight: height,
      maxX,
      maxY,
      fitsInViewBox,
      utilizationRatio
    }
  }
}
