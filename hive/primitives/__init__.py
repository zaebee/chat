"""
🐝⚡ Hive ATCG Primitives ⚡🐝

Sacred architectural primitives following the ATCG pattern:
- A (Aggregate): Structural organization and state management
- T (Transformation): Stateless processing functions for data transformation  
- C (Connector): Communication and protocol translation
- G (Genesis Event): Generative actions and system-wide broadcasting

These primitives enable clean separation of concerns and sacred architectural alignment.
"""

from .score_transformation import ScoreTransformation
from .review_aggregate import ReviewAggregate
from .agro_event_connector import AgroEventConnector

__all__ = [
    "ScoreTransformation",
    "ReviewAggregate", 
    "AgroEventConnector"
]