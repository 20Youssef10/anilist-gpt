"""
MCP Server implementation for ChatGPT integration
"""

import json
import asyncio
from typing import Dict, Any
from datetime import datetime

from src.tools.registry import registry
from src.services.cache.redis_client import RedisClient


class MCPServer:
    """Model Context Protocol Server for AniList GPT"""

    def __init__(self):
        self.sessions: Dict[str, Dict] = {}
        self.redis = RedisClient()
        self.tool_registry = registry

    async def start(self):
        """Initialize MCP server"""
        print(f"[{datetime.now()}] MCP Server started")

    async def stop(self):
        """Cleanup MCP server"""
        print(f"[{datetime.now()}] MCP Server stopped")

    async def handle_request(self, session_id: str, request: Dict) -> Dict:
        """Handle incoming MCP request"""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")

        if method == "initialize":
            return await self._handle_initialize(session_id, params, request_id)
        elif method == "tools/list":
            return await self._handle_list_tools(request_id)
        elif method == "tools/call":
            return await self._handle_call_tool(params, request_id)
        elif method == "resources/list":
            return await self._handle_list_resources(request_id)
        else:
            return {
                "jsonrpc": "2.0",
                "error": {"code": -32601, "message": f"Method not found: {method}"},
                "id": request_id,
            }

    async def _handle_initialize(
        self, session_id: str, params: Dict, request_id: Any
    ) -> Dict:
        """Initialize MCP session"""
        self.sessions[session_id] = {
            "initialized_at": datetime.now().isoformat(),
            "client_info": params.get("clientInfo", {}),
        }

        return {
            "jsonrpc": "2.0",
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {"listChanged": True},
                    "resources": {"subscribe": True},
                },
                "serverInfo": {"name": "anilist-gpt-mcp", "version": "1.0.0"},
            },
            "id": request_id,
        }

    async def _handle_list_tools(self, request_id: Any) -> Dict:
        """List available tools"""
        tools = self.tool_registry.get_schemas()
        return {"jsonrpc": "2.0", "result": {"tools": tools}, "id": request_id}

    async def _handle_call_tool(self, params: Dict, request_id: Any) -> Dict:
        """Execute tool call"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        tool = self.tool_registry.get_tool(tool_name)
        if not tool:
            return {
                "jsonrpc": "2.0",
                "error": {"code": -32602, "message": f"Tool not found: {tool_name}"},
                "id": request_id,
            }

        try:
            result = await tool.handler(**arguments)
            return {
                "jsonrpc": "2.0",
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                },
                "id": request_id,
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "error": {"code": -32603, "message": f"Tool execution error: {str(e)}"},
                "id": request_id,
            }

    async def _handle_list_resources(self, request_id: Any) -> Dict:
        """List available resources"""
        return {
            "jsonrpc": "2.0",
            "result": {
                "resources": [
                    {
                        "uri": "anilist://trending",
                        "name": "Trending Anime",
                        "mimeType": "application/json",
                    }
                ]
            },
            "id": request_id,
        }
