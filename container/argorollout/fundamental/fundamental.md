# Argo Rollout - Fundamental

[Back](../index.md)

- [Argo Rollout - Fundamental](#argo-rollout---fundamental)
  - [Fundamental](#fundamental)
    - [Limitations of K8s Deployments](#limitations-of-k8s-deployments)
  - [Argo Rollouts Architecture](#argo-rollouts-architecture)
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

## Argo Rollouts Architecture

- `Argo Rollouts`
  - a **Kubernetes controller** that **extends** the native Deployment resource to provide advanced deployment strategies (Blue-Green, Canary, etc.).

Key Components

- `Rollout Controller`
  - The brain — **watches** `Rollout CRDs` and **reconciles** desired vs actual state.
  - **Replaces** the standard `Deployment controller` for managed workloads.
- `Rollout CRD`
  - A **superset** of the Kubernetes `Deployment spec`, with extra fields for strategy configuration (canary steps, traffic weights, analysis hooks, etc.).
- `ReplicaSets`
  - Argo still uses standard `ReplicaSets` **under the hood**
  - it just manages which ones get traffic and how much.
- `AnalysisTemplate` / `AnalysisRun`
  - Defines automated rollout **health checks** (Prometheus queries, web hooks, Datadog metrics).
  - An `AnalysisRun` is the live execution instance — **pass/fail drives promotion or rollback**.
- **Traffic Management Integration**
  - Plugs into **ingress/service mesh layers** (Nginx, Istio, Linkerd, AWS ALB, etc.) to do **weighted traffic splitting** between stable and canary ReplicaSets.
- `Argo Rollouts UI` / `CLI` (kubectl-argo-rollouts)
  - Observability and manual control — pause, promote, abort, or watch live rollout progress.

---

- Data Flow (Canary Example)

```txt
New image pushed
      ↓
Rollout Controller detects spec change
      ↓
Creates new ReplicaSet (canary)
      ↓
Shifts traffic: e.g. 10% → canary, 90% → stable
      ↓
AnalysisRun fires (checks metrics/webhooks)
      ↓
  Pass → promote (increase traffic %)
  Fail → auto-rollback to stable ReplicaSet
      ↓
100% traffic on new → old ReplicaSet scaled to 0
```

---

### Common Commands

| Command                           | Description                                     |
| --------------------------------- | ----------------------------------------------- |
| `kubectl argo rollouts version`   | Shows the Argo Rollouts kubectl plugin version. |
| `kubectl argo rollouts dashboard` | Starts the local Argo Rollouts dashboard.       |
