"""
OpsPilot AI - Model Context Protocol (MCP) Server
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

from typing import Dict, Any, List
from backend.tools.base import registry

class MCPServer:
    """
    Standard Model Context Protocol (MCP) interface implementation for OpsPilot AI.
    Exposes SRE operational tools through JSON-RPC compatible protocols.
    """

    def __init__(self):
        self.server_info = {
            "name": "opspilot-ai-mcp",
            "version": "1.0.0",
            "author": "Nivesh Kumar Meena",
            "capabilities": {
                "tools": True,
                "resources": True,
                "prompts": True
            }
        }

    def list_tools(self) -> List[Dict[str, Any]]:
        """Returns standard MCP tool descriptors."""
        tools = []
        for name, meta in registry.list_tools().items():
            tools.append({
                "name": name,
                "description": meta["description"],
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "service": {"type": "string", "description": "Target microservice name"}
                    }
                },
                "riskLevel": meta["risk_level"]
            })
        return tools

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Executes tool through registry with audit logging."""
        result = registry.execute(name, **arguments)
        return {
            "content": [
                {
                    "type": "text",
                    "text": str(result)
                }
            ],
            "isError": result.get("status") == "error"
        }

mcp_server = MCPServer()
