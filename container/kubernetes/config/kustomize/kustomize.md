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
  - [Imperative Command](#imperative-command)
  - [Lab: Kusomization](#lab-kusomization)
    - [configMapGenerator](#configmapgenerator)
    - [secretGenerator](#secretgenerator)
    - [generatorOptions](#generatoroptions)
    - [cross-cutting fields](#cross-cutting-fields)
    - [Composing](#composing)
    - [Customizing](#customizing)
    - [Update image](#update-image)
    - [`replacements` fiel: copy the value from a resource's field](#replacements-fiel-copy-the-value-from-a-resources-field)
  - [Bases and Overlays](#bases-and-overlays)
    - [Lab: Bases and Overlays](#lab-bases-and-overlays)
    - [Lab: Apply](#lab-apply)

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

---

## Imperative Command

| Command                        | Description                               |
| ------------------------------ | ----------------------------------------- |
| `kubectl kustomize`            | Build the current working directory       |
| `kubectl kustomize DIR_PATH`   | Build some shared configuration directory |
| `kubectl kustomize GITHUB_URL` | Build from github                         |

---

## Lab: Kusomization

### configMapGenerator

```sh
mkdir -pv kustomization
cd kustomization

# from regular file
cat <<EOF >application.properties
FOO=Bar
EOF

# from .env file
cat <<EOF >.env
FOO=Bar
EOF

cat <<EOF >./kustomization.yaml
configMapGenerator:
# from regular file
- name: demo-cm-1
  files:
  - application.properties

# from .env file
- name: demo-cm-2
  envs:
  - .env

# from literal kv paire
- name: demo-cm-3
  literals:
  - FOO=Bar
EOF

kubectl kustomize
# apiVersion: v1
# data:
#   application.properties: |
#     FOO=Bar
# kind: ConfigMap
# metadata:
#   name: demo-cm-1-g4hk9g2ff8
# ---
# apiVersion: v1
# data:
#   FOO: Bar
# kind: ConfigMap
# metadata:
#   name: demo-cm-2-42cfbf598f
# ---
# apiVersion: v1
# data:
#   FOO: Bar
# kind: ConfigMap
# metadata:
#   name: demo-cm-3-42cfbf598f

```

---

- Generate and use CM

```sh
# regular file
cat <<EOF >application.properties
FOO=Bar
EOF

# resource file
cat <<EOF >deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-k-app
  labels:
    app: demo-k-app
spec:
  selector:
    matchLabels:
      app: demo-k-app
  template:
    metadata:
      labels:
        app: demo-k-app
    spec:
      containers:
      - name: app
        image: nginx
        volumeMounts:
        - name: config
          mountPath: /config
      volumes:
      - name: config
        configMap:
          name: demo-k-cm   # specify cm
EOF

# create cm
cat <<EOF >./kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
- deployment.yaml

configMapGenerator:
- name: demo-k-cm
  files:
  - application.properties
EOF

# build
kubectl kustomize
# apiVersion: v1
# data:
#   application.properties: |
#     FOO=Bar
# kind: ConfigMap
# metadata:
#   name: demo-k-cm-g4hk9g2ff8
# ---
# apiVersion: apps/v1
# kind: Deployment
# metadata:
#   labels:
#     app: demo-k-app
#   name: demo-k-app
# spec:
#   selector:
#     matchLabels:
#       app: demo-k-app
#   template:
#     metadata:
#       labels:
#         app: demo-k-app
#     spec:
#       containers:
#       - image: nginx
#         name: app
#         volumeMounts:
#         - mountPath: /config
#           name: config
#       volumes:
#       - configMap:
#           name: demo-k-cm-g4hk9g2ff8
#         name: config

```

---

### secretGenerator

- Create secret from file

```sh
# Create a password.txt file
cat <<EOF >./password.txt
username=admin
password=secret
EOF

# create secret from a file
cat <<EOF >./kustomization.yaml
secretGenerator:
- name: demo-secret-1
  files:
  - password.txt
EOF

# build
kubectl kustomize
# apiVersion: v1
# data:
#   password.txt: dXNlcm5hbWU9YWRtaW4KcGFzc3dvcmQ9c2VjcmV0Cg==
# kind: Secret
# metadata:
#   name: demo-secret-1-2kdd8ckcc7
# type: Opaque
```

- Create from literal value

```sh
cat <<EOF >./kustomization.yaml
secretGenerator:
- name: demo-secret-2
  literals:
  - username=admin
  - password=secret
EOF

# build
kubectl kustomize
# apiVersion: v1
# data:
#   password: c2VjcmV0
#   username: YWRtaW4=
# kind: Secret
# metadata:
#   name: demo-secret-2-8c5228dkb9
# type: Opaque
```

- Create and use secret

```sh
# Create a password.txt file
cat <<EOF >./password.txt
username=admin
password=secret
EOF

cat <<EOF >deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-k-secret
  labels:
    app: demo-k-secret
spec:
  selector:
    matchLabels:
      app: demo-k-secret
  template:
    metadata:
      labels:
        app: demo-k-secret
    spec:
      containers:
      - name: app
        image: nginx
        volumeMounts:
        - name: password
          mountPath: /secrets
      volumes:
      - name: password
        secret:
          secretName: demo-k-secret
EOF

cat <<EOF >./kustomization.yaml
resources:
- deployment.yaml
secretGenerator:
- name: demo-k-secret
  files:
  - password.txt
EOF
```

---

### generatorOptions

- disable suffix hash

```sh
cat <<EOF >./kustomization.yaml
configMapGenerator:
- name: demo-cm-3
  literals:
  - FOO=Bar
generatorOptions:
  disableNameSuffixHash: true
  labels:
    type: generated
  annotations:
    note: generated
EOF

kubectl kustomize ./
# apiVersion: v1
# data:
#   FOO: Bar
# kind: ConfigMap
# metadata:
#   annotations:
#     note: generated
#   labels:
#     type: generated
#   name: demo-cm-3
```

---

### cross-cutting fields

use cases for setting cross-cutting fields:

- setting the same `namespace` for all resources
- adding the same name `prefix` or `suffix`
- adding the same set of `labels`
- adding the same set of `annotations`

```sh
# Create resources
cat <<EOF >./deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
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
        image: nginx
EOF

# cross-cutting fields
cat <<EOF >./kustomization.yaml
resources:
- deployment.yaml

namespace: my-namespace
namePrefix: dev-
nameSuffix: "-001"
labels:
  - pairs:
      app: bingo
    includeSelectors: true
commonAnnotations:
  oncallPager: 800-555-1212
EOF

kubectl kustomize ./
# apiVersion: apps/v1
# kind: Deployment
# metadata:
#   annotations:
#     oncallPager: 800-555-1212
#   labels:
#     app: bingo
#   name: dev-nginx-deployment-001
#   namespace: my-namespace
# spec:
#   selector:
#     matchLabels:
#       app: bingo
#   template:
#     metadata:
#       annotations:
#         oncallPager: 800-555-1212
#       labels:
#         app: bingo
#     spec:
#       containers:
#       - image: nginx
#         name: nginx
```

---

### Composing

```sh
# Create a deployment.yaml file
cat <<EOF > deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-nginx
spec:
  selector:
    matchLabels:
      run: my-nginx
  replicas: 2
  template:
    metadata:
      labels:
        run: my-nginx
    spec:
      containers:
      - name: my-nginx
        image: nginx
        ports:
        - containerPort: 80
EOF

# Create a service.yaml file
cat <<EOF > service.yaml
apiVersion: v1
kind: Service
metadata:
  name: my-nginx
  labels:
    run: my-nginx
spec:
  ports:
  - port: 80
    protocol: TCP
  selector:
    run: my-nginx
EOF

# Create a kustomization.yaml composing them
cat <<EOF >./kustomization.yaml
resources:
- deployment.yaml
- service.yaml
EOF

kubectl kustomize ./
# apiVersion: v1
# kind: Service
# metadata:
#   labels:
#     run: my-nginx
#   name: my-nginx
# spec:
#   ports:
#   - port: 80
#     protocol: TCP
#   selector:
#     run: my-nginx
# ---
# apiVersion: apps/v1
# kind: Deployment
# metadata:
#   name: my-nginx
# spec:
#   replicas: 2
#   selector:
#     matchLabels:
#       run: my-nginx
#   template:
#     metadata:
#       labels:
#         run: my-nginx
#     spec:
#       containers:
#       - image: nginx
#         name: my-nginx
#         ports:
#         - containerPort: 80
```

---

### Customizing

- using the `patches` field
  - The target resource is matched using `group`, `version`, `kind`, and `name` fields from the `patch file`.

```sh
# Create a deployment.yaml file
cat <<EOF > deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-nginx
spec:
  selector:
    matchLabels:
      run: my-nginx
  replicas: 2
  template:
    metadata:
      labels:
        run: my-nginx
    spec:
      containers:
      - name: my-nginx
        image: nginx
        ports:
        - containerPort: 80
EOF

# Create a patch increase_replicas.yaml
cat <<EOF > increase_replicas.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-nginx
spec:
  replicas: 3
EOF

# Create another patch set_memory.yaml
cat <<EOF > set_memory.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-nginx
spec:
  template:
    spec:
      containers:
      - name: my-nginx
        resources:
          limits:
            memory: 512Mi
EOF

cat <<EOF >./kustomization.yaml
resources:
- deployment.yaml

patches:
  - path: increase_replicas.yaml
  - path: set_memory.yaml
EOF

# replicas: 3
# memory: 512Mi
kubectl kustomize ./
# apiVersion: apps/v1
# kind: Deployment
# metadata:
#   name: my-nginx
# spec:
#   replicas: 3
#   selector:
#     matchLabels:
#       run: my-nginx
#   template:
#     metadata:
#       labels:
#         run: my-nginx
#     spec:
#       containers:
#       - image: nginx
#         name: my-nginx
#         ports:
#         - containerPort: 80
#         resources:
#           limits:
#             memory: 512Mi
```

---

### Update image

```sh
cat <<EOF > deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-nginx
spec:
  selector:
    matchLabels:
      run: my-nginx
  replicas: 2
  template:
    metadata:
      labels:
        run: my-nginx
    spec:
      containers:
      - name: my-nginx
        image: nginx
        ports:
        - containerPort: 80
EOF

cat <<EOF >./kustomization.yaml
resources:
- deployment.yaml
images:
- name: nginx
  newName: my.image.registry/nginx
  newTag: "1.4.0"
EOF

kubectl kustomize ./
    # spec:
    #   containers:
    #   - image: my.image.registry/nginx:1.4.0
```

---

### `replacements` fiel: copy the value from a resource's field

```sh
# Create a deployment.yaml file (quoting the here doc delimiter)
cat <<'EOF' > deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-nginx
spec:
  selector:
    matchLabels:
      run: my-nginx
  replicas: 2
  template:
    metadata:
      labels:
        run: my-nginx
    spec:
      containers:
      - name: my-nginx
        image: nginx
        command: ["start", "--host", "MY_SERVICE_NAME_PLACEHOLDER"]
EOF

# Create a service.yaml file
cat <<EOF > service.yaml
apiVersion: v1
kind: Service
metadata:
  name: my-nginx
  labels:
    run: my-nginx
spec:
  ports:
  - port: 80
    protocol: TCP
  selector:
    run: my-nginx
EOF

cat <<EOF >./kustomization.yaml
namePrefix: dev-
nameSuffix: "-001"

resources:
- deployment.yaml
- service.yaml

replacements:
- source:
    kind: Service
    name: my-nginx
    fieldPath: metadata.name
  targets:
  - select:
      kind: Deployment
      name: my-nginx
    fieldPaths:
    - spec.template.spec.containers.0.command.2
EOF

kubectl kustomize ./
# apiVersion: v1
# kind: Service
# metadata:
#   labels:
#     run: my-nginx
#   name: dev-my-nginx-001      <==== source value
# spec:
#   ports:
#   - port: 80
#     protocol: TCP
#   selector:
#     run: my-nginx
# ---
# apiVersion: apps/v1
# kind: Deployment
# metadata:
#   name: dev-my-nginx-001
# spec:
#   replicas: 2
#   selector:
#     matchLabels:
#       run: my-nginx
#   template:
#     metadata:
#       labels:
#         run: my-nginx
#     spec:
#       containers:
#       - command:
#         - start
#         - --host
#         - dev-my-nginx-001      <==== replace value
#         image: nginx
#         name: my-nginx
```

---

## Bases and Overlays

- `base`
  - a directory with a `kustomization.yaml`, which contains a set of **resources** and associated **customization**.

- `overlay`
  - a directory with a `kustomization.yaml` that refers to other **kustomization directories** as its bases

### Lab: Bases and Overlays

```sh
# ##############################
# base 
# ##############################

# Create a directory to hold the base
mkdir base
# Create a base/deployment.yaml
cat <<EOF > base/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-nginx
spec:
  selector:
    matchLabels:
      run: my-nginx
  replicas: 2
  template:
    metadata:
      labels:
        run: my-nginx
    spec:
      containers:
      - name: my-nginx
        image: nginx
EOF

# Create a base/service.yaml file
cat <<EOF > base/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: my-nginx
  labels:
    run: my-nginx
spec:
  ports:
  - port: 80
    protocol: TCP
  selector:
    run: my-nginx
EOF

# Create a base/kustomization.yaml
cat <<EOF > base/kustomization.yaml
resources:
- deployment.yaml
- service.yaml
EOF

# ##############################
# overlay
# ##############################
mkdir dev
cat <<EOF > dev/kustomization.yaml
resources:
- ../base
namePrefix: dev-
EOF

mkdir prod
cat <<EOF > prod/kustomization.yaml
resources:
- ../base
namePrefix: prod-
EOF

# ##############################
# build
# ##############################
kubectl kustomize ./dev
# kind: Service
# metadata:
#   name: dev-my-nginx
# ---
# kind: Deployment
# metadata:
#   name: dev-my-nginx

kubectl kustomize ./prod
# kind: Service
# metadata:
#   name: prod-my-nginx
# ---
# kind: Deployment
# metadata:
#   name: prod-my-nginx

```

---

### Lab: Apply

```sh
# Create a deployment.yaml file
cat <<EOF > deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-nginx
spec:
  selector:
    matchLabels:
      run: my-nginx
  replicas: 2
  template:
    metadata:
      labels:
        run: my-nginx
    spec:
      containers:
      - name: my-nginx
        image: nginx
        ports:
        - containerPort: 80
EOF

# Create a kustomization.yaml
cat <<EOF >./kustomization.yaml
resources:
- deployment.yaml

namePrefix: dev-
labels:
  - pairs:
      app: my-nginx
    includeSelectors: true 
EOF

# ##############################
# Apply
# ##############################
kubectl apply -k ./
# deployment.apps/dev-my-nginx created

# confirm
kubectl get -k ./
# NAME           READY   UP-TO-DATE   AVAILABLE   AGE
# dev-my-nginx   2/2     2            2           2m8s

kubectl describe -k ./
# Name:                   dev-my-nginx
# Labels:                 app=my-nginx
# Pod Template:
#   Labels:  app=my-nginx
#            run=my-nginx

kubectl diff -k ./

kubectl delete -k ./
# deployment.apps "dev-my-nginx" deleted
```
