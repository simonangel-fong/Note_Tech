# Helm Chart

[Back](../index.md)

- [Helm Chart](#helm-chart)
  - [Imperative Command](#imperative-command)
  - [Content of a Helm Chart](#content-of-a-helm-chart)
    - [`Chart.yaml`](#chartyaml)
    - [`values.yaml`](#valuesyaml)
    - [`README.md`](#readmemd)
    - [`LICENSE`](#license)
    - [`.helmignore`](#helmignore)
    - [`charts/` directory](#charts-directory)
    - [`templates/` directory](#templates-directory)
      - [`tests/` directory](#tests-directory)
      - [`NOTES.txt`](#notestxt)
      - [`_helpers.tpl`](#_helperstpl)
  - [Lab: Create Custom Helm Chart](#lab-create-custom-helm-chart)

---

## Imperative Command

- Chart Management (Local Development)

| Command                            | Description                                                       |
| ---------------------------------- | ----------------------------------------------------------------- |
| `helm create DIR`                  | Create a new directory with the **default chart template** files. |
| `helm lint DIR`                    | Examines a chart for possible issues and best practices.          |
| `helm template DIR`                | Render chart templates locally and display the output.            |
| `helm template RELEASE REPO/CHART` | Render chart templates locally and display the output.            |
| `helm package DIR`                 | Bundles the chart directory into a versioned .tgz archive file.   |

## Content of a Helm Chart

- Common manifests in a chart

```txt
|_ Chart.yaml
|_ values.yaml
|_ README.md
|_ LICENSE
|_ .helmignore
|_ charts/
|_ templates/
 |_ deploy.yaml
 |_ svc.yaml
 |_ ingress.yaml
 |_ <others>.yaml
 |_ NOTES.txt
 |_ _helpers.tpl
```

---

### `Chart.yaml`

- `Chart.yaml`
  - A YAML file containing **metadata** about the chart.
- key entries:
  - `apiVersion`: The chart API version (v1 or v2). For Helm 3, use `v2`.
  - `name`: The name of the chart.
  - `version`: The version of the chart (uses semantic versioning).
  - `appVersion`: The version of the application enclosed (not Helm itself).
  - `description`: A brief description of the chart.
  - `type`: Type of chart (e.g., application or library).
  - `keywords`: A list of keywords representative of the project.
  - `dependencies`: A list of other charts that the current chart depends on.

---

### `values.yaml`

- `values.yaml`
  - A YAML file containing **default values** for the chart.
  - It's recommended to leverage the `values.yaml` file as much as possible to **avoid hard-coding configuration** into the chart.
  - may be overridden by users during `helm install` or `helm upgrade`.

---

### `README.md`

- `README.md`
  - Provides a **human-readable documentation** file that should contain:
    - A high-level description of the application the chart provides.
    - Prerequisites, requirements, and setup needed to run the chart.
    - Descriptions of options in values.yaml and default values.
    - Other relevant information for chart installation, configuration, or upgrade.

---

### `LICENSE`

- `LICENSE`
  - A plain text file containing the license for the chart (and chart applications, if relevant).

---

### `.helmignore`

- `.helmignore`
  - Used to **ignore** paths when packaging the chart (for example, local development files).

---

### `charts/` directory

- Contains any **chart dependencies** (subcharts).
- These dependencies should be informed in the `Chart.yaml` file, and will be downloaded and saved locally.
- When `Helm` evaluates a chart, it will **send all of the files** in the `templates/` directory through the `template rendering engine`.
  - It then collects the results of those templates and **sends them on to Kubernetes**.

---

### `templates/` directory

- This directory contains multiple files that are relevant for Helm projects, including the multiple Kubernetes manifest templates that are rendered by Helm.

#### `tests/` directory

- Contains tests to be executed when running the helm test command.

#### `NOTES.txt`

- Its contents are printed on the screen upon successful chart installation or upgrade.

#### `_helpers.tpl`

- Contains `template helper functions`, which can be used to reduce duplication.
- Files preceded with an underscore are not included in the final rendering from Helm.

---

## Lab: Create Custom Helm Chart

```sh
mkdir -vp nginx/templates

touch nginx/values.yaml

tee nginx/Chart.yaml<<EOF
apiVersion: v2
name: nginx
description: A helm chart to deploy nginx
type: application
version: 0.1.0
# version of nginx
appVersion: 1.27.0
EOF

tee nginx/templates/deployment.yaml<<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
    name: nginx
    labels:
        app: nginx
spec:
    replicas: 1
    selector:
        matchLabels:
            app: nginx
    template:
        metadata:
            labels:
                app: nginx

        spec:
            containers:
                - name: nginx
                  image: nginx:1.27.0
                  ports:
                    - containerPort: 80

EOF

tee nginx/templates/service.yaml<<EOF
apiVersion: v1
kind: Service
metadata:
    name: nginx-svc
    labels:
        app: nginx
spec:
    type: ClusterIP
    selector:
        app: nginx
    ports:
        - protocol: TCP
          port: 80
          targetPort: 80
EOF

tee nginx/templates/.helmignore<<EOF
.env*
.DS_Store*
.git/
EOF

# render template
helm template nginx

# lint check
helm lint nginx
# ==> Linting nginx
# [INFO] Chart.yaml: icon is recommended

# 1 chart(s) linted, 0 chart(s) failed

# install
helm install local-nginx nginx
# NAME: local-nginx
# LAST DEPLOYED: Mon Jun  8 20:13:24 2026
# NAMESPACE: default
# STATUS: deployed
# REVISION: 1
# TEST SUITE: None

helm list
# NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
# local-nginx     default         1               2026-06-08 20:13:24.354677159 -0400 EDT deployed        nginx-0.1.0     1.27.0

kubectl get po
# NAME                     READY   STATUS    RESTARTS   AGE
# nginx-5577b67f4c-7wg5m   1/1     Running   0          37s

helm uninstall local-nginx
# release "local-nginx" uninstalled
```
