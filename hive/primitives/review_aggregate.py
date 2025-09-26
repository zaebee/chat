"""
🐝⚡ ReviewAggregate (A Primitive) ⚡🐝

Aggregate primitive for AGRO review state management.
Handles structural organization and state persistence for review data.

Sacred Principle: "Aggregates maintain consistency boundaries and encapsulate state"
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
import uuid
from collections import deque


class AgroSeverity(str, Enum):
    """AGRO review severity levels"""

    DIVINE = "divine"  # 90-100 points
    BLESSED = "blessed"  # 80-89 points
    ACCEPTABLE = "acceptable"  # 60-79 points
    CONCERNING = "concerning"  # 40-59 points
    CRITICAL = "critical"  # 0-39 points


class AgroReviewType(str, Enum):
    """Types of AGRO reviews available"""

    PAIN_ANALYSIS = "pain_analysis"
    PEER_COLLABORATION = "peer_collaboration"
    AGGRESSIVE_SCRUTINY = "aggressive_scrutiny"
    SACRED_PROTOCOL_VALIDATION = "sacred_protocol_validation"
    DIVINE_BLESSING_ASSESSMENT = "divine_blessing_assessment"


@dataclass
class AgroReviewResult:
    """Result of AGRO bee-to-peer review"""

    review_id: str
    review_type: AgroReviewType
    agro_score: int
    pain_score: int
    severity: str
    violations: list[dict[str, Any]]
    recommendations: list[str]
    divine_blessing: bool
    peer_reviewers: list[str]
    timestamp: str
    sacred_insights: list[str]

    @classmethod
    def create(
        cls,
        review_type: AgroReviewType,
        agro_score: int,
        pain_score: int,
        severity: str,
        violations: list[dict[str, Any]],
        recommendations: list[str],
        divine_blessing: bool,
        peer_reviewers: list[str],
        sacred_insights: list[str],
    ) -> "AgroReviewResult":
        """Create a new review result with generated ID and timestamp"""
        return cls(
            review_id=f"agro_{uuid.uuid4().hex[:8]}",
            review_type=review_type,
            agro_score=agro_score,
            pain_score=pain_score,
            severity=severity,
            violations=violations,
            recommendations=recommendations,
            divine_blessing=divine_blessing,
            peer_reviewers=peer_reviewers,
            timestamp=datetime.now(timezone.utc).isoformat(),
            sacred_insights=sacred_insights,
        )


@dataclass
class BeeToPeerSession:
    """Bee-to-peer collaborative review session"""

    session_id: str
    participants: list[str]
    review_target: str
    session_type: str
    start_time: str
    end_time: Optional[str] = None
    collaboration_score: float = 0.0
    sacred_alignment: float = 0.0
    divine_guidance: list[str] | None = None

    @classmethod
    def create(
        cls, participants: List[str], review_target: str, session_type: str
    ) -> "BeeToPeerSession":
        """Create a new collaborative session"""
        return cls(
            session_id=f"session_{uuid.uuid4().hex[:8]}",
            participants=participants,
            review_target=review_target,
            session_type=session_type,
            start_time=datetime.now(timezone.utc).isoformat(),
            divine_guidance=[],
        )

    def end_session(
        self, collaboration_score: float = 0.0, sacred_alignment: float = 0.0
    ):
        """End the collaborative session with metrics"""
        self.end_time = datetime.now(timezone.utc).isoformat()
        self.collaboration_score = collaboration_score
        self.sacred_alignment = sacred_alignment


class ReviewAggregate:
    """
    🏗️ A (Aggregate) Primitive for AGRO Review State

    Manages the structural organization and state of AGRO reviews.
    Maintains consistency boundaries and provides controlled access to review data.
    """

    def __init__(self, max_history_size: int = 1000):
        """
        Initialize review aggregate with bounded history

        Args:
            max_history_size: Maximum number of reviews to keep in history
        """
        self.max_history_size = max_history_size

        # Bounded collections to prevent memory leaks
        self.review_history: deque = deque(maxlen=max_history_size)
        self.active_sessions: Dict[str, BeeToPeerSession] = {}

        # Current review state
        self.current_review: Optional[AgroReviewResult] = None
        self.pending_reviews: List[str] = []

        # Metrics tracking
        self.total_reviews_conducted: int = 0
        self.divine_blessings_granted: int = 0
        self.critical_issues_found: int = 0

    def add_review_result(self, result: AgroReviewResult) -> None:
        """
        Add a completed review result to the aggregate

        Args:
            result: Completed AGRO review result
        """
        # Add to bounded history
        self.review_history.append(result)

        # Update current review
        self.current_review = result

        # Update metrics
        self.total_reviews_conducted += 1

        if result.divine_blessing:
            self.divine_blessings_granted += 1

        critical_violations = [
            v for v in result.violations if v.get("severity") == "critical"
        ]
        self.critical_issues_found += len(critical_violations)

    def start_collaborative_session(
        self, participants: List[str], review_target: str, session_type: str
    ) -> BeeToPeerSession:
        """
        Start a new collaborative review session

        Args:
            participants: List of participant identifiers
            review_target: Target code/component being reviewed
            session_type: Type of collaborative session

        Returns:
            BeeToPeerSession: Created session object
        """
        session = BeeToPeerSession.create(participants, review_target, session_type)
        self.active_sessions[session.session_id] = session
        return session

    def end_collaborative_session(
        self,
        session_id: str,
        collaboration_score: float = 0.0,
        sacred_alignment: float = 0.0,
    ) -> Optional[BeeToPeerSession]:
        """
        End a collaborative review session

        Args:
            session_id: ID of session to end
            collaboration_score: Final collaboration effectiveness score
            sacred_alignment: Sacred principle alignment score

        Returns:
            BeeToPeerSession: Ended session or None if not found
        """
        session = self.active_sessions.get(session_id)
        if session:
            session.end_session(collaboration_score, sacred_alignment)
            # Move to history and remove from active
            del self.active_sessions[session_id]
            return session
        return None

    def get_review_history(self, limit: Optional[int] = None) -> List[AgroReviewResult]:
        """
        Get review history with optional limit

        Args:
            limit: Maximum number of reviews to return

        Returns:
            List[AgroReviewResult]: Recent review results
        """
        history = list(self.review_history)
        if limit:
            return history[-limit:]
        return history

    def get_active_sessions(self) -> List[BeeToPeerSession]:
        """Get all currently active collaborative sessions"""
        return list(self.active_sessions.values())

    def get_session_by_id(self, session_id: str) -> Optional[BeeToPeerSession]:
        """Get specific session by ID"""
        return self.active_sessions.get(session_id)

    def get_reviews_by_type(
        self, review_type: AgroReviewType
    ) -> List[AgroReviewResult]:
        """Get all reviews of a specific type"""
        return [
            review
            for review in self.review_history
            if review.review_type == review_type
        ]

    def get_reviews_by_severity(self, severity: str) -> List[AgroReviewResult]:
        """Get all reviews with specific severity level"""
        return [review for review in self.review_history if review.severity == severity]

    def get_aggregate_metrics(self) -> Dict[str, Any]:
        """
        Get aggregate metrics for the review system

        Returns:
            Dict containing various metrics about review activity
        """
        if not self.review_history:
            return {
                "total_reviews": 0,
                "divine_blessings": 0,
                "critical_issues": 0,
                "average_agro_score": 0,
                "average_pain_score": 0,
                "blessing_rate": 0.0,
                "active_sessions": len(self.active_sessions),
            }

        # Calculate averages
        agro_scores = [r.agro_score for r in self.review_history]
        pain_scores = [r.pain_score for r in self.review_history]

        avg_agro = sum(agro_scores) / len(agro_scores) if agro_scores else 0
        avg_pain = sum(pain_scores) / len(pain_scores) if pain_scores else 0

        blessing_rate = (
            self.divine_blessings_granted / self.total_reviews_conducted
            if self.total_reviews_conducted > 0
            else 0.0
        )

        return {
            "total_reviews": self.total_reviews_conducted,
            "divine_blessings": self.divine_blessings_granted,
            "critical_issues": self.critical_issues_found,
            "average_agro_score": round(avg_agro, 2),
            "average_pain_score": round(avg_pain, 2),
            "blessing_rate": round(blessing_rate, 3),
            "active_sessions": len(self.active_sessions),
            "history_size": len(self.review_history),
            "max_history_size": self.max_history_size,
        }

    def clear_history(self) -> int:
        """
        Clear review history (for maintenance/testing)

        Returns:
            int: Number of reviews cleared
        """
        cleared_count = len(self.review_history)
        self.review_history.clear()
        self.current_review = None

        # Reset counters
        self.total_reviews_conducted = 0
        self.divine_blessings_granted = 0
        self.critical_issues_found = 0

        return cleared_count

    def get_status(self) -> Dict[str, Any]:
        """Get current status of the review aggregate"""
        return {
            "current_review_id": self.current_review.review_id
            if self.current_review
            else None,
            "active_sessions_count": len(self.active_sessions),
            "history_size": len(self.review_history),
            "pending_reviews": len(self.pending_reviews),
            "metrics": self.get_aggregate_metrics(),
        }
