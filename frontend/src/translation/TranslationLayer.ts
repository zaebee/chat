/**
 * Frontend Translation Layer - Pure Bridge to Protobuf
 * Translates between internal chemical/mystical metaphors and pure protobuf schemas
 * Maintains ontological purity at communication boundaries
 */

// Pure protobuf interfaces (matching backend protobuf schemas)
export interface ProtobufSystemComponent {
  id: string;
  type: 'AGGREGATE' | 'TRANSFORM' | 'CONNECT' | 'GENERATE';
  metadata: Record<string, string>;
  timestamp: number;
  status: Record<string, any>;
}

export interface ProtobufComponentOperation {
  component_id: string;
  type: 'AGGREGATE' | 'TRANSFORM' | 'CONNECT' | 'GENERATE';
  operation_name: string;
  input_data: Uint8Array;
  parameters: Record<string, string>;
  timestamp: number;
}

export interface ProtobufOperationResult {
  success: boolean;
  error_message: string;
  output_data: Uint8Array;
  metrics: Record<string, string>;
  execution_time_ms: number;
  timestamp: number;
}

// Internal component interface (implementation components)
export interface ComponentInterface {
  id: string;
  type: string;
  metadata: Record<string, any>;
  created_at: Date;
  get_status(): Record<string, any>;
}

export interface TranslationMetrics {
  translations_performed: number;
  successful_translations: number;
  failed_translations: number;
  average_translation_time_ms: number;
  success_rate_percent: number;
  last_updated: string;
}

export interface ValidationResult {
  valid: boolean;
  errors: string[];
  warnings: string[];
  fidelity_score: number;
}

export class FrontendTranslationLayer {
  /**
   * Translation layer between chemical/mystical metaphor implementations and pure protobuf
   * 
   * This class maintains ontological purity by:
   * 1. Keeping chemical/mystical metaphors contained within frontend implementation
   * 2. Translating to pure protobuf schemas at boundaries
   * 3. Preserving all functional behavior while purifying communication
   */
  
  private translationMetrics: TranslationMetrics = {
    translations_performed: 0,
    successful_translations: 0,
    failed_translations: 0,
    average_translation_time_ms: 0.0,
    success_rate_percent: 0.0,
    last_updated: new Date().toISOString()
  };

  /**
   * Translate internal SacredComponent (chemical/mystical metaphors) to pure protobuf
   * 
   * Metaphor Translation Mappings:
   * - SacredComponent → SystemComponent
   * - "Sacred/Divine" terminology → "System" terminology
   * - Chemical/mystical metadata → Implementation metadata
   */
  translateToProtobuf(component: ComponentInterface): ProtobufSystemComponent {
    const startTime = performance.now();
    
    try {
      // Map component types from implementation to pure
      const typeMapping: Record<string, ProtobufSystemComponent['type']> = {
        // Pure components (new)
        'DataAggregator': 'AGGREGATE',
        'DataTransformer': 'TRANSFORM',
        'DataConnector': 'CONNECT',
        'DataGenerator': 'GENERATE',
        // Legacy components (for backward compatibility)
        'SacredAggregator': 'AGGREGATE',
        'SacredLambdaEngine': 'TRANSFORM',
        'SacredConnector': 'CONNECT',
        'SacredGenerator': 'GENERATE',
        'DivineLambdaEngine': 'TRANSFORM',
        'IonicAggregator': 'AGGREGATE',
        'QuantumConnector': 'CONNECT',
        'CosmicGenerator': 'GENERATE'
      };
      
      const componentType = component.type;
      const pureType = typeMapping[componentType] || 'AGGREGATE';
      
      // Translate metadata, removing metaphorical references
      const pureMetadata = this.purifyMetadata(component.metadata);
      
      // Get component status through existing interface
      const status = component.get_status();
      const pureStatus = this.purifyStatus(status);
      
      // Create pure protobuf representation
      const protobufComponent: ProtobufSystemComponent = {
        id: component.id,
        type: pureType,
        metadata: pureMetadata,
        timestamp: component.created_at.getTime(),
        status: pureStatus
      };
      
      // Update metrics
      const executionTime = performance.now() - startTime;
      this.updateTranslationMetrics(true, executionTime);
      
      return protobufComponent;
      
    } catch (error) {
      const executionTime = performance.now() - startTime;
      this.updateTranslationMetrics(false, executionTime);
      throw new Error(`Translation to protobuf failed: ${error}`);
    }
  }

