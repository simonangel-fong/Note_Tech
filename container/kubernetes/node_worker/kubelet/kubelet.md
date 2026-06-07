# Kubernetes - `kubelet`

[Back](../../index.md)

- [Kubernetes - `kubelet`](#kubernetes---kubelet)
  - [Kubelet](#kubelet)
  - [Lab: kubelet failure](#lab-kubelet-failure)

---

## Kubelet

- `kubelet`
  - the **agent** that **runs on every node** in a Kubernetes cluster and ensures that containers are running in Pods as expected on its node.

- Primary Roles
  - **Node Registration & Management**
    - **Registers the node** with the cluster’s `API Server`.
    - Ensures node labels, capacity, and conditions are kept up to date.
  - **Static Pod Management**
    - Runs Pods defined locally on the node (in `/etc/kubernetes/manifests/`).
    - Commonly used to run `control plane` components on `master nodes`.
  - **Pod Lifecycle Management**
    - **Watches** the `API Server` for Pods assigned to its node.
    - **Creates, starts, stops, and deletes** containers to match the `PodSpec`.
    - Continuously checks and **reconciles**: “Are the right Pods running on this node?”
  - **Interface to Container Runtime**
    - Talks to the `container runtime` (Docker, containerd, CRI-O) via the `Container Runtime Interface (CRI)`.
    - Actually launches containers as requested in `PodSpecs`.
  - **Health Monitoring & Reporting**
    - Runs liveness, readiness, and startup **probes** for containers.
    - Reports Pod and Node status (e.g., CPU/memory pressure, health) back to the `API Server`.

---

## Lab: kubelet failure

```sh
# disable kubelet in Worker Node
sudo systemctl stop kubelet
sudo systemctl status kubelet
# ○ kubelet.service - kubelet: The Kubernetes Node Agent
#      Loaded: loaded (/usr/lib/systemd/system/kubelet.service; enabled; preset: enabled)
#     Drop-In: /usr/lib/systemd/system/kubelet.service.d
#              └─10-kubeadm.conf
#      Active: inactive (dead) since Fri 2026-06-05 15:03:38 EDT; 5s ago
#    Duration: 7.359s
#        Docs: https://kubernetes.io/docs/
#     Process: 55102 ExecStart=/usr/bin/kubelet $KUBELET_KUBECONFIG_ARGS $KUBELET_CONFIG_ARGS $KUBELET_KUBEADM_ARGS $KUBELET_EXTRA_ARGS (code=exi>
#    Main PID: 55102 (code=exited, status=0/SUCCESS)
#         CPU: 1.132s

# Jun 05 15:03:33 node01 kubelet[55102]: I0605 15:03:33.034252   55102 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolum>
# Jun 05 15:03:33 node01 kubelet[55102]: I0605 15:03:33.034559   55102 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolum>
# Jun 05 15:03:33 node01 kubelet[55102]: I0605 15:03:33.034582   55102 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolum>
# Jun 05 15:03:33 node01 kubelet[55102]: I0605 15:03:33.113225   55102 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolum>
# Jun 05 15:03:33 node01 kubelet[55102]: I0605 15:03:33.113459   55102 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolum>
# Jun 05 15:03:33 node01 kubelet[55102]: I0605 15:03:33.113480   55102 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolum>
# Jun 05 15:03:38 node01 systemd[1]: Stopping kubelet.service - kubelet: The Kubernetes Node Agent...
# Jun 05 15:03:38 node01 systemd[1]: kubelet.service: Deactivated successfully.
# Jun 05 15:03:38 node01 systemd[1]: Stopped kubelet.service - kubelet: The Kubernetes Node Agent.
# Jun 05 15:03:38 node01 systemd[1]: kubelet.service: Consumed 1.132s CPU ti
```

- Try to connect with pod

```sh
# controlplane
kubectl exec web-65d846d465-29rvx -- curl -I localhost
# error: Internal error occurred: error sending request: Post "https://192.168.10.151:10250/exec/default/web-65d846d465-29rvx/nginx?command=curl&command=-I&command=localhost&error=1&output=1": dial tcp 192.168.10.151:10250: connect: connection refused
```

- try to create po

```sh
# controlplane
kubectl run web-app --image=nginx
# pod/web-app created

kubectl get po web-app
# NAME      READY   STATUS    RESTARTS   AGE
# web-app   0/1     Pending   0          36s

kubectl describe po web-app
# Events:
#   Type     Reason            Age   From               Message
#   ----     ------            ----  ----               -------
#   Warning  FailedScheduling  61s   default-scheduler  0/3 nodes are available: 1 node(s) had untolerated taint {node-role.kubernetes.io/control-plane: }, 2 node(s) had untolerated taint {node.kubernetes.io/unreachable: }. preemption: 0/3 nodes are available: 3 Preemption is not helpful for scheduling.
```

- Restore

```sh
# worker node
sudo systemctl start kubelet

# controlplane
kubectl exec web-65d846d465-29rvx -- curl -I localhost
#   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
#                                  Dload  Upload   Total   Spent    Left  Speed
# HTTP/1.1 200 OK    0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
# Server: nginx/1.31.1
# Date: Fri, 05 Jun 2026 19:07:22 GMT
# Content-Type: text/html
# Content-Length: 896
# Last-Modified: Fri, 22 May 2026 12:50:47 GMT
# Connection: keep-alive
# ETag: "6a105127-380"
# Accept-Ranges: bytes

#   0   896    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0

kubectl get po web-app
# NAME      READY   STATUS    RESTARTS   AGE
# web-app   1/1     Running   0          91s

kubectl describe po web-app
# Events:
#   Type     Reason            Age    From               Message
#   ----     ------            ----   ----               -------
#   Warning  FailedScheduling  2m24s  default-scheduler  0/3 nodes are available: 1 node(s) had untolerated taint {node-role.kubernetes.io/control-plane: }, 2 node(s) had untolerated taint {node.kubernetes.io/unreachable: }. preemption: 0/3 nodes are available: 3 Preemption is not helpful for scheduling.
#   Normal   Scheduled         60s    default-scheduler  Successfully assigned default/web-app to node01
#   Normal   Pulling           56s    kubelet            Pulling image "nginx"
#   Normal   Pulled            55s    kubelet            Successfully pulled image "nginx" in 1.232s (1.232s including waiting). Image size: 63120520 bytes.
#   Normal   Created           55s    kubelet            Created container: web-app
#   Normal   Started           55s    kubelet            Started container web-app
```
