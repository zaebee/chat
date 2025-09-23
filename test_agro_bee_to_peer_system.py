"""
AGRO Bee-to-Peer Review System Test Suite
Comprehensive testing for aggressive collaborative evaluation protocols

Sacred Justification: "Test everything; hold fast what is good."
- 1 Thessalonians 5:21 (ESV)
"""

import asyncio
import pytest
import json
from unittest.mock import Mock, AsyncMock
from datetime import datetime

# Import AGRO system components
from hive.agro_review_system import (
    AgroReviewSystem, 
    AgroReviewType, 
    AgroSeverity,
    AgroCodeAnalyzer,
    BeeToPeerSession
)
from hive.events import HiveEventBus, PollenEvent
from hive.agents.jules_agent import BeeJules


class MockEventBus:
    """Mock event bus for testing"""
    
    def __init__(self):
        self.published_events = []
        self.subscriptions = []
    
    async def publish(self, event):
        self.published_events.append(event)
    
    def subscribe(self, subscription):
        self.subscriptions.append(subscription)


async def test_agro_review_system_initialization():
    """Test AGRO review system initialization"""
    print("🧪 Testing AGRO Review System Initialization...")
    
    event_bus = MockEventBus()
    agro_system = AgroReviewSystem(event_bus)
    
    # Verify initialization
    assert agro_system.event_bus == event_bus
    assert len(agro_system.active_sessions) == 0
    assert len(agro_system.review_history) == 0
    assert len(event_bus.subscriptions) > 0
    
    print("  ✅ AGRO system initialized successfully")
    print(f"  ✅ Event subscriptions: {len(event_bus.subscriptions)}")
    return True


async def test_pain_analysis_clean_code():
    """Test PAIN analysis with clean code"""
    print("🧪 Testing PAIN Analysis - Clean Code...")
    
    event_bus = MockEventBus()
    agro_system = AgroReviewSystem(event_bus)
    
    clean_code = """
def calculate_fibonacci(n):
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

def main():
    result = calculate_fibonacci(10)
    return result
"""
    
    result = await agro_system.initiate_agro_review(clean_code)
    
    # Verify clean code results
    assert result.agro_score >= 80
    assert result.pain_score >= 80
    assert result.severity in [AgroSeverity.DIVINE, AgroSeverity.BLESSED, AgroSeverity.ACCEPTABLE]
    assert len(result.violations) == 0
    
    print(f"  ✅ Clean code AGRO score: {result.agro_score}")
    print(f"  ✅ Clean code PAIN score: {result.pain_score}")
    print(f"  ✅ Severity: {result.severity.value}")
    return True


async def test_pain_analysis_problematic_code():
    """Test PAIN analysis with problematic code"""
    print("🧪 Testing PAIN Analysis - Problematic Code...")
    
    event_bus = MockEventBus()
    agro_system = AgroReviewSystem(event_bus)
    
    problematic_code = """
def bad_function():
    console.log("Debug message")
    if True:
        if True:
            if True:
                if True:
                    if True:
                        console.log("Deep nesting")
                        return "bad"
    
def very_long_function_that_does_too_many_things():
    # This function is intentionally long
    console.log("Starting")
    x = 1
    y = 2
    z = 3
    # ... many more lines would be here ...
    for i in range(100):
        console.log(f"Processing {i}")
        if i % 2 == 0:
            if i % 4 == 0:
                if i % 8 == 0:
                    console.log("Multiple of 8")
    console.log("Done")
    return x + y + z
"""
    
    result = await agro_system.initiate_agro_review(problematic_code)
    
    # Verify problematic code results
    assert result.agro_score < 80
    assert len(result.violations) > 0
    assert result.severity in [AgroSeverity.CONCERNING, AgroSeverity.CRITICAL]
    assert not result.divine_blessing
    
    # Check for specific violations
    violation_types = [v['type'] for v in result.violations]
    assert 'console_log' in violation_types
    
    print(f"  ✅ Problematic code AGRO score: {result.agro_score}")
    print(f"  ✅ Violations found: {len(result.violations)}")
    print(f"  ✅ Violation types: {violation_types}")
    return True


