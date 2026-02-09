"""
Tool registry for MCP tools
"""

from typing import Dict, List, Callable, Any
from dataclasses import dataclass


@dataclass
class MCPTool:
    """MCP Tool definition"""

    name: str
    description: str
    parameters: Dict[str, Any]
    handler: Callable


class ToolRegistry:
    """Registry for MCP tools"""

    def __init__(self):
        self._tools: Dict[str, MCPTool] = {}

    def register(self, tool: MCPTool):
        """Register a tool"""
        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> MCPTool:
        """Get a tool by name"""
        return self._tools.get(name)

    def list_tools(self) -> List[MCPTool]:
        """List all registered tools"""
        return list(self._tools.values())

    def get_schemas(self) -> List[Dict]:
        """Get tool schemas for MCP protocol"""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters,
            }
            for tool in self._tools.values()
        ]


# Global registry instance
registry = ToolRegistry()
