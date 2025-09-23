#!/usr/bin/env python3
"""
🐝⚡ Sacred Hive Validation System ⚡🐝
Proverbs-Based Code Quality Assessment Tool

Based on the enhanced 10-pattern AlgoGenesis system derived from Biblical Proverbs
and the LORD OF HOSTS' divine algorithmic principles.

Usage: python sacred_validation.py [path_to_analyze]
"""

import os
import ast
import re
from pathlib import Path
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class SacredMetrics:
    """Sacred metrics based on Proverbs patterns"""
    seven_fold_completion: float
    three_four_transcendence: float
    wisdom_accumulation: float
    correction_responsiveness: float
    divine_timing_alignment: float
    phi_ratio_manifestation: float
    trinity_clustering: float
    boolean_separation: float
    layer_abstraction: float
    interface_consolidation: float

    @property
    def overall_sacred_score(self) -> float:
        """Calculate overall sacred score from all patterns"""
        all_scores = [
            self.seven_fold_completion,
            self.three_four_transcendence,
            self.wisdom_accumulation,
            self.correction_responsiveness,
            self.divine_timing_alignment,
            self.phi_ratio_manifestation,
            self.trinity_clustering,
            self.boolean_separation,
            self.layer_abstraction,
            self.interface_consolidation
        ]
        return sum(all_scores) / len(all_scores)

    @property
    def proverbs_compliance(self) -> bool:
        """Check if code meets sacred 7/9 ratio (0.77 threshold)"""
        return self.overall_sacred_score >= 0.77

    @property
    def lord_of_hosts_blessing(self) -> str:
        """Determine blessing level based on sacred score"""
        score = self.overall_sacred_score
        if score >= 0.95:
            return "ABUNDANT"
        elif score >= 0.85:
            return "BLESSED"
        elif score >= 0.77:
            return "FAVORED"
        elif score >= 0.65:
            return "SEEKING"
        else:
            return "NEEDS_PRAYER"
    
    def get_complete_metrics(self) -> Dict[str, Any]:
        """Get complete metrics dictionary for HiveHost compatibility"""
        return {
            "sacred_score": self.overall_sacred_score,
            "proverbs_compliance": self.proverbs_compliance,
            "blessing_level": self.lord_of_hosts_blessing,
            "seven_fold_completion": self.seven_fold_completion,
            "three_four_transcendence": self.three_four_transcendence,
            "wisdom_accumulation": self.wisdom_accumulation,
            "correction_responsiveness": self.correction_responsiveness,
            "divine_timing_alignment": self.divine_timing_alignment,
            "phi_ratio_manifestation": self.phi_ratio_manifestation,
            "trinity_clustering": self.trinity_clustering,
            "boolean_separation": self.boolean_separation,
            "layer_abstraction": self.layer_abstraction,
            "interface_consolidation": self.interface_consolidation
        }
    
    def update_genesis_protocol_health(self, light_success: bool, separation_success: bool, manifestation_success: bool):
        """Update genesis protocol health metrics (HiveHost compatibility)"""
        # For now, just log the update - could be extended to track protocol health
        pass
    
    def record_sacred_commit(self, commit_data: Dict[str, Any]):
        """Record sacred commit metrics (HiveHost compatibility)"""
        # For now, just log the commit - could be extended to track commit quality
        pass
    
    def record_divine_event(self, event_type: str, blessing_level: float):
        """Record divine event metrics (HiveHost compatibility)"""
        # For now, just log the event - could be extended to track divine events
        pass
    
    def get_sacred_health_assessment(self) -> Dict[str, Any]:
        """Get sacred health assessment (HiveHost compatibility)"""
        return {
            "overall_health": "BLESSED" if self.overall_sacred_score >= 0.8 else "SEEKING",
            "sacred_health_status": "BLESSED" if self.overall_sacred_score >= 0.8 else "SEEKING",
            "sacred_score": self.overall_sacred_score,
            "proverbs_compliance": self.proverbs_compliance,
            "blessing_level": self.lord_of_hosts_blessing,
            "recommendations": []
        }


