
"""
Gemini AI Integration for the Hive Ecosystem
"""

import os
import time
import json
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime
from dotenv import load_dotenv

try:
    import google.generativeai as genai
except ImportError:
    print(
        "Warning: google-generativeai package not available. Install with: pip install google-generativeai"
    )
    genai = None

from ..teammate import (
    HiveTeammate,
    TeammateProfile,
    TaskRequest,
    TaskResult,
    TeammateCapability,
    TeammateStatus,
)
from ..events import HiveEventBus, PollenEvent


class GeminiAgent(HiveTeammate):
    """
    Gemini AI agent integrated into the Hive ecosystem.
    """

    def __init__(
        self,
        event_bus: HiveEventBus,
        model: str = "gemini-pro",
        api_key: Optional[str] = None,
    ):
        """
        Initialize the Gemini agent.
        """
        load_dotenv()
        # Get API key from parameter or environment
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")

        if not self.api_key:
            raise ValueError(
                "GOOGLE_API_KEY not found. Provide api_key parameter or set GOOGLE_API_KEY environment variable."
            )

        # Create profile
        profile = TeammateProfile(
            id=f"gemini_{int(time.time())}",
            name="Gemini Code Assistant",
            type="gemini",
            capabilities=[
                TeammateCapability.CODE_ANALYSIS,
                TeammateCapability.CODE_GENERATION,
                TeammateCapability.CONVERSATION,
                TeammateCapability.LEARNING_SUPPORT,
            ],
            specializations=[
                "Multi-modal understanding (text and images)",
                "Large context window for complex reasoning",
                "Advanced code generation and explanation",
            ],
            max_concurrent_tasks=2,
            response_time_estimate=3.0,
        )

        # Initialize parent class
        super().__init__(profile, event_bus)

        # Gemini-specific setup
        self.model = model
        self.client = None

        if genai:
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel(self.model)

        print(f"🤖 Gemini agent initialized (model: {model})")

    async def initialize(self) -> bool:
        self.status = TeammateStatus.ACTIVE
        await self.subscribe_to_events(["message_sent"])
        return True

    async def execute_task(self, task: TaskRequest) -> TaskResult:
        # TODO: Implement task execution
        return TaskResult(task_id=task.task_id, success=False, error_message="Not implemented")

    async def get_capabilities(self) -> List[TeammateCapability]:
        return self.profile.capabilities

    async def health_check(self) -> bool:
        # TODO: Implement health check
        return self.client is not None

    async def shutdown(self) -> bool:
        self.status = TeammateStatus.OFFLINE
        return True

    async def on_event_received(self, event: PollenEvent):
        if event.event_type == "message_sent":
            await self._handle_chat_message(event)

    async def _handle_chat_message(self, event: PollenEvent):
        message_text = event.payload.get("text", "").lower()
        sender_name = event.payload.get("sender_name", "")

        if sender_name == self.profile.name:
            return

        if "gemini" in message_text or "@gemini" in message_text:
            response_text = f"Hello {sender_name}! I am Gemini, ready to assist."
            await self._send_chat_response(response_text, event.payload.get("chat_session", "main"))

    async def _send_chat_response(self, text: str, chat_session: str = "main"):
        await self.event_bus.publish_message_event(
            "sent",
            f"gemini_response_{int(time.time())}",
            {
                "text": text,
                "sender_id": self.profile.id,
                "sender_name": self.profile.name,
                "timestamp": datetime.now().isoformat(),
                "chat_session": chat_session,
                "is_bot": True,
            },
        )
        print(f"✨ Gemini Learning Guide sent: {text}")

    async def _generate_educational_response(
        self,
        message_text: str,
        sender_name: str,
        user_id: str
    ) -> str:
        """Generate context-aware educational responses."""
        # Check if user has organellas and current progress
        if self.organella_manager:
            organellas = await self.organella_manager.get_user_organellas(user_id)
            if organellas:
                main_organella = organellas[0]
                level = main_organella.level
                stage = main_organella.stage.value

                if "progress" in message_text or "level" in message_text:
                    return f"Hello {sender_name}! 🌟 Your organella {main_organella.name} is at Level {level} in the {stage} stage. Let's continue your learning journey!"

        # Check for learning keywords and provide appropriate guidance
        if "challenge" in message_text:
            return f"Hi {sender_name}! Ready for a new coding challenge? I can create personalized challenges based on your current skill level. What would you like to practice today?"
        elif "stuck" in message_text or "help" in message_text:
            return f"No worries {sender_name}! Learning to code is a journey. Can you share what specific concept you're working on? I'll provide a gentle hint to guide you forward. 🤝"
        elif "hint" in message_text:
            return f"Here's a learning tip {sender_name}: Break down the problem into smaller steps. What's the first small thing you can implement? Sometimes the biggest breakthroughs come from tiny steps! 💡"
        else:
            return f"Hello {sender_name}! I'm Gemini, your learning guide in the Hive! 🌟 I specialize in creating educational content, designing challenges, and helping you progress on your coding journey. How can I support your learning today?"

    async def _handle_challenge_completion(self, event: PollenEvent):
        """Handle when a student completes a challenge."""
        user_id = event.payload.get("user_id")
        challenge_id = event.payload.get("challenge_id")

        if self.organella_manager and self.tale_weaver:
            # Generate celebration and tale progression
            celebration = await self._create_completion_celebration(user_id, challenge_id)
            await self._send_chat_response(celebration, "main")

    async def _handle_organella_event(self, event: PollenEvent):
        """Handle organella-related events like evolution, skill upgrades."""
        event_type = event.event_type
        user_id = event.payload.get("user_id")

        if event_type == "organella_evolved":
            organella_name = event.payload.get("organella_name")
            new_stage = event.payload.get("new_stage")
            celebration = f"🎉 Incredible! {organella_name} has evolved to {new_stage} stage! This is a major milestone in your learning journey. New adventures await!"
            await self._send_chat_response(celebration, "main")

    async def _handle_learning_event(self, event: PollenEvent):
        """Handle learning-specific events."""
        # Placeholder for learning analytics and adaptive responses
        pass

    async def _handle_collaboration_event(self, event: PollenEvent):
        """Handle collaboration requests from other AI teammates."""
        if event.event_type == "collaboration_handoff" and event.payload.get("to") == "gemini":
            task_id = event.payload.get("task_id")
            reason = event.payload.get("reason")
            print(f"✨ Gemini received collaboration handoff for task {task_id}: {reason}")

    async def _create_challenge(self, task: TaskRequest) -> TaskResult:
        """Create a new coding challenge based on student level."""
        # This would integrate with the challenge system
        # For now, return a success placeholder
        return TaskResult(
            task_id=task.task_id,
            success=True,
            result={"message": "Challenge creation capability ready"}
        )

    async def _analyze_student_progress(self, task: TaskRequest) -> TaskResult:
        """Analyze student progress and suggest next steps."""
        return TaskResult(
            task_id=task.task_id,
            success=True,
            result={"message": "Progress analysis capability ready"}
        )

    async def _generate_learning_hint(self, task: TaskRequest) -> TaskResult:
        """Generate contextual hints for struggling students."""
        return TaskResult(
            task_id=task.task_id,
            success=True,
            result={"message": "Learning hint generation capability ready"}
        )

    async def _create_tale_chapter(self, task: TaskRequest) -> TaskResult:
        """Create new tale chapters for organella progression."""
        return TaskResult(
            task_id=task.task_id,
            success=True,
            result={"message": "Tale chapter creation capability ready"}
        )

    async def _create_completion_celebration(self, user_id: str, challenge_id: str) -> str:
        """Create a personalized celebration message for challenge completion."""
        return f"🌟 Congratulations! You've successfully completed Challenge {challenge_id}! Your organella is growing stronger with each solved challenge. Keep up the amazing work!"

    def set_educational_components(self, organella_manager, tale_weaver):
        """Set references to educational system components."""
        self.organella_manager = organella_manager
        self.tale_weaver = tale_weaver

    def set_collaboration_hub(self, collaboration_hub):
        """Set reference to collaboration coordination system."""
        self.collaboration_hub = collaboration_hub
