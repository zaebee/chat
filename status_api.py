"""
Status API for HiveHost

Provides REST endpoints for system introspection and health monitoring.
Implements the Principle of Observability.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
import asyncio
import json
from datetime import datetime

from hive_host import HiveHost


class StatusAPI:
    """REST API for HiveHost status and health monitoring."""
    
    def __init__(self, host: HiveHost):
        self.host = host
        self.app = FastAPI(title="Hive Status API", version="1.0.0")
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup API routes."""
        
        @self.app.get("/api/v1/status")
        async def get_status():
            """Get comprehensive system status."""
            try:
                status = self.host.get_status()
                return JSONResponse(content={
                    "status": "success",
                    "data": {
                        "host_id": status.host_id,
                        "uptime_seconds": status.uptime_seconds,
                        "agent_count": status.agent_count,
                        "active_agents": status.active_agents,
                        "event_bus_status": status.event_bus_status,
                        "metrics": status.metrics,
                        "last_updated": status.last_updated
                    }
                })
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/v1/health")
        async def health_check():
            """Perform comprehensive health check."""
            try:
                health = await self.host.health_check()
                status_code = 200 if health["status"] == "healthy" else 503
                return JSONResponse(content=health, status_code=status_code)
            except Exception as e:
                return JSONResponse(
                    content={
                        "status": "unhealthy",
                        "error": str(e),
                        "timestamp": datetime.utcnow().isoformat()
                    },
                    status_code=503
                )
        
        @self.app.get("/api/v1/agents")
        async def list_agents():
            """List all registered agents."""
            try:
                agents = self.host.list_agents()
                return JSONResponse(content={
                    "status": "success",
                    "data": {
                        "agents": agents,
                        "count": len(agents)
                    }
                })
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/v1/agents/{agent_id}")
        async def get_agent_status(agent_id: str):
            """Get status for a specific agent."""
            try:
                status = await self.host.get_agent_status(agent_id)
                if status is None:
                    raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
                
                return JSONResponse(content={
                    "status": "success",
                    "data": {
                        "agent_id": agent_id,
                        "status": status
                    }
                })
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/v1/metrics")
        async def get_metrics():
            """Get system metrics (τ, φ, σ)."""
            try:
                metrics = self.host.metrics.get_metrics()
                return JSONResponse(content={
                    "status": "success",
                    "data": metrics
                })
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/")
        async def root():
            """Root endpoint with basic system info."""
            status = self.host.get_status()
            return JSONResponse(content={
                "message": "Hive Host Status API",
                "version": "1.0.0",
                "host_id": status.host_id,
                "uptime_seconds": status.uptime_seconds,
                "endpoints": [
                    "/api/v1/status",
                    "/api/v1/health", 
                    "/api/v1/agents",
                    "/api/v1/metrics"
                ]
            })


def get_status():
    """
    Simple function to get system status without running the full API.
    Can be called from command line or other scripts.
    """
    async def _get_status():
        host = HiveHost("status-check")
        try:
            status = host.get_status()
            return {
                "host_id": status.host_id,
                "uptime_seconds": status.uptime_seconds,
                "agent_count": status.agent_count,
                "active_agents": status.active_agents,
                "timestamp": status.last_updated
            }
        except Exception as e:
            return {"error": str(e), "timestamp": datetime.utcnow().isoformat()}
    
    return asyncio.run(_get_status())


if __name__ == "__main__":
    # Simple status check
    status = get_status()
    print(json.dumps(status, indent=2))