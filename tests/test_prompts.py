import asyncio

import pytest
from mcp.server import MCPServer

from kube_observer_mcp.prompts import register_prompts
from kube_observer_mcp.tools.registry import register_tool_groups


def test_server_factory_registers_default_read_only_inventory_tools() -> None:
    from kube_observer_mcp.server import create_server

    server = create_server()
    tools = asyncio.run(server.list_tools())
    assert {tool.name for tool in tools} == {"list_nodes", "list_pods"}
    assert {prompt.name for prompt in asyncio.run(server.list_prompts())} == {
        "cluster_health_check",
        "summarize_namespace",
    }


def test_cluster_health_prompt_is_read_only_and_names_tool_sequence() -> None:
    server = MCPServer("test")
    register_prompts(server)

    prompts = asyncio.run(server.list_prompts())
    assert {prompt.name for prompt in prompts} == {
        "cluster_health_check",
        "summarize_namespace",
    }

    result = asyncio.run(server.get_prompt("cluster_health_check", {"namespace": "kagent"}))
    rendered = "\n".join(message.content.text for message in result.messages)
    assert "list_nodes" in rendered
    assert "list_pods" in rendered
    assert "namespace='kagent'" in rendered
    assert "do not attempt to change cluster resources" in rendered.lower()


def test_unknown_tool_group_fails_closed() -> None:
    with pytest.raises(ValueError, match="unknown tool group"):
        register_tool_groups(MCPServer("test"), ("write",))