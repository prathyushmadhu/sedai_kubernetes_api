from kubernetes.client import CustomObjectsApi
from kubernetes import config

config.load_kube_config()

api = CustomObjectsApi()

pod_metrics = api.list_namespaced_custom_object(
    group="metrics.k8s.io", version="v1beta1", namespace="default", plural="pods"
)

for pod in pod_metrics['items']:
    print(f"Pod: {pod['metadata']['name']}, Namespace: {pod['metadata']['namespace']}")
    for container in pod['containers']:
        print(f"  Container: {container['name']}")
        print(f"    CPU Usage: {container['usage']['cpu']}")
        print(f"    Memory Usage: {container['usage']['memory']}")
