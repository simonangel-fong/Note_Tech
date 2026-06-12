# Kubernetes Tool - HELM

[Back](../../index.md)

- [Kubernetes Tool - HELM](#kubernetes-tool---helm)
  - [Helm](#helm)
    - [Common chart files](#common-chart-files)
    - [Lifecycle Management](#lifecycle-management)
  - [Imperative Command](#imperative-command)

---

## Helm

- `Helm chart`
  - a package for Kubernetes that bundles together all the resource definitions and configurations needed to run an application.
  - a package manager for k8s

- `helm cli`
  - the utility to execute helm operations.
- `chart`
  - a **collection of files** that contain the instruction in the k8s
- `release`
  - a **single installation** of an application
  - created when a chart is applied to k8s cluster.
  - can use one chart to create multiple releases
  - can use release name to track each release

- `revision`
  - the **snapshot** of the **application**
  - created when a change is made to the application
- `repository`
  - a hub to store charts, can be public or private.
  - multiple repos are available
    - Appscode
    - TrueCharts
    - Bitnami
    - Community Operators
  - all repos are listed on `ArtifactHub.io`
- `metadata`
  - a place where store the data of the cluster.
  - commonly is saved as k8s secrets in the cluster.

- `templating`:
  - to pass value to chart file

---

### Common chart files

- `values.yaml`: define values to be used in the charts
- `Chart.yaml`: contains information about the chart itself
  - e.g., api version, app version
  - 2 types of chart:
    - application, default type
    - library
- Common file structure
  - project/
    - charts/: dependency charts
    - templates/
    - Chart.yaml
    - values.yaml
    - README.md

---

### Lifecycle Management

- release is created when `helm install`
  - indepently from each other by release name

- upgrade a release to a new revision
  - `helm upgrade nginx-release bitnami/nginx`
  - `helm history nginx-release`: show the app history

- Rollback a release to the revision 1
  - `helm rollback nginx-release 1`
  - note: only rollback the cluster object, not the data, like user data.

---

## Imperative Command

- Helm configuration

| Command        | Description                                                        |
| -------------- | ------------------------------------------------------------------ |
| `helm env`     | Prints out information about the local Helm environment variables. |
| `helm version` | Shows the installed version of the Helm client.                    |



---
