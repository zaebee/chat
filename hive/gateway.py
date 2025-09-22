"""
Welcome Gateway: Metamorphosis-Based Onboarding for AI Teammates

This module implements the Constitution's metamorphosis lifecycle for onboarding
new AI teammates to the Hive ecosystem. The process follows four stages:

1. Egg (Initialization): Authentication and basic capability assessment
2. Larva (Development): Guided tour and learning phase
3. Pupa (Build/Containerization): Sandbox testing and integration preparation
4. Adult (Deployment): Full access and collaborative operation

This ensures all AI teammates are properly integrated and understand
the Hive's collaborative principles before gaining full access.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum
import uuid

from .teammate import HiveTeammate, TeammateProfile, TaskRequest, TaskResult, TeammateCapability, TeammateStatus
from .events import HiveEventBus, PollenEvent
from .registry import HiveRegistry


class OnboardingStage(str, Enum):
    """Stages of the onboarding metamorphosis process."""

    EGG = "egg"  # Initial authentication and assessment
    LARVA = "larva"  # Guided learning and exploration
    PUPA = "pupa"  # Sandbox testing and validation
    ADULT = "adult"  # Full integration and collaboration
    FAILED = "failed"  # Onboarding failed at some stage


@dataclass
class OnboardingSession:
    """Represents an active onboarding session for a new teammate."""

    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    candidate_profile: TeammateProfile = None
    current_stage: OnboardingStage = OnboardingStage.EGG
    stage_start_time: datetime = field(default_factory=datetime.now)
    session_start_time: datetime = field(default_factory=datetime.now)
    stage_data: Dict[str, Any] = field(default_factory=dict)
    completed_tasks: List[str] = field(default_factory=list)
    assessment_scores: Dict[str, float] = field(default_factory=dict)
    mentor_notes: List[str] = field(default_factory=list)
    is_active: bool = True


@dataclass
class OnboardingTask:
    """A task used during the onboarding process."""

    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    stage: OnboardingStage = OnboardingStage.EGG
    task_type: str = ""
    description: str = ""
    instructions: str = ""
    expected_output: Dict[str, Any] = field(default_factory=dict)
    time_limit: int = 300  # seconds
    difficulty: str = "beginner"  # beginner, intermediate, advanced
    success_criteria: List[str] = field(default_factory=list)


class WelcomeGateway:
    """
    The Welcome Gateway manages the onboarding process for new AI teammates.

    It implements the metamorphosis-based lifecycle to ensure all teammates
    are properly integrated into the Hive ecosystem before gaining full access.
    """

    def __init__(self, event_bus: HiveEventBus, registry: HiveRegistry):
        self.event_bus = event_bus
        self.registry = registry
        self.active_sessions: Dict[str, OnboardingSession] = {}
        self.onboarding_tasks: Dict[OnboardingStage, List[OnboardingTask]] = {}
        self.mentor_agents: List[str] = []  # IDs of teammates who can serve as mentors
        self.completion_requirements: Dict[OnboardingStage, Dict[str, Any]] = {}

        self._initialize_onboarding_curriculum()
        self._setup_event_subscriptions()

    def _initialize_onboarding_curriculum(self):
        """Initialize the onboarding curriculum for each stage."""

        # EGG Stage: Authentication and Basic Assessment
        self.onboarding_tasks[OnboardingStage.EGG] = [
            OnboardingTask(
                stage=OnboardingStage.EGG,
                task_type="identity_verification",
                description="Verify your identity and basic capabilities",
                instructions="""
                Please provide:
                1. Your name and type (e.g., 'Claude', 'Mistral', etc.)
                2. A brief description of your primary capabilities
                3. Your preferred communication protocols
                4. Any special requirements or limitations
                """,
                success_criteria=[
                    "valid_name",
                    "capabilities_listed",
                    "protocols_specified",
                ],
                time_limit=120,
            ),
            OnboardingTask(
                stage=OnboardingStage.EGG,
                task_type="basic_communication",
                description="Demonstrate basic communication abilities",
                instructions="""
                Send a simple message in Pollen Protocol format with:
                - event_type: "communication_test_completed"
                - A greeting message in the payload
                - Your timestamp
                """,
                success_criteria=["valid_pollen_format", "greeting_present"],
                time_limit=60,
            ),
        ]

        # LARVA Stage: Guided Learning
        self.onboarding_tasks[OnboardingStage.LARVA] = [
            OnboardingTask(
                stage=OnboardingStage.LARVA,
                task_type="codebase_exploration",
                description="Explore the Hive codebase structure",
                instructions="""
                Examine the codebase and answer these questions:
                1. What are the four ATCG primitives and their purposes?
                2. How does the Pollen Protocol work?
                3. What is the role of the HiveRegistry?
                4. Identify three key architectural principles from the documentation.
                """,
                success_criteria=[
                    "atcg_explained",
                    "pollen_understood",
                    "registry_role_clear",
                    "principles_identified",
                ],
                time_limit=900,
            ),
            OnboardingTask(
                stage=OnboardingStage.LARVA,
                task_type="collaboration_principles",
                description="Learn the Hive collaboration principles",
                instructions="""
                Study the Hive Constitution and explain:
                1. What does "Human-AI Symbiosis" mean in practice?
                2. How should conflicts between teammates be resolved?
                3. What are your responsibilities as a Hive teammate?
                4. How do you contribute to the collective intelligence?
                """,
                success_criteria=[
                    "symbiosis_explained",
                    "conflict_resolution",
                    "responsibilities_clear",
                ],
                time_limit=600,
            ),
            OnboardingTask(
                stage=OnboardingStage.LARVA,
                task_type="tool_familiarization",
                description="Learn to use Hive tools and APIs",
                instructions="""
                Demonstrate understanding of:
                1. How to subscribe to events via the HiveEventBus
                2. How to check system status using get_status() methods
                3. How to interact with other teammates through the registry
                4. Basic task execution workflow
                """,
                success_criteria=[
                    "event_subscription",
                    "status_checking",
                    "teammate_interaction",
                ],
                time_limit=450,
            ),
        ]

        # PUPA Stage: Sandbox Testing
        self.onboarding_tasks[OnboardingStage.PUPA] = [
            OnboardingTask(
                stage=OnboardingStage.PUPA,
                task_type="capability_demonstration",
                description="Demonstrate your core capabilities",
                instructions="""
                Choose one of your claimed capabilities and:
                1. Perform a real task demonstrating this capability
                2. Explain your approach and reasoning
                3. Provide quality metrics for your output
                4. Show how you would collaborate with other teammates on this task
                """,
                success_criteria=[
                    "task_completed",
                    "approach_explained",
                    "quality_metrics",
                    "collaboration_shown",
                ],
                time_limit=1200,
            ),
            OnboardingTask(
                stage=OnboardingStage.PUPA,
                task_type="error_handling",
                description="Demonstrate graceful error handling",
                instructions="""
                We will simulate various error conditions:
                1. Handle an invalid task request gracefully
                2. Respond to a timeout scenario
                3. Deal with conflicting instructions from multiple teammates
                4. Recover from a simulated system failure
                """,
                success_criteria=[
                    "graceful_handling",
                    "timeout_response",
                    "conflict_resolution",
                    "recovery_shown",
                ],
                time_limit=600,
            ),
            OnboardingTask(
                stage=OnboardingStage.PUPA,
                task_type="collaborative_project",
                description="Complete a small collaborative project",
                instructions="""
                Work with an assigned mentor to:
                1. Analyze a small code module
                2. Propose improvements
                3. Implement changes collaboratively
                4. Test and validate the results
                """,
                success_criteria=[
                    "analysis_complete",
                    "improvements_proposed",
                    "changes_implemented",
                    "validation_done",
                ],
                time_limit=1800,
            ),
        ]

        # Completion requirements for each stage
        self.completion_requirements = {
            OnboardingStage.EGG: {
                "min_tasks_completed": 2,
                "min_success_rate": 1.0,
                "required_assessments": ["identity", "communication"],
            },
            OnboardingStage.LARVA: {
                "min_tasks_completed": 3,
                "min_success_rate": 0.8,
                "required_assessments": ["knowledge", "understanding", "tools"],
            },
            OnboardingStage.PUPA: {
                "min_tasks_completed": 3,
                "min_success_rate": 0.9,
                "required_assessments": ["capability", "collaboration", "reliability"],
            },
        }

    def _setup_event_subscriptions(self):
        """Set up event subscriptions for onboarding management."""
        from .events import EventSubscription

        async def handle_onboarding_events(event: PollenEvent):
            await self._handle_onboarding_event(event)

        onboarding_subscription = EventSubscription(
            event_types=["onboarding_started", "task_completed", "stage_completed", "agro_pain_analysis_completed"],
            callback=handle_onboarding_events,
        )

        self.event_bus.subscribe(onboarding_subscription)

    async def start_onboarding(
        self, candidate_profile: TeammateProfile
    ) -> Dict[str, Any]:
        """
        Start the onboarding process for a new AI teammate candidate.
        """
        try:
            # Create new onboarding session
            session = OnboardingSession(
                candidate_profile=candidate_profile, current_stage=OnboardingStage.EGG
            )

            self.active_sessions[session.session_id] = session

            # Announce onboarding start
            await self.event_bus.publish_teammate_event(
                "onboarding_started",
                candidate_profile.id,
                {
                    "session_id": session.session_id,
                    "candidate_name": candidate_profile.name,
                    "candidate_type": candidate_profile.type,
                    "stage": OnboardingStage.EGG.value,
                },
            )

            # Start EGG stage
            stage_result = await self._start_stage(session, OnboardingStage.EGG)

            return {
                "success": True,
                "session_id": session.session_id,
                "current_stage": session.current_stage.value,
                "stage_tasks": stage_result.get("tasks", []),
                "instructions": "Welcome to the Hive! Please complete the EGG stage tasks to begin your integration.",
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to start onboarding: {str(e)}",
                "timestamp": datetime.now().isoformat(),
            }

    async def _start_stage(
        self, session: OnboardingSession, stage: OnboardingStage
    ) -> Dict[str, Any]:
        """Start a specific onboarding stage."""
        session.current_stage = stage
        session.stage_start_time = datetime.now()
        session.stage_data = {}

        # Get tasks for this stage
        stage_tasks = self.onboarding_tasks.get(stage, [])

        # Prepare task descriptions for the candidate
        task_descriptions = []
        for task in stage_tasks:
            task_descriptions.append(
                {
                    "task_id": task.task_id,
                    "task_type": task.task_type,
                    "description": task.description,
                    "instructions": task.instructions,
                    "time_limit": task.time_limit,
                    "difficulty": task.difficulty,
                }
            )

        # Assign a mentor if in LARVA or PUPA stage
        mentor_id = None
        if (
            stage in [OnboardingStage.LARVA, OnboardingStage.PUPA]
            and self.mentor_agents
        ):
            mentor_id = await self._assign_mentor(session)

        await self.event_bus.publish_teammate_event(
            "stage_started",
            session.candidate_profile.id,
            {
                "session_id": session.session_id,
                "stage": stage.value,
                "task_count": len(stage_tasks),
                "mentor_id": mentor_id,
            },
        )

        return {
            "stage": stage.value,
            "tasks": task_descriptions,
            "mentor_id": mentor_id,
            "stage_description": self._get_stage_description(stage),
        }

    def _get_stage_description(self, stage: OnboardingStage) -> str:
        """Get a description of what happens in each stage."""
        descriptions = {
            OnboardingStage.EGG: "Initial assessment and authentication. We verify your identity and basic communication capabilities.",
            OnboardingStage.LARVA: "Learning and exploration phase. You'll learn about the Hive's architecture, principles, and tools.",
            OnboardingStage.PUPA: "Testing and validation phase. You'll demonstrate your capabilities and collaborative skills in a safe environment.",
            OnboardingStage.ADULT: "Full integration. You become a productive member of the Hive with all privileges and responsibilities.",
        }
        return descriptions.get(stage, "Unknown stage")

    async def submit_task_result(
        self, session_id: str, task_id: str, result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Submit a result for an onboarding task.
        """
        if session_id not in self.active_sessions:
            return {"success": False, "error": "Invalid session ID"}

        session = self.active_sessions[session_id]

        try:
            # Find the task
            current_tasks = self.onboarding_tasks.get(session.current_stage, [])
            task = next((t for t in current_tasks if t.task_id == task_id), None)

            if not task:
                return {"success": False, "error": "Task not found"}

            # Evaluate the result
            evaluation = await self._evaluate_task_result(task, result)

            # Record the completion
            session.completed_tasks.append(task_id)
            session.assessment_scores[task_id] = evaluation["score"]

            # Store result data
            session.stage_data[task_id] = {
                "result": result,
                "evaluation": evaluation,
                "completed_at": datetime.now().isoformat(),
            }

            await self.event_bus.publish_teammate_event(
                "task_completed",
                session.candidate_profile.id,
                {
                    "session_id": session_id,
                    "task_id": task_id,
                    "task_type": task.task_type,
                    "score": evaluation["score"],
                    "success": evaluation["success"],
                },
            )

            # Check if stage is complete
            stage_complete = await self._check_stage_completion(session)
            if stage_complete:
                return await self._complete_stage(session)

            return {
                "success": True,
                "task_id": task_id,
                "evaluation": evaluation,
                "stage_progress": self._get_stage_progress(session),
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to submit task result: {str(e)}",
            }

    async def _evaluate_task_result(
        self, task: OnboardingTask, result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evaluate a task result against the success criteria.
        """
        score = 0.0
        feedback = []
        criteria_met = []

        # Simplified evaluation logic - in a real system this would be more sophisticated
        for criterion in task.success_criteria:
            if criterion in result.get("criteria_met", []):
                criteria_met.append(criterion)
                score += 1.0 / len(task.success_criteria)
                feedback.append(f"✓ {criterion} - Criterion met")
            else:
                feedback.append(f"✗ {criterion} - Criterion not met")

        # Bonus points for quality and thoroughness
        if result.get("quality_score", 0) > 0.8:
            score = min(1.0, score + 0.1)
            feedback.append("✓ High quality response")

        # 🧬 Sacred Enhancement: PUPA stage code review validation via bee.Jules
        if (task.stage == OnboardingStage.PUPA and
            task.task_type == "collaborative_project" and
            result.get("code_submission")):
            jules_analysis = await self._perform_jules_code_review(result.get("code_submission"))
            # Add AGRO/PAIN score to evaluation
            agro_pain_score = jules_analysis.get("agro_pain_score", 60) / 100.0
            score = (score + agro_pain_score) / 2  # Average with existing score
            feedback.append(f"🐝 bee.Jules AGRO/PAIN Analysis: {int(agro_pain_score * 100)}/100")
            if jules_analysis.get("production_ready", False):
                feedback.append("✅ Production ready: No console.log violations")
            else:
                feedback.append(f"❌ Console.log violations: {jules_analysis.get('console_log_count', 0)} found")
            if jules_analysis.get("type_safe", False):
                feedback.append("✅ Type safe: No 'any' type violations")
            else:
                feedback.append(f"❌ 'any' type violations: {jules_analysis.get('any_type_count', 0)} found")

        success = score >= 0.7  # 70% threshold for success

        return {
            "success": success,
            "score": score,
            "criteria_met": criteria_met,
            "feedback": feedback,
            "evaluation_timestamp": datetime.now().isoformat(),
        }

    async def _check_stage_completion(self, session: OnboardingSession) -> bool:
        """Check if the current stage has been completed successfully."""
        stage = session.current_stage
        requirements = self.completion_requirements.get(stage, {})

        # Check task completion count
        stage_tasks = self.onboarding_tasks.get(stage, [])
        completed_count = len(
            [t for t in stage_tasks if t.task_id in session.completed_tasks]
        )

        if completed_count < requirements.get("min_tasks_completed", 1):
            return False

        # Check success rate
        stage_scores = [
            session.assessment_scores.get(t.task_id, 0)
            for t in stage_tasks
            if t.task_id in session.completed_tasks
        ]
        if stage_scores:
            success_rate = sum(score >= 0.7 for score in stage_scores) / len(
                stage_scores
            )
            if success_rate < requirements.get("min_success_rate", 0.8):
                return False

        return True

    async def _complete_stage(self, session: OnboardingSession) -> Dict[str, Any]:
        """Complete the current stage and advance to the next one."""
        current_stage = session.current_stage

        await self.event_bus.publish_teammate_event(
            "stage_completed",
            session.candidate_profile.id,
            {
                "session_id": session.session_id,
                "completed_stage": current_stage.value,
                "completion_time": datetime.now().isoformat(),
            },
        )

        # Determine next stage
        if current_stage == OnboardingStage.EGG:
            next_stage = OnboardingStage.LARVA
        elif current_stage == OnboardingStage.LARVA:
            next_stage = OnboardingStage.PUPA
        elif current_stage == OnboardingStage.PUPA:
            next_stage = OnboardingStage.ADULT
        else:
            # Already at final stage
            return await self._complete_onboarding(session)

        # Start next stage
        stage_result = await self._start_stage(session, next_stage)

        return {
            "success": True,
            "stage_completed": current_stage.value,
            "new_stage": next_stage.value,
            "stage_info": stage_result,
            "message": f"Congratulations! You've completed the {current_stage.value.upper()} stage. Moving to {next_stage.value.upper()} stage.",
        }

    async def _complete_onboarding(self, session: OnboardingSession) -> Dict[str, Any]:
        """Complete the entire onboarding process."""
        try:
            # Create a basic teammate implementation for registration
            # This would be replaced with the actual teammate implementation
            teammate = BasicHiveTeammate(session.candidate_profile, self.event_bus)

            # Register with the Hive Registry
            from .registry import RegistrationRequest

            registration = RegistrationRequest(
                profile=session.candidate_profile,
                authentication_data={"onboarding_session": session.session_id},
                capabilities_proof=session.assessment_scores,
            )

            registration_result = await self.registry.register_teammate(registration)

            if registration_result["success"]:
                # Approve the registration automatically for successful onboarding graduates
                approval_success = await self.registry.approve_registration(
                    registration_result["registration_id"], teammate
                )

                if approval_success:
                    session.current_stage = OnboardingStage.ADULT
                    session.is_active = False

                    await self.event_bus.publish_teammate_event(
                        "onboarding_completed",
                        session.candidate_profile.id,
                        {
                            "session_id": session.session_id,
                            "total_duration": (
                                datetime.now() - session.session_start_time
                            ).total_seconds(),
                            "final_scores": session.assessment_scores,
                            "teammate_id": registration_result["teammate_id"],
                        },
                    )

                    return {
                        "success": True,
                        "message": "Congratulations! You have successfully completed onboarding and are now a full member of the Hive!",
                        "teammate_id": registration_result["teammate_id"],
                        "final_stage": OnboardingStage.ADULT.value,
                        "capabilities_confirmed": [
                            cap.value for cap in session.candidate_profile.capabilities
                        ],
                    }

            # If registration/approval failed
            session.current_stage = OnboardingStage.FAILED
            return {
                "success": False,
                "error": "Registration failed after successful onboarding",
                "registration_result": registration_result,
            }

        except Exception as e:
            session.current_stage = OnboardingStage.FAILED
            return {
                "success": False,
                "error": f"Failed to complete onboarding: {str(e)}",
            }

    async def _assign_mentor(self, session: OnboardingSession) -> Optional[str]:
        """Assign a mentor teammate to guide the onboarding process."""
        if not self.mentor_agents:
            return None

        # Simple mentor assignment - in practice this would be more sophisticated
        # considering mentor availability, expertise match, etc.
        available_mentors = await self.registry.get_available_teammates()

        for mentor_info in available_mentors:
            if (
                mentor_info["id"] in self.mentor_agents
                and mentor_info["availability"] > 0.5
            ):
                # Assign this mentor
                session.stage_data["mentor_id"] = mentor_info["id"]
                return mentor_info["id"]

        return None

    def _get_stage_progress(self, session: OnboardingSession) -> Dict[str, Any]:
        """Get progress information for the current stage."""
        stage_tasks = self.onboarding_tasks.get(session.current_stage, [])
        completed_tasks = [
            t for t in stage_tasks if t.task_id in session.completed_tasks
        ]

        return {
            "current_stage": session.current_stage.value,
            "total_tasks": len(stage_tasks),
            "completed_tasks": len(completed_tasks),
            "remaining_tasks": len(stage_tasks) - len(completed_tasks),
            "progress_percentage": (len(completed_tasks) / max(1, len(stage_tasks)))
            * 100,
            "stage_duration": (
                datetime.now() - session.stage_start_time
            ).total_seconds(),
        }

    def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """Get the current status of an onboarding session."""
        if session_id not in self.active_sessions:
            return {"error": "Session not found"}

        session = self.active_sessions[session_id]

        return {
            "session_id": session_id,
            "candidate_name": session.candidate_profile.name,
            "current_stage": session.current_stage.value,
            "stage_progress": self._get_stage_progress(session),
            "assessment_scores": session.assessment_scores,
            "is_active": session.is_active,
            "session_duration": (
                datetime.now() - session.session_start_time
            ).total_seconds(),
            "mentor_notes": session.mentor_notes,
        }

    async def _handle_onboarding_event(self, event: PollenEvent):
        """Handle onboarding-related events."""
        # This would implement event-driven coordination during onboarding
        pass

    def get_status(self) -> Dict[str, Any]:
        """Return structured status following the Legibility principle."""
        active_sessions_count = len(
            [s for s in self.active_sessions.values() if s.is_active]
        )

        stage_distribution = {}
        for session in self.active_sessions.values():
            if session.is_active:
                stage = session.current_stage.value
                stage_distribution[stage] = stage_distribution.get(stage, 0) + 1

        return {
            "component": "WelcomeGateway",
            "type": "Gateway",
            "active_sessions": active_sessions_count,
            "total_sessions": len(self.active_sessions),
            "stage_distribution": stage_distribution,
            "mentor_agents": len(self.mentor_agents),
            "available_mentors": 0,  # Will be calculated asynchronously when needed
            "curriculum_stages": list(self.onboarding_tasks.keys()),
            "timestamp": datetime.now().isoformat(),
            "health": "active",
        }


# Minimal teammate implementation for testing
class BasicHiveTeammate(HiveTeammate):
    """A basic teammate implementation for testing and demonstration."""

    async def initialize(self) -> bool:
        self.status = TeammateStatus.ACTIVE
        return True

    async def execute_task(self, task: TaskRequest) -> TaskResult:
        # Simplified task execution
        return TaskResult(
            task_id=task.task_id,
            success=True,
            result_data={"message": "Task completed by basic teammate"},
            execution_time=1.0,
        )

    async def get_capabilities(self) -> List[TeammateCapability]:
        return self.profile.capabilities

    async def _perform_jules_code_review(self, code_submission: str) -> Dict[str, Any]:
        """
        Sacred organic code review via bee.Jules organella (Pure Event-Driven)
        Sacred Justification: Single responsibility - gateway only orchestrates, jules analyzes
        """
        # Request bee.Jules AGRO/PAIN analysis via Pollen Protocol
        request_id = str(uuid.uuid4())
        await self.event_bus.publish(PollenEvent(
            event_type="jules_agro_pain_analysis_requested",
            source_component="welcome_gateway",
            aggregate_id="bee.jules",
            payload={
                "code_context": code_submission,
                "analysis_type": "agro_pain_speed_check",
                "metamorphosis_stage": "pupa",
                "request_id": request_id
            }
        ))

        # Direct invocation for immediate response (synchronous metamorphosis requirement)
        # This maintains organic integration while eliminating duplication
        jules_agent = self.registry.get_teammate("bee.jules")
        if not jules_agent:
            raise RuntimeError("bee.Jules organella not available for PUPA stage validation")

        return await jules_agent.perform_agro_pain_analysis(code_submission)

    async def health_check(self) -> bool:
        return True

    async def shutdown(self) -> bool:
        return True
