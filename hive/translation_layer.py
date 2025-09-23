"""
Backend Translation Layer - Pure Bridge to Protobuf
Translates between internal biological metaphors and pure protobuf schemas
Maintains ontological purity at communication boundaries
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime
import json
import uuid

# Import our existing components (with biological metaphors)
from .primitives import HiveComponent, Aggregate, Transformation, Connector, GenesisEvent

@dataclass
class ProtobufSystemComponent:
    """Pure protobuf SystemComponent representation"""
    id: str
    type: str  # "AGGREGATE", "TRANSFORM", "CONNECT", "GENERATE"
    metadata: Dict[str, str]
    timestamp: int
    status: Dict[str, Any]

@dataclass
class ProtobufComponentOperation:
    """Pure protobuf ComponentOperation representation"""
    component_id: str
    type: str
    operation_name: str
    input_data: bytes
    parameters: Dict[str, str]
    timestamp: int

@dataclass
class ProtobufOperationResult:
    """Pure protobuf OperationResult representation"""
    success: bool
    error_message: str
    output_data: bytes
    metrics: Dict[str, str]
    execution_time_ms: float
    timestamp: int

class BackendTranslationLayer:
    """
    Translation layer between biological metaphor implementations and pure protobuf
    
    This class maintains ontological purity by:
    1. Keeping biological metaphors contained within backend implementation
    2. Translating to pure protobuf schemas at boundaries
    3. Preserving all functional behavior while purifying communication
    """
    
    def __init__(self):
        self.translation_metrics = {
            "translations_performed": 0,
            "successful_translations": 0,
            "failed_translations": 0,
            "average_translation_time_ms": 0.0
        }
    
    def translate_to_protobuf(self, hive_component: HiveComponent) -> ProtobufSystemComponent:
        """
        Translate internal HiveComponent (biological metaphors) to pure protobuf
        
        Metaphor Translation Mappings:
        - HiveComponent → SystemComponent
        - "Hive" terminology → "System" terminology
        - Biological metadata → Implementation metadata
        """
        start_time = datetime.now()
        
        try:
            # Map component types from biological to pure
            type_mapping = {
                "Aggregate": "AGGREGATE",
                "Transformation": "TRANSFORM", 
                "Connector": "CONNECT",
                "GenesisEvent": "GENERATE"
            }
            
            component_type = type(hive_component).__name__
            pure_type = type_mapping.get(component_type, "UNSPECIFIED")
            
            # Translate metadata, removing biological references
            pure_metadata = self._purify_metadata(hive_component.metadata)
            
            # Get component status through existing interface
            status = hive_component.get_status()
            pure_status = self._purify_status(status)
            
            # Create pure protobuf representation
            protobuf_component = ProtobufSystemComponent(
                id=hive_component.id,
                type=pure_type,
                metadata=pure_metadata,
                timestamp=int(hive_component.created_at.timestamp() * 1000),
                status=pure_status
            )
            
            # Update metrics
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            self._update_translation_metrics(True, execution_time)
            
            return protobuf_component
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            self._update_translation_metrics(False, execution_time)
            raise Exception(f"Translation to protobuf failed: {str(e)}")
    
    def translate_from_protobuf(self, protobuf_component: ProtobufSystemComponent) -> Dict[str, Any]:
        """
        Translate pure protobuf back to internal representation format
        
        Note: This returns a dictionary representation rather than recreating
        the full HiveComponent to avoid circular dependencies
        """
        start_time = datetime.now()
        
        try:
            # Map pure types back to biological terminology (for internal use)
            type_mapping = {
                "AGGREGATE": "Aggregate",
                "TRANSFORM": "Transformation",
                "CONNECT": "Connector", 
                "GENERATE": "GenesisEvent"
            }
            
            internal_type = type_mapping.get(protobuf_component.type, "Unknown")
            
            # Restore internal metadata format
            internal_metadata = self._restore_metadata(protobuf_component.metadata)
            
            # Create internal representation
            internal_component = {
                "id": protobuf_component.id,
                "type": internal_type,
                "metadata": internal_metadata,
                "created_at": datetime.fromtimestamp(protobuf_component.timestamp / 1000),
                "status": protobuf_component.status
            }
            
            # Update metrics
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            self._update_translation_metrics(True, execution_time)
            
            return internal_component
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            self._update_translation_metrics(False, execution_time)
            raise Exception(f"Translation from protobuf failed: {str(e)}")
    
    def translate_operation_to_protobuf(self, 
                                      component: HiveComponent,
                                      operation_name: str,
                                      input_data: Any,
                                      parameters: Dict[str, Any] = None) -> ProtobufComponentOperation:
        """Translate operation request to pure protobuf format"""
        
        # Serialize input data
        if isinstance(input_data, dict):
            serialized_input = json.dumps(input_data).encode('utf-8')
        elif isinstance(input_data, str):
            serialized_input = input_data.encode('utf-8')
        elif isinstance(input_data, bytes):
            serialized_input = input_data
        else:
            serialized_input = str(input_data).encode('utf-8')
        
        # Convert parameters to string format
        pure_parameters = {}
        if parameters:
            for key, value in parameters.items():
                pure_parameters[key] = str(value)
        
        # Map component type
        component_type = type(component).__name__
        type_mapping = {
            "Aggregate": "AGGREGATE",
            "Transformation": "TRANSFORM",
            "Connector": "CONNECT", 
            "GenesisEvent": "GENERATE"
        }
        pure_type = type_mapping.get(component_type, "UNSPECIFIED")
        
        return ProtobufComponentOperation(
            component_id=component.id,
            type=pure_type,
            operation_name=operation_name,
            input_data=serialized_input,
            parameters=pure_parameters,
            timestamp=int(datetime.now().timestamp() * 1000)
        )
    
    def translate_result_to_protobuf(self,
                                   success: bool,
                                   result_data: Any = None,
                                   error_message: str = "",
                                   execution_time_ms: float = 0.0,
                                   metrics: Dict[str, Any] = None) -> ProtobufOperationResult:
        """Translate operation result to pure protobuf format"""
        
        # Serialize result data
        if result_data is not None:
            if isinstance(result_data, dict):
                serialized_output = json.dumps(result_data).encode('utf-8')
            elif isinstance(result_data, str):
                serialized_output = result_data.encode('utf-8')
            elif isinstance(result_data, bytes):
                serialized_output = result_data
            else:
                serialized_output = str(result_data).encode('utf-8')
        else:
            serialized_output = b""
        
        # Convert metrics to string format
        pure_metrics = {}
        if metrics:
            for key, value in metrics.items():
                pure_metrics[key] = str(value)
        
        return ProtobufOperationResult(
            success=success,
            error_message=error_message,
            output_data=serialized_output,
            metrics=pure_metrics,
            execution_time_ms=execution_time_ms,
            timestamp=int(datetime.now().timestamp() * 1000)
        )
    
    def _purify_metadata(self, metadata: Dict[str, Any]) -> Dict[str, str]:
        """Remove biological metaphors from metadata"""
        pure_metadata = {}
        
        # Biological to pure mappings
        biological_mappings = {
            "hive_id": "system_id",
            "organism_type": "component_type", 
            "dna_sequence": "config_sequence",
            "enzyme_function": "processor_function",
            "cell_membrane": "component_boundary",
            "nervous_system": "communication_layer",
            "mitochondria": "power_unit",
            "nucleus": "control_center",
            "ribosome": "synthesis_engine",
            "endoplasmic_reticulum": "transport_network",
            "golgi_apparatus": "packaging_system",
            "lysosome": "cleanup_mechanism"
        }
        
        for key, value in metadata.items():
            # Map biological terms to pure terms
            pure_key = biological_mappings.get(key, key)
            
            # Purify the value as well
            pure_value = str(value)
            for bio_term, pure_term in biological_mappings.items():
                if bio_term in pure_value:
                    pure_value = pure_value.replace(bio_term, pure_term)
            
            # Additional value purification
            pure_value = pure_value.replace("complex_cell", "complex_component")
            pure_value = pure_value.replace("_cell", "_component")
            pure_value = pure_value.replace("biological", "system")
            
            # Ensure value is string for protobuf compatibility
            pure_metadata[pure_key] = pure_value
        
        return pure_metadata
    
    def _purify_status(self, status: Dict[str, Any]) -> Dict[str, Any]:
        """Remove biological metaphors from status information"""
        pure_status = {}
        
        for key, value in status.items():
            # Remove biological prefixes/suffixes
            pure_key = key.replace("hive_", "system_")
            pure_key = pure_key.replace("_organism", "_component")
            pure_key = pure_key.replace("_dna", "_config")
            
            pure_status[pure_key] = value
        
        return pure_status
    
    def _restore_metadata(self, pure_metadata: Dict[str, str]) -> Dict[str, Any]:
        """Restore internal metadata format from pure protobuf"""
        internal_metadata = {}
        
        # Pure to biological mappings (reverse of purify)
        pure_mappings = {
            "system_id": "hive_id",
            "component_type": "organism_type",
            "config_sequence": "dna_sequence", 
            "processor_function": "enzyme_function",
            "component_boundary": "cell_membrane",
            "communication_layer": "nervous_system"
        }
        
        for key, value in pure_metadata.items():
            # Map pure terms back to biological terms for internal use
            internal_key = pure_mappings.get(key, key)
            internal_metadata[internal_key] = value
        
        return internal_metadata
    
    def _update_translation_metrics(self, success: bool, execution_time_ms: float):
        """Update translation performance metrics"""
        self.translation_metrics["translations_performed"] += 1
        
        if success:
            self.translation_metrics["successful_translations"] += 1
        else:
            self.translation_metrics["failed_translations"] += 1
        
        # Update average execution time
        total_translations = self.translation_metrics["translations_performed"]
        current_avg = self.translation_metrics["average_translation_time_ms"]
        new_avg = ((current_avg * (total_translations - 1)) + execution_time_ms) / total_translations
        self.translation_metrics["average_translation_time_ms"] = new_avg
    
    def get_translation_metrics(self) -> Dict[str, Any]:
        """Get translation layer performance metrics"""
        success_rate = 0.0
        if self.translation_metrics["translations_performed"] > 0:
            success_rate = (self.translation_metrics["successful_translations"] / 
                          self.translation_metrics["translations_performed"]) * 100
        
        return {
            **self.translation_metrics,
            "success_rate_percent": success_rate,
            "last_updated": datetime.now().isoformat()
        }
    
    def validate_translation(self, 
                           original_component: HiveComponent,
                           protobuf_component: ProtobufSystemComponent) -> Dict[str, Any]:
        """Validate translation fidelity"""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "fidelity_score": 1.0
        }
        
        # Check ID preservation
        if original_component.id != protobuf_component.id:
            validation_result["errors"].append("ID not preserved during translation")
            validation_result["valid"] = False
        
        # Check type mapping
        type_mapping = {
            "Aggregate": "AGGREGATE",
            "Transformation": "TRANSFORM",
            "Connector": "CONNECT",
            "GenesisEvent": "GENERATE"
        }
        expected_type = type_mapping.get(type(original_component).__name__)
        if protobuf_component.type != expected_type:
            validation_result["errors"].append(f"Type mapping incorrect: expected {expected_type}, got {protobuf_component.type}")
            validation_result["valid"] = False
        
        # Check metadata preservation
        original_metadata_count = len(original_component.metadata)
        protobuf_metadata_count = len(protobuf_component.metadata)
        if abs(original_metadata_count - protobuf_metadata_count) > 2:  # Allow some mapping differences
            validation_result["warnings"].append("Significant metadata count difference")
            validation_result["fidelity_score"] -= 0.1
        
        return validation_result

# Global translation layer instance
backend_translator = BackendTranslationLayer()

def translate_hive_component_to_protobuf(component: HiveComponent) -> ProtobufSystemComponent:
    """Convenience function for translating HiveComponent to protobuf"""
    return backend_translator.translate_to_protobuf(component)

def translate_protobuf_to_hive_component(protobuf_component: ProtobufSystemComponent) -> Dict[str, Any]:
    """Convenience function for translating protobuf to internal format"""
    return backend_translator.translate_from_protobuf(protobuf_component)

def get_backend_translation_metrics() -> Dict[str, Any]:
    """Get backend translation layer metrics"""
    return backend_translator.get_translation_metrics()