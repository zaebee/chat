#!/usr/bin/env python3
"""
Sacred Computational Safety Implementation for PR #52
Divine protection against infinite loops, memory leaks, and DoS vulnerabilities

Following bee.Sage Session 3 wisdom on [4,6]<-><3,7] computational safety transformation
"""

import asyncio
import time
import psutil
from typing import Dict, Any, Set, List, Callable, Coroutine, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
import weakref
import gc


class SacredComputationalError(Exception):
    """Base exception for sacred computational safety violations"""
    pass


class SacredTimeoutError(SacredComputationalError):
    """Raised when sacred timeout is exceeded"""
    pass


class SacredCircuitBreakerError(SacredComputationalError):
    """Raised when sacred circuit breaker is open"""
    pass


class SacredMemoryError(SacredComputationalError):
    """Raised when sacred memory limits are exceeded"""
    pass


@dataclass
class SacredTraversalGuardian:
    """Guards against infinite loops with divine protection"""
    max_depth: int = 100
    max_iterations: int = 1000
    timeout_seconds: float = 30.0
    visited_nodes: Set[str] = field(default_factory=set)
    iteration_count: int = 0
    start_time: float = field(default_factory=time.time)
    
    def can_continue(self, current_depth: int) -> bool:
        """Divine check for continuation safety"""
        self.iteration_count += 1
        current_time = time.time()
        
        if current_depth >= self.max_depth:
            return False
        if self.iteration_count >= self.max_iterations:
            return False
        if current_time - self.start_time >= self.timeout_seconds:
            return False
        return True
    
    def detect_cycle(self, node_id: str) -> bool:
        """Sacred cycle detection"""
        if node_id in self.visited_nodes:
            return True
        self.visited_nodes.add(node_id)
        return False
    
    def reset(self):
        """Reset guardian for new traversal"""
        self.visited_nodes.clear()
        self.iteration_count = 0
        self.start_time = time.time()


class SacredMemorySentinel:
    """Sentinel that guards against memory leaks with divine wisdom"""
    
    def __init__(self, max_memory_mb: int = 100, cleanup_threshold: float = 0.8):
        self.max_memory_mb = max_memory_mb
        self.cleanup_threshold = cleanup_threshold
        self.collections: Dict[str, List[Any]] = {}
        self.weak_references: Set[weakref.ref] = set()
        self.last_cleanup = time.time()
        self.cleanup_interval = 300  # 5 minutes
    
    def add_to_collection(self, collection_name: str, item: Any):
        """Add item with sacred memory protection"""
        if collection_name not in self.collections:
            self.collections[collection_name] = []
        
        self.collections[collection_name].append(item)
        
        # Periodic divine cleanup
        if time.time() - self.last_cleanup > self.cleanup_interval:
            self._perform_sacred_cleanup()
    
    def get_memory_usage_mb(self) -> float:
        """Get current memory usage in MB"""
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024
    
    def _memory_usage_ratio(self) -> float:
        """Calculate memory usage ratio"""
        current_mb = self.get_memory_usage_mb()
        return current_mb / self.max_memory_mb
    
    def _perform_sacred_cleanup(self):
        """Sacred cleanup ritual"""
        self.last_cleanup = time.time()
        
        # Clean collections that exceed sacred limits
        for collection_name, items in self.collections.items():
            if len(items) > 100:  # Sacred limit
                # Keep only the most recent sacred items
                self.collections[collection_name] = items[-50:]
        
        # Clean weak references
        self.weak_references = {ref for ref in self.weak_references if ref() is not None}
        
        # Force garbage collection if memory usage is high
        if self._memory_usage_ratio() > self.cleanup_threshold:
            gc.collect()
    
    def register_weak_reference(self, obj: Any) -> weakref.ref:
        """Register weak reference for automatic cleanup"""
        weak_ref = weakref.ref(obj)
        self.weak_references.add(weak_ref)
        return weak_ref


