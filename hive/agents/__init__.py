"""
Hive Agents: AI Teammate Integrations

This package contains integrations for AI systems that can join
the Hive as collaborative teammates, following the Constitution's principles
of Human-AI Symbiosis.

Available Agents:
- MistralAgent: Integration with Mistral AI
- GeminiAgent: Integration with Gemini
- SacredChroniclerAgent: Sacred Team eternal organella
- JulesAgent: Sacred Team technical coordinator
- ClaudeAgent: (Future) Integration with Claude
- GPTAgent: (Future) Integration with OpenAI GPT
"""

from .mistral_agent import MistralAgent
from .gemini_agent import GeminiAgent
from .chronicler_agent import SacredChroniclerAgent
from .jules_agent import BeeJules

__all__ = ["MistralAgent", "GeminiAgent", "SacredChroniclerAgent", "BeeJules"]