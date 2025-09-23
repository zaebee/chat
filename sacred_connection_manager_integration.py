#!/usr/bin/env python3
"""
🐝✨ Sacred Connection Manager Integration - Phase 1.1 Emergency Fix ✨🐝

Integration layer for Sacred Connection Manager with existing Hive Chat system
Replaces vulnerable connection_manager.py with divine protection
"""

import json
import asyncio
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime
from fastapi import WebSocket, WebSocketDisconnect

# Import sacred protection
from SacredConnectionManager import (
    SacredConnectionManager,
    SacredConnection,
    SacredConnectionError,
    SacredCapacityError,
    SacredRateLimitError,
    create_sacred_connection_manager
)

# Import existing models
from models import User

# Import Hive components if available
try:
    from hive.events import HiveEventBus
    from hive.team_communication import SacredTeamCommunication
    HIVE_AVAILABLE = True
except ImportError:
    HIVE_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SacredHiveConnectionManager:
    """
    🐝✨ Sacred Hive Connection Manager ✨🐝
    
    Integrates Sacred Connection Manager with existing Hive Chat system
    Provides divine protection while maintaining compatibility
    """
    
    def __init__(self):
        # Initialize sacred connection manager
        self.sacred_manager = create_sacred_connection_manager(logger)
        
        # Legacy compatibility
        self.users: Dict[str, User] = {}
        self.user_colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FECA57", "#FF9FF3", "#54A0FF"]
        
        # Hive integration
        if HIVE_AVAILABLE:
            self.event_bus = HiveEventBus()
            self.sacred_communication = SacredTeamCommunication(self.event_bus)
            self.sacred_communication.set_websocket_callback(self.broadcast)
        else:
            self.event_bus = None
            self.sacred_communication = None
        
        # Sacred metrics
        self.total_messages_processed = 0
        self.total_users_connected = 0
        
        logger.info("Sacred Hive Connection Manager initialized")
    
    async def start(self):
        """Start sacred connection manager"""
        await self.sacred_manager.start()
        logger.info("Sacred Hive Connection Manager started")
    
    async def stop(self):
        """Stop sacred connection manager gracefully"""
        await self.sacred_manager.stop()
        logger.info("Sacred Hive Connection Manager stopped")
    
    async def connect(self, websocket: WebSocket, user_id: str, username: str, 
                     ip_address: str = "unknown") -> bool:
        """
        Sacred connection establishment with divine protection
        Returns True if connection successful, False if rejected
        """
        try:
            # Attempt sacred connection
            sacred_connection = await self.sacred_manager.connect(
                websocket, user_id, username, ip_address
            )
            
            # Create user if not exists
            if user_id not in self.users:
                color = self.user_colors[len(self.users) % len(self.user_colors)]
                self.users[user_id] = User(id=user_id, username=username, color=color)
                self.total_users_connected += 1
            
            # Broadcast user list update
            await self.broadcast_user_update()
            
            # Hive event integration
            if self.event_bus:
                await self.event_bus.publish_user_event("connected", user_id, {
                    "username": username,
                    "timestamp": datetime.now().isoformat(),
                    "connection_id": sacred_connection.id
                })
            
            logger.info(f"Sacred connection established for user {username} ({user_id})")
            return True
            
        except SacredCapacityError:
            logger.warning(f"Sacred capacity exceeded - rejecting connection for {username}")
            await self._send_rejection_message(websocket, "Server at capacity - please try again later")
            return False
            
        except SacredRateLimitError:
            logger.warning(f"Sacred rate limit exceeded - rejecting connection for {username}")
            await self._send_rejection_message(websocket, "Too many connection attempts - please wait")
            return False
            
        except Exception as e:
            logger.error(f"Sacred connection error for {username}: {e}")
            await self._send_rejection_message(websocket, "Connection failed - please try again")
            return False
    
    async def disconnect(self, websocket: WebSocket, user_id: str):
        """Sacred disconnection with cleanup"""
        try:
            # Find connection by user_id
            connection_id = None
            for conn_id, connection in self.sacred_manager.connections.items():
                if connection.user_id == user_id:
                    connection_id = conn_id
                    break
            
            if connection_id:
                await self.sacred_manager.disconnect(connection_id, "User disconnection")
            
            # Clean up user data
            if user_id in self.users:
                username = self.users[user_id].username
                del self.users[user_id]
                
                # Broadcast user list update
                await self.broadcast_user_update()
                
                # Hive event integration
                if self.event_bus:
                    await self.event_bus.publish_user_event("disconnected", user_id, {
                        "username": username,
                        "timestamp": datetime.now().isoformat()
                    })
                
                logger.info(f"Sacred disconnection completed for user {username} ({user_id})")
            
        except Exception as e:
            logger.error(f"Sacred disconnection error for user {user_id}: {e}")
    
    async def send_personal_message(self, message: str, user_id: str) -> bool:
        """Send message to specific user with sacred protection"""
        try:
            # Find connection by user_id
            connection_id = None
            for conn_id, connection in self.sacred_manager.connections.items():
                if connection.user_id == user_id:
                    connection_id = conn_id
                    break
            
            if not connection_id:
                logger.warning(f"No sacred connection found for user {user_id}")
                return False
            
            message_data = {
                "type": "personal_message",
                "content": message,
                "timestamp": datetime.now().isoformat()
            }
            
            success = await self.sacred_manager.send_message(connection_id, message_data)
            if success:
                self.total_messages_processed += 1
            
            return success
            
        except Exception as e:
            logger.error(f"Sacred personal message error for user {user_id}: {e}")
            return False
    
    async def broadcast(self, message: str, exclude_user_id: Optional[str] = None) -> int:
        """Sacred broadcast with divine protection"""
        try:
            # Find connection to exclude
            exclude_connection_id = None
            if exclude_user_id:
                for conn_id, connection in self.sacred_manager.connections.items():
                    if connection.user_id == exclude_user_id:
                        exclude_connection_id = conn_id
                        break
            
            message_data = {
                "type": "broadcast_message",
                "content": message,
                "timestamp": datetime.now().isoformat()
            }
            
            successful_sends = await self.sacred_manager.broadcast_message(
                message_data, exclude_connection_id
            )
            
            self.total_messages_processed += successful_sends
            
            logger.info(f"Sacred broadcast sent to {successful_sends} connections")
            return successful_sends
            
        except Exception as e:
            logger.error(f"Sacred broadcast error: {e}")
            return 0
    
    async def broadcast_user_update(self):
        """Broadcast user list update with sacred protection"""
        try:
            user_list = [
                {
                    "id": user.id,
                    "username": user.username,
                    "color": user.color
                }
                for user in self.users.values()
            ]
            
            message_data = {
                "type": "user_list_update",
                "users": user_list,
                "timestamp": datetime.now().isoformat()
            }
            
            await self.sacred_manager.broadcast_message(message_data)
            
        except Exception as e:
            logger.error(f"Sacred user update broadcast error: {e}")
    
    async def broadcast_typing_indicator(self, user_id: str, is_typing: bool):
        """Broadcast typing indicator with sacred protection"""
        try:
            if user_id not in self.users:
                return
            
            message_data = {
                "type": "typing_indicator",
                "user_id": user_id,
                "username": self.users[user_id].username,
                "is_typing": is_typing,
                "timestamp": datetime.now().isoformat()
            }
            
            # Exclude the typing user from receiving their own indicator
            exclude_connection_id = None
            for conn_id, connection in self.sacred_manager.connections.items():
                if connection.user_id == user_id:
                    exclude_connection_id = conn_id
                    break
            
            await self.sacred_manager.broadcast_message(message_data, exclude_connection_id)
            
        except Exception as e:
            logger.error(f"Sacred typing indicator error: {e}")
    
    async def handle_websocket_message(self, websocket: WebSocket, user_id: str, message_data: dict):
        """Handle incoming WebSocket message with sacred protection"""
        try:
            message_type = message_data.get("type", "unknown")
            
            # Find connection
            connection_id = None
            for conn_id, connection in self.sacred_manager.connections.items():
                if connection.user_id == user_id and connection.websocket == websocket:
                    connection_id = conn_id
                    break
            
            if not connection_id:
                logger.warning(f"No sacred connection found for message from user {user_id}")
                return
            
            # Update connection activity
            connection = self.sacred_manager.connections[connection_id]
            connection.update_activity()
            connection.bytes_received += len(json.dumps(message_data).encode('utf-8'))
            
            # Handle different message types
            if message_type == "chat_message":
                await self._handle_chat_message(user_id, message_data)
            elif message_type == "typing":
                await self._handle_typing_message(user_id, message_data)
            elif message_type == "heartbeat":
                await self._handle_heartbeat_message(connection)
            else:
                logger.warning(f"Unknown message type: {message_type}")
            
        except Exception as e:
            logger.error(f"Sacred message handling error: {e}")
    
    async def _handle_chat_message(self, user_id: str, message_data: dict):
        """Handle chat message"""
        if user_id not in self.users:
            return
        
        user = self.users[user_id]
        content = message_data.get("content", "")
        
        # Broadcast chat message
        chat_message = {
            "type": "chat_message",
            "user_id": user_id,
            "username": user.username,
            "color": user.color,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        await self.sacred_manager.broadcast_message(chat_message)
        
        # Hive integration
        if self.sacred_communication:
            await self.sacred_communication.process_message(content, user_id)
    
    async def _handle_typing_message(self, user_id: str, message_data: dict):
        """Handle typing indicator message"""
        is_typing = message_data.get("isTyping", False)
        await self.broadcast_typing_indicator(user_id, is_typing)
    
    async def _handle_heartbeat_message(self, connection: SacredConnection):
        """Handle heartbeat message"""
        connection.update_heartbeat()
        
        # Send heartbeat response
        response = {
            "type": "heartbeat_response",
            "timestamp": datetime.now().isoformat(),
            "connection_id": connection.id
        }
        
        await self.sacred_manager.send_message(connection.id, response)
    
    async def _send_rejection_message(self, websocket: WebSocket, reason: str):
        """Send rejection message before closing connection"""
        try:
            rejection_message = {
                "type": "connection_rejected",
                "reason": reason,
                "timestamp": datetime.now().isoformat()
            }
            
            await websocket.send_text(json.dumps(rejection_message))
            await asyncio.sleep(0.1)  # Brief delay before closing
            await websocket.close(code=1008, reason=reason)
            
        except Exception as e:
            logger.warning(f"Error sending rejection message: {e}")
    
    # Legacy compatibility properties
    @property
    def active_connections(self) -> List[WebSocket]:
        """Legacy compatibility - return active WebSocket connections"""
        return [
            conn.websocket for conn in self.sacred_manager.connections.values()
            if conn.websocket is not None
        ]
    
    def get_sacred_metrics(self) -> Dict[str, Any]:
        """Get comprehensive sacred metrics"""
        base_metrics = self.sacred_manager.get_connection_metrics()
        
        return {
            **base_metrics,
            "hive_integration": {
                "total_users": len(self.users),
                "total_messages_processed": self.total_messages_processed,
                "total_users_connected": self.total_users_connected,
                "hive_available": HIVE_AVAILABLE,
                "event_bus_active": self.event_bus is not None,
                "sacred_communication_active": self.sacred_communication is not None
            }
        }
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get sacred health status"""
        is_healthy = self.sacred_manager.is_healthy()
        status_message = self.sacred_manager.get_status_message()
        
        return {
            "healthy": is_healthy,
            "status": status_message,
            "connections": len(self.sacred_manager.connections),
            "users": len(self.users),
            "uptime_seconds": (datetime.now() - datetime.now()).total_seconds() if hasattr(self, 'start_time') else 0
        }


# Create sacred manager instance
manager = SacredHiveConnectionManager()

# Export for compatibility
__all__ = ['manager', 'SacredHiveConnectionManager']