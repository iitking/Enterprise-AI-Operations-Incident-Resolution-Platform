"""
OpsPilot AI - LangGraph Orchestrator Tests
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

import sys
import os
import unittest

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.graph.graph import incident_graph
from backend.graph.state import OpsPilotState

class TestLangGraphOrchestrator(unittest.TestCase):

    def setUp(self):
        self.initial_state: OpsPilotState = {
            "incident_id": "test-graph-001",
            "incident_number": "INC-TEST-001",
            "service_name": "payment-api",
            "title": "Payment API Outage",
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

    def test_investigation_pauses_for_human_approval(self):
        state = incident_graph.run_investigation(self.initial_state)

        # High-risk action on payment-api should pause at awaiting_approval
        self.assertEqual(state["status"], "awaiting_approval")
        self.assertTrue(state["requires_approval"])
        self.assertEqual(state["risk_level"], "HIGH")
        self.assertEqual(state["recommended_action"], "rollback_deployment")
        self.assertGreaterEqual(state["confidence_score"], 0.90)
        self.assertIn("Root Cause: Evidence Correlation", state["execution_steps"])

    def test_resume_after_approval_executes_rollback_and_resolves(self):
        state = incident_graph.run_investigation(self.initial_state)
        self.assertEqual(state["status"], "awaiting_approval")

        # Simulate human approval submitted by Nivesh Kumar Meena
        resolved_state = incident_graph.resume_after_approval(
            state=state,
            approved=True,
            approved_by="Nivesh Kumar Meena"
        )

        self.assertEqual(resolved_state["status"], "resolved")
        self.assertEqual(resolved_state["approval_status"], "approved")
        self.assertEqual(resolved_state["remediation_status"], "succeeded")
        self.assertTrue(resolved_state["verification_passed"])
        self.assertIsNotNone(resolved_state["postmortem"])
        self.assertTrue(resolved_state["slack_delivered"])

if __name__ == "__main__":
    unittest.main()
