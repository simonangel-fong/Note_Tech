# Kubernetes - Manual Scheduler

[Back](../../index.md)

- [Kubernetes - Manual Scheduler](#kubernetes---manual-scheduler)
  - [Manual Scheduler](#manual-scheduler)
    - [Pod spec Method](#pod-spec-method)
    - [Binding object Method](#binding-object-method)

---

## Manual Scheduler

- `Manual Scheduler`

  - Normally, the `Kubernetes Scheduler` **decides** where Pods run.
  - can **bypass** it and **manually assign** `Pods` to `nodes`.
  - used for testing, debugging, or in very small setups.

- Pros

  - **Learning/demo purposes**: understand scheduler internals.
  - **Debugging**: check how a Pod behaves on a specific node.
  - **Tiny clusters / edge setups**: where you don’t want or need the full scheduler.

- Cons
  - **No filtering or scoring**: you must know if the node has enough resources.
  - **Not scalable**: every Pod must be assigned manually.
  - **Easy to make mistakes**: wrong node, resource mismatch, Pod stuck in Pending.

---

### Pod spec Method

- `pod.yaml`

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-manual
spec:
  containers:
    - name: nginx
      image: nginx
  nodeName: worker-node-1
```

- Kubernetes will **not invoke** the `scheduler` at all.
- The `Pod` **goes straight** to the `kubelet` on worker-node-1.
  - If the node name is **invalid** or the node **doesn’t have enough resources**, the Pod stays in **Pending state forever**.

---

### Binding object Method

- `binding.yaml`
  - bind Pod nginx to node worker-node-1.

```yaml
apiVersion: v1
kind: Binding
metadata:
  name: nginx
target:
  apiVersion: v1
  kind: Node
  name: worker-node-1
```
