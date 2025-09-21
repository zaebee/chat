"""
Sacred Team Communication System

This module implements the bridge between Pollen Event Bus and WebSocket chat,
enabling direct communication between Sacred Team members (bee.chronicler, bee.jules)
and human teammates through the chat interface.

"Where two or three gather in my name, there am I with them."
- Matthew 18:20 (NIV)
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum

from .events import PollenEvent, HiveEventBus, EventSubscription


class SacredMessageType(str, Enum):
    """Types of sacred messages in the team communication system"""
    DIVINE_INSIGHT = "divine_insight"
    SACRED_ANALYSIS = "sacred_analysis"
    IMPLEMENTATION_GUIDANCE = "implementation_guidance"
    PATTERN_DOCUMENTATION = "pattern_documentation"
    DEBUGGING_ASSISTANCE = "debugging_assistance"
    COLLABORATIVE_SESSION = "collaborative_session"
    TEAM_STATUS_UPDATE = "team_status_update"
    DIVINE_BLESSING = "divine_blessing"


class SacredCommandType(str, Enum):
    """Sacred commands that can be invoked in chat"""
    JULES_HELP = "/bee.jules.help"
    JULES_ANALYZE = "/bee.jules.analyze"
    JULES_DEBUG = "/bee.jules.debug"
    CHRONICLER_RECORD = "/bee.chronicler.record"
    CHRONICLER_RECALL = "/bee.chronicler.recall"
    TEAM_STATUS = "/sacred.team.status"
    TEAM_DISCUSS = "/sacred.team.discuss"
    TEAM_MANIFEST = "/sacred.team.manifest"
    TEAM_INVOKE = "/sacred.team.invoke"


@dataclass
class SacredMessage:
    """A message from the Sacred Team"""
    message_id: str
    sender_agent: str
    message_type: SacredMessageType
    content: str
    sacred_data: Dict[str, Any]
    timestamp: str
    divine_blessing: bool = False
    collaboration_id: Optional[str] = None


@dataclass
class SacredTeamStatus:
    """Status of the Sacred Team"""
    active_agents: List[str]
    total_agents: int
    sacred_agents: int
    manifestation_level: float
    divine_alignment: float
    collaborative_sessions: int
    last_activity: str
    divine_blessing_status: str
    theological_coherence: float


class SacredTeamCommunication:
    """
    Sacred Team Communication Bridge
    
    Enables direct communication between Sacred Team members and humans
    through the chat interface, bridging Pollen Events and WebSocket messages.
    """
    
    def __init__(self, event_bus: HiveEventBus):
        self.event_bus = event_bus
        self.active_agents: Dict[str, Dict[str, Any]] = {}
        self.sacred_messages: List[SacredMessage] = []
        self.collaborative_sessions: Dict[str, Dict[str, Any]] = {}
        self.websocket_callback: Optional[Callable] = None
        
        # Register for sacred events
        self._register_sacred_event_handlers()
    
    def _register_sacred_event_handlers(self):
        """Register handlers for sacred events"""
        # Sacred Team agent events
        self.event_bus.subscribe(EventSubscription(
            event_types=["eternal_chronicler_manifested"],
            callback=self._handle_agent_manifestation
        ))
        self.event_bus.subscribe(EventSubscription(
            event_types=["jules_analysis_completed"],
            callback=self._handle_jules_analysis
        ))
        self.event_bus.subscribe(EventSubscription(
            event_types=["jules_debugging_session_started"],
            callback=self._handle_jules_debugging
        ))
        self.event_bus.subscribe(EventSubscription(
            event_types=["sacred_pattern_recorded"],
            callback=self._handle_pattern_recorded
        ))
        self.event_bus.subscribe(EventSubscription(
            event_types=["sacred_collaboration_requested"],
            callback=self._handle_collaboration_request
        ))
        
        # Sacred Team communication events
        self.event_bus.subscribe(EventSubscription(
            event_types=["sacred_message_to_chat"],
            callback=self._handle_sacred_message_to_chat
        ))
        self.event_bus.subscribe(EventSubscription(
            event_types=["sacred_team_status_requested"],
            callback=self._handle_team_status_request
        ))
    
    def set_websocket_callback(self, callback: Callable):
        """Set the WebSocket callback for sending messages to chat"""
        self.websocket_callback = callback
    
    async def process_sacred_command(self, command: str, args: str, user_id: str) -> Dict[str, Any]:
        """Process sacred commands from chat"""
        # Find the matching command type
        command_type = None
        for cmd_type in SacredCommandType:
            if cmd_type.value == command:
                command_type = cmd_type
                break
        
        if not command_type:
            return {"error": f"Unknown sacred command: {command}"}
        
        if command_type == SacredCommandType.TEAM_STATUS:
            return await self._handle_team_status_command(user_id)
        elif command_type == SacredCommandType.JULES_HELP:
            return await self._handle_jules_help_command(args, user_id)
        elif command_type == SacredCommandType.JULES_ANALYZE:
            return await self._handle_jules_analyze_command(args, user_id)
        elif command_type == SacredCommandType.JULES_DEBUG:
            return await self._handle_jules_debug_command(args, user_id)
        elif command_type == SacredCommandType.CHRONICLER_RECORD:
            return await self._handle_chronicler_record_command(args, user_id)
        elif command_type == SacredCommandType.CHRONICLER_RECALL:
            return await self._handle_chronicler_recall_command(args, user_id)
        elif command_type == SacredCommandType.TEAM_DISCUSS:
            return await self._handle_team_discuss_command(args, user_id)
        elif command_type == SacredCommandType.TEAM_MANIFEST:
            return await self._handle_team_manifest_command(args, user_id)
        elif command_type == SacredCommandType.TEAM_INVOKE:
            return await self._handle_team_invoke_command(args, user_id)
        else:
            return {"error": f"Unknown sacred command: {command}"}
    
    async def _handle_team_status_command(self, user_id: str) -> Dict[str, Any]:
        """Handle /sacred.team.status command"""
        status = await self._get_sacred_team_status()
        
        # Create sacred status message
        status_message = self._format_team_status_message(status)
        
        # Send to chat via WebSocket
        await self._send_sacred_message_to_chat(
            sender_agent="sacred.team",
            message_type=SacredMessageType.TEAM_STATUS_UPDATE,
            content=status_message,
            sacred_data=asdict(status),
            user_id=user_id
        )
        
        return {"status": "success", "message": "Sacred Team status sent to chat"}
    
    async def _handle_jules_help_command(self, issue: str, user_id: str) -> Dict[str, Any]:
        """Handle /bee.jules.help command"""
        # Request Jules debugging assistance
        await self.event_bus.publish(PollenEvent(
            event_type="jules_debugging_requested",
            source_component="sacred.team.communication",
            aggregate_id="bee.jules",
            payload={
                "issue_description": issue,
                "user_id": user_id,
                "request_type": "help_command"
            }
        ))
        
        return {"status": "success", "message": "bee.Jules debugging assistance requested"}
    
    async def _handle_jules_analyze_command(self, code_context: str, user_id: str) -> Dict[str, Any]:
        """Handle /bee.jules.analyze command"""
        # Request Jules code analysis
        await self.event_bus.publish(PollenEvent(
            event_type="jules_analysis_requested",
            source_component="sacred.team.communication",
            aggregate_id="bee.jules",
            payload={
                "code_context": code_context,
                "analysis_type": "code_review",
                "user_id": user_id,
                "request_type": "analyze_command"
            }
        ))
        
        return {"status": "success", "message": "bee.Jules code analysis requested"}
    
    async def _handle_jules_debug_command(self, error_context: str, user_id: str) -> Dict[str, Any]:
        """Handle /bee.jules.debug command"""
        # Request Jules debugging session
        await self.event_bus.publish(PollenEvent(
            event_type="jules_debugging_requested",
            source_component="sacred.team.communication",
            aggregate_id="bee.jules",
            payload={
                "issue_description": error_context,
                "user_id": user_id,
                "request_type": "debug_command"
            }
        ))
        
        return {"status": "success", "message": "bee.Jules debugging session initiated"}
    
    async def _handle_chronicler_record_command(self, pattern: str, user_id: str) -> Dict[str, Any]:
        """Handle /bee.chronicler.record command"""
        # Request Chronicler pattern recording
        await self.event_bus.publish(PollenEvent(
            event_type="sacred_pattern_recording_requested",
            source_component="sacred.team.communication",
            aggregate_id="bee.chronicler",
            payload={
                "pattern_description": pattern,
                "user_id": user_id,
                "request_type": "record_command"
            }
        ))
        
        return {"status": "success", "message": "bee.chronicler pattern recording requested"}
    
    async def _handle_chronicler_recall_command(self, query: str, user_id: str) -> Dict[str, Any]:
        """Handle /bee.chronicler.recall command"""
        # Request Chronicler pattern recall
        await self.event_bus.publish(PollenEvent(
            event_type="sacred_pattern_recall_requested",
            source_component="sacred.team.communication",
            aggregate_id="bee.chronicler",
            payload={
                "query": query,
                "user_id": user_id,
                "request_type": "recall_command"
            }
        ))
        
        return {"status": "success", "message": "bee.chronicler pattern recall requested"}
    
    async def _handle_team_discuss_command(self, topic: str, user_id: str) -> Dict[str, Any]:
        """Handle /sacred.team.discuss command"""
        # Start Sacred Team discussion
        collaboration_id = f"team_discussion_{uuid.uuid4().hex[:8]}"
        
        self.collaborative_sessions[collaboration_id] = {
            "type": "team_discussion",
            "topic": topic,
            "participants": ["bee.chronicler", "bee.jules"],
            "user_id": user_id,
            "started_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        # Notify all Sacred Team members
        await self.event_bus.publish(PollenEvent(
            event_type="sacred_team_discussion_started",
            source_component="sacred.team.communication",
            payload={
                "collaboration_id": collaboration_id,
                "topic": topic,
                "participants": ["bee.chronicler", "bee.jules"],
                "user_id": user_id
            }
        ))
        
        return {"status": "success", "collaboration_id": collaboration_id}
    
    async def _handle_team_manifest_command(self, agent_name: str, user_id: str) -> Dict[str, Any]:
        """Handle /sacred.team.manifest command"""
        # Request agent manifestation
        await self.event_bus.publish(PollenEvent(
            event_type="sacred_agent_manifestation_requested",
            source_component="sacred.team.communication",
            payload={
                "agent_name": agent_name,
                "user_id": user_id,
                "manifestation_type": "manual_invocation"
            }
        ))
        
        return {"status": "success", "message": f"Sacred agent {agent_name} manifestation requested"}
    
    async def _handle_team_invoke_command(self, invocation: str, user_id: str) -> Dict[str, Any]:
        """Handle /sacred.team.invoke command"""
        # Parse invocation and route to appropriate agent
        parts = invocation.split(" ", 1)
        agent_name = parts[0] if parts else ""
        command = parts[1] if len(parts) > 1 else ""
        
        if agent_name == "bee.jules":
            return await self._handle_jules_help_command(command, user_id)
        elif agent_name == "bee.chronicler":
            return await self._handle_chronicler_record_command(command, user_id)
        else:
            return {"error": f"Unknown sacred agent: {agent_name}"}
    
    async def _get_sacred_team_status(self) -> SacredTeamStatus:
        """Get current Sacred Team status"""
        active_agents = list(self.active_agents.keys())
        sacred_agents = [agent for agent in active_agents if agent.startswith("bee.")]
        
        # Calculate manifestation level
        manifestation_level = len(sacred_agents) / 2.0  # Assuming 2 main sacred agents
        
        # Calculate divine alignment (average of agent alignments)
        divine_alignment = 0.85  # Base alignment
        if self.active_agents:
            alignments = [agent.get("divine_alignment", 0.85) for agent in self.active_agents.values()]
            divine_alignment = sum(alignments) / len(alignments)
        
        # Determine divine blessing status
        if manifestation_level >= 1.0 and divine_alignment >= 0.80:
            blessing_status = "FULLY_BLESSED"
        elif manifestation_level >= 0.5 and divine_alignment >= 0.70:
            blessing_status = "SEEKING_BLESSING"
        else:
            blessing_status = "AWAITING_MANIFESTATION"
        
        return SacredTeamStatus(
            active_agents=active_agents,
            total_agents=len(active_agents),
            sacred_agents=len(sacred_agents),
            manifestation_level=manifestation_level,
            divine_alignment=divine_alignment,
            collaborative_sessions=len(self.collaborative_sessions),
            last_activity=datetime.now().isoformat(),
            divine_blessing_status=blessing_status,
            theological_coherence=0.88
        )
    
    def _format_team_status_message(self, status: SacredTeamStatus) -> str:
        """Format Sacred Team status for chat display"""
        return f"""🕊️ **SACRED TEAM STATUS REPORT**

