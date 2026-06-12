# Helm Chart - Go Templates: Loop

[Back](../index.md)

- [Helm Chart - Go Templates: Loop](#helm-chart---go-templates-loop)
  - [Iteration](#iteration)
  - [Looping with the `range` action](#looping-with-the-range-action)
    - [Lab: loop `range`](#lab-loop-range)
    - [Lab: loop list with index](#lab-loop-list-with-index)
    - [Lab: loop kv-pair with index](#lab-loop-kv-pair-with-index)

---

## Iteration

- associated functions:
  - `list`
  - `range`
  - `len`

## Looping with the `range` action

### Lab: loop `range`

```yaml
# mychart/values.yaml
pizzaToppings:
  - mushrooms
  - cheese
  - peppers
  - onions
  - pineapple
```

```yaml
# mychart/templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  {{- if .Values.pizzaToppings | default list | len }}
  toppings: |-
    {{- range $.Values.pizzaToppings }}
    - {{ . | title | quote }}
    {{- end }}
  {{- end }}
  sizes: |-
    {{- range tuple "small" "medium" "large" }}
    - {{ . }}
    {{- end }}
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
#   toppings: |-
#     - "Mushrooms"
#     - "Cheese"
#     - "Peppers"
#     - "Onions"
#     - "Pineapple"
#   sizes: |-
#     - small
#     - medium
#     - large
```

---

### Lab: loop list with index

```yaml
# mychart/values.yaml
pizzaToppings:
  - mushrooms
  - cheese
  - peppers
  - onions
  - pineapple
```

```yaml
# mychart/templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  toppings: |-
    {{- range $index, $topping := (.Values.pizzaToppings | default list) }}
      {{ $index }}: {{ $topping }}
    {{- end }}
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
#   toppings: |-
#       0: mushrooms
#       1: cheese
#       2: peppers
#       3: onions
#       4: pineapple
```

---

### Lab: loop kv-pair with index

```yaml
# mychart/values.yaml
favorite:
  drink: coffee
  food: pizza
```

```yaml
# mychart/templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  {{- range $key, $val := (.Values.favorite | default dict) }}
  {{ $key }}: {{ $val | quote }}
  {{- end }}
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
#   drink: "coffee"
#   food: "pizza"
```

---
