# Helm Chart - Go Templates: Named Template

[Back](../index.md)

- [Helm Chart - Go Templates: Named Template](#helm-chart---go-templates-named-template)
  - [Named Templates](#named-templates)
    - [`define` and `template` function](#define-and-template-function)
    - [Lab: define and template](#lab-define-and-template)
    - [`include` function](#include-function)
    - [Lab: include with `_helper.tpl`](#lab-include-with-_helpertpl)

---

## Named Templates

- `named template` (partial or a subtemplate)
  - a template defined inside of a file, and given a name.
  - template names are **global**.
    - If you declare two templates with the **same name**, whichever one is **loaded last** will be the one used.

- naming convention
  - prefix each defined template with the name of the chart
  - `{{ define "mychart.labels" }}`

### `define` and `template` function

```yaml
{{- define "MY.NAME" }}
  # body of template here
{{- end }}

{{- template "MY.NAME" }}
```

---

### Lab: define and template

```yaml
# mychart/templates/configmap.yaml
{{- define "mychart.labels" }}
{{- printf "%s-%s" .Release.Name   }}
  labels:
    generator: helm
    date: {{ now | htmlDate }}
{{- end }}

apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
  {{- template "mychart.labels" }}
data:
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
#   labels:
#     generator: helm
#     date: 2026-06-09
# data:
```

> can be moved to the file \_helpers.tpl.

---

### `include` function

- solve the indentation issue
  - the following cannot `template` as indentation error
  - use include + nindent

```yaml
# mychart/templates/configmap.yaml
{{- define "mychart.app" -}}
app_name: {{ .Chart.Name }}
app_version: "{{ .Chart.Version }}"
{{- end -}}

apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
  labels:
    {{- include "mychart.app" . | nindent 4 }}
data:
  myvalue: "Hello World"
  {{- range $key, $val := .Values.favorite }}
  {{ $key }}: {{ $val | quote }}
  {{- end }}
  {{- include "mychart.app" . | nindent 2 }}
```

```sh
helm template geared-marsupi ./mychart
# ---
# # Source: mychart/templates/configmap.yaml
# # mychart/templates/configmap.yamlapiVersion: v1
# kind: ConfigMap
# metadata:
#   name: geared-marsupi-configmap
#   labels:
#     app_name: mychart
#     app_version: "0.1.0"
# data:
#   myvalue: "Hello World"
#   drink: "coffee"
#   food: "pizza"
#   app_name: mychart
#   app_version: "0.1.0"
```

---

### Lab: include with `_helper.tpl`

```tpl
{{- define "mychart.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}


{{- define "mychart.labels" -}}
managed-by: helm
chart: {{ .Chart.Name }}
release: {{ .Release.Name }}
date: {{ now | htmlDate }}
{{- end -}}
```

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: { { include "mychart.fullname" . } }
  labels: { { include "mychart.labels" . | nindent 4 } }
data:
```

```sh
helm template demo-named-template ./go_template
# ---
# # Source: go-template/templates/sanbox.yaml
# apiVersion: v1
# kind: ConfigMap
# metadata:
#   name: demo-named-template-go-template
#   labels:
#     managed-by: helm
#     chart: go-template
#     release: demo-named-template
#     date: 2026-06-09
# data:
```
