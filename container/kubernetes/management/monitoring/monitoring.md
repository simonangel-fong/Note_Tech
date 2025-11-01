# Kubernetes - Monitoring & Logging

[Back](../../index.md)

- [Kubernetes - Monitoring \& Logging](#kubernetes---monitoring--logging)
  - [Metric](#metric)
  - [Metrics Server](#metrics-server)
  - [Lab: Enable Metric Server](#lab-enable-metric-server)

---

## Metric

---

## Metrics Server

- In-memory monitoring solution

  - not store metrics on the disk

- `kubelet`
  - in terms of mornitoring , kubelet has a subcomponent `cadvisor`, the `Container Advisor`
- `cadvisor`
  - a subcomponent of the `kubelet` on each pod used to retrieving performance metrics from pods and exposing through the Kubelet API to make the metrics avaialable for the metrics server.

```sh
# view the logs of a pod with single container
kubectl logs -f pod_name

kubectl logs -f pod_name | grep WARNING

# view the logs of a pod with multiple containers
kubectl logs -f pod_name con_name
```

---

## Lab: Enable Metric Server

```sh
# deploy metric server: minikube
# minikube addons enable metrics-server
# 💡  metrics-server is an addon maintained by Kubernetes. For any concerns contact minikube on GitHub.
# You can view the list of minikube maintainers at: https://github.com/kubernetes/minikube/blob/master/OWNERS
#     ▪ Using image registry.k8s.io/metrics-server/metrics-server:v0.8.0
# 🌟  The 'metrics-server' addon is enabled

# confirm
kubectl get pod -A
# NAMESPACE     NAME                               READY   STATUS    RESTARTS        AGE
# kube-system   metrics-server-85b7d694d7-fjbwr    1/1     Running   0               98s

# view node metric
kubectl top node
# NAME       CPU(cores)   CPU(%)   MEMORY(bytes)   MEMORY(%)
# minikube   211m         5%       1394Mi          17%

kubectl top pod
# NAME               CPU(cores)   MEMORY(bytes)
# busybox-minikube   0m           3Mi
```
