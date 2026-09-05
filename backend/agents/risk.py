"""
OpsPilot AI - Risk & Policy Agent
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

from typing import Dict, Any
from backend.graph.state import OpsPilotState
from backend.security.rbac import evaluate_action_policy

class RiskPolicyAgent:
    """
    Risk & Policy Agent:
    - Enforces enterprise safety boundaries.
    - Classifies remediation actions into LOW, MEDIUM, HIGH, BLOCKED.
    - Determines if human-in-the-loop approval gate must pause the workflow.
    """

    def __init__(self):
        self.name = "Risk & Policy Agent"

    def run(self, state: OpsPilotState) -> Dict[str, Any]:
        service = state.get("service_name", "payment-api")
        github = state.get("github_result") or {}
        confidence = state.get("confidence_score", 0.0)

        # Formulate recommended remediation based on root cause
        target_version = github.get("previous_stable_version") or "v2.4.0"
        
        if any(s in service.lower() for s in ["order", "catalog"]):
            action_name = "restart_service"
        else:
            action_name = "rollback_deployment"

        policy = evaluate_action_policy(action_name)

        approval_payload = {
            "action": action_name,
            "target_service": service,
            "current_version": github.get("latest_version", "v2.4.1"),
            "target_version": target_version,
            "risk_level": policy["risk_level"],
            "requires_approval": policy["requires_approval"],
            "confidence_percent": int(confidence * 100),
            "reason": (
                f"Recent deployment of {service} ({github.get('latest_version')}) "
                f"correlates strongly with increased database query execution latency and connection pool saturation."
            )
        }

        return {
            "agent": self.name,
            "recommended_action": action_name,
            "target_version": target_version,
            "risk_level": policy["risk_level"],
            "requires_approval": policy["requires_approval"],
            "policy_reason": policy["reason"],
            "approval_payload": approval_payload
        }

risk_agent = RiskPolicyAgent()
