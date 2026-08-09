"""
OpsPilot AI - Role-Based Access Control (RBAC) & Tool Policy Engine
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

from enum import Enum
from typing import Dict, Any

try:
    from fastapi import HTTPException, status
except ImportError:
    class HTTPException(Exception):
        def __init__(self, status_code=400, detail=""):
            self.status_code = status_code
            self.detail = detail
            super().__init__(detail)
    class status:
        HTTP_403_FORBIDDEN = 403
        HTTP_401_UNAUTHORIZED = 401

class ActionRiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    BLOCKED = "BLOCKED"

# Risk classification for all enterprise actions
TOOL_RISK_MAP: Dict[str, ActionRiskLevel] = {
    # Low Risk (Read-only / Safe notifications)
    "search_logs": ActionRiskLevel.LOW,
    "get_metrics": ActionRiskLevel.LOW,
    "search_github": ActionRiskLevel.LOW,
    "get_deployment": ActionRiskLevel.LOW,
    "query_rag": ActionRiskLevel.LOW,
    "create_jira": ActionRiskLevel.LOW,
    "send_slack": ActionRiskLevel.LOW,
    "generate_postmortem": ActionRiskLevel.LOW,
    
    # Medium Risk (Service restarts, scaling)
    "restart_service": ActionRiskLevel.MEDIUM,
    "scale_replicas": ActionRiskLevel.MEDIUM,
    "clear_redis_cache": ActionRiskLevel.MEDIUM,

    # High Risk (Production modifications, rollbacks)
    "rollback_deployment": ActionRiskLevel.HIGH,
    "apply_k8s_patch": ActionRiskLevel.HIGH,
    "modify_db_connection_pool": ActionRiskLevel.HIGH,

    # Blocked (Destructive operations - Never permitted)
    "delete_database": ActionRiskLevel.BLOCKED,
    "drop_table": ActionRiskLevel.BLOCKED,
    "truncate_table": ActionRiskLevel.BLOCKED,
    "delete_namespace": ActionRiskLevel.BLOCKED,
    "disable_firewall": ActionRiskLevel.BLOCKED,
}

class UserRole(str, Enum):
    ADMIN = "admin"
    SRE = "sre"
    VIEWER = "viewer"
    AUTOMATION = "automation"

def evaluate_action_policy(action_name: str, user_role: str = "sre") -> Dict[str, Any]:
    """
    Evaluates whether an action can be auto-executed or requires human approval.
    """
    risk = TOOL_RISK_MAP.get(action_name, ActionRiskLevel.HIGH)

    if risk == ActionRiskLevel.BLOCKED:
        return {
            "action": action_name,
            "risk_level": ActionRiskLevel.BLOCKED.value,
            "can_auto_execute": False,
            "requires_approval": False,
            "blocked": True,
            "reason": "Destructive production actions are strictly forbidden by security policy."
        }

    if risk == ActionRiskLevel.LOW:
        return {
            "action": action_name,
            "risk_level": ActionRiskLevel.LOW.value,
            "can_auto_execute": True,
            "requires_approval": False,
            "blocked": False,
            "reason": "Low-risk diagnostic or notification action; safe for autonomous execution."
        }

    if risk == ActionRiskLevel.MEDIUM:
        can_auto = user_role in [UserRole.ADMIN.value, UserRole.AUTOMATION.value]
        return {
            "action": action_name,
            "risk_level": ActionRiskLevel.MEDIUM.value,
            "can_auto_execute": can_auto,
            "requires_approval": not can_auto,
            "blocked": False,
            "reason": "Medium-risk action; impacts service availability temporarily."
        }

    # HIGH RISK
    return {
        "action": action_name,
        "risk_level": ActionRiskLevel.HIGH.value,
        "can_auto_execute": False,
        "requires_approval": True,
        "blocked": False,
        "reason": "High-risk production action; requires verified human approval before execution."
    }

def require_role(allowed_roles: list):
    def role_checker(current_user: dict):
        role = current_user.get("role", "viewer")
        if role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation requires one of roles: {allowed_roles}. Current role: {role}"
            )
        return current_user
    return role_checker
