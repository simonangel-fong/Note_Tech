# ArgoCD - Sync

[Back](../index.md)

- [ArgoCD - Sync](#argocd---sync)
  - [Sync](#sync)
  - [Imparative](#imparative)
  - [Declarative](#declarative)

---

## Sync

- **Automated Sync**
  - By default, `ArgoCD` **polls** `Git repositories` **every 3 minutes** to detect changes to the manifests.
- Argo CD can automatically sync apps when it **detects** differences between the `desired` manifests in Git, and the `live state` in the cluster.
  - **No** need to do **manual** sync anymore.
  - CI/CD pipelines no longer need direct access.
- Notes:
  - An `automated sync` will **only** be performed if the application is `OutOfSync`.
  - Automatic sync will **not reattempt a sync** if the previous sync attempt against the **same commit-SHA** and parameters had **failed**.
  - **Rollback cannot** be performed against an application **with automated sync enabled**.

---

## Imparative

| Command                                                | Description                                                       |
| ------------------------------------------------------ | ----------------------------------------------------------------- |
| `argocd create app <app-name> --sync-policy automated` | Create app with automated sync policy                             |
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

## Declarative

```yaml
spec:
  syncPolicy:
    automated: {}
```

---


