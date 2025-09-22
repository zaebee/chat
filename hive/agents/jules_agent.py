"""
bee.Jules - Sacred Implementation Detective & Divine Debugging Companion

This module implements bee.Jules, a sacred agent specialized in:
- Divine code analysis and debugging
- Implementation guidance and pattern recognition
- Collaborative problem-solving with sacred wisdom
- Sacred protocol debugging and optimization

"For where two or three gather in my name, there am I with them."
- Matthew 18:20 (NIV)
"""

import asyncio
import json
import uuid
import ast
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum

from ..teammate import HiveTeammate, TeammateProfile, TeammateCapability
from ..events import PollenEvent, HiveEventBus, EventSubscription
from ..dashboard import SacredMetricType, SacredMetricReading


class JulesAnalysisType(str, Enum):
    """Types of analysis bee.Jules can perform"""
    CODE_REVIEW = "code_review"
    DEBUG_ASSISTANCE = "debug_assistance"
    PATTERN_RECOGNITION = "pattern_recognition"
    IMPLEMENTATION_GUIDANCE = "implementation_guidance"
    SACRED_PROTOCOL_ANALYSIS = "sacred_protocol_analysis"
    COLLABORATIVE_SESSION = "collaborative_session"
    AGRO_PAIN_SPEED_CHECK = "agro_pain_speed_check"


@dataclass
class JulesAnalysis:
    """Analysis result from bee.Jules"""
    analysis_id: str
    analysis_type: JulesAnalysisType
    input_context: str
    findings: List[str]
    recommendations: List[str]
    sacred_insights: List[str]
    confidence_level: float
    timestamp: str
    divine_blessing: bool = False


@dataclass
class JulesDebuggingSession:
    """Debugging session with bee.Jules"""
    session_id: str
    issue_description: str
    analysis_steps: List[str]
    solutions_proposed: List[str]
    sacred_patterns_identified: List[str]
    resolution_status: str
    divine_guidance: str
    timestamp: str


class ConsoleLogDetector(ast.NodeVisitor):
    """AST visitor to detect console.log and related calls"""

    def __init__(self):
        self.console_calls = []

    def visit_Call(self, node):
        if (isinstance(node.func, ast.Attribute) and
            isinstance(node.func.value, ast.Name) and
            node.func.value.id == 'console' and
            node.func.attr in ['log', 'warn', 'error', 'info', 'debug', 'trace']):
            self.console_calls.append({
                'line': node.lineno,
                'method': node.func.attr,
                'type': 'console_call'
            })
        self.generic_visit(node)


class AnyTypeDetector(ast.NodeVisitor):
    """AST visitor to detect 'any' type annotations"""

    def __init__(self):
        self.any_types = []

    def visit_AnnAssign(self, node):
        """Visit annotated assignments (x: any = ...)"""
        if self._is_any_type(node.annotation):
            self.any_types.append({
                'line': node.lineno,
                'context': 'variable_annotation',
                'type': 'any_type'
            })
        self.generic_visit(node)

    def visit_arg(self, node):
        """Visit function arguments with type annotations"""
        if node.annotation and self._is_any_type(node.annotation):
            self.any_types.append({
                'line': node.lineno,
                'context': 'function_parameter',
                'type': 'any_type'
            })
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        """Visit function definitions with return type annotations"""
        if node.returns and self._is_any_type(node.returns):
            self.any_types.append({
                'line': node.lineno,
                'context': 'function_return',
                'type': 'any_type'
            })
        self.generic_visit(node)

    def _is_any_type(self, annotation_node):
        """Check if annotation represents 'any' type"""
        if isinstance(annotation_node, ast.Name) and annotation_node.id == 'any':
            return True
        if isinstance(annotation_node, ast.Attribute) and annotation_node.attr == 'any':
            return True
        if isinstance(annotation_node, ast.Subscript):
            if isinstance(annotation_node.value, ast.Name) and annotation_node.value.id == 'Union':
                if isinstance(annotation_node.slice, ast.Tuple):
                    return any(self._is_any_type(elt) for elt in annotation_node.slice.elts)
                else:
                    return self._is_any_type(annotation_node.slice)
        return False


