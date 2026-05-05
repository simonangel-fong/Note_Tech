# ArgoCD - Sync Policy

[Back](../index.md)

- [ArgoCD - Sync Policy](#argocd---sync-policy)
  - [Sync and Health Statuses](#sync-and-health-statuses)
    - [Imparative Commands](#imparative-commands)
    - [Declarative](#declarative)
  - [Sync Policy](#sync-policy)
    - [Automated Sync](#automated-sync)
    - [Pruning](#pruning)
    - [Self-Healing](#self-healing)
  - [Sync Otions](#sync-otions)

---

## Sync and Health Statuses

- `Sync status`
  - whether the **live state**, or the deployed kubernetes resources, match the **desired state**, or the configuration files in the application repository.

| Sync status   | Description                                                                            |
| ------------- | -------------------------------------------------------------------------------------- |
| `Synced`      | The Live State **matches** the Desired State                                           |
| `OutOfSync`   | The Live State **does not match** the Desired State. Configuration drift has happened. |
| `Progressing` | The Application is **currently undergoing a sync operation**. Is temporary.            |

---

- `Health status`
  - whether the **live state**, or the deployed kubernetes resources, is in a **healthy status**.
  - Argo CD has built-in **health checks** for different Kubernetes resources.

| Health status | Description                                                                                                                    |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `Healthy`     | All the resources associated with the application are **in a good state**.                                                     |
| `Degraded`    | At **least one** resource is in a failed or unhealthy state. The application might be perfectly Synced, but still be Degraded. |

---

- Example of sync status vs health status
  - manifest defines k8s deployments
  - sync status applies to deployments, but not replicaset/pod, since they are not defined in the manifest.
  - health status applies to deployments, rs, and po, since they are health checked by cluster.

---

### Imparative Commands

| Command                                                | Description                                                       |
| ------------------------------------------------------ | ----------------------------------------------------------------- |
| `argocd app create <app-name> --sync-policy automated` | Create app with automated sync policy                             |
| `argocd app sync <app-name>`                           | Manually sync one application.                                    |
| `argocd app sync <app-name> --dry-run`                 | Preview sync **without applying changes**.                        |
| `argocd app sync <app-name> --prune`                   | Sync and **delete** resources that are no longer defined in Git.  |
| `argocd app sync <app-name> --force`                   | **Force** apply resources, when normal apply fails                |
| `argocd app sync <app-name> --replace`                 | Use **replace** instead of apply for some immutable field issues. |
| `argocd app sync <app-name> --resource <resource>`     | Sync only a specific Kubernetes resource.                         |
| `argocd app sync <app-name> --label <key=value>`       | Sync **only resources** matching a label selector.                |
| `argocd app sync <app-name> --revision <revision>`     | Sync the app to a specific Git revision, tag, or branch.          |
| `argocd app sync <app-name> --async`                   | Start sync and **return immediately without waiting**.            |
| `argocd app wait <app-name> --sync`                    | Wait until the app becomes **synced**.                            |
| `argocd app wait <app-name> --health`                  | Wait until the app becomes **healthy**.                           |
| `argocd app wait <app-name> --sync --health`           | Wait until the app is both **synced and healthy**.                |
| `argocd app terminate-op <app-name>`                   | Stop a running sync operation.                                    |
| `argocd app diff <app-name>`                           | Compare Git desired state with live cluster state before syncing. |
| `argocd app history <app-name>`                        | Show previous sync/deployment history.                            |
| `argocd app rollback <app-name> <history-id>`          | Roll back to a previous deployment state.                         |

---

### Declarative

```yaml
# auto sync
spec:
  syncPolicy:
    automated: {}

# auto sync with
spec:
  syncPolicy:
    automated:
      prune: true   # automated pruning
      selfHeal: true    # self heal
```

---

## Sync Policy

- `Sync Policies`
  - define how and when Git repository **changes are applied to a Kubernetes cluster**.

```yaml
spec:
  syncPolicy:
    automated:
      enabled: true # Enables auto-sync when Git changes are detected
      prune: true # Automatically removes resources no longer in Git
      selfHeal: true # Reverts manual changes made directly in the cluster
```

---

### Automated Sync

- By default, Argo CD only **reports** `Out-Of-Sync`.
  - **polls** Git repositories **every 3 minutes** to detect changes to the manifests.
  - It does not automatically update the Kubernetes resources.
  - Benefits: It gives admin a chance to **review the planned changes before** clicking `SYNC`.

- `Automated Sync`:
  - the policy that allows ArgoCD to **automatically apply the changes without manual approval**.
  - can automatically sync apps when it **detects** differences between the `desired` manifests in Git, and the `live state` in the cluster.

- Notes:
  - Automatic sync will **not reattempt a sync** if the previous sync attempt against the **same commit-SHA** and parameters had **failed**.
  - **Rollback cannot** be performed against an application **with automated sync enabled**.

- Command:

```sh
argocd app create --sync-policy automated
```

- Declarative

```yaml
spec:
  syncPolicy:
    automated: {}

# or
spec:
  syncPolicy:
    enabled: true
```

---

### Pruning

- By default, Argo CD **does not delete resources** if it cannot find their manifests in the source.
  - if you delete a manifest, by default Argo CD will not delete that resource in the cluster.
- `Pruning`
  - the policy that allows Argo CD to **actually clean up orphaned resources** from the cluster if their manifests cannot be found.

- Command:

```sh
argocd app create --auto-prune
```

- Declarative

```yaml
spec:
  syncPolicy:
    automated:
      enabled: true
      prune: true
```

---

### Self-Healing

- Automated sync policies only trigger when the Git repository changes, **not if someone changes something in the cluster**.

- `Self-healing`:
  - a policy that enables self healing when the `live cluster state` **deviates** from `Git state`.
  - immediately **revert changes** to the cluster resources that lead to resources being in a different state than that specified in the Git repository.
  - keep `live state` = `desired state`

- Command

```sh
argocd app create --self-heal
```

- Declarative

```yaml
spec:
  syncPolicy:
    automated:
      enabled: true
      selfHeal: true
```

---

## Sync Otions

- `Sync Options`
  - configuration settings that allow users to **customize how application manifests are applied** to a Kubernetes cluster.
  - enable **finer control** over deployment behavior
  - `spec.syncPolicy.syncOptions`

- Common Sync Options

| Sync Option (Default)            | Description                                                                                    |
| -------------------------------- | ---------------------------------------------------------------------------------------------- |
| `ApplyOutOfSyncOnly=false`       | Only applies resources that are out of sync (skips in-sync ones)                               |
| `CreateNamespace=false`          | Creates the target namespace if it does not exist.                                             |
| `FailOnSharedResource=true`      | prevents an app from syncing if it detects that another application already owns the resource. |
| `Force=false`                    | Deletes and recreates resources when a patch cannot be applied                                 |
| `Prune=false`                    | protect specific resources from being deleted                                                  |
| `PruneLast=false`                | Prunes resources only after all other resources are healthy                                    |
| `Replace=false`                  | Uses kubectl replace instead of kubectl apply (destructive)                                    |
| `RespectIgnoreDifferences=false` | Respects ignored fields during sync, not just during diff display                              |
| `ServerSideApply=false`          | Uses server-side apply instead of client-side apply                                            |
| `Validate=false`                 | Enable client-side Kubernetes schema validation                                                |

---

- Users can customize how resources are synced between target cluster and desired state.
  - Most of the options available **at application level**
  - Some of the options available using **resources annotations**.

- Application level

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
spec:
  syncPolicy:
    syncOptions:
      - Prune=false
```

- Resources level

```yaml
metadata:
  annotations:
    argocd.argoproj.io/sync-options: Prune=false
```

---
