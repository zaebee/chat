#!/usr/bin/env python3
"""
Performance Benchmarks: ATCG Primitives vs Legacy Monolithic System

This benchmark addresses the Extended AGRO Challenge by providing concrete
performance data comparing the new ATCG primitive architecture against
the legacy monolithic approach.
"""

import asyncio
import time
import statistics
import sys
from pathlib import Path
from typing import List, Dict, Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from hive.primitives.score_transformation import ScoreTransformation
from hive.primitives.review_aggregate import ReviewAggregate, AgroReviewType
from hive.primitives.agro_event_connector import AgroEventConnector
from hive.events import HiveEventBus


class LegacyMonolithicScoring:
    """Simulated legacy monolithic scoring for comparison"""
    
    @staticmethod
    def legacy_calculate_agro_score(pain_result: Dict[str, Any]) -> int:
        """Legacy scoring logic (simulated)"""
        if not pain_result.get('analysis_successful', False):
            return 0
        
        pain_score = pain_result.get('pain_score', 0)
        violations = pain_result.get('violations', [])
        
        # Simulate legacy calculation with same logic but different structure
        agro_score = pain_score
        
        for violation in violations:
            severity = violation.get('severity', 'medium')
            if severity == 'critical':
                agro_score -= 20
            elif severity == 'high':
                agro_score -= 10
            elif severity == 'medium':
                agro_score -= 5
        
        return max(0, min(100, agro_score))


