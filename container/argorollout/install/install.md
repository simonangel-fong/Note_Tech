# Argo Rollout - Install

[Back](../index.md)

- [Argo Rollout - Install](#argo-rollout---install)
  - [Installation - Argo Rollout](#installation---argo-rollout)
  - [Installation - Argo Rollout CLI](#installation---argo-rollout-cli)

---

## Installation - Argo Rollout

- ref:
  - doc: https://argo-rollouts.readthedocs.io/en/stable/installation/
  - release: https://github.com/argoproj/argo-rollouts/releases
  - helm: https://artifacthub.io/packages/helm/argo/argo-rollouts

```sh
kubectl create namespace argo-rollouts

# add repo
helm repo add argo https://argoproj.github.io/argo-helm

# search for chart
helm search repo argo rollout
# NAME                    CHART VERSION   APP VERSION     DESCRIPTION
# argo/argo-rollouts      2.40.9          v1.9.0          A Helm chart for Argo Rollouts

helm upgrade --install argo-rollouts argo/argo-rollouts --version 2.40.9 --install --namespace argo-rollouts --create-namespace --set podSecurityContext.runAsNonRoot=false --set dashboard.enabled=true --set dashboard.podSecurityContext.runAsNonRoot=false
# Release "argo-rollouts" does not exist. Installing it now.
# NAME: argo-rollouts
# LAST DEPLOYED: Wed May  6 19:32:02 2026
# NAMESPACE: argo-rollouts
# STATUS: deployed
# REVISION: 1
# TEST SUITE: None

helm list -n argo-rollouts
# NAME            NAMESPACE       REVISION        UPDATED                                 STATUS   CHART                    APP VERSION
# argo-rollouts   argo-rollouts   1               2026-05-06 19:32:02.754726963 -0400 EDT deployed argo-rollouts-2.40.9     v1.9.0

kubectl get po -n argo-rollouts
# NAME                                       READY   STATUS    RESTARTS   AGE
# argo-rollouts-54c5897f5b-6vhtf             1/1     Running   0          6m14s
# argo-rollouts-54c5897f5b-s8l95             1/1     Running   0          6m14s
# argo-rollouts-dashboard-64d9f854c9-nwdmp   1/1     Running   0          6m14s
```

- Enable dashboard

```sh
kubectl argo rollouts dashboard
# or
kubectl port-forward service/argo-rollouts-dashboard 31000:3100 -n argo-rollouts
```

---

## Installation - Argo Rollout CLI

- ref:
  - https://github.com/argoproj/argo-rollouts/releases
- WSL

```sh
curl -LO https://github.com/argoproj/argo-rollouts/releases/download/v1.9.0/kubectl-argo-rollouts-linux-amd64
chmod +x ./kubectl-argo-rollouts-linux-amd64
sudo mv ./kubectl-argo-rollouts-linux-amd64 /usr/local/bin/kubectl-argo-rollouts

# Test to ensure the version
kubectl argo rollouts version
# kubectl-argo-rollouts: v1.9.0+838d4e7
#   BuildDate: 2026-03-20T21:08:11Z
#   GitCommit: 838d4e792be666ec11bd0c80331e0c5511b5010e
#   GitTreeState: clean
#   GoVersion: go1.24.13
#   Compiler: gc
#   Platform: linux/amd64

```