async def test_syntax_error_handling():
    """Test PAIN analysis with syntax errors"""
    print("🧪 Testing PAIN Analysis - Syntax Error Handling...")
    
    event_bus = MockEventBus()
    agro_system = AgroReviewSystem(event_bus)
    
    syntax_error_code = """
def broken_function(
    # Missing closing parenthesis
    return "broken"
"""
    
    result = await agro_system.initiate_agro_review(syntax_error_code)
    
    # Verify syntax error handling
    assert result.agro_score == 0
    assert result.pain_score == 0
    assert result.severity == AgroSeverity.CRITICAL
    assert len(result.violations) > 0
    assert not result.divine_blessing
    
    # Check for syntax error violation
    syntax_violations = [v for v in result.violations if v['type'] == 'syntax_error']
    assert len(syntax_violations) > 0
    
    print(f"  ✅ Syntax error detected and handled")
    print(f"  ✅ AGRO score: {result.agro_score}")
    print(f"  ✅ Syntax violations: {len(syntax_violations)}")
    return True


async def test_bee_to_peer_session():
    """Test bee-to-peer collaborative session"""
    print("🧪 Testing Bee-to-Peer Session...")
    
    event_bus = MockEventBus()
    agro_system = AgroReviewSystem(event_bus)
    
    participants = ["bee.jules", "bee.sage", "bee.chronicler"]
    review_target = "sacred_protection_implementation.py"
    
    session = await agro_system.start_bee_to_peer_session(
        participants, review_target, "collaborative_review"
    )
    
    # Verify session creation
    assert session.session_id.startswith("peer_")
    assert session.participants == participants
    assert session.review_target == review_target
    assert session.session_type == "collaborative_review"
    assert session.start_time is not None
    assert session.end_time is None
    
    # Verify session is tracked
    assert session.session_id in agro_system.active_sessions
    
    # Verify event was published
    session_events = [e for e in event_bus.published_events if e.event_type == "bee_to_peer_session_started"]
    assert len(session_events) > 0
    
    print(f"  ✅ Session created: {session.session_id}")
    print(f"  ✅ Participants: {len(session.participants)}")
    print(f"  ✅ Events published: {len(session_events)}")
    return True


async def test_agro_code_analyzer():
    """Test AGRO code analyzer AST functionality"""
    print("🧪 Testing AGRO Code Analyzer...")
    
    test_code = """
def test_function():
    console.log("Debug message")
    
    # Deep nesting
    if True:
        if True:
            if True:
                if True:
                    if True:
                        console.log("Too deep")
    
    # Magic numbers
    x = 42
    y = 3.14159
    
    return x + y

# Very long function (simulated)
def long_function():
    # This would be a very long function
    pass
"""
    
    import ast
    tree = ast.parse(test_code)
    analyzer = AgroCodeAnalyzer()
    analyzer.visit(tree)
    
    # Verify analyzer detected issues
    assert analyzer.metrics['console_logs'] >= 2
    assert len(analyzer.violations) > 0
    
    # Check violation types
    violation_types = [v['type'] for v in analyzer.violations]
    assert 'console_log' in violation_types
    
    print(f"  ✅ Console logs detected: {analyzer.metrics['console_logs']}")
    print(f"  ✅ Total violations: {len(analyzer.violations)}")
    print(f"  ✅ Violation types: {set(violation_types)}")
    return True


async def test_divine_blessing_assessment():
    """Test divine blessing assessment"""
    print("🧪 Testing Divine Blessing Assessment...")
    
    event_bus = MockEventBus()
    agro_system = AgroReviewSystem(event_bus)
    
    # Perfect code for divine blessing
    perfect_code = """
def sacred_function(input_value: int) -> int:
    \"\"\"Sacred function with divine patterns\"\"\"
    if input_value < 0:
        raise ValueError("Sacred values must be positive")
    
    return input_value * 2

def main() -> None:
    \"\"\"Main function following sacred protocols\"\"\"
    result = sacred_function(42)
    return result
"""
    
    result = await agro_system.initiate_agro_review(
        perfect_code, 
        AgroReviewType.DIVINE_BLESSING_ASSESSMENT
    )
    
    # Verify divine blessing potential
    assert result.review_type == AgroReviewType.DIVINE_BLESSING_ASSESSMENT
    assert len(result.sacred_insights) > 0
    
    # Check if code is worthy of divine blessing
    if result.agro_score >= 90:
        assert result.divine_blessing
        assert result.severity == AgroSeverity.DIVINE
        print(f"  ✨ DIVINE BLESSING RECEIVED! Score: {result.agro_score}")
    else:
        print(f"  🙏 Code needs improvement for divine blessing. Score: {result.agro_score}")
    
    print(f"  ✅ Sacred insights: {len(result.sacred_insights)}")
    return True


