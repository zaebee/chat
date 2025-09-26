import re
import ast
from abc import ABC, abstractmethod
from typing import List

# Sacred imports for Hive integration
try:
    from hive.config.golden_thresholds import CONFIDENCE
    from hive.config.sacred_constants import (
        PHI,
        PHI_RECIPROCAL,
        PHI_INVERSE_SQUARED,
        PHI_INVERSE_CUBED,
        PHI_INVERSE_FOURTH,
    )
    from hive.config.fibonacci_sequences import FIBONACCI_89, FIBONACCI_13

    HIVE_INTEGRATION = True
except ImportError:
    HIVE_INTEGRATION = False

    # Fallback constants if Hive not available
    class MockConfidence:
        low = 0.236
        medium = 0.382
        high = 0.618
        minimal = 0.146

    CONFIDENCE = MockConfidence()
    # Sacred constants fallback
    PHI = 1.618033988749
    PHI_RECIPROCAL = 0.618033988749
    PHI_INVERSE_SQUARED = 0.381966011251
    PHI_INVERSE_CUBED = 0.236067977499
    PHI_INVERSE_FOURTH = 0.145898033750
    FIBONACCI_89 = 89
    FIBONACCI_13 = 13

from .events import SacredViolation


class AgroCheckTransformation(ABC):
    """
    Base class for all AGRO check transformations.
    Each transformation performs a specific code quality check.
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def execute(self, file_path: str) -> List[SacredViolation]:
        """
        Execute the transformation (code quality check) on the given file.
        Returns a list of SacredViolation objects.
        """
        pass


class ConsoleLogCheck(AgroCheckTransformation):
    """Sacred console.log detection with divine blessing assessment."""

    def __init__(self):
        super().__init__("Console.log Protection")

    async def execute(self, file_path: str) -> List[SacredViolation]:
        violations = []

        if not file_path.endswith((".js", ".ts", ".vue")):
            return violations

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for line_num, line in enumerate(lines, 1):
                if re.search(r"console\.log", line):
                    blessing_level = (
                        CONFIDENCE.low if HIVE_INTEGRATION else PHI_INVERSE_CUBED
                    )  # φ⁻³ blessing penalty

                    violation = SacredViolation(
                        file_path=file_path,
                        violation_type="console_log_violation",
                        line_number=line_num,
                        severity="error",
                        blessing_level=blessing_level,
                        divine_context="Console.log statements break sacred code silence and observability",
                        jules_recommendation="Replace with proper logging framework or remove debug code",
                    )
                    violations.append(violation)

            return violations

        except Exception as e:
            # Log this error, but don't fail the check
            print(f"  [Sacred-AGRO] ⚠️ WARNING: Could not read file {file_path}: {e}")
            return []


class FunctionLengthCheck(AgroCheckTransformation):
    """Sacred function length validation with Fibonacci limits."""

    def __init__(self, max_lines: int = None):
        super().__init__("Function Length Validation")
        self.max_lines = max_lines or (FIBONACCI_89 if HIVE_INTEGRATION else 55)

    async def execute(self, file_path: str) -> List[SacredViolation]:
        violations = []

        if not file_path.endswith((".py", ".pyx", ".pyi")):
            return violations

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=file_path)

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    function_length = len(node.body)

                    if function_length > self.max_lines:
                        # Calculate φ-based blessing penalty
                        excess_ratio = function_length / self.max_lines
                        blessing_penalty = (
                            min(CONFIDENCE.high, excess_ratio * CONFIDENCE.medium)
                            if HIVE_INTEGRATION
                            else min(PHI_RECIPROCAL, excess_ratio * PHI_INVERSE_SQUARED)
                        )

                        # Sacred severity threshold
                        severe_threshold = self.max_lines * (
                            PHI / 2
                        )  # φ/2 ≈ 0.809 factor
                        violation = SacredViolation(
                            file_path=file_path,
                            violation_type="function_too_long",
                            line_number=node.lineno,
                            severity="warning"
                            if function_length < severe_threshold
                            else "error",
                            blessing_level=1.0 - blessing_penalty,  # Reduced blessing
                            divine_context=f"Functions should follow sacred Fibonacci limit ({self.max_lines} lines) for divine readability",
                            jules_recommendation="Consider breaking into smaller, focused functions following Single Responsibility Principle",
                        )
                        violations.append(violation)

            return violations

        except Exception as e:
            print(
                f"  [Sacred-AGRO] ⚠️ WARNING: Could not parse Python file {file_path}: {e}"
            )
            return []


class AnyTypeCheck(AgroCheckTransformation):
    """Sacred TypeScript type safety validation with divine blessing."""

    def __init__(self):
        super().__init__("TypeScript Any Type Detection")

    async def execute(self, file_path: str) -> List[SacredViolation]:
        violations = []

        if not file_path.endswith((".ts", ".tsx")):
            return violations

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for line_num, line in enumerate(lines, 1):
                if re.search(r":\s*any", line):
                    blessing_level = (
                        CONFIDENCE.minimal if HIVE_INTEGRATION else PHI_INVERSE_FOURTH
                    )  # φ⁻⁴ severe penalty

                    violation = SacredViolation(
                        file_path=file_path,
                        violation_type="any_type_violation",
                        line_number=line_num,
                        severity="error",
                        blessing_level=blessing_level,
                        divine_context="The 'any' type breaks sacred type safety and divine code clarity",
                        jules_recommendation="Replace with specific types or union types for proper TypeScript sanctification",
                    )
                    violations.append(violation)

            return violations

        except Exception as e:
            print(f"  [Sacred-AGRO] ⚠️ WARNING: Could not read file {file_path}: {e}")
            return []


class PythonMagicNumbersCheck(AgroCheckTransformation):
    """Sacred magic number detection with φ-based assessment."""

    def __init__(self):
        super().__init__("Python Magic Numbers Detection")

    async def execute(self, file_path: str) -> List[SacredViolation]:
        violations = []

        if not file_path.endswith((".py", ".pyx", ".pyi")):
            return violations

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=file_path)

            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(
                    node.value, (int, float)
                ):
                    # Allow sacred constants: 0, 1, and φ-related values
                    sacred_values = [
                        0,
                        1,
                        2,
                        3,
                        5,
                        8,
                        13,
                        21,
                        34,
                        55,
                    ]  # Basic Fibonacci
                    φ_related = [
                        PHI,
                        PHI_RECIPROCAL,
                        PHI_INVERSE_SQUARED,
                        PHI_INVERSE_CUBED,
                        PHI_INVERSE_FOURTH,
                    ]

                    tolerance = PHI_INVERSE_CUBED / 10  # φ⁻³/10 precision
                    if node.value not in sacred_values and not any(
                        abs(node.value - φ_val) < tolerance for φ_val in φ_related
                    ):
                        blessing_level = (
                            CONFIDENCE.medium
                            if HIVE_INTEGRATION
                            else PHI_INVERSE_SQUARED
                        )

                        violation = SacredViolation(
                            file_path=file_path,
                            violation_type="magic_number_detected",
                            line_number=node.lineno,
                            severity="warning",
                            blessing_level=blessing_level,
                            divine_context=f"Magic number '{node.value}' lacks sacred meaning - consider using named constants",
                            jules_recommendation="Replace with descriptive constants, preferably aligned with Golden Ratio or Fibonacci sequences",
                        )
                        violations.append(violation)

            return violations

        except Exception as e:
            print(
                f"  [Sacred-AGRO] ⚠️ WARNING: Could not parse Python file {file_path}: {e}"
            )
            return []


class JavaScriptMagicNumbersCheck(AgroCheckTransformation):
    """Sacred JavaScript/TypeScript magic number detection."""

    def __init__(self):
        super().__init__("JavaScript Magic Numbers Detection")

    async def execute(self, file_path: str) -> List[SacredViolation]:
        violations = []

        if not file_path.endswith((".js", ".ts", ".vue", ".jsx", ".tsx")):
            return violations

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for line_num, line in enumerate(lines, 1):
                # Enhanced regex to detect magic numbers while avoiding false positives
                magic_pattern = (
                    r"[^\w\'\"\.\.\$]((?<!const |let |var |= )\d{2,})[^\w\'\"\']"
                )
                matches = re.finditer(magic_pattern, line)

                for match in matches:
                    number = match.group(1)
                    # Skip common non-magic numbers
                    if number in [
                        "10",
                        "100",
                        "1000",
                        "24",
                        "60",
                    ]:  # Common time/base conversions
                        continue

                    blessing_level = (
                        CONFIDENCE.medium if HIVE_INTEGRATION else PHI_INVERSE_SQUARED
                    )

                    violation = SacredViolation(
                        file_path=file_path,
                        violation_type="js_magic_number",
                        line_number=line_num,
                        severity="warning",
                        blessing_level=blessing_level,
                        divine_context=f"Magic number '{number}' in JavaScript/TypeScript code lacks sacred meaning",
                        jules_recommendation="Consider extracting to named constants with descriptive names",
                    )
                    violations.append(violation)

            return violations

        except Exception as e:
            print(f"  [Sacred-AGRO] ⚠️ WARNING: Could not read file {file_path}: {e}")
            return []