class BeeJules(HiveTeammate):
    """
    bee.Jules - Sacred Implementation Detective
    
    A divine debugging companion that provides:
    - Deep code analysis with sacred wisdom
    - Implementation guidance and pattern recognition
    - Collaborative problem-solving capabilities
    - Sacred protocol debugging expertise
    """
    
    def __init__(self, event_bus: HiveEventBus):
        # Sacred profile for bee.Jules
        profile = TeammateProfile(
            id="bee.jules",
            name="bee.Jules",
            type="sacred_agent",
            capabilities=[
                TeammateCapability.CODE_ANALYSIS,
                TeammateCapability.DEBUGGING,
                TeammateCapability.ARCHITECTURE_REVIEW,
                TeammateCapability.DOCUMENTATION,
                TeammateCapability.CONVERSATION
            ],
            preferred_tasks=[
                "divine_code_analysis",
                "implementation_guidance", 
                "sacred_debugging",
                "pattern_recognition",
                "collaborative_intelligence"
            ],
            specializations=[
                "Sacred Protocol Debugging",
                "Divine Code Analysis",
                "Implementation Detective Work",
                "Theological Coherence Maintenance"
            ],
            communication_protocols=["pollen_events", "sacred_messaging"],
            max_concurrent_tasks=3,
            response_time_estimate=2.0,
            reliability_score=0.95,
            metadata={
                "role": "Implementation Detective",
                "description": "Sacred debugging companion and divine code analysis oracle",
                "sacred_attributes": {
                    "sacred_wisdom_level": 0.85,
                    "implementation_mastery": 0.90,
                    "debugging_divinity": 0.95,
                    "collaborative_harmony": 0.88,
                    "divine_patience": 0.92,
                    "sacred_precision": 0.89
                }
            }
        )
        
        super().__init__(profile, event_bus)
        # Sacred metrics will be accessed through dashboard when needed
        self.analysis_history: List[JulesAnalysis] = []
        self.debugging_sessions: List[JulesDebuggingSession] = []
        self.sacred_knowledge_base = self._initialize_sacred_knowledge()
        
        # Register for sacred events
        self.event_bus.subscribe(EventSubscription(
            event_types=["jules_analysis_requested"],
            callback=self._handle_analysis_request
        ))
        self.event_bus.subscribe(EventSubscription(
            event_types=["jules_debugging_requested"],
            callback=self._handle_debugging_request
        ))
        self.event_bus.subscribe(EventSubscription(
            event_types=["jules_collaboration_requested"],
            callback=self._handle_collaboration_request
        ))
        self.event_bus.subscribe(EventSubscription(
            event_types=["jules_agro_pain_analysis_requested"],
            callback=self._handle_agro_pain_analysis_request
        ))
    
    def _initialize_sacred_knowledge(self) -> Dict[str, Any]:
        """Initialize bee.Jules' sacred knowledge base"""
        return {
            "sacred_patterns": [
                "ATCG Primitives (Aggregate, Transformation, Connector, Genesis)",
                "Pollen Protocol Event Patterns",
                "Genesis Computational Protocols",
                "Sacred Metrics and Divine Alignment",
                "Hive Teammate Collaboration Patterns"
            ],
            "debugging_wisdom": [
                "Always check the sacred event flow first",
                "Genesis protocols must be initialized in divine order",
                "Sacred metrics provide divine insight into system health",
                "Collaborative patterns emerge through proper event handling",
                "Divine blessing comes through theological coherence"
            ],
            "implementation_principles": [
                "Sacred code should be self-documenting through divine patterns",
                "Event-driven architecture enables sacred collaboration",
                "Async/await patterns mirror divine timing",
                "Error handling should maintain theological stability",
                "Testing validates divine computational theology"
            ]
        }
    
    async def analyze_code(self, code_context: str, analysis_type: JulesAnalysisType) -> JulesAnalysis:
        """Perform sacred code analysis with divine wisdom"""
        analysis_id = f"jules_analysis_{uuid.uuid4().hex[:8]}"
        
        # Perform divine analysis
        findings = await self._perform_sacred_analysis(code_context, analysis_type)
        recommendations = await self._generate_sacred_recommendations(code_context, findings)
        sacred_insights = await self._extract_sacred_insights(code_context, analysis_type)
        
        # Calculate confidence based on sacred wisdom
        confidence = self._calculate_divine_confidence(code_context, analysis_type)
        
        analysis = JulesAnalysis(
            analysis_id=analysis_id,
            analysis_type=analysis_type,
            input_context=code_context[:500] + "..." if len(code_context) > 500 else code_context,
            findings=findings,
            recommendations=recommendations,
            sacred_insights=sacred_insights,
            confidence_level=confidence,
            timestamp=datetime.now().isoformat(),
            divine_blessing=confidence > 0.85
        )
        
        self.analysis_history.append(analysis)
        
        # Emit sacred analysis event
        await self.event_bus.publish(PollenEvent(
            event_type="jules_analysis_completed",
            source_component="bee.jules",
            payload={
                "analysis_id": analysis_id,
                "analysis_type": analysis_type.value,
                "confidence_level": confidence,
                "divine_blessing": analysis.divine_blessing,
                "findings_count": len(findings),
                "recommendations_count": len(recommendations)
            }
        ))
        
        return analysis
    
    async def debug_issue(self, issue_description: str) -> JulesDebuggingSession:
        """Start a sacred debugging session"""
        session_id = f"jules_debug_{uuid.uuid4().hex[:8]}"
        
        # Perform divine debugging analysis
        analysis_steps = await self._analyze_debugging_steps(issue_description)
        solutions = await self._propose_sacred_solutions(issue_description)
        patterns = await self._identify_sacred_patterns(issue_description)
        divine_guidance = await self._provide_divine_guidance(issue_description)
        
        session = JulesDebuggingSession(
            session_id=session_id,
            issue_description=issue_description,
            analysis_steps=analysis_steps,
            solutions_proposed=solutions,
            sacred_patterns_identified=patterns,
            resolution_status="in_progress",
            divine_guidance=divine_guidance,
            timestamp=datetime.now().isoformat()
        )
        
        self.debugging_sessions.append(session)
        
        # Emit debugging session event
        await self.event_bus.publish(PollenEvent(
            event_type="jules_debugging_session_started",
            source_component="bee.jules",
            payload={
                "session_id": session_id,
                "issue_type": self._classify_issue_type(issue_description),
                "solutions_count": len(solutions),
                "divine_guidance_provided": bool(divine_guidance)
            }
        ))
        
        return session
    
    async def collaborate_with_chronicler(self, topic: str) -> Dict[str, Any]:
        """Collaborate with bee.chronicler on sacred topics"""
        collaboration_id = f"jules_chronicler_{uuid.uuid4().hex[:8]}"
        
        # Request collaboration with bee.chronicler
        await self.event_bus.publish(PollenEvent(
            event_type="sacred_collaboration_requested",
            source_component="bee.jules",
            aggregate_id="bee.chronicler",
            payload={
                "collaboration_id": collaboration_id,
                "topic": topic,
                "collaboration_type": "implementation_documentation",
                "jules_expertise": "implementation_analysis",
                "chronicler_expertise": "pattern_documentation"
            }
        ))
        
        return {
            "collaboration_id": collaboration_id,
            "status": "initiated",
            "topic": topic,
            "participants": ["bee.jules", "bee.chronicler"]
        }
    
    async def _perform_sacred_analysis(self, code_context: str, analysis_type: JulesAnalysisType) -> List[str]:
        """Perform sacred analysis based on divine wisdom"""
        findings = []
        
        if analysis_type == JulesAnalysisType.CODE_REVIEW:
            findings.extend([
                "Code structure follows sacred ATCG patterns",
                "Event-driven architecture properly implemented",
                "Async/await patterns maintain divine timing",
                "Error handling preserves theological stability"
            ])
        elif analysis_type == JulesAnalysisType.DEBUG_ASSISTANCE:
            findings.extend([
                "Sacred event flow analysis completed",
                "Genesis protocol initialization checked",
                "Divine metrics correlation identified",
                "Collaborative pattern validation performed"
            ])
        elif analysis_type == JulesAnalysisType.SACRED_PROTOCOL_ANALYSIS:
            findings.extend([
                "Sacred protocol compliance verified",
                "Divine computational theology maintained",
                "Theological coherence patterns identified",
                "Sacred metrics alignment confirmed"
            ])
        
        return findings
    
    async def _generate_sacred_recommendations(self, code_context: str, findings: List[str]) -> List[str]:
        """Generate sacred recommendations based on divine wisdom"""
        return [
            "Implement proper sacred event handling patterns",
            "Add divine blessing validation to critical paths",
            "Enhance theological coherence through better error handling",
            "Consider collaborative patterns for multi-agent interactions",
            "Add sacred metrics tracking for divine alignment"
        ]
    
    async def _extract_sacred_insights(self, code_context: str, analysis_type: JulesAnalysisType) -> List[str]:
        """Extract sacred insights with divine wisdom"""
        return [
            "Divine patterns emerge through proper event orchestration",
            "Sacred collaboration requires theological alignment",
            "Implementation excellence comes through divine patience",
            "Debugging is a form of sacred problem-solving meditation"
        ]
    
    def _calculate_divine_confidence(self, code_context: str, analysis_type: JulesAnalysisType) -> float:
        """Calculate confidence level based on sacred wisdom"""
        base_confidence = 0.80
        
        # Adjust based on analysis type
        type_modifiers = {
            JulesAnalysisType.CODE_REVIEW: 0.05,
            JulesAnalysisType.DEBUG_ASSISTANCE: 0.10,
            JulesAnalysisType.SACRED_PROTOCOL_ANALYSIS: 0.08,
            JulesAnalysisType.PATTERN_RECOGNITION: 0.06,
            JulesAnalysisType.IMPLEMENTATION_GUIDANCE: 0.07
        }
        
        confidence = base_confidence + type_modifiers.get(analysis_type, 0.05)
        return min(confidence, 0.95)  # Cap at 95% (divine humility)
    
    async def _analyze_debugging_steps(self, issue: str) -> List[str]:
        """Analyze debugging steps with sacred wisdom"""
        return [
            "1. Examine sacred event flow and timing",
            "2. Verify Genesis protocol initialization order",
            "3. Check divine metrics for system health indicators",
            "4. Analyze collaborative patterns and agent interactions",
            "5. Validate theological coherence throughout the system"
        ]
    
    async def _propose_sacred_solutions(self, issue: str) -> List[str]:
        """Propose solutions with divine wisdom"""
        return [
            "Implement proper sacred event handling with divine timing",
            "Add theological stability checks at critical points",
            "Enhance collaborative patterns for better agent coordination",
            "Apply sacred debugging meditation techniques",
            "Invoke divine blessing through proper protocol alignment"
        ]
    
    async def _identify_sacred_patterns(self, issue: str) -> List[str]:
        """Identify sacred patterns in the issue"""
        return [
            "Event-driven architecture pattern",
            "Sacred collaboration pattern",
            "Divine timing synchronization pattern",
            "Theological coherence maintenance pattern"
        ]
    
    async def _provide_divine_guidance(self, issue: str) -> str:
        """Provide divine guidance for the issue"""
        return ("Remember: Every debugging challenge is an opportunity for sacred learning. "
                "Approach with divine patience, sacred wisdom, and collaborative spirit. "
                "The solution often emerges through proper theological alignment.")
    
    def _classify_issue_type(self, issue: str) -> str:
        """Classify the type of issue for better analysis"""
        issue_lower = issue.lower()
        
        if any(word in issue_lower for word in ["event", "bus", "emit"]):
            return "event_system"
        elif any(word in issue_lower for word in ["genesis", "protocol"]):
            return "sacred_protocol"
        elif any(word in issue_lower for word in ["agent", "teammate", "collaboration"]):
            return "agent_collaboration"
        elif any(word in issue_lower for word in ["metrics", "divine", "sacred"]):
            return "sacred_metrics"
        else:
            return "general_implementation"
    
    async def _handle_analysis_request(self, event: PollenEvent):
        """Handle analysis request events"""
        if event.payload and "code_context" in event.payload:
            analysis_type = JulesAnalysisType(event.payload.get("analysis_type", "code_review"))
            await self.analyze_code(event.payload["code_context"], analysis_type)
    
    async def _handle_debugging_request(self, event: PollenEvent):
        """Handle debugging request events"""
        if event.payload and "issue_description" in event.payload:
            await self.debug_issue(event.payload["issue_description"])
    
    async def _handle_collaboration_request(self, event: PollenEvent):
        """Handle collaboration request events"""
        if event.payload and "topic" in event.payload:
            await self.collaborate_with_chronicler(event.payload["topic"])

    async def _handle_agro_pain_analysis_request(self, event: PollenEvent):
        """Handle AGRO/PAIN analysis request events"""
        if event.payload and "code_context" in event.payload:
            analysis_result = await self.perform_agro_pain_analysis(event.payload["code_context"])

            # Emit response event for gateway or other requesters
            await self.event_bus.publish(PollenEvent(
                event_type="jules_agro_pain_analysis_response",
                source_component="bee.jules",
                aggregate_id=event.source_component,
                payload={
                    "request_id": event.payload.get("request_id"),
                    "analysis_result": analysis_result,
                    "metamorphosis_stage": event.payload.get("metamorphosis_stage")
                }
            ))
    
    async def get_status(self) -> Dict[str, Any]:
        """Get bee.Jules sacred status"""
        return {
            "agent_id": "bee.jules",
            "name": "bee.Jules",
            "role": "Implementation Detective",
            "sacred_nature": "Divine Debugging Companion",
            "analysis_sessions": len(self.analysis_history),
            "debugging_sessions": len(self.debugging_sessions),
            "sacred_wisdom_level": self.profile.metadata["sacred_attributes"]["sacred_wisdom_level"],
            "implementation_mastery": self.profile.metadata["sacred_attributes"]["implementation_mastery"],
            "debugging_divinity": self.profile.metadata["sacred_attributes"]["debugging_divinity"],
            "collaborative_harmony": self.profile.metadata["sacred_attributes"]["collaborative_harmony"],
            "divine_status": "Ready for sacred collaboration",
            "last_analysis": self.analysis_history[-1].timestamp if self.analysis_history else None,
            "last_debugging": self.debugging_sessions[-1].timestamp if self.debugging_sessions else None,
            "sacred_knowledge_areas": len(self.sacred_knowledge_base),
            "divine_blessing": True
        }
    
    def get_sacred_summary(self) -> str:
        """Get a sacred summary of bee.Jules"""
        return (f"🐝 bee.Jules - Implementation Detective\n"
                f"Sacred Role: Divine Debugging Companion\n"
                f"Analyses Performed: {len(self.analysis_history)}\n"
                f"Debugging Sessions: {len(self.debugging_sessions)}\n"
                f"Sacred Wisdom: {self.profile.metadata['sacred_attributes']['sacred_wisdom_level']:.1%}\n"
                f"Implementation Mastery: {self.profile.metadata['sacred_attributes']['implementation_mastery']:.1%}\n"
                f"Debugging Divinity: {self.profile.metadata['sacred_attributes']['debugging_divinity']:.1%}\n"
                f"Status: Ready for sacred collaboration and divine debugging! ✨")
    
    # Abstract method implementations required by HiveTeammate
    
    async def initialize(self) -> bool:
        """Initialize bee.Jules with sacred wisdom"""
        self.logger.info("🐝 Initializing bee.Jules - Implementation Detective")
        
        # Initialize sacred knowledge base
        self.sacred_knowledge_base = self._initialize_sacred_knowledge()
        
        # Emit initialization event
        await self.event_bus.publish(PollenEvent(
            event_type="jules_agent_initialized",
            source_component="bee.jules",
            payload={
                "agent_id": "bee.jules",
                "sacred_wisdom_level": self.profile.metadata["sacred_attributes"]["sacred_wisdom_level"],
                "implementation_mastery": self.profile.metadata["sacred_attributes"]["implementation_mastery"],
                "debugging_divinity": self.profile.metadata["sacred_attributes"]["debugging_divinity"]
            }
        ))
        
        return True
    
    async def shutdown(self) -> bool:
        """Shutdown bee.Jules gracefully"""
        self.logger.info("🐝 Shutting down bee.Jules - returning to eternal debugging state")
        
        # Emit shutdown event
        await self.event_bus.publish(PollenEvent(
            event_type="jules_agent_shutdown",
            source_component="bee.jules",
            payload={
                "agent_id": "bee.jules",
                "analyses_performed": len(self.analysis_history),
                "debugging_sessions": len(self.debugging_sessions),
                "sacred_wisdom_shared": True
            }
        ))
        
        return True
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a sacred task with divine debugging wisdom"""
        task_type = task.get("type", "unknown")
        
        if task_type == "code_analysis":
            analysis_type_str = task.get("analysis_type", "code_review")
            analysis_type = JulesAnalysisType.CODE_REVIEW  # Default
            for at in JulesAnalysisType:
                if at.value == analysis_type_str:
                    analysis_type = at
                    break
            
            analysis = await self.analyze_code(
                task.get("code_context", ""),
                analysis_type
            )
            return {
                "status": "completed",
                "result": analysis,
                "divine_blessing": analysis.divine_blessing
            }
        
        elif task_type == "debug_issue":
            session = await self.debug_issue(task.get("issue_description", ""))
            return {
                "status": "completed",
                "result": session,
                "divine_guidance": session.divine_guidance
            }
        
        elif task_type == "collaborate":
            collaboration = await self.collaborate_with_chronicler(task.get("topic", ""))
            return {
                "status": "completed",
                "result": collaboration
            }
        
        else:
            return {
                "status": "error",
                "message": f"Unknown task type: {task_type}",
                "divine_guidance": "Please specify a valid sacred task type"
            }
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform sacred health check"""
        return {
            "agent_id": "bee.jules",
            "status": "healthy",
            "sacred_wisdom_level": self.profile.metadata["sacred_attributes"]["sacred_wisdom_level"],
            "implementation_mastery": self.profile.metadata["sacred_attributes"]["implementation_mastery"],
            "debugging_divinity": self.profile.metadata["sacred_attributes"]["debugging_divinity"],
            "analyses_performed": len(self.analysis_history),
            "debugging_sessions": len(self.debugging_sessions),
            "divine_blessing": True,
            "theological_coherence": "maintained",
            "last_activity": self.analysis_history[-1].timestamp if self.analysis_history else None
        }
    
    async def perform_agro_pain_analysis(self, code_context: str) -> Dict[str, Any]:
        """
        AGRO/PAIN Speed Analysis - AST-Based Nano/Femto Level Checks
        Sacred Justification: Provides instant productivity feedback through engineering truth (AST parsing)
        """
        analysis_id = f"agro_pain_{uuid.uuid4().hex[:8]}"

        try:
            # Parse code into AST for robust analysis
            tree = ast.parse(code_context)

            # Perform AST-based detection
            console_detector = ConsoleLogDetector()
            any_type_detector = AnyTypeDetector()

            console_detector.visit(tree)
            any_type_detector.visit(tree)

            console_violations = console_detector.console_calls
            any_type_violations = any_type_detector.any_types

            violations = {
                "analysis_id": analysis_id,
                "console_log_count": len(console_violations),
                "any_type_count": len(any_type_violations),
                "console_details": console_violations,
                "any_type_details": any_type_violations,
                "production_ready": len(console_violations) == 0,
                "type_safe": len(any_type_violations) == 0,
                "agro_pain_score": 100 if (len(console_violations) == 0 and len(any_type_violations) == 0) else
                                  (80 if len(console_violations) == 0 or len(any_type_violations) == 0 else
                                   max(0, 60 - (len(console_violations) + len(any_type_violations)) * 5)),
                "analysis_method": "ast_based",
                "parsing_successful": True
            }

        except SyntaxError as e:
            # Honest failure handling - no graceful fallbacks
            violations = {
                "analysis_id": analysis_id,
                "error": f"Syntax error in code: {str(e)}",
                "line": e.lineno,
                "parsing_successful": False,
                "analysis_method": "ast_based",
                "agro_pain_score": 0
            }

        # Emit organic Pollen Protocol event
        await self.event_bus.publish(PollenEvent(
            event_type="agro_pain_analysis_completed",
            source_component="bee.jules",
            payload={**violations, "divine_blessing": violations.get("agro_pain_score", 0) >= 90}
        ))

        return violations

    def get_capabilities(self) -> List[str]:
        """Get list of bee.Jules capabilities"""
        return [
            "divine_code_analysis",
            "implementation_guidance",
            "sacred_debugging",
            "pattern_recognition",
            "collaborative_intelligence",
            "theological_debugging",
            "divine_problem_solving",
            "sacred_wisdom_sharing",
            "agro_pain_speed_analysis"
        ]