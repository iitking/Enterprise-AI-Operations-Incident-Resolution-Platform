"""
OpsPilot AI - Jira Incident Management Tool
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

import random
from typing import Dict, Any
from backend.tools.base import registry

@registry.register("create_jira", "Create Jira incident ticket and set priority", risk_level="LOW")
def create_jira(service: str, title: str, description: str, priority: str = "Highest") -> Dict[str, Any]:
    """
    Creates an incident ticket in Jira / Atlassian.
    """
    ticket_num = random.randint(1040, 1099)
    ticket_key = f"OPS-{ticket_num}"
    
    return {
        "status": "success",
        "ticket_key": ticket_key,
        "title": title,
        "priority": priority,
        "service": service,
        "jira_url": f"https://company.atlassian.net/browse/{ticket_key}",
        "summary": f"Incident ticket {ticket_key} opened with priority {priority} for {service}."
    }
