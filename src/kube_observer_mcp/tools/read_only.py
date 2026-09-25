"""Read-only Kubernetes inventory tools."""

from mcp.server import MCPServer

from kube_observer_mcp.inventory import summarize_nodes, summarize_pods
from kube_observer_mcp.kubernetes_api import fetch_nodes, fetch_pods


def register_read_only_tools(server: MCPServer) -> None:
    """Register narrow inventory tools; this module performs no mutations."""

    @server.tool()
    def list_nodes() -> list[dict[str, str]]:
        """List each node's name and Ready condition, plus OS and Kubernetes version.

        Does not return full Node specifications, addresses, image inventories,
        machine IDs, or other unrelated node details.
        """
        return summarize_nodes(fetch_nodes())

    @server.tool()
    def list_pods(namespace: str) -> list[dict[str, object]]:
        """List concise pod status summaries for exactly one namespace.

        Args:
            namespace: Exact namespace to inspect, for example kagent.

        Returns only pod name, namespace, phase, ready container count, and
        restart count. Does not return images, environment variables, volumes,
        Secret data, or full Pod specifications.
        """
        if not namespace.strip():
            raise ValueError("namespace must not be empty")
        return summarize_pods(fetch_pods(namespace.strip()))
