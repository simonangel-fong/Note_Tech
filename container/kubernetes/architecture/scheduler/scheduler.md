# Kubernetes - Scheduler

[Back](../../index.md)

- [Kubernetes - Scheduler](#kubernetes---scheduler)
  - [Scheduler](#scheduler)

---

## Scheduler

- `scheduler`

  - a **control plane** component used to assign `pods` to `nodes`.
    - **decides** where a `Pod` should run, based on resource availability, constraints, and scheduling **policies**.
  - just **writes the decision** back to the `API Server`.
    - Not to actually place the pod on the node, which is managed by `kubelet`
    - `kubelet` on the chosen `node` then **pulls** the `Pod` spec and starts the containers.

---

- How It Works: `etcd`->`scheduler`->`api server`->`kubelet`->`pod`
  - `API Server` receives a request
    - e.g., `kubectl apply -f pod.yaml`.
  - The Pod object is **stored** in `etcd` but is initially **unscheduled** (no Node assigned).
  - `Scheduler` detects unscheduled Pods and runs its **scheduling algorithm**:
    - **Filtering** (predicates): **eliminate** nodes that cannot host the Pod (not enough CPU/memory, taints, constraints).
    - **Scoring** (priorities): **rank** the remaining nodes by preference (least loaded, locality, affinity, etc.).
  - `Scheduler` selects the **best** node.
  - It writes the **decision** (`.spec.nodeName`) back to the `API Server`.
  - The `kubelet` on that node pulls the `Pod` spec and starts the container.

```sh
kubectl get pods -n kube-system
# NAME                                     READY   STATUS    RESTARTS         AGE
# kube-scheduler-docker-desktop            1/1     Running   201 (4h2m ago)   148d

```
