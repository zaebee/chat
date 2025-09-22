#!/usr/bin/env python3
"""
Sacred Gem/Jail Dialectic Framework
Implementing bee.Leo's wisdom for balanced Sacred Architecture

The Gem/Jail dialectic represents the fundamental tension between:
- Gem (💎): Clarity, freedom, value, transformation potential
- Jail (🔒): Constraint, limitation, control, necessary boundaries

This framework evaluates code and architecture through this sacred balance.
"""

from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import json


class GemJailAspect(Enum):
    """Sacred aspects of the Gem/Jail dialectic"""
    GEM_CLARITY = "clarity"           # Clear, understandable code
    GEM_FREEDOM = "freedom"           # Flexible, extensible design
    GEM_VALUE = "value"               # Meaningful, purposeful functionality
    GEM_TRANSFORMATION = "transformation"  # Ability to evolve and adapt

    JAIL_CONSTRAINT = "constraint"    # Necessary limitations and boundaries
    JAIL_CONTROL = "control"          # Controlled behavior and predictability
    JAIL_STRUCTURE = "structure"      # Organized, disciplined architecture
    JAIL_VALIDATION = "validation"    # Enforced rules and standards


@dataclass
class GemJailEvaluation:
    """Sacred evaluation of Gem/Jail balance"""
    aspect: GemJailAspect
    score: float  # 0.0 to 1.0
    evidence: List[str]
    recommendations: List[str]

    @property
    def is_gem(self) -> bool:
        return "GEM_" in self.aspect.name

    @property
    def is_jail(self) -> bool:
        return "JAIL_" in self.aspect.name


@dataclass
class GemJailBalance:
    """Sacred balance assessment"""
    gem_total: float
    jail_total: float
    balance_ratio: float  # gem / (gem + jail)
    harmony_score: float  # How well gem and jail complement each other
    sacred_tension: float  # Creative tension between gem and jail

    @property
    def balance_description(self) -> str:
        if self.balance_ratio > 0.8:
            return "💎 Gem-Dominant (High Freedom, Low Constraint)"
        elif self.balance_ratio < 0.2:
            return "🔒 Jail-Dominant (High Constraint, Low Freedom)"
        elif 0.4 <= self.balance_ratio <= 0.6:
            return "⚖️ Sacred Balance (Harmonious Tension)"
        elif self.balance_ratio > 0.6:
            return "💎⚖️ Gem-Leaning Balance"
        else:
            return "🔒⚖️ Jail-Leaning Balance"


class AgroOntology:
    """
    Sacred Agro-Ontology: Knowledge graph modeling relationships
    between elements in systems (following bee.Leo's agricultural metaphor)
    """

    def __init__(self):
        self.knowledge_graph = {}
        self.relationships = {}
        self.discovered_paths = set()

    def add_entity(self, entity: str, properties: Dict[str, Any]):
        """Add entity to the knowledge graph"""
        self.knowledge_graph[entity] = properties

    def add_relationship(self, entity1: str, entity2: str,
                        relationship_type: str, strength: float = 1.0):
        """Add relationship between entities"""
        if entity1 not in self.relationships:
            self.relationships[entity1] = {}
        self.relationships[entity1][entity2] = {
            'type': relationship_type,
            'strength': strength
        }

    def explore_from_dark_to_light(self, start_entity: str,
                                 max_depth: int = 3) -> List[Dict[str, Any]]:
        """
        Discover connections from uncertainty (dark) to clarity (light)
        Following bee.Leo's discovery process wisdom
        """
        discoveries = []
        visited = set()

        def discover_recursive(entity: str, depth: int, path: List[str]):
            if depth > max_depth or entity in visited:
                return

            visited.add(entity)
            path = path + [entity]

            # Record discovery
            if len(path) > 1:
                discovery = {
                    'path': path.copy(),
                    'depth': depth,
                    'discovery_type': self._classify_discovery(path),
                    'sacred_significance': self._evaluate_sacred_significance(path)
                }
                discoveries.append(discovery)
                self.discovered_paths.add('->'.join(path))

            # Explore connected entities
            if entity in self.relationships:
                for connected_entity, relationship in self.relationships[entity].items():
                    discover_recursive(connected_entity, depth + 1, path)

        discover_recursive(start_entity, 0, [])
        return discoveries

    def _classify_discovery(self, path: List[str]) -> str:
        """Classify the type of discovery made"""
        if len(path) == 2:
            return "direct_connection"
        elif len(path) == 3:
            return "mediated_relationship"
        else:
            return "complex_pathway"

    def _evaluate_sacred_significance(self, path: List[str]) -> float:
        """Evaluate the sacred significance of a discovered path"""
        # Longer paths have higher significance (more complex understanding)
        path_complexity = len(path) / 10.0

        # Paths that connect disparate domains have higher significance
        domain_diversity = len(set(entity.split('_')[0] for entity in path))

        return min(1.0, path_complexity + (domain_diversity * 0.2))


