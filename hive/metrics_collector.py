"""
ATCG Metrics Collector - Real-time code health monitoring
Implements bee.Queen's dimensional analysis formulas
"""

import ast
import os
import json
import math
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from pathlib import Path
import networkx as nx


@dataclass
class ATCGMetrics:
    """Core ATCG purity metrics"""
    aggregate_purity: float
    transformation_purity: float
    connector_purity: float
    genesis_purity: float
    composite_score: float
    weighted_score: float
    chaos_resistance: float
    singularity_risk: float
    dimensional_integrity: float


class HiveMetricsCollector:
    """Collects and calculates ATCG metrics from codebase"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.dependency_graph = nx.DiGraph()
        self.file_types = {}
        self.connection_matrix = {}
        
    def scan_codebase(self) -> Dict[str, Any]:
        """Scan entire codebase and build dependency graph"""
        file_data = {}
        
        # Scan for relevant files
        patterns = {
            'vue': '**/*.vue',
            'ts': '**/*.ts',
            'js': '**/*.js',
            'jsx': '**/*.jsx',
            'tsx': '**/*.tsx',
            'json': '**/*.json',
            'css': '**/*.css',
            'html': '**/*.html'
        }
        
        for file_type, pattern in patterns.items():
            files = list(self.project_root.glob(pattern))
            # Filter out node_modules and dist
            files = [f for f in files if 'node_modules' not in str(f) and 'dist' not in str(f)]
            
            for file_path in files:
                try:
                    file_data[str(file_path)] = {
                        'type': file_type,
                        'size': file_path.stat().st_size,
                        'dependencies': self._extract_dependencies(file_path, file_type)
                    }
                    self.file_types[str(file_path)] = file_type
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
                    
        return file_data
    
    def _extract_dependencies(self, file_path: Path, file_type: str) -> List[str]:
        """Extract dependencies from file based on type"""
        dependencies = []
        
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            if file_type in ['js', 'ts', 'jsx', 'tsx', 'vue']:
                # Extract import statements
                import_patterns = [
                    r"import.*from\s+['\"]([^'\"]+)['\"]",
                    r"require\(['\"]([^'\"]+)['\"]\)",
                    r"import\(['\"]([^'\"]+)['\"]\)"
                ]
                
                import re
                for pattern in import_patterns:
                    matches = re.findall(pattern, content)
                    dependencies.extend(matches)
                    
            elif file_type == 'json':
                # Extract package dependencies
                try:
                    data = json.loads(content)
                    if 'dependencies' in data:
                        dependencies.extend(data['dependencies'].keys())
                    if 'devDependencies' in data:
                        dependencies.extend(data['devDependencies'].keys())
                except json.JSONDecodeError:
                    pass
                    
        except Exception:
            pass
            
        return dependencies
    
    def build_dependency_graph(self, file_data: Dict[str, Any]) -> nx.DiGraph:
        """Build NetworkX graph from file dependencies"""
        graph = nx.DiGraph()
        
        # Add nodes
        for file_path, data in file_data.items():
            graph.add_node(file_path, **data)
            
        # Add edges
        for file_path, data in file_data.items():
            for dep in data['dependencies']:
                # Try to resolve relative imports to actual files
                resolved_dep = self._resolve_dependency(file_path, dep, file_data)
                if resolved_dep and resolved_dep in file_data:
                    graph.add_edge(file_path, resolved_dep)
                    
        self.dependency_graph = graph
        return graph
    
    def _resolve_dependency(self, source_file: str, dep: str, file_data: Dict[str, Any]) -> str:
        """Resolve dependency path to actual file"""
        source_dir = Path(source_file).parent
        
        # Handle relative imports
        if dep.startswith('.'):
            potential_paths = [
                source_dir / f"{dep}.ts",
                source_dir / f"{dep}.js",
                source_dir / f"{dep}.vue",
                source_dir / f"{dep}/index.ts",
                source_dir / f"{dep}/index.js",
            ]
            
            for path in potential_paths:
                if str(path) in file_data:
                    return str(path)
                    
        return None
    
    def calculate_aggregate_purity(self, file_data: Dict[str, Any]) -> float:
        """Calculate Aggregate (A) purity - Vue component organization"""
        vue_files = [f for f, data in file_data.items() if data['type'] == 'vue']
        if not vue_files:
            return 1.0
            
        total_connections = 0
        internal_connections = 0
        
        for vue_file in vue_files:
            neighbors = list(self.dependency_graph.neighbors(vue_file))
            total_connections += len(neighbors)
            
            # Count connections to other Vue files
            vue_neighbors = [n for n in neighbors if file_data.get(n, {}).get('type') == 'vue']
            internal_connections += len(vue_neighbors)
            
        if total_connections == 0:
            return 1.0
            
        return internal_connections / total_connections
    
    def calculate_transformation_purity(self, file_data: Dict[str, Any]) -> float:
        """Calculate Transformation (T) purity - Function purity in TS/JS"""
        ts_js_files = [f for f, data in file_data.items() 
                      if data['type'] in ['ts', 'js', 'tsx', 'jsx']]
        
        if not ts_js_files:
            return 1.0
            
        pure_score = 0
        total_files = len(ts_js_files)
        
        for file_path in ts_js_files:
            try:
                content = Path(file_path).read_text(encoding='utf-8', errors='ignore')
                
                # Simple heuristics for function purity
                side_effect_indicators = [
                    'console.log', 'document.', 'window.', 'localStorage',
                    'sessionStorage', 'fetch(', 'axios.', 'XMLHttpRequest'
                ]
                
                side_effects = sum(1 for indicator in side_effect_indicators 
                                 if indicator in content)
                
                # Normalize by file size (rough estimate)
                file_score = max(0, 1 - (side_effects / 10))
                pure_score += file_score
                
            except Exception:
                pure_score += 0.5  # Neutral score for unreadable files
                
        return pure_score / total_files if total_files > 0 else 1.0
    
    def calculate_connector_purity(self, file_data: Dict[str, Any]) -> float:
        """Calculate Connector (C) purity - Protocol consistency"""
        if not self.dependency_graph.edges():
            return 1.0
            
        # Analyze connection types
        same_type_connections = 0
        total_connections = 0
        
        for source, target in self.dependency_graph.edges():
            source_type = file_data.get(source, {}).get('type', 'unknown')
            target_type = file_data.get(target, {}).get('type', 'unknown')
            
            total_connections += 1
            if source_type == target_type:
                same_type_connections += 1
                
        protocol_consistency = same_type_connections / total_connections
        
        # Interface stability (simplified - based on file count stability)
        interface_stability = 0.85  # Assume stable for now
        
        return math.sqrt(protocol_consistency * interface_stability)
    
    def calculate_genesis_purity(self, file_data: Dict[str, Any]) -> float:
        """Calculate Genesis (G) purity - Configuration and event quality"""
        config_files = [f for f, data in file_data.items() 
                       if data['type'] in ['json'] or 'config' in f.lower()]
        
        if not config_files:
            return 1.0
            
        # Simple heuristic: fewer config files = better organization
        config_ratio = min(1.0, 10 / len(config_files))  # Ideal: ~10 config files
        
        # Check for circular dependencies in config
        try:
            cycles = list(nx.simple_cycles(self.dependency_graph))
            cycle_penalty = min(0.5, len(cycles) / 20)  # Penalize many cycles
        except:
            cycle_penalty = 0
            
        return config_ratio * (1 - cycle_penalty)
    
    def calculate_chaos_metrics(self, file_data: Dict[str, Any]) -> Tuple[float, float]:
        """Calculate chaos resistance and singularity risk"""
        if not self.dependency_graph.nodes():
            return 1.0, 0.0
            
        # Chaos resistance
        degrees = [self.dependency_graph.degree(node) for node in self.dependency_graph.nodes()]
        max_degree = max(degrees) if degrees else 0
        avg_degree = sum(degrees) / len(degrees) if degrees else 0
        
        hub_concentration = max_degree / avg_degree if avg_degree > 0 else 0
        
        # Connection density
        n_nodes = len(self.dependency_graph.nodes())
        n_edges = len(self.dependency_graph.edges())
        max_edges = n_nodes * (n_nodes - 1) / 2
        connection_density = n_edges / max_edges if max_edges > 0 else 0
        
        chaos_resistance = 1 - (hub_concentration * connection_density / 100)
        singularity_risk = (max_degree / avg_degree) ** 2 * connection_density if avg_degree > 0 else 0
        
        return max(0, min(1, chaos_resistance)), singularity_risk
    
    def calculate_dimensional_integrity(self, file_data: Dict[str, Any]) -> float:
        """Calculate dimensional integrity index"""
        # Count clusters by file type
        type_counts = {}
        for data in file_data.values():
            file_type = data['type']
            type_counts[file_type] = type_counts.get(file_type, 0) + 1
            
        cluster_count = len(type_counts)
        
        # Calculate average cluster cohesion
        total_cohesion = 0
        for file_type in type_counts:
            type_files = [f for f, data in file_data.items() if data['type'] == file_type]
            internal_edges = 0
            total_edges = 0
            
            for file_path in type_files:
                neighbors = list(self.dependency_graph.neighbors(file_path))
                total_edges += len(neighbors)
                same_type_neighbors = [n for n in neighbors 
                                     if file_data.get(n, {}).get('type') == file_type]
                internal_edges += len(same_type_neighbors)
                
            cohesion = internal_edges / total_edges if total_edges > 0 else 1.0
            total_cohesion += cohesion
            
        avg_cohesion = total_cohesion / cluster_count if cluster_count > 0 else 1.0
        
        # Cross-cluster connections
        cross_cluster = sum(1 for source, target in self.dependency_graph.edges()
                           if file_data.get(source, {}).get('type') != 
                              file_data.get(target, {}).get('type'))
        
        return (cluster_count * avg_cohesion) / (cross_cluster + 1)
    
    def collect_metrics(self) -> ATCGMetrics:
        """Main method to collect all ATCG metrics"""
        print("Scanning codebase...")
        file_data = self.scan_codebase()
        
        print("Building dependency graph...")
        self.build_dependency_graph(file_data)
        
        print("Calculating ATCG metrics...")
        
        # Calculate individual metrics
        a_purity = self.calculate_aggregate_purity(file_data)
        t_purity = self.calculate_transformation_purity(file_data)
        c_purity = self.calculate_connector_purity(file_data)
        g_purity = self.calculate_genesis_purity(file_data)
        
        # Composite scores
        composite_score = (a_purity * t_purity * c_purity * g_purity) ** 0.25
        
        # Weighted score (for chat application)
        weighted_score = (a_purity * 0.3 + t_purity * 0.25 + 
                         c_purity * 0.25 + g_purity * 0.2)
        
        # Chaos metrics
        chaos_resistance, singularity_risk = self.calculate_chaos_metrics(file_data)
        
        # Dimensional integrity
        dimensional_integrity = self.calculate_dimensional_integrity(file_data)
        
        return ATCGMetrics(
            aggregate_purity=a_purity,
            transformation_purity=t_purity,
            connector_purity=c_purity,
            genesis_purity=g_purity,
            composite_score=composite_score,
            weighted_score=weighted_score,
            chaos_resistance=chaos_resistance,
            singularity_risk=singularity_risk,
            dimensional_integrity=dimensional_integrity
        )
    
    def generate_report(self, metrics: ATCGMetrics) -> str:
        """Generate human-readable metrics report"""
        def grade(score: float) -> str:
            if score >= 0.9: return "A+"
            elif score >= 0.8: return "A"
            elif score >= 0.7: return "B+"
            elif score >= 0.6: return "B"
            elif score >= 0.5: return "C"
            else: return "D"
        
        report = f"""
