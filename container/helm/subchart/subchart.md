# Helm Chart - Subchart

[Back](../index.md)

- [Helm Chart - Subchart](#helm-chart---subchart)
  - [Subchart](#subchart)
  - [Imperative Commands](#imperative-commands)
  - [Declear dependency](#declear-dependency)
    - [Conditionally enable subchart](#conditionally-enable-subchart)
  - [Passing values from parent](#passing-values-from-parent)
  - [including template from subchart](#including-template-from-subchart)

---

## Subchart

- `subchart` / `chart dependency`
  - allow to **include and manage** the deployment of **other charts** alongside own.
  - another chart that is either:
    - Required for the chart to function properly.
    - Necessary to enable optional functionality in the **installed application**.

- use case:
  - **Databases**:
    - Including a database chart (e.g., MySQL, PostgreSQL) that the application depends on.
  - **Shared Services**:
    - Including **common services** used across multiple applications.
  - **Common Utilities**:
    - Including a library of functions or utilities to support Chart development
- placed under the `charts/` folder
  - either be a **folder** containing all the required Chart files
  - or the `tar` file of an already existing chart.

- `Subcharts` listed **without a repository** must contain **all required files** and be a **valid** Helm chart.
- `Subcharts` can be **conditionally enabled** either via boolean values or tags.

- `Chart.lock` file
  - an **auto-generated dependency lock file** for Helm charts.
  - records the **exact versions** of all `sub-charts` (dependencies) the current chart relies on, along with a cryptographic digest, to ensure deployments are perfectly reproducible across different environments.

---

- Sample

```yaml
apiVersion: v2
name: deps-demo
description: Illustrate deps
type: application
version: 0.1.0
appVersion: "1.16.0"

dependencies:
  - name: mongodb
    version: 16.2.1
    repository: <repo URL>
```

---

## Imperative Commands

| Command                              | Description                                                                    |
| ------------------------------------ | ------------------------------------------------------------------------------ |
| `helm dependency list <chart dir>`   | Shows the installed dependencies for a specific chart                          |
| `helm dependency update <chart dir>` | Updates the `Chart.lock` file. Downloads and saves the dependencies tar files. |
| `helm dependency build <chart dir>`  | Downloads and saves the dependencies `tar` files.                              |

- `helm dependency build`: Fails if the informed version in the `Chart.yaml` is different from the `Chart.lock` file.

---

## Declear dependency

chart

### Conditionally enable subchart
method 1: condition key
method 2: tag key

## Passing values from parent

## including template from subchart


