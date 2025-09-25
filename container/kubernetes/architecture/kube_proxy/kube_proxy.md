# Kubernetes - kube-proxy

[Back](../../index.md)

- [Kubernetes - kube-proxy](#kubernetes---kube-proxy)
  - [kube-proxy](#kube-proxy)

---

## kube-proxy

- `kube-proxy`

  - a **networking component** that runs **on every node** in a Kubernetes cluster.
  - used to **maintain the network rules** that allow communication to `Services` and the `Pods` behind them.

- Primary Roles
  - **Service Implementation**
    - Watches the `API Server` for `Service` and `Endpoint` objects.
    - Ensures that **traffic** sent to a `Service` (ClusterIP, NodePort, LoadBalancer) is routed to one of its `backend Pods`.
  - **Load Balancing**
    - **Distributes requests** across all healthy Pods behind a Service.
    - Uses round-robin or other mechanisms depending on the backend mode (iptables, IPVS).
  - **Programming Network Rules**
    - Manages `iptables` or `IPVS` rules on the node.
    - Ensures packets destined for a Service are redirected to the correct Pod IPs.

```sh
kubectl get pods -n kube-system
# kube-proxy-xbtjz                         1/1     Running   122 (4h29m ago)   148d

kubectl get daemonset -n kube-system
# NAME         DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
# kube-proxy   1         1         1       1            1           kubernetes.io/os=linux   148d
```
