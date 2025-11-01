# Kubernetes - Pod: Static Pod

[Back](../../index.md)

- [Kubernetes - Pod: Static Pod](#kubernetes---pod-static-pod)
  - [Static Pod](#static-pod)
    - [vs DaemonSets](#vs-daemonsets)
    - [Designated Directory for manifest file](#designated-directory-for-manifest-file)
  - [Common Command](#common-command)
  - [Lab: Create a Static Pod](#lab-create-a-static-pod)

---

## Static Pod

- `static pod`

  - A `Pod` **managed directly** by the `kubelet` on a node
    - not by the `API server`, `scheduler`, or `controllers`.
  - The `kubelet` periodically checks a **local directory** for `Pod manifest files` (YAML).
    - If a file **appears/changes**, the kubelet **creates/updates** the Pod on that node only.
    - If the `static pod` crashes, `kubelet` attempts ot restart it.

- vs common pod:

  - common pods managed by K8S cluster components
  - static pod managed by `kubelet`

- Feature:

  - **No scheduler**:
    - The Pod always runs on the node whose `kubelet` loaded the file.
  - **Mirror Pod**:
    - The `kubelet` creates a read-only “mirror” `Pod` object in the `API server` so kubectl get pods can show it. API 可见且只读
    - The Pod name gets a `-<nodeName>` suffix.
  - Lifecycle tied to file:
    - Add/modify/delete the **manifest file** → kubelet creates/updates/stops the **Pod**.
  - **No controllers**:
    - don’t get ReplicaSets, Jobs, rollouts, or auto-restarts by a `controller`
    - `kubelet` will **restart containers** if they crash per its restart policy, but there’s no higher-level management.
  - **Node-scoped**:
    - Each node can have different static Pods by placing different files on each node.

- Common use cases:
  - used by `kubeadm` to **bootstrap control-plane components** (kube-apiserver, kube-scheduler, etc.)
  - **Node-local agents/daemons** that must run even if the API server is down.

---

### vs DaemonSets

| Static Pods                             | DaemonSets                                                      |
| --------------------------------------- | --------------------------------------------------------------- |
| Ignored by `kube-scheduler`             | Ignored by `kube-scheduler`                                     |
| Managed by `kubelet`                    | Managed by `kube-apiserver`(DaemonSet Controller)               |
| Used to deploy control-plane components | Used to deploy agent on nodes (Monitoring, logging, networking) |

---

### Designated Directory for manifest file

- default location: `/etc/kubernetes/manifests`

---

- Identify the location:

```sh
cat /var/lib/kubelet/config.yaml | grep staticPodPath
# staticPodPath: /etc/kubernetes/manifests
```

---

- Specify a path in `kubectl` service

  - Service file:
    ```conf
    ExecStar=/usr/local/bin/kubelet
        --container-runtime=remote
        --container-runtime-ndpoints=unix:///var/run/containerd/containerd.sock
        --pod-manifest-path=/etc/kubernetes/manifests   # specify path
        --kubeconfig=/var/lib/kubelet/kubeconfig
        --network-plugin=cni
        --register-node=true
        --v=2
    ```

- Specify a conf file, then specify in the cf
  - Service file:
    ```conf
    ExecStar=/usr/local/bin/kubelet
        --container-runtime=remote
        --container-runtime-ndpoints=unix:///var/run/containerd/containerd.sock
        --config=kubeconfig.yaml   # specify a cf
        --kubeconfig=/var/lib/kubelet/kubeconfig
        --network-plugin=cni
        --register-node=true
        --v=2
    ```
  - config file:
    ```yaml
    staticPodPath: /etc/kubernetes/manifests
    ```

---

## Common Command

- Since it is managed by `kubelet` on each node,
  - `kubectl` is only used to read.

| Command                                     | Desc                                |
| ------------------------------------------- | ----------------------------------- |
| `docker ps`                                 | List the static pod on node         |
| `kubectl get pod -A \| grep -E *-node_name` | List the static pod in API endpoint |

---

## Lab: Create a Static Pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: static-busybox
  namespace: default
spec:
  containers:
    - image: busybox
      name: busybox
      command: ["sleep"]
      args: ["1000"]
```

kubectl run static-busybox --image=busybox -- sleep 1000 --dry-run=client -o yaml > bb.yaml
