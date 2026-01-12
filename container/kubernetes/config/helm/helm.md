# Kubernetes Tool - HELM

[Back](../../index.md)

- [Kubernetes Tool - HELM](#kubernetes-tool---helm)
  - [Helm](#helm)
  - [Install helm](#install-helm)
  - [Components](#components)
  - [Release](#release)
  - [Repo](#repo)
  - [Chart](#chart)
  - [Helm CLI](#helm-cli)
  - [Customizing Chart Parameters](#customizing-chart-parameters)
  - [Lifecycle Management](#lifecycle-management)
  - [Lab: Install Traefik](#lab-install-traefik)
    - [Repo](#repo-1)
    - [Install Application](#install-application)
    - [Remove App](#remove-app)
    - [Chart info](#chart-info)

---

## Helm

- `Helm chart`
  - a package for Kubernetes that bundles together all the resource definitions and configurations needed to run an application.
  - a package manager for k8s

---

## Install helm

- Windows??

```sh
choco install kubernetes-helm
```

- Ubuntu\

```sh
sudo apt-get install curl gpg apt-transport-https --yes
curl -fsSL https://packages.buildkite.com/helm-linux/helm-debian/gpgkey | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/helm.gpg] https://packages.buildkite.com/helm-linux/helm-debian/any/ any main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm
```

---

## Components

- `helm cli`
  - the utility to execute helm operations.
- `chart`
  - a collection of files that contain the instruction in the k8s
- `release`
  - a single installation of an application
  - created when a chart is applied to k8s cluster.
- `revision`
  - the snapshot of the application
  - created when a change is made to the application
- `repository`
  - a hub to store charts, can be public or private.
- `metadata`
  - a place where store the data of the cluster.
  - commonly is saved as k8s secrets in the cluster.

---

## Release

- can use on chart to create multiple releases
  - can use release name to track each release

---

## Repo

- multiple repos are available

  - Appscode
  - TrueCharts
  - Bitnami
  - Community Operators

- all repos are listed on `ArtifactHub.io`

---

## Chart

- `templating`:
  - to pass value to chart file
  - Example

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: hello-world
spec:
  type: NodePort
  ports:
    - port: 80
      targetPort: http
      protocol: TCP
      name: http
  selector:
    app: hello-world
```

```yaml
# deployment.yaml
apiVersion: app/v1
kind: Deployment
metadata:
  name: hello-world
spec:
  replicas: { { .vlues.replicaCount } }
  selector:
    matchLabels:
      app: hello-world
  template:
    metadata:
      labels:
        app: hello-world
    spec:
      containers:
        - name: nginx
          image: { { .values.image.repository } }
          ports:
            - name: http
              containerPort: 80
              protocol: TCP
```

```yaml
# values.yaml
replicaCount: 1
image:
  repository: nginx
```

---

- Common chart files
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

## Helm CLI

- Repo

| CMD                         | DESC                                         |
| --------------------------- | -------------------------------------------- |
| `helm search hub KEYWORD `  | Search for Helm charts in the Hub            |
| `helm search repo KEYWORD ` | Search for chart in the local repo           |
| `helm repo add REPO URL`    | Add a chart repository from url              |
| `helm repo list`            | List chart repositories                      |
| `helm repo update`          | Gets the latest information of all charts    |
| `helm repo update REPO`     | Gets the latest information of a chart       |
| `helm repo remove REPO`     | Remove one or more chart repositories        |
| `helm pull REPO/CHART`      | Retrieve a package from a package repository |
| `helm push REPO`            | Upload a chart to a registry.                |

- info

| CMD                           | DESC                              |
| ----------------------------- | --------------------------------- |
| `helm show all REPO/CHART`    | show all information of the chart |
| `helm show chart REPO/CHART`  | show the chart's definition       |
| `helm show crds REPO/CHART`   | show the chart's CRDs             |
| `helm show values REPO/CHART` | show the chart's values           |
| `helm show readme REPO/CHART` | show the chart's README           |
| `helm show readme REPO/CHART` | show the chart's README           |
| `helm get values RELEASE`     | get the release value             |

- Release

| CMD                                              | DESC                                            |
| ------------------------------------------------ | ----------------------------------------------- |
| `helm list`                                      | Lists all of the releases for current namespace |
| `helm list -a`                                   | Show all releases                               |
| `helm list -A`                                   | List releases across all namespaces             |
| `helm list -n NAMESPACE`                         | List releases for a specific namespaces         |
| `helm list -f 'ara[a-z]+'`                       | Filter releases                                 |
| `helm list -l STRING`                            | Filter by labels                                |
| `helm install -f YAML_FILE APP_NAME`             | Install an app with yaml file                   |
| `helm install APP_NAME REPO/CHART`               | Install app from repo                           |
| `helm install APP_NAME DIR`                      | Install app from a dir                          |
| `helm install APP_NAME URL`                      | Install app from an url                         |
| `helm install --repo URL APP_NAME`               | Install app from a repo url                     |
| `helm install --set key=val APP_NAME REPO/CHART` | Install app from repo and set values            |
| `helm unistall APP_NAME`                         | Remove an application                           |
| `helm show values REPO/CHART`                    | Show values of a repo                           |

---

## Customizing Chart Parameters

- Imerative method

```sh
helm install --set param1_name=param1_value release_name --set param2_name=param2_value release_name chart_name
```

---

- Declarative method

```yaml
# custom-values.yaml
param1_name: param1_value
param2_name: param2_value
```

- Apply the value file

```sh
helm install --values custom-values.yaml release_name chart_name
```

---

- Overwrite the app value file
  - pull from repo
  - overwrite file

```sh
# pull
helm pull bitnami/wordpress
helm pull --untar bitnami/wordpress #pull the untar files

ls wordpress
# overwrite values.yaml

# apply
helm install release_name ./wordpress
```

---

## Lifecycle Management

- release is created when `helm install`

  - indepently from each other by release name

- upgrade a release to a new revision

  - `helm upgrade nginx-release bitnami/nginx`
  - `helm history nginx-release`: show the app history

- Rollback a release to the revision 1
  - `helm rollback nginx-release 1`
  - note: only rollback the cluster object, not the data, like user data.

---

## Lab: Install Traefik

### Repo

```sh
helm search hub traefik

# add repo
helm repo add traefik https://traefik.github.io/charts
# "traefik" has been added to your repositories

helm repo update
# Hang tight while we grab the latest from your chart repositories...
# ...Successfully got an update from the "traefik" chart repository
# Update Complete. ⎈Happy Helming!⎈

# pull
helm pull traefik/traefik
```

---

### Install Application

```sh
# install with new ns
helm install traefik-app traefik/traefik -n traefik --create-namespace
# NAME: traefik-app
# LAST DEPLOYED: Sat Jan 10 14:45:23 2026
# NAMESPACE: traefik
# STATUS: deployed
# REVISION: 1
# TEST SUITE: None
# NOTES:
# traefik-app with docker.io/traefik:v3.6.6 has been deployed successfully on traefik namespace!

# confirm
helm list -A
# NAME            NAMESPACE       REVISION        UPDATED                                STATUS          CHART           APP VERSION
# traefik-app     traefik         1               2026-01-10 14:45:23.258773107 -0500 ESTdeployed        traefik-38.0.2  v3.6.6

```

---

### Remove App

```sh
helm uninstall traefik-app -n traefik
# release "traefik-app" uninstalled
```

---

### Chart info

```sh
# show all info
helm show all traefik/traefik

# show chart
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
