# Kubernetes Tool - HELM

[Back](../../index.md)

- [Kubernetes Tool - HELM](#kubernetes-tool---helm)
  - [Helm](#helm)
    - [Common chart files](#common-chart-files)
    - [Lifecycle Management](#lifecycle-management)
    - [Install helm](#install-helm)
  - [Imperative Command](#imperative-command)
  - [Lab: Repo Management](#lab-repo-management)
    - [Add repo](#add-repo)
    - [Show info](#show-info)

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

### Install helm

- Windows

```sh
choco install kubernetes-helm
```

- Ubuntu

```sh
sudo apt-get install curl gpg apt-transport-https --yes
curl -fsSL https://packages.buildkite.com/helm-linux/helm-debian/gpgkey | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/helm.gpg] https://packages.buildkite.com/helm-linux/helm-debian/any/ any main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
```

---

## Imperative Command

- Helm configuration

| Command        | Description                                                        |
| -------------- | ------------------------------------------------------------------ |
| `helm env`     | Prints out information about the local Helm environment variables. |
| `helm version` | Shows the installed version of the Helm client.                    |

- Chart Management (Local Development)

| Command                            | Description                                                       |
| ---------------------------------- | ----------------------------------------------------------------- |
| `helm create DIR`                  | Create a new directory with the **default chart template** files. |
| `helm lint DIR`                    | Examines a chart for possible issues and best practices.          |
| `helm template DIR`                | Out the all manifest of a chart                                   |
| `helm template RELEASE REPO/CHART` | Out the all manifest of a repo's chart                            |
| `helm package DIR`                 | Bundles the chart directory into a versioned .tgz archive file.   |

- Install Release

| Command                                               | Description                                                  |
| ----------------------------------------------------- | ------------------------------------------------------------ |
| `helm install RELEASE REPO/CHART`                     | Install a release from a chart within a repo.                |
| `helm install RELEASE REPO/CHART --version VERSION`   | Install a release from a chart of a version.                 |
| `helm install RELEASE REPO/CHART --set key=val`       | Install a release from a chart within a repo and set values. |
| `helm install RELEASE REPO/CHART --values VALUE_YAML` | Install a release from a chart within a yaml file of values  |
| `helm install RELEASE CHART_DIR`                      | Install a release from a local chart.                        |
| `helm install RELEASE CHART_ZIP`                      | Install a release from a local zipped chart.                 |
| `helm install RELEASE REMOTE_URL`                     | Install a release from a remote url.                         |
| `helm install RELEASE CHART --repo REPO_URL`          | Install a release from a remote repo.                        |
| `helm install RELEASE CHART_DIR --dry-run=client`     | Output all generated chart manifests                         |
| `helm install RELEASE CHART_DIR --debug`              | Enable verbose output                                        |

- Release Management

| Command                                                | Description                                                          |
| ------------------------------------------------------ | -------------------------------------------------------------------- |
| `helm list`                                            | Lists all of the releases for current namespace                      |
| `helm list -a`                                         | Show all releases                                                    |
| `helm list -A`                                         | List releases across all namespaces                                  |
| `helm list -n NAMESPACE`                               | List releases for a specific namespaces                              |
| `helm list -f 'ara[a-z]+'`                             | Filter releases                                                      |
| `helm list -l STRING`                                  | Filter by labels                                                     |
| `helm status RELEASE`                                  | Displays the real-time state of a deployed release.                  |
| `helm get values RELEASE`                              | Shows the specific values (--set or values.yaml) used for a release. |
| `helm history RELEASE`                                 | Lists the revision history of a specific release.                    |
| `helm upgrade RELEASE CHART_DIR`                       | Upgrade release from a local chart                                   |
| `helm upgrade RELEASE RELEASE/CHART`                   | Upgrade release from repo chart                                      |
| `helm upgrade RELEASE RELEASE/CHART --version=VERSION` | Upgrade release to a version from repo chart                         |
| `helm rollback RELEASE VERSION`                        | Reverts a release to a specific previous revision.                   |
| `helm uninstall RELEASE`                               | Removes all resources associated with a release from the cluster.    |

- Repository Management

| Command                     | Description                                                           |
| --------------------------- | --------------------------------------------------------------------- |
| `helm search repo REPO`     | Searches added repositories for specific charts.                      |
| `helm search hub KEYWORD `  | Search for Helm charts in the Hub                                     |
| `helm repo list`            | List chart repositories                                               |
| `helm repo add REPO URL`    | Connects local Helm client to a remote chart repository.              |
| `helm repo update`          | Gets the latest information of all charts                             |
| `helm repo update REPO`     | Gets the latest information of a chart                                |
| `helm repo index CHART_DIR` | Create an index file given a directory containing packaged charts     |
| `helm repo remove REPO`     | Remove one or more chart repositories                                 |
| `helm pull`                 | Downloads a chart from a remote repository to current path.           |
| `helm pull --untar`         | Downloads and unzip a chart from a remote repository to current path. |

- repo info

| CMD                           | DESC                              |
| ----------------------------- | --------------------------------- |
| `helm show all REPO/CHART`    | show all information of the chart |
| `helm show chart REPO/CHART`  | show the chart's definition       |
| `helm show crds REPO/CHART`   | show the chart's CRDs             |
| `helm show values REPO/CHART` | show the chart's values           |
| `helm show readme REPO/CHART` | show the chart's README           |
| `helm show readme REPO/CHART` | show the chart's README           |
| `helm get values RELEASE`     | get the release value             |

---

## Lab: Repo Management

### Add repo

```sh
helm repo add traefik https://traefik.github.io/charts
# "traefik" has been added to your repositories

helm repo update
# Hang tight while we grab the latest from your chart repositories...
# ...Successfully got an update from the "traefik" chart repository
# Update Complete. ⎈Happy Helming!⎈

helm repo list
# NAME    URL
# traefik https://traefik.github.io/charts

helm search repo traefik
# NAME                    CHART VERSION   APP VERSION     DESCRIPTION
# traefik/traefik         38.0.2          v3.6.6          A Traefik based Kubernetes ingress controller
# traefik/traefik-crds    1.13.1                          A Traefik based Kubernetes ingress controller
# traefik/traefik-hub     4.2.0           v2.11.0         Traefik Hub Ingress Controller
# traefik/traefik-mesh    4.1.1           v1.4.8          Traefik Mesh - Simpler Service Mesh
# traefik/traefikee       4.2.5           v2.12.5         Traefik Enterprise is a unified cloud-native ne...
# traefik/maesh           2.1.2           v1.3.2          Maesh - Simpler Service Mesh

# download
helm pull traefik/traefik

ls -lh traefik-38.0.2.tgz
# -rw-r--r-- 1 ubuntuadmin ubuntuadmin 294K Jan 18 17:43 traefik-38.0.2.tgz
```

---

### Show info

```sh
helm show chart traefik/traefik
# annotations:
#   artifacthub.io/changes: |
#     - "revert(CRDs): use Traefik Hub v3.18.0 compatible crds"
#     - "fix(security): set the seccomp profile to RuntimeDefault"
#     - "fix(CRDs): enforce the fact that this Chart does not support Traefik Hub v3.19.0"
#     - "feat(deps): update traefik docker tag to v3.6.6"
#     - "chore(release): publish traefik 38.0.2 and crds 1.13.1"
# apiVersion: v2
# appVersion: v3.6.6
# description: A Traefik based Kubernetes ingress controller
# home: https://traefik.io/
# icon: https://raw.githubusercontent.com/traefik/traefik/master/docs/content/assets/img/traefik.logo.png
# keywords:
# - traefik
# - ingress
# - networking
# kubeVersion: '>=1.22.0-0'
# maintainers:
# - email: michel.loiseleur@traefik.io
#   name: mloiseleur
# - email: remi.buisson@traefik.io
#   name: darkweaver87
# - name: jnoordsij
# name: traefik
# sources:
# - https://github.com/traefik/traefik-helm-chart
# - https://github.com/traefik/traefik
# type: application
# version: 38.0.2

# show crd
helm show crds traefik/traefik

# show values
helm show values traefik/traefik

# show readme
helm show readme traefik/traefik

```
