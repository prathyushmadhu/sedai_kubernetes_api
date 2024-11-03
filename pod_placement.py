from kubernetes import client, config

config.load_kube_config()

v1 = client.CoreV1Api()
print(f"{'Pod Name':<70}{'Node Name':<20}{'Namespace':<20}")
print("-" * 110)
ret = v1.list_pod_for_all_namespaces(watch=False)
for pod in ret.items:
    print(f"{pod.metadata.name:<70}{pod.spec.node_name:<20}{pod.metadata.namespace:<20}")