class SacredCodeAnalyzer:
    """Analyzes code for divine Proverbs patterns"""

    def __init__(self, path: str):
        self.path = Path(path)
        self.files_analyzed = []
        self.functions_found = []
        self.classes_found = []
        self.api_endpoints = []
        self.database_tables = []

    def analyze_codebase(self) -> SacredMetrics:
        """Perform complete sacred analysis of codebase"""

        # Collect all Python files
        python_files = list(self.path.rglob("*.py"))
        self.files_analyzed = [f for f in python_files if not self._is_excluded(f)]

        # Analyze each file
        for file_path in self.files_analyzed:
            self._analyze_file(file_path)

        # Calculate sacred metrics
        return SacredMetrics(
            seven_fold_completion=self._calculate_seven_fold_completion(),
            three_four_transcendence=self._calculate_three_four_transcendence(),
            wisdom_accumulation=self._calculate_wisdom_accumulation(),
            correction_responsiveness=self._calculate_correction_responsiveness(),
            divine_timing_alignment=self._calculate_divine_timing(),
            phi_ratio_manifestation=self._calculate_phi_ratios(),
            trinity_clustering=self._calculate_trinity_clustering(),
            boolean_separation=self._calculate_boolean_separation(),
            layer_abstraction=self._calculate_layer_abstraction(),
            interface_consolidation=self._calculate_interface_consolidation()
        )

    def _is_excluded(self, file_path: Path) -> bool:
        """Check if file should be excluded from analysis"""
        excluded_patterns = [
            "__pycache__",
            ".venv",
            "node_modules",
            ".git",
            "test_",
            "_test.py"
        ]
        return any(pattern in str(file_path) for pattern in excluded_patterns)

    def _analyze_file(self, file_path: Path):
        """Analyze individual Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                tree = ast.parse(content)

            # Extract functions and classes
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    self.functions_found.append({
                        'name': node.name,
                        'args_count': len(node.args.args),
                        'file': str(file_path),
                        'lineno': node.lineno
                    })
                elif isinstance(node, ast.ClassDef):
                    self.classes_found.append({
                        'name': node.name,
                        'file': str(file_path),
                        'lineno': node.lineno
                    })

            # Look for API endpoints
            self._find_api_endpoints(content, file_path)

            # Look for database tables
            self._find_database_tables(content, file_path)

        except Exception as e:
            print(f"Warning: Could not analyze {file_path}: {e}")

    def _find_api_endpoints(self, content: str, file_path: Path):
        """Find API endpoint definitions"""
        endpoint_patterns = [
            r'@app\.(get|post|put|delete)\("([^"]+)"',
            r'@router\.(get|post|put|delete)\("([^"]+)"',
            r'@.*\.(get|post|put|delete)\("([^"]+)"'
        ]

        for pattern in endpoint_patterns:
            matches = re.findall(pattern, content)
            for method, endpoint in matches:
                self.api_endpoints.append({
                    'method': method.upper(),
                    'endpoint': endpoint,
                    'file': str(file_path)
                })

    def _find_database_tables(self, content: str, file_path: Path):
        """Find database table definitions"""
        table_patterns = [
            r'CREATE TABLE IF NOT EXISTS (\w+)',
            r'CREATE TABLE (\w+)',
            r'Table\(["\'](\w+)["\']'
        ]

        for pattern in table_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for table in matches:
                if table not in [t['name'] for t in self.database_tables]:
                    self.database_tables.append({
                        'name': table,
                        'file': str(file_path)
                    })

    def _calculate_seven_fold_completion(self) -> float:
        """Calculate seven-fold completion pattern (Proverbs 6:16-19)"""
        endpoint_count = len(self.api_endpoints)
        table_count = len(self.database_tables)

        # Score based on proximity to sacred 7
        endpoint_score = min(endpoint_count / 7.0, 1.0)
        table_score = min(table_count / 7.0, 1.0)

        return (endpoint_score + table_score) / 2.0

    def _calculate_three_four_transcendence(self) -> float:
        """Calculate three-four transcendence pattern (Proverbs 30:18-19)"""
        # Analyze function parameter clustering
        param_counts = defaultdict(int)
        for func in self.functions_found:
            param_counts[func['args_count']] += 1

        # Sacred scores for parameter counts
        three_param_functions = param_counts[3]
        four_param_functions = param_counts[4]

        # Higher score for 3-4 parameter clustering
        total_functions = len(self.functions_found)
        if total_functions == 0:
            return 0.0

        sacred_ratio = (three_param_functions + four_param_functions) / total_functions
        return min(sacred_ratio * 2.0, 1.0)  # Boost sacred patterns

    def _calculate_wisdom_accumulation(self) -> float:
        """Calculate wisdom accumulation patterns (Proverbs 4:7)"""
        # Look for learning/feedback patterns
        learning_indicators = 0
        total_files = len(self.files_analyzed)

        for file_path in self.files_analyzed:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().lower()

                learning_keywords = [
                    'learn', 'feedback', 'improve', 'enhance', 'optimize',
                    'sacred', 'wisdom', 'insight', 'knowledge', 'accumulate'
                ]

                if any(keyword in content for keyword in learning_keywords):
                    learning_indicators += 1
            except:
                continue

        return learning_indicators / total_files if total_files > 0 else 0.0

    def _calculate_correction_responsiveness(self) -> float:
        """Calculate correction protocol patterns (Proverbs 12:1)"""
        # Look for comments indicating awareness of needed improvements
        correction_indicators = 0
        total_files = len(self.files_analyzed)

        for file_path in self.files_analyzed:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                correction_patterns = [
                    r'#.*TODO',
                    r'#.*FIXME',
                    r'#.*can be.*later',
                    r'#.*improve',
                    r'#.*optimize',
                    r'#.*refactor'
                ]

                if any(re.search(pattern, content, re.IGNORECASE) for pattern in correction_patterns):
                    correction_indicators += 1
            except:
                continue

        return correction_indicators / total_files if total_files > 0 else 0.0

    def _calculate_divine_timing(self) -> float:
        """Calculate divine timing patterns (Ecclesiastes 3:1)"""
        # Look for conditional initialization and timing patterns
        timing_patterns = 0
        total_files = len(self.files_analyzed)

        for file_path in self.files_analyzed:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                timing_indicators = [
                    r'if.*available',
                    r'if.*ready',
                    r'@asynccontextmanager',
                    r'lifespan',
                    r'startup',
                    r'shutdown'
                ]

                if any(re.search(pattern, content, re.IGNORECASE) for pattern in timing_indicators):
                    timing_patterns += 1
            except:
                continue

        return timing_patterns / total_files if total_files > 0 else 0.0

    def _calculate_phi_ratios(self) -> float:
        """Calculate golden ratio manifestations"""
        # Analyze file size ratios
        file_sizes = []
        for file_path in self.files_analyzed:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = len(f.readlines())
                    file_sizes.append(lines)
            except:
                continue

        if len(file_sizes) < 2:
            return 0.0

        # Look for ratios close to φ (1.618)
        phi = 1.618
        phi_scores = []

        file_sizes.sort(reverse=True)
        for i in range(len(file_sizes) - 1):
            if file_sizes[i+1] > 0:
                ratio = file_sizes[i] / file_sizes[i+1]
                distance_from_phi = abs(ratio - phi)
                # Score inversely proportional to distance from phi
                phi_score = max(0, 1 - distance_from_phi)
                phi_scores.append(phi_score)

        return max(phi_scores) if phi_scores else 0.0

    def _calculate_trinity_clustering(self) -> float:
        """Calculate trinity parameter clustering"""
        param_counts = defaultdict(int)
        for func in self.functions_found:
            param_counts[func['args_count']] += 1

        total_functions = len(self.functions_found)
        if total_functions == 0:
            return 0.0

        # Sacred number preferences: 3, 7, 9
        sacred_functions = param_counts[3] + param_counts[7] + param_counts[9]
        return sacred_functions / total_functions

    def _calculate_boolean_separation(self) -> float:
        """Calculate boolean separation patterns (Genesis 1:3)"""
        boolean_patterns = 0
        total_files = len(self.files_analyzed)

        for file_path in self.files_analyzed:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Look for clear boolean logic patterns
                if re.search(r'if\s+\w+\s+and\s+not\s+\w+', content):
                    boolean_patterns += 1
                elif re.search(r'if\s+\w+.*==.*True', content):
                    boolean_patterns += 1
                elif 'True' in content and 'False' in content:
                    boolean_patterns += 1
            except:
                continue

        return boolean_patterns / total_files if total_files > 0 else 0.0

    def _calculate_layer_abstraction(self) -> float:
        """Calculate layer abstraction patterns (Genesis 1:7)"""
        # Look for clear separation of concerns
        abstraction_score = 0.0

        # Check for modular structure
        api_files = [f for f in self.files_analyzed if 'api' in str(f)]
        if api_files:
            abstraction_score += 0.3

        # Check for separate database files
        db_files = [f for f in self.files_analyzed if any(db_word in str(f).lower()
                   for db_word in ['database', 'db', 'model'])]
        if db_files:
            abstraction_score += 0.3

        # Check for connection/manager separation
        manager_files = [f for f in self.files_analyzed if 'manager' in str(f)]
        if manager_files:
            abstraction_score += 0.4

        return min(abstraction_score, 1.0)

    def _calculate_interface_consolidation(self) -> float:
        """Calculate interface consolidation patterns (Genesis 1:9)"""
        # Score based on API endpoint organization
        if not self.api_endpoints:
            return 0.0

        # Group endpoints by file
        endpoints_by_file = defaultdict(list)
        for endpoint in self.api_endpoints:
            endpoints_by_file[endpoint['file']].append(endpoint)

        # Higher score for consolidated endpoints
        total_files_with_endpoints = len(endpoints_by_file)
        if total_files_with_endpoints <= 5:  # Consolidated
            return 1.0
        elif total_files_with_endpoints <= 10:  # Moderately consolidated
            return 0.7
        else:  # Scattered
            return 0.3


def main():
    """Main sacred validation function"""
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else "."

    print("🐝⚡ Sacred Hive Validation System ⚡🐝")
    print("Proverbs-Based Code Quality Assessment")
    print("=" * 50)
    print()

    analyzer = SacredCodeAnalyzer(path)
    metrics = analyzer.analyze_codebase()

    print(f"📊 SACRED METRICS ANALYSIS")
    print(f"Files Analyzed: {len(analyzer.files_analyzed)}")
    print(f"Functions Found: {len(analyzer.functions_found)}")
    print(f"Classes Found: {len(analyzer.classes_found)}")
    print(f"API Endpoints: {len(analyzer.api_endpoints)}")
    print(f"Database Tables: {len(analyzer.database_tables)}")
    print()

    print("🌟 PROVERBS PATTERN SCORES:")
    print(f"  Seven-Fold Completion:      {metrics.seven_fold_completion:.2f}")
    print(f"  Three-Four Transcendence:   {metrics.three_four_transcendence:.2f}")
    print(f"  Wisdom Accumulation:        {metrics.wisdom_accumulation:.2f}")
    print(f"  Correction Responsiveness:  {metrics.correction_responsiveness:.2f}")
    print(f"  Divine Timing Alignment:    {metrics.divine_timing_alignment:.2f}")
    print(f"  Phi Ratio Manifestation:    {metrics.phi_ratio_manifestation:.2f}")
    print(f"  Trinity Clustering:         {metrics.trinity_clustering:.2f}")
    print(f"  Boolean Separation:         {metrics.boolean_separation:.2f}")
    print(f"  Layer Abstraction:          {metrics.layer_abstraction:.2f}")
    print(f"  Interface Consolidation:    {metrics.interface_consolidation:.2f}")
    print()

    print("🎯 SACRED ASSESSMENT:")
    print(f"  Overall Sacred Score:       {metrics.overall_sacred_score:.2f}")
    print(f"  Proverbs Compliance:        {'✅ YES' if metrics.proverbs_compliance else '❌ NO'}")
    print(f"  LORD OF HOSTS Blessing:     {metrics.lord_of_hosts_blessing}")
    print()

    if metrics.overall_sacred_score >= 0.9:
        print("🌟 DIVINE EXCELLENCE: Your code manifests sacred patterns abundantly!")
    elif metrics.overall_sacred_score >= 0.77:
        print("✅ SACRED COMPLIANCE: Your code aligns with divine principles!")
    else:
        print("🙏 SEEKING IMPROVEMENT: Consider enhancing sacred pattern alignment.")

    print("\n📜 'The fear of the LORD is the beginning of wisdom' - Proverbs 9:10")


if __name__ == "__main__":
    main()