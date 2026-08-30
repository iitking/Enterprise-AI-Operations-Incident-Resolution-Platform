"""
OpsPilot AI - Supervisor & Router Agent
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

from typing import Dict, Any, List
from backend.graph.state import OpsPilotState

class SupervisorAgent:
    """
    Supervisor Agent:
    - Master controller of multi-agent incident investigation.
    - Evaluates incoming context, determines active agent routes.
    - Tracks investigation convergence and ensures sufficient evidence before root-cause synthesis.
    """

    def __init__(self):
        self.name = "Supervisor Agent"

    def plan(self, state: OpsPilotState) -> Dict[str, Any]:
        """Determines initial routing for an incoming alert."""
        service = state.get("service_name")
        error_rate = state.get("error_rate", 0.0)

        required_tracks = ["logs", "metrics", "github", "rag"]

        return {
            "agent": self.name,
            "status": "investigation_started",
            "tracks": required_tracks,
            "decision": f"Routing incident on service '{service}' (error rate {error_rate}%) to parallel investigation tracks."
        }

    def evaluate_convergence(self, state: OpsPilotState) -> bool:
        """Checks if parallel investigations have yielded sufficient evidence."""
        has_logs = state.get("logs_result") is not None
        has_metrics = state.get("metrics_result") is not None
        has_github = state.get("github_result") is not None
        return has_logs and has_metrics and has_github

supervisor_agent = SupervisorAgent()
