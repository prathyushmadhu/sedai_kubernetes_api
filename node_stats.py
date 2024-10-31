from kubernetes.client import CustomObjectsApi
from kubernetes import config

config.load_kube_config()

api = CustomObjectsApi()
node_metrics = api.list_cluster_custom_object(
    group="metrics.k8s.io", version="v1beta1", plural="nodes"
)

for node in node_metrics['items']:
    print(f"Node: {node['metadata']['name']}")
    print(f"  CPU Usage: {node['usage']['cpu']}")
    print(f"  Memory Usage: {node['usage']['memory']}")