#!/usr/bin/env python3
"""
Performance monitoring and metrics collection.
"""

import time
import statistics
from typing import List, Dict, Any
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

class PerformanceMetrics:
    """Collect and analyze performance metrics."""
    
    def __init__(self):
        self.metrics = {
            'initialization_time': [],
            'document_loading_time': [],
            'qa_response_times': [],
            'summarization_times': [],
            'search_times': [],
            'embedding_times': []
        }
    
    @contextmanager
    def measure_time(self, metric_name: str):
        """Context manager to measure execution time."""
        start_time = time.time()
        try:
            yield
        finally:
            execution_time = time.time() - start_time
            self.add_metric(metric_name, execution_time)
            logger.debug(f"{metric_name}: {execution_time:.3f}s")
    
    def add_metric(self, metric_name: str, value: float):
        """Add a metric value."""
        if metric_name not in self.metrics:
            self.metrics[metric_name] = []
        self.metrics[metric_name].append(value)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get performance summary statistics."""
        summary = {}
        
        for metric_name, values in self.metrics.items():
            if values:
                summary[metric_name] = {
                    'count': len(values),
                    'mean': statistics.mean(values),
                    'median': statistics.median(values),
                    'min': min(values),
                    'max': max(values),
                    'std_dev': statistics.stdev(values) if len(values) > 1 else 0
                }
            else:
                summary[metric_name] = {
                    'count': 0,
                    'mean': 0,
                    'median': 0,
                    'min': 0,
                    'max': 0,
                    'std_dev': 0
                }
        
        return summary
    
    def print_summary(self):
        """Print formatted performance summary."""
        summary = self.get_summary()
        
        print("\n" + "="*60)
        print("PERFORMANCE METRICS SUMMARY")
        print("="*60)
        
        for metric_name, stats in summary.items():
            if stats['count'] > 0:
                print(f"\n📊 {metric_name.replace('_', ' ').title()}:")
                print(f"  Count: {stats['count']}")
                print(f"  Mean: {stats['mean']:.3f}s")
                print(f"  Median: {stats['median']:.3f}s")
                print(f"  Range: {stats['min']:.3f}s - {stats['max']:.3f}s")
                if stats['std_dev'] > 0:
                    print(f"  Std Dev: {stats['std_dev']:.3f}s")
    
    def export_metrics(self, filepath: str):
        """Export metrics to JSON file."""
        import json
        
        summary = self.get_summary()
        summary['timestamp'] = time.time()
        summary['raw_data'] = self.metrics
        
        with open(filepath, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Metrics exported to {filepath}")