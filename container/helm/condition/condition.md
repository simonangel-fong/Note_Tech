# Helm Chart - Go Templates: Condition

[Back](../index.md)

- [Helm Chart - Go Templates: Condition](#helm-chart---go-templates-condition)
  - [Condition](#condition)
    - [Lab: if else](#lab-if-else)
    - [Lab: `with`](#lab-with)

---

## Condition

- `if`/`else`: creating conditional blocks
- `with`:
  - check if an entry is empty;
  - only work for non-empty entry;
  - `.` assigned to the entry

---

### Lab: if else

```yaml
# mychart/values.yaml
favorite:
  drink: coffee
env: prod
```

```yaml
# mychart/templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  count: {{ if eq .Values.env "prod" -}} 3 {{- else -}} 1 {{- end }}
  drink: {{ .Values.favorite.drink | default "tea" | quote }}
  {{- if eq .Values.favorite.drink "coffee" }}
  mug: "true"
  {{ end }}
```

```sh
helm template geared-marsupi ./mychart
# ---
# # Source: go-template/templates/sanbox.yaml
# apiVersion: v1
# kind: ConfigMap
# metadata:
#   name: demo-named-template-configmap
# data:
#   count: 3
#   drink: "coffee"
#   mug: "true"
```

---

### Lab: `with`

```yaml
# mychart/values.yaml
favorite:
  drink: coffee
  food: pizza
```

- if `.Values.favorite` is not empty
  - $: root scope
  - .food: the scope is `.Values.favorite`

```yaml
# mychart/templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  {{- with .Values.favorite }}
  release: {{ $.Release.Name }}
  drink: {{ .drink | default "tea" | quote }}
  food: {{ .food | upper | quote }}
  {{- end }}
```

```sh
helm template demo-named-template ./mychart
# ---
# # Source: go-template/templates/sanbox.yaml
# apiVersion: v1
# kind: ConfigMap
# metadata:
#   name: demo-named-template-configmap
# data:
#   release: demo-named-template
#   drink: "coffee"
#   food: "PIZZA"
```

---
