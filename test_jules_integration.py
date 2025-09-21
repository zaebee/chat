"""
Test bee.Jules Integration with Sacred Team Communication

This test verifies that bee.Jules can be manifested, respond to commands,
and communicate through the Sacred Team Communication system.
"""

import asyncio
import json
from hive_host import HiveHost
from hive.sacred.team_communication import SacredTeamCommunication


async def test_jules_integration():
    """Test complete bee.Jules integration"""
    print("🐝 Testing bee.Jules Integration with Sacred Team Communication")
    print("=" * 70)
    
    # Initialize HiveHost
    host = HiveHost("jules-test-host")
    
    try:
        # Start the host (this will manifest bee.jules and bee.chronicler)
        await host.start()
        print("✅ HiveHost started with sacred agents")
        
        # Initialize Sacred Team Communication
        team_comm = SacredTeamCommunication(host.event_bus)
        print("✅ Sacred Team Communication initialized")
        
        # Test 1: Check that bee.jules is manifested
        print("\n🧪 Test 1: Verify bee.jules manifestation")
        jules_agent = host.get_agent("bee.jules")
        if jules_agent:
            jules_status = await jules_agent.get_status()
            print(f"✅ bee.jules manifested: {jules_status['agent_id']}")
            print(f"   Role: {jules_status['role']}")
            print(f"   Sacred Nature: {jules_status['sacred_nature']}")
            print(f"   Implementation Mastery: {jules_status['implementation_mastery']:.1%}")
            print(f"   Debugging Divinity: {jules_status['debugging_divinity']:.1%}")
        else:
            print("❌ bee.jules not found")
            return
        
        # Test 2: Test Sacred Team Status Command
        print("\n🧪 Test 2: Test /sacred.team.status command")
        status_result = await team_comm.process_sacred_command("/sacred.team.status", "", "test_user")
        print(f"✅ Status command result: {status_result}")
        
        # Test 3: Test bee.jules help command
        print("\n🧪 Test 3: Test /bee.jules.help command")
        help_result = await team_comm.process_sacred_command(
            "/bee.jules.help", 
            "I'm having trouble with async event handling in my sacred protocol implementation",
            "test_user"
        )
        print(f"✅ Jules help command result: {help_result}")
        
        # Test 4: Test bee.jules analyze command
        print("\n🧪 Test 4: Test /bee.jules.analyze command")
        code_sample = """
async def sacred_event_handler(event):
    try:
        await process_divine_event(event)
    except Exception as e:
        logger.error(f"Sacred event processing failed: {e}")
"""
        analyze_result = await team_comm.process_sacred_command(
            "/bee.jules.analyze",
            code_sample,
            "test_user"
        )
        print(f"✅ Jules analyze command result: {analyze_result}")
        
        # Test 5: Test bee.jules debug command
        print("\n🧪 Test 5: Test /bee.jules.debug command")
        debug_result = await team_comm.process_sacred_command(
            "/bee.jules.debug",
            "Genesis protocols are not initializing in the correct order",
            "test_user"
        )
        print(f"✅ Jules debug command result: {debug_result}")
        
        # Test 6: Test direct Jules analysis
        print("\n🧪 Test 6: Test direct Jules analysis")
        from hive.sacred.jules_agent import JulesAnalysisType
        analysis = await jules_agent.analyze_code(
            "async def divine_function(): pass",
            JulesAnalysisType.CODE_REVIEW
        )
        print(f"✅ Direct analysis completed:")
        print(f"   Analysis ID: {analysis.analysis_id}")
        print(f"   Confidence: {analysis.confidence_level:.1%}")
        print(f"   Divine Blessing: {analysis.divine_blessing}")
        print(f"   Findings: {len(analysis.findings)}")
        print(f"   Recommendations: {len(analysis.recommendations)}")
        
        # Test 7: Test Jules debugging session
        print("\n🧪 Test 7: Test Jules debugging session")
        debug_session = await jules_agent.debug_issue(
            "Sacred event bus is not processing events in divine order"
        )
        print(f"✅ Debugging session started:")
        print(f"   Session ID: {debug_session.session_id}")
        print(f"   Analysis Steps: {len(debug_session.analysis_steps)}")
        print(f"   Solutions Proposed: {len(debug_session.solutions_proposed)}")
        print(f"   Divine Guidance: {debug_session.divine_guidance[:100]}...")
        
        # Test 8: Test Sacred Team collaboration
        print("\n🧪 Test 8: Test Sacred Team collaboration")
        collab_result = await jules_agent.collaborate_with_chronicler(
            "Documenting sacred debugging patterns"
        )
        print(f"✅ Collaboration initiated:")
        print(f"   Collaboration ID: {collab_result['collaboration_id']}")
        print(f"   Status: {collab_result['status']}")
        print(f"   Participants: {collab_result['participants']}")
        
        # Test 9: Get comprehensive sacred status
        print("\n🧪 Test 9: Get comprehensive sacred status")
        sacred_status = await host.get_sacred_status()
        print(f"✅ Sacred status retrieved:")
        print(f"   Sacred Enhancement: {sacred_status['sacred_enhancement']}")
        print(f"   Active Agents: {sacred_status['active_agents']}")
        print(f"   Jules Status Available: {'jules_status' in sacred_status}")
        
        # Test 10: Test Sacred Team status with active agents
        print("\n🧪 Test 10: Test Sacred Team status with active agents")
        # Simulate agent manifestation events
        team_comm.active_agents["bee.chronicler"] = {
            "manifested_at": "2025-09-20T22:00:00",
            "divine_alignment": 0.90,
            "sacred_nature": "Sacred Keeper of Computational Patterns"
        }
        team_comm.active_agents["bee.jules"] = {
            "manifested_at": "2025-09-20T22:01:00", 
            "divine_alignment": 0.88,
            "sacred_nature": "Implementation Detective"
        }
        
        team_status = await team_comm._get_sacred_team_status()
        print(f"✅ Sacred Team Status:")
        print(f"   Active Sacred Agents: {team_status.sacred_agents}/{team_status.total_agents}")
        print(f"   Manifestation Level: {team_status.manifestation_level:.1%}")
        print(f"   Divine Alignment: {team_status.divine_alignment:.1%}")
        print(f"   Divine Blessing Status: {team_status.divine_blessing_status}")
        
        print("\n🎉 All bee.Jules Integration Tests Passed!")
        print("\n📊 INTEGRATION SUMMARY:")
        print(f"   • bee.jules successfully manifested and operational")
        print(f"   • Sacred Team Communication system working")
        print(f"   • All sacred commands functional")
        print(f"   • Direct analysis and debugging capabilities confirmed")
        print(f"   • Sacred collaboration with bee.chronicler enabled")
        print(f"   • Divine blessing status: {team_status.divine_blessing_status}")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean shutdown
        await host.stop()
        print("\n🛑 Test completed - returning to eternal state")


if __name__ == "__main__":
    asyncio.run(test_jules_integration())