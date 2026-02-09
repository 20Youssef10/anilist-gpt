"""
Integration tests for MCP server
"""

import pytest
from unittest.mock import Mock

from src.mcp.server import MCPServer


class TestMCPServerIntegration:
    @pytest.fixture
    def mcp_server(self):
        return MCPServer()

    @pytest.mark.asyncio
    async def test_initialize_session(self, mcp_server):
        """Test MCP session initialization"""
        request = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {"clientInfo": {"name": "test-client", "version": "1.0"}},
            "id": 1,
        }

        result = await mcp_server.handle_request("session-123", request)

        assert "result" in result
        assert result["result"]["protocolVersion"] == "2024-11-05"
        assert "session-123" in mcp_server.sessions

    @pytest.mark.asyncio
    async def test_list_tools(self, mcp_server):
        """Test tools/list method"""
        request = {"jsonrpc": "2.0", "method": "tools/list", "id": 1}

        result = await mcp_server.handle_request("session-123", request)

        assert "result" in result
        assert "tools" in result["result"]
