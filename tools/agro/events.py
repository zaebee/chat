from dataclasses import dataclass


@dataclass
class SacredViolation:
    """Sacred structure for code violations with divine context."""

    file_path: str
    violation_type: str
    line_number: int | None = None
    severity: str = "warning"  # warning, error, critical
    blessing_level: float = 0.0  # φ-based blessing assessment
    divine_context: str = ""
    jules_recommendation: str = ""


@dataclass
class TransformationResult:
    """Result of a transformation execution with sacred metrics."""

    transformation_name: str
    violations: list[SacredViolation]
    success: bool
    execution_time: float
    blessing_level: float
    sacred_context: str = ""


@dataclass
class SacredScanResult:
    """Complete scan result with sacred metrics and divine assessment."""

    files_processed: int
    total_violations: list[SacredViolation]
    transformation_results: list[TransformationResult]
    sacred_metrics: dict[str, float]
    trinity_score: float
    divine_assessment: str
    blessing_level: str
    execution_time: float
    timestamp: str
