# Kubernetes - Yaml File

[Back](../../index.md)

- [Kubernetes - Yaml File](#kubernetes---yaml-file)
  - [YAML](#yaml)
  - [Base Rule](#base-rule)
  - [Basic Components](#basic-components)
    - [Key Value Pair](#key-value-pair)
    - [Array/List members](#arraylist-members)
    - [Dictionary/Map](#dictionarymap)
    - [Advanced](#advanced)
  - [Yaml File in Kubernetes](#yaml-file-in-kubernetes)

---

## YAML

- `YAML`

  - `yet another markup language` / `YAML ain't markup language`
  - a human-readable **data serialization language** that is often used for writing configuration files.

- `YAML` includes a **markup language** with important **construct**, to distinguish data-oriented language with the document markup.
- Feature
  - Matches native **data structures** of agile methodology and its languages such as Perl, Python, PHP, Ruby and JavaScript
  - YAML data is **portable** between programming languages
  - Includes data consistent **data model**
  - Easily **readable** by humans
  - Supports one-direction processing
  - Ease of implementation and usage

---

## Base Rule

- YAML is **case sensitive**
- The files should have `.yaml` as the **extension**
- YAML does **not allow** the use of **tabs** while creating YAML files;
  - **spaces** are allowed instead

---

## Basic Components

- **Comments**: `#`
- **Indentation**

  - use **whitespace** to denote structure.
    - number of space indicates different structure
  - Not use Tabs

- **Multiple documents** with single streams

  - separated with 3 hyphens (`---`).

```yaml
defaults: &defaults
  adapter: postgres
  host: localhost

development:
  database: myapp_development
  <<: *defaults

test:
  database: myapp_test
  <<: *defaults
```

---

### Key Value Pair

```yaml
Fruit: Apple
Vegetable: Carrot
Liquid: Water
Meat: Chicken
```

---

### Array/List members

- a leading hyphen (`-`).
- option: enclosed in **square brackets**

```yaml
Fruits:
  - Orange
  - Apple
  - Banna

Vegetables:
  - Carrot
  - Cauliflower
  - Tomato
```

---

### Dictionary/Map

```yaml
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
