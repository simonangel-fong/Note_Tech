# Argo Rollout - Fundamental

[Back](../index.md)

- [Argo Rollout - Fundamental](#argo-rollout---fundamental)
  - [Fundamental](#fundamental)
    - [Limitations of K8s Deployments](#limitations-of-k8s-deployments)
    - [Common Commands](#common-commands)

---

## Fundamental

### Limitations of K8s Deployments

- **Too Fast and "All or Nothing"**
  - Once a RollingUpdate begins, it proceeds to **completion as quickly as** it can create new pods.
  - There is **no** concept of **pausing** the rollout to observe the new version's behavior.
  - If you deploy a version with a bug, the `RollingUpdate` will happily **continue replacing all** of your pods with broken ones, rapidly escalating a small problem into a full-blown outage.
- **"Success" is Defined Poorly**
  - A `readiness probe` only confirms that a pod is **ready to accept traffic**.
    - It does not confirm that the application is **logically correct**.
    - As long as the readiness probe endpoint returns a 200 OK, Kubernetes considers the pod "Ready" and continues the rollout.
- **There is No Real Traffic Control**
  - The `RollingUpdate` strategy ties instance scaling directly to traffic shifting.
  - As soon as a new pod becomes "Ready", it's added to the Service's load balancing pool and begins receiving a portion of live user traffic.
- **Rollbacks Are Just Another Risky `RollingUpdate`**
  - When you trigger a rollback on a Deployment, Kubernetes **doesn't instantly switch back** to the old version.
  - Instead, it simply starts another RollingUpdate in reverse, replacing the bad pods with the last known-good version.

---

### Common Commands

| Command                           | Description                                     |
| --------------------------------- | ----------------------------------------------- |
| `kubectl argo rollouts version`   | Shows the Argo Rollouts kubectl plugin version. |
| `kubectl argo rollouts dashboard` | Starts the local Argo Rollouts dashboard.       |
