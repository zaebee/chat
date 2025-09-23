#!/usr/bin/env python3
"""
🐝✨ Sacred Connection Manager - Phase 1.1 Emergency Fix ✨🐝

IMMEDIATE IMPLEMENTATION - Addresses bee.Sage critical vulnerability:
"Connection Manager Chaos - DoS vulnerability through connection flooding"

Sacred Protection Mechanisms:
- Connection bounds with automatic rejection
- Rate limiting shields for resource protection
- Circuit breaker patterns for cascade failure prevention
- Graceful degradation under connection stress
- Sacred timeout guards for all operations
- Comprehensive connection lifecycle management
"""

import asyncio
import time
import logging
import weakref
from typing import Dict, Set, Optional, List, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict, deque
import json
import uuid
from enum import Enum

# Import sacred computational safety components
from sacred_computational_safety_pr52 import (
    SacredCircuitBreaker,
    SacredMemorySentinel,
    SacredTimeoutManager,
    SacredComputationalError,
    SacredTimeoutError,
    SacredCircuitBreakerError
)

# Sacred Configuration Constants
SACRED_CONNECTION_LIMITS = {
    'MAX_CONNECTIONS': 1000,
    'MAX_CONNECTIONS_PER_IP': 10,
    'MAX_CONNECTIONS_PER_USER': 5,
    'CONNECTION_TIMEOUT_SECONDS': 300,  # 5 minutes
    'HEARTBEAT_INTERVAL_SECONDS': 30,
    'RATE_LIMIT_REQUESTS_PER_MINUTE': 100,
    'RATE_LIMIT_WINDOW_SECONDS': 60,
    'CIRCUIT_BREAKER_THRESHOLD': 10,
    'CIRCUIT_BREAKER_RECOVERY_SECONDS': 60,
    'BROADCAST_TIMEOUT_SECONDS': 5,
    'CLEANUP_INTERVAL_SECONDS': 60,
    'MAX_MESSAGE_SIZE_BYTES': 64 * 1024,  # 64KB
    'MAX_PENDING_MESSAGES': 100
}

# Sacred Error Types
class SacredConnectionError(Exception):
    """Base class for sacred connection errors"""
    def __init__(self, message: str, code: str, connection_id: Optional[str] = None):
        super().__init__(message)
        self.code = code
        self.connection_id = connection_id
        self.timestamp = datetime.utcnow()

class SacredCapacityError(SacredConnectionError):
    """Raised when connection capacity is exceeded"""
    def __init__(self, connection_id: Optional[str] = None):
        super().__init__(
            "Sacred capacity exceeded - connection rejected for divine protection",
            "CAPACITY_EXCEEDED",
            connection_id
        )

class SacredRateLimitError(SacredConnectionError):
    """Raised when rate limits are exceeded"""
    def __init__(self, connection_id: Optional[str] = None):
        super().__init__(
            "Sacred rate limit exceeded - please reduce request frequency",
            "RATE_LIMIT_EXCEEDED", 
            connection_id
        )

class SacredTimeoutError(SacredConnectionError):
    """Raised when operations timeout"""
    def __init__(self, operation: str, connection_id: Optional[str] = None):
        super().__init__(
            f"Sacred timeout during {operation} - operation cancelled for protection",
            "TIMEOUT_EXCEEDED",
            connection_id
        )

# Sacred Connection States
class SacredConnectionState(Enum):
    CONNECTING = "connecting"
    CONNECTED = "connected"
    AUTHENTICATED = "authenticated"
    ACTIVE = "active"
    IDLE = "idle"
    DISCONNECTING = "disconnecting"
    DISCONNECTED = "disconnected"
    REJECTED = "rejected"
    ERROR = "error"

