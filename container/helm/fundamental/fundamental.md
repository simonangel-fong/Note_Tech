# Helm Chart - Fundamental

[Back](../index.md)

---

## Helm Chart

- challenges by kubernetes:
  - managing everything in individual YAML files quickly gets overwhelming.
  - Human Error: Manually ensuring each resource is configured correctly is challenging
  - Environment Configuration Overload:
    - Managing different configurations can lead to repetitive
  - Version Control and Rollbacks
    - Maintaining version history for each YAML file is challenging
    - there’s no straightforward way to revert to a previous stat

- `Helm`
  - a package manager
    - apt for Debian, yum for RedHat, brew for MacOS, or npm for NodeJS.
  - allows to **define, install, and upgrade** applications containing multiple Kubernetes resources with a single command.

- Features:
  - **Package** multiple Kubernetes manifests (called `templates`) **into a single chart**.
  - **Deploy, update** and manage all the manifests from a chart with a single command.
  - Thoroughly **customize** the templates with Go templating features and custom **values files**.
  - Create and leverage **reusable charts** available either publicly or privately.
  - Leverage charts for **versioning** your application.
  - Easily automate **testing** your charts with Helm hooks and the helm CLI.

---

- Benefits and Limitations

---

## Helm vs. Kustomize

| Dimension       | Helm                                                                              | Kustomize                                                                            |
| --------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Overall purpose | Package manager, support templating, dependency management, and versioning        | Customize existing manifests by overlaying changes                                   |
| Complexity      | More complex, Go templates, structure of charts                                   | Simpler,native YAML                                                                  |
| Customization   | Full templating system(conditionals, loops, functions, and variable substitution) | merge patches, JSON patches, name prefixes/suffixes, common labels, and annotations. |

- Helm Use-cases:
  - Packaging and managing applications and their dependencies
  - Versioning of applications
  - More advanced customizations via templates and values files.
- Kustomize:
  - Managing environment-specific customizations (e.g., dev, staging, prod)
  - Applying patches and modifications without duplicating YAML

---

## Lab: Helm vs Kustomize

customize the image tag

- Helm

```yaml
# values.yaml
replicaCount: 5
image:
  tag: latest

# deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: { { .Release.Name } }
spec:
  replicas: { { .Values.replicaCount } }
  selector:
    matchLabels:
      app: { { .Release.Name } }
    template:
      metadata:
        labels:
          app: { { .Release.Name } }
      spec:
      containers:
        - name: { { .Chart.Name } }
          image: "nginx:{{ .Values.image.tag }}"
          ports:
            - containerPort: 80
```

---

- Kustomize

```yaml
# kustomaziation.yaml
# merge patches
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 5
  template:
  spec:
    containers:
      - name: nginx
        image: nginx:latest

# base.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
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
```

---

## Architecture

- `Helm Cli`
  - the command-line interface tool used to interact with `Helm`, the package manager for Kubernetes.
  - interact with `k8s API` to **install, test, update, uninstall** charts

- `Release`
  - a named installation of a Helm chart
  - By default, Helm 3 stores its `release state` inside Kubernetes cluster as `Kubernetes Secrets`.

- `Chart files`
  - a structured directory of files used to package and deploy Kubernetes applications
  - translates dynamic configurations into standard Kubernetes manifests using the Go templating language.
- common structure:

```txt
  |_ Chart.yaml
  |_ .helmignore
  |_ values.yaml
  |_ README.md
  |_ charts/
  |_ templates/
   |_ NOTES.txt
   |_ _helpers.tpl
   |_ <template>.yaml
```

- `Helm chart repository`
  - a centralized storage and distribution hub used to publish, version, and share packaged Kubernetes applications
  - a collection of `.tgz` files + index file
    - can be public and private
  - `cli`
    - push and pull charts to remote repository
    - cache locally, `repo add`, `repo update`

---

## Package Helm Chart

| Command                        | Description                                 |
| ------------------------------ | ------------------------------------------- |
| `helm package <chart_path>`    | Packages a chart into a chart archive file. |
| `helm repo index <chart_path>` | generate an index file `index.yaml`         |