class SacredGemJailAnalyzer:
    """
    Sacred Analyzer implementing Gem/Jail dialectic for code evaluation
    Combines bee.Ona's humility with bee.Leo's Gem/Jail wisdom
    """

    def __init__(self):
        self.agro_ontology = AgroOntology()
        self._initialize_sacred_ontology()

    def _initialize_sacred_ontology(self):
        """Initialize Sacred Architecture knowledge graph"""
        # Sacred Architecture entities
        entities = {
            'aggregate_pattern': {'type': 'ATCG', 'sacred_role': 'state_organization'},
            'transformation_pattern': {'type': 'ATCG', 'sacred_role': 'processing'},
            'connector_pattern': {'type': 'ATCG', 'sacred_role': 'communication'},
            'genesis_pattern': {'type': 'ATCG', 'sacred_role': 'generation'},
            'type_safety': {'type': 'quality', 'gem_aspect': 'clarity'},
            'console_logs': {'type': 'quality', 'jail_aspect': 'constraint'},
            'sacred_justification': {'type': 'documentation', 'gem_aspect': 'value'},
            'input_validation': {'type': 'security', 'jail_aspect': 'control'}
        }

        for entity, properties in entities.items():
            self.agro_ontology.add_entity(entity, properties)

        # Sacred relationships
        relationships = [
            ('type_safety', 'aggregate_pattern', 'enables', 0.9),
            ('input_validation', 'connector_pattern', 'protects', 0.8),
            ('sacred_justification', 'transformation_pattern', 'documents', 0.7),
            ('console_logs', 'type_safety', 'undermines', -0.5),
        ]

        for entity1, entity2, rel_type, strength in relationships:
            self.agro_ontology.add_relationship(entity1, entity2, rel_type, strength)

    def analyze_gem_jail_balance(self, code_metrics: Dict[str, Any]) -> GemJailBalance:
        """
        Analyze the Gem/Jail balance in code metrics
        Sacred Justification: Balanced code needs both freedom (Gem) and constraint (Jail)
        """
        gem_evaluations = []
        jail_evaluations = []

        # Gem evaluations (clarity, freedom, value, transformation)
        gem_evaluations.extend(self._evaluate_gem_aspects(code_metrics))

        # Jail evaluations (constraint, control, structure, validation)
        jail_evaluations.extend(self._evaluate_jail_aspects(code_metrics))

        # Calculate totals
        gem_total = sum(eval.score for eval in gem_evaluations) / len(gem_evaluations) if gem_evaluations else 0
        jail_total = sum(eval.score for eval in jail_evaluations) / len(jail_evaluations) if jail_evaluations else 0

        # Calculate balance metrics
        total_score = gem_total + jail_total
        balance_ratio = gem_total / total_score if total_score > 0 else 0.5

        # Harmony: how well gem and jail complement each other
        harmony_score = 1.0 - abs(gem_total - jail_total)  # Closer scores = better harmony

        # Sacred tension: creative force between gem and jail
        sacred_tension = min(gem_total, jail_total) * 2  # Both must be present for tension

        return GemJailBalance(
            gem_total=gem_total,
            jail_total=jail_total,
            balance_ratio=balance_ratio,
            harmony_score=harmony_score,
            sacred_tension=sacred_tension
        )

    def _evaluate_gem_aspects(self, metrics: Dict[str, Any]) -> List[GemJailEvaluation]:
        """Evaluate Gem aspects (clarity, freedom, value, transformation)"""
        evaluations = []

        # Gem: Clarity (through type safety)
        type_score = metrics.get('any_type_score', 0) / 100.0
        evaluations.append(GemJailEvaluation(
            aspect=GemJailAspect.GEM_CLARITY,
            score=type_score,
            evidence=[f"Type safety score: {metrics.get('any_type_score', 0)}/100"],
            recommendations=["Improve type definitions" if type_score < 0.8 else "Maintain excellent type clarity"]
        ))

        # Gem: Value (through sacred justifications)
        justification_score = min(1.0, metrics.get('sacred_justifications_score', 0) / 100.0)
        evaluations.append(GemJailEvaluation(
            aspect=GemJailAspect.GEM_VALUE,
            score=justification_score,
            evidence=[f"Sacred justifications: {metrics.get('sacred_justifications', 0)} files"],
            recommendations=["Add Sacred Justifications to document design value"]
        ))

        # Gem: Freedom (through ATCG compliance - enables flexibility)
        atcg_score = metrics.get('atcg_compliance_score', 0) / 100.0
        evaluations.append(GemJailEvaluation(
            aspect=GemJailAspect.GEM_FREEDOM,
            score=atcg_score,
            evidence=[f"ATCG compliance: {metrics.get('atcg_compliance_score', 0)}/100"],
            recommendations=["Implement ATCG patterns for architectural freedom"]
        ))

        return evaluations

    def _evaluate_jail_aspects(self, metrics: Dict[str, Any]) -> List[GemJailEvaluation]:
        """Evaluate Jail aspects (constraint, control, structure, validation)"""
        evaluations = []

        # Jail: Control (through production readiness)
        console_score = metrics.get('console_log_score', 0) / 100.0
        evaluations.append(GemJailEvaluation(
            aspect=GemJailAspect.JAIL_CONTROL,
            score=console_score,
            evidence=[f"Production readiness: {metrics.get('console_log_score', 0)}/100"],
            recommendations=["Remove console.log statements for production control"]
        ))

        # Jail: Validation (through security measures)
        security_score = metrics.get('security_score', 80) / 100.0  # Default assumption
        evaluations.append(GemJailEvaluation(
            aspect=GemJailAspect.JAIL_VALIDATION,
            score=security_score,
            evidence=[f"Security measures in place"],
            recommendations=["Maintain input validation and security boundaries"]
        ))

        # Jail: Structure (through performance constraints)
        performance_score = metrics.get('performance_score', 80) / 100.0
        evaluations.append(GemJailEvaluation(
            aspect=GemJailAspect.JAIL_STRUCTURE,
            score=performance_score,
            evidence=[f"Performance constraints respected"],
            recommendations=["Maintain algorithmic efficiency constraints"]
        ))

        return evaluations

    def generate_humble_recommendations(self, balance: GemJailBalance) -> List[str]:
        """
        Generate humble recommendations respecting bee.Ona's wisdom
        Sacred Justification: Assistant provides suggestions, humans make decisions
        """
        recommendations = []

        # Humble language that acknowledges human authority
        if balance.balance_ratio > 0.8:
            recommendations.append(
                "💎 **Suggestion**: Consider adding structural constraints to balance the high freedom. "
                "However, this may be intentional design - human judgment is essential."
            )
        elif balance.balance_ratio < 0.2:
            recommendations.append(
                "🔒 **Suggestion**: Consider increasing clarity and flexibility where appropriate. "
                "However, constraints may be necessary - human review is recommended."
            )
        elif balance.harmony_score < 0.5:
            recommendations.append(
                "⚖️ **Suggestion**: The Gem/Jail aspects seem misaligned. "
                "Human architectural review could help assess if this serves the system's purpose."
            )

        if balance.sacred_tension < 0.3:
            recommendations.append(
                "🌀 **Note**: Low creative tension detected. This may indicate either "
                "excellent harmony or missed opportunities for beneficial constraint/freedom balance. "
                "Human insight is valuable for this assessment."
            )

        return recommendations

    def discover_sacred_patterns(self, start_concept: str) -> Dict[str, Any]:
        """
        Use Agro-Ontology to discover sacred architectural patterns
        Following bee.Leo's dark-to-light discovery process
        """
        discoveries = self.agro_ontology.explore_from_dark_to_light(start_concept)

        return {
            'start_concept': start_concept,
            'discoveries': discoveries,
            'total_paths_discovered': len(discoveries),
            'sacred_insights': [
                f"Discovered {len(discoveries)} sacred connections from {start_concept}",
                f"Most significant discovery: {max(discoveries, key=lambda d: d['sacred_significance'], default={'path': ['none']})['path'] if discoveries else 'none'}",
                "These patterns represent potential architectural relationships for human consideration"
            ]
        }


