"""MCP server exposing explicitly registered Kubernetes capabilities."""

import json

from mcp.server import MCPServer
from starlette.responses import JSONResponse

from kube_observer_mcp.prompts import register_prompts
from kube_observer_mcp.tools.registry import DEFAULT_TOOL_GROUPS, register_tool_groups


def create_server(tool_groups: tuple[str, ...] = DEFAULT_TOOL_GROUPS) -> MCPServer:
    """Create a server with explicitly registered tool groups and prompt templates."""
    server = MCPServer("kube-observer-mcp")
    register_tool_groups(server, tool_groups)
    register_prompts(server)

    @server.custom_route("/health", methods=["GET"], include_in_schema=False)
    async def health(_request: object) -> JSONResponse:
        """Provide a lightweight liveness/readiness response."""
        return JSONResponse({"status": "ok"})

    @server.resource("kube-observer://capabilities")
    def capabilities() -> str:
        """Describe built-in tool groups and the server's default safety posture."""
        return json.dumps(
            {
                "tool_groups": {
                    "read_only": ["list_nodes", "list_pods"],
                    "write": [],
                },
                "default_group": "read_only",
                "write_tools_enabled": False,
                "authorization_boundary": "Kubernetes RBAC",
            },
            sort_keys=True,
        )

    return server


def main() -> None:
    """Run the server with Streamable HTTP for Kubernetes/Kagent deployment."""
    create_server().run(transport="streamable-http", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
