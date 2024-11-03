from kubernetes.client import CustomObjectsApi
from kubernetes import config
import numpy as np

def calculate_stats(data):
    avg = np.mean(data)
    max_val = np.max(data)
    p99 = np.percentile(data, 99)
    return avg, max_val, p99

config.load_kube_config()

api = CustomObjectsApi()

pod_metrics = api.list_namespaced_custom_object(
    group="metrics.k8s.io", version="v1beta1", namespace="default", plural="pods"
)

c_usages = []
m_usages = []

print("Pod-wise CPU and Memory Usage Stats:\n")

for pod in pod_metrics['items']:
    pod_cpu_usages = []
    pod_memory_usages = []

    print(f"Pod: {pod['metadata']['name']}, Namespace: {pod['metadata']['namespace']}")

    
    for container in pod['containers']:
        cpu_usage = int(container['usage']['cpu'].rstrip('n')) / 1e6  
        memory_usage = int(container['usage']['memory'].rstrip('Ki')) / 1024  

        pod_cpu_usages.append(cpu_usage)
        pod_memory_usages.append(memory_usage)

        print(f"  Container: {container['name']}")
        print(f"    CPU Usage: {cpu_usage:.2f}m")
        print(f"    Memory Usage: {memory_usage:.2f} MiB")

    c_avg, c_max, c_p99 = calculate_stats(pod_cpu_usages)
    m_avg, m_max, m_p99 = calculate_stats(pod_memory_usages)

    print(f"  Pod CPU Usage: Avg: {c_avg:.2f}m, Max: {c_max:.2f}m, P99: {c_p99:.2f}m")
    print(f"  Pod Memory Usage: Avg: {m_avg:.2f} MiB, Max: {m_max:.2f} MiB, P99: {m_p99:.2f} MiB\n")

    c_usages.extend(pod_cpu_usages)
    m_usages.extend(pod_memory_usages)

cpu_avg, cpu_max, cpu_p99 = calculate_stats(c_usages)
memory_avg, memory_max, memory_p99 = calculate_stats(m_usages)

print("Overall Cluster CPU and Memory Usage Stats:")
print(f"  CPU Usage : Avg: {cpu_avg:.2f}m, Max: {cpu_max:.2f}m, P99: {cpu_p99:.2f}m")
print(f"  Memory Usage : Avg: {memory_avg:.2f} MiB, Max: {memory_max:.2f} MiB, P99: {memory_p99:.2f} MiB")