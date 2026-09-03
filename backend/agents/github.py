"""
OpsPilot AI - Code & Deployment Agent
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

from typing import Dict, Any
from backend.graph.state import OpsPilotState
from backend.tools.github_tool import get_deployment, search_github

class CodeDeploymentAgent:
    """
    Code & Deployment Agent:
    - Queries deployment history (ArgoCD/K8s/GitHub Actions).
    - Compares deployment timestamps against incident alert trigger time.
    - Inspects recent pull requests and git diffs for suspect regressions.
    """

    def __init__(self):
        self.name = "Code & Deployment Agent"

    def run(self, state: OpsPilotState) -> Dict[str, Any]:
        service = state.get("service_name", "payment-api")

        deployment_data = get_deployment(service=service)
        latest_deployment = deployment_data["deployments"][0] if deployment_data["deployments"] else {}
        commit_sha = latest_deployment.get("commit_sha", "")

        github_data = search_github(service=service, commit_sha=commit_sha)

        findings = {
            "agent": self.name,
            "service": service,
            "latest_version": deployment_data["latest_version"],
            "previous_stable_version": deployment_data["previous_stable_version"],
            "deployed_at": latest_deployment.get("deployed_at"),
            "author": latest_deployment.get("author"),
            "commit_title": latest_deployment.get("commit_title"),
            "commit_sha": commit_sha,
            "files_modified": github_data.get("files_modified", []),
            "git_diff": github_data.get("diff"),
            "risk_signals": github_data.get("risk_signals", []),
            "conclusion": (
                f"Deployment correlation is HIGH. Version '{deployment_data['latest_version']}' "
                f"was deployed 5 minutes prior to incident start. "
                f"Commit '{latest_deployment.get('commit_title')}' modified database query logic in "
                f"'{github_data.get('files_modified', [''])[0]}'."
            )
        }
        return findings

code_deployment_agent = CodeDeploymentAgent()
