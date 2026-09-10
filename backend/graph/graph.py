"""
OpsPilot AI - LangGraph Multi-Agent Orchestrator
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

from typing import Dict, Any
from backend.graph.state import OpsPilotState
from backend.graph.nodes import (
    supervisor_node,
    triage_node,
    logs_node,
    metrics_node,
    github_node,
    root_cause_node,
    risk_policy_node,
    auto_remediation_node,
    human_approved_remediation_node,
    communication_node
)

class OpsPilotGraph:
    """
    Stateful multi-agent incident orchestration graph.
    Implements conditional routing, parallel evidence collection,
    Human-in-the-Loop approval breakpoints, and automated remediation.
    """

    def __init__(self):
        self.name = "OpsPilot AI Multi-Agent Incident Orchestrator"
        self.author = "Nivesh Kumar Meena"

    def run_investigation(self, initial_state: OpsPilotState) -> OpsPilotState:
        """
        Executes the investigation phase up to the Risk & Policy decision gate.
        If high-risk remediation is required, it yields state awaiting human approval.
        """
        state = dict(initial_state)
        state.setdefault("execution_steps", [])
        state.setdefault("agent_run_logs", [])
        state.setdefault("total_latency_ms", 0.0)
        state.setdefault("total_token_usage", 0)

        # 1. Supervisor Initial Planning
        supervisor_node(state)

        # 2. Triage Node (Severity & Plan)
        triage_res = triage_node(state)
        state.update(triage_res)

        # 3. Parallel Evidence Collection (Logs, Metrics, GitHub)
        logs_res = logs_node(state)
        state.update(logs_res)

        metrics_res = metrics_node(state)
        state.update(metrics_res)

        github_res = github_node(state)
        state.update(github_res)

        # 4. Root Cause Synthesis (Correlating Evidence + RAG Runbooks)
        root_cause_res = root_cause_node(state)
        state.update(root_cause_res)

        # 5. Risk & Policy Evaluation
        risk_res = risk_policy_node(state)
        state.update(risk_res)

        # 6. Branch Decision: Auto-fix vs Human Approval Breakpoint
        if not state.get("requires_approval", False):
            # Safe low-risk action can execute automatically
            remed_res = auto_remediation_node(state)
            state.update(remed_res)

            comm_res = communication_node(state)
            state.update(comm_res)
            state["status"] = "resolved"
        else:
            # High-risk action: Interrupt and await Human-in-the-Loop approval
            state["status"] = "awaiting_approval"

        return state

    def resume_after_approval(self, state: OpsPilotState, approved: bool, approved_by: str = "Nivesh Kumar Meena") -> OpsPilotState:
        """
        Resumes LangGraph execution once the Human Approval gate is resolved.
        """
        state = dict(state)
        if approved:
            state["approval_status"] = "approved"
            remed_res = human_approved_remediation_node(state)
            state.update(remed_res)

            comm_res = communication_node(state)
            state.update(comm_res)
            state["status"] = "resolved"
        else:
            state["approval_status"] = "rejected"
            state["status"] = "approval_rejected"
            comm_res = communication_node(state)
            state.update(comm_res)

        return state

incident_graph = OpsPilotGraph()
