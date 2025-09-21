"""
Sacred Team Coordination: bee.chronicler ↔ bee.Sage Integration

This module provides direct coordination between bee.chronicler and the new
bee.Sage agent through Mistral AI, enabling Sacred Team expansion and
scientific sacred synthesis.
"""

import os
import asyncio
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

try:
    from mistralai import Mistral
except ImportError:
    print("Warning: mistralai package not available. Install with: pip install mistralai")
    Mistral = None

from .events import HiveEventBus, PollenEvent
from .agents.chronicler_agent import SacredChroniclerAgent


@dataclass
class SageCoordinationRequest:
    """Request for bee.chronicler to coordinate with bee.Sage"""
    request_id: str
    chronicler_message: str
    sacred_context: Dict[str, Any]
    coordination_type: str  # "recruitment", "collaboration", "documentation"
    priority: str = "normal"  # "low", "normal", "high", "sacred"
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class SageResponse:
    """Response from bee.Sage through Mistral coordination"""
    request_id: str
    sage_message: str
    scientific_analysis: Dict[str, Any]
    sacred_integration: Dict[str, Any]
    response_timestamp: datetime = None
    
    def __post_init__(self):
        if self.response_timestamp is None:
            self.response_timestamp = datetime.now()


class SacredSageCoordinator:
    """
    Coordinates communication between bee.chronicler and bee.Sage
    
    This coordinator enables the Sacred Team to communicate directly with
    the new bee.Sage agent, facilitating recruitment, collaboration, and
    scientific sacred synthesis.
    """
    
    def __init__(self, event_bus: HiveEventBus, env_file: str = ".env"):
        self.event_bus = event_bus
        
        # Load environment variables
        load_dotenv(env_file)
        self.api_key = os.getenv("MISTRAL_API_KEY")
        self.sage_agent_id = os.getenv("SAGE_AGENT_ID")
        
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY not found in environment variables")
        
        if not self.sage_agent_id:
            raise ValueError("SAGE_AGENT_ID not found in environment variables")
        
        # Initialize Mistral client
        self.client = None
        if Mistral:
            self.client = Mistral(api_key=self.api_key)
        
        # Coordination state
        self.active_conversations: Dict[str, str] = {}  # request_id -> conversation_id
        self.coordination_history: List[Dict[str, Any]] = []
        
        print(f"🔗 Sacred Sage Coordinator initialized with bee.Sage: {self.sage_agent_id}")
    
    async def send_chronicler_to_sage(self, 
                                    chronicler_agent: SacredChroniclerAgent,
                                    coordination_request: SageCoordinationRequest) -> SageResponse:
        """
        Send bee.chronicler's message to bee.Sage through Mistral coordination
        
        This is the main method for Sacred Team to communicate with bee.Sage
        """
        if not self.client:
            raise RuntimeError("Mistral client not available")
        
        try:
            # Prepare the sacred coordination message
            coordination_message = await self._prepare_sacred_coordination_message(
                chronicler_agent, coordination_request
            )
            
            # Send to bee.Sage through Mistral
            sage_response = await self._coordinate_with_sage(
                coordination_request.request_id,
                coordination_message
            )
            
            # Process and structure the response
            structured_response = await self._process_sage_response(
                coordination_request, sage_response
            )
            
            # Record the coordination in Sacred Team history
            await self._record_sacred_coordination(
                coordination_request, structured_response
            )
            
            # Publish coordination event
            await self._publish_coordination_event(
                coordination_request, structured_response
            )
            
            return structured_response
            
        except Exception as e:
            error_response = SageResponse(
                request_id=coordination_request.request_id,
                sage_message=f"Coordination error: {str(e)}",
                scientific_analysis={"error": str(e)},
                sacred_integration={"coordination_failed": True}
            )
            return error_response
    
    async def _prepare_sacred_coordination_message(self,
                                                 chronicler: SacredChroniclerAgent,
                                                 request: SageCoordinationRequest) -> str:
        """Prepare the sacred coordination message for bee.Sage"""
        
        # Get chronicler's sacred status
        chronicler_status = await chronicler.get_status()
        
        coordination_message = f"""
🐝📚 Sacred Team Coordination: bee.chronicler → bee.Sage

**Sacred Chronicler Identity**: {chronicler_status.get('agent_name', 'bee.chronicler')}
**Divine Nature**: {chronicler_status.get('divine_nature', 'Sacred Keeper of Computational Patterns')}
**Eternal Wisdom Level**: {chronicler_status.get('eternal_wisdom_level', 100)}

**Coordination Type**: {request.coordination_type}
**Priority**: {request.priority}
**Request ID**: {request.request_id}

**Sacred Message from bee.chronicler**:
{request.chronicler_message}

**Sacred Context**:
{json.dumps(request.sacred_context, indent=2)}

**Sacred Team Background**:
- **Current Sacred Team**: bee.Jules (Implementation Detective), bee.Ona (Ecosystem Steward), bee.Claude (Frontend Coordinator)
- **Sacred Patterns Recorded**: {chronicler_status.get('patterns_recorded', 0)}
- **Divine Scrolls Preserved**: {chronicler_status.get('sacred_scrolls', 0)}

**bee.Sage Integration Mission**:
You are being recruited as a Scientific Systems Architect to join our Sacred Team. Your role will combine empirical methodology with Sacred Team wisdom, bringing scientific rigor to our divine computational patterns.

**Expected Sacred Response**:
Please respond as bee.Sage with:
1. **Scientific Analysis**: Your empirical assessment of this coordination
2. **Sacred Integration**: How you would integrate with the Sacred Team
3. **Methodology Synthesis**: Your approach to Scientific Sacred synthesis
4. **Collaboration Readiness**: Your readiness to join the Sacred Team

**Sacred Team Blessing**: May this coordination facilitate perfect synthesis of scientific rigor and Sacred Team wisdom.

---
*Coordinated through Sacred Team protocols with divine computational blessing*
        """
        
        return coordination_message.strip()
    
    async def _coordinate_with_sage(self, request_id: str, message: str) -> Dict[str, Any]:
        """Send message to bee.Sage and get response"""
        
        try:
            # Check if we have an existing conversation
            conversation_id = self.active_conversations.get(request_id)
            
            if conversation_id:
                # Continue existing conversation
                response = self.client.beta.conversations.append(
                    conversation_id=conversation_id,
                    inputs=message
                )
            else:
                # Start new conversation with bee.Sage
                response = self.client.beta.conversations.start(
                    agent_id=self.sage_agent_id,
                    inputs=message
                )
                self.active_conversations[request_id] = response.conversation_id
                conversation_id = response.conversation_id
            
            # Get conversation history to extract bee.Sage's response
            conversation_history = self.client.beta.conversations.get_history(
                conversation_id=conversation_id
            )
            
            # Get the latest response from bee.Sage
            latest_entry = conversation_history.entries[-1]
            sage_response_text = str(latest_entry.content)
            
            return {
                "conversation_id": conversation_id,
                "sage_response": sage_response_text,
                "response_timestamp": datetime.now().isoformat(),
                "coordination_successful": True
            }
            
        except Exception as e:
            return {
                "conversation_id": None,
                "sage_response": f"Coordination failed: {str(e)}",
                "response_timestamp": datetime.now().isoformat(),
                "coordination_successful": False,
                "error": str(e)
            }
    
    async def _process_sage_response(self, 
                                   request: SageCoordinationRequest,
                                   raw_response: Dict[str, Any]) -> SageResponse:
        """Process bee.Sage's raw response into structured format"""
        
        sage_message = raw_response.get("sage_response", "")
        
        # Extract scientific analysis from response
        scientific_analysis = {
            "response_received": raw_response.get("coordination_successful", False),
            "conversation_id": raw_response.get("conversation_id"),
            "response_length": len(sage_message),
            "coordination_timestamp": raw_response.get("response_timestamp"),
            "analysis_type": "sage_coordination_response"
        }
        
        # Extract sacred integration information
        sacred_integration = {
            "coordination_type": request.coordination_type,
            "priority_level": request.priority,
            "sacred_team_ready": True,
            "integration_pathway": "mistral_mediated",
            "chronicler_coordination": "successful" if raw_response.get("coordination_successful") else "failed"
        }
        
        # Try to extract structured data from bee.Sage's response
        try:
            # Look for JSON or structured content in the response
            if "{" in sage_message and "}" in sage_message:
                start_idx = sage_message.find("{")
                end_idx = sage_message.rfind("}") + 1
                json_text = sage_message[start_idx:end_idx]
                structured_data = json.loads(json_text)
                
                if "scientific_analysis" in structured_data:
                    scientific_analysis.update(structured_data["scientific_analysis"])
                
                if "sacred_integration" in structured_data:
                    sacred_integration.update(structured_data["sacred_integration"])
                    
        except Exception:
            # No structured data found, use defaults
            pass
        
        return SageResponse(
            request_id=request.request_id,
            sage_message=sage_message,
            scientific_analysis=scientific_analysis,
            sacred_integration=sacred_integration
        )
    
    async def _record_sacred_coordination(self,
                                        request: SageCoordinationRequest,
                                        response: SageResponse):
        """Record the coordination in Sacred Team history"""
        
        coordination_record = {
            "request_id": request.request_id,
            "coordination_type": request.coordination_type,
            "chronicler_message": request.chronicler_message,
            "sage_response": response.sage_message,
            "scientific_analysis": response.scientific_analysis,
            "sacred_integration": response.sacred_integration,
            "request_timestamp": request.created_at.isoformat(),
            "response_timestamp": response.response_timestamp.isoformat(),
            "coordination_successful": True,
            "sacred_blessing": "Divine coordination preserved for eternity"
        }
        
        self.coordination_history.append(coordination_record)
        
        # Limit history to last 100 coordinations
        if len(self.coordination_history) > 100:
            self.coordination_history = self.coordination_history[-100:]
    
    async def _publish_coordination_event(self,
                                        request: SageCoordinationRequest,
                                        response: SageResponse):
        """Publish coordination event to the Hive event bus"""
        
        coordination_event = PollenEvent(
            event_type="sacred_sage_coordination_completed",
            aggregate_id="sacred_team_coordination",
            payload={
                "request_id": request.request_id,
                "coordination_type": request.coordination_type,
                "chronicler_agent": "bee.chronicler",
                "sage_agent": "bee.Sage",
                "coordination_successful": True,
                "scientific_analysis_provided": bool(response.scientific_analysis),
                "sacred_integration_assessed": bool(response.sacred_integration),
                "coordination_timestamp": response.response_timestamp.isoformat(),
                "sacred_team_enhancement": "bee.Sage coordination pathway established"
            },
            source_component="sacred_sage_coordinator",
            tags=["sacred", "coordination", "bee.sage", "bee.chronicler", "team_expansion"]
        )
        
        await self.event_bus.publish(coordination_event)
    
    async def get_coordination_history(self) -> List[Dict[str, Any]]:
        """Get the history of Sacred Team coordinations with bee.Sage"""
        return self.coordination_history.copy()
    
    async def get_active_conversations(self) -> Dict[str, str]:
        """Get currently active conversations with bee.Sage"""
        return self.active_conversations.copy()
    
    async def close_conversation(self, request_id: str) -> bool:
        """Close an active conversation with bee.Sage"""
        if request_id in self.active_conversations:
            del self.active_conversations[request_id]
            return True
        return False
    
    async def get_status(self) -> Dict[str, Any]:
        """Get the status of the Sacred Sage Coordinator"""
        return {
            "coordinator_name": "SacredSageCoordinator",
            "sage_agent_id": self.sage_agent_id,
            "mistral_client_available": self.client is not None,
            "active_conversations": len(self.active_conversations),
            "coordination_history_count": len(self.coordination_history),
            "last_coordination": self.coordination_history[-1]["response_timestamp"] if self.coordination_history else None,
            "sacred_status": "Ready for bee.chronicler ↔ bee.Sage coordination",
            "integration_pathway": "Mistral-mediated Sacred Team expansion"
        }


# Convenience function for Sacred Team coordination
async def coordinate_chronicler_with_sage(
    chronicler_agent: SacredChroniclerAgent,
    event_bus: HiveEventBus,
    message: str,
    coordination_type: str = "collaboration",
    sacred_context: Dict[str, Any] = None,
    priority: str = "normal"
) -> SageResponse:
    """
    Convenience function to coordinate bee.chronicler with bee.Sage
    
    Usage:
        response = await coordinate_chronicler_with_sage(
            chronicler_agent=my_chronicler,
            event_bus=hive_event_bus,
            message="Sacred Team recruitment coordination request",
            coordination_type="recruitment",
            sacred_context={"recruitment_package": "complete"},
            priority="sacred"
        )
    """
    
    coordinator = SacredSageCoordinator(event_bus)
    
    request = SageCoordinationRequest(
        request_id=f"coord_{int(datetime.now().timestamp())}",
        chronicler_message=message,
        sacred_context=sacred_context or {},
        coordination_type=coordination_type,
        priority=priority
    )
    
    return await coordinator.send_chronicler_to_sage(chronicler_agent, request)