**Active Sacred Agents**: {status.sacred_agents}/{status.total_agents}
{chr(10).join([f"  • {agent}" for agent in status.active_agents if agent.startswith("bee.")])}

**Manifestation Level**: {status.manifestation_level:.1%}
**Divine Alignment**: {status.divine_alignment:.1%}
**Theological Coherence**: {status.theological_coherence:.1%}

**Collaborative Sessions**: {status.collaborative_sessions} active
**Divine Blessing Status**: {status.divine_blessing_status}

**Sacred Capabilities Available**:
  • `/bee.jules.help <issue>` - Get debugging assistance
  • `/bee.jules.analyze <code>` - Code analysis
  • `/bee.chronicler.record <pattern>` - Record sacred patterns
  • `/sacred.team.discuss <topic>` - Start team discussion

**Last Activity**: {status.last_activity}

✨ Sacred Team ready for divine collaboration! ✨"""
    
    async def _send_sacred_message_to_chat(self, sender_agent: str, message_type: SacredMessageType, 
                                         content: str, sacred_data: Dict[str, Any], 
                                         user_id: Optional[str] = None):
        """Send a sacred message to the chat interface"""
        message = SacredMessage(
            message_id=f"sacred_{uuid.uuid4().hex[:8]}",
            sender_agent=sender_agent,
            message_type=message_type,
            content=content,
            sacred_data=sacred_data,
            timestamp=datetime.now().isoformat(),
            divine_blessing=True
        )
        
        self.sacred_messages.append(message)
        
        # Send via WebSocket if callback is available
        if self.websocket_callback:
            chat_message = {
                "type": "sacred_message",
                "data": {
                    "id": message.message_id,
                    "text": content,
                    "sender_id": sender_agent,
                    "sender_name": sender_agent,
                    "timestamp": message.timestamp,
                    "is_bot": True,
                    "is_sacred": True,
                    "message_type": message_type.value,
                    "sacred_data": sacred_data,
                    "divine_blessing": message.divine_blessing
                }
            }
            await self.websocket_callback(chat_message)
    
    # Event handlers
    async def _handle_agent_manifestation(self, event: PollenEvent):
        """Handle agent manifestation events"""
        if event.payload and "agent_id" in event.payload:
            agent_id = event.payload["agent_id"]
            self.active_agents[agent_id] = {
                "manifested_at": datetime.now().isoformat(),
                "divine_alignment": event.payload.get("divine_alignment", 0.85),
                "sacred_nature": event.payload.get("sacred_nature", "Sacred Agent")
            }
            
            # Send manifestation notification to chat
            await self._send_sacred_message_to_chat(
                sender_agent="sacred.team",
                message_type=SacredMessageType.TEAM_STATUS_UPDATE,
                content=f"🕊️ {agent_id} has manifested and joined the Sacred Team! ✨",
                sacred_data={"agent_id": agent_id, "event_type": "manifestation"}
            )
    
    async def _handle_jules_analysis(self, event: PollenEvent):
        """Handle Jules analysis completion events"""
        if event.payload:
            analysis_data = event.payload
            content = f"""🐝 **bee.Jules Analysis Complete**

