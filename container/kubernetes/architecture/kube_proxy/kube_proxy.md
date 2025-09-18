# Kubernetes - Kubelet

[Back](../index.md)

- [Kubernetes - Kubelet](#kubernetes---kubelet)
  - [Kube-proxy](#kube-proxy)

---

## Kube-proxy

- `Kube-proxy`
  - a network proxy that runs on each node in a Kubernetes cluster.
  - a process that runs on each node in the k8s cluster
    - lives only in memory
    - monitor the service
      - whenever a new service is created, it creates the rules on each node to forward the traffic to the target pods.

```sh
kubectl get pods -n kube-system
# kube-proxy-xbtjz                         1/1     Running   122 (4h29m ago)   148d

kubectl get daemonset -n kube-system
# NAME         DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
# kube-proxy   1         1         1       1            1           kubernetes.io/os=linux   148d
```
