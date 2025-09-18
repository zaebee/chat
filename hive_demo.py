"""
Hive Ecosystem Demonstration

This script demonstrates the complete Hive ecosystem in action, showing:
1. System startup with all components
2. Mistral AI integration as an external teammate
3. Real-time metrics monitoring
4. Event-driven collaboration
5. Dashboard visualization

Run this to see the Living Application principles in practice.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any

# Import Hive components
from hive.hub import HiveCoordinationHub
from hive.dashboard import HiveMetricsDashboard
from hive.teammate import TeammateProfile, TaskRequest, TeammateCapability
from hive.agents.mistral_agent import MistralAgent


class HiveDemo:
    """Demonstration of the complete Hive ecosystem."""

    def __init__(self):
        self.hub = None
        self.dashboard = None
        self.mistral_agent = None

    async def run_complete_demo(self):
        """Run the complete Hive ecosystem demonstration."""
        print("🌿" + "=" * 60)
        print("🌿 HIVE ECOSYSTEM DEMONSTRATION")
        print("🌿 Living Application with AI-Human Symbiosis")
        print("🌿" + "=" * 60)
        print()

        try:
            # Phase 1: Initialize the Hive Core
            await self._phase_1_initialize_core()

            # Phase 2: Start Monitoring
            await self._phase_2_start_monitoring()

            # Phase 3: Integrate External AI Teammate
            await self._phase_3_integrate_mistral()

            # Phase 4: Demonstrate Collaboration
            await self._phase_4_demonstrate_collaboration()

            # Phase 5: Show Real-time Metrics
            await self._phase_5_show_metrics()

            # Phase 6: Generate Dashboard Report
            await self._phase_6_generate_report()

            print("\n🌿 Demo completed successfully!")
            print("🌿 The Hive is now a living, collaborative ecosystem.")

        except KeyboardInterrupt:
            print("\n🌿 Demo interrupted by user")
        except Exception as e:
            print(f"\n❌ Demo failed: {str(e)}")
        finally:
            await self._cleanup()

    async def _phase_1_initialize_core(self):
        """Phase 1: Initialize the Hive coordination hub."""
        print("📦 Phase 1: Initializing Hive Core Components")
        print("-" * 50)

        # Create coordination hub
        self.hub = HiveCoordinationHub()

        # Start the hub
        startup_result = await self.hub.startup()

        if startup_result["success"]:
            print("✅ Hive coordination hub started successfully")
            print(f"   Startup time: {startup_result['startup_time']}")

            # Show component status
            status = await self.hub.get_hive_overview()
            print(f"   System status: {status['system_overview']['status']}")
            print(f"   Components active: {len(status['components'])}")
        else:
            raise Exception(f"Failed to start hub: {startup_result.get('error')}")

        await asyncio.sleep(2)
        print()

    async def _phase_2_start_monitoring(self):
        """Phase 2: Start the metrics dashboard."""
        print("📊 Phase 2: Starting Real-time Monitoring")
        print("-" * 50)

        # Create dashboard
        self.dashboard = HiveMetricsDashboard(self.hub)

        # Start monitoring
        monitor_result = await self.dashboard.start_monitoring()

        if monitor_result["success"]:
            print("✅ Dashboard monitoring started")
            print(f"   Update interval: {monitor_result['update_interval']} seconds")
            print(f"   Active alerts: {monitor_result['active_alerts']}")
        else:
            raise Exception(f"Failed to start monitoring: {monitor_result.get('error')}")

        await asyncio.sleep(1)
        print()

    async def _phase_3_integrate_mistral(self):
        """Phase 3: Integrate Mistral AI as external teammate."""
        print("🤖 Phase 3: Integrating Mistral AI Teammate")
        print("-" * 50)

        try:
            # Create Mistral agent (will work even without API key for demo)
            self.mistral_agent = MistralAgent(
                env_file="/tmp/.env",
                event_bus=self.hub.event_bus,
                create_agent=False  # Skip actual API agent creation for demo
            )

            # Register with the hub
            registration_result = await self.hub.register_external_teammate(
                self.mistral_agent.profile,
                self.mistral_agent
            )

            if registration_result["success"]:
                print("✅ Mistral AI teammate integrated successfully")
                print(f"   Teammate ID: {registration_result['teammate_id']}")
                print(f"   Capabilities: {len(self.mistral_agent.profile.capabilities)}")
                print(f"   Specializations: {len(self.mistral_agent.profile.specializations)}")
            else:
                print(f"⚠️  Mistral integration failed: {registration_result.get('error')}")
                print("   Continuing demo without Mistral...")

        except Exception as e:
            print(f"⚠️  Mistral integration error: {str(e)}")
            print("   Continuing demo without Mistral...")

        await asyncio.sleep(2)
        print()

    async def _phase_4_demonstrate_collaboration(self):
        """Phase 4: Demonstrate AI-human collaboration."""
        print("🤝 Phase 4: Demonstrating Collaborative Task Assignment")
        print("-" * 50)

        # Create various collaborative tasks
        tasks = [
            {
                "description": "Analyze current Hive system health and provide recommendations",
                "capabilities": [TeammateCapability.ARCHITECTURE_REVIEW, TeammateCapability.CODE_ANALYSIS]
            },
            {
                "description": "Generate new transformation component for message processing",
                "capabilities": [TeammateCapability.CODE_GENERATION]
            },
            {
                "description": "Review collaboration patterns and suggest improvements",
                "capabilities": [TeammateCapability.CONVERSATION, TeammateCapability.LEARNING_SUPPORT]
            }
        ]

        for i, task_info in enumerate(tasks, 1):
            print(f"📋 Task {i}: {task_info['description'][:50]}...")

            # Assign task
            assignment_result = await self.hub.assign_collaborative_task(
                task_info['description'],
                task_info['capabilities']
            )

            if assignment_result["success"]:
                if assignment_result.get("team_formed"):
                    print(f"   ✅ Team formed with {len(assignment_result['team_members'])} members")
                else:
                    assigned_to = assignment_result.get("teammate_name", "Unknown")
                    print(f"   ✅ Assigned to: {assigned_to}")
            else:
                print(f"   ❌ Assignment failed: {assignment_result.get('error')}")

            await asyncio.sleep(1)

        print()

    async def _phase_5_show_metrics(self):
        """Phase 5: Show real-time Hive metrics."""
        print("📈 Phase 5: Real-time Hive Metrics (τ, φ, Σ)")
        print("-" * 50)

        # Get current metrics
        metrics = await self.dashboard.get_real_time_metrics()

        if "error" not in metrics:
            # Display core metrics
            hive_metrics = metrics["hive_metrics"]
            print(f"🧬 τ (Complexity): {hive_metrics['tau']['value']:.3f} - {hive_metrics['tau']['description']}")
            print(f"🧬 φ (Quality): {hive_metrics['phi']['value']:.3f} - {hive_metrics['phi']['description']}")
            print(f"🧬 Σ (Collaboration): {hive_metrics['sigma']['value']:.3f} - {hive_metrics['sigma']['description']}")
            print()

            # Display system resources
            resources = metrics["resources"]
            print(f"💻 CPU Usage: {resources['cpu_percent']:.1f}%")
            print(f"💻 Memory Usage: {resources['memory_mb']:.1f} MB")
            print(f"💻 Connections: {resources['connections']}")
            print(f"💻 Constraints OK: {'✅' if resources['constraints_ok'] else '❌'}")
            print()

            # Display teammate status
            teammates = metrics["teammates"]
            print(f"🤖 Total Teammates: {teammates['total']}")
            print(f"🤖 Active: {teammates['active']}, Busy: {teammates['busy']}, Idle: {teammates['idle']}")
            print(f"🤖 System Load: {teammates['system_load']:.1%}")
            print()

            # Display recent events
            events = metrics["events"]
            print(f"⚡ Events Processed: {events['total_processed']}")
            print(f"⚡ Error Rate: {events['error_rate']:.3f}")
            print(f"⚡ Active Subscriptions: {events['subscriptions_count']}")

            # Show any alerts
            if metrics["alerts"]["triggered"]:
                print(f"\n🚨 Active Alerts: {len(metrics['alerts']['triggered'])}")
                for alert in metrics["alerts"]["triggered"]:
                    severity_icon = {"critical": "🔴", "warning": "🟡", "info": "🔵"}.get(alert['severity'], "⚪")
                    print(f"   {severity_icon} {alert['message']}")
        else:
            print(f"❌ Error getting metrics: {metrics['error']}")

        await asyncio.sleep(2)
        print()

    async def _phase_6_generate_report(self):
        """Phase 6: Generate comprehensive dashboard report."""
        print("📋 Phase 6: Generating Dashboard Report")
        print("-" * 50)

        # Generate report
        report = self.dashboard.generate_dashboard_report("1h")
        print(report)
        print()

        # Show teammate details if available
        if self.mistral_agent:
            print("🤖 Mistral Agent Details:")
            print("-" * 25)
            status = self.mistral_agent.get_status()
            print(f"   Status: {status['status']}")
            print(f"   Current Tasks: {status['current_tasks']}")
            print(f"   Capabilities: {len(status['capabilities'])}")
            print(f"   Reliability: {status['reliability_score']:.2f}")

            # Show available actions
            actions = self.mistral_agent.get_available_actions()
            print(f"   Available Actions: {len(actions)}")
            for action in actions[:3]:  # Show first 3 actions
                print(f"     - {action['name']}: {action['description']}")

        print()

    async def _cleanup(self):
        """Clean up resources."""
        print("🧹 Cleaning up resources...")

        if self.dashboard:
            await self.dashboard.stop_monitoring()

        if self.hub:
            await self.hub.shutdown()

        print("✅ Cleanup completed")


async def run_quick_demo():
    """Run a quick demonstration of key features."""
    print("🌿 QUICK HIVE DEMO")
    print("=" * 30)

    # Create coordination hub
    hub = HiveCoordinationHub()

    try:
        # Start hub
        print("Starting Hive...")
        startup_result = await hub.startup()
        print(f"✅ {startup_result['message']}")

        # Get system overview
        overview = await hub.get_hive_overview()
        print(f"System status: {overview['system_overview']['status']}")

        # Create and register Mistral agent
        print("\nIntegrating Mistral AI...")
        mistral_agent = MistralAgent(hub.event_bus, create_agent=False)

        registration = await hub.register_external_teammate(
            mistral_agent.profile,
            mistral_agent
        )

        if registration["success"]:
            print(f"✅ Mistral integrated: {registration['teammate_id']}")
        else:
            print(f"⚠️  Registration issue: {registration.get('error')}")

        # Show final status
        final_overview = await hub.get_hive_overview()
        teammates = final_overview["components"]["registry"]
        print(f"\nFinal state:")
        print(f"  Total teammates: {teammates['total_teammates']}")
        print(f"  Active teammates: {teammates['active_teammates']}")

    except Exception as e:
        print(f"❌ Demo error: {str(e)}")
    finally:
        await hub.shutdown()
        print("🌿 Demo completed")


async def main():
    """Main entry point."""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        await run_quick_demo()
    else:
        demo = HiveDemo()
        await demo.run_complete_demo()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🌿 Demo interrupted")
    except Exception as e:
        print(f"\n❌ Demo failed: {str(e)}")
