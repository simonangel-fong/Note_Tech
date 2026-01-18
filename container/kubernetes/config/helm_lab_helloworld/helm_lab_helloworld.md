# `helm chart` Lab: hello world

[Back](../../index.md)

- [`helm chart` Lab: hello world](#helm-chart-lab-hello-world)
  - [Lab: hello world](#lab-hello-world)
    - [Create Charts](#create-charts)
    - [`helm template`: output all manifest](#helm-template-output-all-manifest)
    - [`helm template`: output all manifest with values](#helm-template-output-all-manifest-with-values)
    - [Install Release from Chart](#install-release-from-chart)
    - [Update Release with values](#update-release-with-values)
    - [Update Release with changed charts](#update-release-with-changed-charts)
    - [Rollback - Previous verion](#rollback---previous-verion)
    - [Rollback - a specific verion](#rollback---a-specific-verion)
    - [Uninstall Release](#uninstall-release)

---

## Lab: hello world

### Create Charts

```sh
# create a helm chart
helm create helloworld
# Creating helloworld

ls
# helloworld

ls -alh helloworld
total 32K
# drwxr-xr-x 4 ubuntuadmin ubuntuadmin 4.0K Jan 17 23:54 .
# drwxrwxr-x 3 ubuntuadmin ubuntuadmin 4.0K Jan 17 23:54 ..
# drwxr-xr-x 2 ubuntuadmin ubuntuadmin 4.0K Jan 17 23:54 charts
# -rw-r--r-- 1 ubuntuadmin ubuntuadmin 1.2K Jan 17 23:54 Chart.yaml
# -rw-r--r-- 1 ubuntuadmin ubuntuadmin  349 Jan 17 23:54 .helmignore
# drwxr-xr-x 3 ubuntuadmin ubuntuadmin 4.0K Jan 17 23:54 templates
# -rw-r--r-- 1 ubuntuadmin ubuntuadmin 5.2K Jan 17 23:54 values.yaml

ls -alh helloworld/templates
# total 44K
# drwxr-xr-x 3 ubuntuadmin ubuntuadmin 4.0K Jan 17 23:54 .
# drwxr-xr-x 4 ubuntuadmin ubuntuadmin 4.0K Jan 17 23:54 ..
# -rw-r--r-- 1 ubuntuadmin ubuntuadmin 2.4K Jan 17 23:54 deployment.yaml
# -rw-r--r-- 1 ubuntuadmin ubuntuadmin 1.8K Jan 17 23:54 _helpers.tpl
# -rw-r--r-- 1 ubuntuadmin ubuntuadmin 1000 Jan 17 23:54 hpa.yaml
# -rw-r--r-- 1 ubuntuadmin ubuntuadmin  959 Jan 17 23:54 httproute.yaml
# -rw-r--r-- 1 ubuntuadmin ubuntuadmin 1.1K Jan 17 23:54 ingress.yaml
# -rw-r--r-- 1 ubuntuadmin ubuntuadmin 2.8K Jan 17 23:54 NOTES.txt
# -rw-r--r-- 1 ubuntuadmin ubuntuadmin  395 Jan 17 23:54 serviceaccount.yaml
# -rw-r--r-- 1 ubuntuadmin ubuntuadmin  370 Jan 17 23:54 service.yaml
# drwxr-xr-x 2 ubuntuadmin ubuntuadmin 4.0K Jan 17 23:54 tests

ls -alh helloworld/templates/tests/
# total 12K
# drwxr-xr-x 2 ubuntuadmin ubuntuadmin 4.0K Jan 17 23:54 .
# drwxr-xr-x 3 ubuntuadmin ubuntuadmin 4.0K Jan 17 23:54 ..
# -rw-r--r-- 1 ubuntuadmin ubuntuadmin  388 Jan 17 23:54 test-connection.yaml

```

---

### `helm template`: output all manifest

```sh
helm template helloworld
# ---
# # Source: helloworld/templates/serviceaccount.yaml
# apiVersion: v1
# kind: ServiceAccount
# metadata:
#   name: release-name-helloworld
#   labels:
#     helm.sh/chart: helloworld-0.1.0
#     app.kubernetes.io/name: helloworld
#     app.kubernetes.io/instance: release-name
#     app.kubernetes.io/version: "1.16.0"
#     app.kubernetes.io/managed-by: Helm
# automountServiceAccountToken: true
# ---
# # Source: helloworld/templates/service.yaml
# apiVersion: v1
# kind: Service
# metadata:
#   name: release-name-helloworld
#   labels:
#     helm.sh/chart: helloworld-0.1.0
#     app.kubernetes.io/name: helloworld
#     app.kubernetes.io/instance: release-name
#     app.kubernetes.io/version: "1.16.0"
#     app.kubernetes.io/managed-by: Helm
# spec:
#   type: NodePort
#   ports:
#     - port: 80
#       targetPort: http
#       protocol: TCP
#       name: http
#   selector:
#     app.kubernetes.io/name: helloworld
#     app.kubernetes.io/instance: release-name
# ---
# # Source: helloworld/templates/deployment.yaml
# apiVersion: apps/v1
# kind: Deployment
# metadata:
#   name: release-name-helloworld
#   labels:
#     helm.sh/chart: helloworld-0.1.0
#     app.kubernetes.io/name: helloworld
#     app.kubernetes.io/instance: release-name
#     app.kubernetes.io/version: "1.16.0"
#     app.kubernetes.io/managed-by: Helm
# spec:
#   replicas: 1
#   selector:
#     matchLabels:
#       app.kubernetes.io/name: helloworld
#       app.kubernetes.io/instance: release-name
#   template:
#     metadata:
#       labels:
#         helm.sh/chart: helloworld-0.1.0
#         app.kubernetes.io/name: helloworld
#         app.kubernetes.io/instance: release-name
#         app.kubernetes.io/version: "1.16.0"
#         app.kubernetes.io/managed-by: Helm
#     spec:
#       serviceAccountName: release-name-helloworld
#       containers:
#         - name: helloworld
#           image: "nginx:1.16.0"
#           imagePullPolicy: IfNotPresent
#           ports:
#             - name: http
#               containerPort: 80
#               protocol: TCP
#           livenessProbe:
#             httpGet:
#               path: /
#               port: http
#           readinessProbe:
#             httpGet:
#               path: /
#               port: http
# ---
# # Source: helloworld/templates/tests/test-connection.yaml
# apiVersion: v1
# kind: Pod
# metadata:
#   name: "release-name-helloworld-test-connection"
#   labels:
#     helm.sh/chart: helloworld-0.1.0
#     app.kubernetes.io/name: helloworld
#     app.kubernetes.io/instance: release-name
#     app.kubernetes.io/version: "1.16.0"
#     app.kubernetes.io/managed-by: Helm
#   annotations:
#     "helm.sh/hook": test
# spec:
#   containers:
#     - name: wget
#       image: busybox
#       command: ['wget']
#       args: ['release-name-helloworld:80']
#   restartPolicy: Never
```

---

### `helm template`: output all manifest with values

```sh
helm template helloworld --set image.tag=1.28.1
# ---
# # Source: helloworld/templates/serviceaccount.yaml
# apiVersion: v1
# kind: ServiceAccount
# metadata:
#   name: release-name-helloworld
#   labels:
#     helm.sh/chart: helloworld-0.1.0
#     app.kubernetes.io/name: helloworld
#     app.kubernetes.io/instance: release-name
#     app.kubernetes.io/version: "1.16.0"
#     app.kubernetes.io/managed-by: Helm
# automountServiceAccountToken: true
# ---
# # Source: helloworld/templates/service.yaml
# apiVersion: v1
# kind: Service
# metadata:
#   name: release-name-helloworld
#   labels:
#     helm.sh/chart: helloworld-0.1.0
#     app.kubernetes.io/name: helloworld
#     app.kubernetes.io/instance: release-name
#     app.kubernetes.io/version: "1.16.0"
#     app.kubernetes.io/managed-by: Helm
# spec:
#   type: NodePort
#   ports:
#     - port: 80
#       targetPort: http
#       protocol: TCP
#       name: http
#   selector:
#     app.kubernetes.io/name: helloworld
#     app.kubernetes.io/instance: release-name
# ---
# # Source: helloworld/templates/deployment.yaml
# apiVersion: apps/v1
# kind: Deployment
# metadata:
#   name: release-name-helloworld
#   labels:
#     helm.sh/chart: helloworld-0.1.0
#     app.kubernetes.io/name: helloworld
#     app.kubernetes.io/instance: release-name
#     app.kubernetes.io/version: "1.16.0"
#     app.kubernetes.io/managed-by: Helm
# spec:
#   replicas: 1
#   selector:
#     matchLabels:
#       app.kubernetes.io/name: helloworld
#       app.kubernetes.io/instance: release-name
#   template:
#     metadata:
#       labels:
#         helm.sh/chart: helloworld-0.1.0
#         app.kubernetes.io/name: helloworld
#         app.kubernetes.io/instance: release-name
#         app.kubernetes.io/version: "1.16.0"
#         app.kubernetes.io/managed-by: Helm
#     spec:
#       serviceAccountName: release-name-helloworld
#       containers:
#         - name: helloworld
#           image: "nginx:1.28.1"
#           imagePullPolicy: IfNotPresent
#           ports:
#             - name: http
#               containerPort: 80
#               protocol: TCP
#           livenessProbe:
#             httpGet:
#               path: /
#               port: http
#           readinessProbe:
#             httpGet:
#               path: /
#               port: http
# ---
# # Source: helloworld/templates/tests/test-connection.yaml
# apiVersion: v1
# kind: Pod
# metadata:
#   name: "release-name-helloworld-test-connection"
#   labels:
#     helm.sh/chart: helloworld-0.1.0
#     app.kubernetes.io/name: helloworld
#     app.kubernetes.io/instance: release-name
#     app.kubernetes.io/version: "1.16.0"
#     app.kubernetes.io/managed-by: Helm
#   annotations:
#     "helm.sh/hook": test
# spec:
#   containers:
#     - name: wget
#       image: busybox
#       command: ['wget']
#       args: ['release-name-helloworld:80']
#   restartPolicy: Never
```

---

### Install Release from Chart

```sh
# install: helm install release_name chart_path
helm install my-hello-world helloworld
# NAME: my-hello-world
# LAST DEPLOYED: Sun Jan 18 10:51:55 2026
# NAMESPACE: default
# STATUS: deployed
# REVISION: 1
# NOTES:
# 1. Get the application URL by running these commands:
#   export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=helloworld,app.kubernetes.io/instance=my-hello-world" -o jsonpath="{.items[0].metadata.name}")
#   export CONTAINER_PORT=$(kubectl get pod --namespace default $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
#   echo "Visit http://127.0.0.1:8080 to use your application"
#   kubectl --namespace default port-forward $POD_NAME 8080:$CONTAINER_PORT

# confirm
helm list
# NAME            NAMESPACE       REVISION        UPDATED                                 STATUS   CHART                    APP VERSION
# my-hello-world  default         1               2026-01-18 10:51:55.803398815 -0500 EST deployed helloworld-0.1.0         1.16.0

kubectl get deploy -o wide
# NAME                        READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS      IMAGES                     SELECTOR
# my-hello-world-helloworld   1/1     1            1           13s   helloworld      nginx:1.16.0               app.kubernetes.io/instance=my-hello-world,app.kubernetes.io/name=helloworld

kubectl get svc
# NAME                        TYPE           CLUSTER-IP    EXTERNAL-IP   PORT(S)                      AGE
# my-hello-world-helloworld   ClusterIP      10.99.7.0     <none>        80/TCP                       115s

```

---

### Update Release with values

```sh
helm upgrade my-hello-world helloworld --set image.tag=1.28.1
# Release "my-hello-world" has been upgraded. Happy Helming!
# NAME: my-hello-world
# LAST DEPLOYED: Sun Jan 18 11:30:31 2026
# NAMESPACE: default
# STATUS: deployed
# REVISION: 2

helm get values my-hello-world
# USER-SUPPLIED VALUES:
# image:
#   tag: 1.28.1

helm history my-hello-world
# REVISION        UPDATED                         STATUS          CHART                   APP VERSION       DESCRIPTION
# 1               Sun Jan 18 11:28:05 2026        superseded      helloworld-0.1.0        1.16.0            Install complete
# 2               Sun Jan 18 11:30:31 2026        deployed        helloworld-0.1.0        1.16.0            Upgrade complete

# confirm
kubectl get deploy my-hello-world-helloworld -o wide
# NAME                        READY   UP-TO-DATE   AVAILABLE   AGE    CONTAINERS   IMAGES         SELECTOR
# my-hello-world-helloworld   1/1     1            1           3m8s   helloworld   nginx:1.28.1   app.kubernetes.io/instance=my-hello-world,app.kubernetes.io/name=helloworld
```

---

### Update Release with changed charts

```sh
vi helloworld/values.yaml
# update:
# service:
#   type: NodePort

# upgrade
helm upgrade my-hello-world helloworld
# Release "my-hello-world" has been upgraded. Happy Helming!
# NAME: my-hello-world
# LAST DEPLOYED: Sun Jan 18 11:32:48 2026
# NAMESPACE: default
# STATUS: deployed
# REVISION: 3

helm history my-hello-world
# REVISION        UPDATED                         STATUS          CHART                   APP VERSION       DESCRIPTION
# 1               Sun Jan 18 11:28:05 2026        superseded      helloworld-0.1.0        1.16.0            Install complete
# 2               Sun Jan 18 11:30:31 2026        superseded      helloworld-0.1.0        1.16.0            Upgrade complete
# 3               Sun Jan 18 11:32:48 2026        deployed        helloworld-0.1.0        1.16.0            Upgrade complete

# confirm
kubectl get svc
# NAME                        TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
# my-hello-world-helloworld   NodePort       10.101.98.181   <none>        80:31813/TCP                 5m17s
```

---

### Rollback - Previous verion

```sh
helm history my-hello-world
# REVISION        UPDATED                         STATUS          CHART                   APP VERSION       DESCRIPTION
# 1               Sun Jan 18 11:28:05 2026        superseded      helloworld-0.1.0        1.16.0            Install complete
# 2               Sun Jan 18 11:30:31 2026        superseded      helloworld-0.1.0        1.16.0            Upgrade complete
# 3               Sun Jan 18 11:32:48 2026        deployed        helloworld-0.1.0        1.16.0            Upgrade complete

# rollback previous version
helm rollback my-hello-world 0
# Rollback was a success! Happy Helming!

helm history my-hello-world
# REVISION        UPDATED                         STATUS          CHART                   APP VERSION       DESCRIPTION
# 1               Sun Jan 18 11:28:05 2026        superseded      helloworld-0.1.0        1.16.0            Install complete
# 2               Sun Jan 18 11:30:31 2026        superseded      helloworld-0.1.0        1.16.0            Upgrade complete
# 3               Sun Jan 18 11:32:48 2026        superseded      helloworld-0.1.0        1.16.0            Upgrade complete
# 4               Sun Jan 18 11:34:01 2026        deployed        helloworld-0.1.0        1.16.0            Rollback to 2

# confirm: svc type == clusterip
kubectl get svc
# NAME                        TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
# my-hello-world-helloworld   ClusterIP      10.101.98.181   <none>        80/TCP                       6m31s
```

---

### Rollback - a specific verion

```sh
helm history my-hello-world
# REVISION        UPDATED                         STATUS          CHART                   APP VERSION       DESCRIPTION
# 1               Sun Jan 18 11:28:05 2026        superseded      helloworld-0.1.0        1.16.0            Install complete
# 2               Sun Jan 18 11:30:31 2026        superseded      helloworld-0.1.0        1.16.0            Upgrade complete
# 3               Sun Jan 18 11:32:48 2026        superseded      helloworld-0.1.0        1.16.0            Upgrade complete
# 4               Sun Jan 18 11:34:01 2026        deployed        helloworld-0.1.0        1.16.0            Rollback to 2

# rollback the 1st version
helm rollback my-hello-world 1
# Rollback was a success! Happy Helming!

helm history my-hello-world
# REVISION        UPDATED                         STATUS          CHART                   APP VERSION       DESCRIPTION
# 1               Sun Jan 18 11:28:05 2026        superseded      helloworld-0.1.0        1.16.0            Install complete
# 2               Sun Jan 18 11:30:31 2026        superseded      helloworld-0.1.0        1.16.0            Upgrade complete
# 3               Sun Jan 18 11:32:48 2026        superseded      helloworld-0.1.0        1.16.0            Upgrade complete
# 4               Sun Jan 18 11:34:01 2026        superseded      helloworld-0.1.0        1.16.0            Rollback to 2
# 5               Sun Jan 18 11:35:22 2026        deployed        helloworld-0.1.0        1.16.0            Rollback to 1

# confirm: svc type == clusterIP
kubectl get svc my-hello-world-helloworld
# NAME                        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
# my-hello-world-helloworld   ClusterIP   10.101.98.181   <none>        80/TCP    7m38s

# confirm: nginx=1.16.0
kubectl get deploy -o wide
# NAME                        READY   UP-TO-DATE   AVAILABLE   AGE    CONTAINERS      IMAGES                     SELECTOR
# my-hello-world-helloworld   1/1     1            1           8m1s   helloworld      nginx:1.16.0               app.kubernetes.io/instance=my-hello-world,app.kubernetes.io/name=helloworld
```

---

### Uninstall Release

```sh
helm list -a -A
# NAME            NAMESPACE       REVISION        UPDATED                                 STATUS   CHART                    APP VERSION
# my-hello-world  default         1               2026-01-18 10:29:33.508777192 -0500 EST deployed helloworld-0.1.0         1.16.0

helm uninstall my-hello-world
# release "my-hello-world" uninstalled

# confirm
helm list -a -A
```

---
