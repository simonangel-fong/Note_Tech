# Helm - Repository & Hub

[Back](../index.md)

- [Helm - Repository \& Hub](#helm---repository--hub)
  - [Helm Repository](#helm-repository)
  - [Imperative Command](#imperative-command)
  - [Lab: Repo Management](#lab-repo-management)
    - [Add repo](#add-repo)
    - [Show info](#show-info)

---

## Helm Repository

- `Helm Repository`
  - registry used to store and share Kubernetes applications

- Key files in repo:
  - `index.yaml`
    - the metadata file catalogs the charts, their versions, and their download URLs.
  - Chart Archives:
    - Charts are stored as compressed `.tgz` files and hosted on a **standard HTTP/HTTPS server** or an **OCI-based registry**.

- Types of Helm Repositories
  - HTTP/HTTPS Web Servers (Traditional)
    - Basic **web servers** (e.g., NGINX, Apache) or cloud **storage buckets** (Amazon S3, Google Cloud Storage) serving static files.
    - connect via a web URL and pull down the index.yaml catalog
  - OCI-Compatible Registries (Modern Standard)
    - Container registries supporting the `Open Container Initiative (OCI)`.
    - charts are pushed and pulled like standard container images using `oci://` URIs

- Artifact Hub:
  - The central public registry where community-maintained charts are hosted.
  - url: https://artifacthub.io/

---

## Imperative Command

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
