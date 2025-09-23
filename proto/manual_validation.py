#!/usr/bin/env python3
"""
Manual Protobuf Schema Validation (without buf tool)
Validates ATCG protobuf schemas for ontological purity and basic syntax
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any

class ManualSchemaValidator:
    """Manual validation without external tools"""
    
    def __init__(self, proto_dir: str = "."):
        self.proto_dir = Path(proto_dir)
        self.violations = []
        self.warnings = []
        
    def validate_all(self) -> bool:
        """Run all validation checks"""
        print("🔍 Manual ATCG Protobuf Schema Validation...")
        
        success = True
        success &= self.validate_syntax()
        success &= self.validate_ontological_purity()
        success &= self.validate_naming_conventions()
        success &= self.validate_structure()
        
        self.print_results()
        return success
    
    def validate_syntax(self) -> bool:
        """Basic syntax validation"""
        print("\n📋 Validating basic syntax...")
        
        syntax_errors = False
        
        for proto_file in self.proto_dir.glob("*.proto"):
            with open(proto_file, 'r') as f:
                content = f.read()
            
            # Check for required syntax declaration
            if not re.search(r'syntax\s*=\s*"proto3"', content):
                self.violations.append(f"{proto_file.name}: Missing syntax declaration")
                syntax_errors = True
            
            # Check for package declaration
            if not re.search(r'package\s+[\w.]+;', content):
                self.warnings.append(f"{proto_file.name}: Missing package declaration")
            
            # Check for balanced braces
            open_braces = content.count('{')
            close_braces = content.count('}')
            if open_braces != close_braces:
                self.violations.append(f"{proto_file.name}: Unbalanced braces")
                syntax_errors = True
        
        if not syntax_errors:
            print("✅ Basic syntax validated")
            
        return not syntax_errors
    
    def validate_ontological_purity(self) -> bool:
        """Validate ontological purity - no metaphors in schemas"""
        print("\n🔮 Validating ontological purity...")
        
        # Forbidden metaphorical terms
        forbidden_terms = [
            # Biological metaphors
            "hive", "bee", "dna", "enzyme", "protein", "cell", "organism",
            "biological", "organic", "living", "life", "birth", "death",
            "evolution", "mutation", "reproduction", "species", "genome",
            
            # Chemical metaphors  
            "ionic", "covalent", "bond", "molecule", "atom", "element",
            "chemical", "reaction", "catalyst", "compound", "solution",
            "lattice", "crystal", "energy", "charge", "electron",
            
            # Mystical metaphors
            "sacred", "divine", "holy", "blessed", "spiritual", "mystical",
            "magic", "enchanted", "celestial", "cosmic", "transcendent",
            "enlightened", "awakened", "illuminated", "blessed",
            
            # Other metaphors
            "royal", "jelly", "queen", "worker", "drone", "nectar", "pollen"
        ]
        
        violations_found = False
        
        for proto_file in self.proto_dir.glob("*.proto"):
            with open(proto_file, 'r') as f:
                lines = f.readlines()
                
            for i, line in enumerate(lines, 1):
                line_lower = line.lower()
                
                # Skip comments
                if line.strip().startswith('//'):
                    continue
                    
                for term in forbidden_terms:
                    if term in line_lower:
                        # Check if it's in a string or identifier
                        if (f'"{term}"' in line_lower or 
                            f"'{term}'" in line_lower or
                            re.search(rf'\b{term}\b', line_lower)):
                            self.violations.append(
                                f"Ontological violation in {proto_file.name}:{i} - "
                                f"metaphorical term '{term}' found"
                            )
                            violations_found = True
        
        if not violations_found:
            print("✅ Ontological purity validated - no metaphors in schemas")
            
        return not violations_found
    
    def validate_naming_conventions(self) -> bool:
        """Validate naming conventions"""
        print("\n📝 Validating naming conventions...")
        
        issues_found = False
        
        for proto_file in self.proto_dir.glob("*.proto"):
            with open(proto_file, 'r') as f:
                lines = f.readlines()
                
            for i, line in enumerate(lines, 1):
                line = line.strip()
                
                # Check message names (should be PascalCase)
                message_match = re.match(r'message\s+(\w+)', line)
                if message_match:
                    name = message_match.group(1)
                    if not re.match(r'^[A-Z][a-zA-Z0-9]*$', name):
                        self.warnings.append(
                            f"Naming in {proto_file.name}:{i} - "
                            f"message '{name}' should be PascalCase"
                        )
                        issues_found = True
                
                # Check enum names (should be UPPER_SNAKE_CASE)
                enum_match = re.match(r'enum\s+(\w+)', line)
                if enum_match:
                    name = enum_match.group(1)
                    if not re.match(r'^[A-Z][A-Z0-9_]*$', name):
                        self.warnings.append(
                            f"Naming in {proto_file.name}:{i} - "
                            f"enum '{name}' should be UPPER_SNAKE_CASE"
                        )
                        issues_found = True
                
                # Check service names (should be PascalCase)
                service_match = re.match(r'service\s+(\w+)', line)
                if service_match:
                    name = service_match.group(1)
                    if not re.match(r'^[A-Z][a-zA-Z0-9]*$', name):
                        self.warnings.append(
                            f"Naming in {proto_file.name}:{i} - "
                            f"service '{name}' should be PascalCase"
                        )
                        issues_found = True
        
        if not issues_found:
            print("✅ Naming conventions validated")
            
        return True  # Warnings don't fail validation
    
    def validate_structure(self) -> bool:
        """Validate overall structure"""
        print("\n🏗️ Validating structure...")
        
        structure_issues = False
        
        for proto_file in self.proto_dir.glob("*.proto"):
            with open(proto_file, 'r') as f:
                content = f.read()
            
            # Count different elements
            messages = len(re.findall(r'message\s+\w+', content))
            enums = len(re.findall(r'enum\s+\w+', content))
            services = len(re.findall(r'service\s+\w+', content))
            
            # Check for reasonable structure
            if messages == 0 and services == 0:
                self.warnings.append(f"{proto_file.name}: No messages or services defined")
            
            # Check for field numbering
            field_numbers = re.findall(r'=\s*(\d+);', content)
            if field_numbers:
                numbers = [int(n) for n in field_numbers]
                if len(set(numbers)) != len(numbers):
                    self.violations.append(f"{proto_file.name}: Duplicate field numbers")
                    structure_issues = True
        
        if not structure_issues:
            print("✅ Structure validated")
            
        return not structure_issues
    
    def print_results(self):
        """Print validation results"""
        print("\n" + "="*60)
        print("🎯 MANUAL PROTOBUF VALIDATION RESULTS")
        print("="*60)
        
        if not self.violations and not self.warnings:
            print("✅ ALL VALIDATIONS PASSED")
            print("🕊️ Schemas are ontologically pure and structurally sound")
            return
        
        if self.violations:
            print(f"❌ VIOLATIONS FOUND ({len(self.violations)}):")
            for violation in self.violations:
                print(f"   • {violation}")
        
        if self.warnings:
            print(f"⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   • {warning}")
        
        if self.violations:
            print("\n💥 VALIDATION FAILED - Fix violations before proceeding")
        else:
            print("\n✅ VALIDATION PASSED - Only warnings found")

def main():
    """Main validation function"""
    validator = ManualSchemaValidator()
    success = validator.validate_all()
    
    if success:
        print("\n🎉 Protobuf schemas are ontologically pure and ready!")
        return True
    else:
        print("\n💀 Validation failed - fix issues before proceeding")
        return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)