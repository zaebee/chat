"""
Hive Agents: External AI Teammate Integrations

This package contains integrations for external AI systems that can join
the Hive as collaborative teammates, following the Constitution's principles
of Human-AI Symbiosis.

Available Agents:
- MistralAgent: Integration with Mistral AI
- ClaudeAgent: (Future) Integration with Claude
- GPTAgent: (Future) Integration with OpenAI GPT
"""

from .mistral_agent import MistralAgent

__all__ = ["MistralAgent"]