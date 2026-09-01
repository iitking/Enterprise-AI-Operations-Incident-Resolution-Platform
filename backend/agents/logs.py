"""
OpsPilot AI - Log Investigation Agent
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

from typing import Dict, Any
from backend.graph.state import OpsPilotState
from backend.tools.logs_tool import search_logs

class LogInvestigationAgent:
    """
    Log Investigation Agent:
    - Queries centralized application and infrastructure error logs.
    - Filters stack traces, aggregates error frequency, detects patterns.
    """

    def __init__(self):
        self.name = "Log Investigation Agent"

    def run(self, state: OpsPilotState) -> Dict[str, Any]:
        service = state.get("service_name", "payment-api")
        raw_logs_result = search_logs(service=service, minutes_back=15)

        findings = {
            "agent": self.name,
            "service": service,
            "total_errors": raw_logs_result["total_errors_detected"],
            "primary_error": raw_logs_result["primary_error"],
            "symptom_summary": raw_logs_result["symptom_summary"],
            "error_distribution": raw_logs_result["error_distribution"],
            "conclusion": (
                f"Log analysis for '{service}' reveals {raw_logs_result['total_errors_detected']} errors. "
                f"Dominant pattern: {raw_logs_result['primary_error']} "
                f"({raw_logs_result['error_distribution'][0]['percentage']}% of total errors)."
            )
        }
        return findings

logs_agent = LogInvestigationAgent()
