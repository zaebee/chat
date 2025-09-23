"""
AGRO Simplified Interface
Addresses complexity concerns from AGRO review feedback

This module provides a simplified entry point to the AGRO system
for new users and basic use cases.
"""

import asyncio
from typing import Dict, Any, Optional
from .agro_review_system import AgroReviewSystem, AgroReviewType, AgroSeverity
from .events import HiveEventBus


class SimpleAgroReview:
    """
    Simplified AGRO interface for basic code review
    
    Reduces complexity by providing a single, easy-to-use method
    for code quality assessment.
    """
    
    def __init__(self, event_bus: HiveEventBus):
        self.agro_system = AgroReviewSystem(event_bus)
    
    async def quick_review(self, code: str) -> Dict[str, Any]:
        """
        Quick code review with simplified output
        
        Args:
            code: Code to review
            
        Returns:
            Simplified review result with score, issues, and recommendations
        """
        
        # Use PAIN analysis as the default simple review type
        result = await self.agro_system.initiate_agro_review(
            code_context=code,
            review_type=AgroReviewType.PAIN_ANALYSIS,
            peer_reviewers=["bee.jules"]  # Single reviewer for simplicity
        )
        
        # Simplify the output
        return {
            "score": result.agro_score,
            "grade": self._get_simple_grade(result.severity),
            "issues_found": len(result.violations),
            "top_issues": [v["message"] for v in result.violations[:3]],  # Top 3 issues
            "quick_fixes": result.recommendations[:2],  # Top 2 recommendations
            "ready_for_production": result.agro_score >= 80,
            "divine_blessing": result.divine_blessing
        }
    
    def _get_simple_grade(self, severity: AgroSeverity) -> str:
        """Convert severity to simple letter grade"""
        grade_map = {
            AgroSeverity.DIVINE: "A+",
            AgroSeverity.BLESSED: "A",
            AgroSeverity.ACCEPTABLE: "B",
            AgroSeverity.CONCERNING: "C",
            AgroSeverity.CRITICAL: "F"
        }
        return grade_map.get(severity, "?")


