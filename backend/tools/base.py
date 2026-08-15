"""
OpsPilot AI - Base Tool Registry & Execution Harness
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

import time
from typing import Dict, Any, Callable
from backend.security.rbac import evaluate_action_policy
from backend.security.pii import redact_dict

class ToolRegistry:
    """Registry managing available operational tools and logging audit traces."""

    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._metadata: Dict[str, Dict[str, Any]] = {}

    def register(self, name: str, description: str, risk_level: str = "LOW"):
        def decorator(func: Callable):
            self._tools[name] = func
            self._metadata[name] = {
                "name": name,
                "description": description,
                "risk_level": risk_level,
                "callable": func
            }
            return func
        return decorator

    def execute(self, name: str, **kwargs) -> Dict[str, Any]:
        """Executes a registered tool within policy and audit guardrails."""
        if name not in self._tools:
            return {
                "tool": name,
                "status": "error",
                "error": f"Tool '{name}' is not registered.",
                "latency_ms": 0.0
            }

        policy = evaluate_action_policy(name)
        if policy["blocked"]:
            return {
                "tool": name,
                "status": "blocked",
                "error": f"Execution BLOCKED by security policy: {policy['reason']}",
                "policy": policy,
                "latency_ms": 0.0
            }

        start_time = time.time()
        try:
            raw_result = self._tools[name](**kwargs)
            duration_ms = round((time.time() - start_time) * 1000, 2)
            sanitized_result = redact_dict(raw_result)
            return {
                "tool": name,
                "status": "success",
                "parameters": kwargs,
                "result": sanitized_result,
                "policy": policy,
                "latency_ms": duration_ms
            }
        except Exception as e:
            duration_ms = round((time.time() - start_time) * 1000, 2)
            return {
                "tool": name,
                "status": "error",
                "error": str(e),
                "parameters": kwargs,
                "latency_ms": duration_ms
            }

    def list_tools(self) -> Dict[str, Any]:
        return {
            name: {
                "description": meta["description"],
                "risk_level": meta["risk_level"]
            }
            for name, meta in self._metadata.items()
        }

registry = ToolRegistry()
