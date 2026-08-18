"""
OpsPilot AI - GitHub & CI/CD Deployment Tool
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
from backend.tools.base import registry

@registry.register("get_deployment", "Retrieve recent deployment history and timestamps", risk_level="LOW")
def get_deployment(service: str) -> Dict[str, Any]:
    """
    Retrieves deployment events from ArgoCD / Kubernetes / GitHub Deployments.
    """
    now = datetime.utcnow()
    five_mins_ago = now - timedelta(minutes=5)
    two_days_ago = now - timedelta(days=2)

    if "payment" in service.lower():
        recent_deployments = [
            {
                "version": "v2.4.1",
                "deployed_at": five_mins_ago.strftime("%Y-%m-%d %H:%M:%S UTC"),
                "status": "deployed",
                "commit_sha": "a8f3b9c1d2e",
                "author": "john.doe@company.internal",
                "commit_title": "Optimize payment query and update transaction indexing",
                "is_suspect": True
            },
            {
                "version": "v2.4.0",
                "deployed_at": two_days_ago.strftime("%Y-%m-%d %H:%M:%S UTC"),
                "status": "healthy_previous_stable",
                "commit_sha": "7c12a4f09d8",
                "author": "sarah.smith@company.internal",
                "commit_title": "Release v2.4.0 with core checkout improvements",
                "is_suspect": False
            }
        ]
    else:
        recent_deployments = [
            {
                "version": "v1.8.0",
                "deployed_at": (now - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S UTC"),
                "status": "deployed",
                "commit_sha": "3b4c5d6e7f8",
                "author": "dev@company.internal",
                "commit_title": "Routine dependency update",
                "is_suspect": False
            }
        ]

    return {
        "service": service,
        "latest_version": recent_deployments[0]["version"],
        "previous_stable_version": recent_deployments[1]["version"] if len(recent_deployments) > 1 else None,
        "deployments": recent_deployments,
        "has_recent_deployment": True
    }

@registry.register("search_github", "Inspect GitHub commits, pull requests and code diffs", risk_level="LOW")
def search_github(service: str, commit_sha: str = "a8f3b9c1d2e") -> Dict[str, Any]:
    """
    Inspects GitHub PRs, commits, and file diffs for regressions.
    """
    if "payment" in service.lower() or "a8f3b9c1d2e" in commit_sha:
        diff_summary = (
            "diff --git a/services/payment/db/queries.py b/services/payment/db/queries.py\n"
            "--- a/services/payment/db/queries.py\n"
            "+++ b/services/payment/db/queries.py\n"
            "@@ -45,7 +45,7 @@ def get_user_transaction_history(user_id):\n"
            "-    # Indexed lookup by (user_id, status)\n"
            "-    return db.query(Transactions).filter_by(user_id=user_id, status='COMPLETED')\n"
            "+    # Custom query with full table join\n"
            "+    return db.query(Transactions).join(LedgerEntry).filter(Transactions.user_id == user_id).order_by(Transactions.created_at.desc())\n"
        )
        return {
            "commit_sha": commit_sha or "a8f3b9c1d2e",
            "author": "john.doe@company.internal",
            "message": "Optimize payment query and update transaction indexing",
            "pull_request": "PR #418 - Optimize payment history retrieval",
            "files_modified": [
                "services/payment/db/queries.py",
                "services/payment/handlers/checkout.py"
            ],
            "diff": diff_summary,
            "risk_signals": [
                "Modified database query in queries.py replaces indexed lookup with unindexed cross-table join",
                "Deployment occurred exactly 5 minutes before error rate spike"
            ]
        }

    return {
        "commit_sha": commit_sha,
        "author": "dev@company.internal",
        "message": "Routine patch",
        "files_modified": ["config.json"],
        "diff": "Small config update",
        "risk_signals": []
    }