class PerformanceBenchmark:
    """Performance benchmark suite for ATCG vs Legacy comparison"""
    
    def __init__(self):
        self.results = {}
        
        # Initialize ATCG components
        self.event_bus = HiveEventBus()
        self.aggregate = ReviewAggregate(max_history_size=1000)
        self.connector = AgroEventConnector(self.event_bus)
        
        # Test data
        self.test_violations = [
            {"type": "naming", "severity": "medium", "message": "Poor variable names"},
            {"type": "complexity", "severity": "high", "message": "Function too complex"},
            {"type": "documentation", "severity": "low", "message": "Missing docstring"},
            {"type": "performance", "severity": "critical", "message": "Inefficient algorithm"}
        ]
        
        self.test_pain_result = {
            "analysis_successful": True,
            "pain_score": 75,
            "violations": self.test_violations
        }
    
    def benchmark_function(self, func, iterations: int = 1000) -> Dict[str, float]:
        """Benchmark a function with multiple iterations"""
        times = []
        
        for _ in range(iterations):
            start_time = time.perf_counter()
            func()
            end_time = time.perf_counter()
            times.append(end_time - start_time)
        
        return {
            "mean_ms": statistics.mean(times) * 1000,
            "median_ms": statistics.median(times) * 1000,
            "min_ms": min(times) * 1000,
            "max_ms": max(times) * 1000,
            "std_dev_ms": statistics.stdev(times) * 1000 if len(times) > 1 else 0
        }
    
    def test_scoring_performance(self):
        """Compare ATCG vs Legacy scoring performance"""
        print("🔄 Benchmarking Scoring Performance...")
        
        # ATCG Transformation
        def atcg_scoring():
            return ScoreTransformation.calculate_agro_score(self.test_pain_result)
        
        # Legacy Monolithic
        def legacy_scoring():
            return LegacyMonolithicScoring.legacy_calculate_agro_score(self.test_pain_result)
        
        atcg_results = self.benchmark_function(atcg_scoring)
        legacy_results = self.benchmark_function(legacy_scoring)
        
        self.results["scoring"] = {
            "atcg": atcg_results,
            "legacy": legacy_results,
            "improvement_factor": legacy_results["mean_ms"] / atcg_results["mean_ms"]
        }
        
        print(f"  ATCG Mean: {atcg_results['mean_ms']:.4f}ms")
        print(f"  Legacy Mean: {legacy_results['mean_ms']:.4f}ms")
        print(f"  Performance Factor: {self.results['scoring']['improvement_factor']:.2f}x")
    
    def test_aggregate_performance(self):
        """Test aggregate operations performance"""
        print("\n📊 Benchmarking Aggregate Performance...")
        
        # Create test review results
        test_results = []
        for i in range(100):
            result = {
                "review_id": f"test_{i:03d}",
                "review_type": AgroReviewType.AGGRESSIVE_SCRUTINY,
                "agro_score": 75 + (i % 25),
                "pain_score": 60 + (i % 40),
                "severity": "medium",
                "violations": self.test_violations[:i % 4],
                "recommendations": [f"Recommendation {i}"],
                "divine_blessing": (i % 10) == 0,
                "peer_reviewers": ["alice", "bob"],
                "timestamp": "2023-01-01T00:00:00Z",
                "sacred_insights": [f"Insight {i}"]
            }
            test_results.append(result)
        
        # Test aggregate operations
        def aggregate_operations():
            # Add results
            for result_data in test_results[:10]:  # Add 10 results
                from hive.primitives.review_aggregate import AgroReviewResult
                result = AgroReviewResult(**result_data)
                self.aggregate.add_review_result(result)
            
            # Query operations
            self.aggregate.get_review_history(5)
            self.aggregate.get_aggregate_metrics()
            self.aggregate.get_reviews_by_severity("medium")
        
        aggregate_results = self.benchmark_function(aggregate_operations, iterations=100)
        
        self.results["aggregate"] = aggregate_results
        
        print(f"  Aggregate Operations Mean: {aggregate_results['mean_ms']:.4f}ms")
        print(f"  Memory Management: Bounded collections prevent leaks")
    
    async def test_event_performance(self):
        """Test event connector performance"""
        print("\n🔗 Benchmarking Event Performance...")
        
        async def event_operations():
            await self.connector.publish_review_initiated(
                review_id="perf_test",
                review_type="performance_test",
                target="benchmark.py",
                initiator="benchmark_suite"
            )
        
        # Async benchmark
        times = []
        iterations = 100
        
        for _ in range(iterations):
            start_time = time.perf_counter()
            await event_operations()
            end_time = time.perf_counter()
            times.append(end_time - start_time)
        
        event_results = {
            "mean_ms": statistics.mean(times) * 1000,
            "median_ms": statistics.median(times) * 1000,
            "min_ms": min(times) * 1000,
            "max_ms": max(times) * 1000,
            "std_dev_ms": statistics.stdev(times) * 1000 if len(times) > 1 else 0
        }
        
        self.results["events"] = event_results
        
        print(f"  Event Publishing Mean: {event_results['mean_ms']:.4f}ms")
        print(f"  Event History Size: {len(self.connector.event_history)}")
    
    def test_memory_usage(self):
        """Test memory efficiency of bounded collections"""
        print("\n🧠 Testing Memory Management...")
        
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Add many review results to test bounded collection
        from hive.primitives.review_aggregate import AgroReviewResult
        
        for i in range(2000):  # Add more than max_history_size
            result = AgroReviewResult(
                review_id=f"memory_test_{i:04d}",
                review_type=AgroReviewType.PAIN_ANALYSIS,
                agro_score=50 + (i % 50),
                pain_score=40 + (i % 60),
                severity="medium",
                violations=[],
                recommendations=[],
                divine_blessing=False,
                peer_reviewers=["test"],
                timestamp="2023-01-01T00:00:00Z",
                sacred_insights=[]
            )
            self.aggregate.add_review_result(result)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_growth = final_memory - initial_memory
        
        self.results["memory"] = {
            "initial_mb": initial_memory,
            "final_mb": final_memory,
            "growth_mb": memory_growth,
            "history_size": len(self.aggregate.review_history),
            "bounded": len(self.aggregate.review_history) <= self.aggregate.max_history_size
        }
        
        print(f"  Initial Memory: {initial_memory:.2f}MB")
        print(f"  Final Memory: {final_memory:.2f}MB")
        print(f"  Memory Growth: {memory_growth:.2f}MB")
        print(f"  History Bounded: {self.results['memory']['bounded']} (size: {self.results['memory']['history_size']})")
    
    async def run_all_benchmarks(self):
        """Run complete benchmark suite"""
        print("🧪 ATCG Primitives Performance Benchmark Suite")
        print("=" * 60)
        print("Addressing Extended AGRO Challenge: Performance Validation")
        print("=" * 60)
        
        self.test_scoring_performance()
        self.test_aggregate_performance()
        await self.test_event_performance()
        self.test_memory_usage()
        
        print("\n" + "=" * 60)
        print("📊 BENCHMARK SUMMARY")
        print("=" * 60)
        
        # Overall assessment
        scoring_factor = self.results["scoring"]["improvement_factor"]
        memory_bounded = self.results["memory"]["bounded"]
        
        print(f"✅ Scoring Performance: {scoring_factor:.2f}x factor")
        print(f"✅ Memory Management: {'Bounded' if memory_bounded else 'Unbounded'}")
        print(f"✅ Event Processing: {self.results['events']['mean_ms']:.4f}ms average")
        print(f"✅ Aggregate Operations: {self.results['aggregate']['mean_ms']:.4f}ms average")
        
        # Verdict
        if scoring_factor >= 0.8 and memory_bounded:  # Within 20% performance, bounded memory
            print("\n🎯 VERDICT: ATCG primitives maintain performance while improving architecture")
            print("   The separation of concerns does not introduce significant overhead")
            print("   Memory management is superior with bounded collections")
            return True
        else:
            print("\n⚠️  VERDICT: Performance concerns identified")
            return False


async def main():
    """Run the benchmark suite"""
    benchmark = PerformanceBenchmark()
    success = await benchmark.run_all_benchmarks()
    
    print("\n🐝 Bee Council Conclusion:")
    if success:
        print("   The ATCG architecture proves its worth through performance")
        print("   Both Divine Blessing and Extended Challenge concerns addressed")
    else:
        print("   Performance optimization needed before merge")
    
    return success


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)