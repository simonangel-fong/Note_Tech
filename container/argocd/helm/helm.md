# ArgoCD - Deploying Helm Charts

[Back](../index.md)

- [ArgoCD - Deploying Helm Charts](#argocd---deploying-helm-charts)
  - [Deploy Helm Charts](#deploy-helm-charts)
    - [Lab: Deploy Helm Chart](#lab-deploy-helm-chart)
  - [Specify Value](#specify-value)
    - [Value File](#value-file)
      - [Lab: Deploy Helm Charts with valueFiles](#lab-deploy-helm-charts-with-valuefiles)
    - [Parameters](#parameters)
      - [Lab: Deploy Helm Charts with parameters](#lab-deploy-helm-charts-with-parameters)

---

## Deploy Helm Charts

- `Argo CD` is a `helm template` engine.
  - When managing a Helm chart with Argo CD, it does not run `helm install` or `helm upgrade`.
  - there is no Helm history, helm install, helm upgrade, or helm uninstall.
- can use `Argo CD` to deploy both charts stored **in private own repositories**, as well as charts that are **publicly** available.

![pic](./pic/helm_template.png)

---

### Lab: Deploy Helm Chart

- Argocd application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: guestbook
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/simonangel-fong/argocd-example-apps.git
    targetRevision: HEAD
    path: helm-guestbook
  destination:
    server: "https://kubernetes.default.svc"
    namespace: default
```

```sh
kubectl apply -f guestbook-app.yaml
# application.argoproj.io/guestbook created

argocd app list
# NAME              CLUSTER                         NAMESPACE  PROJECT  STATUS     HEALTH   SYNCPOLICY  CONDITIONS  REPO                                                        PATH            TARGET
# argocd/guestbook  https://kubernetes.default.svc  default    default  OutOfSync  Missing  Manual      <none>      https://github.com/simonangel-fong/argocd-example-apps.git  helm-guestbook  HEAD

argocd app sync argocd/guestbookargocd app sync argocd/guestbook
# TIMESTAMP                  GROUP        KIND   NAMESPACE                  NAME        STATUS    HEALTH        HOOK  MESSAGE
# 2026-05-05T13:03:09-04:00            Service     default  guestbook-helm-guestbook  OutOfSync  Missing
# 2026-05-05T13:03:09-04:00   apps  Deployment     default  guestbook-helm-guestbook  OutOfSync  Missing
# 2026-05-05T13:03:10-04:00            Service     default  guestbook-helm-guestbook  OutOfSync  Missing              service/guestbook-helm-guestbook created
# 2026-05-05T13:03:10-04:00   apps  Deployment     default  guestbook-helm-guestbook  OutOfSync  Missing              deployment.apps/guestbook-helm-guestbook created

# Name:               argocd/guestbook
# Project:            default
# Server:             https://kubernetes.default.svc
# Namespace:          default
# URL:                https://argocd.example.com/applications/argocd/guestbook
# Source:
# - Repo:             https://github.com/simonangel-fong/argocd-example-apps.git
#   Target:           HEAD
#   Path:             helm-guestbook
# SyncWindow:         Sync Allowed
# Sync Policy:        Manual
# Sync Status:        Synced to HEAD (723b86e)
# Health Status:      Progressing

# Operation:          Sync
# Sync Revision:      723b86e01bea11dcf72316cb172868fcbf05d69e
# Phase:              Succeeded
# Start:              2026-05-05 13:03:09 -0400 EDT
# Finished:           2026-05-05 13:03:09 -0400 EDT
# Duration:           0s
# Message:            successfully synced (all tasks run)

# GROUP  KIND        NAMESPACE  NAME                      STATUS  HEALTH       HOOK  MESSAGE
#        Service     default    guestbook-helm-guestbook  Synced  Healthy            service/guestbook-helm-guestbook created
# apps   Deployment  default    guestbook-helm-guestbook  Synced  Progressing        deployment.apps/guestbook-helm-guestbook created

argocd app get argocd/guestbook
# Name:               argocd/guestbook
# Project:            default
# Server:             https://kubernetes.default.svc
# Namespace:          default
# URL:                https://argocd.example.com/applications/guestbook
# Source:
# - Repo:             https://github.com/simonangel-fong/argocd-example-apps.git
#   Target:           HEAD
#   Path:             helm-guestbook
# SyncWindow:         Sync Allowed
# Sync Policy:        Manual
# Sync Status:        Synced to HEAD (723b86e)
# Health Status:      Healthy

# GROUP  KIND        NAMESPACE  NAME                      STATUS  HEALTH   HOOK  MESSAGE
#        Service     default    guestbook-helm-guestbook  Synced  Healthy        service/guestbook-helm-guestbook created
# apps   Deployment  default    guestbook-helm-guestbook  Synced  Healthy        deployment.apps/guestbook-helm-guestbook created
```

---

## Specify Value

### Value File

```yaml
spec:
  source:
    helm:
      valueFiles:
        - values.yaml
```

---

#### Lab: Deploy Helm Charts with valueFiles

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: guestbook-valuefile
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/simonangel-fong/argocd-example-apps.git
    targetRevision: HEAD
    path: helm-guestbook
    helm:
      valueFiles:
        - values.yaml
  destination:
    server: "https://kubernetes.default.svc"
    namespace: default
```

```sh
kubectl apply -f guestbook-app-valuefile.yaml
# application.argoproj.io/guestbook-valuefile created

argocd app list
# NAME                        CLUSTER                         NAMESPACE  PROJECT  STATUS     HEALTH   SYNCPOLICY  CONDITIONS  REPO                                                        PATH            TARGET
# argocd/guestbook            https://kubernetes.default.svc  default    default  Synced     Healthy  Manual      <none>      https://github.com/simonangel-fong/argocd-example-apps.git  helm-guestbook  HEAD
# argocd/guestbook-valuefile  https://kubernetes.default.svc  default    default  OutOfSync  Missing  Manual      <none>      https://github.com/simonangel-fong/argocd-example-apps.git  helm-guestbook  HEAD

argocd app sync argocd/guestbook-valuefile
```

---

### Parameters

```yaml
spec:
  source:
    helm:
      parameters:
        - name: "replicaCount"
          value: "3"
```

#### Lab: Deploy Helm Charts with parameters

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: guestbook-app-parameters
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/simonangel-fong/argocd-example-apps.git
    targetRevision: HEAD
    path: helm-guestbook
    helm:
      # parameters
      parameters:
        - name: "replicaCount"
          value: "3"
  destination:
    server: "https://kubernetes.default.svc"
    namespace: default
```

```sh
kubectl apply -f guestbook-app-parameters.yaml
# application.argoproj.io/guestbook-app-parameters created

argocd app list
# NAME                             CLUSTER                         NAMESPACE  PROJECT  STATUS     HEALTH   SYNCPOLICY  CONDITIONS  REPO                                                        PATH            TARGET
# argocd/guestbook-app-parameters  https://kubernetes.default.svc  default    default  OutOfSync  Missing  Manual      <none>      https://github.com/simonangel-fong/argocd-example-apps.git  helm-guestbook  HEAD

argocd app sync argocd/guestbook-app-parameters --replace

kubectl get po
# NAME                                                      READY   STATUS    RESTARTS   AGE
# guestbook-app-parameters-helm-guestbook-78d98bb7b-79msz   1/1     Running   0          32s
# guestbook-app-parameters-helm-guestbook-78d98bb7b-k8pvm   1/1     Running   0          32s
# guestbook-app-parameters-helm-guestbook-78d98bb7b-z5b8j   1/1     Running   0          32s
```
