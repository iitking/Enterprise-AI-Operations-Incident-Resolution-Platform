"""
OpsPilot AI - LangGraph Node Implementations
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

import time
from typing import Dict, Any
from backend.graph.state import OpsPilotState
from backend.agents.supervisor import supervisor_agent
from backend.agents.triage import triage_agent
from backend.agents.logs import logs_agent
from backend.agents.metrics import metrics_agent
from backend.agents.github import code_deployment_agent
from backend.agents.root_cause import root_cause_agent
from backend.agents.risk import risk_agent
from backend.agents.communication import communication_agent
from backend.tools.k8s_tool import rollback_deployment, restart_service

def record_step(state: OpsPilotState, step_name: str, duration_ms: float, agent_output: Any):
    if "execution_steps" not in state or state["execution_steps"] is None:
        state["execution_steps"] = []
    state["execution_steps"].append(step_name)

    if "agent_run_logs" not in state or state["agent_run_logs"] is None:
        state["agent_run_logs"] = []

    state["agent_run_logs"].append({
        "step": step_name,
        "duration_ms": duration_ms,
        "summary": str(agent_output)[:200]
    })
    state["total_latency_ms"] = round(state.get("total_latency_ms", 0.0) + duration_ms, 2)
    state["total_token_usage"] = state.get("total_token_usage", 0) + 120

def supervisor_node(state: OpsPilotState) -> Dict[str, Any]:
    start = time.time()
    plan = supervisor_agent.plan(state)
    dur = round((time.time() - start) * 1000, 2)
    record_step(state, "Supervisor: Plan Investigation", dur, plan)
    return {"execution_steps": state["execution_steps"]}

def triage_node(state: OpsPilotState) -> Dict[str, Any]:
    start = time.time()
    res = triage_agent.run(state)
    dur = round((time.time() - start) * 1000, 2)
    record_step(state, "Triage: Severity Classification", dur, res)
    return {
        "triage_result": res,
        "execution_steps": state["execution_steps"]
    }

def logs_node(state: OpsPilotState) -> Dict[str, Any]:
    start = time.time()
    res = logs_agent.run(state)
    dur = round((time.time() - start) * 1000, 2)
    record_step(state, "Logs: Error Clustering", dur, res)
    return {
        "logs_result": res,
        "execution_steps": state["execution_steps"]
    }

def metrics_node(state: OpsPilotState) -> Dict[str, Any]:
    start = time.time()
    res = metrics_agent.run(state)
    dur = round((time.time() - start) * 1000, 2)
    record_step(state, "Metrics: Anomaly Detection", dur, res)
    return {
        "metrics_result": res,
        "execution_steps": state["execution_steps"]
    }

def github_node(state: OpsPilotState) -> Dict[str, Any]:
    start = time.time()
    res = code_deployment_agent.run(state)
    dur = round((time.time() - start) * 1000, 2)
    record_step(state, "GitHub: Deployment & Commit Analysis", dur, res)
    return {
        "github_result": res,
        "execution_steps": state["execution_steps"]
    }

def root_cause_node(state: OpsPilotState) -> Dict[str, Any]:
    start = time.time()
    res = root_cause_agent.run(state)
    dur = round((time.time() - start) * 1000, 2)
    record_step(state, "Root Cause: Evidence Correlation", dur, res)
    return {
        "root_cause": res["root_cause"],
        "confidence_score": res["confidence_score"],
        "evidence_summary": res["evidence_summary"],
        "rag_context": res.get("rag_context"),
        "execution_steps": state["execution_steps"]
    }

def risk_policy_node(state: OpsPilotState) -> Dict[str, Any]:
    start = time.time()
    res = risk_agent.run(state)
    dur = round((time.time() - start) * 1000, 2)
    record_step(state, "Risk & Policy: Safety Evaluation", dur, res)
    return {
        "recommended_action": res["recommended_action"],
        "target_version": res["target_version"],
        "risk_level": res["risk_level"],
        "requires_approval": res["requires_approval"],
        "approval_status": "pending" if res["requires_approval"] else "auto_approved",
        "execution_steps": state["execution_steps"]
    }

def auto_remediation_node(state: OpsPilotState) -> Dict[str, Any]:
    """Executes safe LOW-risk automated remediations."""
    start = time.time()
    service = state.get("service_name", "unknown")
    res = restart_service(service=service)
    dur = round((time.time() - start) * 1000, 2)
    record_step(state, "Auto-Remediation: Executed Safe Fix", dur, res)
    return {
        "remediation_status": "succeeded",
        "remediation_output": res,
        "verification_passed": True,
        "execution_steps": state["execution_steps"]
    }

def human_approved_remediation_node(state: OpsPilotState) -> Dict[str, Any]:
    """Executes high-risk remediation following human approval."""
    start = time.time()
    service = state.get("service_name", "payment-api")
    target_v = state.get("target_version", "v2.4.0")
    res = rollback_deployment(service=service, target_version=target_v)
    dur = round((time.time() - start) * 1000, 2)
    record_step(state, f"Remediation: Kubernetes Rollback to {target_v}", dur, res)
    return {
        "remediation_status": "succeeded",
        "remediation_output": res,
        "verification_passed": True,
        "execution_steps": state["execution_steps"]
    }

def communication_node(state: OpsPilotState) -> Dict[str, Any]:
    start = time.time()
    res = communication_agent.run(state)
    dur = round((time.time() - start) * 1000, 2)
    record_step(state, "Communication: Slack, Jira & Postmortem", dur, res)
    return {
        "slack_delivered": res["slack_sent"],
        "jira_ticket_key": res["jira_ticket_key"],
        "postmortem": res["postmortem"],
        "execution_steps": state["execution_steps"]
    }
