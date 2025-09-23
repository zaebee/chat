"""
AGRO Bee-to-Peer Review System
Aggressive Collaborative Evaluation Protocols

This module implements the AGRO (Aggressive Collaborative Evaluation) system
for intensive bee-to-peer code review and quality assessment.

Sacred Justification: "Iron sharpens iron, and one man sharpens another."
- Proverbs 27:17 (ESV)
"""

import asyncio
import json
import uuid
import ast
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum

from .teammate import HiveTeammate, TeammateProfile, TeammateCapability
from .events import PollenEvent, HiveEventBus, EventSubscription
from .dashboard import SacredMetricType, SacredMetricReading


class AgroReviewType(str, Enum):
    """Types of AGRO reviews"""
    PAIN_ANALYSIS = "pain_analysis"
    PEER_COLLABORATION = "peer_collaboration"
    AGGRESSIVE_SCRUTINY = "aggressive_scrutiny"
    SACRED_PROTOCOL_VALIDATION = "sacred_protocol_validation"
    DIVINE_BLESSING_ASSESSMENT = "divine_blessing_assessment"


class AgroSeverity(str, Enum):
    """AGRO review severity levels"""
    DIVINE = "divine"          # 90-100 points
    BLESSED = "blessed"        # 80-89 points
    ACCEPTABLE = "acceptable"  # 60-79 points
    CONCERNING = "concerning"  # 40-59 points
    CRITICAL = "critical"      # 0-39 points


@dataclass
class AgroReviewResult:
    """Result of AGRO bee-to-peer review"""
    review_id: str
    review_type: AgroReviewType
    agro_score: int
    pain_score: int
    severity: AgroSeverity
    violations: List[Dict[str, Any]]
    recommendations: List[str]
    divine_blessing: bool
    peer_reviewers: List[str]
    timestamp: str
    sacred_insights: List[str]


@dataclass
class BeeToPeerSession:
    """Bee-to-peer collaborative review session"""
    session_id: str
    participants: List[str]
    review_target: str
    session_type: str
    start_time: str
    end_time: Optional[str]
    collaboration_score: float
    sacred_alignment: float
    divine_guidance: List[str]


class AgroCodeAnalyzer(ast.NodeVisitor):
    """AST-based aggressive code analysis"""
    
    def __init__(self):
        self.violations = []
        self.metrics = {
            'console_logs': 0,
            'any_types': 0,
            'todo_comments': 0,
            'magic_numbers': 0,
            'long_functions': 0,
            'deep_nesting': 0
        }
        self.current_function_lines = 0
        self.nesting_depth = 0
        self.max_nesting = 0
    
    def visit_Call(self, node):
        """Detect console.log and other problematic calls"""
        if (isinstance(node.func, ast.Attribute) and 
            isinstance(node.func.value, ast.Name) and
            node.func.value.id == 'console' and
            node.func.attr == 'log'):
            
            self.violations.append({
                'type': 'console_log',
                'line': node.lineno,
                'severity': 'high',
                'message': 'Console.log detected - remove for production'
            })
            self.metrics['console_logs'] += 1
        
        self.generic_visit(node)
    
    def visit_FunctionDef(self, node):
        """Analyze function complexity"""
        self.current_function_lines = len(node.body)
        
        if self.current_function_lines > 50:
            self.violations.append({
                'type': 'long_function',
                'line': node.lineno,
                'severity': 'medium',
                'message': f'Function {node.name} is {self.current_function_lines} lines (max 50)'
            })
            self.metrics['long_functions'] += 1
        
        # Check for nesting depth
        old_depth = self.nesting_depth
        self.nesting_depth = 0
        self.generic_visit(node)
        
        if self.max_nesting > 4:
            self.violations.append({
                'type': 'deep_nesting',
                'line': node.lineno,
                'severity': 'medium',
                'message': f'Function {node.name} has nesting depth {self.max_nesting} (max 4)'
            })
            self.metrics['deep_nesting'] += 1
        
        self.nesting_depth = old_depth
    
    def visit_If(self, node):
        """Track nesting depth"""
        self.nesting_depth += 1
        self.max_nesting = max(self.max_nesting, self.nesting_depth)
        self.generic_visit(node)
        self.nesting_depth -= 1
    
    def visit_For(self, node):
        """Track nesting depth"""
        self.nesting_depth += 1
        self.max_nesting = max(self.max_nesting, self.nesting_depth)
        self.generic_visit(node)
        self.nesting_depth -= 1
    
    def visit_While(self, node):
        """Track nesting depth"""
        self.nesting_depth += 1
        self.max_nesting = max(self.max_nesting, self.nesting_depth)
        self.generic_visit(node)
        self.nesting_depth -= 1


