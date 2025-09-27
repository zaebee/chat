/**
 * Project Analysis API Service
 *
 * Integrates with Sacred ATCG backend endpoints for 4D→3D project analysis
 * Provides data for ProjectDetailGraph component
 */

import type {
  ProjectNode4D,
  ProjectRelationship,
  DimensionalAnalysis,
  TesseractProjection,
} from "@/atcg/transformations/project_analyzer";

import type { SacredProjectMetrics } from "@/utils/SacredProjectMetrics";

export interface ProjectAnalysisResponse {
  readonly projectId: string;
  readonly nodes: ProjectNode4D[];
  readonly relationships: ProjectRelationship[];
  readonly dimensionalAnalysis: DimensionalAnalysis;
  readonly tesseractProjection: TesseractProjection;
  readonly sacredMetrics: SacredProjectMetrics;
  readonly lastUpdated: string;
}

export interface ProjectHealthResponse {
  readonly projectId: string;
  readonly healthScore: number;
  readonly overallHealth: "Excellent" | "Good" | "Warning" | "Critical";
  readonly criticalIssues: string[];
  readonly recommendations: string[];
  readonly strengths: string[];
  readonly dimensionalStability: string;
  readonly lastAnalyzed: string;
}

/**
 * Dynamic API base URL detection
 * Supports both local development and production deployment
 */
function getApiBaseUrl(): string {
  // Check for environment variable first (Vite environment)
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL;
  }

  // Production detection - if we're on chat.zae.life, use HTTPS
  if (window.location.hostname === "chat.zae.life") {
    return "https://chat.zae.life";
  }

  // Local development detection
  if (
    window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1"
  ) {
    // Try to use the same port as the frontend for backend, or default to 8001
    const frontendPort = window.location.port;
    const backendPort =
      frontendPort === "5173" ? "8001" : frontendPort || "8001";
    return `http://localhost:${backendPort}`;
  }

  // Fallback: use current origin
  return window.location.origin;
}

/**
 * Project Analysis API Client
 */
export class ProjectAnalysisAPI {
  private readonly baseUrl: string;

  constructor() {
    this.baseUrl = getApiBaseUrl();
  }

  /**
   * Fetches complete project analysis including 4D→3D projections
   */
  async getProjectAnalysis(
    projectId: string,
  ): Promise<ProjectAnalysisResponse> {
    try {
      // Use the real Hive analysis endpoint (which includes real data)
      const response = await fetch(
        `${this.baseUrl}/api/hive/project-analysis/${projectId}`,
      );

      if (response.ok) {
        const data = await response.json();
        return data;
      }

      // If endpoint not available, use mock data
      console.warn(
        "Real Hive analysis endpoint not available, using mock data",
      );
      return this.generateMockProjectAnalysis(projectId);
    } catch (error) {
      console.warn(
        "Project analysis endpoint not available, using mock data:",
        error,
      );
      return this.generateMockProjectAnalysis(projectId);
    }
  }

