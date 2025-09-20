import asyncio
import logging
from typing import Any

class BaseAgent:
    def __init__(self, p2p_client: Any, event_bus: asyncio.Queue, logger: logging.Logger):
        self.p2p_client = p2p_client
        self.event_bus = event_bus
        self.logger = logger
        self.name = self.__class__.__name__

    async def start(self):
        self.logger.info(f"Agent {self.name} starting.")
        # Agents can subscribe to host events here
        asyncio.create_task(self._subscribe_to_host_events())

    async def stop(self):
        self.logger.info(f"Agent {self.name} stopping.")

    async def _subscribe_to_host_events(self):
        while True:
            event = await self.event_bus.get()
            self.logger.info(f"Agent {self.name} received host event: {event}")
            if event["type"] == "host_shutdown":
                self.logger.info(f"Agent {self.name} received host shutdown event. Stopping.")
                break
            # Process other host events

    def get_status(self) -> dict:
        return {"name": self.name, "status": "running"}
