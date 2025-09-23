#!/usr/bin/env python3
"""
Protobuf Schema Validation Script
Validates ATCG protobuf schemas for ontological purity and technical correctness
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple

class SchemaValidator:
    """Validates protobuf schemas for purity and correctness"""
    
    def __init__(self, proto_dir: str = "proto"):
        self.proto_dir = Path(proto_dir)
        self.violations = []
        self.warnings = []
        
    def validate_all(self) -> bool:
        """Run all validation checks"""
        print("🔍 Validating ATCG Protobuf Schemas...")
        
        success = True
        success &= self.validate_compilation()
        success &= self.validate_ontological_purity()
        success &= self.validate_naming_conventions()
        success &= self.validate_dependencies()
        
        self.print_results()
        return success
    
    def validate_compilation(self) -> bool:
        """Test protobuf compilation"""
        print("\n📋 Testing protobuf compilation...")
        
        try:
            # Check if buf is available
            result = subprocess.run(
                ["buf", "--version"], 
                capture_output=True, 
                text=True, 
                cwd=self.proto_dir
            )
            
            if result.returncode != 0:
                self.violations.append("buf tool not available - install from https://buf.build")
                return False
                
            # Lint protobuf files
            result = subprocess.run(
                ["buf", "lint"], 
                capture_output=True, 
                text=True, 
                cwd=self.proto_dir
            )
            
            if result.returncode != 0:
                self.violations.append(f"Protobuf linting failed: {result.stderr}")
                return False
            
            # Check for breaking changes (if previous version exists)
            result = subprocess.run(
                ["buf", "breaking", "--against", "."], 
                capture_output=True, 
                text=True, 
                cwd=self.proto_dir
            )
            
            if result.returncode != 0 and "no previous version" not in result.stderr:
                self.warnings.append(f"Breaking changes detected: {result.stderr}")
            
            print("✅ Protobuf compilation successful")
            return True
            
        except FileNotFoundError:
            self.violations.append("buf tool not found - install from https://buf.build")
            return False
        except Exception as e:
            self.violations.append(f"Compilation test failed: {str(e)}")
            return False
    
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
                content = f.read().lower()
                
            for term in forbidden_terms:
                if term in content:
                    # Check if it's in a comment (allowed) or actual definition (forbidden)
                    lines = content.split('\n')
                    for i, line in enumerate(lines, 1):
                        if term in line and not line.strip().startswith('//'):
                            self.violations.append(
                                f"Ontological violation in {proto_file.name}:{i} - "
                                f"metaphorical term '{term}' in schema definition"
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
                if line.startswith('message '):
                    name = line.split()[1]
                    if not name[0].isupper() or '_' in name:
                        self.warnings.append(
                            f"Naming convention in {proto_file.name}:{i} - "
                            f"message '{name}' should be PascalCase"
                        )
                        issues_found = True
                
                # Check enum names (should be UPPER_SNAKE_CASE)
                if line.startswith('enum '):
                    name = line.split()[1]
                    if not name.isupper():
                        self.warnings.append(
                            f"Naming convention in {proto_file.name}:{i} - "
                            f"enum '{name}' should be UPPER_SNAKE_CASE"
                        )
                        issues_found = True
                
                # Check field names (should be snake_case)
                if '=' in line and not line.startswith('//'):
                    parts = line.split('=')
                    if len(parts) >= 2:
                        field_part = parts[0].strip().split()
                        if len(field_part) >= 2:
                            field_name = field_part[-1]
                            if field_name[0].isupper() or '-' in field_name:
                                self.warnings.append(
                                    f"Naming convention in {proto_file.name}:{i} - "
                                    f"field '{field_name}' should be snake_case"
                                )
                                issues_found = True
        
        if not issues_found:
            print("✅ Naming conventions validated")
            
        return True  # Warnings don't fail validation
    
    def validate_dependencies(self) -> bool:
        """Validate import dependencies"""
        print("\n🔗 Validating dependencies...")
        
        proto_files = list(self.proto_dir.glob("*.proto"))
        imports = {}
        
        # Collect all imports
        for proto_file in proto_files:
            with open(proto_file, 'r') as f:
                content = f.read()
                
            file_imports = []
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('import '):
                    import_path = line.split('"')[1]
                    file_imports.append(import_path)
                    
            imports[proto_file.name] = file_imports
        
        # Check for circular dependencies
        def has_circular_dependency(file1: str, file2: str, visited: set) -> bool:
            if file1 in visited:
                return True
            visited.add(file1)
            
            for imported in imports.get(file1, []):
                imported_name = Path(imported).name
                if imported_name == file2:
                    return True
                if has_circular_dependency(imported_name, file2, visited.copy()):
                    return True
            return False
        
        circular_found = False
        for file_name, file_imports in imports.items():
            for imported in file_imports:
                imported_name = Path(imported).name
                if has_circular_dependency(imported_name, file_name, set()):
                    self.violations.append(
                        f"Circular dependency detected: {file_name} ↔ {imported_name}"
                    )
                    circular_found = True
        
        # Check for missing imports
        missing_found = False
        for file_name, file_imports in imports.items():
            for imported in file_imports:
                if not imported.startswith('google/') and not imported.startswith('buf.build/'):
                    imported_path = self.proto_dir / imported
                    if not imported_path.exists():
                        self.violations.append(
                            f"Missing import in {file_name}: {imported} not found"
                        )
                        missing_found = True
        
        if not circular_found and not missing_found:
            print("✅ Dependencies validated")
            
        return not (circular_found or missing_found)
    
    def print_results(self):
        """Print validation results"""
        print("\n" + "="*60)
        print("🎯 ATCG PROTOBUF VALIDATION RESULTS")
        print("="*60)
        
        if not self.violations and not self.warnings:
            print("✅ ALL VALIDATIONS PASSED")
            print("🕊️ Schemas are ontologically pure and technically correct")
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
    validator = SchemaValidator()
    success = validator.validate_all()
    
    if success:
        print("\n🎉 Protobuf schemas ready for sacred implementation!")
        sys.exit(0)
    else:
        print("\n💀 Validation failed - fix issues before proceeding")
        sys.exit(1)

if __name__ == "__main__":
    main()