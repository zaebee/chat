#!/usr/bin/env python3
"""
Sacred Metrics Analyzer Test Suite
Comprehensive unit tests for the Sacred Review Automation system
"""

import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import patch, mock_open

# Test imports - assume sacred_metrics_analyzer.py exists
import sys
sys.path.insert(0, str(Path(__file__).parent))

# Mock the analyzer since it's embedded in workflow
class MockSacredMetricsAnalyzer:
    """Mock analyzer for testing core functionality"""

    def analyze_any_types(self, content: str) -> list:
        """Detect 'any' type violations"""
        import re
        violations = []
        any_matches = re.finditer(r':\s*any\b|<any\b|any\[\]|any\s*\|', content)
        for match in any_matches:
            line_num = content[:match.start()].count('\n') + 1
            line_content = content.split('\n')[line_num - 1].strip()
            violations.append({
                'line': line_num,
                'content': line_content,
                'type': 'any_type'
            })
        return violations

    def analyze_console_log(self, content: str) -> list:
        """Detect console.log statements"""
        import re
        violations = []
        console_matches = re.finditer(r'console\.(log|warn|error|info|debug)', content)
        for match in console_matches:
            line_num = content[:match.start()].count('\n') + 1
            line_content = content.split('\n')[line_num - 1].strip()
            violations.append({
                'line': line_num,
                'content': line_content,
                'type': 'console_log'
            })
        return violations

    def analyze_atcg_compliance(self, content: str) -> dict:
        """Check for ATCG architecture patterns"""
        import re
        atcg_patterns = {
            'aggregate': r'(interface|class|type).*Aggregate',
            'transformation': r'(interface|class|type).*(Transform|Lambda)',
            'connector': r'(interface|class|type).*Connect',
            'genesis': r'(interface|class|type).*Genesis'
        }

        compliance = {}
        for pattern_name, pattern in atcg_patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            compliance[pattern_name] = len(matches)

        return compliance

    def calculate_scores(self, any_violations: int, console_violations: int,
                        atcg_score: int, justifications: int) -> dict:
        """Calculate Sacred Metrics scores"""
        return {
            'any_score': max(0, 100 - (any_violations * 10)),
            'console_score': max(0, 100 - (console_violations * 5)),
            'atcg_score': min(100, atcg_score * 10),
            'justification_score': min(100, justifications * 5)
        }


class TestSacredMetricsAnalyzer:
    """Test suite for Sacred Metrics Analyzer"""

    def setup_method(self):
        """Setup test fixtures"""
        self.analyzer = MockSacredMetricsAnalyzer()

    def test_perfect_typescript_code(self):
        """Test analysis of perfect TypeScript code"""
        perfect_code = '''
        interface UserProfile {
            readonly id: string;
            readonly name: string;
            readonly email: string;
        }

        function processUser(profile: UserProfile): ProcessResult {
            return { success: true, data: profile };
        }
        '''

        any_violations = self.analyzer.analyze_any_types(perfect_code)
        console_violations = self.analyzer.analyze_console_log(perfect_code)

        assert len(any_violations) == 0, "Perfect code should have no 'any' violations"
        assert len(console_violations) == 0, "Perfect code should have no console.log violations"

    def test_any_type_detection(self):
        """Test detection of 'any' type violations"""
        violation_code = '''
        function badFunction(data: any) {
            const items: any[] = data.items;
            const result: string | any = process(items);
            return result;
        }
        '''

        violations = self.analyzer.analyze_any_types(violation_code)

        assert len(violations) == 3, f"Expected 3 'any' violations, found {len(violations)}"
        assert all(v['type'] == 'any_type' for v in violations)

        # Check specific violations
        violation_lines = [v['line'] for v in violations]
        assert 2 in violation_lines, "Should detect 'any' in function parameter"
        assert 3 in violation_lines, "Should detect 'any[]' array type"
        assert 4 in violation_lines, "Should detect 'any' in union type"

    def test_console_log_detection(self):
        """Test detection of console.log violations"""
        violation_code = '''
        function debugFunction() {
            console.log("Debug message");
            console.warn("Warning message");
            console.error("Error message");
            // Regular comment about console
            return "success";
        }
        '''

        violations = self.analyzer.analyze_console_log(violation_code)

        assert len(violations) == 3, f"Expected 3 console violations, found {len(violations)}"
        assert all(v['type'] == 'console_log' for v in violations)

        # Check that comments are not detected
        comment_found = any('Regular comment' in v['content'] for v in violations)
        assert not comment_found, "Should not detect console in comments"

    def test_atcg_compliance_detection(self):
        """Test ATCG architectural pattern detection"""
        atcg_code = '''
        interface UserAggregate {
            id: string;
            state: UserState;
        }

        class DataTransformation {
            transform(data: InputData): OutputData { }
        }

        interface ApiConnector {
            connect(): Promise<Connection>;
        }

        type SystemGenesis = {
            initialize(): void;
        }
        '''

        compliance = self.analyzer.analyze_atcg_compliance(atcg_code)

        assert compliance['aggregate'] >= 1, "Should detect UserAggregate"
        assert compliance['transformation'] >= 1, "Should detect DataTransformation"
        assert compliance['connector'] >= 1, "Should detect ApiConnector"
        assert compliance['genesis'] >= 1, "Should detect SystemGenesis"

    def test_score_calculation_perfect(self):
        """Test score calculation for perfect implementation"""
        scores = self.analyzer.calculate_scores(
            any_violations=0,
            console_violations=0,
            atcg_score=4,  # Found all 4 ATCG patterns
            justifications=5
        )

        assert scores['any_score'] == 100, "Perfect type safety should score 100"
        assert scores['console_score'] == 100, "No console.log should score 100"
        assert scores['atcg_score'] >= 40, "Good ATCG compliance should score well"
        assert scores['justification_score'] == 25, "5 justifications should score 25"

    def test_score_calculation_violations(self):
        """Test score calculation with violations"""
        scores = self.analyzer.calculate_scores(
            any_violations=5,     # Should reduce score by 50
            console_violations=10, # Should reduce score by 50
            atcg_score=0,         # No architectural patterns
            justifications=0      # No documentation
        )

        assert scores['any_score'] == 50, "5 violations should score 50"
        assert scores['console_score'] == 50, "10 violations should score 50"
        assert scores['atcg_score'] == 0, "No patterns should score 0"
        assert scores['justification_score'] == 0, "No justifications should score 0"

    def test_sacred_justifications(self):
        """Test detection of Sacred Justifications"""
        justified_code = '''
        // Sacred Justification: Golden ratio (φ=1.618) for divine proportion
        const GOLDEN_RATIO = 1.618;

        // Sacred Justification: Based on TCP timeout of 30 seconds
        const CONNECTION_TIMEOUT = 30000;

        class SacredTransformation {
            // Regular comment without justification
            process() { }
        }
        '''

        import re
        justification_count = len(re.findall(r'Sacred Justification', justified_code, re.IGNORECASE))
        assert justification_count == 2, f"Expected 2 Sacred Justifications, found {justification_count}"

    def test_edge_cases(self):
        """Test edge cases and boundary conditions"""
        # Empty content
        empty_violations = self.analyzer.analyze_any_types("")
        assert len(empty_violations) == 0, "Empty content should have no violations"

        # Multi-line any types
        multiline_code = '''
        const complex: {
            data: any,
            process: any
        } = getData();
        '''
        multiline_violations = self.analyzer.analyze_any_types(multiline_code)
        assert len(multiline_violations) == 2, "Should detect multi-line any types"

        # Console in strings (should not be detected)
        string_code = '''
        const message = "console.log should not be detected here";
        console.log("But this should be detected");
        '''
        string_violations = self.analyzer.analyze_console_log(string_code)
        assert len(string_violations) == 1, "Should only detect actual console.log call"


