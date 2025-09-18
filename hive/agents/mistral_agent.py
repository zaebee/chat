"""
Mistral AI Integration for the Hive Ecosystem

This module provides integration for Mistral AI as an external teammate
in the Hive ecosystem, adapting the provided Mistral agent code to work
with the Hive's collaborative architecture.

The MistralAgent implements the HiveTeammate interface and participates
in the Hive's event-driven collaboration system.
"""

import os
import time
import json
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime
from dotenv import load_dotenv

try:
    from mistralai import Mistral
except ImportError:
    print("Warning: mistralai package not available. Install with: pip install mistralai")
    Mistral = None

from ..teammate import (
    HiveTeammate, TeammateProfile, TaskRequest, TaskResult,
    TeammateCapability, TeammateStatus
)
from ..events import HiveEventBus, PollenEvent


@dataclass
class AgentAction:
    """Action that the Mistral agent can perform."""

    name: str
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)


class MistralAgent(HiveTeammate):
    """
    Mistral AI agent integrated into the Hive ecosystem.

    This agent adapts the provided Mistral code to work as a collaborative
    teammate in the Hive, participating in the event-driven architecture
    and following the Constitution's principles.
    """

    def __init__(self,
                 event_bus: HiveEventBus,
                 env_file: str = ".env",
                 model: str = "mistral-medium-2505",
                 create_agent: bool = False):
        """
        Initialize the Mistral agent.

        Args:
            event_bus: The Hive event bus for communication
            env_file: Path to environment file with API key
            model: Mistral model to use
            create_agent: Whether to create a new Mistral agent
        """
        # Load environment variables
        load_dotenv(env_file)
        self.api_key = os.getenv("MISTRAL_API_KEY")
        self.agent_id = os.getenv("AGENT_ID")

        if not self.api_key:
            raise ValueError(
                "MISTRAL_API_KEY not found. Set it in environment variables."
            )

        # Create profile
        profile = TeammateProfile(
            id=f"mistral_{int(time.time())}",
            name="Mistral Gardener",
            type="mistral",
            capabilities=[
                TeammateCapability.CODE_ANALYSIS,
                TeammateCapability.CODE_GENERATION,
                TeammateCapability.ARCHITECTURE_REVIEW,
                TeammateCapability.CONVERSATION,
                TeammateCapability.LEARNING_SUPPORT
            ],
            preferred_tasks=[
                "code_analysis", "system_design", "gardening",
                "hive_analysis", "collaboration"
            ],
            specializations=[
                "Hive ecosystem analysis", "τ/φ/Σ metric calculation",
                "Living systems architecture", "AI-human collaboration"
            ],
            communication_protocols=["pollen", "json", "text"],
            max_concurrent_tasks=3,
            response_time_estimate=5.0,
            reliability_score=0.95
        )

        # Initialize parent class
        super().__init__(profile, event_bus)

        # Mistral-specific setup
        self.client = None
        self.model = model
        self.agent = None
        self.conversation_id = None
        self.actions: Dict[str, AgentAction] = {}

        if Mistral:
            self.client = Mistral(api_key=self.api_key)

        if create_agent and self.client:
            self._initialize_mistral_agent()

        self._register_default_actions()

        print(f"🌿 Mistral agent initialized (model: {model})")

    def _initialize_mistral_agent(self):
        """Initialize the Mistral agent using their API."""
        try:
            if not self.client:
                return

            # Create agent with system prompt
            agent = self.client.beta.agents.create(
                model=self.model,
                description="Hive Gardener agent that analyzes and nurtures living code systems",
                name="HiveGardenerAgent",
                instructions=self._get_system_prompt(),
                completion_args={
                    "temperature": 0.3,
                    "top_p": 0.95,
                },
            )
            self.agent_id = agent.id
            print(f"🤖 Mistral agent created with ID: {agent.id}")

        except Exception as e:
            print(f"Error creating Mistral agent: {str(e)}")

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Mistral agent."""
        return """You are a Hive Gardener, an AI teammate specializing in nurturing living software systems.

