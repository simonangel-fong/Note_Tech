# Kubernetes - DaemonSets

[Back](../../index.md)

- [Kubernetes - DaemonSets](#kubernetes---daemonsets)
  - [DaemonSet](#daemonset)
    - [How does it work](#how-does-it-work)
    - [DaemonSet vs ReplicaSet vs Deployment](#daemonset-vs-replicaset-vs-deployment)
  - [Imperatives Commands](#imperatives-commands)
  - [Declarative File](#declarative-file)
  - [Lab: DS](#lab-ds)

---

## DaemonSet

- `DaemonSet`

  - a workload controller that replicates a particular Pod across the Nodes
  - As `nodes` **join/leave** the cluster, the `DaemonSet` automatically **adds/removes** the `Pod` on those `nodes`.

- By default, `DaemonSets` will attempt to **run on all nodes** that are **not tainted** to prevent scheduling, such as control plane nodes.

- Feature

  - Automatic **Pod Creation**
    - **automatically schedules** one **instance** of its defined Pod on **each eligible node** in the cluster.
  - **Node Addition** Handling
    - automatically detects and schedules a new Pod on that newly added node.
  - **Node Removal** Handling:
    - If a node is **removed** from the cluster, the DaemonSet controller detects this and automatically garbage collects (deletes) the corresponding Pod running on that removed node.

- Common use cases
  - networking:
    - `kube-proxy`, an agent used to set up Service forwarding on each node.
    - `calico`, an agent for networking solution
  - Monitoring and logging:
    - log shippers (Fluent Bit/Fluentd),
    - metrics (node-exporter),
    - security/EBPF agents (Falco),
    - backup daemons
  - CNI/CNI add-ons, CSI node plugins

---

### How does it work

- Before v1.12
  - use the nodeName in the pode to schedule on each node
- v1.12
  - use Default Scheduler + NodeAffinity

---

### DaemonSet vs ReplicaSet vs Deployment

- If need one per node: `DaemonSet`.
- If need N replicas with rollouts & rollback: `Deployment`.
- Use `ReplicaSet` directly only for niche cases (e.g., custom controllers, teaching) — most users should use Deployments.

---

## Imperatives Commands

- CRUD

| Command                                     | Description                                                 |
| ------------------------------------------- | ----------------------------------------------------------- |
| `kubectl explain ds`                        | See field docs (`spec`, `updateStrategy`, etc.).            |
| `kubectl get ds -A`                         | List all DaemonSets across namespaces.                      |
| `kubectl get ds`                            | List all DaemonSets in current namespaces.                  |
| `kubectl get ds ds_name -n ns_name`         | Show a DaemonSet.                                           |
| `kubectl get ds ds_name -n ns_name -o wide` | Show a DaemonSet with node, images, and selectors.          |
| `kubectl describe ds ds_name -n ns_name`    | Detailed spec, events (great for scheduling/taints issues). |
| `kubectl apply -f ds.yaml`                  | Create/update from a manifest file.                         |
| `kubectl edit ds ds_name -n ns_name`        | Edit the DaemonSet live (opens your editor).                |
| `kubectl delete ds ds_name -n ns_name`      | Delete the DaemonSet (Pods will be removed).                |

- Manage

| Command                                                              | Description                                                      |
| -------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `kubectl label ds/ds_name key=value -n ns_name`                      | Add or change labels.                                            |
| `kubectl set image ds/ds_name con_name=image:tag -n ns_name`         | Update container image (triggers rolling update).                |
| `kubectl set env ds/ds_name KEY=VALUE --containers=<ctr> -n ns_name` | Add/change env vars.                                             |
| `kubectl annotate ds/ds_name key=value -n ns_name`                   | Add or change annotations.                                       |
| `kubectl patch ds/ds_name -n ns_name -p '<json/strategic merge>'`    | Quick, targeted spec changes.                                    |
| `kubectl rollout status ds/ds_name -n ns_name`                       | Watch rollout progress.                                          |
| `kubectl rollout history ds/ds_name -n ns_name`                      | See past revisions.                                              |
| `kubectl rollout undo ds/ds_name -n ns_name [--to-revision=N]`       | Roll back to a prior revision.                                   |
| `kubectl rollout restart ds/ds_name -n ns_name`                      | Restart Pods managed by the DaemonSet.                           |
| `kubectl get pods -l <selector> -n ns_name -o wide`                  | List the DaemonSet’s Pods (one per node).                        |
| `kubectl logs -l <selector> -n ns_name --all-containers`             | Stream logs from all matching Pods.                              |
| `kubectl drain <node> --ignore-daemonsets`                           | Drain a node without evicting DaemonSet Pods (node maintenance). |

---

## Declarative File

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: monitoring-daemon
spec:
  selector:
    matchLabels:
      app: monitoring-agent
  template:
    spec:
      containers:
        - name: monitoring-agent
          image: monitoring-agent
```

---

## Lab: DS

```sh
# list all ds
kubectl get ds -A
# NAMESPACE     NAME         DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
# kube-system   kube-proxy   1         1         1       1            1           kubernetes.io/os=linux   16d

# list ds in system ns
kubectl get ds kube-proxy -n kube-system
# NAME         DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
# kube-proxy   1         1         1       1            1           kubernetes.io/os=linux   16d

# with pod, image ans selector
kubectl get ds kube-proxy -n kube-system -o wide
# NAME         DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE   CONTAINERS   IMAGES                               SELECTOR
# kube-proxy   1         1         1       1            1           kubernetes.io/os=linux   16d   kube-proxy   registry.k8s.io/kube-proxy:v1.34.1   k8s-app=kube-proxy

# show details
kubectl describe ds kube-proxy -n kube-system
# Name:           kube-proxy
# Namespace:      kube-system
# Selector:       k8s-app=kube-proxy
# Node-Selector:  kubernetes.io/os=linux
# Labels:         k8s-app=kube-proxy
# Annotations:    deprecated.daemonset.template.generation: 1
# Desired Number of Nodes Scheduled: 1
# Current Number of Nodes Scheduled: 1
# Number of Nodes Scheduled with Up-to-date Pods: 1
# Number of Nodes Scheduled with Available Pods: 1
# Number of Nodes Misscheduled: 0
# Pods Status:  1 Running / 0 Waiting / 0 Succeeded / 0 Failed


```
