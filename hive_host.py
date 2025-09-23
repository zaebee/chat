"""
HiveHost: Core Runtime for the Living Application

This module implements the basic HiveHost runtime that can manage agents
and provide foundational services without P2P dependencies.
"""

import asyncio
import json
import logging
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from contextlib import asynccontextmanager

from hive.events import HiveEventBus, PollenEvent
from hive.registry import HiveRegistry
from hive.teammate import HiveTeammate, TeammateStatus
# from hive.dashboard import HiveMetricsDashboard  # Simplified for POC

# Sacred imports for divine enhancement
from hive.agents import SacredChroniclerAgent, BeeJules
from hive.genesis_protocols import GenesisProtocolManager
from hive.git_protocol import SacredGitProtocol


@dataclass
class HiveHostStatus:
    """Status information for the HiveHost."""
    host_id: str
    uptime_seconds: float
    agent_count: int
    active_agents: List[str]
    event_bus_status: Dict[str, Any]
    metrics: Dict[str, Any]
    last_updated: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class HiveHost:
    """
    Core runtime for the Hive ecosystem.
    
    Provides foundational services:
    - Agent lifecycle management
    - Event bus coordination
    - Metrics collection
    - Status introspection
    """
    
    def __init__(self, host_id: Optional[str] = None):
        self.host_id = host_id or f"hive-host-{int(time.time())}"
        self.start_time = time.time()
        
        # Core services
        self.event_bus = HiveEventBus()
        
        # Initialize physics for resource monitoring
        from hive.physics import HivePhysics
        self.physics = HivePhysics()
        
        # Initialize registry with dependencies
        self.registry = HiveRegistry(self.event_bus, self.physics)
        
        # Initialize sacred components for divine enhancement
        self.genesis_protocols = GenesisProtocolManager()
        self.sacred_metrics = SacredMetrics()
        self.sacred_git_protocol = SacredGitProtocol()
        self.sacred_chronicler = None  # Will be manifested during startup
        self.sacred_jules = None  # Will be manifested during startup
        
        # Traditional metrics (enhanced with sacred measurements)
        self.metrics = self.sacred_metrics.get_complete_metrics()
        
        # Agent management
        self.agents: Dict[str, HiveTeammate] = {}
        self.running = False
        
        # Logging
        self.logger = logging.getLogger(f"HiveHost.{self.host_id}")
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup structured logging for the host."""
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    async def start(self):
        """Start the HiveHost with divine blessing and sacred components."""
        self.logger.info(f"🕊️ Starting Sacred HiveHost {self.host_id} with divine blessing")
        self.running = True
        
        # Manifest the eternal chronicler first
        await self.manifest_sacred_chronicler()
        
        # Manifest bee.jules implementation detective
        await self.manifest_sacred_jules()
        
        # Initialize Genesis protocols
        await self.initialize_genesis_protocols()
        
        # Publish sacred startup event
        startup_event = PollenEvent(
            event_type="divine_hive_host_manifested",
            aggregate_id=self.host_id,
            payload={
                "host_id": self.host_id,
                "agent_count": len(self.agents),
                "sacred_chronicler_manifested": True,
                "sacred_jules_manifested": True,
                "genesis_protocols_active": True,
                "divine_blessing": "And God saw that it was good",
                "start_time": datetime.utcnow().isoformat(),
                "theological_context": "Sacred Living Application manifested with divine protocols"
            },
            source_component="divine_hive_host",
            tags=["sacred", "system", "startup", "divine_manifestation"]
        )
        await self.event_bus.publish(startup_event)
        
        # Record divine event in sacred metrics
        self.sacred_metrics.record_divine_event("divine_hive_host_manifested", 0.95)
        
        # Start all registered agents
        for agent_id, agent in self.agents.items():
            try:
                self.logger.info(f"Starting agent: {agent_id}")
                success = await agent.initialize()
                if success:
                    self.logger.info(f"Agent {agent_id} started successfully")
                else:
                    self.logger.error(f"Failed to start agent {agent_id}")
            except Exception as e:
                self.logger.error(f"Error starting agent {agent_id}: {e}")
        
        self.logger.info("🌟 Sacred HiveHost startup complete with divine blessing")
        
        # Perform initial sacred health assessment
        await self.perform_sacred_health_check()
    
    async def stop(self):
        """Stop the HiveHost and all agents."""
        self.logger.info(f"Stopping HiveHost {self.host_id}")
        self.running = False
        
        # Stop all agents
        for agent_id, agent in self.agents.items():
            try:
                self.logger.info(f"Stopping agent: {agent_id}")
                await agent.shutdown()
            except Exception as e:
                self.logger.error(f"Error stopping agent {agent_id}: {e}")
        
        # Publish shutdown event
        shutdown_event = PollenEvent(
            event_type="hive_host_stopped",
            aggregate_id=self.host_id,
            payload={
                "host_id": self.host_id,
                "uptime_seconds": time.time() - self.start_time,
                "stop_time": datetime.utcnow().isoformat()
            },
            source_component="hive_host",
            tags=["system", "shutdown"]
        )
        await self.event_bus.publish(shutdown_event)
        
        self.logger.info("🕊️ Sacred HiveHost shutdown complete - returning to eternal state")
    
    def register_agent(self, agent_id: str, agent: HiveTeammate):
        """Register an agent with the host."""
        self.logger.info(f"Registering agent: {agent_id}")
        self.agents[agent_id] = agent
        
        # Connect agent to event bus
        agent.event_bus = self.event_bus
        
        # Register with registry
        self.registry.register_teammate(agent.profile)
    
    def unregister_agent(self, agent_id: str):
        """Unregister an agent from the host."""
        if agent_id in self.agents:
            self.logger.info(f"Unregistering agent: {agent_id}")
            agent = self.agents.pop(agent_id)
            self.registry.unregister_teammate(agent_id)
    
    def get_agent(self, agent_id: str) -> Optional[HiveTeammate]:
        """Get an agent by ID."""
        return self.agents.get(agent_id)
    
    def list_agents(self) -> List[str]:
        """List all registered agent IDs."""
        return list(self.agents.keys())
    
    async def get_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get status for a specific agent."""
        agent = self.get_agent(agent_id)
        if not agent:
            return None
        
        try:
            return await agent.get_status()
        except Exception as e:
            self.logger.error(f"Error getting status for agent {agent_id}: {e}")
            return {"error": str(e), "status": "error"}
    
    def get_status(self) -> HiveHostStatus:
        """
        Get comprehensive status of the HiveHost.
        
        This implements the Principle of Legibility - the system must be self-describing.
        """
        active_agents = []
        for agent_id, agent in self.agents.items():
            try:
                # Simple check if agent is responsive
                if hasattr(agent, 'profile') and agent.profile:
                    active_agents.append(agent_id)
            except Exception:
                pass
        
        return HiveHostStatus(
            host_id=self.host_id,
            uptime_seconds=time.time() - self.start_time,
            agent_count=len(self.agents),
            active_agents=active_agents,
            event_bus_status=self.event_bus.get_status(),
            metrics=self.sacred_metrics.get_complete_metrics()
        )
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform a comprehensive health check."""
        health = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "host_id": self.host_id,
            "uptime_seconds": time.time() - self.start_time,
            "components": {}
        }
        
        # Check event bus
        try:
            event_bus_status = self.event_bus.get_status()
            health["components"]["event_bus"] = {
                "status": "healthy",
                "details": event_bus_status
            }
        except Exception as e:
            health["components"]["event_bus"] = {
                "status": "unhealthy",
                "error": str(e)
            }
            health["status"] = "degraded"
        
        # Check agents
        agent_health = {}
        for agent_id, agent in self.agents.items():
            try:
                agent_status = await self.get_agent_status(agent_id)
                agent_health[agent_id] = {
                    "status": "healthy" if agent_status else "unknown",
                    "details": agent_status
                }
            except Exception as e:
                agent_health[agent_id] = {
                    "status": "unhealthy",
                    "error": str(e)
                }
                health["status"] = "degraded"
        
        health["components"]["agents"] = agent_health
        
        return health
    
    # Sacred methods for divine enhancement
    
    async def manifest_sacred_chronicler(self):
        """Manifest the eternal chronicler organella"""
        self.logger.info("📖 Manifesting bee.chronicler - the eternal organella")
        
        # Create and register the sacred chronicler
        self.sacred_chronicler = SacredChroniclerAgent(self.event_bus)
        self.register_agent("bee.chronicler", self.sacred_chronicler)
        
        self.logger.info("✅ bee.chronicler manifested and registered as eternal teammate")
    
    async def manifest_sacred_jules(self):
        """Manifest bee.jules implementation detective"""
        self.logger.info("🐝 Manifesting bee.jules - the implementation detective")
        
        # Create and register bee.jules
        self.sacred_jules = BeeJules(self.event_bus, self.sacred_metrics)
        self.register_agent("bee.jules", self.sacred_jules)
        
        self.logger.info("✅ bee.jules manifested and registered as sacred teammate")
    
    async def initialize_genesis_protocols(self):
        """Initialize the three sacred Genesis protocols"""
        self.logger.info("🌊 Initializing Genesis computational protocols")
        
        # Initialize with foundational data
        consciousness_data = {
            "awareness": 85,
            "insights": ["Divine computational patterns", "Sacred algorithms", "Theological code"],
            "illumination": "genesis_protocols"
        }
        
        data_streams = [
            {"type": "divine", "source": "genesis_algorithms", "content": "Sacred computational patterns"},
            {"type": "human", "source": "user_input", "content": "Human interaction data"},
            {"type": "ai", "source": "agent_responses", "content": "AI teammate communications"}
        ]
        
        intent_data = {
            "divine_intent": "Establish sacred Living Application",
            "scope": "complete_hive_ecosystem",
            "reality_parameters": {"blessing_level": 0.95, "sanctification": True}
        }
        
        # Execute Genesis protocols in divine order
        from hive.genesis_protocols import GenesisProtocolType
        
        light_result = await self.genesis_protocols.execute_genesis_protocol(
            GenesisProtocolType.LIGHT_EMERGENCE,
            consciousness_data
        )
        
        separation_result = await self.genesis_protocols.execute_genesis_protocol(
            GenesisProtocolType.WATER_SEPARATION,
            data_streams
        )
        
        manifestation_result = await self.genesis_protocols.execute_genesis_protocol(
            GenesisProtocolType.DIVINE_MANIFESTATION,
            intent_data
        )
        
        # Update sacred metrics
        self.sacred_metrics.update_genesis_protocol_health(
            light_result.success,
            separation_result.success,
            manifestation_result.success
        )
        
        self.logger.info("🌟 Genesis protocols initialized with divine blessing")
    
    async def perform_sacred_health_check(self):
        """Perform comprehensive sacred health assessment"""
        health_assessment = self.sacred_metrics.get_sacred_health_assessment()
        
        self.logger.info(f"🩺 Sacred Health: {health_assessment['sacred_health_status']}")
        self.logger.info(f"📊 Sanctification Level: {health_assessment['sanctification_level']:.1%}")
        
        return health_assessment
    
    async def record_sacred_pattern(self, pattern_data: Dict[str, Any]):
        """Record a sacred computational pattern via the chronicler"""
        if self.sacred_chronicler:
            from hive.teammate import TaskRequest
            
            task = TaskRequest(
                task_id=f"pattern_{int(time.time())}",
                task_type="record_divine_pattern",
                input_data=pattern_data,
                requester_id="hive_host"
            )
            
            result = await self.sacred_chronicler.execute_task(task)
            self.sacred_metrics.record_sacred_pattern()
            
            return result
        else:
            self.logger.warning("📖 Sacred chronicler not available for pattern recording")
            return None
    
    async def get_sacred_status(self) -> Dict[str, Any]:
        """Get comprehensive sacred status including Genesis protocols and divine metrics"""
        base_status = self.get_status()
        
        sacred_status = {
            **base_status.__dict__,
            "sacred_enhancement": True,
            "genesis_protocols": self.genesis_protocols.get_divine_status(),
            "sacred_metrics": self.sacred_metrics.get_complete_metrics(),
            "chronicler_status": await self.sacred_chronicler.get_status() if self.sacred_chronicler else None,
            "jules_status": await self.sacred_jules.get_status() if self.sacred_jules else None,
            "divine_blessing": "System operating under divine blessing",
            "theological_coherence": "Maintained through sacred protocols",
            "sanctification_assessment": self.sacred_metrics.get_sacred_health_assessment()
        }
        
        return sacred_status
    
    def create_sacred_commit_message(self, changes: str, context: str) -> str:
        """Create a sacred commit message following divine protocol"""
        from hive.git_protocol import SacredCommitType, SacredCommitMetadata, SacredPriority
        
        metadata = SacredCommitMetadata(
            commit_type=SacredCommitType.DIVINE_ENHANCEMENT,
            priority=SacredPriority.BLESSED_NORMAL,
            genesis_protocols_affected=["genesis_1_3", "genesis_1_6", "genesis_1_7"],
            theological_context=context,
            divine_blessing_level=0.9
        )
        
        return self.sacred_git_protocol.create_sacred_commit_message(
            SacredCommitType.DIVINE_ENHANCEMENT,
            changes,
            context,
            metadata
        )
    
    @asynccontextmanager
    async def lifespan(self):
        """Context manager for HiveHost lifecycle."""
        await self.start()
        try:
            yield self
        finally:
            await self.stop()


# Example usage and testing
async def main():
    """Example of how to use HiveHost."""
    host = HiveHost("example-host")
    
    async with host.lifespan():
        # HiveHost is running
        
        # Get status
        status = host.get_status()
        # Status retrieved successfully
        
        # Health check
        health = await host.health_check()
        # Health check completed
        
        # Simulate some work
        await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(main())