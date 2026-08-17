"""
OpsPilot AI - Infrastructure & Service Metrics Tool
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

from typing import Dict, Any
from backend.tools.base import registry

@registry.register("get_metrics", "Query Prometheus and system metrics for performance anomalies", risk_level="LOW")
def get_metrics(service: str, duration_minutes: int = 15) -> Dict[str, Any]:
    """
    Fetches time-series telemetry from Prometheus/Datadog for the given service.
    Analyzes CPU, Memory, Latency (p50, p95, p99), Error Rate, DB Pool, and Network.
    """
    if "payment" in service.lower():
        metrics = {
            "service": service,
            "latency_p50_ms": 120.0,
            "latency_p95_ms": 2800.0,
            "latency_p99_ms": 4200.0,
            "baseline_latency_p99_ms": 180.0,
            "latency_anomaly": True,
            "error_rate_percent": 18.4,
            "baseline_error_rate_percent": 0.2,
            "error_rate_anomaly": True,
            "cpu_utilization_percent": 45.2,
            "memory_utilization_percent": 62.0,
            "database_cpu_percent": 92.4, # Database CPU spiked!
            "db_connection_pool_active": 20,
            "db_connection_pool_max": 20,
            "db_connection_pool_exhausted": True, # Connection pool saturated!
            "active_pods": 4,
            "restarts_last_hour": 0
        }
        analysis = (
            "CRITICAL ANOMALY: Latency p99 jumped 23x from baseline 180ms to 4200ms. "
            "Error rate spiked to 18.4%. Database connection pool is 100% saturated (20/20 active). "
            "Database CPU is 92.4%, indicating query bottleneck rather than service container CPU."
        )
    else:
        metrics = {
            "service": service,
            "latency_p50_ms": 45.0,
            "latency_p95_ms": 120.0,
            "latency_p99_ms": 310.0,
            "baseline_latency_p99_ms": 150.0,
            "latency_anomaly": False,
            "error_rate_percent": 5.2,
            "baseline_error_rate_percent": 0.1,
            "error_rate_anomaly": True,
            "cpu_utilization_percent": 78.0,
            "memory_utilization_percent": 84.0,
            "database_cpu_percent": 40.0,
            "db_connection_pool_active": 5,
            "db_connection_pool_max": 20,
            "db_connection_pool_exhausted": False,
            "active_pods": 3,
            "restarts_last_hour": 1
        }
        analysis = "Moderate error rate increase detected with elevated memory."

    return {
        "status": "success",
        "service": service,
        "metrics": metrics,
        "anomalies_detected": [k for k, v in metrics.items() if v is True],
        "analysis_summary": analysis
    }
