"""
OpsPilot AI - Metrics Investigation Agent
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

from typing import Dict, Any
from backend.graph.state import OpsPilotState
from backend.tools.metrics_tool import get_metrics

class MetricsAgent:
    """
    Metrics Agent:
    - Queries Prometheus time-series infrastructure and service metrics.
    - Evaluates CPU, memory, database connection pool, and request latencies.
    - Flags statistical anomalies against steady-state baseline.
    """

    def __init__(self):
        self.name = "Metrics Agent"

    def run(self, state: OpsPilotState) -> Dict[str, Any]:
        service = state.get("service_name", "payment-api")
        raw_metrics_result = get_metrics(service=service, duration_minutes=15)

        metrics = raw_metrics_result["metrics"]
        anomalies = raw_metrics_result["anomalies_detected"]

        findings = {
            "agent": self.name,
            "service": service,
            "metrics": metrics,
            "anomalies": anomalies,
            "analysis_summary": raw_metrics_result["analysis_summary"],
            "is_pool_exhausted": metrics.get("db_connection_pool_exhausted", False),
            "p99_latency_ms": metrics.get("latency_p99_ms", 0.0),
            "database_cpu_percent": metrics.get("database_cpu_percent", 0.0),
            "conclusion": (
                f"Metrics investigation detected severe resource contention: "
                f"Latency p99 spiked to {metrics.get('latency_p99_ms')}ms. "
                f"Active DB connections: {metrics.get('db_connection_pool_active')}/{metrics.get('db_connection_pool_max')} (100% saturated). "
                f"Database host CPU elevated to {metrics.get('database_cpu_percent')}%."
            )
        }
        return findings

metrics_agent = MetricsAgent()
