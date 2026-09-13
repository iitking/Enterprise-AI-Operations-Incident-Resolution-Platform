"""
OpsPilot AI - Incident Management & AI Investigation Routes
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from backend.api.router_compat import APIRouter, Depends, HTTPException, Query
try:
    from sqlalchemy.orm import Session
except ImportError:
    Session = None

from backend.models.database import get_db
from backend.models.entities import Incident, Approval, Postmortem
from backend.models.schemas import IncidentCreate, AlertPayload
from backend.graph.graph import incident_graph
from backend.graph.state import OpsPilotState

router = APIRouter(prefix="/api/incidents", tags=["Incidents"])

# In-memory fast cache for active incident investigation states
ACTIVE_INCIDENTS_STATE: Dict[str, OpsPilotState] = {}

@router.get("")
def list_incidents(
    status: Optional[str] = None,
    severity: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """List recorded incidents with optional status or severity filters."""
    # Combine active state and database records
    items = []
    for inc_id, state in ACTIVE_INCIDENTS_STATE.items():
        if status and state.get("status") != status:
            continue
        if severity and state.get("triage_result", {}).get("severity") != severity:
            continue
        items.append({
            "id": state["incident_id"],
            "incident_number": state["incident_number"],
            "service_name": state["service_name"],
            "title": state["title"],
            "severity": state.get("triage_result", {}).get("severity", "P2"),
            "status": state.get("status", "investigating"),
            "error_rate": state.get("error_rate", 0.0),
            "latency_ms": state.get("latency_ms", 0.0),
            "root_cause": state.get("root_cause"),
            "confidence": state.get("confidence_score", 0.0),
            "recommended_action": state.get("recommended_action"),
            "risk_level": state.get("risk_level", "LOW"),
            "created_at": state.get("created_at")
        })

    return sorted(items, key=lambda x: x["created_at"], reverse=True)

@router.get("/{incident_id}")
def get_incident_detail(incident_id: str):
    """Retrieve complete multi-agent investigation transcript and state for an incident."""
    if incident_id not in ACTIVE_INCIDENTS_STATE:
        raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found")
    return ACTIVE_INCIDENTS_STATE[incident_id]

@router.post("/trigger")
def trigger_incident(payload: IncidentCreate):
    """Triggers autonomous multi-agent incident investigation."""
    inc_id = str(uuid.uuid4())
    inc_num = f"INC-{len(ACTIVE_INCIDENTS_STATE) + 1042}"

    initial_state: OpsPilotState = {
        "incident_id": inc_id,
        "incident_number": inc_num,
        "service_name": payload.service_name,
        "title": payload.title,
        "environment": payload.environment,
        "created_at": datetime.utcnow().isoformat(),
        "error_rate": payload.error_rate,
        "latency_ms": payload.latency_ms,
        "raw_alert": payload.dict(),
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

    final_state = incident_graph.run_investigation(initial_state)
    ACTIVE_INCIDENTS_STATE[inc_id] = final_state
    return final_state

@router.post("/simulate-p1")
def simulate_payment_api_incident():
    """
    1-Click simulation of the benchmark P1 production incident:
    'Payment API Failure due to database query regression and connection pool exhaustion'
    """
    payload = IncidentCreate(
        service_name="payment-api",
        title="Payment API Latency Degradation & Elevated 500 Error Rate",
        description="Prometheus fired HighErrorRateAlert: 18.4% payment transactions failing",
        severity="P1",
        environment="production",
        error_rate=18.4,
        latency_ms=4200.0
    )
    return trigger_incident(payload)