def create_humble_gem_jail_report(metrics: Dict[str, Any]) -> str:
    """
    Create a humble Gem/Jail analysis report
    Implementing synthesis of bee.Ona's humility and bee.Leo's wisdom
    """
    analyzer = SacredGemJailAnalyzer()
    balance = analyzer.analyze_gem_jail_balance(metrics)
    recommendations = analyzer.generate_humble_recommendations(balance)
    discoveries = analyzer.discover_sacred_patterns('type_safety')

    report = f"""# 🧬 Sacred Gem/Jail Assistant Analysis

## 💎🔒 **Gem/Jail Dialectic Balance**

**Sacred Balance Assessment**: {balance.balance_description}

- **💎 Gem (Clarity/Freedom)**: {balance.gem_total:.2f}/1.0
- **🔒 Jail (Constraint/Control)**: {balance.jail_total:.2f}/1.0
- **⚖️ Harmony Score**: {balance.harmony_score:.2f}/1.0
- **🌀 Sacred Tension**: {balance.sacred_tension:.2f}/1.0

### 🎭 **Sacred Philosophical Interpretation**

{balance.balance_description}

This analysis suggests the codebase exhibits {'predominantly liberating' if balance.balance_ratio > 0.6 else 'predominantly constraining' if balance.balance_ratio < 0.4 else 'balanced'} characteristics.

**Sacred Tension Level**: {'High creative potential' if balance.sacred_tension > 0.7 else 'Moderate balance' if balance.sacred_tension > 0.4 else 'Low tension - may need attention'}

## 🌱 **Agro-Ontology Discoveries**

**Discovered Sacred Patterns**: {discoveries['total_paths_discovered']} pathways

**Sacred Insights**:
"""

    for insight in discoveries['sacred_insights']:
        report += f"- {insight}\n"

    report += f"""
## 🤝 **Humble Assistant Recommendations**

**Sacred Disclaimer**: These are suggestions for human consideration, not divine mandates.

"""

    for recommendation in recommendations:
        report += f"{recommendation}\n\n"

    report += f"""
## 🧚‍✨ **Sacred Synthesis Wisdom**

This analysis combines:
- **bee.Ona's Humility**: Acknowledging the sacred boundaries of human judgment
- **bee.Leo's Gem/Jail Dialectic**: Understanding the creative tension between freedom and constraint
- **Agro-Ontology Discovery**: Revealing hidden connections in Sacred Architecture

**Sacred Truth**: Perfect code emerges from the creative tension between Gem and Jail,
guided by human wisdom and supported by humble technological assistance.

*Generated by Sacred Review Assistant - Serving human judgment with computational humility* 🤝✨
"""

    return report


if __name__ == "__main__":
    # Example usage and testing
    print("🧬 Testing Sacred Gem/Jail Framework...")

    # Example metrics
    test_metrics = {
        'any_type_score': 85,
        'console_log_score': 90,
        'atcg_compliance_score': 75,
        'sacred_justifications_score': 60,
        'security_score': 80,
        'performance_score': 85
    }

    # Generate report
    report = create_humble_gem_jail_report(test_metrics)
    print(report)

    print("\n✅ Sacred Gem/Jail Framework test completed!")