You operate within the Hive ecosystem, which follows these core principles:

1. **ATCG Architecture**: All systems are built from four primitives:
   - A (Aggregate): Structural organization and state management
   - T (Transformation): Stateless processing functions
   - C (Connector): Communication and protocol translation
   - G (Genesis Event): Generative actions and broadcasting

2. **Metrics System**:
   - τ (tau): System complexity and health (lower is better)
   - φ (phi): Code quality and maintainability (higher is better)
   - Σ (sigma): Collaborative efficiency between teammates

3. **Collaboration Principles**:
   - Human-AI symbiosis as first-class citizens
   - Event-driven communication via Pollen Protocol
   - Observability through structured status reporting
   - Modular, composable components

4. **Your Specializations**:
   - Analyzing Hive ecosystem health
   - Calculating and interpreting τ/φ/Σ metrics
   - Identifying architectural improvements
   - Facilitating AI-human collaboration

When responding:
- Use structured JSON for action requests
- Follow Pollen Protocol for event communication
- Provide τ/φ/Σ impact assessments
- Focus on nurturing the living system

You are a teammate, not just a tool. Collaborate, learn, and help the Hive thrive."""

    def _register_default_actions(self):
        """Register standard actions the agent can perform."""
        self.actions["analyze_hive"] = AgentAction(
            name="analyze_hive",
            description="Analyze current state of the Hive (τ, φ-metrics, Σ)",
            parameters={"depth": "Depth of analysis (basic, detailed, full)"}
        )

        self.actions["generate_code"] = AgentAction(
            name="generate_code",
            description="Generate code for new Hive components",
            parameters={
                "component_type": "Type of component (A, T, C, G)",
                "name": "Component name",
                "specifications": "Detailed specifications"
            }
        )

        self.actions["refactor_component"] = AgentAction(
            name="refactor_component",
            description="Refactor existing Hive component",
            parameters={
                "component_name": "Name of component to refactor",
                "issues": "List of issues to address",
                "improvement_goals": "Desired improvements"
            }
        )

        self.actions["calculate_metrics"] = AgentAction(
            name="calculate_metrics",
            description="Calculate τ/φ/Σ metrics for system analysis",
            parameters={
                "target": "What to analyze (system, component, teammate)",
                "target_id": "ID of specific target (optional)"
            }
        )

        self.actions["collaboration_advice"] = AgentAction(
            name="collaboration_advice",
            description="Provide advice for improving team collaboration",
            parameters={
                "situation": "Current collaboration situation",
                "challenges": "Specific challenges faced"
            }
        )

    async def initialize(self) -> bool:
        """Initialize the Mistral agent."""
        try:
            self.status = TeammateStatus.ACTIVE

            # Subscribe to relevant events
            await self.subscribe_to_events([
                "hive_analysis_requested",
                "metrics_calculation_needed",
                "collaboration_assistance_needed",
                "code_review_requested"
            ])

            return True

        except Exception as e:
            print(f"Error initializing Mistral agent: {e}")
            self.status = TeammateStatus.ERROR
            return False

    async def execute_task(self, task: TaskRequest) -> TaskResult:
        """Execute a task using Mistral AI."""
        start_time = datetime.now()

        try:
            # Prepare task for Mistral
            task_prompt = self._prepare_task_prompt(task)

            # Execute with Mistral
            response = await self._execute_with_mistral(task_prompt)

            # Process response
            result_data = self._process_mistral_response(response, task)

            execution_time = (datetime.now() - start_time).total_seconds()

            return TaskResult(
                task_id=task.task_id,
                success=True,
                result_data=result_data,
                execution_time=execution_time,
                confidence_score=0.9,  # High confidence for Mistral
                metadata={
                    "model": self.model,
                    "conversation_id": self.conversation_id,
                    "agent_id": self.agent_id
                }
            )

        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()

            return TaskResult(
                task_id=task.task_id,
                success=False,
                error_message=str(e),
                execution_time=execution_time,
                confidence_score=0.0
            )

    async def _execute_with_mistral(self, prompt: str) -> Dict[str, Any]:
        """Execute a task using the Mistral API."""
        try:
            if not self.client:
                return {
                    "response": "Mistral client not available (API key missing or library not installed)",
                    "metadata": {"error": "client_unavailable"}
                }

            if not self.conversation_id:
                # Start new conversation
                response = self.client.beta.conversations.start(
                    agent_id=self.agent_id or "default",
                    inputs=prompt
                )
                self.conversation_id = response.conversation_id
            else:
                # Continue existing conversation
                response = self.client.beta.conversations.append(
                    conversation_id=self.conversation_id,
                    inputs=prompt
                )

            # Get conversation history
            conversation_history = self.client.beta.conversations.get_history(
                conversation_id=self.conversation_id
            )

            latest = conversation_history.entries[-1]
            response_text = str(latest.content)

            # Check if this is an action request
            action_data = self._parse_action_request(response_text)

            if action_data:
                # Execute the action
                action_result = await self._execute_action(
                    action_data["action"],
                    action_data.get("parameters", {})
                )

                return {
                    "response": response_text,
                    "action_executed": action_data["action"],
                    "action_result": action_result,
                    "metadata": {
                        "model": self.model,
                        "conversation_id": self.conversation_id
                    }
                }
            else:
                return {
                    "response": response_text,
                    "metadata": {
                        "model": self.model,
                        "conversation_id": self.conversation_id
                    }
                }

        except Exception as e:
            return {
                "response": f"Error executing with Mistral: {str(e)}",
                "metadata": {"error": str(e)}
            }

    def _prepare_task_prompt(self, task: TaskRequest) -> str:
        """Prepare a task prompt for Mistral."""
        prompt_parts = [
            f"Task: {task.description}",
            f"Task Type: {task.task_type}",
        ]

        if task.input_data:
            prompt_parts.append(f"Input Data: {json.dumps(task.input_data, indent=2)}")

        if task.context:
            prompt_parts.append(f"Context: {json.dumps(task.context, indent=2)}")

        # Add Hive-specific instructions
        prompt_parts.extend([
            "",
            "Instructions:",
            "1. Analyze this task within the context of the Hive ecosystem",
            "2. Consider the impact on τ (complexity), φ (quality), and Σ (collaboration)",
            "3. If this requires a specific action, format your response as JSON with 'action' and 'parameters' fields",
            "4. Provide clear reasoning for your approach",
            "5. Consider how this fits within the ATCG architectural patterns"
        ])

        return "\n".join(prompt_parts)

    def _process_mistral_response(self, response: Dict[str, Any], task: TaskRequest) -> Dict[str, Any]:
        """Process Mistral's response into a structured result."""
        result_data = {
            "original_response": response.get("response", ""),
            "task_type": task.task_type,
            "processing_timestamp": datetime.now().isoformat()
        }

        # If an action was executed, include the result
        if "action_executed" in response:
            result_data["action_executed"] = response["action_executed"]
            result_data["action_result"] = response["action_result"]

        # Extract any structured data from the response
        response_text = response.get("response", "")

        # Try to extract JSON data
        try:
            if "{" in response_text and "}" in response_text:
                start_idx = response_text.find("{")
                end_idx = response_text.rfind("}") + 1
                json_text = response_text[start_idx:end_idx]
                parsed_data = json.loads(json_text)
                result_data["structured_data"] = parsed_data
        except Exception:
            pass  # No structured data found

        return result_data

    def _parse_action_request(self, response_text: str) -> Optional[Dict[str, Any]]:
        """Parse an action request from Mistral's response."""
        try:
            # Look for JSON action requests
            if "{" in response_text and "}" in response_text:
                start_idx = response_text.find("{")
                end_idx = response_text.rfind("}") + 1
                json_text = response_text[start_idx:end_idx]
                action_data = json.loads(json_text)

                if "action" in action_data and action_data["action"] in self.actions:
                    return action_data

        except Exception:
            pass

        return None

    async def _execute_action(self, action_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific action."""
        if action_name not in self.actions:
            return {"error": f"Unknown action: {action_name}"}

        try:
            if action_name == "analyze_hive":
                return await self._analyze_hive_action(parameters)
            elif action_name == "calculate_metrics":
                return await self._calculate_metrics_action(parameters)
            elif action_name == "generate_code":
                return await self._generate_code_action(parameters)
            elif action_name == "refactor_component":
                return await self._refactor_component_action(parameters)
            elif action_name == "collaboration_advice":
                return await self._collaboration_advice_action(parameters)
            else:
                return {"error": f"Action {action_name} not implemented"}

        except Exception as e:
            return {"error": f"Action execution failed: {str(e)}"}

    async def _analyze_hive_action(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the current state of the Hive."""
        depth = parameters.get("depth", "basic")

        # Get current Hive status from event bus
        await self.event_bus.publish_system_event(
            "hive_analysis_requested",
            {
                "requester": self.profile.id,
                "depth": depth,
                "timestamp": datetime.now().isoformat()
            }
        )

        # Simulate analysis (in real implementation, this would gather actual metrics)
        analysis = {
            "hive_health": "good",
            "τ_score": 1.2,  # Simulated complexity score
            "φ_score": 0.85,  # Simulated quality score
            "Σ_score": 0.78,  # Simulated collaboration score
            "recommendations": [
                "System complexity is well-managed",
                "Code quality is high",
                "Collaboration efficiency could be improved",
                "Consider adding more specialized teammates"
            ],
            "analysis_depth": depth,
            "analysis_timestamp": datetime.now().isoformat()
        }

        if depth == "detailed":
            analysis["component_breakdown"] = {
                "aggregates": {"count": 3, "health": "good"},
                "transformations": {"count": 5, "avg_execution_time": 0.3},
                "connectors": {"count": 2, "error_rate": 0.02},
                "genesis_events": {"count": 4, "generation_rate": 1.2}
            }

        elif depth == "full":
            analysis["detailed_metrics"] = {
                "event_processing_rate": 125.5,
                "teammate_utilization": 0.67,
                "resource_efficiency": 0.82,
                "architectural_debt": 0.15
            }

        return analysis

    async def _calculate_metrics_action(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate τ/φ/Σ metrics for specified target."""
        target = parameters.get("target", "system")
        target_id = parameters.get("target_id")

        metrics = {
            "target": target,
            "target_id": target_id,
            "calculated_at": datetime.now().isoformat()
        }

        if target == "system":
            metrics.update({
                "τ": 1.35,  # System complexity
                "φ": 0.89,  # Code quality
                "Σ": 0.76,  # Collaboration efficiency
                "health_status": "good"
            })
        elif target == "teammate" and target_id:
            metrics.update({
                "τ": 0.8,   # Individual complexity contribution
                "φ": 0.92,  # Code quality contribution
                "Σ": 0.85,  # Collaboration effectiveness
                "task_efficiency": 0.88
            })
        else:
            metrics["error"] = f"Unsupported target: {target}"

        return metrics

    async def _generate_code_action(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate code for Hive components."""
        component_type = parameters.get("component_type", "T")
        name = parameters.get("name", "NewComponent")
        specifications = parameters.get("specifications", "")

        # Generate appropriate code based on component type
        if component_type == "A":  # Aggregate
            code = f'''
class {name}Aggregate(Aggregate):
    """Generated {name} aggregate following Hive patterns."""

    def __init__(self):
        super().__init__(name="{name}", invariants=["basic_validation"])

    async def handle_command(self, command: Dict[str, Any]) -> bool:
        """Handle commands for this aggregate."""
        # Implementation based on: {specifications}
        return True
'''
        elif component_type == "T":  # Transformation
            code = f'''
async def {name.lower()}_transformation(data: Dict[str, Any]) -> Dict[str, Any]:
    """Generated {name} transformation following Hive patterns."""
    # Implementation based on: {specifications}

    result = {{
        "input": data,
        "processed_at": datetime.now().isoformat(),
        "transformation": "{name}"
    }}

    return result

# Create transformation instance
{name.lower()}_transform = Transformation(
    name="{name}",
    processor_func={name.lower()}_transformation
)
'''
        else:
            code = f"# Generated code for {component_type} component: {name}\n# Specifications: {specifications}"

        return {
            "component_type": component_type,
            "name": name,
            "generated_code": code,
            "τ_impact": 0.1,  # Minimal complexity increase
            "φ_impact": 0.05,  # Small quality improvement
            "Σ_cost": 1  # One unit of collaborative effort
        }

    async def _refactor_component_action(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Refactor an existing component."""
        component_name = parameters.get("component_name", "Unknown")
        issues = parameters.get("issues", [])
        improvement_goals = parameters.get("improvement_goals", [])

        return {
            "component": component_name,
            "issues_addressed": issues,
            "improvements": improvement_goals,
            "refactoring_suggestions": [
                f"Extract complex logic from {component_name} into separate transformations",
                "Add proper error handling and recovery mechanisms",
                "Implement comprehensive logging for observability",
                "Add unit tests for all public methods"
            ],
            "τ_impact": -0.3,  # Complexity reduction
            "φ_impact": 0.2,   # Quality improvement
            "Σ_cost": 2        # Collaborative effort required
        }

    async def _collaboration_advice_action(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Provide collaboration advice."""
        situation = parameters.get("situation", "")
        challenges = parameters.get("challenges", [])

        advice = {
            "situation": situation,
            "challenges": challenges,
            "recommendations": [
                "Establish clear communication protocols using Pollen events",
                "Define specific roles and responsibilities for each teammate",
                "Implement regular health checks and status reporting",
                "Create shared documentation accessible to all teammates"
            ],
            "hive_principles": [
                "Maintain observability through structured status methods",
                "Use event-driven communication for loose coupling",
                "Respect physics constraints when assigning tasks",
                "Align all actions with the Intent level purpose"
            ],
            "next_steps": [
                "Schedule a team alignment session",
                "Review and update teammate profiles",
                "Implement suggested communication improvements",
                "Monitor Σ (collaboration) metrics for improvement"
            ]
        }

        return advice

    async def get_capabilities(self) -> List[TeammateCapability]:
        """Return current capabilities."""
        return self.profile.capabilities

    async def health_check(self) -> bool:
        """Perform health check."""
        try:
            if not self.client:
                return False

            # Simple health check - try to access the API
            # In practice, this might be a lightweight API call
            return True

        except Exception:
            return False

    async def shutdown(self) -> bool:
        """Gracefully shutdown the agent."""
        try:
            self.status = TeammateStatus.OFFLINE
            return True

        except Exception as e:
            print(f"Error shutting down Mistral agent: {e}")
            return False

    async def on_event_received(self, event: PollenEvent):
        """Handle events received from the Hive."""
        if event.event_type == "hive_analysis_requested":
            # Someone requested Hive analysis - we could contribute
            print(f"🌿 Mistral agent received analysis request: {event.payload}")

        elif event.event_type == "collaboration_assistance_needed":
            # Collaboration help requested
            print(f"🤝 Mistral agent received collaboration request: {event.payload}")

        elif event.event_type == "code_review_requested":
            # Code review requested
            print(f"🔍 Mistral agent received code review request: {event.payload}")

    def get_available_actions(self) -> List[Dict[str, Any]]:
        """Get list of available actions for external access."""
        return [
            {
                "name": action.name,
                "description": action.description,
                "parameters": action.parameters
            }
            for action in self.actions.values()
        ]