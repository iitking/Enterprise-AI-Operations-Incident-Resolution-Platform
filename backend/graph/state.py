"""
OpsPilot AI - LangGraph State Definition
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

from typing import TypedDict, List, Dict, Any, Optional
from datetime import datetime

class OpsPilotState(TypedDict):
    """
    State schema for OpsPilot AI multi-agent orchestration workflow.
    Preserves incident context, parallel investigation findings, evidence correlation,
    human approval gates, and remediation results.
    """
    # Incident Identifiers & Metadata
    incident_id: str
    incident_number: str
    service_name: str
    title: str
    environment: str
    created_at: str

    # Alert Data
    error_rate: float
    latency_ms: float
    raw_alert: Dict[str, Any]

    # Agent Findings
    triage_result: Optional[Dict[str, Any]] # severity, investigation_plan
    logs_result: Optional[Dict[str, Any]]   # log errors, breakdown, traces
    metrics_result: Optional[Dict[str, Any]] # anomalies, pool usage, CPU
    github_result: Optional[Dict[str, Any]]  # recent deployment, commit diff
    rag_context: Optional[Dict[str, Any]]    # runbooks, past incident postmortems

    # Root Cause & Decision
    root_cause: Optional[str]
    root_cause_explanation: Optional[str]
    confidence_score: float # e.g. 0.94 (94%)
    evidence_summary: List[str]

    # Risk & Remediation Policy
    recommended_action: Optional[str]
    target_version: Optional[str]
    risk_level: str # LOW, MEDIUM, HIGH, BLOCKED
    requires_approval: bool
    approval_status: str # pending, approved, rejected, auto_approved
    approval_comments: Optional[str]

    # Execution & Verification
    remediation_status: str # pending, executing, succeeded, failed
    remediation_output: Optional[Dict[str, Any]]
    verification_passed: bool

    # Communications & Reporting
    slack_delivered: bool
    jira_ticket_key: Optional[str]
    postmortem: Optional[Dict[str, Any]]

    # Observability & Tracing
    execution_steps: List[str]
    agent_run_logs: List[Dict[str, Any]]
    total_latency_ms: float
    total_token_usage: int
