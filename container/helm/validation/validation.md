# Helm Chart - Go Templates: Validation Function

[Back](../index.md)

- [Helm Chart - Go Templates: Validation Function](#helm-chart---go-templates-validation-function)
  - [Validation Function](#validation-function)
  - [Lab: `fail`](#lab-fail)
    - [Valid](#valid)
    - [Invalid](#invalid)
  - [Lab: `required`](#lab-required)
    - [Valid values](#valid-values)
    - [invalid values](#invalid-values)
    - [Assign directly to the entry](#assign-directly-to-the-entry)
  - [Custom Validation](#custom-validation)
    - [Lab: Custom Validation](#lab-custom-validation)
    - [Options: Group validator at the top](#options-group-validator-at-the-top)

---

## Validation Function

- `required`:
  - Specify values that must be set with required:

```yaml
{ { - required "A valid foo is required!" .Bar } }
```

- If .Bar is empty or not defined (see default on how this is evaluated), the template will **not render** and will return the error message supplied instead.

---

- `fail`
  - Unconditionally returns an **empty string** and an **error** with the specified text.
  - This is useful in scenarios where other conditionals have determined that template rendering should fail.
    - work with if. e.g., if securityContext.runAsUser=0, always fails

```yaml
fail "Please accept the end user license agreement"
```

---

## Lab: `fail`

```yaml
# mychart/templates/configmap.yaml
{{- if ne .Values.pizzaToppings "mushrooms" }}
{{- fail "pizzaToppings must be mushrooms" }}
{{- end }}
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  toppings: {{ .Values.pizzaToppings }}
```

### Valid

```yaml
# mychart/values.yaml
# pizzaToppings: mushrooms
```

```sh
helm template geared-marsupi ./mychart
# ---
# # Source: go-template/templates/sanbox.yaml
# # mychart/templates/configmap.yaml
# apiVersion: v1
# kind: ConfigMap
# metadata:
#   name: geared-marsupi-configmap
# data:
#   toppings: mushrooms
```

---

### Invalid

```yaml
# mychart/values.yaml
pizzaToppings: capricciosa
```

```sh
helm template geared-marsupi ./mychart
# Error: execution error at (go-template/templates/sanbox.yaml:3:4): pizzaToppings must be mushrooms

```

---

## Lab: `required`

```yaml
# mychart/templates/configmap.yaml
{{- $_ := required "pizzaToppings.option is required" .Values.pizzaToppings }}

apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  toppings: {{ .Values.pizzaToppings }}
```

---

### Valid values

```yaml
# mychart/values.yaml
pizzaToppings: mushrooms
```

```sh
helm template geared-marsupi ./mychart
# ---
# # Source: go-template/templates/sanbox.yaml
# # mychart/templates/configmap.yaml

# apiVersion: v1
# kind: ConfigMap
# metadata:
#   name: geared-marsupi-configmap
# data:
#   toppings: mushrooms
```

### invalid values

```yaml
# mychart/values.yaml
# pizzaToppings: mushrooms
```

```sh
helm template geared-marsupi ./mychart
# Error: execution error at (go-template/templates/sanbox.yaml:2:4): pizzaToppings.option is required

# Use --debug flag to render out invalid YAML
```

---

### Assign directly to the entry

```yaml
# mychart/templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  toppings: {{ required "pizzaToppings.option is required" .Values.pizzaToppings }}
```

- valid

```sh
helm template geared-marsupi ./mychart
# ---
# # Source: go-template/templates/sanbox.yaml
# # mychart/templates/configmap.yaml
# apiVersion: v1
# kind: ConfigMap
# metadata:
#   name: geared-marsupi-configmap
# data:
#   toppings: mushrooms
```

- invalid

```sh
helm template geared-marsupi ./mychart
# Error: execution error at (go-template/templates/sanbox.yaml:7:15): pizzaToppings.option is required
#
# Use --debug flag to render out invalid YAML
```

---

## Custom Validation

- Group custom validations in the \_helpers.tpl

---

### Lab: Custom Validation

- `_helpers.tpl`

```yaml
{{/* Expects a port to be passed as the context. */}}
{{- define "mychart.validators.portRange" -}}
{{- $sanitizedPort := int . -}}
{{- if or (lt $sanitizedPort 1) (gt $sanitizedPort 65535) -}}
{{- fail "Error: Ports must always be between 1 and 65535" -}}
{{- end -}}
{{/* Reurns the port value. */}}
{{- . }}
{{- end -}}
```

```yaml
# mychart/templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  port: {{ include "mychart.validators.portRange" .Values.port }}
```

- Valid

```yaml
# mychart/values.yaml
port: 80
# port: 1111111111111
```

```sh
helm template geared-marsupi ./mychart
# ---
# # Source: go-template/templates/sanbox.yaml
# # mychart/templates/configmap.yaml
# apiVersion: v1
# kind: ConfigMap
# metadata:
#   name: geared-marsupi-configmap
# data:
#   port: 80
```

- invalid

```yaml
# mychart/values.yaml
port: 1111111111111
```

```sh
helm template geared-marsupi ./mychart
# Error: execution error at (go-template/templates/sanbox.yaml:7:11): Error: Ports must always be between 1 and 65535
```

---

### Options: Group validator at the top

- `_helpers.tpl`

```yaml
{{/* Expects a port to be passed as the context. */}}
{{- define "mychart.validators.portRange" -}}
{{- $sanitizedPort := int . -}}
{{- if or (lt $sanitizedPort 1) (gt $sanitizedPort 65535) -}}
{{- fail "Error: Ports must always be between 1 and 65535" -}}
{{- end -}}
{{- end -}}
```

```yaml
# mychart/templates/configmap.yaml
{{- include "mychart.validators.portRange" .Values.port -}}
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  port: {{ .Values.port }}
```

- Test: it works

---