# Sacred Connection Data Structure
@dataclass
class SacredConnection:
    """Sacred connection with divine protection and monitoring"""
    id: str
    websocket: Any  # WebSocket object
    user_id: Optional[str]
    username: Optional[str]
    ip_address: str
    state: SacredConnectionState
    connected_at: datetime
    last_activity: datetime
    last_heartbeat: datetime
    message_count: int = 0
    bytes_sent: int = 0
    bytes_received: int = 0
    rate_limit_tokens: int = field(default_factory=lambda: SACRED_CONNECTION_LIMITS['RATE_LIMIT_REQUESTS_PER_MINUTE'])
    rate_limit_reset_time: datetime = field(default_factory=datetime.utcnow)
    pending_messages: deque = field(default_factory=deque)
    error_count: int = 0
    last_error: Optional[str] = None
    
    def __post_init__(self):
        """Initialize sacred connection properties"""
        if not self.id:
            self.id = str(uuid.uuid4())
        
    def is_expired(self) -> bool:
        """Check if connection has exceeded timeout"""
        timeout = timedelta(seconds=SACRED_CONNECTION_LIMITS['CONNECTION_TIMEOUT_SECONDS'])
        return datetime.utcnow() - self.last_activity > timeout
    
    def needs_heartbeat(self) -> bool:
        """Check if connection needs heartbeat"""
        interval = timedelta(seconds=SACRED_CONNECTION_LIMITS['HEARTBEAT_INTERVAL_SECONDS'])
        return datetime.utcnow() - self.last_heartbeat > interval
    
    def update_activity(self):
        """Update last activity timestamp"""
        self.last_activity = datetime.utcnow()
    
    def update_heartbeat(self):
        """Update last heartbeat timestamp"""
        self.last_heartbeat = datetime.utcnow()
        self.update_activity()
    
    def can_send_message(self) -> bool:
        """Check if connection can send message (rate limiting)"""
        now = datetime.utcnow()
        
        # Reset rate limit tokens if window has passed
        if now >= self.rate_limit_reset_time:
            self.rate_limit_tokens = SACRED_CONNECTION_LIMITS['RATE_LIMIT_REQUESTS_PER_MINUTE']
            self.rate_limit_reset_time = now + timedelta(seconds=SACRED_CONNECTION_LIMITS['RATE_LIMIT_WINDOW_SECONDS'])
        
        return self.rate_limit_tokens > 0
    
    def consume_rate_limit_token(self):
        """Consume a rate limit token"""
        if self.rate_limit_tokens > 0:
            self.rate_limit_tokens -= 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get connection metrics"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'ip_address': self.ip_address,
            'state': self.state.value,
            'connected_duration': (datetime.utcnow() - self.connected_at).total_seconds(),
            'last_activity_seconds_ago': (datetime.utcnow() - self.last_activity).total_seconds(),
            'message_count': self.message_count,
            'bytes_sent': self.bytes_sent,
            'bytes_received': self.bytes_received,
            'rate_limit_tokens': self.rate_limit_tokens,
            'pending_messages': len(self.pending_messages),
            'error_count': self.error_count
        }