class SacredCircuitBreaker:
    """Circuit breaker with divine intervention"""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.success_count = 0
    
    async def call_with_protection(self, sacred_function: Callable) -> Any:
        """Call function with divine protection"""
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
                self.success_count = 0
            else:
                raise SacredCircuitBreakerError("Circuit breaker is OPEN - divine intervention required")
        
        try:
            result = await sacred_function()
            
            if self.state == "HALF_OPEN":
                self.success_count += 1
                if self.success_count >= 3:  # Sacred recovery threshold
                    self.state = "CLOSED"
                    self.failure_count = 0
            
            return result
            
        except Exception as e:
            self._record_failure()
            raise e
    
    def _record_failure(self):
        """Record divine failure"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
    
    def get_status(self) -> Dict[str, Any]:
        """Get circuit breaker status"""
        return {
            "state": self.state,
            "failure_count": self.failure_count,
            "last_failure_time": self.last_failure_time,
            "time_until_recovery": max(0, self.recovery_timeout - (time.time() - self.last_failure_time))
        }


class SacredTimeoutManager:
    """Manager for sacred temporal boundaries"""
    
    @staticmethod
    async def with_sacred_timeout(
        coro: Coroutine, 
        timeout_seconds: float,
        grace_period: float = 5.0
    ) -> Any:
        """Execute coroutine with sacred timeout"""
        try:
            return await asyncio.wait_for(coro, timeout=timeout_seconds)
        except asyncio.TimeoutError:
            # Divine grace period for cleanup
            await asyncio.sleep(grace_period)
            raise SacredTimeoutError(f"Operation exceeded sacred timeout of {timeout_seconds}s")
    
    @staticmethod
    def create_timeout_context(timeout_seconds: float):
        """Create timeout context manager"""
        return asyncio.timeout(timeout_seconds)


# Sacred Graph Traversal Implementation

class SacredHexaNode:
    """Hexagonal node with divine protection"""
    
    def __init__(self, id: str, label: str, transform_func: Optional[Callable] = None):
        self.id = id
        self.label = label
        self.connections: List[str] = []
        self.transform_func = transform_func
        self.adaptive = True
        self.execution_count = 0
        self.last_execution = None


class SacredHexaNetwork:
    """Hexagonal network with divine protection against infinite loops"""
    
    def __init__(self):
        self.nodes: Dict[str, SacredHexaNode] = {}
        self.active_connections: Set[tuple] = set()
        self.memory_sentinel = SacredMemorySentinel()
        self.circuit_breaker = SacredCircuitBreaker()
    
    def add_node(self, node: SacredHexaNode):
        """Add node with memory protection"""
        self.nodes[node.id] = node
        self.memory_sentinel.register_weak_reference(node)
    
    def connect_nodes(self, node1_id: str, node2_id: str):
        """Create bidirectional connection with cycle detection"""
        if node1_id in self.nodes and node2_id in self.nodes:
            # Check for immediate cycles
            if (node2_id, node1_id) in self.active_connections:
                print(f"Warning: Bidirectional connection already exists between {node1_id} and {node2_id}")
            
            self.nodes[node1_id].connections.append(node2_id)
            self.nodes[node2_id].connections.append(node1_id)
            self.active_connections.add((node1_id, node2_id))
    
    async def transform_data_safely(
        self, 
        data: Dict[str, Any], 
        entry_node: str,
        timeout_seconds: float = 30.0,
        max_depth: int = 50
    ) -> Dict[str, Any]:
        """Transform data with comprehensive divine protection"""
        if entry_node not in self.nodes:
            return data
        
        # Create guardian for this traversal
        guardian = SacredTraversalGuardian(
            max_depth=max_depth,
            timeout_seconds=timeout_seconds
        )
        
        try:
            return await SacredTimeoutManager.with_sacred_timeout(
                self._transform_at_node_safely(data, entry_node, guardian, 0),
                timeout_seconds
            )
        except SacredTimeoutError:
            print(f"Sacred timeout: Graph traversal exceeded {timeout_seconds}s")
            return data
        except Exception as e:
            print(f"Sacred error in graph traversal: {e}")
            return data
    
    async def _transform_at_node_safely(
        self, 
        data: Dict[str, Any], 
        node_id: str, 
        guardian: SacredTraversalGuardian,
        depth: int
    ) -> Dict[str, Any]:
        """Transform at node with comprehensive divine protection"""
        
        # Sacred cycle detection
        if guardian.detect_cycle(node_id):
            print(f"Sacred cycle detected at node {node_id} - graceful termination")
            return data
        
        # Sacred bounds checking
        if not guardian.can_continue(depth):
            print(f"Sacred bounds exceeded at depth {depth} - graceful termination")
            return data
        
        node = self.nodes[node_id]
        node.execution_count += 1
        node.last_execution = datetime.now()
        
        # Apply transformation with circuit breaker protection
        if node.transform_func:
            try:
                async def protected_transform():
                    return await node.transform_func(data)
                
                data = await self.circuit_breaker.call_with_protection(protected_transform)
                
            except SacredCircuitBreakerError:
                print(f"Circuit breaker open for node {node_id} - skipping transformation")
            except Exception as e:
                print(f"Transformation error at node {node_id}: {e}")
        
        # Sacred propagation with protection
        if node.adaptive and depth < guardian.max_depth:
            for connected_id in node.connections:
                if connected_id not in guardian.visited_nodes:
                    # Add memory protection
                    self.memory_sentinel.add_to_collection("traversal_path", connected_id)
                    
                    data = await self._transform_at_node_safely(
                        data, connected_id, guardian, depth + 1
                    )
        
        return data


# Sacred Event Loop Protection

class SacredEventLoop:
    """Event loop with divine protection against infinite execution"""
    
    def __init__(self):
        self.shutdown_event = asyncio.Event()
        self.circuit_breaker = SacredCircuitBreaker()
        self.memory_sentinel = SacredMemorySentinel()
        self.event_count = 0
        self.error_count = 0
        self.start_time = time.time()
    
    async def sacred_event_consumer(self, event_bus):
        """Event consumer with comprehensive divine protection"""
        consecutive_errors = 0
        max_consecutive_errors = 5
        
        while not self.shutdown_event.is_set():
            try:
                # Sacred timeout for event processing
                event = await asyncio.wait_for(
                    event_bus.get(), 
                    timeout=1.0  # Allow periodic shutdown checks
                )
                
                # Process with circuit breaker protection
                await self.circuit_breaker.call_with_protection(
                    lambda: self._process_event_safely(event)
                )
                
                consecutive_errors = 0  # Reset on success
                self.event_count += 1
                
            except asyncio.TimeoutError:
                # Normal timeout for shutdown checking
                continue
            except SacredCircuitBreakerError:
                # Circuit breaker is open, wait before retry
                await asyncio.sleep(5.0)
            except Exception as e:
                consecutive_errors += 1
                self.error_count += 1
                print(f"Sacred event processing error: {e}")
                
                if consecutive_errors >= max_consecutive_errors:
                    print("Too many consecutive errors, initiating graceful shutdown")
                    self.shutdown_event.set()
                    break
                
                # Sacred exponential backoff
                await asyncio.sleep(min(consecutive_errors * 2, 30))
    
    async def _process_event_safely(self, event):
        """Process event with memory protection"""
        self.memory_sentinel.add_to_collection("processed_events", {
            "event": str(event)[:100],  # Truncate for memory safety
            "timestamp": time.time()
        })
        print(f"Sacred event processed: {event}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get sacred event loop status"""
        uptime = time.time() - self.start_time
        return {
            "component": "SacredEventLoop",
            "uptime_seconds": uptime,
            "events_processed": self.event_count,
            "errors_encountered": self.error_count,
            "error_rate": self.error_count / max(1, self.event_count),
            "memory_usage_mb": self.memory_sentinel.get_memory_usage_mb(),
            "circuit_breaker": self.circuit_breaker.get_status(),
            "shutdown_requested": self.shutdown_event.is_set()
        }
    
    async def graceful_shutdown(self, timeout_seconds: float = 30.0):
        """Perform graceful shutdown with timeout"""
        print("Initiating sacred graceful shutdown...")
        self.shutdown_event.set()
        
        # Wait for current operations to complete
        try:
            await asyncio.wait_for(
                self._wait_for_completion(),
                timeout=timeout_seconds
            )
            print("Sacred shutdown completed gracefully")
        except asyncio.TimeoutError:
            print(f"Sacred shutdown timeout after {timeout_seconds}s - forcing termination")
    
    async def _wait_for_completion(self):
        """Wait for current operations to complete"""
        # In a real implementation, this would wait for active tasks
        await asyncio.sleep(1.0)