  /**
   * Fetches project health assessment
   */
  async getProjectHealth(projectId: string): Promise<ProjectHealthResponse> {
    try {
      const response = await fetch(
        `${this.baseUrl}/api/hive/project-health/${projectId}`,
      );

      if (!response.ok) {
        throw new Error(
          `Failed to fetch project health: ${response.statusText}`,
        );
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.warn(
        "Project health endpoint not available, using mock data:",
        error,
      );
      return this.generateMockProjectHealth(projectId);
    }
  }

  /**
   * Triggers project analysis refresh
   */
  async refreshProjectAnalysis(projectId: string): Promise<void> {
    try {
      const response = await fetch(
        `${this.baseUrl}/api/hive/project-analysis/${projectId}/refresh`,
        { method: "POST" },
      );

      if (!response.ok) {
        throw new Error(
          `Failed to refresh project analysis: ${response.statusText}`,
        );
      }
    } catch (error) {
      console.warn("Project refresh endpoint not available:", error);
      // Silently continue - mock data doesn't need refreshing
    }
  }

  /**
   * Fetches ATCG distribution for a project
   */
  async getATCGDistribution(projectId: string): Promise<any> {
    try {
      // Use existing topology endpoint as fallback
      const response = await fetch(
        `${this.baseUrl}/api/hive/topology/atcg-distribution`,
      );

      if (response.ok) {
        return await response.json();
      }
    } catch (error) {
      console.warn("ATCG distribution endpoint not available:", error);
    }

    // Return mock ATCG data
    return this.generateMockATCGDistribution(projectId);
  }

  /**
   * Generates mock project analysis data for development/testing
   */
  private generateMockProjectAnalysis(
    projectId: string,
  ): ProjectAnalysisResponse {
    const mockNodes: ProjectNode4D[] = [
      {
        id: `${projectId}-frontend-components`,
        name: "Frontend Components",
        type: "Aggregate",
        atcgType: "A",
        componentCount: 47,
        complexity: 2.318,
        connectionCount: 12,
        coordinates4D: { x: 1, y: 1, z: 0, w: 0.5 },
        isDimensionalBridge: true,
      },
      {
        id: `${projectId}-sacred-transformations`,
        name: "Sacred Transformations",
        type: "Transformation",
        atcgType: "T",
        componentCount: 23,
        complexity: 1.618,
        connectionCount: 8,
        coordinates4D: { x: -1, y: 1, z: 0.5, w: 0 },
        isDimensionalBridge: false,
      },
      {
        id: `${projectId}-api-connectors`,
        name: "API Connectors",
        type: "Connector",
        atcgType: "C",
        componentCount: 31,
        complexity: 1.414,
        connectionCount: 15,
        coordinates4D: { x: -1, y: -1, z: 0, w: -0.5 },
        isDimensionalBridge: true,
      },
      {
        id: `${projectId}-event-genesis`,
        name: "Event Genesis",
        type: "Genesis",
        atcgType: "G",
        componentCount: 19,
        complexity: 2.718,
        connectionCount: 6,
        coordinates4D: { x: 1, y: -1, z: -0.5, w: 0 },
        isDimensionalBridge: false,
      },
    ];

    const mockRelationships: ProjectRelationship[] = [
      {
        from: `${projectId}-frontend-components`,
        to: `${projectId}-sacred-transformations`,
        type: "strong",
        dimensionalBridge: true,
        tesseractEdge: false,
        hexagonalFlow: true,
      },
      {
        from: `${projectId}-sacred-transformations`,
        to: `${projectId}-api-connectors`,
        type: "medium",
        dimensionalBridge: false,
        tesseractEdge: true,
        hexagonalFlow: true,
      },
      {
        from: `${projectId}-api-connectors`,
        to: `${projectId}-event-genesis`,
        type: "strong",
        dimensionalBridge: true,
        tesseractEdge: false,
        hexagonalFlow: false,
      },
      {
        from: `${projectId}-event-genesis`,
        to: `${projectId}-frontend-components`,
        type: "weak",
        dimensionalBridge: false,
        tesseractEdge: true,
        hexagonalFlow: true,
      },
    ];

    const mockDimensionalAnalysis: DimensionalAnalysis = {
      vertices4D: [
        {
          id: 1,
          fourDCoords: "(1,1,1,1)",
          threeDCoords: "(1.0,1.0,1.0)",
          projectionType: "Primary",
          mappedComponent: mockNodes[0].id,
        },
        {
          id: 2,
          fourDCoords: "(-1,1,0.5,0)",
          threeDCoords: "(-0.8,0.8,0.4)",
          projectionType: "W-Slice",
          mappedComponent: mockNodes[1].id,
        },
        {
          id: 3,
          fourDCoords: "(-1,-1,0,-0.5)",
          threeDCoords: "(-0.8,-0.8,0.0)",
          projectionType: "ZW-Slice",
          mappedComponent: mockNodes[2].id,
        },
        {
          id: 4,
          fourDCoords: "(1,-1,-0.5,0)",
          threeDCoords: "(0.8,-0.8,-0.4)",
          projectionType: "Z-Slice",
          mappedComponent: mockNodes[3].id,
        },
      ],
      hexagonalBridges: [
        {
          vertexRatio: 0.75,
          goldenPhiFactor: 1.618034,
          bridgeEfficiency: 0.891,
          dimensionalWindow: 0.405,
        },
      ],
      sacredFrequencies: [
        { name: "Base Φ", value: 699.5, harmonicType: "Base" },
        { name: "4D Bridge", value: 396.0, harmonicType: "Bridge" },
        { name: "Tesseract", value: 440.0, harmonicType: "Tesseract" },
        { name: "Sacred 6", value: 528.0, harmonicType: "Sacred" },
        { name: "Cube 8", value: 528.0, harmonicType: "Sacred" },
      ],
      projectionQuality: {
        fidelity: 0.87,
        informationLoss: 0.23,
        geometricStability: 0.91,
        visualClarity: 0.78,
      },
    };

    const mockTesseractProjection: TesseractProjection = {
      tesseractScore: 2.134,
      bridgeFactor: 1.213,
      sacredRatio: 0.75,
      dimensionalStability: "Good",
      bridgeEfficiency: 0.891,
      projectionMatrix: [
        [1.213, -0.75, 0, 0],
        [0.75, 1.213, 0, 0],
        [0, 0, 1, -0.5],
        [0, 0, 0, 1],
      ],
    };

    const mockSacredMetrics: SacredProjectMetrics = {
      tau: 1.867,
      phi: 1.425,
      sigma: 2.234,
      tesseractScore: 2.134,
      bridgeFactor: 1.213,
      sacredRatio: 0.75,
      dimensionalStability: "Good",
      architecturalComplexity: 1.789,
      componentDistribution: {
        aggregates: 0.26,
        transformations: 0.19,
        connectors: 0.26,
        genesis: 0.16,
        balance: 0.76,
      },
      connectionDensity: 0.67,
      modularityIndex: 0.84,
      goldenRatioAlignment: 0.72,
      hexagonalHarmony: 0.58,
      tesseractCoherence: 0.87,
      analysisTimestamp: new Date().toISOString(),
      projectId,
      nodeCount: mockNodes.length,
      relationshipCount: mockRelationships.length,
    };

    return {
      projectId,
      nodes: mockNodes,
      relationships: mockRelationships,
      dimensionalAnalysis: mockDimensionalAnalysis,
      tesseractProjection: mockTesseractProjection,
      sacredMetrics: mockSacredMetrics,
      lastUpdated: new Date().toISOString(),
    };
  }

  /**
   * Generates mock project health data
   */
  private generateMockProjectHealth(projectId: string): ProjectHealthResponse {
    const healthScores = {
      "master-architecture": 89,
      "intent-level": 92,
      "physics-level": 78,
      "implementation-level": 85,
      "atcg-primitives": 94,
      "codons-level": 81,
      "cell-level": 87,
      "organism-level": 83,
    };

    const healthScore =
      healthScores[projectId as keyof typeof healthScores] || 75;

    let overallHealth: "Excellent" | "Good" | "Warning" | "Critical";
    if (healthScore >= 90) overallHealth = "Excellent";
    else if (healthScore >= 80) overallHealth = "Good";
    else if (healthScore >= 60) overallHealth = "Warning";
    else overallHealth = "Critical";

    const criticalIssues =
      healthScore < 80
        ? [
            "Dimensional projection instability detected",
            "ATCG component imbalance",
          ]
        : [];

    const recommendations = [
      "Enhance hexagonal bridge connections",
      "Optimize Sacred geometry alignment",
      "Implement more 4D→3D transformation patterns",
    ];

    const strengths = [
      "Strong tesseract structural coherence",
      "Excellent golden ratio alignment",
      "Well-balanced ATCG distribution",
    ];

    return {
      projectId,
      healthScore,
      overallHealth,
      criticalIssues,
      recommendations,
      strengths,
      dimensionalStability:
        overallHealth === "Excellent" ? "Excellent" : "Good",
      lastAnalyzed: new Date().toISOString(),
    };
  }

  /**
   * Generates mock ATCG distribution data
   */
  private generateMockATCGDistribution(projectId: string): any {
    return {
      chart_data: [
        {
          type: "Aggregate (A)",
          count: 47,
          color: "#e74c3c",
        },
        {
          type: "Transformation (T)",
          count: 23,
          color: "#3498db",
        },
        {
          type: "Connector (C)",
          count: 31,
          color: "#f39c12",
        },
        {
          type: "Genesis (G)",
          count: 19,
          color: "#27ae60",
        },
      ],
      project_id: projectId,
      analysis_timestamp: new Date().toISOString(),
    };
  }
}

// Export singleton instance
export const projectAnalysisAPI = new ProjectAnalysisAPI();
