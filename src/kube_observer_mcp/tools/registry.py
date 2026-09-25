"""Explicit tool-group registration; only read-only tools are enabled by default."""

from collections.abc import Callable, Iterable

from mcp.server import MCPServer

from kube_observer_mcp.tools.read_only import register_read_only_tools

ToolRegistrar = Callable[[MCPServer], None]

TOOL_GROUPS: dict[str, ToolRegistrar] = {
    "read_only": register_read_only_tools,
}
DEFAULT_TOOL_GROUPS = ("read_only",)


def register_tool_groups(
    server: MCPServer,
    groups: Iterable[str] = DEFAULT_TOOL_GROUPS,
) -> None:
    """Register explicitly selected groups and fail closed for unknown groups."""
    for name in groups:
        try:
            registrar = TOOL_GROUPS[name]
        except KeyError as exc:
            raise ValueError(f"unknown tool group: {name}") from exc
        registrar(server)
