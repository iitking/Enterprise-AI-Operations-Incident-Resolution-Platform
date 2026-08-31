"""
OpsPilot AI - Incident Triage Agent
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

from typing import Dict, Any
from backend.graph.state import OpsPilotState

class IncidentTriageAgent:
    """
    Incident Triage Agent:
    - Assesses blast radius and error metrics.
    - Classifies severity (P1 to P4).
    - Formulates prioritized investigation plan.
    """

    def __init__(self):
        self.name = "Incident Triage Agent"

    def run(self, state: OpsPilotState) -> Dict[str, Any]:
        error_rate = state.get("error_rate", 0.0)
        latency_ms = state.get("latency_ms", 0.0)
        env = state.get("environment", "production")
        service = state.get("service_name", "unknown")

        # Classify severity according to SRE enterprise SLA guidelines
        if (error_rate >= 10.0 or latency_ms >= 2500.0) and env == "production":
            severity = "P1"
            urgency = "CRITICAL"
        elif error_rate >= 5.0 or latency_ms >= 1000.0:
            severity = "P2"
            urgency = "HIGH"
        elif error_rate >= 1.0 or latency_ms >= 500.0:
            severity = "P3"
            urgency = "MEDIUM"
        else:
            severity = "P4"
            urgency = "LOW"

        investigation_plan = [
            "search_logs",
            "get_metrics",
            "get_deployment",
            "search_github",
            "retrieve_runbooks_and_postmortems"
        ]

        triage_summary = (
            f"Incident classified as {severity} ({urgency}) for service '{service}' in '{env}'. "
            f"Error rate: {error_rate}%, Latency: {latency_ms}ms. "
            f"Initiating parallel diagnostic investigation across telemetry, infrastructure, source code, and knowledge base."
        )

        return {
            "severity": severity,
            "urgency": urgency,
            "investigation_plan": investigation_plan,
            "triage_summary": triage_summary
        }

triage_agent = IncidentTriageAgent()
