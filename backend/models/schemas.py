"""
OpsPilot AI - Pydantic Schemas
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
try:
    from pydantic import BaseModel, Field
except ImportError:
    class BaseModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def dict(self):
            return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
    def Field(default=None, **kwargs):
        return default

# User & Auth
class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = "Nivesh Kumar Meena"
    role: str = "sre"

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    full_name: str

# Services & Deployments
class ServiceCreate(BaseModel):
    name: str
    namespace: str = "production"
    description: Optional[str] = None
    repo_url: Optional[str] = None
    current_version: str = "v1.0.0"

class DeploymentCreate(BaseModel):
    service_name: str
    version: str
    git_commit_sha: Optional[str] = None
    git_commit_message: Optional[str] = None
    author: Optional[str] = "DevOps Engineer"

# Incidents & Alerts
class AlertPayload(BaseModel):
    service: str
    environment: str = "production"
    error_rate: float = Field(default=0.0, description="Error percentage rate e.g. 18.5")
    latency_ms: float = Field(default=0.0, description="Response latency in milliseconds")
    alert_name: Optional[str] = "HighErrorRateAlert"
    message: Optional[str] = "Service degraded performance detected"
    metrics: Optional[Dict[str, Any]] = None

class IncidentCreate(BaseModel):
    service_name: str
    title: str
    description: Optional[str] = None
    severity: str = "P2"
    environment: str = "production"
    error_rate: float = 0.0
    latency_ms: float = 0.0

class IncidentResponse(BaseModel):
    id: str
    incident_number: str
    service_name: str
    severity: str
    status: str
    title: str
    description: Optional[str]
    environment: str
    error_rate: float
    latency_ms: float
    root_cause: Optional[str]
    confidence: float
    investigation_summary: Optional[str]
    recommended_action: Optional[str]
    risk_level: str
    created_at: datetime
    resolved_at: Optional[datetime]

    class Config:
        from_attributes = True

# Agent State & Runs
class AgentRunResponse(BaseModel):
    id: str
    incident_id: str
    agent_name: str
    status: str
    latency_ms: float
    token_usage: int
    created_at: datetime

    class Config:
        from_attributes = True

class AgentDecisionResponse(BaseModel):
    id: str
    incident_id: str
    agent_name: str
    decision_type: str
    rationale: Optional[str]
    confidence: float
    evidence_json: Optional[Dict[str, Any]]
    created_at: datetime

    class Config:
        from_attributes = True

class ToolCallResponse(BaseModel):
    id: str
    incident_id: str
    agent_name: str
    tool_name: str
    parameters: Optional[Dict[str, Any]]
    result: Optional[Any]
    status: str
    execution_time_ms: float
    created_at: datetime

    class Config:
        from_attributes = True

# Approvals & Actions
class ApprovalDecisionRequest(BaseModel):
    decision: str = Field(..., description="'approved' or 'rejected'")
    approved_by: Optional[str] = "Nivesh Kumar Meena"
    comments: Optional[str] = None

class ApprovalResponse(BaseModel):
    id: str
    incident_id: str
    action: str
    target_service: str
    target_version: Optional[str]
    risk_level: str
    requested_by: str
    approved_by: Optional[str]
    status: str
    comments: Optional[str]
    created_at: datetime
    approved_at: Optional[datetime]

    class Config:
        from_attributes = True

class ActionResponse(BaseModel):
    id: str
    incident_id: str
    action_type: str
    command: Optional[str]
    status: str
    execution_output: Optional[str]
    executed_by: str
    executed_at: datetime

    class Config:
        from_attributes = True

# Postmortem
class PostmortemResponse(BaseModel):
    id: str
    incident_id: str
    incident_number: str
    title: str
    summary: str
    root_cause: str
    timeline_json: Optional[List[Dict[str, Any]]]
    impact_summary: Optional[str]
    resolution: Optional[str]
    preventive_actions_json: Optional[List[str]]
    author: str
    created_at: datetime

    class Config:
        from_attributes = True

# RAG
class RAGQueryRequest(BaseModel):
    query: str
    top_k: int = 4
    category: Optional[str] = None # runbook, postmortem, architecture

class RAGDocumentResponse(BaseModel):
    id: str
    title: str
    category: str
    content: str
    score: float
    metadata: Optional[Dict[str, Any]] = None

# Benchmarks
class EvaluationResponse(BaseModel):
    id: str
    test_case_name: str
    expected_root_cause: str
    actual_root_cause: str
    root_cause_matched: bool
    tool_selection_score: float
    severity_matched: bool
    latency_ms: float
    token_cost: float

    class Config:
        from_attributes = True

class BenchmarkSummaryResponse(BaseModel):
    total_incidents: int
    root_cause_accuracy: float
    tool_selection_accuracy: float
    severity_accuracy: float
    avg_latency_ms: float
    avg_tokens_per_incident: float
