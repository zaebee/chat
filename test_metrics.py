#!/usr/bin/env python3
"""
Test the ATCG metrics collector on current Hive
"""

from hive.metrics_collector import HiveMetricsCollector

def main():
    print("🐝 Testing ATCG Metrics Collector on Current Hive")
    print("=" * 50)
    
    collector = HiveMetricsCollector(".")
    metrics = collector.collect_metrics()
    
    print(collector.generate_report(metrics))
    
    # Validate against bee.Queen's manual calculations
    print("\n🔍 VALIDATION AGAINST BEE.QUEEN'S ANALYSIS:")
    print("-" * 45)
    
    expected_ranges = {
        'aggregate_purity': (0.65, 0.75),
        'transformation_purity': (0.70, 0.80),
        'connector_purity': (0.40, 0.50),
        'genesis_purity': (0.80, 0.90),
        'weighted_score': (0.65, 0.75)
    }
    
    for metric, (min_val, max_val) in expected_ranges.items():
        actual = getattr(metrics, metric)
        status = "✅" if min_val <= actual <= max_val else "⚠️"
        print(f"{metric:20}: {actual:.3f} (expected {min_val:.2f}-{max_val:.2f}) {status}")
    
    print(f"\n🎯 Overall Assessment: {'MATCHES BEE.QUEEN ANALYSIS' if 0.65 <= metrics.weighted_score <= 0.75 else 'NEEDS CALIBRATION'}")

if __name__ == "__main__":
    main()