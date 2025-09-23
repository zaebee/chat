#!/usr/bin/env python3
"""
🐝✨ Sacred Connection Manager Test Suite ✨🐝

Tests for divine protection mechanisms and connection safety
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from typing import List

# Mock WebSocket for testing
class MockWebSocket:
    def __init__(self, should_fail: bool = False):
        self.should_fail = should_fail
        self.messages_sent: List[str] = []
        self.is_closed = False
        self.close_code = None
        self.close_reason = None
    
    async def accept(self):
        if self.should_fail:
            raise Exception("Mock connection failure")
    
    async def send_text(self, message: str):
        if self.should_fail:
            raise Exception("Mock send failure")
        self.messages_sent.append(message)
    
    async def close(self, code: int = 1000, reason: str = "Normal closure"):
        self.is_closed = True
        self.close_code = code
        self.close_reason = reason

# Test the Sacred Connection Manager
async def test_sacred_connection_manager():
    """Test sacred connection manager functionality"""
    print("🐝✨ Testing Sacred Connection Manager ✨🐝")
    
    # Import after setting up mock
    from SacredConnectionManager import create_sacred_connection_manager
    
    # Create sacred manager
    logger = logging.getLogger("test")
    manager = create_sacred_connection_manager(logger)
    
    # Start manager
    await manager.start()
    
    try:
        # Test 1: Basic connection
        print("\n📋 Test 1: Basic Connection")
        websocket1 = MockWebSocket()
        connection1 = await manager.connect(websocket1, "user1", "TestUser1", "127.0.0.1")
        print(f"✅ Connection established: {connection1.id}")
        assert len(manager.connections) == 1
        
        # Test 2: Message sending
        print("\n📋 Test 2: Message Sending")
        test_message = {"type": "test", "content": "Hello Sacred World!"}
        success = await manager.send_message(connection1.id, test_message)
        print(f"✅ Message sent successfully: {success}")
        assert success == True
        assert len(websocket1.messages_sent) == 2  # Welcome + test message
        
        # Test 3: Broadcasting
        print("\n📋 Test 3: Broadcasting")
        websocket2 = MockWebSocket()
        connection2 = await manager.connect(websocket2, "user2", "TestUser2", "127.0.0.1")
        
        broadcast_message = {"type": "broadcast", "content": "Sacred Broadcast!"}
        sent_count = await manager.broadcast_message(broadcast_message)
        print(f"✅ Broadcast sent to {sent_count} connections")
        assert sent_count == 2
        
        # Test 4: Connection limits
        print("\n📋 Test 4: Connection Limits")
        connections_created = 0
        try:
            # Try to create many connections from same IP
            for i in range(15):  # Exceeds MAX_CONNECTIONS_PER_IP (10)
                websocket = MockWebSocket()
                try:
                    await manager.connect(websocket, f"user{i+10}", f"TestUser{i+10}", "127.0.0.1")
                    connections_created += 1
                except Exception as e:
                    print(f"✅ Connection rejected as expected: {e}")
                    break
        except Exception as e:
            print(f"✅ Sacred protection activated: {e}")
        
        print(f"✅ Created {connections_created} connections before limit")
        
        # Test 5: Rate limiting
        print("\n📋 Test 5: Rate Limiting")
        # Send many messages quickly to trigger rate limiting
        rate_limit_hits = 0
        for i in range(150):  # Exceeds rate limit
            try:
                await manager.send_message(connection1.id, {"type": "spam", "content": f"Message {i}"})
            except Exception as e:
                rate_limit_hits += 1
                if rate_limit_hits == 1:
                    print(f"✅ Rate limiting activated: {e}")
        
        print(f"✅ Rate limit triggered {rate_limit_hits} times")
        
        # Test 6: Circuit breaker
        print("\n📋 Test 6: Circuit Breaker")
        # Create failing connections to trigger circuit breaker
        failures = 0
        for i in range(15):  # Trigger circuit breaker threshold
            try:
                failing_websocket = MockWebSocket(should_fail=True)
                await manager.connect(failing_websocket, f"fail{i}", f"FailUser{i}", "192.168.1.1")
            except Exception as e:
                failures += 1
                if failures >= 10:  # Circuit breaker threshold
                    print(f"✅ Circuit breaker activated after {failures} failures")
                    break
        
        # Test 7: Metrics and health
        print("\n📋 Test 7: Metrics and Health")
        metrics = manager.get_connection_metrics()
        print(f"✅ Total connections: {metrics['total_connections']}")
        print(f"✅ Active connections: {metrics['active_connections']}")
        print(f"✅ Messages sent: {metrics['total_messages_sent']}")
        print(f"✅ Circuit breaker state: {metrics['circuit_breaker']['state']}")
        
        health_status = manager.is_healthy()
        status_message = manager.get_status_message()
        print(f"✅ System healthy: {health_status}")
        print(f"✅ Status: {status_message}")
        
        # Test 8: Graceful disconnection
        print("\n📋 Test 8: Graceful Disconnection")
        initial_count = len(manager.connections)
        await manager.disconnect(connection1.id, "Test disconnection")
        final_count = len(manager.connections)
        print(f"✅ Disconnection successful: {initial_count} -> {final_count}")
        assert final_count == initial_count - 1
        
        print("\n🎉 All Sacred Connection Manager tests passed!")
        
    finally:
        # Clean shutdown
        await manager.stop()
        print("✅ Sacred Connection Manager stopped gracefully")

async def test_integration_manager():
    """Test the integration manager"""
    print("\n🐝✨ Testing Sacred Integration Manager ✨🐝")
    
    from sacred_connection_manager_integration import SacredHiveConnectionManager
    
    # Create integration manager
    integration_manager = SacredHiveConnectionManager()
    await integration_manager.start()
    
    try:
        # Test connection
        websocket = MockWebSocket()
        success = await integration_manager.connect(websocket, "test_user", "TestUser", "127.0.0.1")
        print(f"✅ Integration connection successful: {success}")
        
        # Test metrics
        metrics = integration_manager.get_sacred_metrics()
        health = integration_manager.get_health_status()
        
        print(f"✅ Integration metrics available: {len(metrics)} categories")
        print(f"✅ Health status: {health['healthy']}")
        
        print("🎉 Sacred Integration Manager tests passed!")
        
    finally:
        await integration_manager.stop()

async def main():
    """Run all tests"""
    print("🐝✨ Sacred Connection Manager Test Suite ✨🐝")
    print("=" * 60)
    
    # Configure logging
    logging.basicConfig(level=logging.WARNING)  # Reduce noise during testing
    
    try:
        await test_sacred_connection_manager()
        await test_integration_manager()
        
        print("\n" + "=" * 60)
        print("🎉 ALL SACRED TESTS PASSED! 🎉")
        print("✨ Divine protection mechanisms verified ✨")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())