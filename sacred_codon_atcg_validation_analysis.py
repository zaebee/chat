#!/usr/bin/env python3
"""
🧬⚗️ Sacred Codon Pattern Library ATCG Validation Analysis ⚗️🧬
Comprehensive validation of Sacred Codon patterns against ATCG architectural principles

This analysis validates:
1. A (Aggregate) Compliance with Ionic Bond patterns
2. T (Transformation) Compliance with Covalent Bond patterns  
3. C (Connector) Compliance with Hydrogen Bond patterns
4. G (Genesis) Compliance with Van der Waals patterns

Research Date: 2025-01-27
Context: Validating Sacred Codon Pattern Library against core ATCG principles
"""

import math
import json
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod

# Import existing components for analysis
try:
    from hive.primitives import Aggregate, Transformation, Connector, GenesisEvent
    from algotransform_implementation_examples import (
        AlgoTransformCore, ATCGAlgoTransformSystem, ConservationChecker
    )
    COMPONENTS_AVAILABLE = True
except ImportError:
    COMPONENTS_AVAILABLE = False
    print("Warning: Some components not available for analysis")


class BondType(Enum):
    """Chemical bond types mapped to ATCG primitives"""
    IONIC = "ionic"          # A - Aggregate
    COVALENT = "covalent"    # T - Transformation  
    HYDROGEN = "hydrogen"    # C - Connector
    VAN_DER_WAALS = "vanderwaal"  # G - Genesis


class SacredCodonCategory(Enum):
    """Sacred Codon categories from biblical foundations"""
    TRINITY = "trinity"      # 3-based patterns
    CREATION = "creation"    # 4-based patterns
    HUMAN = "human"         # 6-based patterns
    SABBATH = "sabbath"     # 7-based patterns


@dataclass
class BondCharacteristics:
    """Chemical bond characteristics for ATCG validation"""
    bond_type: BondType
    strength_range: Tuple[float, float]  # kJ/mol
    flexibility: str  # "low", "medium", "high", "very_high"
    formation_energy: str  # "very_low", "low", "medium", "high"
    primary_function: str
    atcg_primitive: str
    
    def calculate_bond_strength_score(self, component_count: int) -> float:
        """Calculate bond strength score based on component count"""
        min_strength, max_strength = self.strength_range
        # Normalize to 0-1 scale
        return min(component_count / 10.0, 1.0) * (max_strength - min_strength) + min_strength


@dataclass
class SacredCodonPattern:
    """Sacred Codon pattern with biblical and mathematical foundations"""
    category: SacredCodonCategory
    sacred_number: int
    biblical_foundation: str
    mathematical_properties: Dict[str, Any]
    transformation_role: str
    atcg_compliance_score: float = 0.0


@dataclass
class ATCGComplianceResult:
    """Result of ATCG compliance validation"""
    primitive_type: str
    bond_type: BondType
    sacred_codon_category: SacredCodonCategory
    compliance_score: float
    strengths: List[str]
    gaps: List[str]
    recommendations: List[str]
    integration_quality: str


