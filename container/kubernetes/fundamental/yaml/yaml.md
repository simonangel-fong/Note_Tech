# Kubernetes - YAML File

[Back](../../index.md)

- [Kubernetes - YAML File](#kubernetes---yaml-file)
  - [YAML](#yaml)
  - [Basic Syntax](#basic-syntax)
  - [Common Data Structure](#common-data-structure)
    - [scalar - Strings, numbers, boolean, ...](#scalar---strings-numbers-boolean-)
    - [Mapping - Maps/Dictionaries](#mapping---mapsdictionaries)
    - [Sequences - Arrays/Lists](#sequences---arrayslists)
    - [Advanced](#advanced)
  - [Yaml File in Kubernetes](#yaml-file-in-kubernetes)

---

## YAML

- `YAML` / `yet another markup language` / `YAML ain't markup language`

  - a human-readable **data serialization language** that is often used for **writing configuration files**.

---

## Basic Syntax

- **case sensitive**
- extension: `.yaml` / `.yml`
- Indentation:
  - **whitespace**
  - **No** tabs
- Comments: `#`
- start marker: 3 hyphens `---`
  - signal the beginning of a new YAML document within a single file or stream.

```yaml
---
# document 1
codename: YAML
name: YAML ain't markup language
release: 2001
---
# document 2
uses:
  - configuration language
  - data persistence
  - internet messaging
  - cross-language data sharing
---
# document 3
company: spacelift
domain:
  - devops
  - devsecops
tutorial:
  - name: yaml
  - type: awesome
  - rank: 1
  - born: 2001
author: omkarbirade
published: true
```

---

## Common Data Structure

### scalar - Strings, numbers, boolean, ...

- `scalar`

  - literals Unicode characters.
  - can be strings, numbers, boolean, etc.

- Folding Strings: `>`
  - interpreted without the new line characters

```yaml
message: >
  even though
  it looks like
  this is a multiline message,
  it is actually not

# ==
message: "even though it looks like this is a multiline message,it is actually not"

```

- Block strings: `|`
  - interpreted with the new lines (\n)

```yaml
message: |
  this is
  a real multiline
  message
```

---

### Mapping - Maps/Dictionaries

- `mapping`

  - an **unordered** set of **key/value** node pairs
  - each of the **keys** is **unique**

- example

```yaml
Fruit: Apple
Vegetable: Carrot
Liquid: Water
Meat: Chicken

Banana:
  Calories: 105
  Fat: 0.4 g
  Carbs: 27 g

Grapes:
  Calories: 62
  Fat: 0.3 g
  Carbs: 16 g
```

---

### Sequences - Arrays/Lists

- `sequences`

  - an ordered series of zero or more nodes.
  - each of the **keys** is **unique**
  - a leading hyphen (`-`).
  - option: enclosed in **square brackets** `[]`

```yaml
Fruits:
  - Orange
  - Apple
  - Banna

Vegetables: [Carrot, Cauliflower, Tomato]
```

---

### Advanced

```yaml
Fruits:
  - Banana:
      Calories: 105
      Fat: 0.4 g
      Carbs: 27 g

  - Grapes:
      Calories: 62
      Fat: 0.3 g
      Carbs: 16 g
```

---

## Yaml File in Kubernetes

- Contain 4 top level and required fields
  - `apiVersion`:
    - Version of Kub API
    - value: string
  - `kind`:
    - Type of object to create
    - Can be pod, service, replicaSet, Deployment
    - value: string
  - `metadata`:
    - The data about the object
    - value: dictionary
      - be careful with the indentation
  - `spec`:
    - specification of the object
    - value: dictionary

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  # user custom label
  labels:
    app: myapp
    type: front-end
spec:
  # a list
  containers:
    - name: nginx-container
      image: nginx
```

- possible value for apiVersion field

| Kind       | Version |
| ---------- | ------- |
| pod        | v1      |
| Service    | v1      |
| ReplicaSet | apps/v1 |
| Deployment | apps/v1 |
