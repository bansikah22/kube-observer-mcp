"""Small, explicit summaries of Kubernetes nodes and pods."""

from collections.abc import Iterable
from typing import Any


def summarize_node(node: Any) -> dict[str, str]:
    """Return node name, Ready condition, Kubernetes version, OS, and architecture."""
    status = getattr(node, "status", None)
    info = getattr(status, "node_info", None)
    conditions = getattr(status, "conditions", None) or []
    ready_condition = next((item for item in conditions if item.type == "Ready"), None)

    return {
        "name": node.metadata.name,
        "ready": ready_condition.status if ready_condition else "Unknown",
        "kubelet_version": getattr(info, "kubelet_version", "") or "Unknown",
        "operating_system": getattr(info, "operating_system", "") or "Unknown",
        "architecture": getattr(info, "architecture", "") or "Unknown",
    }


def summarize_pod(pod: Any) -> dict[str, Any]:
    """Return concise pod identity/readiness data, not the full Pod specification."""
    status = getattr(pod, "status", None)
    container_statuses = getattr(status, "container_statuses", None) or []
    ready_count = sum(1 for item in container_statuses if item.ready)
    restart_count = sum(item.restart_count or 0 for item in container_statuses)
    total_containers = len(container_statuses)

    return {
        "name": pod.metadata.name,
        "namespace": pod.metadata.namespace,
        "phase": getattr(status, "phase", None) or "Unknown",
        "ready": f"{ready_count}/{total_containers}",
        "restarts": restart_count,
    }


def summarize_nodes(nodes: Iterable[Any]) -> list[dict[str, str]]:
    """Convert Kubernetes Node objects to concise inventory records."""
    return sorted((summarize_node(node) for node in nodes), key=lambda item: item["name"])


def summarize_pods(pods: Iterable[Any]) -> list[dict[str, Any]]:
    """Convert Kubernetes Pod objects to concise inventory records."""
    return sorted(
        (summarize_pod(pod) for pod in pods),
        key=lambda item: (item["namespace"], item["name"]),
    )
