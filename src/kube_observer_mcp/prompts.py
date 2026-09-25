"""Reusable, non-executable MCP prompt templates (workflow guidance)."""

from mcp.server import MCPServer


def register_prompts(server: MCPServer) -> None:
    """Register workflow prompts separately from executable tools."""

    @server.prompt()
    def cluster_health_check(namespace: str = "kagent") -> str:
        """Guide a read-only health check for nodes and one namespace."""
        return (
            "Perform a read-only Kubernetes health check. First call list_nodes "
            "and report each node name and Ready condition. Then call list_pods "
            f"with namespace={namespace!r} and group pods by Running, Pending, "
            "Failed, or other phase. Include only pod name, Ready containers, "
            "phase, and restart count. Do not infer data that the tools did not "
            "return, and do not attempt to change cluster resources."
        )

    @server.prompt()
    def summarize_namespace(namespace: str) -> str:
        """Request a concise, read-only summary for exactly one namespace."""
        if not namespace.strip():
            raise ValueError("namespace must not be empty")
        return (
            f"Call list_pods with namespace={namespace.strip()!r}. Group the returned "
            "pods by phase and report each pod name, ready containers, and restart "
            "count. Do not discuss images or full specifications unless asked. "
            "Do not change cluster resources."
        )