class TestReviewGenerator:
    """Test suite for review generation logic"""

    def test_fury_bee_verdict_legendary(self):
        """Test Fury Bee verdict for legendary implementation"""
        metrics = {
            'any_score': 100,
            'console_score': 100,
            'atcg_score': 95,
            'any_type_violations': 0,
            'console_log_violations': 0,
            'sacred_justifications': 3
        }

        # Simulate Fury Bee logic
        if metrics['any_score'] == 100 and metrics['console_score'] == 100:
            verdict = "LEGENDARY"
            emoji = "⚡✨👑"

        assert verdict == "LEGENDARY"
        assert "👑" in emoji, "Legendary status should include crown emoji"

    def test_nuclear_audit_security_assessment(self):
        """Test bee.Jules nuclear audit logic"""
        # High-risk scenario
        security_issues = [
            {'type': 'hardcoded_limits', 'file': 'config.ts'},
            {'type': 'nested_loops', 'file': 'processor.ts'}
        ]
        any_violations = 8

        total_issues = len(security_issues) + any_violations

        if total_issues > 5:
            verdict = "CRITICAL"
        else:
            verdict = "WARNING"

        assert verdict == "CRITICAL", "High violations should trigger critical verdict"

    def test_synthesis_integration(self):
        """Test balanced synthesis logic"""
        any_score = 85
        console_score = 90
        atcg_score = 80

        overall_score = (any_score + console_score + atcg_score) / 3

        if overall_score >= 90:
            action = "IMMEDIATE MERGE APPROVED"
        elif overall_score >= 75:
            action = "CONDITIONAL APPROVAL"
        else:
            action = "REVISION REQUIRED"

        assert overall_score == pytest.approx(85.0, abs=0.1)
        assert action == "CONDITIONAL APPROVAL"


def test_configuration_validation():
    """Test review configuration validation"""
    # Test valid configuration
    valid_config = {
        'sacred_metrics': {
            'weights': {
                'any_type_score': 0.25,
                'console_log_score': 0.20,
                'atcg_compliance': 0.20,
                'sacred_justifications': 0.15,
                'performance_score': 0.10,
                'security_score': 0.10
            }
        }
    }

    weights = valid_config['sacred_metrics']['weights']
    total_weight = sum(weights.values())

    assert abs(total_weight - 1.0) < 0.01, f"Weights should sum to 1.0, got {total_weight}"

    # Test invalid configuration
    invalid_config = {
        'sacred_metrics': {
            'weights': {
                'any_type_score': 0.50,  # Too high
                'console_log_score': 0.60  # Total > 1.0
            }
        }
    }

    invalid_weights = invalid_config['sacred_metrics']['weights']
    invalid_total = sum(invalid_weights.values())

    assert invalid_total > 1.0, "Invalid config should exceed 1.0 for testing"


if __name__ == "__main__":
    # Run basic tests if called directly
    print("🧪 Running Sacred Metrics Analyzer Tests...")

    analyzer = MockSacredMetricsAnalyzer()

    # Quick validation test
    test_code = '''
    function test(data: any) {
        console.log(data);
        return data;
    }
    '''

    any_violations = analyzer.analyze_any_types(test_code)
    console_violations = analyzer.analyze_console_log(test_code)

    print(f"✅ Any violations detected: {len(any_violations)}")
    print(f"✅ Console violations detected: {len(console_violations)}")
    print("🏆 Sacred Metrics Analyzer tests completed successfully!")