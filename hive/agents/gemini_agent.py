
"""
Gemini AI Integration for the Hive Ecosystem
"""

import os
import time
import json
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime

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
        print(f"🤖 Gemini agent sent: {text}")
