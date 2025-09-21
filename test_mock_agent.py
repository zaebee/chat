"""
Test with Mock AI Agent

This script tests the HiveHost with a simple mock AI agent.
"""

import asyncio
from typing import Dict, Any, Optional

from hive_host import HiveHost
from hive.teammate import HiveTeammate, TeammateProfile, TaskRequest, TaskResult, TeammateCapability, TeammateStatus
from hive.events import HiveEventBus
from hive.events import PollenEvent

class MockAIAgent(HiveTeammate):
    """Mock AI agent for testing purposes."""
    
    def __init__(self, name: str = "MockBot", event_bus: Optional[HiveEventBus] = None):
        profile = TeammateProfile(
            name=name,
            type="mock",
            capabilities=[
                TeammateCapability.CONVERSATION,
                TeammateCapability.CODE_ANALYSIS
            ],
            specializations=["Testing", "Mock Responses"],
            max_concurrent_tasks=5,
            response_time_estimate=0.5
        )
        # Create a dummy event bus if none provided
        if event_bus is None:
            from hive.events import HiveEventBus
            event_bus = HiveEventBus()
        
        super().__init__(profile, event_bus)
        self.is_initialized = False
        self.task_count = 0
    
    async def initialize(self) -> bool:
        """Initialize the mock agent."""
        print(f"🤖 Initializing {self.profile.name}")
        self.is_initialized = True
        
        # Publish initialization event
        if self.event_bus:
            event = PollenEvent(
                event_type="agent_initialized",
                aggregate_id=self.profile.name,
                payload={
                    "agent_name": self.profile.name,
                    "agent_type": self.profile.type,
                    "capabilities": [cap.value for cap in self.profile.capabilities]
                },
                source_component="mock_agent",
                tags=["agent", "initialization", "mock"]
            )
            await self.event_bus.publish(event)
        
        return True
    
    async def shutdown(self) -> bool:
        """Shutdown the mock agent."""
        print(f"🛑 Shutting down {self.profile.name}")
        self.is_initialized = False
        return True
    
    async def get_capabilities(self) -> list[TeammateCapability]:
        """Return current capabilities."""
        return self.profile.capabilities
    
    async def health_check(self) -> bool:
        """Perform health check."""
        return self.is_initialized
    
    async def execute_task(self, task: TaskRequest) -> TaskResult:
        """Process a task request."""
        self.task_count += 1
        
        print(f"📝 {self.profile.name} processing task: {task.task_type}")
        
        # Simulate processing time
        await asyncio.sleep(0.1)
        
        # Generate mock response based on task type
        if task.task_type == "chat_message":
            response = f"🐝 Hello! I'm {self.profile.name}, a mock AI agent. You said: '{task.input_data.get('message', '')}'"
        elif task.task_type == "code_review":
            response = f"🔍 Code looks good! This is a mock review from {self.profile.name}."
        else:
            response = f"✅ Task '{task.task_type}' completed by {self.profile.name}"
        
        return TaskResult(
            task_id=task.task_id,
            success=True,
            result_data={"response": response, "mock": True},
            execution_time=0.1,
            metadata={"agent": self.profile.name, "task_count": self.task_count}
        )
    
    async def get_status(self) -> Dict[str, Any]:
        """Get agent status."""
        return {
            "agent_name": self.profile.name,
            "type": self.profile.type,
            "status": "active" if self.is_initialized else "inactive",
            "tasks_processed": self.task_count,
            "capabilities": [cap.value for cap in self.profile.capabilities],
            "uptime": "mock_uptime",
            "health": "healthy"
        }

async def test_mock_agent():
    """Test HiveHost with mock AI agent."""
    print("🐝 Testing HiveHost with Mock AI Agent")
    
    # Create HiveHost
    host = HiveHost("mock-test-host")
    
    try:
        # Start the host
        await host.start()
        print(f"✅ HiveHost started: {host.host_id}")
        
        # Create and register mock agents
        agent1 = MockAIAgent("BuzzyBot", host.event_bus)
        agent2 = MockAIAgent("HoneyHelper", host.event_bus)
        
        host.register_agent("buzzy", agent1)
        host.register_agent("honey", agent2)
        
        print(f"✅ Registered agents: {host.list_agents()}")
        
        # Test agent status
        for agent_id in host.list_agents():
            status = await host.get_agent_status(agent_id)
            print(f"📊 {agent_id} status: {status}")
        
        # Test task processing
        print("\n📝 Testing task processing")
        
        task1 = TaskRequest(
            task_id="test_task_1",
            task_type="chat_message",
            input_data={"message": "Hello from the Hive!"},
            requester_id="test_user",
            priority=1
        )
        
        result1 = await agent1.execute_task(task1)
        print(f"✅ Task result: {result1.result_data}")
        
        # Test HiveHost status with agents
        print("\n📊 Final HiveHost Status")
        status = host.get_status()
        print(f"Host ID: {status.host_id}")
        print(f"Agent Count: {status.agent_count}")
        print(f"Active Agents: {status.active_agents}")
        
        # Test health check
        health = await host.health_check()
        print(f"\n❤️ Health Status: {health['status']}")
        
        print("\n🎉 Mock agent test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up
        await host.stop()
        print("🛑 HiveHost stopped")

if __name__ == "__main__":
    asyncio.run(test_mock_agent())