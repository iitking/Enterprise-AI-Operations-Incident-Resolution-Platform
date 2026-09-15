"""
OpsPilot AI - Alert Ingestion Webhook Routes
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

from typing import Dict, Any
from backend.api.router_compat import APIRouter
from backend.models.schemas import AlertPayload, IncidentCreate
from backend.api.incident_routes import trigger_incident
from backend.api.approval_routes import submit_approval_decision
from backend.models.schemas import ApprovalDecisionRequest

router = APIRouter(prefix="/api/webhooks", tags=["Webhooks"])

@router.post("/alert")
def receive_prometheus_alert(payload: Dict[str, Any]):
    """
    Ingests alerts from Prometheus Alertmanager, Datadog or n8n automation.
    Normalizes payload and starts multi-agent investigation.
    """
    # Parse standard Prometheus or generic format
    service = "payment-api"
    error_rate = 18.4
    latency_ms = 4200.0
    title = "High Error Rate Detected"

    if "alerts" in payload and len(payload["alerts"]) > 0:
        first_alert = payload["alerts"][0]
        labels = first_alert.get("labels", {})
        annotations = first_alert.get("annotations", {})
        service = labels.get("service", labels.get("job", "payment-api"))
        title = annotations.get("summary", annotations.get("description", "Alertmanager Triggered Alert"))
        error_rate = float(labels.get("error_rate", 18.4))
        latency_ms = float(labels.get("latency_ms", 4200.0))
    elif "service" in payload:
        service = payload["service"]
        error_rate = float(payload.get("error_rate", 18.4))
        latency_ms = float(payload.get("latency_ms", 4200.0))
        title = payload.get("title", f"Telemetry alert on {service}")

    incident_req = IncidentCreate(
        service_name=service,
        title=title,
        severity="P1" if error_rate > 10.0 else "P2",
        environment="production",
        error_rate=error_rate,
        latency_ms=latency_ms
    )

    return trigger_incident(incident_req)

@router.post("/n8n/approval")
def receive_n8n_slack_approval(payload: Dict[str, Any]):
    """
    Webhook receiver for n8n Slack interactive button approvals.
    """
    incident_id = payload.get("incident_id")
    decision = payload.get("decision", "approved")
    approver = payload.get("approved_by", "Nivesh Kumar Meena")

    req = ApprovalDecisionRequest(
        decision=decision,
        approved_by=approver,
        comments="Approved via Slack interactive notification via n8n"
    )
    return submit_approval_decision(incident_id=incident_id, payload=req)