# Sacred Rate Limiter
class SacredRateLimiter:
    """Sacred rate limiting with divine protection"""
    
    def __init__(self):
        self.request_history: Dict[str, deque] = defaultdict(deque)
        self.blocked_ips: Dict[str, datetime] = {}
        self.blocked_users: Dict[str, datetime] = {}
    
    def is_allowed(self, identifier: str, limit: int = None, window: int = None) -> bool:
        """Check if request is allowed under rate limits"""
        if limit is None:
            limit = SACRED_CONNECTION_LIMITS['RATE_LIMIT_REQUESTS_PER_MINUTE']
        if window is None:
            window = SACRED_CONNECTION_LIMITS['RATE_LIMIT_WINDOW_SECONDS']
        
        now = time.time()
        
        # Check if identifier is blocked
        if identifier in self.blocked_ips:
            if now < self.blocked_ips[identifier].timestamp():
                return False
            else:
                del self.blocked_ips[identifier]
        
        # Clean old requests
        history = self.request_history[identifier]
        while history and history[0] < now - window:
            history.popleft()
        
        # Check rate limit
        if len(history) >= limit:
            # Block for additional time if severely over limit
            if len(history) > limit * 2:
                self.blocked_ips[identifier] = datetime.utcnow() + timedelta(minutes=5)
            return False
        
        # Record request
        history.append(now)
        return True
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get rate limiter metrics"""
        return {
            'active_limiters': len(self.request_history),
            'blocked_ips': len(self.blocked_ips),
            'blocked_users': len(self.blocked_users),
            'total_requests_tracked': sum(len(history) for history in self.request_history.values())
        }

# Main Sacred Connection Manager
class SacredConnectionManager:
    """Sacred WebSocket connection manager with divine protection"""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
        
        # Sacred protection components
        self.circuit_breaker = SacredCircuitBreaker(
            failure_threshold=SACRED_CONNECTION_LIMITS['CIRCUIT_BREAKER_THRESHOLD'],
            recovery_timeout=SACRED_CONNECTION_LIMITS['CIRCUIT_BREAKER_RECOVERY_SECONDS']
        )
        self.memory_sentinel = SacredMemorySentinel(max_memory_mb=500)
        self.timeout_manager = SacredTimeoutManager()
        self.rate_limiter = SacredRateLimiter()
        
        # Connection storage
        self.connections: Dict[str, SacredConnection] = {}
        self.connections_by_ip: Dict[str, Set[str]] = defaultdict(set)
        self.connections_by_user: Dict[str, Set[str]] = defaultdict(set)
        
        # Sacred metrics
        self.total_connections_created = 0
        self.total_connections_rejected = 0
        self.total_messages_sent = 0
        self.total_messages_received = 0
        self.total_bytes_transferred = 0
        
        # Sacred monitoring
        self.is_running = False
        self.cleanup_task: Optional[asyncio.Task] = None
        self.heartbeat_task: Optional[asyncio.Task] = None
        
        self.logger.info("Sacred Connection Manager initialized with divine protection")
    
    async def start(self):
        """Start sacred connection manager"""
        if self.is_running:
            return
        
        self.is_running = True
        
        # Start sacred monitoring tasks
        self.cleanup_task = asyncio.create_task(self._sacred_cleanup_loop())
        self.heartbeat_task = asyncio.create_task(self._sacred_heartbeat_loop())
        
        self.logger.info("Sacred Connection Manager started")
    
    async def stop(self):
        """Stop sacred connection manager gracefully"""
        self.is_running = False
        
        # Cancel monitoring tasks
        if self.cleanup_task:
            self.cleanup_task.cancel()
        if self.heartbeat_task:
            self.heartbeat_task.cancel()
        
        # Disconnect all connections gracefully
        await self._disconnect_all_connections()
        
        self.logger.info("Sacred Connection Manager stopped")
    
    async def connect(self, websocket: Any, user_id: Optional[str] = None, 
                     username: Optional[str] = None, ip_address: str = "unknown") -> SacredConnection:
        """Sacred connection establishment with divine protection"""
        
        return await self.circuit_breaker.call_with_protection(
            lambda: self._perform_sacred_connection(websocket, user_id, username, ip_address)
        )
    
    async def _perform_sacred_connection(self, websocket: Any, user_id: Optional[str], 
                                       username: Optional[str], ip_address: str) -> SacredConnection:
        """Perform sacred connection with all protection checks"""
        
        # Sacred capacity checking
        if len(self.connections) >= SACRED_CONNECTION_LIMITS['MAX_CONNECTIONS']:
            self.total_connections_rejected += 1
            await self._close_websocket_safely(websocket, 1013, "Sacred capacity exceeded")
            raise SacredCapacityError()
        
        # Sacred IP-based limiting
        if len(self.connections_by_ip[ip_address]) >= SACRED_CONNECTION_LIMITS['MAX_CONNECTIONS_PER_IP']:
            self.total_connections_rejected += 1
            await self._close_websocket_safely(websocket, 1008, "Sacred IP limit exceeded")
            raise SacredCapacityError()
        
        # Sacred user-based limiting
        if user_id and len(self.connections_by_user[user_id]) >= SACRED_CONNECTION_LIMITS['MAX_CONNECTIONS_PER_USER']:
            self.total_connections_rejected += 1
            await self._close_websocket_safely(websocket, 1008, "Sacred user limit exceeded")
            raise SacredCapacityError()
        
        # Sacred rate limiting
        if not self.rate_limiter.is_allowed(ip_address):
            self.total_connections_rejected += 1
            await self._close_websocket_safely(websocket, 1008, "Sacred rate limit exceeded")
            raise SacredRateLimitError()
        
        # Create sacred connection
        now = datetime.utcnow()
        connection = SacredConnection(
            id=str(uuid.uuid4()),
            websocket=websocket,
            user_id=user_id,
            username=username,
            ip_address=ip_address,
            state=SacredConnectionState.CONNECTING,
            connected_at=now,
            last_activity=now,
            last_heartbeat=now
        )
        
        try:
            # Accept WebSocket connection
            await asyncio.wait_for(
                websocket.accept(),
                timeout=SACRED_CONNECTION_LIMITS['BROADCAST_TIMEOUT_SECONDS']
            )
            
            # Register connection
            self.connections[connection.id] = connection
            self.connections_by_ip[ip_address].add(connection.id)
            if user_id:
                self.connections_by_user[user_id].add(connection.id)
            
            connection.state = SacredConnectionState.CONNECTED
            self.total_connections_created += 1
            
            self.logger.info(f"Sacred connection established: {connection.id} ({username}@{ip_address})")
            
            # Send welcome message
            await self._send_to_connection(connection, {
                'type': 'sacred_welcome',
                'connection_id': connection.id,
                'server_time': datetime.utcnow().isoformat(),
                'limits': {
                    'max_message_size': SACRED_CONNECTION_LIMITS['MAX_MESSAGE_SIZE_BYTES'],
                    'rate_limit': SACRED_CONNECTION_LIMITS['RATE_LIMIT_REQUESTS_PER_MINUTE']
                }
            })
            
            return connection
            
        except Exception as e:
            # Clean up on failure
            await self._cleanup_connection(connection)
            self.logger.error(f"Sacred connection failed: {e}")
            raise SacredConnectionError(f"Connection establishment failed: {e}", "CONNECTION_FAILED", connection.id)
    
    async def disconnect(self, connection_id: str, reason: str = "Sacred disconnection"):
        """Sacred connection disconnection"""
        connection = self.connections.get(connection_id)
        if not connection:
            return
        
        connection.state = SacredConnectionState.DISCONNECTING
        
        try:
            await self._close_websocket_safely(connection.websocket, 1000, reason)
        except Exception as e:
            self.logger.warning(f"Error during sacred disconnection: {e}")
        finally:
            await self._cleanup_connection(connection)
    
    async def send_message(self, connection_id: str, message: Dict[str, Any]) -> bool:
        """Sacred message sending with protection"""
        connection = self.connections.get(connection_id)
        if not connection:
            return False
        
        return await self.circuit_breaker.call_with_protection(
            lambda: self._perform_sacred_send(connection, message)
        )
    
    async def _perform_sacred_send(self, connection: SacredConnection, message: Dict[str, Any]) -> bool:
        """Perform sacred message send with all protections"""
        
        # Sacred rate limiting check
        if not connection.can_send_message():
            raise SacredRateLimitError(connection.id)
        
        # Sacred message size check
        message_json = json.dumps(message)
        message_size = len(message_json.encode('utf-8'))
        
        if message_size > SACRED_CONNECTION_LIMITS['MAX_MESSAGE_SIZE_BYTES']:
            raise SacredConnectionError(
                f"Message too large: {message_size} bytes",
                "MESSAGE_TOO_LARGE",
                connection.id
            )
        
        # Sacred pending message check
        if len(connection.pending_messages) >= SACRED_CONNECTION_LIMITS['MAX_PENDING_MESSAGES']:
            raise SacredConnectionError(
                "Too many pending messages",
                "QUEUE_FULL",
                connection.id
            )
        
        return await self._send_to_connection(connection, message)
    
    async def _send_to_connection(self, connection: SacredConnection, message: Dict[str, Any]) -> bool:
        """Send message to specific connection with timeout protection"""
        try:
            message_json = json.dumps(message)
            
            await asyncio.wait_for(
                connection.websocket.send_text(message_json),
                timeout=SACRED_CONNECTION_LIMITS['BROADCAST_TIMEOUT_SECONDS']
            )
            
            # Update connection metrics
            connection.message_count += 1
            connection.bytes_sent += len(message_json.encode('utf-8'))
            connection.consume_rate_limit_token()
            connection.update_activity()
            
            self.total_messages_sent += 1
            self.total_bytes_transferred += len(message_json.encode('utf-8'))
            
            return True
            
        except asyncio.TimeoutError:
            self.logger.warning(f"Sacred send timeout for connection {connection.id}")
            await self._handle_connection_error(connection, "Send timeout")
            return False
        except Exception as e:
            self.logger.error(f"Sacred send error for connection {connection.id}: {e}")
            await self._handle_connection_error(connection, str(e))
            return False
    
    async def broadcast_message(self, message: Dict[str, Any], exclude_connection_id: Optional[str] = None) -> int:
        """Sacred broadcast with divine protection"""
        
        return await self.circuit_breaker.call_with_protection(
            lambda: self._perform_sacred_broadcast(message, exclude_connection_id)
        )
    
    async def _perform_sacred_broadcast(self, message: Dict[str, Any], exclude_connection_id: Optional[str]) -> int:
        """Perform sacred broadcast with parallel sending and error handling"""
        
        active_connections = [
            conn for conn in self.connections.values()
            if conn.state in [SacredConnectionState.CONNECTED, SacredConnectionState.ACTIVE]
            and conn.id != exclude_connection_id
        ]
        
        if not active_connections:
            return 0
        
        # Sacred parallel broadcasting with timeout protection
        tasks = []
        for connection in active_connections:
            task = asyncio.create_task(
                self._send_to_connection(connection, message)
            )
            tasks.append((connection.id, task))
        
        # Sacred graceful handling of broadcast results
        successful_sends = 0
        try:
            results = await asyncio.gather(
                *[task for _, task in tasks],
                return_exceptions=True
            )
            
            for (connection_id, _), result in zip(tasks, results):
                if isinstance(result, Exception):
                    self.logger.warning(f"Sacred broadcast failed for {connection_id}: {result}")
                elif result:
                    successful_sends += 1
                    
        except Exception as e:
            self.logger.error(f"Sacred broadcast error: {e}")
        
        return successful_sends
    
    async def _handle_connection_error(self, connection: SacredConnection, error: str):
        """Handle connection errors with sacred grace"""
        connection.error_count += 1
        connection.last_error = error
        connection.state = SacredConnectionState.ERROR
        
        # Disconnect if too many errors
        if connection.error_count >= 5:
            await self.disconnect(connection.id, "Too many errors")
    
    async def _cleanup_connection(self, connection: SacredConnection):
        """Sacred connection cleanup"""
        # Remove from all tracking structures
        self.connections.pop(connection.id, None)
        
        if connection.ip_address in self.connections_by_ip:
            self.connections_by_ip[connection.ip_address].discard(connection.id)
            if not self.connections_by_ip[connection.ip_address]:
                del self.connections_by_ip[connection.ip_address]
        
        if connection.user_id and connection.user_id in self.connections_by_user:
            self.connections_by_user[connection.user_id].discard(connection.id)
            if not self.connections_by_user[connection.user_id]:
                del self.connections_by_user[connection.user_id]
        
        connection.state = SacredConnectionState.DISCONNECTED
        
        self.logger.info(f"Sacred connection cleaned up: {connection.id}")
    
    async def _close_websocket_safely(self, websocket: Any, code: int = 1000, reason: str = "Sacred closure"):
        """Safely close WebSocket with timeout protection"""
        try:
            await asyncio.wait_for(
                websocket.close(code=code, reason=reason),
                timeout=5.0
            )
        except Exception as e:
            self.logger.warning(f"Error closing WebSocket: {e}")
    
    async def _disconnect_all_connections(self):
        """Gracefully disconnect all connections"""
        if not self.connections:
            return
        
        self.logger.info(f"Disconnecting {len(self.connections)} sacred connections")
        
        # Create disconnect tasks
        tasks = []
        for connection in list(self.connections.values()):
            task = asyncio.create_task(
                self.disconnect(connection.id, "Server shutdown")
            )
            tasks.append(task)
        
        # Wait for all disconnections with timeout
        try:
            await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True),
                timeout=30.0
            )
        except asyncio.TimeoutError:
            self.logger.warning("Sacred disconnection timeout - forcing cleanup")
            self.connections.clear()
            self.connections_by_ip.clear()
            self.connections_by_user.clear()
    
    async def _sacred_cleanup_loop(self):
        """Sacred cleanup loop for expired connections"""
        while self.is_running:
            try:
                await asyncio.sleep(SACRED_CONNECTION_LIMITS['CLEANUP_INTERVAL_SECONDS'])
                await self._perform_sacred_cleanup()
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Sacred cleanup error: {e}")
    
    async def _perform_sacred_cleanup(self):
        """Perform sacred cleanup of expired connections"""
        expired_connections = [
            conn for conn in self.connections.values()
            if conn.is_expired()
        ]
        
        if expired_connections:
            self.logger.info(f"Cleaning up {len(expired_connections)} expired sacred connections")
            
            for connection in expired_connections:
                await self.disconnect(connection.id, "Connection expired")
    
    async def _sacred_heartbeat_loop(self):
        """Sacred heartbeat loop for connection health"""
        while self.is_running:
            try:
                await asyncio.sleep(SACRED_CONNECTION_LIMITS['HEARTBEAT_INTERVAL_SECONDS'])
                await self._perform_sacred_heartbeat()
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Sacred heartbeat error: {e}")
    
    async def _perform_sacred_heartbeat(self):
        """Perform sacred heartbeat for all connections"""
        heartbeat_message = {
            'type': 'sacred_heartbeat',
            'timestamp': datetime.utcnow().isoformat(),
            'server_status': 'operational'
        }
        
        connections_needing_heartbeat = [
            conn for conn in self.connections.values()
            if conn.needs_heartbeat() and conn.state in [
                SacredConnectionState.CONNECTED,
                SacredConnectionState.ACTIVE
            ]
        ]
        
        if connections_needing_heartbeat:
            for connection in connections_needing_heartbeat:
                try:
                    await self._send_to_connection(connection, heartbeat_message)
                    connection.update_heartbeat()
                except Exception as e:
                    self.logger.warning(f"Sacred heartbeat failed for {connection.id}: {e}")
    
    def get_connection_metrics(self) -> Dict[str, Any]:
        """Get comprehensive connection metrics"""
        active_connections = sum(
            1 for conn in self.connections.values()
            if conn.state in [SacredConnectionState.CONNECTED, SacredConnectionState.ACTIVE]
        )
        
        return {
            'total_connections': len(self.connections),
            'active_connections': active_connections,
            'connections_by_state': {
                state.value: sum(1 for conn in self.connections.values() if conn.state == state)
                for state in SacredConnectionState
            },
            'total_connections_created': self.total_connections_created,
            'total_connections_rejected': self.total_connections_rejected,
            'total_messages_sent': self.total_messages_sent,
            'total_messages_received': self.total_messages_received,
            'total_bytes_transferred': self.total_bytes_transferred,
            'circuit_breaker': self.circuit_breaker.get_status(),
            'rate_limiter': self.rate_limiter.get_metrics(),
            'memory_usage': {
                'current_memory_mb': self.memory_sentinel.get_memory_usage_mb(),
                'max_memory_mb': self.memory_sentinel.max_memory_mb,
                'usage_ratio': self.memory_sentinel._memory_usage_ratio()
            },
            'connections_by_ip_count': len(self.connections_by_ip),
            'connections_by_user_count': len(self.connections_by_user)
        }
    
    def get_connection_details(self) -> List[Dict[str, Any]]:
        """Get detailed information about all connections"""
        return [conn.get_metrics() for conn in self.connections.values()]
    
    def is_healthy(self) -> bool:
        """Check if connection manager is healthy"""
        return (
            self.is_running and
            self.circuit_breaker.state != 'OPEN' and
            len(self.connections) < SACRED_CONNECTION_LIMITS['MAX_CONNECTIONS'] * 0.9
        )
    
    def get_status_message(self) -> str:
        """Get human-readable status message"""
        if not self.is_running:
            return "Sacred Connection Manager: Stopped"
        
        if self.circuit_breaker.state == 'OPEN':
            return "Sacred Protection: Circuit breaker active"
        
        connection_percentage = (len(self.connections) / SACRED_CONNECTION_LIMITS['MAX_CONNECTIONS']) * 100
        
        if connection_percentage > 90:
            return f"Sacred Protection: High capacity ({connection_percentage:.1f}%)"
        elif connection_percentage > 70:
            return f"Sacred Protection: Moderate load ({connection_percentage:.1f}%)"
        else:
            return f"Sacred Protection: All systems operational ({connection_percentage:.1f}%)"


# Sacred Connection Manager Factory
def create_sacred_connection_manager(logger: Optional[logging.Logger] = None) -> SacredConnectionManager:
    """Create and configure sacred connection manager"""
    return SacredConnectionManager(logger)


# Export sacred components
__all__ = [
    'SacredConnectionManager',
    'SacredConnection',
    'SacredConnectionState',
    'SacredConnectionError',
    'SacredCapacityError',
    'SacredRateLimitError',
    'SacredTimeoutError',
    'SacredRateLimiter',
    'SACRED_CONNECTION_LIMITS',
    'create_sacred_connection_manager'
]