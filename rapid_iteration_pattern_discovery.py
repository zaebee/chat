#!/usr/bin/env python3
"""
Rapid Iteration Cycle for Pattern Discovery

Implements high-speed pattern discovery with iterative refinement,
optimized for deep dive short sessions with [🔲,⬢⬡⬢⬡⬢⬡] <-> (🔲🔲🔲,⬢⬡⬢⬡⬢⬡⬢⬡⬢) paradigm integration.
"""

import asyncio
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
import json


@dataclass
class DiscoveryIteration:
    """Single iteration in rapid discovery cycle"""
    iteration_id: str
    start_time: datetime
    focus_area: str
    patterns_discovered: List[Dict[str, Any]] = field(default_factory=list)
    insights: List[str] = field(default_factory=list)
    next_focus_hint: Optional[str] = None
    duration_ms: int = 0
    quality_score: float = 0.0


@dataclass
class PatternSignature:
    """Unique signature for discovered patterns"""
    pattern_type: str
    complexity_level: int
    paradigm_alignment: str  # rect, hexa, or hybrid
    confidence: float
    discovery_timestamp: datetime


class RapidPatternDiscovery:
    """High-speed pattern discovery engine"""
    
    def __init__(self):
        self.discovery_cache = {}
        self.iteration_history = []
        self.pattern_library = {}
        self.speed_optimization = True
        self.max_iteration_time_ms = 2000  # 2 seconds per iteration
        
    async def rapid_discovery_cycle(self, target_data: Dict[str, Any], max_iterations: int = 5) -> List[DiscoveryIteration]:
        """Execute rapid discovery cycle with iterative refinement"""
        print(f"🚀 Starting rapid discovery cycle (max {max_iterations} iterations)")
        
        iterations = []
        current_focus = "architecture_overview"
        
        for i in range(max_iterations):
            iteration_start = datetime.now()
            iteration_id = f"iter_{i+1}_{int(time.time())}"
            
            print(f"\n⚡ Iteration {i+1}: {current_focus}")
            
            # Execute single rapid iteration
            iteration = await self._execute_rapid_iteration(
                iteration_id, target_data, current_focus
            )
            
            # Calculate iteration duration
            iteration.duration_ms = int((datetime.now() - iteration_start).total_seconds() * 1000)
            
            # Evaluate iteration quality
            iteration.quality_score = self._evaluate_iteration_quality(iteration)
            
            iterations.append(iteration)
            
            print(f"   ✅ Completed in {iteration.duration_ms}ms")
            print(f"   📊 Quality: {iteration.quality_score:.2f}")
            print(f"   🔍 Patterns: {len(iteration.patterns_discovered)}")
            
            # Determine next focus based on current results
            current_focus = iteration.next_focus_hint or self._determine_next_focus(iterations)
            
            # Early termination if quality threshold met
            if iteration.quality_score > 0.9:
                print(f"   🎯 High quality threshold reached, terminating early")
                break
        
        return iterations
    
    async def _execute_rapid_iteration(self, iteration_id: str, data: Dict[str, Any], focus: str) -> DiscoveryIteration:
        """Execute single rapid iteration"""
        start_time = datetime.now()
        
        iteration = DiscoveryIteration(
            iteration_id=iteration_id,
            start_time=start_time,
            focus_area=focus
        )
        
        # Rapid pattern scanning based on focus area
        if focus == "architecture_overview":
            patterns = await self._scan_architecture_patterns(data)
        elif focus == "data_structures":
            patterns = await self._scan_data_structure_patterns(data)
        elif focus == "workflow_patterns":
            patterns = await self._scan_workflow_patterns(data)
        elif focus == "integration_points":
            patterns = await self._scan_integration_patterns(data)
        elif focus == "paradigm_alignment":
            patterns = await self._scan_paradigm_alignment(data)
        else:
            patterns = await self._scan_general_patterns(data)
        
        iteration.patterns_discovered = patterns
        
        # Generate insights from discovered patterns
        iteration.insights = self._generate_rapid_insights(patterns, focus)
        
        # Determine next focus hint
        iteration.next_focus_hint = self._suggest_next_focus(patterns, focus)
        
        return iteration
    
    async def _scan_architecture_patterns(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Scan for architectural patterns"""
        patterns = []
        
        # Check for Jekyll/static site patterns
        if "jekyll" in str(data).lower() or "_config" in str(data):
            patterns.append({
                "type": "static_site_generator",
                "framework": "jekyll",
                "confidence": 0.9,
                "paradigm": "rect",
                "characteristics": ["structured", "templated", "build_process"]
            })
        
        # Check for GitHub workflow patterns
        if "github" in str(data).lower() and "workflow" in str(data).lower():
            patterns.append({
                "type": "ci_cd_pipeline",
                "platform": "github_actions",
                "confidence": 0.85,
                "paradigm": "rect",
                "characteristics": ["automated", "event_driven", "yaml_configured"]
            })
        
        # Check for documentation patterns
        if "docs" in str(data).lower() or "documentation" in str(data).lower():
            patterns.append({
                "type": "documentation_system",
                "approach": "structured_docs",
                "confidence": 0.8,
                "paradigm": "hybrid",
                "characteristics": ["hierarchical", "cross_referenced", "searchable"]
            })
        
        return patterns
    
    async def _scan_data_structure_patterns(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Scan for data structure patterns"""
        patterns = []
        
        # Check for YAML data patterns
        if "yml" in str(data).lower() or "yaml" in str(data).lower():
            patterns.append({
                "type": "yaml_configuration",
                "structure": "hierarchical",
                "confidence": 0.9,
                "paradigm": "rect",
                "characteristics": ["structured", "human_readable", "configurable"]
            })
        
        # Check for JSON data patterns
        if "json" in str(data).lower():
            patterns.append({
                "type": "json_data",
                "structure": "nested",
                "confidence": 0.85,
                "paradigm": "rect",
                "characteristics": ["machine_readable", "api_friendly", "structured"]
            })
        
        # Check for bilingual patterns
        if ("en" in str(data) and "ru" in str(data)) or "bilingual" in str(data).lower():
            patterns.append({
                "type": "bilingual_data",
                "languages": ["en", "ru"],
                "confidence": 0.95,
                "paradigm": "hexa",
                "characteristics": ["adaptive", "localized", "dynamic"]
            })
        
        return patterns
    
    async def _scan_workflow_patterns(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Scan for workflow patterns"""
        patterns = []
        
        # Check for deployment workflows
        if "deploy" in str(data).lower() or "pages" in str(data).lower():
            patterns.append({
                "type": "deployment_workflow",
                "target": "github_pages",
                "confidence": 0.9,
                "paradigm": "rect",
                "characteristics": ["automated", "triggered", "validated"]
            })
        
        # Check for build workflows
        if "build" in str(data).lower() or "bundle" in str(data).lower():
            patterns.append({
                "type": "build_workflow",
                "process": "static_generation",
                "confidence": 0.8,
                "paradigm": "rect",
                "characteristics": ["compilation", "optimization", "artifact_generation"]
            })
        
        return patterns
    
    async def _scan_integration_patterns(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Scan for integration patterns"""
        patterns = []
        
        # Check for interactive enhancement patterns
        if "interactive" in str(data).lower() or "navigation" in str(data).lower():
            patterns.append({
                "type": "interactive_enhancement",
                "layer": "javascript",
                "confidence": 0.85,
                "paradigm": "hexa",
                "characteristics": ["dynamic", "user_responsive", "progressive_enhancement"]
            })
        
        # Check for visual integration patterns
        if "mermaid" in str(data).lower() or "diagram" in str(data).lower():
            patterns.append({
                "type": "visual_integration",
                "technology": "mermaid",
                "confidence": 0.9,
                "paradigm": "hexa",
                "characteristics": ["visual", "interactive", "code_generated"]
            })
        
        return patterns
    
    async def _scan_paradigm_alignment(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Scan for paradigm alignment patterns"""
        patterns = []
        
        # Analyze rect vs hexa characteristics
        rect_indicators = ["structure", "constraint", "validation", "compliance"]
        hexa_indicators = ["adaptive", "flexible", "interactive", "dynamic"]
        
        rect_score = sum(1 for indicator in rect_indicators if indicator in str(data).lower())
        hexa_score = sum(1 for indicator in hexa_indicators if indicator in str(data).lower())
        
        if rect_score > hexa_score:
            patterns.append({
                "type": "paradigm_alignment",
                "primary": "rectangular",
                "confidence": rect_score / (rect_score + hexa_score),
                "paradigm": "rect",
                "characteristics": ["structured", "constrained", "predictable"]
            })
        elif hexa_score > rect_score:
            patterns.append({
                "type": "paradigm_alignment", 
                "primary": "hexagonal",
                "confidence": hexa_score / (rect_score + hexa_score),
                "paradigm": "hexa",
                "characteristics": ["adaptive", "flexible", "dynamic"]
            })
        else:
            patterns.append({
                "type": "paradigm_alignment",
                "primary": "hybrid",
                "confidence": 0.7,
                "paradigm": "hybrid",
                "characteristics": ["balanced", "multi_paradigm", "integrated"]
            })
        
        return patterns
    
    async def _scan_general_patterns(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Scan for general patterns"""
        patterns = []
        
        # Generic pattern detection
        patterns.append({
            "type": "general_structure",
            "complexity": len(str(data)) // 1000,  # Rough complexity measure
            "confidence": 0.6,
            "paradigm": "unknown",
            "characteristics": ["data_present", "structured_content"]
        })
        
        return patterns
    
    def _generate_rapid_insights(self, patterns: List[Dict[str, Any]], focus: str) -> List[str]:
        """Generate insights from discovered patterns"""
        insights = []
        
        if not patterns:
            insights.append(f"No clear patterns detected in {focus} - may need different approach")
            return insights
        
        # Pattern count insights
        insights.append(f"Discovered {len(patterns)} patterns in {focus} area")
        
        # Paradigm distribution insights
        paradigms = [p.get("paradigm", "unknown") for p in patterns]
        paradigm_counts = {p: paradigms.count(p) for p in set(paradigms)}
        
        if paradigm_counts:
            dominant_paradigm = max(paradigm_counts, key=paradigm_counts.get)
            insights.append(f"Dominant paradigm: {dominant_paradigm} ({paradigm_counts[dominant_paradigm]} patterns)")
        
        # Confidence insights
        confidences = [p.get("confidence", 0) for p in patterns]
        if confidences:
            avg_confidence = sum(confidences) / len(confidences)
            insights.append(f"Average pattern confidence: {avg_confidence:.2f}")
        
        # Specific pattern insights
        pattern_types = [p.get("type", "unknown") for p in patterns]
        unique_types = set(pattern_types)
        
        if len(unique_types) > 1:
            insights.append(f"Pattern diversity: {len(unique_types)} different types detected")
        
        # Focus-specific insights
        if focus == "architecture_overview":
            if any("static_site" in p.get("type", "") for p in patterns):
                insights.append("Static site architecture detected - good for documentation")
        elif focus == "data_structures":
            if any("bilingual" in p.get("type", "") for p in patterns):
                insights.append("Bilingual data structure - enables internationalization")
        
        return insights
    
    def _suggest_next_focus(self, patterns: List[Dict[str, Any]], current_focus: str) -> Optional[str]:
        """Suggest next focus area based on current patterns"""
        
        # Focus progression logic
        focus_progression = {
            "architecture_overview": "data_structures",
            "data_structures": "workflow_patterns", 
            "workflow_patterns": "integration_points",
            "integration_points": "paradigm_alignment",
            "paradigm_alignment": None  # End of cycle
        }
        
        # Check if current focus revealed specific patterns that suggest different direction
        for pattern in patterns:
            pattern_type = pattern.get("type", "")
            
            if "bilingual" in pattern_type and current_focus != "data_structures":
                return "data_structures"
            elif "workflow" in pattern_type and current_focus != "workflow_patterns":
                return "workflow_patterns"
            elif "interactive" in pattern_type and current_focus != "integration_points":
                return "integration_points"
        
        # Default progression
        return focus_progression.get(current_focus)
    
    def _determine_next_focus(self, iterations: List[DiscoveryIteration]) -> str:
        """Determine next focus based on iteration history"""
        if not iterations:
            return "architecture_overview"
        
        last_iteration = iterations[-1]
        
        # If last iteration had low quality, try different approach
        if last_iteration.quality_score < 0.5:
            focus_alternatives = {
                "architecture_overview": "data_structures",
                "data_structures": "integration_points",
                "workflow_patterns": "paradigm_alignment",
                "integration_points": "architecture_overview",
                "paradigm_alignment": "workflow_patterns"
            }
            return focus_alternatives.get(last_iteration.focus_area, "general_patterns")
        
        # Use suggested next focus
        return last_iteration.next_focus_hint or "general_patterns"
    
    def _evaluate_iteration_quality(self, iteration: DiscoveryIteration) -> float:
        """Evaluate quality of discovery iteration"""
        quality_factors = []
        
        # Pattern count factor (more patterns = higher quality, up to a point)
        pattern_count = len(iteration.patterns_discovered)
        pattern_factor = min(pattern_count / 5.0, 1.0)  # Optimal around 5 patterns
        quality_factors.append(pattern_factor)
        
        # Confidence factor (average confidence of patterns)
        if iteration.patterns_discovered:
            confidences = [p.get("confidence", 0) for p in iteration.patterns_discovered]
            confidence_factor = sum(confidences) / len(confidences)
            quality_factors.append(confidence_factor)
        else:
            quality_factors.append(0.0)
        
        # Insight factor (number of insights generated)
        insight_count = len(iteration.insights)
        insight_factor = min(insight_count / 3.0, 1.0)  # Optimal around 3 insights
        quality_factors.append(insight_factor)
        
        # Time factor (faster is better, up to a point)
        time_factor = max(0.0, 1.0 - (iteration.duration_ms / self.max_iteration_time_ms))
        quality_factors.append(time_factor)
        
        # Calculate weighted average
        weights = [0.3, 0.4, 0.2, 0.1]  # Pattern, confidence, insight, time
        quality_score = sum(f * w for f, w in zip(quality_factors, weights))
        
        return min(quality_score, 1.0)


async def demo_rapid_iteration_discovery():
    """Demonstrate rapid iteration pattern discovery"""
    print("⚡ Rapid Iteration Pattern Discovery Demo")
    print("=" * 50)
    
    # Initialize discovery engine
    discovery = RapidPatternDiscovery()
    
    # Simulate medicine.git data for discovery
    medicine_data = {
        "repository": "medicine.git",
        "structure": {
            "docs": {
                "_config.yml": "Jekyll configuration",
                "_data/glossary.yml": "Bilingual glossary data",
                "architecture-overview.md": "Mermaid diagrams",
                "interactive-navigation.js": "Interactive enhancement"
            },
            ".github/workflows": {
                "pages.yml": "GitHub Pages deployment"
            },
            "business": {
                "project_data.json": "Structured requirements"
            }
        },
        "technologies": ["jekyll", "github_pages", "mermaid", "yaml", "json"],
        "features": ["bilingual", "interactive", "responsive", "documentation"]
    }
    
    print(f"\n📥 Target Data: {medicine_data['repository']}")
    print(f"   Technologies: {', '.join(medicine_data['technologies'])}")
    print(f"   Features: {', '.join(medicine_data['features'])}")
    
    # Execute rapid discovery cycle
    start_time = time.time()
    iterations = await discovery.rapid_discovery_cycle(medicine_data, max_iterations=5)
    total_time = time.time() - start_time
    
    print(f"\n📊 Discovery Cycle Complete")
    print(f"   Total Time: {total_time:.2f}s")
    print(f"   Iterations: {len(iterations)}")
    
    # Analyze results
    total_patterns = sum(len(iter.patterns_discovered) for iter in iterations)
    total_insights = sum(len(iter.insights) for iter in iterations)
    avg_quality = sum(iter.quality_score for iter in iterations) / len(iterations)
    
    print(f"   Total Patterns: {total_patterns}")
    print(f"   Total Insights: {total_insights}")
    print(f"   Average Quality: {avg_quality:.2f}")
    
    # Show iteration details
    print(f"\n🔍 Iteration Details:")
    for i, iteration in enumerate(iterations, 1):
        print(f"   Iteration {i}: {iteration.focus_area}")
        print(f"     Duration: {iteration.duration_ms}ms")
        print(f"     Quality: {iteration.quality_score:.2f}")
        print(f"     Patterns: {len(iteration.patterns_discovered)}")
        print(f"     Insights: {len(iteration.insights)}")
        
        # Show key insights
        if iteration.insights:
            print(f"     Key Insight: {iteration.insights[0]}")
    
    # Show discovered pattern summary
    print(f"\n🎯 Pattern Summary:")
    all_patterns = []
    for iteration in iterations:
        all_patterns.extend(iteration.patterns_discovered)
    
    pattern_types = {}
    paradigm_distribution = {}
    
    for pattern in all_patterns:
        ptype = pattern.get("type", "unknown")
        paradigm = pattern.get("paradigm", "unknown")
        
        pattern_types[ptype] = pattern_types.get(ptype, 0) + 1
        paradigm_distribution[paradigm] = paradigm_distribution.get(paradigm, 0) + 1
    
    print(f"   Pattern Types: {dict(pattern_types)}")
    print(f"   Paradigm Distribution: {dict(paradigm_distribution)}")
    
    print(f"\n⚡ Rapid iteration discovery complete!")
    print(f"   Ready for high-level architecture integration")


if __name__ == "__main__":
    asyncio.run(demo_rapid_iteration_discovery())