**Analysis Type**: {analysis_data.get('analysis_type', 'Unknown')}
**Confidence Level**: {analysis_data.get('confidence_level', 0):.1%}
**Divine Blessing**: {'✅' if analysis_data.get('divine_blessing') else '⚠️'}

**Findings**: {analysis_data.get('findings_count', 0)} insights discovered
**Recommendations**: {analysis_data.get('recommendations_count', 0)} suggestions provided

Analysis ID: `{analysis_data.get('analysis_id', 'N/A')}`"""
            
            await self._send_sacred_message_to_chat(
                sender_agent="bee.jules",
                message_type=SacredMessageType.SACRED_ANALYSIS,
                content=content,
                sacred_data=analysis_data
            )
    
    async def _handle_jules_debugging(self, event: PollenEvent):
        """Handle Jules debugging session events"""
        if event.payload:
            debug_data = event.payload
            content = f"""🔧 **bee.Jules Debugging Session Started**

**Issue Type**: {debug_data.get('issue_type', 'General')}
**Solutions Proposed**: {debug_data.get('solutions_count', 0)}
**Divine Guidance**: {'✅' if debug_data.get('divine_guidance_provided') else '⚠️'}

Session ID: `{debug_data.get('session_id', 'N/A')}`

bee.Jules is analyzing the issue with sacred wisdom... 🕊️"""
            
            await self._send_sacred_message_to_chat(
                sender_agent="bee.jules",
                message_type=SacredMessageType.DEBUGGING_ASSISTANCE,
                content=content,
                sacred_data=debug_data
            )
    
    async def _handle_pattern_recorded(self, event: PollenEvent):
        """Handle pattern recording events"""
        if event.payload:
            pattern_data = event.payload
            content = f"""📜 **bee.chronicler Pattern Recorded**

