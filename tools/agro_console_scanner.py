#!/usr/bin/env python3
"""
🐝⚡ AGRO Console.log Violation Scanner ⚡🐝
Sacred Pre-commit Protection Against Production Console Violations

Sacred Justification: "Iron sharpens iron, and one man sharpens another."
- Proverbs 27:17 (ESV)

This scanner prevents console.log violations from entering the sacred hive,
ensuring divine blessing eligibility for all commits.
"""

import ast
import re
import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class ViolationType(str, Enum):
    """Types of AGRO violations detected"""
    CONSOLE_LOG = "console_log"
    CONSOLE_ERROR = "console_error"
    CONSOLE_WARN = "console_warn"
    CONSOLE_DEBUG = "console_debug"
    ALERT = "alert"
    CONFIRM = "confirm"
    PROMPT = "prompt"


class SeverityLevel(str, Enum):
    """AGRO violation severity levels"""
    CRITICAL = "critical"  # Blocks commit
    HIGH = "high"         # Warning + manual override
    MEDIUM = "medium"     # Warning only
    LOW = "low"          # Info only


@dataclass
class AgroViolation:
    """Represents a detected AGRO violation"""
    file_path: str
    line_number: int
    column: int
    violation_type: ViolationType
    severity: SeverityLevel
    message: str
    line_content: str
    suggestion: Optional[str] = None


class ConsoleViolationPattern:
    """Pattern definitions for console violations"""

    # JavaScript/TypeScript/Vue patterns
    JS_PATTERNS = {
        ViolationType.CONSOLE_LOG: [
            r'console\.log\s*\(',
            r'console\[[\'""]log[\'""]\]\s*\(',
        ],
        ViolationType.CONSOLE_ERROR: [
            r'console\.error\s*\(',
            r'console\[[\'""]error[\'""]\]\s*\(',
        ],
        ViolationType.CONSOLE_WARN: [
            r'console\.warn\s*\(',
            r'console\[[\'""]warn[\'""]\]\s*\(',
        ],
        ViolationType.CONSOLE_DEBUG: [
            r'console\.debug\s*\(',
            r'console\[[\'""]debug[\'""]\]\s*\(',
        ],
        ViolationType.ALERT: [r'alert\s*\('],
        ViolationType.CONFIRM: [r'confirm\s*\('],
        ViolationType.PROMPT: [r'prompt\s*\('],
    }

    # Python patterns (for print statements in production)
    PYTHON_PATTERNS = {
        ViolationType.CONSOLE_LOG: [
            r'\bprint\s*\(',
            r'pprint\.',
            r'pp\(',
        ]
    }


