# Helm Chart - Go Templates

[Back](../index.md)

- [Helm Chart - Go Templates](#helm-chart---go-templates)
  - [Go Templates](#go-templates)
  - [Built-in Objects](#built-in-objects)
    - [Lab: Go template - Object](#lab-go-template---object)
      - [Create Helm Chart](#create-helm-chart)
      - [Built-in Object](#built-in-object)
  - [Values file](#values-file)
    - [Lab: Values File](#lab-values-file)
  - [Variables](#variables)
  - [Functions \& Pipelines](#functions--pipelines)
    - [Lab: Functions](#lab-functions)
    - [Lab: list \& dict](#lab-list--dict)

---

## Go Templates

- `$`: the root scope
- `.`: current scope
- `# <comment>`: yaml comment, remains in manifest
- `{{- }}`: special characters to tell the template engine to chomp whitespace.
- `{{/* */}}`: go template comment, not show in manifestas, but render as an empty line
- `{{- /* */}}`: go template comment, not show in manifests.

---

## Built-in Objects

- `Objects` are passed into a template from the `template engine`.

| Common Object  | Description                                                                              |
| -------------- | ---------------------------------------------------------------------------------------- |
| `Release`      | the object describes the release                                                         |
| `Values`       | Values passed into the template from `templates/values.yaml` file or user-supplied files |
| `Chart`        | The contents of the `Chart.yaml` file.                                                   |
| `Subcharts`    | provides access to the scope of **subcharts to the parent**.                             |
| `Files`        | This provides access to all non-special files in a chart.                                |
| `Capabilities` | information about what capabilities the Kubernetes cluster supports.                     |
| `Template`     | information about the current template that is being executed                            |

### Lab: Go template - Object

#### Create Helm Chart

```sh
mkdir -pv mychart
# mkdir: created directory 'mychart'

helm create mychart
# Creating mychart

# remove templates
rm -rf mychart/templates/*
```

- `mychart/templates/configmap.yaml`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  myvalue: "Hello World"
```

```sh
# no specific release name
helm template mychart
# ---
# # Source: mychart/templates/configmap.yaml
# apiVersion: v1
# kind: ConfigMap
# metadata:
#   name: release-name-configmap
# data:
#   myvalue: "Hello World"

# with specific release name
helm template my-helm-chart ./mychart
# ---
# # Source: mychart/templates/configmap.yaml
# apiVersion: v1
# kind: ConfigMap
# metadata:
#   name: my-helm-chart-configmap
# data:
#   myvalue: "Hello World"

# debug and dry-run
helm install --debug --dry-run goodly-guppy ./mychart
# install.go:225: 2026-06-09 12:34:49.010997935 -0400 EDT m=+0.705199683 [debug] Original chart version: ""
# install.go:242: 2026-06-09 12:34:49.011457844 -0400 EDT m=+0.705659593 [debug] CHART PATH: /home/ubuntuadmin/mychart

# NAME: goodly-guppy
# LAST DEPLOYED: Tue Jun  9 12:34:49 2026
# NAMESPACE: default
# STATUS: pending-install
# REVISION: 1
# TEST SUITE: None
# USER-SUPPLIED VALUES:
# {}

# COMPUTED VALUES:
# affinity: {}
# autoscaling:
#   enabled: false
#   maxReplicas: 100
#   minReplicas: 1
#   targetCPUUtilizationPercentage: 80
# fullnameOverride: ""
# httpRoute:
#   annotations: {}
#   enabled: false
#   hostnames:
#   - chart-example.local
#   parentRefs:
#   - name: gateway
#     sectionName: http
#   rules:
#   - matches:
#     - path:
#         type: PathPrefix
#         value: /headers
# image:
#   pullPolicy: IfNotPresent
#   repository: nginx
#   tag: ""
# imagePullSecrets: []
# ingress:
#   annotations: {}
#   className: ""
#   enabled: false
#   hosts:
#   - host: chart-example.local
#     paths:
#     - path: /
#       pathType: ImplementationSpecific
#   tls: []
# livenessProbe:
#   httpGet:
#     path: /
#     port: http
# nameOverride: ""
# nodeSelector: {}
# podAnnotations: {}
# podLabels: {}
# podSecurityContext: {}
# readinessProbe:
#   httpGet:
#     path: /
#     port: http
# replicaCount: 1
# resources: {}
# securityContext: {}
# service:
#   port: 80
#   type: ClusterIP
# serviceAccount:
#   annotations: {}
#   automount: true
#   create: true
#   name: ""
# tolerations: []
# volumeMounts: []
# volumes: []

# HOOKS:
# MANIFEST:
# ---
# # Source: mychart/templates/configmap.yaml
# apiVersion: v1
# kind: ConfigMap
# metadata:
#   name: goodly-guppy-configmap
# data:
#   myvalue: "Hello World"
```

---

#### Built-in Object

- `mychart/templates/configmap.yaml`

```yaml
# mychart/templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  releaseName: {{ .Release.Name }}
  releaseNamespace: {{ .Release.Namespace }}
  releaseIsUpgrade: {{ .Release.IsUpgrade }}
  releaseIsInstall: {{ .Release.IsInstall }}
  releaseRevision: {{ .Release.Revision }}
  releaseService: {{ .Release.Service }}
  chartName: {{ .Chart.Name }}
  chartVersion : {{ .Chart.Version }}
  chartKubeVersion : {{ .Chart.KubeVersion }}
  chartAppVersion : {{ .Chart.AppVersion }}
  capabilitiesKubeVersion : {{ .Capabilities.KubeVersion }}
  capabilitiesKubeVersionMajor : {{ .Capabilities.KubeVersion.Major }}
  capabilitiesKubeVersionMinor : {{ .Capabilities.KubeVersion.Minor }}
  capabilitiesHelmVersion : {{ .Capabilities.HelmVersion }}
```

```sh
helm template builtin-obj ./mychart
# ---
# # Source: mychart/templates/configmap.yaml
# # mychart/templates/configmap.yaml
# apiVersion: v1
# kind: ConfigMap
# metadata:
#   name: builtin-obj-configmap
# data:
#   releaseName: builtin-obj
#   releaseNamespace: default
#   releaseIsUpgrade: false
#   releaseIsInstall: true
#   releaseRevision: 1
#   releaseService: Helm
#   chartName: mychart
#   chartVersion : 0.1.0
#   chartKubeVersion :
#   chartAppVersion : 1.16.0
#   capabilitiesKubeVersion : v1.35.0
#   capabilitiesKubeVersionMajor : 1
#   capabilitiesKubeVersionMinor : 35
#   capabilitiesHelmVersion : {v3.20.0 b2e4314fa0f229a1de7b4c981273f61d69ee5a59 clean go1.25.6}
```

---

## Values file

### Lab: Values File

- edit `./mychart/values.yaml`

```yaml
# mychart/values.yaml
favorite:
  drink: coffee
  food: pizza
```

- `mychart/templates/configmap.yaml`

```yaml
# mychart/templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  myvalue: "Hello World"
  drink: {{ .Values.favorite.drink }}
  food: {{ .Values.favorite.food }}
```

- Ingress values

```sh
helm template geared-marsupi ./mychart
# ---
# # Source: mychart/templates/configmap.yaml
# apiVersion: v1
# kind: ConfigMap
# metadata:
#   name: geared-marsupi-configmap
# data:
#   myvalue: "Hello World"
#   drink: coffee
#   food: pizza

# set value
helm template geared-marsupi ./mychart --set favorite.food=salad --set favorite.drink=tea
# ---
# # Source: mychart/templates/configmap.yaml
# apiVersion: v1
# kind: ConfigMap
# metadata:
#   name: geared-marsupi-configmap
# data:
#   myvalue: "Hello World"
#   drink: tea
#   food: salad
```

- Remove an entry: remove food
  - set entry value = null

```sh
helm template geared-marsupi ./mychart --set favorite.food=null
# ---
# # Source: mychart/templates/configmap.yaml
# apiVersion: v1
# kind: ConfigMap
# metadata:
#   name: geared-marsupi-configmap
# data:
#   myvalue: "Hello World"
#   drink: coffee
#   food:
```

---

## Variables

- Syntax:
  - define and assign value: `{{ $<varName> := <value>`
  - assign value: `{{ $<varName> = <value>`
  - call: `entry: {{ $<varName> }}`

```yaml
# mychart/templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  {{- $relname := "my release" }}
  release: {{ $relname | quote }}
```

```sh
helm template geared-marsupi ./mychart
# ---
# # Source: mychart/templates/configmap.yaml
# # mychart/templates/configmap.yaml
# apiVersion: v1
# kind: ConfigMap
# metadata:
#   name: geared-marsupi-configmap
# data:
#   release: "my release"
```

---

## Functions & Pipelines

- Functions
  - syntax
    - `functionName arg1 arg2...`
- operators: `eq`, `ne`, `lt`, `gt`, and, `or`
- Function List: https://helm.sh/docs/chart_template_guide/function_list/

---

- Pipelines: `|`
  - a tool for **chaining** together a series of template commands to compactly express a series of transformations.

---

### Lab: Functions

```yaml
# mychart/values.yaml
favorite:
  drink: coffee
  food: pizza
  dessert: pudding
```

- `mychart/templates/configmap.yaml`

```yaml
# mychart/templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  myvalue: "Hello World"
  drink: {{ .Values.favorite.drink | quote }}
  food: {{ .Values.favorite.food | upper | quote }}
  dessert: {{ .Values.favorite.dessert | repeat 5 | quote }}
  appetizer: {{ .Values.favorite.appetizer | default "chicken nugget" | quote }}
```

```sh
helm template geared-marsupi ./mychart
# ---
# # Source: mychart/templates/configmap.yaml
# apiVersion: v1
# kind: ConfigMap
# metadata:
#   name: geared-marsupi-configmap
# data:
#   myvalue: "Hello World"
#   drink: "coffee"
#   food: "PIZZA"
#   dessert: "puddingpuddingpuddingpuddingpudding"
#   appetizer: "chicken nugget"
```

---

### Lab: list & dict

- `mychart/templates/configmap.yaml`

```yaml
# mychart/templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  myList:
    values:
      example: {{ list "a" "b" "c" | toYaml | nindent 6 }}
  myDict: {{ dict "str" "myStr" "int" "myInt" | toYaml | nindent 4 }}
```

```sh
helm template geared-marsupi ./mychart
# ---
# # Source: mychart/templates/configmap.yaml
# # mychart/templates/configmap.yaml
# apiVersion: v1
# kind: ConfigMap
# metadata:
#   name: geared-marsupi-configmap
# data:
#   myList:
#     values:
#       example:
#       - a
#       - b
#       - c
#   myDict:
#     int: myInt
#     str: myStr
```

---
