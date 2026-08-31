"""
OpsPilot AI - Agent Unit Tests
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

import unittest
from backend.agents.triage import triage_agent
from backend.agents.logs import logs_agent
from backend.agents.metrics import metrics_agent
from backend.agents.github import code_deployment_agent
from backend.agents.root_cause import root_cause_agent
from backend.agents.risk import risk_agent
from backend.agents.communication import communication_agent
from backend.graph.state import OpsPilotState

class TestOpsPilotAgents(unittest.TestCase):

    def setUp(self):
        self.sample_state: OpsPilotState = {
            "incident_id": "test-inc-101",
            "incident_number": "INC-101",
            "service_name": "payment-api",
            "title": "Payment API Critical Failure",
            "environment": "production",
            "created_at": "2026-10-08T00:00:00Z",
            "error_rate": 18.4,
            "latency_ms": 4200.0,
            "raw_alert": {},
            "triage_result": None,
            "logs_result": None,
            "metrics_result": None,
            "github_result": None,
            "rag_context": None,
            "root_cause": None,
            "root_cause_explanation": None,
            "confidence_score": 0.0,
            "evidence_summary": [],
            "recommended_action": None,
            "target_version": None,
            "risk_level": "LOW",
            "requires_approval": False,
            "approval_status": "pending",
            "approval_comments": None,
            "remediation_status": "pending",
            "remediation_output": None,
            "verification_passed": False,
            "slack_delivered": False,
            "jira_ticket_key": None,
            "postmortem": None,
            "execution_steps": [],
            "agent_run_logs": [],
            "total_latency_ms": 0.0,
            "total_token_usage": 0
        }

    def test_triage_agent_classifies_p1(self):
        res = triage_agent.run(self.sample_state)
        self.assertEqual(res["severity"], "P1")
        self.assertEqual(res["urgency"], "CRITICAL")
        self.assertIn("search_logs", res["investigation_plan"])

    def test_logs_agent(self):
        res = logs_agent.run(self.sample_state)
        self.assertGreater(res["total_errors"], 0)
        self.assertIn("PostgreSQL", res["primary_error"])

    def test_metrics_agent(self):
        res = metrics_agent.run(self.sample_state)
        self.assertTrue(res["is_pool_exhausted"])
        self.assertGreaterEqual(res["p99_latency_ms"], 4000)

    def test_github_agent(self):
        res = code_deployment_agent.run(self.sample_state)
        self.assertEqual(res["latest_version"], "v2.4.1")
        self.assertIn("queries.py", res["files_modified"][0])

    def test_risk_agent_flags_high_risk_and_approval(self):
        state = dict(self.sample_state)
        state["github_result"] = code_deployment_agent.run(self.sample_state)
        res = risk_agent.run(state)
        self.assertEqual(res["risk_level"], "HIGH")
        self.assertTrue(res["requires_approval"])
        self.assertEqual(res["recommended_action"], "rollback_deployment")

    def test_communication_agent_generates_postmortem(self):
        state = dict(self.sample_state)
        state["root_cause"] = "Database connection pool exhaustion"
        res = communication_agent.run(state)
        self.assertTrue(res["slack_sent"])
        self.assertIsNotNone(res["jira_ticket_key"])
        self.assertIsNotNone(res["postmortem"])
        self.assertEqual(res["postmortem"]["severity"], "P1")

if __name__ == "__main__":
    unittest.main()