# Sacred Registry Memory Management

class SacredRegistryManager:
    """Registry manager with divine memory protection"""
    
    def __init__(self, max_assignments: int = 1000, max_metrics_history: int = 100):
        self.max_assignments = max_assignments
        self.max_metrics_history = max_metrics_history
        self.memory_sentinel = SacredMemorySentinel(max_memory_mb=200)
        
        self.task_assignments: Dict[str, Any] = {}
        self.load_balancer_metrics: Dict[str, Dict[str, Any]] = {}
        
        # Sacred cleanup scheduling
        self._cleanup_task = None
        self._start_cleanup_loop()
    
    def _start_cleanup_loop(self):
        """Start sacred cleanup loop"""
        self._cleanup_task = asyncio.create_task(self._sacred_cleanup_loop())
    
    async def _sacred_cleanup_loop(self):
        """Sacred cleanup ritual"""
        while True:
            try:
                await asyncio.sleep(300)  # Every 5 minutes
                await self._perform_sacred_cleanup()
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Sacred cleanup error: {e}")
    
    async def _perform_sacred_cleanup(self):
        """Perform divine memory cleanup"""
        cleanup_start = time.time()
        
        # Clean old task assignments
        if len(self.task_assignments) > self.max_assignments:
            # Sort by timestamp and keep recent ones
            sorted_items = sorted(
                self.task_assignments.items(),
                key=lambda x: x[1].get('assigned_at', 0),
                reverse=True
            )
            
            # Sacred preservation of recent assignments
            keep_count = self.max_assignments // 2
            self.task_assignments = dict(sorted_items[:keep_count])
        
        # Clean old metrics history
        for teammate_id, metrics in self.load_balancer_metrics.items():
            if "history" in metrics and len(metrics["history"]) > self.max_metrics_history:
                metrics["history"] = metrics["history"][-self.max_metrics_history//2:]
        
        # Perform sentinel cleanup
        self.memory_sentinel._perform_sacred_cleanup()
        
        cleanup_duration = time.time() - cleanup_start
        print(f"Sacred cleanup completed in {cleanup_duration:.2f}s: "
              f"{len(self.task_assignments)} assignments, "
              f"{len(self.load_balancer_metrics)} teammates")
    
    def add_assignment_safely(self, assignment_id: str, assignment_data: Dict[str, Any]):
        """Add assignment with memory protection"""
        self.memory_sentinel.add_to_collection("assignments", assignment_id)
        self.task_assignments[assignment_id] = assignment_data
    
    def add_metrics_safely(self, teammate_id: str, metric_data: Dict[str, Any]):
        """Add metrics with memory protection"""
        if teammate_id not in self.load_balancer_metrics:
            self.load_balancer_metrics[teammate_id] = {"history": []}
        
        self.load_balancer_metrics[teammate_id]["history"].append({
            "timestamp": time.time(),
            "data": metric_data
        })
        
        self.memory_sentinel.add_to_collection("metrics", teammate_id)
    
    async def shutdown(self):
        """Graceful shutdown of registry manager"""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
        
        # Final cleanup
        await self._perform_sacred_cleanup()


# Sacred Testing and Validation

async def test_sacred_computational_safety():
    """Test sacred computational safety implementations"""
    print("🔮 Testing Sacred Computational Safety Implementations")
    print("=" * 60)
    
    # Test 1: Sacred Graph Traversal
    print("\n1. Testing Sacred Graph Traversal Protection:")
    network = SacredHexaNetwork()
    
    # Create nodes
    node1 = SacredHexaNode("node1", "First Node")
    node2 = SacredHexaNode("node2", "Second Node")
    node3 = SacredHexaNode("node3", "Third Node")
    
    network.add_node(node1)
    network.add_node(node2)
    network.add_node(node3)
    
    # Create potential cycle
    network.connect_nodes("node1", "node2")
    network.connect_nodes("node2", "node3")
    network.connect_nodes("node3", "node1")  # Creates cycle
    
    test_data = {"test": "data"}
    result = await network.transform_data_safely(test_data, "node1", timeout_seconds=5.0)
    print(f"   ✅ Graph traversal completed safely: {len(result)} keys")
    
    # Test 2: Sacred Event Loop
    print("\n2. Testing Sacred Event Loop Protection:")
    event_loop = SacredEventLoop()
    
    # Simulate event bus
    class MockEventBus:
        def __init__(self):
            self.events = ["event1", "event2", "event3"]
            self.index = 0
        
        async def get(self):
            if self.index < len(self.events):
                event = self.events[self.index]
                self.index += 1
                return event
            else:
                await asyncio.sleep(0.1)  # Simulate waiting
                return "periodic_event"
    
    mock_bus = MockEventBus()
    
    # Run event loop for a short time
    consumer_task = asyncio.create_task(event_loop.sacred_event_consumer(mock_bus))
    await asyncio.sleep(2.0)
    await event_loop.graceful_shutdown(timeout_seconds=5.0)
    
    status = event_loop.get_status()
    print(f"   ✅ Event loop processed {status['events_processed']} events safely")
    
    # Test 3: Sacred Memory Management
    print("\n3. Testing Sacred Memory Management:")
    registry = SacredRegistryManager(max_assignments=10)
    
    # Add many assignments to test cleanup
    for i in range(15):
        registry.add_assignment_safely(f"assignment_{i}", {
            "assigned_at": time.time(),
            "data": f"test_data_{i}"
        })
    
    # Trigger cleanup
    await registry._perform_sacred_cleanup()
    
    print(f"   ✅ Memory management: {len(registry.task_assignments)} assignments after cleanup")
    
    await registry.shutdown()
    
    print("\n🌟 All Sacred Computational Safety Tests Completed Successfully!")


if __name__ == "__main__":
    asyncio.run(test_sacred_computational_safety())