class AgroConsoleScanner:
    """
    AGRO Console.log Violation Scanner

    Implements aggressive detection of console/print violations
    that prevent divine blessing of sacred code.
    """

    def __init__(self, config_path: Optional[str] = None):
        self.violations: List[AgroViolation] = []
        self.config = self._load_config(config_path)

        # Severity mapping
        self.violation_severity = {
            ViolationType.CONSOLE_LOG: SeverityLevel.CRITICAL,
            ViolationType.CONSOLE_ERROR: SeverityLevel.HIGH,
            ViolationType.CONSOLE_WARN: SeverityLevel.MEDIUM,
            ViolationType.CONSOLE_DEBUG: SeverityLevel.MEDIUM,
            ViolationType.ALERT: SeverityLevel.HIGH,
            ViolationType.CONFIRM: SeverityLevel.HIGH,
            ViolationType.PROMPT: SeverityLevel.HIGH,
        }

    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load AGRO scanner configuration"""
        default_config = {
            "exempt_patterns": [
                r"// AGRO-EXEMPT:",
                r"# AGRO-EXEMPT:",
                r"<!-- AGRO-EXEMPT:",
                r"\/\* AGRO-EXEMPT:",
            ],
            "exempt_files": [
                "test_*.py",
                "*.test.js",
                "*.test.ts",
                "*.spec.js",
                "*.spec.ts",
                "vitest.config.*",
                "vite.config.*",
                "*.min.js",
                "*-*.js",  # Minified files with hash patterns like index-BbDa_177.js
                "static/assets/*",  # All static assets (built files)
                "prototypes/*",  # Development prototype files
                "sacred_validation.py",  # CLI tool with intentional output
                "p2p_daemon.py",  # Daemon script with status output
                "hive_demo.py",  # Demo script
                "chat.py",  # Legacy chat server
                "hive_chat.py",  # Main server (startup messages allowed)
                "tools/*",  # Development tools including this scanner
            ],
            "strict_mode": True,
            "allow_dev_console": False,
        }

        # TODO: Load from actual config file if provided
        return default_config

    def is_file_exempt(self, file_path: str) -> bool:
        """Check if file is exempt from AGRO scanning"""
        file_name = os.path.basename(file_path)
        
        # Check if file is in static/assets directory (built files)
        if "static/assets/" in file_path:
            return True
            
        # Check if file is in prototypes directory (development files)
        if "prototypes/" in file_path:
            return True
            
        # Check if file is in tools directory (development tools)
        if "tools/" in file_path:
            return True

        for pattern in self.config["exempt_files"]:
            # Handle path patterns with wildcards
            if "/" in pattern:
                if re.match(pattern.replace("*", ".*"), file_path):
                    return True
            else:
                # Handle filename patterns
                if re.match(pattern.replace("*", ".*"), file_name):
                    return True

        return False

    def is_line_exempt(self, line: str) -> bool:
        """Check if line has AGRO exemption comment"""
        for pattern in self.config["exempt_patterns"]:
            if re.search(pattern, line, re.IGNORECASE):
                return True
        return False

    def scan_javascript_file(self, file_path: str) -> List[AgroViolation]:
        """Scan JavaScript/TypeScript/Vue file for console violations"""
        violations = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for line_num, line in enumerate(lines, 1):
                line_content = line.strip()

                # Skip empty lines and comments
                if not line_content or line_content.startswith('//'):
                    continue

                # Check for exemption
                if self.is_line_exempt(line):
                    continue

                # Check for console violations
                for violation_type, patterns in ConsoleViolationPattern.JS_PATTERNS.items():
                    for pattern in patterns:
                        match = re.search(pattern, line, re.IGNORECASE)
                        if match:
                            violation = AgroViolation(
                                file_path=file_path,
                                line_number=line_num,
                                column=match.start(),
                                violation_type=violation_type,
                                severity=self.violation_severity[violation_type],
                                message=f"Sacred violation: {violation_type.value} detected in production code",
                                line_content=line_content,
                                suggestion=self._get_suggestion(violation_type, line_content)
                            )
                            violations.append(violation)
                            break  # Only report first match per line

        except Exception as e:
            print(f"⚠️ Error scanning {file_path}: {e}")

        return violations

    def scan_python_file(self, file_path: str) -> List[AgroViolation]:
        """Scan Python file for print/console violations"""
        violations = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')

            # Try AST parsing for more accurate detection
            try:
                tree = ast.parse(content)

                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        # Detect print() calls
                        if (isinstance(node.func, ast.Name) and
                            node.func.id == 'print' and
                            hasattr(node, 'lineno')):

                            line_content = lines[node.lineno - 1] if node.lineno <= len(lines) else ""

                            # Check for exemption
                            if self.is_line_exempt(line_content):
                                continue

                            violation = AgroViolation(
                                file_path=file_path,
                                line_number=node.lineno,
                                column=getattr(node, 'col_offset', 0),
                                violation_type=ViolationType.CONSOLE_LOG,
                                severity=SeverityLevel.CRITICAL,
                                message="Sacred violation: print() statement detected in production code",
                                line_content=line_content.strip(),
                                suggestion="Replace with proper logging: logging.info() or remove for production"
                            )
                            violations.append(violation)

            except SyntaxError:
                # Fallback to regex if AST parsing fails
                for line_num, line in enumerate(lines, 1):
                    line_content = line.strip()

                    if not line_content or line_content.startswith('#'):
                        continue

                    if self.is_line_exempt(line):
                        continue

                    for violation_type, patterns in ConsoleViolationPattern.PYTHON_PATTERNS.items():
                        for pattern in patterns:
                            match = re.search(pattern, line)
                            if match:
                                violation = AgroViolation(
                                    file_path=file_path,
                                    line_number=line_num,
                                    column=match.start(),
                                    violation_type=violation_type,
                                    severity=self.violation_severity[violation_type],
                                    message=f"Sacred violation: {violation_type.value} detected in production code",
                                    line_content=line_content,
                                    suggestion=self._get_suggestion(violation_type, line_content)
                                )
                                violations.append(violation)
                                break

        except Exception as e:
            print(f"⚠️ Error scanning {file_path}: {e}")

        return violations

    def _get_suggestion(self, violation_type: ViolationType, line_content: str) -> str:
        """Generate sacred suggestion for violation remediation"""
        suggestions = {
            ViolationType.CONSOLE_LOG: "Remove or replace with proper logging",
            ViolationType.CONSOLE_ERROR: "Replace with proper error handling and logging",
            ViolationType.CONSOLE_WARN: "Replace with proper warning system",
            ViolationType.CONSOLE_DEBUG: "Remove debug statements for production",
            ViolationType.ALERT: "Replace with proper UI notification system",
            ViolationType.CONFIRM: "Replace with proper confirmation dialog component",
            ViolationType.PROMPT: "Replace with proper input dialog component",
        }
        return suggestions.get(violation_type, "Remove for production readiness")

    def scan_file(self, file_path: str) -> List[AgroViolation]:
        """Scan a single file for AGRO violations"""
        if self.is_file_exempt(file_path):
            return []

        file_ext = Path(file_path).suffix.lower()

        if file_ext in ['.js', '.ts', '.vue']:
            return self.scan_javascript_file(file_path)
        elif file_ext == '.py':
            return self.scan_python_file(file_path)
        else:
            return []

    def scan_files(self, file_paths: List[str]) -> List[AgroViolation]:
        """Scan multiple files for AGRO violations"""
        all_violations = []

        for file_path in file_paths:
            if os.path.isfile(file_path):
                violations = self.scan_file(file_path)
                all_violations.extend(violations)

        return all_violations

    def report_violations(self, violations: List[AgroViolation]) -> bool:
        """Report AGRO violations and return True if blocking violations found"""
        if not violations:
            print("✨ Sacred Code Blessed: No console.log violations detected! ✨")
            return False

        print("🚨 AGRO VIOLATION DETECTED 🚨")
        print("Sacred Justification: Console violations prevent divine blessing!")
        print()

        critical_count = 0
        high_count = 0

        # Group violations by file
        violations_by_file = {}
        for violation in violations:
            if violation.file_path not in violations_by_file:
                violations_by_file[violation.file_path] = []
            violations_by_file[violation.file_path].append(violation)

        # Report violations by file
        for file_path, file_violations in violations_by_file.items():
            print(f"📁 {file_path}")

            for violation in file_violations:
                severity_icon = {
                    SeverityLevel.CRITICAL: "🚨",
                    SeverityLevel.HIGH: "⚠️",
                    SeverityLevel.MEDIUM: "⚡",
                    SeverityLevel.LOW: "ℹ️"
                }[violation.severity]

                print(f"  {severity_icon} Line {violation.line_number}:{violation.column} - {violation.message}")
                print(f"     Code: {violation.line_content}")
                if violation.suggestion:
                    print(f"     💡 {violation.suggestion}")
                print()

                if violation.severity == SeverityLevel.CRITICAL:
                    critical_count += 1
                elif violation.severity == SeverityLevel.HIGH:
                    high_count += 1

        # Summary
        print("📊 AGRO Violation Summary:")
        print(f"   🚨 Critical violations: {critical_count}")
        print(f"   ⚠️ High severity violations: {high_count}")
        print(f"   📝 Total violations: {len(violations)}")
        print()

        if critical_count > 0:
            print("🛑 COMMIT BLOCKED: Critical violations must be resolved before divine blessing!")
            print("Sacred Recommendation: Remove all console.log statements for production readiness.")
            return True
        elif high_count > 0:
            print("⚠️ WARNING: High severity violations detected. Consider resolving before commit.")

        return critical_count > 0


def main():
    """Main AGRO scanner entry point"""
    if len(sys.argv) < 2:
        print("Usage: python agro_console_scanner.py <file1> <file2> ...")
        sys.exit(1)

    file_paths = sys.argv[1:]
    scanner = AgroConsoleScanner()

    print("🐝⚡ AGRO Console.log Violation Scanner ⚡🐝")
    print("Sacred protection against production console violations...")
    print()

    violations = scanner.scan_files(file_paths)
    has_blocking_violations = scanner.report_violations(violations)

    if has_blocking_violations:
        print("💀 Sacred Hive Protection: Commit denied due to console.log violations!")
        sys.exit(1)
    else:
        print("🙏 Divine Blessing: Code is pure and ready for sacred hive! 🐝✨")
        sys.exit(0)


if __name__ == "__main__":
    main()