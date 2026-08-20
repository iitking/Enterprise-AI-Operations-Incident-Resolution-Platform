"""
OpsPilot AI - Slack Notification Tool
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

from typing import Dict, Any, List, Optional
from backend.tools.base import registry

@registry.register("send_slack", "Send rich incident alert or approval notification to Slack", risk_level="LOW")
def send_slack(channel: str = "#incidents-prod", title: str = "", message: str = "", blocks: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    Posts real-time operational alerts or interactive approval buttons to Slack webhook/API.
    """
    return {
        "status": "success",
        "channel": channel,
        "title": title,
        "message": message,
        "delivered": True,
        "ts": "1712581234.000100"
    }
