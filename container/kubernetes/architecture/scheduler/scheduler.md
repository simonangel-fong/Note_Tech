# Kubernetes - Scheduler

[Back](../index.md)

- [Kubernetes - Scheduler](#kubernetes---scheduler)
  - [Scheduler](#scheduler)

---

## Scheduler

- used to control which pod runs on which node.
  - Not to actually place the pod on the node, which is managed by `kubelet`
- scheduler looks at each pod and tries to find the best node for it.
  - Filter nodes
  - rank nodes

```sh
kubectl get pods -n kube-system
# NAME                                     READY   STATUS    RESTARTS         AGE
# kube-scheduler-docker-desktop            1/1     Running   201 (4h2m ago)   148d

```
