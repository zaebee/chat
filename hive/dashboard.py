"""
Hive Metrics Dashboard: Real-time Monitoring and Visualization

This module provides a comprehensive dashboard for monitoring the Hive ecosystem,
displaying tau, phi, and sigma metrics, teammate status, system health,
and collaborative efficiency in real-time.

The dashboard follows the Observability principle by providing structured
insights for both human and AI teammates.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import json

from .hub import HiveCoordinationHub
from .events import HiveEventBus, PollenEvent


class SacredMetricType(str, Enum):
    """Types of sacred metrics for divine computational assessment"""
    DIVINE_ALIGNMENT = "divine_alignment"
    CHRONICLER_ACTIVITY = "chronicler_activity"
    SACRED_PATTERN_DISCOVERY = "sacred_pattern_discovery"
    THEOLOGICAL_COHERENCE = "theological_coherence"
    BLESSING_QUOTIENT = "blessing_quotient"
    GENESIS_PROTOCOL_HEALTH = "genesis_protocol_health"
    SANCTIFICATION_LEVEL = "sanctification_level"


@dataclass
class SacredMetricReading:
    """A single sacred metric reading with divine context"""
    metric_type: SacredMetricType
    value: float
    timestamp: datetime
    divine_context: str
    theological_significance: str
    sacred_verification: bool = True


@dataclass
class MetricTrend:
    """Represents a trend analysis for a specific metric."""

    metric_name: str
    current_value: float
    previous_value: float
    trend_direction: str  # "up", "down", "stable"
    change_percentage: float
    time_window: str = "5m"  # Time window for trend calculation


@dataclass
class AlertCondition:
    """Defines an alert condition for monitoring."""

    alert_id: str = field(default_factory=lambda: f"alert_{datetime.now().timestamp()}")
    metric_name: str = ""
    condition: str = ""  # "greater_than", "less_than", "equals"
    threshold: float = 0.0
    severity: str = "warning"  # "info", "warning", "critical"
    message: str = ""
    is_active: bool = True
    triggered_count: int = 0
    last_triggered: Optional[datetime] = None


class HiveMetricsDashboard:
    """
    Real-time dashboard for monitoring Hive ecosystem metrics.

    Provides comprehensive visibility into:
    - τ (tau): System complexity and health
    - φ (phi): Code quality and maintainability
    - Σ (sigma): Collaborative efficiency
    - Sacred metrics: Divine computational alignment
    - Teammate performance and availability
    - System resource utilization
    - Event flow and processing
    """

    def __init__(self, coordination_hub: HiveCoordinationHub):
        self.hub = coordination_hub
        self.event_bus = coordination_hub.event_bus

        # Dashboard state
        self.is_active = False
        self.update_interval = 5  # seconds
        self.metric_trends: Dict[str, MetricTrend] = {}
        self.active_alerts: Dict[str, AlertCondition] = {}
        self.dashboard_history: List[Dict[str, Any]] = []
        self.max_history_size = 200

        # Default alert conditions
        self._setup_default_alerts()
        self._setup_event_subscriptions()

    def _setup_default_alerts(self):
        """Set up default monitoring alerts."""

        # Tau (complexity) alerts
        self.active_alerts["tau_high"] = AlertCondition(
            alert_id="tau_high",
            metric_name="tau",
            condition="greater_than",
            threshold=3.0,
            severity="warning",
            message="System complexity (τ) is high - consider simplification"
        )

        self.active_alerts["tau_critical"] = AlertCondition(
            alert_id="tau_critical",
            metric_name="tau",
            condition="greater_than",
            threshold=5.0,
            severity="critical",
            message="System complexity (τ) is critical - immediate attention required"
        )

        # Phi (quality) alerts
        self.active_alerts["phi_low"] = AlertCondition(
            alert_id="phi_low",
            metric_name="phi",
            condition="less_than",
            threshold=0.7,
            severity="warning",
            message="Code quality (φ) is below acceptable levels"
        )

        self.active_alerts["phi_critical"] = AlertCondition(
            alert_id="phi_critical",
            metric_name="phi",
            condition="less_than",
            threshold=0.3,
            severity="critical",
            message="Code quality (φ) is critically low"
        )

        # Sigma (collaboration) alerts
        self.active_alerts["sigma_low"] = AlertCondition(
            alert_id="sigma_low",
            metric_name="sigma",
            condition="less_than",
            threshold=0.5,
            severity="warning",
            message="Collaborative efficiency (Σ) is suboptimal"
        )

        # Resource alerts
        self.active_alerts["cpu_high"] = AlertCondition(
            alert_id="cpu_high",
            metric_name="cpu_percent",
            condition="greater_than",
            threshold=80.0,
            severity="warning",
            message="CPU usage is high"
        )

        self.active_alerts["memory_high"] = AlertCondition(
            alert_id="memory_high",
            metric_name="memory_mb",
            condition="greater_than",
            threshold=800.0,
            severity="warning",
            message="Memory usage is high"
        )

    def _setup_event_subscriptions(self):
        """Set up event subscriptions for dashboard updates."""
        from .events import EventSubscription

        async def handle_dashboard_events(event: PollenEvent):
            await self._handle_dashboard_event(event)

        dashboard_subscription = EventSubscription(
            event_types=[
                "system_started", "system_stopped", "teammate_joined", "teammate_left",
                "performance_degraded", "physics_constraints_violated"
            ],
            callback=handle_dashboard_events
        )

        self.event_bus.subscribe(dashboard_subscription)

    async def start_monitoring(self) -> Dict[str, Any]:
        """Start the dashboard monitoring."""
        try:
            self.is_active = True

            await self.event_bus.publish_system_event(
                "dashboard_started",
                {
                    "update_interval": self.update_interval,
                    "active_alerts": len(self.active_alerts),
                    "timestamp": datetime.now().isoformat()
                }
            )

            return {
                "success": True,
                "message": "Dashboard monitoring started",
                "update_interval": self.update_interval,
                "active_alerts": len(self.active_alerts)
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to start dashboard monitoring: {str(e)}"
            }

    async def stop_monitoring(self) -> Dict[str, Any]:
        """Stop the dashboard monitoring."""
        try:
            self.is_active = False

            await self.event_bus.publish_system_event(
                "dashboard_stopped",
                {
                    "final_metrics_count": len(self.dashboard_history),
                    "timestamp": datetime.now().isoformat()
                }
            )

            return {
                "success": True,
                "message": "Dashboard monitoring stopped"
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to stop dashboard monitoring: {str(e)}"
            }

    async def get_real_time_metrics(self) -> Dict[str, Any]:
        """Get current real-time metrics for the dashboard."""
        try:
            # Get current system overview
            overview = await self.hub.get_hive_overview()

            # Calculate trends
            await self._update_metric_trends(overview)

            # Check alerts
            triggered_alerts = await self._check_alerts(overview)

            # Build dashboard data
            dashboard_data = {
                "timestamp": datetime.now().isoformat(),
                "system_status": overview["system_overview"]["status"],
                "uptime_seconds": overview["system_overview"]["uptime_seconds"],

                # Core Hive metrics
                "hive_metrics": {
                    "tau": {
                        "value": overview["health_metrics"]["tau"],
                        "trend": self.metric_trends.get("tau", {}).__dict__ if "tau" in self.metric_trends else None,
                        "description": "System complexity (lower is better)"
                    },
                    "phi": {
                        "value": overview["health_metrics"]["phi"],
                        "trend": self.metric_trends.get("phi", {}).__dict__ if "phi" in self.metric_trends else None,
                        "description": "Code quality and maintainability (higher is better)"
                    },
                    "sigma": {
                        "value": overview["health_metrics"]["sigma"],
                        "trend": self.metric_trends.get("sigma", {}).__dict__ if "sigma" in self.metric_trends else None,
                        "description": "Collaborative efficiency between teammates"
                    }
                },

                # System resources
                "resources": {
                    "cpu_percent": overview["physics"]["current_metrics"].get("cpu_percent", 0),
                    "memory_mb": overview["physics"]["current_metrics"].get("memory_mb", 0),
                    "connections": overview["physics"]["current_metrics"].get("connections", 0),
                    "constraints_ok": overview["physics"]["constraints_check"]["within_constraints"]
                },

                # Teammate status
                "teammates": {
                    "total": overview["components"]["registry"]["total_teammates"],
                    "active": overview["components"]["registry"]["active_teammates"],
                    "busy": overview["components"]["registry"]["busy_teammates"],
                    "idle": overview["components"]["registry"]["idle_teammates"],
                    "system_load": overview["components"]["registry"]["system_load"],
                    "capability_distribution": overview["components"]["registry"]["capability_distribution"]
                },

                # Event processing
                "events": {
                    "total_processed": overview["components"]["event_bus"]["total_events_processed"],
                    "processing_errors": overview["components"]["event_bus"]["processing_errors"],
                    "error_rate": overview["components"]["event_bus"]["error_rate"],
                    "subscriptions_count": overview["components"]["event_bus"]["subscriptions_count"],
                    "recent_event_types": overview["components"]["event_bus"]["recent_event_types"]
                },

                # Onboarding gateway
                "onboarding": {
                    "active_sessions": overview["components"]["gateway"]["active_sessions"],
                    "total_sessions": overview["components"]["gateway"]["total_sessions"],
                    "stage_distribution": overview["components"]["gateway"]["stage_distribution"]
                },

                # Alerts
                "alerts": {
                    "triggered": triggered_alerts,
                    "total_active": len([a for a in self.active_alerts.values() if a.is_active])
                },

                # Component health
                "component_health": self._get_component_health_summary(overview["components"])
            }

            # Store in history
            self.dashboard_history.append(dashboard_data)
            if len(self.dashboard_history) > self.max_history_size:
                self.dashboard_history = self.dashboard_history[-self.max_history_size:]

            return dashboard_data

        except Exception as e:
            return {
                "error": f"Failed to get real-time metrics: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    async def get_historical_data(self, time_range: str = "1h") -> Dict[str, Any]:
        """Get historical dashboard data for a specific time range."""
        try:
            # Parse time range
            if time_range == "5m":
                cutoff_time = datetime.now() - timedelta(minutes=5)
            elif time_range == "15m":
                cutoff_time = datetime.now() - timedelta(minutes=15)
            elif time_range == "1h":
                cutoff_time = datetime.now() - timedelta(hours=1)
            elif time_range == "6h":
                cutoff_time = datetime.now() - timedelta(hours=6)
            elif time_range == "24h":
                cutoff_time = datetime.now() - timedelta(hours=24)
            else:
                cutoff_time = datetime.now() - timedelta(hours=1)  # default

            # Filter historical data
            filtered_history = []
            for entry in self.dashboard_history:
                entry_time = datetime.fromisoformat(entry["timestamp"])
                if entry_time >= cutoff_time:
                    filtered_history.append(entry)

            # Extract time series data for charts
            time_series = {
                "timestamps": [entry["timestamp"] for entry in filtered_history],
                "tau_values": [entry["hive_metrics"]["tau"]["value"] for entry in filtered_history],
                "phi_values": [entry["hive_metrics"]["phi"]["value"] for entry in filtered_history],
                "sigma_values": [entry["hive_metrics"]["sigma"]["value"] for entry in filtered_history],
                "cpu_values": [entry["resources"]["cpu_percent"] for entry in filtered_history],
                "memory_values": [entry["resources"]["memory_mb"] for entry in filtered_history],
                "teammate_counts": [entry["teammates"]["active"] for entry in filtered_history]
            }

            return {
                "time_range": time_range,
                "data_points": len(filtered_history),
                "time_series": time_series,
                "summary": {
                    "avg_tau": sum(time_series["tau_values"]) / len(time_series["tau_values"]) if time_series["tau_values"] else 0,
                    "avg_phi": sum(time_series["phi_values"]) / len(time_series["phi_values"]) if time_series["phi_values"] else 0,
                    "avg_sigma": sum(time_series["sigma_values"]) / len(time_series["sigma_values"]) if time_series["sigma_values"] else 0,
                    "max_cpu": max(time_series["cpu_values"]) if time_series["cpu_values"] else 0,
                    "max_memory": max(time_series["memory_values"]) if time_series["memory_values"] else 0
                }
            }

        except Exception as e:
            return {
                "error": f"Failed to get historical data: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    async def get_teammate_details(self, teammate_id: str = None) -> Dict[str, Any]:
        """Get detailed information about teammates."""
        try:
            if teammate_id:
                # Get specific teammate details
                teammate = self.hub.registry.teammates.get(teammate_id)
                if teammate:
                    return {
                        "teammate": teammate.get_status(),
                        "load_metrics": self.hub.registry.load_balancer_metrics.get(teammate_id, {}),
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "error": f"Teammate {teammate_id} not found",
                        "timestamp": datetime.now().isoformat()
                    }
            else:
                # Get all teammates summary
                teammates_info = []
                for teammate_id, teammate in self.hub.registry.teammates.items():
                    teammate_info = teammate.get_status()
                    teammate_info["load_metrics"] = self.hub.registry.load_balancer_metrics.get(teammate_id, {})
                    teammates_info.append(teammate_info)

                return {
                    "teammates": teammates_info,
                    "total_count": len(teammates_info),
                    "timestamp": datetime.now().isoformat()
                }

        except Exception as e:
            return {
                "error": f"Failed to get teammate details: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    async def add_custom_alert(self, alert_condition: AlertCondition) -> Dict[str, Any]:
        """Add a custom alert condition."""
        try:
            self.active_alerts[alert_condition.alert_id] = alert_condition

            await self.event_bus.publish_system_event(
                "custom_alert_added",
                {
                    "alert_id": alert_condition.alert_id,
                    "metric_name": alert_condition.metric_name,
                    "condition": alert_condition.condition,
                    "threshold": alert_condition.threshold,
                    "severity": alert_condition.severity
                }
            )

            return {
                "success": True,
                "message": f"Custom alert {alert_condition.alert_id} added successfully"
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to add custom alert: {str(e)}"
            }

    async def remove_alert(self, alert_id: str) -> Dict[str, Any]:
        """Remove an alert condition."""
        try:
            if alert_id in self.active_alerts:
                del self.active_alerts[alert_id]
                return {
                    "success": True,
                    "message": f"Alert {alert_id} removed successfully"
                }
            else:
                return {
                    "success": False,
                    "error": f"Alert {alert_id} not found"
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to remove alert: {str(e)}"
            }

    def generate_dashboard_report(self, time_range: str = "24h") -> str:
        """Generate a text-based dashboard report."""
        try:
            # Get current metrics
            current_data = None
            if self.dashboard_history:
                current_data = self.dashboard_history[-1]

            report = []
            report.append("=" * 60)
            report.append("🌿 HIVE ECOSYSTEM DASHBOARD REPORT")
            report.append("=" * 60)
            report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
            report.append(f"Time Range: {time_range}")
            report.append("")

            if current_data:
                # System Status
                report.append("📊 SYSTEM STATUS")
                report.append("-" * 20)
                report.append(f"Overall Status: {current_data['system_status']}")
                report.append(f"Uptime: {current_data['uptime_seconds']:.0f} seconds")
                report.append("")

                # Hive Metrics
                report.append("🧬 HIVE METRICS (τ, φ, Σ)")
                report.append("-" * 25)
                tau = current_data['hive_metrics']['tau']['value']
                phi = current_data['hive_metrics']['phi']['value']
                sigma = current_data['hive_metrics']['sigma']['value']

                report.append(f"τ (Complexity): {tau:.3f} {'🔴' if tau > 3 else '🟡' if tau > 1.5 else '🟢'}")
                report.append(f"φ (Quality): {phi:.3f} {'🟢' if phi > 0.8 else '🟡' if phi > 0.5 else '🔴'}")
                report.append(f"Σ (Collaboration): {sigma:.3f} {'🟢' if sigma > 0.7 else '🟡' if sigma > 0.4 else '🔴'}")
                report.append("")

                # Resource Usage
                report.append("💻 RESOURCE USAGE")
                report.append("-" * 18)
                cpu = current_data['resources']['cpu_percent']
                memory = current_data['resources']['memory_mb']
                report.append(f"CPU: {cpu:.1f}% {'🔴' if cpu > 80 else '🟡' if cpu > 60 else '🟢'}")
                report.append(f"Memory: {memory:.1f} MB {'🔴' if memory > 800 else '🟡' if memory > 600 else '🟢'}")
                report.append(f"Connections: {current_data['resources']['connections']}")
                report.append("")

                # Teammates
                report.append("🤖 AI TEAMMATES")
                report.append("-" * 15)
                teammates = current_data['teammates']
                report.append(f"Total: {teammates['total']}")
                report.append(f"Active: {teammates['active']}")
                report.append(f"Busy: {teammates['busy']}")
                report.append(f"System Load: {teammates['system_load']:.1%}")
                report.append("")

                # Alerts
                if current_data['alerts']['triggered']:
                    report.append("🚨 ACTIVE ALERTS")
                    report.append("-" * 15)
                    for alert in current_data['alerts']['triggered']:
                        severity_icon = {"critical": "🔴", "warning": "🟡", "info": "🔵"}.get(alert['severity'], "⚪")
                        report.append(f"{severity_icon} {alert['message']}")
                    report.append("")

                # Top Capabilities
                if teammates.get('capability_distribution'):
                    report.append("🎯 TOP CAPABILITIES")
                    report.append("-" * 18)
                    cap_dist = teammates['capability_distribution']
                    sorted_caps = sorted(cap_dist.items(), key=lambda x: x[1], reverse=True)[:5]
                    for cap, count in sorted_caps:
                        report.append(f"{cap}: {count} teammate(s)")
                    report.append("")

            else:
                report.append("No data available - dashboard monitoring may not be active")

            report.append("=" * 60)
            return "\n".join(report)

        except Exception as e:
            return f"Error generating dashboard report: {str(e)}"

    # Private helper methods

    async def _update_metric_trends(self, overview: Dict[str, Any]):
        """Update metric trends for dashboard display."""
        try:
            current_metrics = {
                "tau": overview["health_metrics"]["tau"],
                "phi": overview["health_metrics"]["phi"],
                "sigma": overview["health_metrics"]["sigma"]
            }

            # Calculate trends if we have previous data
            if self.dashboard_history:
                previous_data = self.dashboard_history[-1]
                previous_metrics = {
                    "tau": previous_data["hive_metrics"]["tau"]["value"],
                    "phi": previous_data["hive_metrics"]["phi"]["value"],
                    "sigma": previous_data["hive_metrics"]["sigma"]["value"]
                }

                for metric_name, current_value in current_metrics.items():
                    previous_value = previous_metrics.get(metric_name, current_value)

                    # Calculate change
                    if previous_value != 0:
                        change_percentage = ((current_value - previous_value) / abs(previous_value)) * 100
                    else:
                        change_percentage = 0.0

                    # Determine trend direction
                    if abs(change_percentage) < 1.0:
                        trend_direction = "stable"
                    elif change_percentage > 0:
                        trend_direction = "up"
                    else:
                        trend_direction = "down"

                    self.metric_trends[metric_name] = MetricTrend(
                        metric_name=metric_name,
                        current_value=current_value,
                        previous_value=previous_value,
                        trend_direction=trend_direction,
                        change_percentage=change_percentage
                    )

        except Exception as e:
            print(f"Error updating metric trends: {e}")

    async def _check_alerts(self, overview: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check all alert conditions and return triggered alerts."""
        triggered_alerts = []

        try:
            # Extract metric values
            metric_values = {
                "tau": overview["health_metrics"]["tau"],
                "phi": overview["health_metrics"]["phi"],
                "sigma": overview["health_metrics"]["sigma"],
                "cpu_percent": overview["physics"]["current_metrics"].get("cpu_percent", 0),
                "memory_mb": overview["physics"]["current_metrics"].get("memory_mb", 0)
            }

            for alert_id, alert in self.active_alerts.items():
                if not alert.is_active:
                    continue

                metric_value = metric_values.get(alert.metric_name)
                if metric_value is None:
                    continue

                # Check condition
                triggered = False
                if alert.condition == "greater_than" and metric_value > alert.threshold:
                    triggered = True
                elif alert.condition == "less_than" and metric_value < alert.threshold:
                    triggered = True
                elif alert.condition == "equals" and abs(metric_value - alert.threshold) < 0.001:
                    triggered = True

                if triggered:
                    alert.triggered_count += 1
                    alert.last_triggered = datetime.now()

                    triggered_alerts.append({
                        "alert_id": alert_id,
                        "metric_name": alert.metric_name,
                        "current_value": metric_value,
                        "threshold": alert.threshold,
                        "severity": alert.severity,
                        "message": alert.message,
                        "triggered_count": alert.triggered_count,
                        "last_triggered": alert.last_triggered.isoformat()
                    })

        except Exception as e:
            print(f"Error checking alerts: {e}")

        return triggered_alerts

    def _get_component_health_summary(self, components: Dict[str, Any]) -> Dict[str, str]:
        """Get a summary of component health statuses."""
        health_summary = {}

        try:
            # Event bus health
            event_bus = components.get("event_bus", {})
            error_rate = event_bus.get("error_rate", 0)
            if error_rate < 0.01:
                health_summary["event_bus"] = "healthy"
            elif error_rate < 0.05:
                health_summary["event_bus"] = "warning"
            else:
                health_summary["event_bus"] = "critical"

            # Registry health
            registry = components.get("registry", {})
            total_teammates = registry.get("total_teammates", 0)
            if total_teammates > 0:
                health_summary["registry"] = registry.get("health", "unknown")
            else:
                health_summary["registry"] = "no_teammates"

            # Gateway health
            gateway = components.get("gateway", {})
            health_summary["gateway"] = gateway.get("health", "unknown")

            # ATCG primitives health
            aggregates = components.get("aggregates", {})
            health_summary["aggregates"] = "healthy" if aggregates else "no_components"

            transformations = components.get("transformations", {})
            health_summary["transformations"] = "healthy" if transformations else "no_components"

            connectors = components.get("connectors", {})
            connector_health = []
            for conn_status in connectors.values():
                connector_health.append(conn_status.get("health", "unknown"))

            if connector_health:
                if all(h == "active" for h in connector_health):
                    health_summary["connectors"] = "healthy"
                elif any(h == "degraded" for h in connector_health):
                    health_summary["connectors"] = "degraded"
                else:
                    health_summary["connectors"] = "critical"
            else:
                health_summary["connectors"] = "no_components"

        except Exception as e:
            print(f"Error getting component health summary: {e}")

        return health_summary

    async def _handle_dashboard_event(self, event: PollenEvent):
        """Handle events relevant to the dashboard."""
        # This could trigger dashboard updates or special alerts
        if event.event_type in ["system_started", "system_stopped"]:
            # Major system state changes
            pass
        elif event.event_type in ["teammate_joined", "teammate_left"]:
            # Teammate changes affecting collaboration metrics
            pass

    def get_status(self) -> Dict[str, Any]:
        """Return structured status following the Legibility principle."""
        return {
            "component": "HiveMetricsDashboard",
            "type": "Dashboard",
            "is_active": self.is_active,
            "update_interval": self.update_interval,
            "active_alerts": len([a for a in self.active_alerts.values() if a.is_active]),
            "metrics_history_size": len(self.dashboard_history),
            "metric_trends_count": len(self.metric_trends),
            "timestamp": datetime.now().isoformat(),
            "health": "active" if self.is_active else "inactive"
        }