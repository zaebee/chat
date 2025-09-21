"""
Hive Integration Example

This script shows how to integrate the new Hive ecosystem with the existing
chat application, demonstrating how to bridge legacy systems with the new
Living Application architecture.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any, List

from hive.hub import HiveCoordinationHub
from hive.dashboard import HiveMetricsDashboard
from hive.teammate import TeammateProfile, TeammateCapability
from hive.agents.mistral_agent import MistralAgent
from hive.events import PollenEvent


class ChatToHiveBridge:
    """
    Bridge between the legacy chat system and the new Hive ecosystem.

    This demonstrates how to gradually migrate existing systems to the
    Living Application architecture without breaking existing functionality.
    """

    def __init__(self):
        self.hub = None
        self.dashboard = None
        self.chat_message_count = 0

    async def initialize_hive_backend(self):
        """Initialize the Hive ecosystem as a backend service."""
        print("🌿 Initializing Hive ecosystem backend...")

        # Create and start coordination hub
        self.hub = HiveCoordinationHub()
        startup_result = await self.hub.startup()

        if not startup_result["success"]:
            raise Exception(f"Failed to start Hive: {startup_result.get('error')}")

        # Start metrics dashboard
        self.dashboard = HiveMetricsDashboard(self.hub)
        await self.dashboard.start_monitoring()

        # Subscribe to chat-related events
        await self._setup_chat_event_handlers()

        print("✅ Hive backend initialized successfully")
        return startup_result

    async def _setup_chat_event_handlers(self):
        """Set up event handlers for chat integration."""
        from hive.events import EventSubscription

        async def handle_chat_events(event: PollenEvent):
            await self._process_chat_event(event)

        # Subscribe to message events
        chat_subscription = EventSubscription(
            event_types=["message_sent", "user_joined", "user_left"],
            callback=handle_chat_events
        )

        self.hub.event_bus.subscribe(chat_subscription)

    async def _process_chat_event(self, event: PollenEvent):
        """Process chat events and provide Hive intelligence."""
        if event.event_type == "message_sent":
            self.chat_message_count += 1

            # Analyze message for collaboration opportunities
            message_text = event.payload.get("text", "")

            if any(keyword in message_text.lower() for keyword in ["help", "error", "problem"]):
                # User needs assistance - could dispatch to AI teammates
                await self.hub.event_bus.publish_system_event(
                    "assistance_needed",
                    {
                        "source": "chat_message",
                        "message": message_text,
                        "user_id": event.payload.get("sender_id"),
                        "timestamp": datetime.now().isoformat()
                    }
                )

    async def add_mistral_teammate(self):
        """Add Mistral AI as a chat assistant teammate."""
        print("🤖 Adding Mistral AI teammate...")

        try:
            # Create Mistral agent
            mistral_agent = MistralAgent(
                event_bus=self.hub.event_bus,
                create_agent=False  # Skip API creation for demo
            )

            # Register with Hive
            registration_result = await self.hub.register_external_teammate(
                mistral_agent.profile,
                mistral_agent
            )

            if registration_result["success"]:
                print(f"✅ Mistral teammate added: {registration_result['teammate_id']}")
                return mistral_agent
            else:
                print(f"❌ Failed to add Mistral: {registration_result.get('error')}")
                return None

        except Exception as e:
            print(f"❌ Error adding Mistral: {str(e)}")
            return None

    def simulate_chat_activity(self, num_messages: int = 5):
        """Simulate chat activity to show Hive metrics in action."""
        print(f"💬 Simulating {num_messages} chat messages...")

        # Simulate various types of chat messages
        messages = [
            {"text": "Hello everyone!", "sender": "Alice", "type": "greeting"},
            {"text": "I need help with Python functions", "sender": "Bob", "type": "help_request"},
            {"text": "Here's a code example: def hello(): print('hi')", "sender": "Charlie", "type": "code_sharing"},
            {"text": "Thanks for the help! 🙏", "sender": "Bob", "type": "gratitude"},
            {"text": "What's the weather like today?", "sender": "Diana", "type": "casual"}
        ]

        for i, msg in enumerate(messages[:num_messages]):
            # Publish message event
            asyncio.create_task(self.hub.event_bus.publish_message_event(
                "sent",
                f"msg_{i}",
                {
                    "text": msg["text"],
                    "sender_name": msg["sender"],
                    "sender_id": f"user_{msg['sender'].lower()}",
                    "message_type": msg["type"],
                    "timestamp": datetime.now().isoformat()
                }
            ))

    async def get_hive_insights(self) -> Dict[str, Any]:
        """Get insights from the Hive about chat activity."""
        if not self.dashboard:
            return {"error": "Dashboard not initialized"}

        # Get current metrics
        metrics = await self.dashboard.get_real_time_metrics()

        # Get teammate status
        teammate_details = await self.dashboard.get_teammate_details()

        return {
            "chat_activity": {
                "messages_processed": self.chat_message_count,
                "active_teammates": teammate_details.get("total_count", 0)
            },
            "hive_metrics": metrics.get("hive_metrics", {}),
            "system_health": metrics.get("system_status", "unknown"),
            "collaboration_score": metrics.get("hive_metrics", {}).get("sigma", {}).get("value", 0.0),
            "recommendations": self._generate_chat_recommendations(metrics)
        }

    def _generate_chat_recommendations(self, metrics: Dict[str, Any]) -> List[str]:
        """Generate recommendations for improving chat collaboration."""
        recommendations = []

        if not metrics:
            return ["Enable Hive metrics monitoring for insights"]

        # Analyze collaboration efficiency
        sigma = metrics.get("hive_metrics", {}).get("sigma", {}).get("value", 0.0)

        if sigma < 0.5:
            recommendations.append("Low collaboration efficiency detected - consider adding AI assistants")
        elif sigma < 0.7:
            recommendations.append("Moderate collaboration - add specialized AI teammates for specific topics")
        else:
            recommendations.append("Good collaboration efficiency - system is working well")

        # Analyze system complexity
        tau = metrics.get("hive_metrics", {}).get("tau", {}).get("value", 0.0)

        if tau > 3.0:
            recommendations.append("System complexity is high - consider simplifying chat workflows")
        elif tau > 1.5:
            recommendations.append("Monitor system complexity - ensure chat features remain intuitive")

        # Check teammate availability
        teammates = metrics.get("teammates", {})
        if teammates.get("total", 0) == 0:
            recommendations.append("No AI teammates available - add assistants to improve user experience")

        return recommendations

    async def shutdown(self):
        """Gracefully shutdown the Hive backend."""
        print("🧹 Shutting down Hive backend...")

        if self.dashboard:
            await self.dashboard.stop_monitoring()

        if self.hub:
            await self.hub.shutdown()

        print("✅ Hive backend shutdown complete")


async def demo_integration():
    """Demonstrate Hive integration with chat system."""
    print("🌿 HIVE + CHAT INTEGRATION DEMO")
    print("=" * 40)

    bridge = ChatToHiveBridge()

    try:
        # Step 1: Initialize Hive backend
        await bridge.initialize_hive_backend()

        # Step 2: Add AI teammate
        mistral = await bridge.add_mistral_teammate()

        # Step 3: Simulate chat activity
        bridge.simulate_chat_activity(3)

        # Wait a moment for event processing
        await asyncio.sleep(2)

        # Step 4: Get Hive insights
        insights = await bridge.get_hive_insights()

        # Step 5: Display results
        print("\n📊 HIVE INSIGHTS FOR CHAT SYSTEM")
        print("-" * 35)
        print(f"Chat Messages Processed: {insights['chat_activity']['messages_processed']}")
        print(f"Active AI Teammates: {insights['chat_activity']['active_teammates']}")
        print(f"System Health: {insights['system_health']}")
        print(f"Collaboration Score: {insights['collaboration_score']:.2f}")

        print("\n💡 RECOMMENDATIONS:")
        for i, rec in enumerate(insights['recommendations'], 1):
            print(f"  {i}. {rec}")

        # Step 6: Show Hive metrics
        if 'hive_metrics' in insights:
            metrics = insights['hive_metrics']
            print(f"\n🧬 HIVE METRICS:")
            if 'tau' in metrics:
                print(f"  τ (Complexity): {metrics['tau']['value']:.3f}")
            if 'phi' in metrics:
                print(f"  φ (Quality): {metrics['phi']['value']:.3f}")
            if 'sigma' in metrics:
                print(f"  Σ (Collaboration): {metrics['sigma']['value']:.3f}")

        print("\n✨ Integration demonstrates how the Hive ecosystem can enhance")
        print("   existing chat applications with AI-powered insights and collaboration!")

    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
    finally:
        await bridge.shutdown()


if __name__ == "__main__":
    asyncio.run(demo_integration())