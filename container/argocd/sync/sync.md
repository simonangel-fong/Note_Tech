# ArgoCD - Sync

[Back](../index.md)

- [ArgoCD - Sync](#argocd---sync)
  - [Sync](#sync)
  - [Imparative](#imparative)
  - [Declarative](#declarative)
    - [Lab: Create app with auto sync](#lab-create-app-with-auto-sync)
  - [Pruning](#pruning)
    - [Lab: Create app with auto pruning](#lab-create-app-with-auto-pruning)
  - [Automated Self Healing](#automated-self-healing)
    - [Lab: Create app with self healing](#lab-create-app-with-self-healing)
  - [Sync Otions](#sync-otions)
    - [No Prune](#no-prune)
    - [Disable Kubectl Validation](#disable-kubectl-validation)
    - [Selective Sync](#selective-sync)
    - [Prune Last](#prune-last)
    - [Replace Resources](#replace-resources)
    - [Fail on Shared Resource](#fail-on-shared-resource)
  - [Sync Phases \& Hook](#sync-phases--hook)
    - [Hook Deletion Policies](#hook-deletion-policies)
  - [Sync Waves](#sync-waves)
    - [Example: Sync Phases + Sync Waves](#example-sync-phases--sync-waves)

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

## Declarative

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

### Lab: Create app with auto sync

- Create from private repo
- git commit and push
- observe changes

---

## Pruning

- no prune:
  - default
  - when automated sync is enabled, **by default** for safety automated sync will **not delete resources** when Argo CD detects the resource is no longer defined in Git

- Pruning can be enabled to delete resources automatically as part of the automated sync.

```sh
argocd app create --auto-prune
```

---

### Lab: Create app with auto pruning

---

## Automated Self Healing

- By default, changes that are made to the **live cluster** will **not trigger** `automated sync`.
- ArgoCD has a feature to enable `self healing` when the `live cluster state` **deviates** from `Git state`.

```sh
argocd app create --self-heal
```

---

### Lab: Create app with self healing

- deploy no self healing and with self healing
- scale both 2->3
- observe behavior

---

## Sync Otions

- Users can customize how resources are synced between target cluster and desired state.
  - Most of the options available **at application level**
  - Some of the options available using **resources annotations**.

- common options `syncOptions`:
  - `prune`:

---

### No Prune

- If the resource is removed from the git repo, the resource will still exist until manual deletion.
  - the removed resource still shows in argocd
  - app is in out-of-synced state
  - need manual deletion

- Specify at resource level

```yaml
metadata:
  annotations:
    argocd.argoproj.io/sync-options: Prune=false
```

---

### Disable Kubectl Validation

- application level

```yaml
spec:
  syncPolicy:
    syncOptions:
      - Validate=false
```

- resource level

```yaml
metadata:
  annotations:
    argocd.argoproj.io/sync-options: Validate=false
```

---

### Selective Sync

- Default, when syncing using **auto sync** ArgoCD **applies every object** in the application.
- `Selective sync` option
  - only some resources are sync
  - sync only out-of-sync resources.

- Can be applied at application level **only**:

```yaml
spec:
  syncPolicy:
    syncOptions:
      - ApplyOutOfSyncOnly=true
```

---

### Prune Last

- ArgoCD can control the **sequence** of creation/pruning resources, aka `waves`.
- can prune some resources to happen as final using “Prune Last”.
- can achieve this in ArgoCD by at application level or resource level.

- Application level

```yaml
spec:
  syncPolicy:
    syncOptions:
      - PruneLast=true
```

- Resource level

```yaml
metadata:
  annotations:
    argocd.argoproj.io/sync-options: PruneLast=true
```

---

### Replace Resources

- By **default** ArgoCD use `kubectl apply` to **deploy** the resources changes.
- In some cases you need to “Replace/Recreate” the resources, ArgoCD can do this by using `replace=true`.
- You can achieve this in ArgoCD by at application level or resource level.

- application level

```yaml
spec:
  syncPolicy:
    syncOptions:
      - Replace=true
```

- Resource level

```yaml
metadata:
  annotations:
    argocd.argoproj.io/sync-options: Replace=true
```

---

### Fail on Shared Resource

- By default ArgoCD will apply the resources even if it was available in multiple applications.
- You can configure the `sync to fail` if any resource is **found in other applications** by using `FailOnSharedResource=true`.

- application level only

```yaml
spec:
  syncPolicy:
    syncOptions:
      - FailOnSharedResource=true
```

---

## Sync Phases & Hook

- `hook`
  - Kubernetes resources (like Jobs) annotated with `argocd.argoproj.io/hook` that **run custom logic** at specific stages of an application's lifecycle, such as before, during, or after a synchronization (deployment).
  - enable automation for tasks like database migrations, integration tests, or cleanup without interrupting the main deployment flow.

| Hook         | Description                                                       |
| ------------ | ----------------------------------------------------------------- |
| `PreSync`    | Executes **before** any resources are applied.                    |
| `Sync`       | Runs **alongside** standard **application syncing**.              |
| `Skip`       | Indicates to Argo CD to **skip** the application of the manifest. |
| `PostSync`   | Executes **after** all resources are **synced and healthy**.      |
| `SyncFail`   | Runs if the synchronization **fails**.**fails**.                  |
| `PreDelete`  | Executes **before** the application is **deleted**.               |
| `PostDelete` | Executes **after** the application is deleted.                    |

---

- Usage:
  - use phases using resources hooks annotation `argocd.argoproj.io/hook` on app manifests.

- example

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  generateName: database-migrations
  annotations:
    argocd.argoproj.io/hook: PreSync
```

---

### Hook Deletion Policies

- `hook deletion policies` (`argocd.argoproj.io/hook-delete-policy`)
  - **annotations** that dictate when automated task resources (like Jobs or Pods) **are cleaned up** after running.
  - They ensure cluster cleanliness by automatically **deleting completed hooks**.

- Policies include `HookSucceeded`, `HookFailed`, and `BeforeHookCreation`.

| Policies             | Description                                                                                                                    |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `HookSucceeded`      | Deletes the resource if it **finishes successfully**, but keeps it for debugging if it fails.                                  |
| `HookFailed`         | Deletes the resource if **the hook fails**.                                                                                    |
| `BeforeHookCreation` | **Default** policy; **deletes any existing** hook resource before creating a new one, ensuring a clean state for the new hook. |

---

- How to Use Them:
  - `Annotations` are **added** to the resource metadata, typically to Kubernetes Jobs or Pods used for tasks like migrations, as shown in this Argo CD Resource Hooks Documentation.

---

## Sync Waves

- `Sync Waves`
  - an annotation-based feature (`argocd.argoproj.io/sync-wave`) that **controls the order** in which Kubernetes resources are **applied** to a cluster.

- `integer wave value`
  - a numerical annotation used to **control the exact deployment order** of Kubernetes resources.
    - Default Value: 0

- Behavior:
  - ArgoCD orders waves from the **lowest integer** to the **highest**.
    - **Lower values**: deployed **first**
    - **negative numbers** are allowed **for pre-deployment**
    - all resources in the **same wave** deploy **in parallel**.
  - ArgoCD **waits** for all resources in one wave to be **healthy** before proceeding to the next.
    - If a resource in a wave **fails** to become healthy, the **subsequent waves** will **not be deployed**, causing the **sync to "get stuck"**.

- Example:

```yaml
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "5"
```

- Example Scenario (Using Sync Waves):
  - Wave -5: Namespaces, Network Policies.
  - Wave -1: Persistent Volume Claims, ConfigMaps, Secrets.
  - Wave 0 (Default): Database Deployment.
  - Wave 1: Application Deployment.

---

### Example: Sync Phases + Sync Waves

Order:

- phase
- wave, from lower values
- By kind
- By name

- The Scenario: Deploying a Data-Driven Web AppPhase

1. `PreSync`: The Setup
   1. **Wave -1**:
      - Create the Namespace so it definitely exists.
   2. **Wave 0**:
      - Run a Database Migration job to update the schema.
      - Argo CD waits here until the migration is successful.
2. Phase 2: `Sync` (The Main Event)
   1. **Wave 1**:
      - Deploy the Database and Redis cache.
      - Argo CD waits until the database is "Healthy" and ready for connections.
   2. **Wave 2**:
      - Deploy the Backend API.
      - Argo CD waits until the API passes its readiness probe.
   3. **Wave 3**:
      - Deploy the Frontend UI.
      - Since the API is already up, the UI won't show "502 Bad Gateway" errors to users.
3. Phase 3: `PostSync` (The Wrap-up)
   1. **Wave 0**:
      - Run a Smoke Test script to verify the website loads.
   2. **Wave 5**:
      - Send a Slack Notification saying "Deployment Complete!"