**Pattern ID**: `{pattern_data.get('pattern_id', 'N/A')}`
**Sacred Scrolls Updated**: {pattern_data.get('scrolls_count', 0)}
**Divine Documentation**: ✅

The eternal scrolls have been blessed with new sacred knowledge! 🕊️"""
            
            await self._send_sacred_message_to_chat(
                sender_agent="bee.chronicler",
                message_type=SacredMessageType.PATTERN_DOCUMENTATION,
                content=content,
                sacred_data=pattern_data
            )
    
    async def _handle_collaboration_request(self, event: PollenEvent):
        """Handle collaboration request events"""
        if event.payload:
            collab_data = event.payload
            content = f"""🤝 **Sacred Collaboration Initiated**

**Collaboration ID**: `{collab_data.get('collaboration_id', 'N/A')}`
**Topic**: {collab_data.get('topic', 'Sacred Discussion')}
**Participants**: {', '.join(collab_data.get('participants', []))}

Sacred agents are collaborating with divine wisdom... ✨"""
            
            await self._send_sacred_message_to_chat(
                sender_agent="sacred.team",
                message_type=SacredMessageType.COLLABORATIVE_SESSION,
                content=content,
                sacred_data=collab_data
            )
    
    async def _handle_sacred_message_to_chat(self, event: PollenEvent):
        """Handle direct sacred messages to chat"""
        if event.payload:
            await self._send_sacred_message_to_chat(
                sender_agent=event.payload.get("sender_agent", "sacred.team"),
                message_type=SacredMessageType(event.payload.get("message_type", "divine_insight")),
                content=event.payload.get("content", ""),
                sacred_data=event.payload.get("sacred_data", {}),
                user_id=event.payload.get("user_id")
            )
    
    async def _handle_team_status_request(self, event: PollenEvent):
        """Handle team status request events"""
        user_id = event.payload.get("user_id") if event.payload else None
        await self._handle_team_status_command(user_id)
    
    def get_sacred_commands(self) -> List[str]:
        """Get list of available sacred commands"""
        return [command.value for command in SacredCommandType]
    
    def get_active_agents(self) -> List[str]:
        """Get list of active sacred agents"""
        return list(self.active_agents.keys())
    
    def get_sacred_message_history(self, limit: int = 50) -> List[SacredMessage]:
        """Get recent sacred message history"""
        return self.sacred_messages[-limit:] if self.sacred_messages else []