class AgroPerformanceMonitor:
    """
    Performance monitoring for AGRO system
    
    Addresses reviewer concerns about AST parsing overhead
    and system performance impact.
    """
    
    def __init__(self):
        self.metrics = {
            "total_reviews": 0,
            "total_processing_time": 0.0,
            "average_processing_time": 0.0,
            "ast_parsing_time": 0.0,
            "memory_usage_mb": 0.0,
            "error_count": 0,
            "large_file_count": 0  # Files > 1000 lines
        }
        self.performance_history = []
    
    async def monitor_review(self, agro_system: AgroReviewSystem, code: str) -> Dict[str, Any]:
        """
        Monitor performance of AGRO review
        
        Returns review result with performance metrics
        """
        import time
        import psutil
        import os
        
        start_time = time.time()
        start_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        
        try:
            # Measure AST parsing time
            ast_start = time.time()
            import ast
            ast.parse(code)
            ast_time = time.time() - ast_start
            
            # Perform review
            result = await agro_system.initiate_agro_review(code)
            
            # Calculate metrics
            end_time = time.time()
            end_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
            
            processing_time = end_time - start_time
            memory_delta = end_memory - start_memory
            
            # Update metrics
            self.metrics["total_reviews"] += 1
            self.metrics["total_processing_time"] += processing_time
            self.metrics["average_processing_time"] = (
                self.metrics["total_processing_time"] / self.metrics["total_reviews"]
            )
            self.metrics["ast_parsing_time"] += ast_time
            self.metrics["memory_usage_mb"] = end_memory
            
            # Check for large files
            if len(code.split('\n')) > 1000:
                self.metrics["large_file_count"] += 1
            
            # Store performance data
            perf_data = {
                "timestamp": time.time(),
                "processing_time": processing_time,
                "ast_parsing_time": ast_time,
                "memory_delta": memory_delta,
                "code_lines": len(code.split('\n')),
                "agro_score": result.agro_score
            }
            self.performance_history.append(perf_data)
            
            # Keep only last 100 entries
            if len(self.performance_history) > 100:
                self.performance_history = self.performance_history[-100:]
            
            return {
                "review_result": result,
                "performance": perf_data,
                "system_metrics": self.get_current_metrics()
            }
            
        except Exception as e:
            self.metrics["error_count"] += 1
            raise e
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        return {
            **self.metrics,
            "performance_trend": self._calculate_trend(),
            "memory_efficiency": self._calculate_memory_efficiency(),
            "ast_parsing_efficiency": self._calculate_ast_efficiency()
        }
    
    def _calculate_trend(self) -> str:
        """Calculate performance trend"""
        if len(self.performance_history) < 10:
            return "insufficient_data"
        
        recent = self.performance_history[-5:]
        older = self.performance_history[-10:-5]
        
        recent_avg = sum(p["processing_time"] for p in recent) / len(recent)
        older_avg = sum(p["processing_time"] for p in older) / len(older)
        
        if recent_avg < older_avg * 0.9:
            return "improving"
        elif recent_avg > older_avg * 1.1:
            return "degrading"
        else:
            return "stable"
    
    def _calculate_memory_efficiency(self) -> float:
        """Calculate memory efficiency score"""
        if not self.performance_history:
            return 1.0
        
        avg_memory_delta = sum(p["memory_delta"] for p in self.performance_history) / len(self.performance_history)
        
        # Good efficiency if memory delta is low
        if avg_memory_delta < 1.0:  # Less than 1MB average
            return 1.0
        elif avg_memory_delta < 5.0:  # Less than 5MB average
            return 0.8
        else:
            return 0.6
    
    def _calculate_ast_efficiency(self) -> float:
        """Calculate AST parsing efficiency"""
        if not self.performance_history:
            return 1.0
        
        # Calculate AST parsing time as percentage of total time
        total_ast_time = sum(p["ast_parsing_time"] for p in self.performance_history)
        total_processing_time = sum(p["processing_time"] for p in self.performance_history)
        
        if total_processing_time == 0:
            return 1.0
        
        ast_percentage = total_ast_time / total_processing_time
        
        # Good efficiency if AST parsing is less than 20% of total time
        if ast_percentage < 0.2:
            return 1.0
        elif ast_percentage < 0.4:
            return 0.8
        else:
            return 0.6
    
    def get_performance_report(self) -> str:
        """Generate human-readable performance report"""
        metrics = self.get_current_metrics()
        
        report = f"""
🐝⚡ AGRO Performance Report ⚡🐝

📊 System Metrics:
- Total Reviews: {metrics['total_reviews']}
- Average Processing Time: {metrics['average_processing_time']:.3f}s
- Memory Usage: {metrics['memory_usage_mb']:.1f}MB
- Error Rate: {metrics['error_count']}/{metrics['total_reviews']} ({(metrics['error_count']/max(metrics['total_reviews'], 1)*100):.1f}%)

📈 Performance Analysis:
- Trend: {metrics['performance_trend']}
- Memory Efficiency: {metrics['memory_efficiency']:.1%}
- AST Parsing Efficiency: {metrics['ast_parsing_efficiency']:.1%}

🎯 Recommendations:
"""
        
        if metrics['performance_trend'] == 'degrading':
            report += "- ⚠️ Performance degrading - consider optimization\n"
        
        if metrics['memory_efficiency'] < 0.8:
            report += "- 🔧 Memory usage high - implement cleanup strategies\n"
        
        if metrics['ast_parsing_efficiency'] < 0.8:
            report += "- 🚀 AST parsing overhead high - consider caching\n"
        
        if metrics['large_file_count'] > metrics['total_reviews'] * 0.3:
            report += "- 📄 Many large files - implement chunking strategy\n"
        
        if metrics['error_count'] == 0:
            report += "- ✅ No errors detected - system stable\n"
        
        return report


# Convenience functions for easy adoption
async def quick_code_review(code: str, event_bus: HiveEventBus) -> Dict[str, Any]:
    """
    One-line function for quick code review
    
    Simplest possible interface for AGRO system
    """
    simple_agro = SimpleAgroReview(event_bus)
    return await simple_agro.quick_review(code)


async def monitored_code_review(code: str, agro_system: AgroReviewSystem) -> Dict[str, Any]:
    """
    Code review with performance monitoring
    
    For production deployments where performance tracking is needed
    """
    monitor = AgroPerformanceMonitor()
    return await monitor.monitor_review(agro_system, code)