🐝 HIVE ATCG METRICS REPORT
==========================

CORE ATCG SCORES:
-----------------
Aggregate (A):      {metrics.aggregate_purity:.3f} ({grade(metrics.aggregate_purity)})
Transformation (T): {metrics.transformation_purity:.3f} ({grade(metrics.transformation_purity)})
Connector (C):      {metrics.connector_purity:.3f} ({grade(metrics.connector_purity)})
Genesis (G):        {metrics.genesis_purity:.3f} ({grade(metrics.genesis_purity)})

COMPOSITE SCORES:
-----------------
ATCG Composite:     {metrics.composite_score:.3f} ({grade(metrics.composite_score)})
Weighted Score:     {metrics.weighted_score:.3f} ({grade(metrics.weighted_score)})

DIMENSIONAL HEALTH:
-------------------
Chaos Resistance:   {metrics.chaos_resistance:.3f} ({grade(metrics.chaos_resistance)})
Singularity Risk:   {metrics.singularity_risk:.3f} ({'⚠️ Monitor' if metrics.singularity_risk > 1.0 else '✅ Safe'})
Dimensional Integrity: {metrics.dimensional_integrity:.3f} ({grade(metrics.dimensional_integrity)})

OVERALL HEALTH: {grade(metrics.weighted_score)}
"""
        return report


def main():
    """CLI interface for metrics collection"""
    collector = HiveMetricsCollector()
    metrics = collector.collect_metrics()
    print(collector.generate_report(metrics))
    
    # Save metrics to JSON
    metrics_dict = {
        'aggregate_purity': metrics.aggregate_purity,
        'transformation_purity': metrics.transformation_purity,
        'connector_purity': metrics.connector_purity,
        'genesis_purity': metrics.genesis_purity,
        'composite_score': metrics.composite_score,
        'weighted_score': metrics.weighted_score,
        'chaos_resistance': metrics.chaos_resistance,
        'singularity_risk': metrics.singularity_risk,
        'dimensional_integrity': metrics.dimensional_integrity
    }
    
    with open('hive_metrics.json', 'w') as f:
        json.dump(metrics_dict, f, indent=2)
    
    print("\n📊 Metrics saved to hive_metrics.json")


if __name__ == "__main__":
    main()