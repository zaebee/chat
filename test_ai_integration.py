"""
Test AI Agents Integration with HiveHost

This script tests the integration of AI agents (Mistral, Gemini) with the HiveHost.
"""

import asyncio
import os
from dotenv import load_dotenv

from hive_host import HiveHost
from hive.agents.mistral_agent import MistralAgent
from hive.teammate import TeammateProfile, TeammateCapability

# Load environment variables
load_dotenv()

async def test_ai_integration():
    """Test AI agents integration with HiveHost."""
    print("🐝 Testing AI Agents Integration with HiveHost")
    
    # Create HiveHost
    host = HiveHost("ai-test-host")
    
    try:
        # Start the host
        await host.start()
        print(f"✅ HiveHost started: {host.host_id}")
        
        # Test 1: Check if we can create a Mistral agent
        print("\n📝 Test 1: Creating Mistral Agent")
        
        # Check if Mistral API key is available
        mistral_api_key = os.getenv('MISTRAL_API_KEY')
        if mistral_api_key:
            print("✅ Mistral API key found")
            
            # Create Mistral agent profile
            mistral_profile = TeammateProfile(
                name="Test Mistral Agent",
                type="mistral",
                capabilities=[
                    TeammateCapability.CODE_ANALYSIS,
                    TeammateCapability.CODE_GENERATION,
                    TeammateCapability.CONVERSATION
                ],
                specializations=["Python", "Code Review", "Documentation"],
                max_concurrent_tasks=2,
                response_time_estimate=3.0
            )
            
            # Create and register Mistral agent
            mistral_agent = MistralAgent(mistral_profile, mistral_api_key)
            host.register_agent("mistral_test", mistral_agent)
            
            print(f"✅ Mistral agent registered: {mistral_agent.profile.name}")
            
            # Test agent status
            agent_status = await host.get_agent_status("mistral_test")
            print(f"📊 Agent status: {agent_status}")
            
        else:
            print("⚠️ Mistral API key not found - skipping Mistral agent test")
        
        # Test 2: Check HiveHost status with agents
        print("\n📊 Test 2: HiveHost Status with Agents")
        status = host.get_status()
        print(f"Host ID: {status.host_id}")
        print(f"Agent Count: {status.agent_count}")
        print(f"Active Agents: {status.active_agents}")
        print(f"Uptime: {status.uptime_seconds:.2f}s")
        
        # Test 3: Health check
        print("\n❤️ Test 3: Health Check")
        health = await host.health_check()
        print(f"Overall Status: {health['status']}")
        print(f"Components: {list(health['components'].keys())}")
        
        # Test 4: Event bus integration
        print("\n📡 Test 4: Event Bus Integration")
        event_status = host.event_bus.get_status()
        print(f"Events processed: {event_status['total_events_processed']}")
        print(f"Recent event types: {event_status['recent_event_types']}")
        
        print("\n🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up
        await host.stop()
        print("🛑 HiveHost stopped")

if __name__ == "__main__":
    asyncio.run(test_ai_integration())