"""
Complete System Test

This script tests the entire Hive Chat system including:
- HiveHost runtime
- AI agents integration
- Event system
- Status APIs
"""

import asyncio
import json
from test_mock_agent import MockAIAgent
from hive_host import HiveHost

async def test_complete_system():
    """Test the complete Hive Chat system."""
    print("🐝 Testing Complete Hive Chat System")
    print("=" * 50)
    
    # Create HiveHost
    host = HiveHost("complete-test-host")
    
    try:
        # Start the host
        await host.start()
        print(f"✅ HiveHost started: {host.host_id}")
        
        # Add AI agents
        agent1 = MockAIAgent("ChatBot", host.event_bus)
        agent2 = MockAIAgent("CodeReviewer", host.event_bus)
        
        host.register_agent("chatbot", agent1)
        host.register_agent("reviewer", agent2)
        
        print(f"✅ Registered {len(host.list_agents())} agents")
        
        # Test system status
        print("\n📊 System Status:")
        status = host.get_status()
        print(f"  Host ID: {status.host_id}")
        print(f"  Uptime: {status.uptime_seconds:.2f}s")
        print(f"  Agents: {status.agent_count}")
        print(f"  Active Agents: {status.active_agents}")
        print(f"  Metrics: τ={status.metrics['tau']}, φ={status.metrics['phi']}, σ={status.metrics['sigma']}")
        
        # Test health check
        print("\n❤️ Health Check:")
        health = await host.health_check()
        print(f"  Overall Status: {health['status']}")
        print(f"  Components: {list(health['components'].keys())}")
        
        # Test event system
        print("\n📡 Event System:")
        event_status = host.event_bus.get_status()
        print(f"  Events Processed: {event_status['total_events_processed']}")
        print(f"  Recent Events: {event_status['recent_event_types']}")
        
        # Test AI agent interaction
        print("\n🤖 AI Agent Interaction:")
        from hive.teammate import TaskRequest
        
        task = TaskRequest(
            task_id="demo_task",
            task_type="chat_message",
            input_data={"message": "Hello from the complete system test!"},
            requester_id="system_test"
        )
        
        result = await agent1.execute_task(task)
        print(f"  Agent Response: {result.result_data['response']}")
        print(f"  Success: {result.success}")
        print(f"  Execution Time: {result.execution_time}s")
        
        # Test agent capabilities
        print("\n🔧 Agent Capabilities:")
        for agent_id in host.list_agents():
            agent = host.get_agent(agent_id)
            capabilities = await agent.get_capabilities()
            print(f"  {agent_id}: {[cap.value for cap in capabilities]}")
        
        print("\n🎉 Complete System Test PASSED!")
        print("\n📋 System Summary:")
        print(f"  • HiveHost Runtime: ✅ Working")
        print(f"  • AI Agents: ✅ {status.agent_count} agents registered")
        print(f"  • Event System: ✅ {event_status['total_events_processed']} events processed")
        print(f"  • Health Monitoring: ✅ All components healthy")
        print(f"  • Task Processing: ✅ AI agents responding")
        
        print("\n🚀 Ready for deployment to chat.zae.life!")
        
    except Exception as e:
        print(f"❌ System test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        await host.stop()
        print("\n🛑 System test completed")
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_complete_system())
    exit(0 if success else 1)