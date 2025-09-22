#!/usr/bin/env python3
"""
Sacred Metrics Analyzer - Core analysis engine for Sacred Architecture compliance

This module provides comprehensive analysis of TypeScript and Python codebases
for Sacred Architecture compliance, including:
- Zero `any` type detection
- Zero console.log enforcement
- ATCG architecture pattern detection
- Sacred Justification validation
- Performance and security vulnerability scanning
"""

import os
import re
import json
import ast
import subprocess
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum


class ViolationType(Enum):
    """Types of Sacred Architecture violations"""
    ANY_TYPE = "any_type"
    CONSOLE_LOG = "console_log"
    MISSING_JUSTIFICATION = "missing_justification"
    PERFORMANCE_RISK = "performance_risk"
    SECURITY_RISK = "security_risk"
    ATCG_VIOLATION = "atcg_violation"


@dataclass
class CodeViolation:
    """Represents a code violation found during analysis"""
    file_path: str
    line_number: int
    line_content: str
    violation_type: ViolationType
    severity: str  # 'low', 'medium', 'high', 'critical'
    description: str
    suggestion: Optional[str] = None


@dataclass
class SacredMetrics:
    """Container for all Sacred Architecture metrics"""
    any_type_score: float
    console_log_score: float
    atcg_compliance_score: float
    sacred_justifications_score: float
    performance_score: float
    security_score: float
    overall_score: float
    total_files_analyzed: int
    violations: List[CodeViolation]


