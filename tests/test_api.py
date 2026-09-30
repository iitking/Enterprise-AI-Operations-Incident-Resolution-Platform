"""
OpsPilot AI - API Route Handlers Tests
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

import sys
import os
import unittest

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.api.incident_routes import simulate_payment_api_incident, list_incidents, ACTIVE_INCIDENTS_STATE
from backend.api.approval_routes import list_pending_approvals, submit_approval_decision
from backend.models.schemas import ApprovalDecisionRequest
from backend.api.rag_routes import search_knowledge_base
from backend.models.schemas import RAGQueryRequest
from backend.api.analytics_routes import get_analytics_summary

class TestAPIRoutes(unittest.TestCase):

    def test_simulate_p1_incident_api(self):
        state = simulate_payment_api_incident()
        self.assertIsNotNone(state)
        self.assertEqual(state["status"], "awaiting_approval")
        self.assertEqual(state["risk_level"], "HIGH")

        # Test listing incidents
        incidents = list_incidents(status=None, severity=None, limit=10, db=None)
        self.assertGreater(len(incidents), 0)

    def test_approval_decision_workflow_api(self):
        state = simulate_payment_api_incident()
        inc_id = state["incident_id"]

        # Check pending approvals
        pending = list_pending_approvals()
        self.assertGreater(len(pending), 0)

        # Submit human approval
        req = ApprovalDecisionRequest(
            decision="approved",
            approved_by="Nivesh Kumar Meena",
            comments="Rollback authorized."
        )
        res = submit_approval_decision(incident_id=inc_id, payload=req)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["decision"], "approved")
        self.assertEqual(res["incident_status"], "resolved")

    def test_rag_knowledge_search_api(self):
        req = RAGQueryRequest(query="connection pool timeout postgresql", top_k=2)
        res = search_knowledge_base(payload=req)
        self.assertGreater(res["total"], 0)
        self.assertIn("Payment API", res["results"][0]["title"])

    def test_analytics_summary_api(self):
        summary = get_analytics_summary()
        self.assertIn("kpis", summary)
        self.assertIn("langsmith_benchmarks", summary)
        self.assertEqual(summary["system_status"]["author"], "Nivesh Kumar Meena")

if __name__ == "__main__":
    unittest.main()
