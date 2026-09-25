from types import SimpleNamespace

from kube_observer_mcp.inventory import summarize_node, summarize_nodes, summarize_pod


def make_node(name: str, ready: str | None) -> SimpleNamespace:
    conditions = [] if ready is None else [SimpleNamespace(type="Ready", status=ready)]
    return SimpleNamespace(
        metadata=SimpleNamespace(name=name),
        status=SimpleNamespace(
            conditions=conditions,
            node_info=SimpleNamespace(
                kubelet_version="v1.35.5+k3s1",
                operating_system="linux",
                architecture="arm64",
            ),
        ),
    )


def test_node_summary_reports_ready_without_full_node_details() -> None:
    result = summarize_node(make_node("worker-a", "True"))

    assert result == {
        "name": "worker-a",
        "ready": "True",
        "kubelet_version": "v1.35.5+k3s1",
        "operating_system": "linux",
        "architecture": "arm64",
    }
    assert "images" not in result
    assert "status" not in result


def test_node_summary_uses_unknown_when_ready_condition_is_absent() -> None:
    assert summarize_node(make_node("worker-b", None))["ready"] == "Unknown"


def test_nodes_are_sorted_by_name() -> None:
    nodes = [make_node("worker-b", "True"), make_node("worker-a", "False")]

    assert [node["name"] for node in summarize_nodes(nodes)] == ["worker-a", "worker-b"]


def test_pod_summary_contains_only_requested_status_fields() -> None:
    pod = SimpleNamespace(
        metadata=SimpleNamespace(name="api-123", namespace="demo"),
        status=SimpleNamespace(
            phase="Running",
            container_statuses=[
                SimpleNamespace(ready=True, restart_count=1),
                SimpleNamespace(ready=False, restart_count=0),
            ],
        ),
    )

    result = summarize_pod(pod)

    assert result == {
        "name": "api-123",
        "namespace": "demo",
        "phase": "Running",
        "ready": "1/2",
        "restarts": 1,
    }
    assert "image" not in result
    assert "environment" not in result