  /**
   * Translate pure protobuf back to internal representation format
   * 
   * Note: This returns a plain object representation rather than recreating
   * the full SacredComponent to avoid circular dependencies
   */
  translateFromProtobuf(protobufComponent: ProtobufSystemComponent): Record<string, any> {
    const startTime = performance.now();
    
    try {
      // Map pure types back to implementation terminology (for internal use)
      const typeMapping: Record<string, string> = {
        'AGGREGATE': 'DataAggregator',
        'TRANSFORM': 'DataTransformer',
        'CONNECT': 'DataConnector',
        'GENERATE': 'DataGenerator'
      };
      
      const internalType = typeMapping[protobufComponent.type] || 'SacredComponent';
      
      // Restore internal metadata format
      const internalMetadata = this.restoreMetadata(protobufComponent.metadata);
      
      // Create internal representation
      const internalComponent = {
        id: protobufComponent.id,
        type: internalType,
        metadata: internalMetadata,
        created_at: new Date(protobufComponent.timestamp),
        status: protobufComponent.status
      };
      
      // Update metrics
      const executionTime = performance.now() - startTime;
      this.updateTranslationMetrics(true, executionTime);
      
      return internalComponent;
      
    } catch (error) {
      const executionTime = performance.now() - startTime;
      this.updateTranslationMetrics(false, executionTime);
      throw new Error(`Translation from protobuf failed: ${error}`);
    }
  }

  /**
   * Translate operation request to pure protobuf format
   */
  translateOperationToProtobuf(
    component: ComponentInterface,
    operationName: string,
    inputData: any,
    parameters: Record<string, any> = {}
  ): ProtobufComponentOperation {
    
    // Serialize input data
    let serializedInput: Uint8Array;
    if (typeof inputData === 'object') {
      serializedInput = new TextEncoder().encode(JSON.stringify(inputData));
    } else if (typeof inputData === 'string') {
      serializedInput = new TextEncoder().encode(inputData);
    } else if (inputData instanceof Uint8Array) {
      serializedInput = inputData;
    } else {
      serializedInput = new TextEncoder().encode(String(inputData));
    }
    
    // Convert parameters to string format
    const pureParameters: Record<string, string> = {};
    for (const [key, value] of Object.entries(parameters)) {
      pureParameters[key] = String(value);
    }
    
    // Map component type
    const typeMapping: Record<string, ProtobufComponentOperation['type']> = {
      // Pure components (new)
      'DataAggregator': 'AGGREGATE',
      'DataTransformer': 'TRANSFORM',
      'DataConnector': 'CONNECT',
      'DataGenerator': 'GENERATE',
      // Legacy components (for backward compatibility)
      'SacredAggregator': 'AGGREGATE',
      'SacredLambdaEngine': 'TRANSFORM',
      'SacredConnector': 'CONNECT',
      'SacredGenerator': 'GENERATE'
    };
    const pureType = typeMapping[component.type] || 'AGGREGATE';
    
    return {
      component_id: component.id,
      type: pureType,
      operation_name: operationName,
      input_data: serializedInput,
      parameters: pureParameters,
      timestamp: Date.now()
    };
  }

  /**
   * Translate operation result to pure protobuf format
   */
  translateResultToProtobuf(
    success: boolean,
    resultData: any = null,
    errorMessage: string = '',
    executionTimeMs: number = 0.0,
    metrics: Record<string, any> = {}
  ): ProtobufOperationResult {
    
    // Serialize result data
    let serializedOutput: Uint8Array;
    if (resultData !== null) {
      if (typeof resultData === 'object') {
        serializedOutput = new TextEncoder().encode(JSON.stringify(resultData));
      } else if (typeof resultData === 'string') {
        serializedOutput = new TextEncoder().encode(resultData);
      } else if (resultData instanceof Uint8Array) {
        serializedOutput = resultData;
      } else {
        serializedOutput = new TextEncoder().encode(String(resultData));
      }
    } else {
      serializedOutput = new Uint8Array(0);
    }
    
    // Convert metrics to string format
    const pureMetrics: Record<string, string> = {};
    for (const [key, value] of Object.entries(metrics)) {
      pureMetrics[key] = String(value);
    }
    
    return {
      success,
      error_message: errorMessage,
      output_data: serializedOutput,
      metrics: pureMetrics,
      execution_time_ms: executionTimeMs,
      timestamp: Date.now()
    };
  }

  /**
   * Remove metaphorical terms from metadata
   */
  private purifyMetadata(metadata: Record<string, any>): Record<string, string> {
    const pureMetadata: Record<string, string> = {};
    
    // Metaphorical to pure mappings
    const metaphorMappings: Record<string, string> = {
      'system_id': 'system_id',
      'component_type': 'component_type',
      'connection_strength': 'connection_strength',
      'structural_energy': 'structural_energy',
      'optimization_ratio': 'optimization_ratio',
      'processing_frequency': 'processing_frequency',
      'component_state': 'component_state',
      'system_alignment': 'system_alignment',
      'system_constant': 'system_constant',
      'data_connection': 'data_connection',
      'data_structure': 'data_structure',
      'structural_order': 'structural_order'
    };
    
    for (const [key, value] of Object.entries(metadata)) {
      // Map metaphorical terms to pure terms
      const pureKey = metaphorMappings[key] || key;
      
      // Ensure value is string for protobuf compatibility
      pureMetadata[pureKey] = String(value);
    }
    
    return pureMetadata;
  }

