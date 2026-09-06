"""
OpsPilot AI - Communication & Postmortem Agent
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

from typing import Dict, Any, List
from datetime import datetime
from backend.graph.state import OpsPilotState
from backend.tools.slack_tool import send_slack
from backend.tools.jira_tool import create_jira

class CommunicationAgent:
    """
    Communication Agent:
    - Automatically notifies engineering stakeholders via Slack and Jira.
    - Generates executive summaries and blameless postmortem documentation.
    """

    def __init__(self):
        self.name = "Communication Agent"

    def run(self, state: OpsPilotState) -> Dict[str, Any]:
        service = state.get("service_name", "payment-api")
        incident_num = state.get("incident_number", "INC-1042")
        triage = state.get("triage_result") or {}
        severity = triage.get("severity", "P1")
        root_cause = state.get("root_cause", "Database connection pool exhaustion")
        confidence = state.get("confidence_score", 0.94)

        # 1. Dispatch Slack update
        slack_msg = (
            f"*{severity} Incident Update - {incident_num}*\n"
            f"*Service:* {service}\n"
            f"*Impact:* {state.get('error_rate', 18.4)}% requests failing\n"
            f"*Root Cause:* {root_cause[:120]}...\n"
            f"*Recommended Action:* Rollback to {state.get('target_version', 'v2.4.0')}\n"
            f"*Confidence:* {int(confidence*100)}%"
        )
        slack_res = send_slack(channel="#incidents-prod", title=f"{severity} Incident Update", message=slack_msg)

        # 2. Open Jira Ticket
        jira_res = create_jira(
            service=service,
            title=f"[{severity}] Production incident on {service} - {incident_num}",
            description=f"Automated incident opened by OpsPilot AI.\n\nRoot Cause: {root_cause}\nConfidence: {int(confidence*100)}%",
            priority="Highest" if severity == "P1" else "High"
        )

        # 3. Generate Blameless Postmortem
        postmortem = {
            "incident_number": incident_num,
            "service": service,
            "severity": severity,
            "title": f"Production Outage: Database Query Regression on {service}",
            "summary": (
                f"On {datetime.utcnow().strftime('%Y-%m-%d')}, an automated alert was triggered for {service} "
                f"due to elevated error rate ({state.get('error_rate', 18.4)}%) and p99 latency spikes (4200ms). "
                f"OpsPilot AI identified query latency regression in v2.4.1 causing connection pool exhaustion."
            ),
            "root_cause": root_cause,
            "impact_summary": f"{state.get('error_rate', 18.4)}% of user checkout requests failed. Latency increased by 23x.",
            "resolution": f"Approved rollback of {service} from {(state.get('github_result') or {}).get('latest_version', 'v2.4.1')} to {state.get('target_version', 'v2.4.0')}.",
            "timeline": [
                {"time": "14:32 UTC", "event": "Prometheus fired alert: HighErrorRateAlert on payment-api"},
                {"time": "14:33 UTC", "event": "OpsPilot AI triage agent classified incident as P1 Critical"},
                {"time": "14:34 UTC", "event": "Log & Metrics agents identified 73% DB timeout errors and 100% pool saturation"},
                {"time": "14:35 UTC", "event": "Root cause synthesized with 94% confidence; matched past INC-097 runbook"},
                {"time": "14:36 UTC", "event": "Human approval requested for high-risk production rollback"},
                {"time": "14:37 UTC", "event": "SRE approved rollback; Kubernetes rolled out v2.4.0; error rate restored to 0.4%"}
            ],
            "preventive_actions": [
                "1. Add mandatory query performance benchmark gate in CI/CD pipeline.",
                "2. Implement canary deployment rollout for payment-api service.",
                "3. Configure proactive database slow-query and connection pool utilization alerts in Prometheus.",
                "4. Enforce PgBouncer connection pooling layer in production namespace."
            ],
            "author": "OpsPilot AI - Nivesh Kumar Meena"
        }

        return {
            "agent": self.name,
            "slack_sent": slack_res["delivered"],
            "jira_ticket_key": jira_res["ticket_key"],
            "jira_url": jira_res["jira_url"],
            "postmortem": postmortem
        }

communication_agent = CommunicationAgent()