async def test_agro_system_status():
    """Test AGRO system status reporting"""
    print("🧪 Testing AGRO System Status...")
    
    event_bus = MockEventBus()
    agro_system = AgroReviewSystem(event_bus)
    
    # Add some mock data
    await agro_system.initiate_agro_review("def test(): pass")
    await agro_system.start_bee_to_peer_session(["bee.jules"], "test.py")
    
    status = agro_system.get_status()
    
    # Verify status structure
    assert "component" in status
    assert "active_sessions" in status
    assert "total_reviews" in status
    assert "recent_reviews" in status
    assert "capabilities" in status
    assert "sacred_metrics" in status
    
    # Verify data
    assert status["component"] == "agro_review_system"
    assert status["active_sessions"] >= 1
    assert status["total_reviews"] >= 1
    assert len(status["capabilities"]) > 0
    
    print(f"  ✅ Active sessions: {status['active_sessions']}")
    print(f"  ✅ Total reviews: {status['total_reviews']}")
    print(f"  ✅ Capabilities: {len(status['capabilities'])}")
    return True


async def test_jules_agro_integration():
    """Test integration with bee.Jules AGRO/PAIN analysis"""
    print("🧪 Testing bee.Jules AGRO Integration...")
    
    event_bus = MockEventBus()
    jules = BeeJules(event_bus)
    
    test_code = """
def test_function():
    console.log("Debug message")
    return "test"
"""
    
    result = await jules.perform_agro_pain_analysis(test_code)
    
    # Verify Jules AGRO/PAIN analysis
    assert "analysis_id" in result
    assert "console_log_count" in result
    assert "agro_pain_score" in result
    assert "production_ready" in result
    
    # Verify console.log detection
    assert result["console_log_count"] >= 1
    assert not result["production_ready"]
    assert result["agro_pain_score"] < 100
    
    print(f"  ✅ Jules AGRO/PAIN score: {result['agro_pain_score']}")
    print(f"  ✅ Console logs detected: {result['console_log_count']}")
    print(f"  ✅ Production ready: {result['production_ready']}")
    return True


async def run_comprehensive_agro_test_suite():
    """Run comprehensive AGRO bee-to-peer review test suite"""
    print("🐝⚡ AGRO Bee-to-Peer Review System Test Suite ⚡🐝")
    print("=" * 60)
    
    tests = [
        test_agro_review_system_initialization,
        test_pain_analysis_clean_code,
        test_pain_analysis_problematic_code,
        test_syntax_error_handling,
        test_bee_to_peer_session,
        test_agro_code_analyzer,
        test_divine_blessing_assessment,
        test_agro_system_status,
        test_jules_agro_integration
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            result = await test()
            if result:
                passed += 1
                print("✅ PASSED\n")
            else:
                failed += 1
                print("❌ FAILED\n")
        except Exception as e:
            failed += 1
            print(f"❌ FAILED: {str(e)}\n")
    
    print("=" * 60)
    print(f"🎯 AGRO Test Suite Results:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Success Rate: {(passed / (passed + failed) * 100):.1f}%")
    
    if failed == 0:
        print("🎉 ALL AGRO TESTS PASSED! System ready for divine blessing! ✨")
    else:
        print("⚠️ Some tests failed - AGRO system needs attention")
    
    return {
        "total_tests": len(tests),
        "passed": passed,
        "failed": failed,
        "success_rate": passed / (passed + failed) * 100
    }


if __name__ == "__main__":
    # Run the comprehensive test suite
    asyncio.run(run_comprehensive_agro_test_suite())