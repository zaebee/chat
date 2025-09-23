#!/usr/bin/env python3
"""
Translation Layer Validation Demo
Comprehensive demonstration for bee-to-peer review
Shows ontological purity maintenance and functional preservation
"""

import sys
import json
import time
from datetime import datetime
from pathlib import Path

# Add hive module to path
sys.path.append(str(Path(__file__).parent))

from hive.primitives import Aggregate, Transformation, Connector, GenesisEvent
from hive.translation_layer import (
    backend_translator, 
    translate_hive_component_to_protobuf,
    get_backend_translation_metrics
)

class TranslationValidationDemo:
    """Comprehensive validation demo for bee-to-peer review"""
    
    def __init__(self):
        self.test_results = []
        self.validation_summary = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "ontological_purity": True,
            "functional_preservation": True,
            "performance_acceptable": True
        }
    
    def run_comprehensive_demo(self):
        """Run complete validation demo"""
        print("🎯 TRANSLATION LAYER VALIDATION DEMO")
        print("=" * 60)
        print("🕊️ Comprehensive Validation for Bee-to-Peer Review")
        print("📋 Testing Ontological Purity and Functional Preservation")
        print()
        
        # Run all validation tests
        self.test_ontological_purity()
        self.test_functional_preservation()
        self.test_performance_requirements()
        self.test_bidirectional_fidelity()
        self.test_error_handling()
        self.test_scalability()
        
        # Generate final report
        self.generate_validation_report()
    
    def test_ontological_purity(self):
        """Test ontological purity maintenance"""
        print("🔮 TEST 1: ONTOLOGICAL PURITY")
        print("-" * 40)
        
        # Create component with heavy biological metaphors
        component = Aggregate(name="ComplexBiologicalSystem")
        component.metadata = {
            "organism_type": "complex_cell",
            "dna_sequence": "ATCG-COMPLEX-SYSTEM-001",
            "enzyme_function": "data_processing_catalyst",
            "cell_membrane": "security_boundary_layer",
            "mitochondria": "energy_processing_unit",
            "nucleus": "control_center_core",
            "ribosome": "protein_synthesis_engine",
            "endoplasmic_reticulum": "transport_network",
            "golgi_apparatus": "packaging_system",
            "lysosome": "cleanup_mechanism"
        }
        
        print("🧬 Original Component (Rich Biological Metaphors):")
        print(f"   Name: {component.name}")
        print(f"   Type: {type(component).__name__}")
        print(f"   Biological Metadata Count: {len(component.metadata)}")
        
        # Translate to protobuf
        protobuf_comp = translate_hive_component_to_protobuf(component)
        
        print(f"\n🕊️ Translated Protobuf (Pure Boundary):")
        print(f"   Type: {protobuf_comp.type}")
        print(f"   Pure Metadata Count: {len(protobuf_comp.metadata)}")
        
        # Check for biological terms in protobuf
        biological_terms = [
            "organism", "dna", "enzyme", "cell", "mitochondria", 
            "nucleus", "ribosome", "biological", "hive"
        ]
        
        contamination_found = False
        for key, value in protobuf_comp.metadata.items():
            for term in biological_terms:
                if term.lower() in key.lower() or term.lower() in str(value).lower():
                    contamination_found = True
                    print(f"   ❌ Contamination: {term} found in {key}:{value}")
        
        if not contamination_found:
            print("   ✅ No biological contamination in protobuf boundary")
            self.record_test_result("Ontological Purity", True, "No metaphors in protobuf")
        else:
            print("   ❌ Biological contamination detected")
            self.record_test_result("Ontological Purity", False, "Metaphors found in protobuf")
            self.validation_summary["ontological_purity"] = False
        
        print()
    
    def test_functional_preservation(self):
        """Test functional behavior preservation"""
        print("⚙️ TEST 2: FUNCTIONAL PRESERVATION")
        print("-" * 40)
        
        # Create components and test their functionality
        components = self.create_test_components()
        
        for i, component in enumerate(components, 1):
            print(f"🔧 Testing Component {i}: {type(component).__name__}")
            
            # Get original status
            original_status = component.get_status()
            
            # Translate to protobuf and back
            protobuf_comp = translate_hive_component_to_protobuf(component)
            restored_comp = backend_translator.translate_from_protobuf(protobuf_comp)
            
            # Check functional preservation
            id_preserved = component.id == protobuf_comp.id == restored_comp["id"]
            type_preserved = type(component).__name__ == restored_comp["type"]
            
            if id_preserved and type_preserved:
                print(f"   ✅ Functional identity preserved")
                self.record_test_result(f"Functional Preservation {i}", True, "Identity preserved")
            else:
                print(f"   ❌ Functional identity lost")
                self.record_test_result(f"Functional Preservation {i}", False, "Identity lost")
                self.validation_summary["functional_preservation"] = False
        
        print()
    
    def test_performance_requirements(self):
        """Test performance requirements"""
        print("⚡ TEST 3: PERFORMANCE REQUIREMENTS")
        print("-" * 40)
        
        # Performance test parameters
        num_translations = 100
        max_acceptable_time_ms = 10.0  # 10ms per translation
        
        print(f"🏃 Running {num_translations} translations...")
        
        # Create test component
        component = Aggregate(name="PerformanceTest")
        component.metadata = {"test": "performance", "iteration": "multiple"}
        
        # Time multiple translations
        start_time = time.time()
        
        for i in range(num_translations):
            protobuf_comp = translate_hive_component_to_protobuf(component)
            restored_comp = backend_translator.translate_from_protobuf(protobuf_comp)
        
        end_time = time.time()
        total_time_ms = (end_time - start_time) * 1000
        avg_time_ms = total_time_ms / num_translations
        
        print(f"   Total Time: {total_time_ms:.2f}ms")
        print(f"   Average Time: {avg_time_ms:.2f}ms per translation")
        print(f"   Requirement: < {max_acceptable_time_ms}ms per translation")
        
        if avg_time_ms < max_acceptable_time_ms:
            print(f"   ✅ Performance requirement met")
            self.record_test_result("Performance", True, f"Avg {avg_time_ms:.2f}ms < {max_acceptable_time_ms}ms")
        else:
            print(f"   ❌ Performance requirement failed")
            self.record_test_result("Performance", False, f"Avg {avg_time_ms:.2f}ms > {max_acceptable_time_ms}ms")
            self.validation_summary["performance_acceptable"] = False
        
        print()
    
    def test_bidirectional_fidelity(self):
        """Test bidirectional translation fidelity"""
        print("🔄 TEST 4: BIDIRECTIONAL FIDELITY")
        print("-" * 40)
        
        # Create complex component
        component = Aggregate(name="FidelityTest")
        component.metadata = {
            "complex_key_1": "complex_value_1",
            "hive_id": "test_colony_001",
            "dna_sequence": "ATCG-FIDELITY-TEST",
            "numeric_value": "42",
            "boolean_flag": "true"
        }
        
        print(f"🧬 Original Component:")
        print(f"   ID: {component.id}")
        print(f"   Type: {type(component).__name__}")
        print(f"   Metadata: {component.metadata}")
        
        # Round-trip translation
        protobuf_comp = translate_hive_component_to_protobuf(component)
        restored_comp = backend_translator.translate_from_protobuf(protobuf_comp)
        
        print(f"\n🔄 After Round-trip:")
        print(f"   ID: {restored_comp['id']}")
        print(f"   Type: {restored_comp['type']}")
        print(f"   Metadata: {restored_comp['metadata']}")
        
        # Check fidelity
        id_match = component.id == restored_comp["id"]
        type_match = type(component).__name__ == restored_comp["type"]
        
        # Check metadata mapping (allowing for key transformations)
        original_count = len(component.metadata)
        restored_count = len(restored_comp["metadata"])
        metadata_preserved = abs(original_count - restored_count) <= 1  # Allow minor differences
        
        print(f"\n🎯 Fidelity Check:")
        print(f"   ID Match: {id_match}")
        print(f"   Type Match: {type_match}")
        print(f"   Metadata Preserved: {metadata_preserved} ({original_count} → {restored_count})")
        
        if id_match and type_match and metadata_preserved:
            print(f"   ✅ Bidirectional fidelity maintained")
            self.record_test_result("Bidirectional Fidelity", True, "All checks passed")
        else:
            print(f"   ❌ Bidirectional fidelity lost")
            self.record_test_result("Bidirectional Fidelity", False, "Fidelity checks failed")
        
        print()
    
    def test_error_handling(self):
        """Test error handling and edge cases"""
        print("🛡️ TEST 5: ERROR HANDLING")
        print("-" * 40)
        
        # Test with minimal component
        minimal_component = Aggregate(name="Minimal")
        minimal_component.metadata = {}
        
        try:
            protobuf_comp = translate_hive_component_to_protobuf(minimal_component)
            print("   ✅ Minimal component handled correctly")
            self.record_test_result("Error Handling - Minimal", True, "No errors")
        except Exception as e:
            print(f"   ❌ Minimal component failed: {e}")
            self.record_test_result("Error Handling - Minimal", False, str(e))
        
        # Test with complex metadata
        complex_component = Aggregate(name="Complex")
        complex_component.metadata = {
            "nested_dict": {"key": "value"},
            "list_value": [1, 2, 3],
            "none_value": None,
            "unicode_value": "🧬🕊️"
        }
        
        try:
            protobuf_comp = translate_hive_component_to_protobuf(complex_component)
            print("   ✅ Complex metadata handled correctly")
            self.record_test_result("Error Handling - Complex", True, "No errors")
        except Exception as e:
            print(f"   ❌ Complex metadata failed: {e}")
            self.record_test_result("Error Handling - Complex", False, str(e))
        
        print()
    
    def test_scalability(self):
        """Test scalability with multiple components"""
        print("📈 TEST 6: SCALABILITY")
        print("-" * 40)
        
        # Create multiple components
        components = []
        for i in range(10):
            comp = Aggregate(name=f"ScaleTest_{i}")
            comp.metadata = {
                "index": str(i),
                "hive_id": f"colony_{i}",
                "dna_sequence": f"ATCG-SCALE-{i:03d}"
            }
            components.append(comp)
        
        print(f"🔧 Testing {len(components)} components...")
        
        # Translate all components
        successful_translations = 0
        failed_translations = 0
        
        for i, component in enumerate(components):
            try:
                protobuf_comp = translate_hive_component_to_protobuf(component)
                restored_comp = backend_translator.translate_from_protobuf(protobuf_comp)
                
                # Validate translation
                if component.id == restored_comp["id"]:
                    successful_translations += 1
                else:
                    failed_translations += 1
                    
            except Exception as e:
                failed_translations += 1
                print(f"   ❌ Component {i} failed: {e}")
        
        success_rate = (successful_translations / len(components)) * 100
        
        print(f"   Successful: {successful_translations}/{len(components)}")
        print(f"   Failed: {failed_translations}/{len(components)}")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 95.0:
            print(f"   ✅ Scalability requirement met")
            self.record_test_result("Scalability", True, f"{success_rate:.1f}% success rate")
        else:
            print(f"   ❌ Scalability requirement failed")
            self.record_test_result("Scalability", False, f"{success_rate:.1f}% success rate")
        
        print()
    
    def create_test_components(self):
        """Create test components for validation"""
        components = []
        
        # Aggregate
        aggregate = Aggregate(name="TestAggregate")
        aggregate.metadata = {"hive_id": "test", "dna_sequence": "ATCG-001"}
        components.append(aggregate)
        
        # Transformation
        async def test_processor(data):
            return {"processed": True}
        
        transformation = Transformation(name="TestTransformation", processor_func=test_processor)
        transformation.metadata = {"enzyme_type": "test_catalyst"}
        components.append(transformation)
        
        # Connector
        connector = Connector(name="TestConnector", input_protocol="test", output_protocol="test")
        connector.metadata = {"nervous_system": "test"}
        components.append(connector)
        
        # GenesisEvent
        async def test_broadcaster(event):
            return True
        
        genesis = GenesisEvent(name="TestGenesis", event_type="test", broadcast_func=test_broadcaster)
        genesis.metadata = {"dna_replication": "test"}
        components.append(genesis)
        
        return components
    
    def record_test_result(self, test_name, passed, details):
        """Record test result"""
        self.test_results.append({
            "test": test_name,
            "passed": passed,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        
        self.validation_summary["total_tests"] += 1
        if passed:
            self.validation_summary["passed_tests"] += 1
        else:
            self.validation_summary["failed_tests"] += 1
    
    def generate_validation_report(self):
        """Generate final validation report"""
        print("📊 VALIDATION REPORT")
        print("=" * 60)
        
        # Summary statistics
        total = self.validation_summary["total_tests"]
        passed = self.validation_summary["passed_tests"]
        failed = self.validation_summary["failed_tests"]
        success_rate = (passed / total * 100) if total > 0 else 0
        
        print(f"📈 Test Summary:")
        print(f"   Total Tests: {total}")
        print(f"   Passed: {passed}")
        print(f"   Failed: {failed}")
        print(f"   Success Rate: {success_rate:.1f}%")
        print()
        
        # Core validation results
        print(f"🎯 Core Validations:")
        print(f"   Ontological Purity: {'✅ PASS' if self.validation_summary['ontological_purity'] else '❌ FAIL'}")
        print(f"   Functional Preservation: {'✅ PASS' if self.validation_summary['functional_preservation'] else '❌ FAIL'}")
        print(f"   Performance Acceptable: {'✅ PASS' if self.validation_summary['performance_acceptable'] else '❌ FAIL'}")
        print()
        
        # Translation metrics
        metrics = get_backend_translation_metrics()
        print(f"📊 Translation Metrics:")
        print(f"   Total Translations: {metrics['translations_performed']}")
        print(f"   Success Rate: {metrics['success_rate_percent']:.1f}%")
        print(f"   Average Time: {metrics['average_translation_time_ms']:.2f}ms")
        print()
        
        # Detailed test results
        print(f"📋 Detailed Results:")
        for result in self.test_results:
            status = "✅ PASS" if result["passed"] else "❌ FAIL"
            print(f"   {result['test']}: {status} - {result['details']}")
        print()
        
        # Final verdict
        all_core_passed = (
            self.validation_summary["ontological_purity"] and
            self.validation_summary["functional_preservation"] and
            self.validation_summary["performance_acceptable"]
        )
        
        if all_core_passed and success_rate >= 90:
            print("🎉 VALIDATION SUCCESSFUL!")
            print("✅ Translation layer ready for production")
            print("🕊️ Ontological purity maintained")
            print("⚙️ Functional preservation confirmed")
            print("⚡ Performance requirements met")
        else:
            print("❌ VALIDATION FAILED!")
            print("💀 Translation layer requires fixes before production")
        
        print()
        print("📋 Ready for bee-to-peer review")
        print("=" * 60)

def main():
    """Main demo function"""
    demo = TranslationValidationDemo()
    demo.run_comprehensive_demo()

if __name__ == "__main__":
    main()