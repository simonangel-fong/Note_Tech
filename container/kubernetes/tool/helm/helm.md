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

| CMD                                    | DESC                              |
| -------------------------------------- | --------------------------------- |
| `helm search hub chart_name `          | Search for chart on the hub       |
| `helm repo add bitnami repo_url`       | Add a repo                        |
| `helm install release_name chart_name` | Deploy application to the cluster |
| `helm list`                            | List all release                  |
| `helm unistall chart_name`             | remove an application             |

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
