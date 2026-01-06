# Kubernetes Tool - Kustomize

[Back](../../index.md)

- [Kubernetes Tool - Kustomize](#kubernetes-tool---kustomize)
  - [Kustomize](#kustomize)
    - [vs helm](#vs-helm)
  - [Install](#install)
  - [kustomization.yaml file](#kustomizationyaml-file)
    - [Example](#example)
  - [Lab:](#lab)
  - [Common Transformer](#common-transformer)
    - [Image transformer](#image-transformer)
  - [Lab](#lab-1)
  - [Patches](#patches)
    - [Types of patch](#types-of-patch)
    - [JSON 6902 patch](#json-6902-patch)
    - [Strategic merge patch](#strategic-merge-patch)
  - [Overlays](#overlays)
  - [Components](#components)

---

## Kustomize

- Example Problem

  - one k8s app for multiple env:
    - dev, staging, prod

- Solution:
  - individual yaml files for each env
    - most of the codes are identical
    - few parameters dedicated to the env
    - drawback
      - unscalable: when the app scales, more files comes in, more duplicate code should be maintained
  - kustomized: one base + overlay
    - base config: identical codes and default config
    - overlay: customize parameters for each env

---

- Kustomize file structure
- project/
  - base/: share/default config
    - kustomization.yaml:
    - app.yaml:
  - overlays/: env specific config
    - dev/: env dir
      - kustomization.yaml
      - config-map.yaml: env specific param
    - stg/: env dir
      - kustomization.yaml
      - config-map.yaml: env specific param

---

- kustomize
  - built-in with kubectl

---

### vs helm

helm:

- a package manager for app
- use go templates to assign variables for vary environment
  - helm templates are not valid yaml
  - complex templates are hard to read
- provides extra features

  - conditional
  - loops
  - functions
  - hooks

- file structure
- project/
  - environments/
    - values.dev.yaml
    - values.stg.yaml
    - values.prod.yaml
  - templates/
    - nginx.yaml
    - nginx-service.yaml
    - db.yaml
    - db-service.yaml

---

kustomize:

- valid YAML files
- less features

---

## Install

```sh
# install: windows
choco install kustomize

# install linux
curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh"  | bash

# confirm
kustomize version
# v5.5.0
```

---

## kustomization.yaml file

- `kustomization.yaml`

  - the **central configuration** file used by Kustomize, a tool for customizing Kubernetes configurations.
  - as a **declarative blueprint** for how Kubernetes resources should be managed, customized, and layered without directly modifying the original YAML files.

- key components

```yaml
# k8s/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

# list of resources file
resources:
  - nginx.yaml
  - nginx-service.yaml

# list of customizations
commonLabels:
  company: abc
```

- build kustomize
  - combine all the manifests
  - not apply/deploy the k8s resources to a cluster

```sh
# build and output the config, not deploy
kustomize build k8s/

# apply the config built by kustomize
kustomize build k8s/ | kubectl apply -f -
kubectl apply -k k8s/

# delete the config built by kustomize
kustomize build k8s/ | kubectl delete -f -
kubectl delete -k k8s/
```

---

### Example

- file structure management
- k8s/: project dir
  - kustomization.yaml: central config files
  - api/
    - api-deploy.yaml
    - api-service.yaml
  - db/
    - db-deploy.yaml
    - db-service.yaml

---

- kustomization.yaml

```yaml
# k8s/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - api/api-deploy.yaml
  - api/api-service.yaml
  - db/db-deploy.yaml
  - db/db-service.yaml
```

- deploy

```sh
kubectl apply -k -f k8s/
```

---

- the app grow
- k8s/
  - kustomization.yaml
  - api/
    - kustomization.yaml
  - db/
    - kustomization.yaml
  - cache/
    - kustomization.yaml
  - kafka/
    - kustomization.yaml

---

- each subdir yaml file list the file within the dir

```yaml
# k8s/api/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - api/api-deploy.yaml
  - api/api-service.yaml
```

- a central yaml file list dir

```yaml
# k8s/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - api/
  - db/
  - cache/
```

- deploy

```sh
kubectl apply -k -f k8s/
```

---

## Lab:

---

## Common Transformer

- `Kustomize common transforms`

  - built-in functionalities in `kustomization.yaml` that apply consistent modifications **across all Kubernetes resources**

- root yaml vs subdir yaml
  - root: apply to all resources
  - subdir: apply only to resources defined within the subdir

| Common Transformer        | Desciption                                  |
| ------------------------- | ------------------------------------------- |
| `commonLabels`            | Adds specified labels to all resources.     |
| `namespace`               | Sets a default namespace for all resources. |
| `namePrefix`/`nameSuffix` | Prepends or appends text to resource names. |
| `commonAnnotations`       | Adds common annotations to all resources    |

---

### Image transformer

- `image Transformer`

  - Updates container image names and tags across deployments

- example:

```yaml
# kustomization.yaml
images:
  - name: nginx # the name of the image in template
    newName: haproxy # the name to apply
    newTag: "2.4" # the tag of the image to apply
```

```yaml
# web-deploy.yaml
spec:
  containers:
    - name: web
      image: nginx
```

---

## Lab

---

## Patches

- `patches`

  - a method that **surgically modify** base Kubernetes configurations without altering the original files,

- 3 parameters to create a patch:
  - operation:
    - add
    - remove
    - replace
  - target: the resource should the patch be applied on
    - kind
    - version/group
    - name
    - namespace
    - labelSelector
    - AnnnotaiontSelector
  - Value: the value to apply

---

- example

```yaml
# api-deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
spec:
  replicas: 1
```

- JSON 6902 Patch

```yaml
# kustomization.yaml
patches:
  # what target to apply
  - target:
      kind: Deployment
      name: api-deployment
    # inline patch: |-
    patch: |-
      - op: replace
        path: /metadata/name
        value: web-deployment
  - target:
      kind: Deployment
      name: api-deployment
    patch: |-
      - op: replace
        path: /spec/replicas
        value: 5
```

---

- Strategic merge patch

```yaml
patches:
  - path: |-
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: api-deployment
      spec:
        replicas: 5
```

---

### Types of patch

### JSON 6902 patch

- inline

```yaml
# kustomization.yaml
patches:
  - target:
      kind: Deployment
      name: api-deployment
    patch: |-
      - op: replace
        path: /metadata/name
        value: web-deployment
```

- separate file

```yaml
# kustomization.yaml
patches:
  - path: replica-patch.yaml
    target:
      king: Deployment
      name: nginx-deployment
```

```yaml
# replica-patch.yaml
- op: replace
  path: /spec/replicas
  value: 5
```

---

### Strategic merge patch

- inline

```yaml
# kustomization.yaml
patches:
  - path: |-
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: api-deployment
      spec:
        replicas: 5
```

- Separate file

```yaml
# kustomization.yaml
patches:
  - replica-patch.yaml
```

```yaml
# replica-patch.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
spec:
  replicas: 5
```

---

- Patch on a dictionary in yaml file

  - add
  - replace
  - remove

- Patch on a list in yaml file
  - add
  - replace
  - remove

---

## Overlays

- use to patch the value in the base
- can also include new resources in the env
  - include the yaml in the resources field of the env kustomization.yaml file

---

- Example

```yaml
# k8s/base/kustomization.yaml

resources:
  - nginx-deploy.yaml
```

```yaml
# k8s/base/nginx-deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 1
```

```yaml
# k8s/overlays/dev/kustomization.yaml
bases:
  - ../../base

patch: |-
  - op: replace
    patch: /spec/replicas
    value: 2
```

---

## Components

- `Components`

  - the **reusable, modular chunks** of Kubernetes **configuration (resources + patches)** that you can easily enable, disable, or mix into different environments (overlays) without duplicating code,
  - subset of overlays
    - the reusable config that
      - not common for all overlays,
        - if it is, it should be in the base
      - but common for subset of overlays
        - e.g., external db for the overlays stg and prod, but not in the dev overlay

- file structure:
- project/
  - base/
    - kustomization.yaml
    - api-deploy.yaml
  - components/
    - db/
      - kustomization.yaml
      - postgres-deploy.yaml
      - api-deploy-patch.yaml
  - overlays/
    - dev/
      - kustomization.yaml
    - stg/
      - kustomization.yaml
    - prod/
      - kustomization.yaml

---

```yaml
# components/db/kustomization.yaml
apiVersion: kustomize.config.k8s/v1alpha1
kind: Component

resources:
  - postgres-deploy.yaml

secreGenerator:
  - name: postgres-crd
    literals:
      - password=postgres123

patches:
  - deploy-patch.yaml
```

```yaml
# api-deploy-patch.yaml
apiVersion: apps/v1
# update the pgdb pwd in the patch for the api-deploy
```

---

- Import the component

```yaml
# overlays/dev/kustomization.yaml
bases:
  - ../../base

components:
  - ../../components/db
```
