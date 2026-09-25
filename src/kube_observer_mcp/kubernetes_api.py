"""Kubernetes API client setup and read-only inventory calls."""

from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException


def core_v1_api() -> client.CoreV1Api:
    """Load in-cluster credentials, falling back to the current kubeconfig locally."""
    try:
        config.load_incluster_config()
    except ConfigException:
        config.load_kube_config()
    return client.CoreV1Api()


def fetch_nodes() -> list[client.V1Node]:
    """List Kubernetes nodes through the Core API."""
    return core_v1_api().list_node(_request_timeout=10).items


def fetch_pods(namespace: str) -> list[client.V1Pod]:
    """List pods from one namespace through the Core API."""
    return core_v1_api().list_namespaced_pod(
        namespace=namespace,
        _request_timeout=10,
    ).items