  /**
   * Remove metaphorical terms from status information
   */
  private purifyStatus(status: Record<string, any>): Record<string, any> {
    const pureStatus: Record<string, any> = {};
    
    for (const [key, value] of Object.entries(status)) {
      // Remove metaphorical prefixes/suffixes and normalize
      let pureKey = key.replace(/^system_/, 'system_');
      pureKey = pureKey.replace(/^component_/, 'component_');
      pureKey = pureKey.replace(/^connection_/, 'connection_');
      pureKey = pureKey.replace(/^data_/, 'data_');
      pureKey = pureKey.replace(/_metric$/, '_metric');
      pureKey = pureKey.replace(/_connection$/, '_connection');
      
      pureStatus[pureKey] = value;
    }
    
    return pureStatus;
  }

  /**
   * Restore internal metadata format from pure protobuf
   */
  private restoreMetadata(pureMetadata: Record<string, string>): Record<string, any> {
    const internalMetadata: Record<string, any> = {};
    
    // Pure to internal mappings (identity mapping for pure components)
    const pureMappings: Record<string, string> = {
      'system_id': 'system_id',
      'component_type': 'component_type',
      'connection_strength': 'connection_strength',
      'structural_energy': 'structural_energy',
      'optimization_ratio': 'optimization_ratio',
      'processing_frequency': 'processing_frequency',
      'component_state': 'component_state',
      'system_alignment': 'system_alignment',
      'system_constant': 'system_constant',
      'data_connection': 'data_connection',
      'data_structure': 'data_structure',
      'structural_order': 'structural_order'
    };
    
    for (const [key, value] of Object.entries(pureMetadata)) {
      // Map pure terms back to metaphorical terms for internal use
      const internalKey = pureMappings[key] || key;
      internalMetadata[internalKey] = value;
    }
    
    return internalMetadata;
  }

  /**
   * Update translation performance metrics
   */
  private updateTranslationMetrics(success: boolean, executionTimeMs: number): void {
    this.translationMetrics.translations_performed += 1;
    
    if (success) {
      this.translationMetrics.successful_translations += 1;
    } else {
      this.translationMetrics.failed_translations += 1;
    }
    
    // Update average execution time
    const totalTranslations = this.translationMetrics.translations_performed;
    const currentAvg = this.translationMetrics.average_translation_time_ms;
    const newAvg = ((currentAvg * (totalTranslations - 1)) + executionTimeMs) / totalTranslations;
    this.translationMetrics.average_translation_time_ms = newAvg;
    
    // Update success rate
    this.translationMetrics.success_rate_percent = 
      (this.translationMetrics.successful_translations / totalTranslations) * 100;
    
    this.translationMetrics.last_updated = new Date().toISOString();
  }

  /**
   * Get translation layer performance metrics
   */
  getTranslationMetrics(): TranslationMetrics {
    return { ...this.translationMetrics };
  }

  /**
   * Validate translation fidelity
   */
  validateTranslation(
    originalComponent: any,
    protobufComponent: ProtobufSystemComponent
  ): ValidationResult {
    const validationResult: ValidationResult = {
      valid: true,
      errors: [],
      warnings: [],
      fidelity_score: 1.0
    };
    
    // Check ID preservation
    if (originalComponent.id !== protobufComponent.id) {
      validationResult.errors.push('ID not preserved during translation');
      validationResult.valid = false;
    }
    
    // Check type mapping
    const typeMapping: Record<string, string> = {
      // Pure components (new)
      'DataAggregator': 'AGGREGATE',
      'DataTransformer': 'TRANSFORM',
      'DataConnector': 'CONNECT',
      'DataGenerator': 'GENERATE',
      // Legacy components (for backward compatibility)
      'SacredAggregator': 'AGGREGATE',
      'SacredLambdaEngine': 'TRANSFORM',
      'SacredConnector': 'CONNECT',
      'SacredGenerator': 'GENERATE'
    };
    const expectedType = typeMapping[originalComponent.type];
    if (protobufComponent.type !== expectedType) {
      validationResult.errors.push(
        `Type mapping incorrect: expected ${expectedType}, got ${protobufComponent.type}`
      );
      validationResult.valid = false;
    }
    
    // Check metadata preservation
    const originalMetadataCount = Object.keys(originalComponent.metadata).length;
    const protobufMetadataCount = Object.keys(protobufComponent.metadata).length;
    if (Math.abs(originalMetadataCount - protobufMetadataCount) > 2) {
      validationResult.warnings.push('Significant metadata count difference');
      validationResult.fidelity_score -= 0.1;
    }
    
    return validationResult;
  }
}

// Global translation layer instance
export const frontendTranslator = new FrontendTranslationLayer();

/**
 * Convenience function for translating component to protobuf
 */
export function translateComponentToProtobuf(component: any): ProtobufSystemComponent {
  return frontendTranslator.translateToProtobuf(component);
}

/**
 * Convenience function for translating protobuf to internal format
 */
export function translateProtobufToComponent(protobufComponent: ProtobufSystemComponent): Record<string, any> {
  return frontendTranslator.translateFromProtobuf(protobufComponent);
}

// Legacy aliases for backward compatibility
export const translateSacredComponentToProtobuf = translateComponentToProtobuf;
export const translateProtobufToSacredComponent = translateProtobufToComponent;

/**
 * Get frontend translation layer metrics
 */
export function getFrontendTranslationMetrics(): TranslationMetrics {
  return frontendTranslator.getTranslationMetrics();
}