"""
OpsPilot AI - Human-in-the-Loop (HITL) Approval Routes
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

from typing import List, Dict, Any
from backend.api.router_compat import APIRouter, HTTPException
from backend.models.schemas import ApprovalDecisionRequest
from backend.api.incident_routes import ACTIVE_INCIDENTS_STATE
from backend.graph.graph import incident_graph

router = APIRouter(prefix="/api/approvals", tags=["Human Approvals"])

@router.get("")
def list_pending_approvals():
    """Lists all actions pending human approval."""
    approvals = []
    for inc_id, state in ACTIVE_INCIDENTS_STATE.items():
        if state.get("requires_approval") and state.get("status") == "awaiting_approval":
            approvals.append({
                "incident_id": inc_id,
                "incident_number": state["incident_number"],
                "service_name": state["service_name"],
                "action": state.get("recommended_action"),
                "current_version": state.get("github_result", {}).get("latest_version"),
                "target_version": state.get("target_version"),
                "risk_level": state.get("risk_level", "HIGH"),
                "confidence_percent": int(state.get("confidence_score", 0.0) * 100),
                "reason": state.get("root_cause"),
                "created_at": state.get("created_at")
            })
    return approvals

@router.post("/{incident_id}/decision")
def submit_approval_decision(incident_id: str, payload: ApprovalDecisionRequest):
    """
    Submits human decision (approved/rejected).
    Resumes LangGraph execution to apply remediation and generate postmortem.
    """
    if incident_id not in ACTIVE_INCIDENTS_STATE:
        raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found")

    state = ACTIVE_INCIDENTS_STATE[incident_id]
    is_approved = payload.decision.lower() in ["approved", "approve", "yes"]

    # Resume graph execution
    updated_state = incident_graph.resume_after_approval(
        state=state,
        approved=is_approved,
        approved_by=payload.approved_by or "Nivesh Kumar Meena"
    )
    updated_state["approval_comments"] = payload.comments

    ACTIVE_INCIDENTS_STATE[incident_id] = updated_state

    return {
        "status": "success",
        "incident_id": incident_id,
        "decision": payload.decision,
        "approved_by": payload.approved_by or "Nivesh Kumar Meena",
        "incident_status": updated_state["status"],
        "remediation_output": updated_state.get("remediation_output"),
        "postmortem_generated": updated_state.get("postmortem") is not None
    }
