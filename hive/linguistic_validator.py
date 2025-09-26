"""
Linguistic Validator for Pollen Protocol Events

This module provides comprehensive linguistic analysis for validating
past-tense event types in the Pollen Protocol, replacing basic suffix
checking with proper grammar analysis.

Following the Hive Constitution requirement that all events use
clear past-tense verbs to describe completed actions.
"""

import re
from typing import List
from dataclasses import dataclass

from .config.golden_thresholds import CONFIDENCE, LINGUISTIC
from .config.fibonacci_sequences import MAX_SUGGESTIONS


@dataclass
class ValidationResult:
    """Result of linguistic validation."""

    is_valid: bool
    confidence: float  # 0.0 to 1.0
    detected_tense: str
    suggestions: List[str]
    reason: str


class LinguisticValidator:
    """
    Advanced linguistic validator for past-tense event types.

    Provides more sophisticated validation than simple suffix checking,
    including irregular verbs, compound forms, and grammar analysis.
    """

    def __init__(self):
        """Initialize with comprehensive linguistic rules."""
        self._load_irregular_verbs()
        self._load_past_tense_patterns()
        self._load_common_event_types()

    def _load_irregular_verbs(self):
        """Load dictionary of irregular past-tense verbs."""
        self.irregular_past_tense = {
            # Common irregular verbs used in events
            "begin": "began",
            "break": "broke",
            "bring": "brought",
            "build": "built",
            "catch": "caught",
            "choose": "chose",
            "come": "came",
            "cut": "cut",
            "do": "did",
            "draw": "drew",
            "drink": "drank",
            "drive": "drove",
            "eat": "ate",
            "fall": "fell",
            "feel": "felt",
            "find": "found",
            "fly": "flew",
            "forget": "forgot",
            "get": "got",
            "give": "gave",
            "go": "went",
            "grow": "grew",
            "have": "had",
            "hear": "heard",
            "keep": "kept",
            "know": "knew",
            "leave": "left",
            "lose": "lost",
            "make": "made",
            "mean": "meant",
            "meet": "met",
            "put": "put",
            "read": "read",
            "run": "ran",
            "say": "said",
            "see": "saw",
            "sell": "sold",
            "send": "sent",
            "set": "set",
            "show": "showed",
            "shut": "shut",
            "sing": "sang",
            "sit": "sat",
            "sleep": "slept",
            "speak": "spoke",
            "spend": "spent",
            "stand": "stood",
            "take": "took",
            "teach": "taught",
            "tell": "told",
            "think": "thought",
            "understand": "understood",
            "wake": "woke",
            "wear": "wore",
            "win": "won",
            "write": "wrote",
        }

        # Create reverse mapping for validation
        self.past_tense_forms = set(self.irregular_past_tense.values())

        # Common past participles that might be used in passive voice events
        self.past_participles = {
            "broken",
            "built",
            "caught",
            "chosen",
            "cut",
            "done",
            "drawn",
            "eaten",
            "fallen",
            "felt",
            "found",
            "forgotten",
            "given",
            "gone",
            "grown",
            "heard",
            "kept",
            "known",
            "left",
            "lost",
            "made",
            "meant",
            "put",
            "read",
            "run",
            "said",
            "seen",
            "sent",
            "shown",
            "shut",
            "sung",
            "slept",
            "spoken",
            "spent",
            "stood",
            "taken",
            "taught",
            "told",
            "thought",
            "understood",
            "woken",
            "worn",
            "won",
            "written",
        }

    def _load_past_tense_patterns(self):
        """Load regex patterns for detecting past-tense forms."""
        self.past_tense_patterns = [
            # Regular past tense endings
            (r"\w+ed$", "regular_past"),
            (r"\w+ied$", "regular_past_y_to_i"),  # tried, copied
            (r"\w+ued$", "regular_past_ue"),  # continued, argued
            (r"\w+pped$", "regular_past_double"),  # stopped, mapped
            (r"\w+tted$", "regular_past_double"),  # committed, submitted
            (r"\w+nned$", "regular_past_double"),  # planned, scanned
            # Past participle forms (often used in passive events)
            (r"\w+en$", "past_participle"),  # taken, given, written
            (r"\w+n$", "past_participle_short"),  # run, won
            # Special cases
            (r"\w+ought$", "irregular_ought"),  # brought, thought, caught
            (r"\w+aught$", "irregular_aught"),  # taught, caught
        ]

        # Compile patterns for efficiency
        self.compiled_patterns = [
            (re.compile(pattern), pattern_type)
            for pattern, pattern_type in self.past_tense_patterns
        ]

    def _load_common_event_types(self):
        """Load common valid past-tense event types."""
        self.common_event_types = {
            # User actions
            "user_registered",
            "user_logged_in",
            "user_logged_out",
            "user_updated",
            "user_deleted",
            "user_activated",
            "user_deactivated",
            # Data events
            "data_created",
            "data_updated",
            "data_deleted",
            "data_synchronized",
            "data_exported",
            "data_imported",
            "data_backed_up",
            "data_restored",
            # System events
            "system_started",
            "system_stopped",
            "system_restarted",
            "system_configured",
            "error_occurred",
            "warning_issued",
            "alert_triggered",
            "notification_sent",
            # Process events
            "task_completed",
            "task_failed",
            "task_started",
            "task_cancelled",
            "job_queued",
            "job_executed",
            "job_finished",
            "job_retried",
            # Communication events
            "message_sent",
            "message_received",
            "message_delivered",
            "message_read",
            "email_sent",
            "notification_pushed",
            "alert_broadcasted",
            # File operations
            "file_uploaded",
            "file_downloaded",
            "file_deleted",
            "file_moved",
            "file_copied",
            "file_renamed",
            "file_compressed",
            "file_extracted",
            # API events
            "request_received",
            "response_sent",
            "api_called",
            "webhook_triggered",
            "endpoint_accessed",
            "rate_limit_exceeded",
            "authentication_failed",
            # Business events
            "order_placed",
            "order_shipped",
            "order_delivered",
            "order_cancelled",
            "payment_processed",
            "payment_failed",
            "payment_refunded",
            "invoice_generated",
            "invoice_paid",
            "subscription_created",
            # AI/Hive specific events
            "agent_spawned",
            "agent_terminated",
            "model_trained",
            "prediction_made",
            "analysis_completed",
            "report_generated",
            "decision_reached",
            "collaboration_initiated",
            "teammate_joined",
            "teammate_left",
        }

    def validate_past_tense(self, event_type: str) -> ValidationResult:
        """
        Comprehensive validation of event type for past-tense compliance.

        Args:
            event_type: The event type string to validate

        Returns:
            ValidationResult with validation details and suggestions
        """
        if not event_type or not isinstance(event_type, str):
            return ValidationResult(
                is_valid=False,
                confidence=1.0,
                detected_tense="invalid",
                suggestions=[],
                reason="Event type must be a non-empty string",
            )

        # Normalize for analysis
        normalized = event_type.lower().strip()

        # Check if it's a known valid event type
        if normalized in self.common_event_types:
            return ValidationResult(
                is_valid=True,
                confidence=1.0,
                detected_tense="past",
                suggestions=[],
                reason="Recognized valid past-tense event type",
            )

        # Extract the main verb from compound event types
        main_verb = self._extract_main_verb(normalized)

        # Check irregular past tense forms
        if main_verb in self.past_tense_forms:
            return ValidationResult(
                is_valid=True,
                confidence=CONFIDENCE.high,  # φ⁻¹ ≈ 0.618
                detected_tense="past_irregular",
                suggestions=[],
                reason=f"Irregular past tense form: {main_verb}",
            )

        # Check past participles (common in passive voice events)
        if main_verb in self.past_participles:
            return ValidationResult(
                is_valid=True,
                confidence=CONFIDENCE.medium
                + 0.5 * (CONFIDENCE.high - CONFIDENCE.medium),  # Sacred interpolation
                detected_tense="past_participle",
                suggestions=[],
                reason=f"Past participle form: {main_verb}",
            )

        # Check against regex patterns
        for pattern, pattern_type in self.compiled_patterns:
            if pattern.match(normalized):
                confidence = self._calculate_pattern_confidence(
                    pattern_type, normalized
                )
                return ValidationResult(
                    is_valid=True,
                    confidence=confidence,
                    detected_tense=pattern_type,
                    suggestions=[],
                    reason=f"Matches {pattern_type} pattern",
                )

        # If no past-tense pattern found, try to suggest corrections
        suggestions = self._generate_suggestions(normalized)

        return ValidationResult(
            is_valid=False,
            confidence=0.0,
            detected_tense="present_or_other",
            suggestions=suggestions,
            reason="Does not match any recognized past-tense pattern",
        )

    def _extract_main_verb(self, event_type: str) -> str:
        """Extract the main verb from compound event types."""
        # Handle common patterns like "user_registered", "data_created"
        parts = event_type.split("_")
        if len(parts) >= 2:
            # Usually the verb is the last part
            return parts[-1]
        return event_type

    def _calculate_pattern_confidence(self, pattern_type: str, word: str) -> float:
        """Calculate confidence score based on pattern type and word characteristics."""
        base_confidence = {
            "regular_past": CONFIDENCE.medium
            + 0.5 * (CONFIDENCE.high - CONFIDENCE.medium),  # Sacred interpolation
            "regular_past_y_to_i": CONFIDENCE.high,  # φ⁻¹
            "regular_past_ue": CONFIDENCE.high,  # φ⁻¹
            "regular_past_double": CONFIDENCE.medium
            + 0.5 * (CONFIDENCE.high - CONFIDENCE.medium),
            "past_participle": (CONFIDENCE.high + CONFIDENCE.medium) / 2,  # Golden mean
            "past_participle_short": CONFIDENCE.medium
            + 0.3 * (CONFIDENCE.high - CONFIDENCE.medium),
            "irregular_ought": CONFIDENCE.high,  # φ⁻¹
            "irregular_aught": CONFIDENCE.high,  # φ⁻¹
        }.get(pattern_type, CONFIDENCE.acceptable)  # Sacred threshold

        # Adjust confidence based on word length and characteristics
        if len(word) < LINGUISTIC.minimum_length:
            base_confidence *= LINGUISTIC.short_word_penalty  # φ² - φ ≈ 0.618
        elif len(word) > LINGUISTIC.maximum_length // 3:  # Fibonacci-based threshold
            base_confidence *= LINGUISTIC.long_word_penalty  # φ⁻¹ ≈ 0.618

        return min(base_confidence, 1.0)

    def _generate_suggestions(self, event_type: str) -> List[str]:
        """Generate past-tense suggestions for non-compliant event types."""
        suggestions = []

        # Simple transformations for common cases
        if event_type.endswith("e"):
            suggestions.append(event_type + "d")  # create -> created
        elif event_type.endswith("y") and len(event_type) > 2:
            suggestions.append(event_type[:-1] + "ied")  # copy -> copied
        elif event_type.endswith(("p", "t", "n")) and len(event_type) > 2:
            # Double consonant cases
            suggestions.append(event_type + event_type[-1] + "ed")  # stop -> stopped
        else:
            suggestions.append(event_type + "ed")  # process -> processed

        # Check for irregular verb base forms
        if event_type in self.irregular_past_tense:
            suggestions.append(self.irregular_past_tense[event_type])

        # Add compound suggestions for common prefixes
        prefixes = ["user_", "data_", "system_", "task_", "message_", "file_"]
        for prefix in prefixes:
            if not event_type.startswith(prefix):
                suggestions.append(prefix + event_type + "ed")

        return suggestions[:MAX_SUGGESTIONS]  # Limit to Fibonacci 5 suggestions

    def validate_event_name_style(self, event_type: str) -> ValidationResult:
        """
        Validate event naming style conventions beyond just past-tense.

        Checks for:
        - Snake_case formatting
        - Descriptive naming
        - Appropriate length
        - No reserved words
        """
        if not event_type:
            return ValidationResult(
                is_valid=False,
                confidence=1.0,
                detected_tense="invalid",
                suggestions=[],
                reason="Event type cannot be empty",
            )

        issues = []
        suggestions = []

        # Check snake_case convention
        if not re.match(r"^[a-z][a-z0-9_]*[a-z0-9]$", event_type):
            issues.append("Should use snake_case (lowercase with underscores)")
            suggestions.append(
                re.sub(
                    r"[A-Z]", lambda m: "_" + str(m.group()).lower(), event_type
                ).strip("_")
            )

        # Check length (sacred bounds)
        if len(event_type) < LINGUISTIC.minimum_length:
            issues.append(
                f"Event type too short (minimum {LINGUISTIC.minimum_length} characters)"
            )
        elif len(event_type) > LINGUISTIC.maximum_length:
            issues.append(
                f"Event type too long (maximum {LINGUISTIC.maximum_length} characters)"
            )

        # Check for descriptive content
        if len(event_type.replace("_", "")) < 5:
            issues.append("Event type should be more descriptive")

        # Check for reserved words or patterns
        reserved_patterns = ["test", "temp", "debug", "tmp"]
        if any(pattern in event_type.lower() for pattern in reserved_patterns):
            issues.append("Avoid using temporary/debug terms in production events")

        is_valid = len(issues) == 0
        confidence = (
            CONFIDENCE.perfect
            if is_valid
            else max(
                CONFIDENCE.medium, CONFIDENCE.perfect - len(issues) * CONFIDENCE.low
            )
        )  # Sacred penalty calculation

        return ValidationResult(
            is_valid=is_valid,
            confidence=confidence,
            detected_tense="style_check",
            suggestions=suggestions,
            reason="; ".join(issues) if issues else "Event naming style is compliant",
        )
