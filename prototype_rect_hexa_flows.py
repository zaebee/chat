#!/usr/bin/env python3
"""
Prototype: [rect<hexa>] Data Interconnect/Transform Flows

This prototype demonstrates soft merge between rectangular (strict) and 
hexagonal (flexible) data flow paradigms for markdown processing and 
living documentation systems.
"""

import asyncio
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class RectConstraint:
    """Rectangular paradigm constraint"""
    name: str
    validation_rule: str
    compliance_level: str
    required: bool = True


@dataclass
class HexaNode:
    """Hexagonal paradigm network node"""
    id: str
    label: str
    connections: List[str] = field(default_factory=list)
    transform_func: Optional[callable] = None
    adaptive: bool = True


@dataclass
class MergePoint:
    """Soft merge integration point"""
    rect_stage: str
    hexa_nodes: List[str]
    merge_strategy: str = "enhance_rect"
    compliance_preserved: bool = True


class BoundaryLayer:
    """Interface between [rect] and <hexa> paradigms"""
    
    def __init__(self):
        self.rect_constraints = {}
        self.compliance_monitor = ComplianceMonitor()
    
    def add_rect_constraint(self, constraint: RectConstraint):
        """Add rectangular constraint"""
        self.rect_constraints[constraint.name] = constraint
    
    def validate_rect_input(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate input against rect constraints"""
        validated = data.copy()
        
        for name, constraint in self.rect_constraints.items():
            if constraint.required and name not in validated:
                raise ValueError(f"Required rect constraint '{name}' missing")
            
            if name in validated:
                # Apply validation rule
                if not self._apply_validation_rule(validated[name], constraint.validation_rule):
                    raise ValueError(f"Rect constraint '{name}' validation failed")
        
        return validated
    
    def ensure_rect_output(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure output meets rect constraints"""
        # Apply compliance monitoring
        compliance_result = self.compliance_monitor.check_compliance(data)
        
        if not compliance_result.valid:
            raise ValueError(f"Output compliance failed: {compliance_result.errors}")
        
        return data
    
    def _apply_validation_rule(self, value: Any, rule: str) -> bool:
        """Apply validation rule to value"""
        if rule == "non_empty_string":
            return isinstance(value, str) and len(value.strip()) > 0
        elif rule == "valid_json":
            try:
                json.loads(value) if isinstance(value, str) else json.dumps(value)
                return True
            except:
                return False
        elif rule == "markdown_format":
            return isinstance(value, str) and ("#" in value or "##" in value)
        return True


class HexaNetwork:
    """Hexagonal paradigm transformation network"""
    
    def __init__(self):
        self.nodes = {}
        self.active_connections = set()
    
    def add_node(self, node: HexaNode):
        """Add node to hexa network"""
        self.nodes[node.id] = node
    
    def connect_nodes(self, node1_id: str, node2_id: str):
        """Create bidirectional connection between nodes"""
        if node1_id in self.nodes and node2_id in self.nodes:
            self.nodes[node1_id].connections.append(node2_id)
            self.nodes[node2_id].connections.append(node1_id)
            self.active_connections.add((node1_id, node2_id))
    
    async def transform_data(self, data: Dict[str, Any], entry_node: str) -> Dict[str, Any]:
        """Transform data through hexa network"""
        if entry_node not in self.nodes:
            return data
        
        current_data = data.copy()
        visited_nodes = set()
        
        # Start transformation from entry node
        current_data = await self._transform_at_node(current_data, entry_node, visited_nodes)
        
        return current_data
    
    async def _transform_at_node(self, data: Dict[str, Any], node_id: str, visited: set) -> Dict[str, Any]:
        """Transform data at specific node"""
        if node_id in visited:
            return data
        
        visited.add(node_id)
        node = self.nodes[node_id]
        
        # Apply node transformation
        if node.transform_func:
            data = await node.transform_func(data)
        
        # Propagate to connected nodes if adaptive
        if node.adaptive:
            for connected_id in node.connections:
                if connected_id not in visited:
                    data = await self._transform_at_node(data, connected_id, visited)
        
        return data


class TransformHub:
    """Central hub for [rect<hexa>] data transformations"""
    
    def __init__(self):
        self.boundary = BoundaryLayer()
        self.hexa_network = HexaNetwork()
        self.merge_points = []
        self.rect_processors = {}
    
    def register_rect_processor(self, name: str, processor: callable):
        """Register rectangular processor"""
        self.rect_processors[name] = processor
    
    def create_merge_point(self, rect_stage: str, hexa_nodes: List[str]) -> MergePoint:
        """Create soft merge integration point"""
        merge_point = MergePoint(
            rect_stage=rect_stage,
            hexa_nodes=hexa_nodes
        )
        self.merge_points.append(merge_point)
        return merge_point
    
    async def process_with_soft_merge(self, data: Dict[str, Any], flow_pattern: str) -> Dict[str, Any]:
        """Process data using soft merge pattern"""
        # Phase 1: Rect validation
        validated_data = self.boundary.validate_rect_input(data)
        
        # Phase 2: Apply merge points
        for merge_point in self.merge_points:
            if merge_point.rect_stage in self.rect_processors:
                # Apply rect processor
                rect_result = await self.rect_processors[merge_point.rect_stage](validated_data)
                
                # Apply hexa transformations
                for hexa_node in merge_point.hexa_nodes:
                    hexa_result = await self.hexa_network.transform_data(rect_result, hexa_node)
                    
                    # Merge results based on strategy
                    if merge_point.merge_strategy == "enhance_rect":
                        validated_data = self._enhance_rect_with_hexa(rect_result, hexa_result)
                    elif merge_point.merge_strategy == "hexa_override":
                        validated_data = hexa_result
                    else:
                        validated_data = rect_result
        
        # Phase 3: Rect output validation
        return self.boundary.ensure_rect_output(validated_data)
    
    def _enhance_rect_with_hexa(self, rect_data: Dict[str, Any], hexa_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance rect data with hexa transformations"""
        enhanced = rect_data.copy()
        
        # Add hexa enhancements while preserving rect structure
        for key, value in hexa_data.items():
            if key.startswith("hexa_"):
                enhanced[key] = value
            elif key in enhanced and isinstance(enhanced[key], dict) and isinstance(value, dict):
                enhanced[key].update(value)
        
        return enhanced


class ComplianceMonitor:
    """Monitor compliance during transformations"""
    
    def check_compliance(self, data: Dict[str, Any]) -> 'ComplianceResult':
        """Check data compliance"""
        errors = []
        
        # Check for sensitive data exposure
        if self._contains_sensitive_data(data):
            errors.append("Sensitive data detected in output")
        
        # Check for required metadata
        if "metadata" not in data:
            errors.append("Required metadata missing")
        
        return ComplianceResult(valid=len(errors) == 0, errors=errors)
    
    def _contains_sensitive_data(self, data: Dict[str, Any]) -> bool:
        """Check for sensitive data patterns"""
        sensitive_patterns = ["password", "ssn", "credit_card", "medical_id"]
        data_str = json.dumps(data).lower()
        return any(pattern in data_str for pattern in sensitive_patterns)


@dataclass
class ComplianceResult:
    """Compliance check result"""
    valid: bool
    errors: List[str] = field(default_factory=list)


# Medicine Project Specific Transformations

async def json_parser_transform(data: Dict[str, Any]) -> Dict[str, Any]:
    """Transform JSON data (rect processor)"""
    result = data.copy()
    result["parsed_json"] = True
    result["metadata"] = {
        "processor": "json_parser",
        "timestamp": datetime.now().isoformat(),
        "compliance_level": "medical_strict"
    }
    return result


async def markdown_parser_transform(data: Dict[str, Any]) -> Dict[str, Any]:
    """Transform markdown data (rect processor)"""
    result = data.copy()
    result["parsed_markdown"] = True
    if "metadata" not in result:
        result["metadata"] = {}
    result["metadata"]["markdown_processed"] = True
    return result


async def semantic_analyzer_transform(data: Dict[str, Any]) -> Dict[str, Any]:
    """Semantic analysis transformation (hexa node)"""
    result = data.copy()
    result["hexa_semantic_analysis"] = {
        "entities_extracted": ["clinic", "doctor", "appointment"],
        "relationships": ["doctor_works_at_clinic", "patient_books_appointment"],
        "confidence": 0.85
    }
    return result


async def visual_aggregator_transform(data: Dict[str, Any]) -> Dict[str, Any]:
    """Visual aggregation transformation (hexa node)"""
    result = data.copy()
    result["hexa_visual_aggregation"] = {
        "mermaid_enhanced": True,
        "interactive_elements": ["navigation", "filters", "search"],
        "responsive_design": True
    }
    return result


async def interconnect_mapper_transform(data: Dict[str, Any]) -> Dict[str, Any]:
    """Interconnect mapping transformation (hexa node)"""
    result = data.copy()
    result["hexa_interconnect_mapping"] = {
        "cross_references": ["business/brief.md", "technical/architecture.md"],
        "dependency_graph": {"brief": ["architecture"], "architecture": ["deployment"]},
        "navigation_paths": 3
    }
    return result


async def main():
    """Demonstrate [rect<hexa>] soft merge prototype"""
    print("🔄 [rect<hexa>] Data Interconnect/Transform Flows Prototype")
    print("=" * 60)
    
    # Initialize transform hub
    hub = TransformHub()
    
    # Set up rect constraints
    hub.boundary.add_rect_constraint(RectConstraint(
        name="project_name",
        validation_rule="non_empty_string",
        compliance_level="required"
    ))
    
    hub.boundary.add_rect_constraint(RectConstraint(
        name="documentation",
        validation_rule="markdown_format",
        compliance_level="medical_strict"
    ))
    
    # Register rect processors
    hub.register_rect_processor("json_parser", json_parser_transform)
    hub.register_rect_processor("markdown_parser", markdown_parser_transform)
    
    # Set up hexa network
    semantic_node = HexaNode("semantic_analyzer", "Semantic Analysis", transform_func=semantic_analyzer_transform)
    visual_node = HexaNode("visual_aggregator", "Visual Aggregation", transform_func=visual_aggregator_transform)
    interconnect_node = HexaNode("interconnect_mapper", "Interconnect Mapping", transform_func=interconnect_mapper_transform)
    
    hub.hexa_network.add_node(semantic_node)
    hub.hexa_network.add_node(visual_node)
    hub.hexa_network.add_node(interconnect_node)
    
    # Create connections
    hub.hexa_network.connect_nodes("semantic_analyzer", "visual_aggregator")
    hub.hexa_network.connect_nodes("visual_aggregator", "interconnect_mapper")
    
    # Create merge points
    hub.create_merge_point("json_parser", ["semantic_analyzer"])
    hub.create_merge_point("markdown_parser", ["visual_aggregator", "interconnect_mapper"])
    
    # Test data (medicine project style)
    test_data = {
        "project_name": "Medical Clinic Website",
        "documentation": "# Medical Clinic\n## Services\n### Appointments",
        "json_requirements": {
            "functional_requirements": ["Adaptive design", "Online booking"],
            "nonfunctional": {"performance": "< 2s load time"},
            "compliance": ["HIPAA", "GDPR"]
        }
    }
    
    print("\n📥 Input Data:")
    print(json.dumps(test_data, indent=2))
    
    # Process with soft merge
    try:
        result = await hub.process_with_soft_merge(test_data, "medicine_docs")
        
        print("\n📤 Output Data (after [rect<hexa>] processing):")
        print(json.dumps(result, indent=2))
        
        print("\n✅ Soft merge successful!")
        print(f"   - Rect constraints preserved: {len(hub.boundary.rect_constraints)} constraints")
        print(f"   - Hexa enhancements applied: {len([k for k in result.keys() if k.startswith('hexa_')])} enhancements")
        print(f"   - Merge points executed: {len(hub.merge_points)} points")
        
    except Exception as e:
        print(f"\n❌ Soft merge failed: {e}")
    
    print("\n🔄 Prototype complete - ready for bee.Saga medium-deep collaboration")


if __name__ == "__main__":
    asyncio.run(main())