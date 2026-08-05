"""
OpsPilot AI - SQLAlchemy Entities
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

import uuid
from datetime import datetime
try:
    from sqlalchemy import (
        Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, JSON
    )
    from sqlalchemy.orm import relationship
except ImportError:
    def Column(*args, **kwargs): return None
    def String(*args, **kwargs): return None
    def Integer(*args, **kwargs): return None
    def Float(*args, **kwargs): return None
    def Boolean(*args, **kwargs): return None
    def DateTime(*args, **kwargs): return None
    def Text(*args, **kwargs): return None
    def ForeignKey(*args, **kwargs): return None
    def JSON(*args, **kwargs): return None
    def relationship(*args, **kwargs): return None

from backend.models.database import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), default="Nivesh Kumar Meena")
    role = Column(String(50), default="sre") # admin, sre, viewer, automation
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Service(Base):
    __tablename__ = "services"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), unique=True, index=True, nullable=False)
    namespace = Column(String(100), default="production")
    description = Column(Text, nullable=True)
    repo_url = Column(String(255), nullable=True)
    health_status = Column(String(50), default="healthy") # healthy, degraded, critical
    current_version = Column(String(50), default="v1.0.0")
    created_at = Column(DateTime, default=datetime.utcnow)

    deployments = relationship("Deployment", back_populates="service", cascade="all, delete-orphan")
    incidents = relationship("Incident", back_populates="service")

class Deployment(Base):
    __tablename__ = "deployments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    service_id = Column(String(36), ForeignKey("services.id"), nullable=False)
    version = Column(String(50), nullable=False)
    git_commit_sha = Column(String(40), nullable=True)
    git_commit_message = Column(Text, nullable=True)
    author = Column(String(100), default="DevOps Engineer")
    status = Column(String(50), default="successful") # successful, rolled_back, failed
    deployed_at = Column(DateTime, default=datetime.utcnow)

    service = relationship("Service", back_populates="deployments")

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    incident_number = Column(String(50), unique=True, index=True, nullable=False)
    service_id = Column(String(36), ForeignKey("services.id"), nullable=True)
    service_name = Column(String(100), index=True, nullable=False)
    severity = Column(String(10), default="P2") # P1, P2, P3, P4
    status = Column(String(50), default="investigating") # open, investigating, awaiting_approval, remediating, resolved, closed
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    environment = Column(String(50), default="production")
    error_rate = Column(Float, default=0.0)
    latency_ms = Column(Float, default=0.0)
    root_cause = Column(Text, nullable=True)
    confidence = Column(Float, default=0.0)
    investigation_summary = Column(Text, nullable=True)
    recommended_action = Column(String(255), nullable=True)
    risk_level = Column(String(20), default="LOW") # LOW, MEDIUM, HIGH, BLOCKED
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    service = relationship("Service", back_populates="incidents")
    agent_runs = relationship("AgentRun", back_populates="incident", cascade="all, delete-orphan")
    agent_decisions = relationship("AgentDecision", back_populates="incident", cascade="all, delete-orphan")
    tool_calls = relationship("ToolCall", back_populates="incident", cascade="all, delete-orphan")
    approvals = relationship("Approval", back_populates="incident", cascade="all, delete-orphan")
    actions = relationship("Action", back_populates="incident", cascade="all, delete-orphan")
    postmortem = relationship("Postmortem", back_populates="incident", uselist=False, cascade="all, delete-orphan")

class AgentRun(Base):
    __tablename__ = "agent_runs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    incident_id = Column(String(36), ForeignKey("incidents.id"), nullable=False)
    agent_name = Column(String(100), nullable=False)
    status = Column(String(50), default="completed") # running, completed, failed
    input_state = Column(JSON, nullable=True)
    output_state = Column(JSON, nullable=True)
    latency_ms = Column(Float, default=0.0)
    token_usage = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    incident = relationship("Incident", back_populates="agent_runs")

class AgentDecision(Base):
    __tablename__ = "agent_decisions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    incident_id = Column(String(36), ForeignKey("incidents.id"), nullable=False)
    agent_name = Column(String(100), nullable=False)
    decision_type = Column(String(100), nullable=False)
    rationale = Column(Text, nullable=True)
    confidence = Column(Float, default=1.0)
    evidence_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    incident = relationship("Incident", back_populates="agent_decisions")

class ToolCall(Base):
    __tablename__ = "tool_calls"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    incident_id = Column(String(36), ForeignKey("incidents.id"), nullable=False)
    agent_name = Column(String(100), nullable=False)
    tool_name = Column(String(100), nullable=False)
    parameters = Column(JSON, nullable=True)
    result = Column(JSON, nullable=True)
    status = Column(String(50), default="success") # success, error, timeout
    execution_time_ms = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    incident = relationship("Incident", back_populates="tool_calls")

class Approval(Base):
    __tablename__ = "approvals"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    incident_id = Column(String(36), ForeignKey("incidents.id"), nullable=False)
    action = Column(String(255), nullable=False)
    target_service = Column(String(100), nullable=False)
    target_version = Column(String(50), nullable=True)
    risk_level = Column(String(20), default="HIGH") # LOW, MEDIUM, HIGH, BLOCKED
    requested_by = Column(String(100), default="OpsPilot AI")
    approved_by = Column(String(100), nullable=True)
    status = Column(String(50), default="pending") # pending, approved, rejected, cancelled
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    approved_at = Column(DateTime, nullable=True)

    incident = relationship("Incident", back_populates="approvals")
    actions = relationship("Action", back_populates="approval")

class Action(Base):
    __tablename__ = "actions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    incident_id = Column(String(36), ForeignKey("incidents.id"), nullable=False)
    approval_id = Column(String(36), ForeignKey("approvals.id"), nullable=True)
    action_type = Column(String(100), nullable=False) # rollback, restart, scale, db_config
    command = Column(String(255), nullable=True)
    status = Column(String(50), default="pending") # pending, executing, succeeded, failed
    execution_output = Column(Text, nullable=True)
    executed_by = Column(String(100), default="n8n_automation")
    executed_at = Column(DateTime, default=datetime.utcnow)

    incident = relationship("Incident", back_populates="actions")
    approval = relationship("Approval", back_populates="actions")

class Postmortem(Base):
    __tablename__ = "postmortems"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    incident_id = Column(String(36), ForeignKey("incidents.id"), nullable=False)
    incident_number = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    summary = Column(Text, nullable=False)
    root_cause = Column(Text, nullable=False)
    timeline_json = Column(JSON, nullable=True)
    impact_summary = Column(Text, nullable=True)
    resolution = Column(Text, nullable=True)
    preventive_actions_json = Column(JSON, nullable=True)
    author = Column(String(100), default="OpsPilot AI - Nivesh Kumar Meena")
    created_at = Column(DateTime, default=datetime.utcnow)

    incident = relationship("Incident", back_populates="postmortem")

class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    incident_id = Column(String(36), ForeignKey("incidents.id"), nullable=True)
    test_case_name = Column(String(255), nullable=False)
    expected_root_cause = Column(Text, nullable=False)
    actual_root_cause = Column(Text, nullable=False)
    root_cause_matched = Column(Boolean, default=False)
    tool_selection_score = Column(Float, default=1.0)
    severity_matched = Column(Boolean, default=False)
    hallucination_detected = Column(Boolean, default=False)
    latency_ms = Column(Float, default=0.0)
    token_cost = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