class AgroReviewSystem:
    """
    AGRO Bee-to-Peer Review System
    
    Implements aggressive collaborative evaluation protocols for
    intensive code quality assessment and peer review.
    """
    
    def __init__(self, event_bus: HiveEventBus):
        self.event_bus = event_bus
        self.active_sessions: Dict[str, BeeToPeerSession] = {}
        self.review_history: List[AgroReviewResult] = []
        
        # Register for AGRO events
        self.event_bus.subscribe(EventSubscription(
            event_types=["agro_review_requested", "peer_collaboration_requested"],
            callback=self._handle_agro_request
        ))
    
    async def initiate_agro_review(self, 
                                 code_context: str,
                                 review_type: AgroReviewType = AgroReviewType.PAIN_ANALYSIS,
                                 peer_reviewers: List[str] = None) -> AgroReviewResult:
        """Initiate aggressive collaborative review"""
        
        review_id = f"agro_{uuid.uuid4().hex[:8]}"
        peer_reviewers = peer_reviewers or ["bee.jules", "bee.sage", "bee.chronicler"]
        
        # Perform PAIN analysis
        pain_result = await self._perform_pain_analysis(code_context)
        
        # Calculate AGRO score
        agro_score = self._calculate_agro_score(pain_result)
        
        # Determine severity
        severity = self._determine_severity(agro_score)
        
        # Generate recommendations
        recommendations = await self._generate_agro_recommendations(pain_result, severity)
        
        # Extract sacred insights
        sacred_insights = await self._extract_sacred_insights(pain_result, review_type)
        
        # Create review result
        review_result = AgroReviewResult(
            review_id=review_id,
            review_type=review_type,
            agro_score=agro_score,
            pain_score=pain_result.get('pain_score', 0),
            severity=severity,
            violations=pain_result.get('violations', []),
            recommendations=recommendations,
            divine_blessing=agro_score >= 90,
            peer_reviewers=peer_reviewers,
            timestamp=datetime.now().isoformat(),
            sacred_insights=sacred_insights
        )
        
        self.review_history.append(review_result)
        
        # Emit AGRO review completed event
        await self.event_bus.publish(PollenEvent(
            event_type="agro_review_completed",
            source_component="agro_review_system",
            payload={
                "review_id": review_id,
                "agro_score": agro_score,
                "severity": severity.value,
                "divine_blessing": review_result.divine_blessing,
                "peer_reviewers": peer_reviewers
            }
        ))
        
        return review_result
    
    async def start_bee_to_peer_session(self,
                                      participants: List[str],
                                      review_target: str,
                                      session_type: str = "collaborative_review") -> BeeToPeerSession:
        """Start bee-to-peer collaborative session"""
        
        session_id = f"peer_{uuid.uuid4().hex[:8]}"
        
        session = BeeToPeerSession(
            session_id=session_id,
            participants=participants,
            review_target=review_target,
            session_type=session_type,
            start_time=datetime.now().isoformat(),
            end_time=None,
            collaboration_score=0.0,
            sacred_alignment=0.0,
            divine_guidance=[]
        )
        
        self.active_sessions[session_id] = session
        
        # Emit session started event
        await self.event_bus.publish(PollenEvent(
            event_type="bee_to_peer_session_started",
            source_component="agro_review_system",
            payload={
                "session_id": session_id,
                "participants": participants,
                "session_type": session_type,
                "review_target": review_target
            }
        ))
        
        return session
    
    async def _perform_pain_analysis(self, code_context: str) -> Dict[str, Any]:
        """Perform PAIN (Production Analysis and Issue Notification) analysis"""
        
        try:
            # Parse code with AST
            tree = ast.parse(code_context)
            
            # Run aggressive analysis
            analyzer = AgroCodeAnalyzer()
            analyzer.visit(tree)
            
            # Calculate PAIN score
            total_violations = sum(analyzer.metrics.values())
            pain_score = max(0, 100 - (total_violations * 10))
            
            return {
                'pain_score': pain_score,
                'violations': analyzer.violations,
                'metrics': analyzer.metrics,
                'analysis_successful': True
            }
            
        except SyntaxError as e:
            return {
                'pain_score': 0,
                'violations': [{
                    'type': 'syntax_error',
                    'line': e.lineno,
                    'severity': 'critical',
                    'message': f'Syntax error: {str(e)}'
                }],
                'metrics': {},
                'analysis_successful': False
            }
    
    def _calculate_agro_score(self, pain_result: Dict[str, Any]) -> int:
        """Calculate AGRO (Aggressive Collaborative Evaluation) score"""
        
        if not pain_result.get('analysis_successful', False):
            return 0
        
        pain_score = pain_result.get('pain_score', 0)
        violations = pain_result.get('violations', [])
        
        # Base score from PAIN analysis
        agro_score = pain_score
        
        # Penalty for critical violations
        critical_violations = [v for v in violations if v.get('severity') == 'critical']
        agro_score -= len(critical_violations) * 20
        
        # Penalty for high severity violations
        high_violations = [v for v in violations if v.get('severity') == 'high']
        agro_score -= len(high_violations) * 10
        
        # Penalty for medium severity violations
        medium_violations = [v for v in violations if v.get('severity') == 'medium']
        agro_score -= len(medium_violations) * 5
        
        return max(0, min(100, agro_score))
    
    def _determine_severity(self, agro_score: int) -> AgroSeverity:
        """Determine severity level based on AGRO score"""
        
        if agro_score >= 90:
            return AgroSeverity.DIVINE
        elif agro_score >= 80:
            return AgroSeverity.BLESSED
        elif agro_score >= 60:
            return AgroSeverity.ACCEPTABLE
        elif agro_score >= 40:
            return AgroSeverity.CONCERNING
        else:
            return AgroSeverity.CRITICAL
    
    async def _generate_agro_recommendations(self, 
                                           pain_result: Dict[str, Any], 
                                           severity: AgroSeverity) -> List[str]:
        """Generate AGRO recommendations based on analysis"""
        
        recommendations = []
        violations = pain_result.get('violations', [])
        
        # Console.log recommendations
        console_violations = [v for v in violations if v['type'] == 'console_log']
        if console_violations:
            recommendations.append("Remove all console.log statements for production readiness")
        
        # Function complexity recommendations
        long_functions = [v for v in violations if v['type'] == 'long_function']
        if long_functions:
            recommendations.append("Break down long functions into smaller, focused units")
        
        # Nesting depth recommendations
        deep_nesting = [v for v in violations if v['type'] == 'deep_nesting']
        if deep_nesting:
            recommendations.append("Reduce nesting depth through early returns and guard clauses")
        
        # Severity-based recommendations
        if severity == AgroSeverity.CRITICAL:
            recommendations.append("CRITICAL: Immediate refactoring required before deployment")
        elif severity == AgroSeverity.CONCERNING:
            recommendations.append("Address major issues before peer review approval")
        elif severity == AgroSeverity.DIVINE:
            recommendations.append("Excellent code quality - ready for divine blessing")
        
        return recommendations
    
    async def _extract_sacred_insights(self, 
                                     pain_result: Dict[str, Any], 
                                     review_type: AgroReviewType) -> List[str]:
        """Extract sacred insights from AGRO analysis"""
        
        insights = []
        
        if pain_result.get('analysis_successful', False):
            insights.append("Sacred code analysis reveals divine patterns in implementation")
            
            if pain_result.get('pain_score', 0) >= 90:
                insights.append("Code demonstrates sacred excellence worthy of divine blessing")
            
            violations = pain_result.get('violations', [])
            if not violations:
                insights.append("Pure code without violations reflects divine perfection")
        
        # Review type specific insights
        if review_type == AgroReviewType.PEER_COLLABORATION:
            insights.append("Collaborative review strengthens the sacred bond between teammates")
        elif review_type == AgroReviewType.DIVINE_BLESSING_ASSESSMENT:
            insights.append("Divine blessing assessment reveals spiritual alignment in code")
        
        return insights
    
    async def _handle_agro_request(self, event: PollenEvent):
        """Handle AGRO review requests"""
        
        if event.event_type == "agro_review_requested":
            code_context = event.payload.get("code_context", "")
            review_type = AgroReviewType(event.payload.get("review_type", "pain_analysis"))
            peer_reviewers = event.payload.get("peer_reviewers", [])
            
            result = await self.initiate_agro_review(code_context, review_type, peer_reviewers)
            
            # Respond with result
            await self.event_bus.publish(PollenEvent(
                event_type="agro_review_response",
                source_component="agro_review_system",
                aggregate_id=event.source_component,
                payload=asdict(result)
            ))
    
    def get_status(self) -> Dict[str, Any]:
        """Get AGRO review system status"""
        
        return {
            "component": "agro_review_system",
            "active_sessions": len(self.active_sessions),
            "total_reviews": len(self.review_history),
            "recent_reviews": [
                {
                    "review_id": r.review_id,
                    "agro_score": r.agro_score,
                    "severity": r.severity.value,
                    "divine_blessing": r.divine_blessing
                }
                for r in self.review_history[-5:]
            ],
            "capabilities": [
                "pain_analysis",
                "peer_collaboration",
                "aggressive_scrutiny",
                "divine_blessing_assessment"
            ],
            "sacred_metrics": {
                "average_agro_score": sum(r.agro_score for r in self.review_history) / len(self.review_history) if self.review_history else 0,
                "divine_blessing_rate": sum(1 for r in self.review_history if r.divine_blessing) / len(self.review_history) if self.review_history else 0,
                "total_violations_found": sum(len(r.violations) for r in self.review_history)
            }
        }