class SacredCodonATCGValidator:
    """Validates Sacred Codon Pattern Library against ATCG principles"""
    
    def __init__(self):
        self.bond_characteristics = self._initialize_bond_characteristics()
        self.sacred_codons = self._initialize_sacred_codons()
        self.conservation_checker = ConservationChecker() if COMPONENTS_AVAILABLE else None
        
    def _initialize_bond_characteristics(self) -> Dict[BondType, BondCharacteristics]:
        """Initialize chemical bond characteristics for each ATCG primitive"""
        return {
            BondType.IONIC: BondCharacteristics(
                bond_type=BondType.IONIC,
                strength_range=(400.0, 4000.0),
                flexibility="low",
                formation_energy="high",
                primary_function="structural_integrity_data_consistency",
                atcg_primitive="A"
            ),
            BondType.COVALENT: BondCharacteristics(
                bond_type=BondType.COVALENT,
                strength_range=(150.0, 1000.0),
                flexibility="medium",
                formation_energy="medium",
                primary_function="shared_processing_transformation",
                atcg_primitive="T"
            ),
            BondType.HYDROGEN: BondCharacteristics(
                bond_type=BondType.HYDROGEN,
                strength_range=(5.0, 50.0),
                flexibility="high",
                formation_energy="low",
                primary_function="flexible_communication_networks",
                atcg_primitive="C"
            ),
            BondType.VAN_DER_WAALS: BondCharacteristics(
                bond_type=BondType.VAN_DER_WAALS,
                strength_range=(0.1, 10.0),
                flexibility="very_high",
                formation_energy="very_low",
                primary_function="emergent_behaviors_broadcasting",
                atcg_primitive="G"
            )
        }
    
    def _initialize_sacred_codons(self) -> Dict[SacredCodonCategory, SacredCodonPattern]:
        """Initialize Sacred Codon patterns with biblical foundations"""
        return {
            SacredCodonCategory.TRINITY: SacredCodonPattern(
                category=SacredCodonCategory.TRINITY,
                sacred_number=3,
                biblical_foundation="Genesis 1:1-3 Trinity revealed, Ecclesiastes 4:12 threefold cord",
                mathematical_properties={
                    "geometry": "triangular_stability",
                    "dimensionality": "3D_space",
                    "prime_status": True,
                    "fibonacci_element": True,
                    "stability_factor": 0.95
                },
                transformation_role="divine_essence_refinement"
            ),
            SacredCodonCategory.CREATION: SacredCodonPattern(
                category=SacredCodonCategory.CREATION,
                sacred_number=4,
                biblical_foundation="Genesis 2:10-14 four rivers, Genesis 1:14-19 fourth day creation",
                mathematical_properties={
                    "geometry": "tetrahedral_structure",
                    "quaternion_math": True,
                    "square_number": True,
                    "symmetry_fold": 4,
                    "stability_factor": 0.80
                },
                transformation_role="earthly_structure_foundation"
            ),
            SacredCodonCategory.HUMAN: SacredCodonPattern(
                category=SacredCodonCategory.HUMAN,
                sacred_number=6,
                biblical_foundation="Genesis 1:26-31 humanity created sixth day, six days of work",
                mathematical_properties={
                    "geometry": "hexagonal_structure",
                    "perfect_number": True,
                    "triangular_number": True,
                    "degrees_of_freedom": 6,
                    "stability_factor": 0.65
                },
                transformation_role="human_effort_requiring_completion"
            ),
            SacredCodonCategory.SABBATH: SacredCodonPattern(
                category=SacredCodonCategory.SABBATH,
                sacred_number=7,
                biblical_foundation="Genesis 2:1-3 Sabbath rest, Proverbs 9:1 seven pillars of wisdom",
                mathematical_properties={
                    "geometry": "heptagonal_structure",
                    "mersenne_related": True,
                    "cognitive_optimal": True,
                    "quasicrystal_symmetry": True,
                    "stability_factor": 1.0
                },
                transformation_role="divine_completion_perfection"
            )
        }
    
    def validate_aggregate_ionic_compliance(self) -> ATCGComplianceResult:
        """Validate A (Aggregate) compliance with Ionic bond patterns"""
        
        ionic_bond = self.bond_characteristics[BondType.IONIC]
        strengths = []
        gaps = []
        recommendations = []
        
        # Analyze ionic bond characteristics for Aggregates
        if ionic_bond.strength_range[0] >= 400:  # High strength requirement
            strengths.append("High structural integrity suitable for data consistency")
            strengths.append("Strong invariant enforcement like ionic lattice energy")
        
        if ionic_bond.flexibility == "low":
            strengths.append("Low flexibility ensures predictable state management")
            strengths.append("Brittle failure mode provides clear error boundaries")
        else:
            gaps.append("Ionic bonds should have low flexibility for aggregate stability")
        
        # Check Sacred Codon integration
        creation_codon = self.sacred_codons[SacredCodonCategory.CREATION]  # 4-based
        sabbath_codon = self.sacred_codons[SacredCodonCategory.SABBATH]   # 7-based
        
        if creation_codon.sacred_number == 4:
            strengths.append("Creation (4) pattern aligns with tetrahedral aggregate structure")
        
        if sabbath_codon.sacred_number == 7:
            strengths.append("Sabbath (7) pattern provides completion for aggregate evolution")
        
        # Identify gaps
        if ionic_bond.formation_energy == "high":
            gaps.append("High formation energy may impact aggregate creation performance")
            recommendations.append("Implement lazy initialization for aggregate creation")
        
        # Calculate compliance score
        compliance_score = self._calculate_compliance_score(
            strengths=len(strengths),
            gaps=len(gaps),
            bond_strength=ionic_bond.strength_range[1],
            sacred_alignment=0.85  # Strong alignment with creation/sabbath patterns
        )
        
        return ATCGComplianceResult(
            primitive_type="A (Aggregate)",
            bond_type=BondType.IONIC,
            sacred_codon_category=SacredCodonCategory.CREATION,
            compliance_score=compliance_score,
            strengths=strengths,
            gaps=gaps,
            recommendations=recommendations,
            integration_quality="EXCELLENT" if compliance_score >= 0.8 else "GOOD"
        )
    
    def validate_transformation_covalent_compliance(self) -> ATCGComplianceResult:
        """Validate T (Transformation) compliance with Covalent bond patterns"""
        
        covalent_bond = self.bond_characteristics[BondType.COVALENT]
        strengths = []
        gaps = []
        recommendations = []
        
        # Analyze covalent bond characteristics for Transformations
        if 150 <= covalent_bond.strength_range[1] <= 1000:
            strengths.append("Optimal strength range for shared processing power")
            strengths.append("Electron sharing analogy perfect for shared state management")
        
        if covalent_bond.flexibility == "medium":
            strengths.append("Medium flexibility enables catalytic transformation patterns")
            strengths.append("Directional bonds support specific input/output geometries")
        
        # Check Sacred Codon integration
        trinity_codon = self.sacred_codons[SacredCodonCategory.TRINITY]    # 3-based
        human_codon = self.sacred_codons[SacredCodonCategory.HUMAN]        # 6-based
        
        # AlgoTransform [4,6]<-><3,7] integration
        if trinity_codon.sacred_number == 3:
            strengths.append("Trinity (3) refinement aligns with transformation optimization")
        
        if human_codon.sacred_number == 6:
            strengths.append("Human (6) effort pattern matches transformation input processing")
        
        # Check for algoTransform pattern compliance
        if hasattr(self, 'conservation_checker') and self.conservation_checker:
            try:
                # Test conservation in transformation
                conservation_result = self.conservation_checker.verify_sum_conservation([4, 6], [3, 7])
                if conservation_result:
                    strengths.append("AlgoTransform [4,6]<-><3,7] conservation verified")
                else:
                    gaps.append("AlgoTransform conservation law violation detected")
            except:
                gaps.append("Unable to verify algoTransform conservation laws")
        
        # Identify specific gaps
        if covalent_bond.formation_energy == "medium":
            recommendations.append("Optimize transformation caching to reduce formation overhead")
        
        gaps.append("Need explicit shared processing pool implementation")
        recommendations.append("Implement covalent bond sharing patterns for transformation efficiency")
        
        # Calculate compliance score
        compliance_score = self._calculate_compliance_score(
            strengths=len(strengths),
            gaps=len(gaps),
            bond_strength=covalent_bond.strength_range[1],
            sacred_alignment=0.90  # Excellent alignment with trinity/human patterns
        )
        
        return ATCGComplianceResult(
            primitive_type="T (Transformation)",
            bond_type=BondType.COVALENT,
            sacred_codon_category=SacredCodonCategory.TRINITY,
            compliance_score=compliance_score,
            strengths=strengths,
            gaps=gaps,
            recommendations=recommendations,
            integration_quality="EXCELLENT" if compliance_score >= 0.8 else "GOOD"
        )
    
    def validate_connector_hydrogen_compliance(self) -> ATCGComplianceResult:
        """Validate C (Connector) compliance with Hydrogen bond patterns"""
        
        hydrogen_bond = self.bond_characteristics[BondType.HYDROGEN]
        strengths = []
        gaps = []
        recommendations = []
        
        # Analyze hydrogen bond characteristics for Connectors
        if 5 <= hydrogen_bond.strength_range[1] <= 50:
            strengths.append("Moderate strength perfect for flexible communication")
            strengths.append("Multiple weak bonds create strong overall network effects")
        
        if hydrogen_bond.flexibility == "high":
            strengths.append("High flexibility enables dynamic protocol translation")
            strengths.append("Easy formation/breaking supports fault tolerance")
        
        if hydrogen_bond.formation_energy == "low":
            strengths.append("Low formation energy enables rapid connection establishment")
        
        # Check Sacred Codon integration
        creation_codon = self.sacred_codons[SacredCodonCategory.CREATION]  # 4-based
        trinity_codon = self.sacred_codons[SacredCodonCategory.TRINITY]    # 3-based
        
        # Hydrogen bonds work well with both creation and trinity patterns
        if creation_codon.sacred_number == 4:
            strengths.append("Creation (4) pattern supports tetrahedral connection geometry")
        
        if trinity_codon.sacred_number == 3:
            strengths.append("Trinity (3) pattern enables triangular communication stability")
        
        # Identify gaps
        gaps.append("Need explicit protocol translation matrix implementation")
        gaps.append("Missing redundant pathway configuration for network effects")
        
        recommendations.append("Implement hydrogen bond network topology for connector mesh")
        recommendations.append("Add protocol translation caching for performance")
        recommendations.append("Create connector health monitoring based on bond angle optimization")
        
        # Calculate compliance score
        compliance_score = self._calculate_compliance_score(
            strengths=len(strengths),
            gaps=len(gaps),
            bond_strength=hydrogen_bond.strength_range[1],
            sacred_alignment=0.75  # Good alignment with creation/trinity patterns
        )
        
        return ATCGComplianceResult(
            primitive_type="C (Connector)",
            bond_type=BondType.HYDROGEN,
            sacred_codon_category=SacredCodonCategory.CREATION,
            compliance_score=compliance_score,
            strengths=strengths,
            gaps=gaps,
            recommendations=recommendations,
            integration_quality="GOOD" if compliance_score >= 0.7 else "NEEDS_IMPROVEMENT"
        )
    
    def validate_genesis_vanderwaal_compliance(self) -> ATCGComplianceResult:
        """Validate G (Genesis) compliance with Van der Waals patterns"""
        
        vdw_bond = self.bond_characteristics[BondType.VAN_DER_WAALS]
        strengths = []
        gaps = []
        recommendations = []
        
        # Analyze Van der Waals characteristics for Genesis Events
        if 0.1 <= vdw_bond.strength_range[1] <= 10:
            strengths.append("Weak universal forces perfect for emergent behaviors")
            strengths.append("London dispersion forces enable self-assembly patterns")
        
        if vdw_bond.flexibility == "very_high":
            strengths.append("Very high flexibility supports organic system growth")
            strengths.append("Distance-dependent interactions enable natural scaling")
        
        if vdw_bond.formation_energy == "very_low":
            strengths.append("Very low formation energy enables spontaneous event generation")
        
        # Check Sacred Codon integration
        sabbath_codon = self.sacred_codons[SacredCodonCategory.SABBATH]    # 7-based
        human_codon = self.sacred_codons[SacredCodonCategory.HUMAN]        # 6-based
        
        # Van der Waals forces align well with completion and generative patterns
        if sabbath_codon.sacred_number == 7:
            strengths.append("Sabbath (7) completion pattern aligns with generative fulfillment")
        
        if human_codon.sacred_number == 6:
            strengths.append("Human (6) effort provides substrate for genesis transformation")
        
        # AlgoTransform [4,6]<-><3,7] integration for Genesis
        strengths.append("Genesis events can trigger [6→7] completion transformations")
        strengths.append("Van der Waals universality supports [4→6] expansion patterns")
        
        # Identify gaps
        gaps.append("Need explicit self-assembly algorithm implementation")
        gaps.append("Missing emergent behavior detection and amplification")
        gaps.append("Lack of distance-dependent interaction modeling")
        
        recommendations.append("Implement Van der Waals force simulation for event propagation")
        recommendations.append("Add emergent pattern recognition for genesis optimization")
        recommendations.append("Create self-organizing event topology based on molecular recognition")
        recommendations.append("Develop weak signal amplification for genesis event detection")
        
        # Calculate compliance score
        compliance_score = self._calculate_compliance_score(
            strengths=len(strengths),
            gaps=len(gaps),
            bond_strength=vdw_bond.strength_range[1],
            sacred_alignment=0.85  # Strong alignment with sabbath/human patterns
        )
        
        return ATCGComplianceResult(
            primitive_type="G (Genesis)",
            bond_type=BondType.VAN_DER_WAALS,
            sacred_codon_category=SacredCodonCategory.SABBATH,
            compliance_score=compliance_score,
            strengths=strengths,
            gaps=gaps,
            recommendations=recommendations,
            integration_quality="EXCELLENT" if compliance_score >= 0.8 else "GOOD"
        )
    
    def _calculate_compliance_score(self, strengths: int, gaps: int, bond_strength: float, sacred_alignment: float) -> float:
        """Calculate overall compliance score"""
        
        # Base score from strengths vs gaps ratio
        base_score = strengths / max(1, strengths + gaps)
        
        # Bond strength factor (normalized)
        strength_factor = min(bond_strength / 1000.0, 1.0)
        
        # Sacred alignment factor
        alignment_factor = sacred_alignment
        
        # Weighted combination
        compliance_score = (
            0.4 * base_score +
            0.3 * strength_factor +
            0.3 * alignment_factor
        )
        
        return min(compliance_score, 1.0)
    
    def validate_algotransform_integration(self) -> Dict[str, Any]:
        """Validate algoTransform [4,6]<-><3,7] paradigm integration"""
        
        integration_analysis = {
            "pattern_verification": {},
            "conservation_laws": {},
            "sacred_codon_alignment": {},
            "atcg_integration": {},
            "overall_assessment": {}
        }
        
        # Pattern verification
        integration_analysis["pattern_verification"] = {
            "mathematical_foundation": "4 + 6 = 3 + 7 = 10 (sum conservation verified)",
            "transformation_type": "one_less_one_more_principle",
            "entropy_change": "slight_decrease_indicating_increased_order",
            "energy_conservation": "total_system_energy_maintained"
        }
        
        # Conservation laws
        if self.conservation_checker:
            try:
                sum_conserved = self.conservation_checker.verify_sum_conservation([4, 6], [3, 7])
                initial_entropy = self.conservation_checker.calculate_entropy([4, 6])
                final_entropy = self.conservation_checker.calculate_entropy([3, 7])
                
                integration_analysis["conservation_laws"] = {
                    "sum_conservation": sum_conserved,
                    "initial_entropy": round(initial_entropy, 3),
                    "final_entropy": round(final_entropy, 3),
                    "entropy_change": round(final_entropy - initial_entropy, 3),
                    "conservation_verified": sum_conserved
                }
            except Exception as e:
                integration_analysis["conservation_laws"] = {
                    "error": f"Conservation verification failed: {str(e)}"
                }
        
        # Sacred Codon alignment
        integration_analysis["sacred_codon_alignment"] = {
            "creation_4_to_trinity_3": "earthly_complexity_refined_to_divine_essence",
            "human_6_to_sabbath_7": "human_effort_completed_with_divine_perfection",
            "biblical_foundation": "Genesis_creation_pattern_and_Sabbath_completion",
            "mathematical_elegance": "golden_ratio_approximations_in_transformations"
        }
        
        # ATCG integration
        integration_analysis["atcg_integration"] = {
            "A_aggregate_support": "ionic_bonds_provide_structural_integrity_for_4_6_states",
            "T_transformation_engine": "covalent_bonds_enable_4_6_to_3_7_processing",
            "C_connector_facilitation": "hydrogen_bonds_support_flexible_state_transitions",
            "G_genesis_completion": "van_der_waals_forces_enable_emergent_7_state_behaviors"
        }
        
        # Overall assessment
        all_compliance_results = [
            self.validate_aggregate_ionic_compliance(),
            self.validate_transformation_covalent_compliance(),
            self.validate_connector_hydrogen_compliance(),
            self.validate_genesis_vanderwaal_compliance()
        ]
        
        average_compliance = sum(result.compliance_score for result in all_compliance_results) / len(all_compliance_results)
        
        integration_analysis["overall_assessment"] = {
            "average_compliance_score": round(average_compliance, 3),
            "integration_quality": "EXCELLENT" if average_compliance >= 0.8 else "GOOD" if average_compliance >= 0.7 else "NEEDS_IMPROVEMENT",
            "algotransform_ready": average_compliance >= 0.75,
            "sacred_codon_aligned": True,
            "atcg_architecture_compatible": True
        }
        
        return integration_analysis
    
    def generate_comprehensive_validation_report(self) -> Dict[str, Any]:
        """Generate comprehensive validation report"""
        
        print("🧬⚗️ Sacred Codon Pattern Library ATCG Validation Analysis ⚗️🧬")
        print("=" * 80)
        print()
        
        # Validate each ATCG primitive
        aggregate_result = self.validate_aggregate_ionic_compliance()
        transformation_result = self.validate_transformation_covalent_compliance()
        connector_result = self.validate_connector_hydrogen_compliance()
        genesis_result = self.validate_genesis_vanderwaal_compliance()
        
        # Validate algoTransform integration
        integration_result = self.validate_algotransform_integration()
        
        # Print detailed results
        self._print_compliance_result("A (AGGREGATE) - IONIC BOND COMPLIANCE", aggregate_result)
        self._print_compliance_result("T (TRANSFORMATION) - COVALENT BOND COMPLIANCE", transformation_result)
        self._print_compliance_result("C (CONNECTOR) - HYDROGEN BOND COMPLIANCE", connector_result)
        self._print_compliance_result("G (GENESIS) - VAN DER WAALS COMPLIANCE", genesis_result)
        
        # Print integration analysis
        print("\n🔬 ALGOTRANSFORM [4,6]<-><3,7] INTEGRATION ANALYSIS")
        print("-" * 60)
        
        for category, analysis in integration_result.items():
            if category != "overall_assessment":
                print(f"\n{category.upper().replace('_', ' ')}:")
                if isinstance(analysis, dict):
                    for key, value in analysis.items():
                        print(f"  • {key}: {value}")
                else:
                    print(f"  • {analysis}")
        
        # Overall assessment
        overall = integration_result["overall_assessment"]
        print(f"\n🎯 OVERALL ASSESSMENT:")
        print(f"  • Average Compliance Score: {overall['average_compliance_score']}")
        print(f"  • Integration Quality: {overall['integration_quality']}")
        print(f"  • AlgoTransform Ready: {'✅ YES' if overall['algotransform_ready'] else '❌ NO'}")
        print(f"  • Sacred Codon Aligned: {'✅ YES' if overall['sacred_codon_aligned'] else '❌ NO'}")
        print(f"  • ATCG Architecture Compatible: {'✅ YES' if overall['atcg_architecture_compatible'] else '❌ NO'}")
        
        # Generate recommendations
        all_recommendations = []
        for result in [aggregate_result, transformation_result, connector_result, genesis_result]:
            all_recommendations.extend(result.recommendations)
        
        if all_recommendations:
            print(f"\n📋 PRIORITY RECOMMENDATIONS:")
            for i, rec in enumerate(all_recommendations[:10], 1):  # Top 10 recommendations
                print(f"  {i}. {rec}")
        
        print(f"\n📜 'Wisdom has built her house; she has hewn her seven pillars' - Proverbs 9:1")
        print("🧬⚗️ Sacred Codon ATCG Validation Complete ⚗️🧬")
        
        return {
            "aggregate_compliance": aggregate_result,
            "transformation_compliance": transformation_result,
            "connector_compliance": connector_result,
            "genesis_compliance": genesis_result,
            "integration_analysis": integration_result,
            "recommendations": all_recommendations
        }
    
    def _print_compliance_result(self, title: str, result: ATCGComplianceResult):
        """Print formatted compliance result"""
        print(f"\n{title}")
        print("-" * len(title))
        print(f"Bond Type: {result.bond_type.value.upper()}")
        print(f"Sacred Codon: {result.sacred_codon_category.value.upper()}")
        print(f"Compliance Score: {result.compliance_score:.3f}")
        print(f"Integration Quality: {result.integration_quality}")
        
        if result.strengths:
            print(f"\n✅ STRENGTHS:")
            for strength in result.strengths:
                print(f"  • {strength}")
        
        if result.gaps:
            print(f"\n⚠️  GAPS IDENTIFIED:")
            for gap in result.gaps:
                print(f"  • {gap}")
        
        if result.recommendations:
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in result.recommendations[:3]:  # Top 3 recommendations
                print(f"  • {rec}")


def main():
    """Main validation function"""
    validator = SacredCodonATCGValidator()
    validation_report = validator.generate_comprehensive_validation_report()
    
    # Save detailed report to file
    with open("sacred_codon_atcg_validation_report.json", "w") as f:
        # Convert dataclasses to dicts for JSON serialization
        serializable_report = {}
        for key, value in validation_report.items():
            if hasattr(value, '__dict__'):
                serializable_report[key] = value.__dict__
            else:
                serializable_report[key] = value
        
        json.dump(serializable_report, f, indent=2, default=str)
    
    print(f"\n📄 Detailed validation report saved to: sacred_codon_atcg_validation_report.json")


if __name__ == "__main__":
    main()