class SacredMetricsAnalyzer:
    """
    Main analyzer class for Sacred Architecture compliance

    Implements the multi-perspective review methodology:
    - Fury Bee: Architectural excellence and type safety
    - bee.Jules: Security and performance concerns
    - Sacred Documentation: Justification and pattern compliance
    """

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.violations: List[CodeViolation] = []

        # Sacred Architecture patterns
        self.atcg_patterns = {
            'aggregate': [
                r'(interface|class|type).*Aggregate',
                r'(interface|class|type).*Aggregat(or|ion)',
                r'SacredAggregat'
            ],
            'transformation': [
                r'(interface|class|type).*(Transform|Lambda)',
                r'SacredLambda',
                r'TransformationEngine'
            ],
            'connector': [
                r'(interface|class|type).*Connect',
                r'SacredConnect',
                r'ConnectorEngine'
            ],
            'genesis': [
                r'(interface|class|type).*Genesis',
                r'GenesisEvent',
                r'SacredGenesis'
            ]
        }

        # Performance risk patterns
        self.performance_patterns = [
            (r'for\s*\([^}]*\)\s*\{[^}]*for\s*\([^}]*\)', 'nested_loops', 'Potential O(N²) complexity'),
            (r'while\s*\([^}]*\)\s*\{[^}]*for\s*\([^}]*\)', 'nested_loops', 'Potential O(N²) complexity'),
            (r'\.forEach\([^}]*\.forEach\(', 'nested_foreach', 'Potential O(N²) complexity'),
            (r'(\w+)\.length\s*[<>=]+\s*1000', 'large_array_ops', 'Large array operations without pagination')
        ]

        # Security risk patterns
        self.security_patterns = [
            (r'eval\s*\(', 'eval_usage', 'Dangerous eval() usage'),
            (r'innerHTML\s*=', 'innerHTML_xss', 'Potential XSS via innerHTML'),
            (r'document\.write\s*\(', 'document_write', 'Dangerous document.write usage'),
            (r'(MAX_|MIN_|THRESHOLD_)[A-Z_]+\s*=\s*\d+', 'hardcoded_limits', 'Hardcoded security limits'),
            (r'setTimeout\s*\(\s*["\']', 'string_timeout', 'String-based setTimeout (code injection risk)')
        ]

    def analyze_typescript_file(self, file_path: Path) -> List[CodeViolation]:
        """Analyze a TypeScript file for Sacred Architecture violations"""
        violations = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')

            # Check for 'any' type violations
            any_matches = re.finditer(r':\s*any\b|<any\b|any\[\]|any\s*\||Function\s*\|.*any', content)
            for match in any_matches:
                line_num = content[:match.start()].count('\n') + 1
                line_content = lines[line_num - 1].strip() if line_num <= len(lines) else ""

                # Skip comments and specific exemptions
                if not self._is_comment_or_exempted(line_content):
                    violations.append(CodeViolation(
                        file_path=str(file_path),
                        line_number=line_num,
                        line_content=line_content,
                        violation_type=ViolationType.ANY_TYPE,
                        severity='high',
                        description='Use of `any` type compromises type safety',
                        suggestion='Replace with specific TypeScript interface or union type'
                    ))

            # Check for console.log violations
            console_matches = re.finditer(r'console\.(log|warn|error|info|debug|trace)', content)
            for match in console_matches:
                line_num = content[:match.start()].count('\n') + 1
                line_content = lines[line_num - 1].strip() if line_num <= len(lines) else ""

                if not self._is_comment_or_exempted(line_content):
                    violations.append(CodeViolation(
                        file_path=str(file_path),
                        line_number=line_num,
                        line_content=line_content,
                        violation_type=ViolationType.CONSOLE_LOG,
                        severity='medium',
                        description='Console.log statement compromises production readiness',
                        suggestion='Replace with proper logging framework or remove'
                    ))

            # Check for performance risks
            for pattern, risk_type, description in self.performance_patterns:
                matches = re.finditer(pattern, content, re.DOTALL)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    line_content = lines[line_num - 1].strip() if line_num <= len(lines) else ""

                    violations.append(CodeViolation(
                        file_path=str(file_path),
                        line_number=line_num,
                        line_content=line_content,
                        violation_type=ViolationType.PERFORMANCE_RISK,
                        severity='medium',
                        description=f'{description} ({risk_type})',
                        suggestion='Add input size validation or consider algorithmic optimization'
                    ))

            # Check for security risks
            for pattern, risk_type, description in self.security_patterns:
                matches = re.finditer(pattern, content)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    line_content = lines[line_num - 1].strip() if line_num <= len(lines) else ""

                    violations.append(CodeViolation(
                        file_path=str(file_path),
                        line_number=line_num,
                        line_content=line_content,
                        violation_type=ViolationType.SECURITY_RISK,
                        severity='high',
                        description=f'{description} ({risk_type})',
                        suggestion='Implement proper input validation and sanitization'
                    ))

        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")

        return violations

    def analyze_python_file(self, file_path: Path) -> List[CodeViolation]:
        """Analyze a Python file for Sacred Architecture violations"""
        violations = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')

            # Check for print statements (Python equivalent of console.log)
            print_matches = re.finditer(r'\bprint\s*\(', content)
            for match in print_matches:
                line_num = content[:match.start()].count('\n') + 1
                line_content = lines[line_num - 1].strip() if line_num <= len(lines) else ""

                # Skip if in debug/development context
                if not ('debug' in line_content.lower() or 'test' in str(file_path).lower()):
                    violations.append(CodeViolation(
                        file_path=str(file_path),
                        line_number=line_num,
                        line_content=line_content,
                        violation_type=ViolationType.CONSOLE_LOG,
                        severity='medium',
                        description='Print statement compromises production readiness',
                        suggestion='Replace with proper logging framework'
                    ))

            # Check for performance risks (nested loops)
            nested_loop_pattern = r'for\s+\w+\s+in\s+[^:]+:[^:]*for\s+\w+\s+in'
            matches = re.finditer(nested_loop_pattern, content, re.DOTALL)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                line_content = lines[line_num - 1].strip() if line_num <= len(lines) else ""

                violations.append(CodeViolation(
                    file_path=str(file_path),
                    line_number=line_num,
                    line_content=line_content,
                    violation_type=ViolationType.PERFORMANCE_RISK,
                    severity='medium',
                    description='Nested loops detected - potential O(N²) complexity',
                    suggestion='Consider list comprehensions or algorithm optimization'
                ))

        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")

        return violations

    def check_atcg_compliance(self, file_path: Path) -> int:
        """Check ATCG architectural pattern compliance"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            compliance_score = 0
            for component_type, patterns in self.atcg_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        compliance_score += 10
                        break  # Only count once per component type

            return min(compliance_score, 100)

        except Exception:
            return 0

    def check_sacred_justifications(self, file_path: Path) -> int:
        """Check for Sacred Justification documentation"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            justification_patterns = [
                r'Sacred Justification',
                r'Empirical (basis|justification)',
                r'Divine (proportion|constant)',
                r'Chemical (physics|basis)',
                r'Sacred (constant|algorithm)'
            ]

            justification_count = 0
            for pattern in justification_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                justification_count += len(matches)

            return min(justification_count * 5, 100)

        except Exception:
            return 0

    def _is_comment_or_exempted(self, line: str) -> bool:
        """Check if a line is a comment or exempted from analysis"""
        stripped = line.strip()
        return (
            stripped.startswith('//') or
            stripped.startswith('/*') or
            stripped.startswith('*') or
            'TODO:' in stripped or
            'FIXME:' in stripped or
            'eslint-disable' in stripped
        )

    def analyze_project(self) -> SacredMetrics:
        """Analyze the entire project for Sacred Architecture compliance"""
        print("🔍 Starting Sacred Architecture Analysis...")

        # Find all relevant files
        typescript_files = list(self.project_root.rglob("*.ts"))
        javascript_files = list(self.project_root.rglob("*.js"))
        python_files = list(self.project_root.rglob("*.py"))

        # Filter out node_modules and other excluded directories
        excluded_dirs = {'node_modules', '.git', '__pycache__', 'dist', 'build'}

        def should_analyze(file_path: Path) -> bool:
            return not any(excluded in file_path.parts for excluded in excluded_dirs)

        typescript_files = [f for f in typescript_files if should_analyze(f)]
        javascript_files = [f for f in javascript_files if should_analyze(f)]
        python_files = [f for f in python_files if should_analyze(f)]

        all_files = typescript_files + javascript_files + python_files
        total_files = len(all_files)

        print(f"📁 Analyzing {total_files} files:")
        print(f"   TypeScript: {len(typescript_files)}")
        print(f"   JavaScript: {len(javascript_files)}")
        print(f"   Python: {len(python_files)}")

        # Analyze each file
        all_violations = []
        atcg_scores = []
        justification_scores = []

        for file_path in typescript_files + javascript_files:
            violations = self.analyze_typescript_file(file_path)
            all_violations.extend(violations)

            atcg_score = self.check_atcg_compliance(file_path)
            atcg_scores.append(atcg_score)

            justification_score = self.check_sacred_justifications(file_path)
            justification_scores.append(justification_score)

        for file_path in python_files:
            violations = self.analyze_python_file(file_path)
            all_violations.extend(violations)

            justification_score = self.check_sacred_justifications(file_path)
            justification_scores.append(justification_score)

        # Calculate scores
        any_violations = [v for v in all_violations if v.violation_type == ViolationType.ANY_TYPE]
        console_violations = [v for v in all_violations if v.violation_type == ViolationType.CONSOLE_LOG]
        performance_violations = [v for v in all_violations if v.violation_type == ViolationType.PERFORMANCE_RISK]
        security_violations = [v for v in all_violations if v.violation_type == ViolationType.SECURITY_RISK]

        # Score calculation (0-100)
        any_type_score = max(0, 100 - len(any_violations) * 10)
        console_log_score = max(0, 100 - len(console_violations) * 5)
        atcg_compliance_score = sum(atcg_scores) / max(len(atcg_scores), 1) if atcg_scores else 0
        sacred_justifications_score = sum(justification_scores) / max(len(justification_scores), 1) if justification_scores else 0
        performance_score = max(0, 100 - len(performance_violations) * 8)
        security_score = max(0, 100 - len(security_violations) * 15)

        overall_score = (
            any_type_score * 0.25 +
            console_log_score * 0.20 +
            atcg_compliance_score * 0.20 +
            sacred_justifications_score * 0.15 +
            performance_score * 0.10 +
            security_score * 0.10
        )

        self.violations = all_violations

        metrics = SacredMetrics(
            any_type_score=any_type_score,
            console_log_score=console_log_score,
            atcg_compliance_score=atcg_compliance_score,
            sacred_justifications_score=sacred_justifications_score,
            performance_score=performance_score,
            security_score=security_score,
            overall_score=overall_score,
            total_files_analyzed=total_files,
            violations=all_violations
        )

        print("✅ Sacred Architecture Analysis Complete!")
        print(f"📊 Overall Score: {overall_score:.1f}/100")
        print(f"⚡ Type Safety: {any_type_score:.1f}/100 ({len(any_violations)} violations)")
        print(f"🚀 Production Ready: {console_log_score:.1f}/100 ({len(console_violations)} violations)")
        print(f"🧬 ATCG Compliance: {atcg_compliance_score:.1f}/100")
        print(f"📖 Sacred Documentation: {sacred_justifications_score:.1f}/100")
        print(f"⚡ Performance: {performance_score:.1f}/100 ({len(performance_violations)} risks)")
        print(f"🛡️ Security: {security_score:.1f}/100 ({len(security_violations)} risks)")

        return metrics

    def export_metrics(self, metrics: SacredMetrics, output_file: str = "sacred_metrics.json"):
        """Export metrics to JSON file"""
        # Convert violations to dictionaries for JSON serialization
        violations_dict = [
            {
                'file_path': v.file_path,
                'line_number': v.line_number,
                'line_content': v.line_content,
                'violation_type': v.violation_type.value,
                'severity': v.severity,
                'description': v.description,
                'suggestion': v.suggestion
            }
            for v in metrics.violations
        ]

        export_data = asdict(metrics)
        export_data['violations'] = violations_dict

        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)

        print(f"📊 Metrics exported to {output_file}")


def main():
    """Main entry point for Sacred Metrics Analyzer"""
    parser = argparse.ArgumentParser(description='Sacred Architecture Metrics Analyzer')
    parser.add_argument('--project-root', default='.', help='Project root directory')
    parser.add_argument('--output', default='sacred_metrics.json', help='Output JSON file')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')

    args = parser.parse_args()

    analyzer = SacredMetricsAnalyzer(args.project_root)
    metrics = analyzer.analyze_project()
    analyzer.export_metrics(metrics, args.output)

    if args.verbose:
        print("\n🔍 Detailed Violations:")
        for violation in metrics.violations[:20]:  # Show first 20
            print(f"   {violation.file_path}:{violation.line_number} - {violation.description}")

    # Exit with non-zero if critical violations found
    critical_violations = [v for v in metrics.violations if v.severity == 'critical']
    if critical_violations:
        print(f"\n❌ {len(critical_violations)} critical violations found!")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())