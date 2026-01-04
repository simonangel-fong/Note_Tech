# Kubernetes: Storage - ConfigMap

[Back](../../index.md)

- [Kubernetes: Storage - ConfigMap](#kubernetes-storage---configmap)
  - [ConfigMap](#configmap)
    - [ConfigMap object](#configmap-object)
    - [Declarative Manifest](#declarative-manifest)
    - [Imperative Command](#imperative-command)
  - [Lab: Create ConfigMap](#lab-create-configmap)
    - [Imperative Command from Literals](#imperative-command-from-literals)
    - [Imperative Command from file](#imperative-command-from-file)
    - [Imperative Command from file with custom key name](#imperative-command-from-file-with-custom-key-name)
    - [Imperative Command From multiple files in a directory](#imperative-command-from-multiple-files-in-a-directory)
    - [Imperative Command From an env file](#imperative-command-from-an-env-file)
    - [Imperative Command From multple env files](#imperative-command-from-multple-env-files)
    - [Declarative File](#declarative-file)
    - [Edit ConfigMap](#edit-configmap)
    - [Delete ConfigMap](#delete-configmap)

---

## ConfigMap

- `ConfigMap`

  - an API object used to **store non-confidential data** in **key-value pairs**.
  - `Pods` can **consume** `ConfigMaps` as
    - **environment variables** in command line arguments
    - **configuration files** in a volume.
  - If the data is to store are **confidential**,
    - use a `Secret` rather than a `ConfigMap`
    - use **additional (third party) tools** to keep your data private.

- **Role**:

  - allows to **decouple** **environment-specific configuration** from your container **images**, so that the applications are easily **portable**.

- **Limitation**:

  - does not provide **secrecy** or **encryption**.

- Common **user cases**:

  - app settings
  - feature flags
  - file-based configs (nginx.conf, application.yml).

- the **key/value pairs** in the `config map` are passed to `containers` as

  - `environment variables`
  - **mounted as files** in the container’s filesystem via a `configMap volume`

- Benefits:

  - dicouple pod with configuration
  - apply different configurations for different environments
    - Same `pod` definition + different `config map`

- The **amount** of information that can fit in a `config map` is dictated by `etcd`
  - the **maximum** size is **one megabyte**.

---

### ConfigMap object

- The **name** of a ConfigMap **must** be a valid **DNS subdomain name**.

- keys:

  - must consist of **alphanumeric characters**, `-,` `_` or `.`.

- fields

  - don't have `spec` field
  - `data field`

    - optional
    - key-value pairs
    - contain **UTF-8 strings**

  - `binaryData field`
    - optional
    - key-value pairs
    - contain **binary data** as **base64-encoded strings**.
    - keys stored in data must not overlap with the keys in the binaryData field.

- can add an `immutable field` to a `ConfigMap` definition to create an `immutable ConfigMap`.

---

### Declarative Manifest

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_MODE: "prod"
  application.yml: |
    server:
      port: 8080
```

---

### Imperative Command

| CMD                                                                                  | DESC                                           |
| ------------------------------------------------------------------------------------ | ---------------------------------------------- |
| `kubectl get cm`                                                                     | List ConfigMaps in the current namespace.      |
| `kubectl get cm app-config -o yaml`                                                  | Show a specific ConfigMap in YAML.             |
| `kubectl create cm app-config --from-literal=K=V --dry-run=client -o yaml > cm.yaml` | Generate YAML from an imperative command       |
| `kubectl describe cm app-config`                                                     | Detailed view: keys, events, annotations, etc. |
| `kubectl edit cm app-config`                                                         | Edit a ConfigMap in editor.                    |
| `kubectl delete cm app-config`                                                       | Delete a ConfigMap.                            |

- Create CM

| CMD                                                       | DESC                                                    |
| --------------------------------------------------------- | ------------------------------------------------------- |
| `kubectl create cm cm_name --from-literal=key=value`      | Create a ConfigMap from one or more literal key/values. |
| `kubectl create cm cm_name --from-literal=key=value`      | Create a ConfigMap from one or more literal key/values. |
| `kubectl create cm cm_name --from-file=cf_file`           | Create from a file; filename becomes the key            |
| `kubectl create cm cm_name --from-file=mykey=config.yaml` | Create from a file; Specify the key                     |
| `kubectl create cm cm_name --from-file=./templates/`      | Create from a directory; each file becomes a key.       |
| `kubectl create cm cm_name --from-env-file=.env`          | Create from a dotenv file (KEY=VALUE lines).            |

- Common Options

| Option            | Desc                                                        |
| ----------------- | ----------------------------------------------------------- |
| `--from-literal`  | Inserts a key and a literal value.                          |
| `--from-env-file` | Inserts each line of the specified file as a separate entry |
| `--from-file`     | Inserts the contents of a file                              |

- `--from-file` option:
  - `--from-file filename`
    - key: the filename
    - value: content of the file
    - e.g., `--from-file myfile.txt`; key=`myfile.txt`; value=myfile.txt content
  - `--from-file keyname=filename`
    - key: keyname
    - value: content of the file
    - e.g., `--from-file mykey=myfile.txt`; key=`mykey`; value=myfile.txt content
  - `--from-file dir/`
    - key: each filename in dir
    - value: content of each file
    - e.g., `--from-file mydir/`; key=the name of each file in mydir; value=the content of each file;
    - Subdirectories, symbolic links, devices, pipes, and files whose **base name isn’t a valid config map key** are **ignored**.

---

## Lab: Create ConfigMap

### Imperative Command from Literals

```sh
kubectl create cm config-literal --from-literal=APP_MODE="prod" --from-literal=LOG_LEVEL="info"
# configmap/config-literal created

kubectl get cm
# NAME               DATA   AGE
# config-literal     1      10s

kubectl describe cm config-literal
# Name:         config-literal
# Namespace:    default
# Labels:       <none>
# Annotations:  <none>

# Data
# ====
# APP_MODE:
# ----
# prod

# LOG_LEVEL:
# ----
# info


# BinaryData
# ====

# Events:  <none>
```

---

### Imperative Command from file

```sh
mkdir conffile

# create file
cat > conffile/config-file.yaml <<'EOF'
APP_MODE: "prod"
LOG_LEVEL: "info"
application.yml: |
  server:
    port: 8080
EOF

kubectl create configmap config-file --from-file=./conffile/config-file.yaml
# configmap/config-file created

# confirm
kubectl get cm
# NAME               DATA   AGE
# config-file        1      15s

kubectl describe cm config-file
# Name:         config-file
# Namespace:    default
# Labels:       <none>
# Annotations:  <none>

# Data
# ====
# config-file.yaml:
# ----
# APP_MODE: "prod"\r
# LOG_LEVEL: "info"\r
# application.yml: |\r
#   server:\r
#     port: 8080


# BinaryData
# ====

# Events:  <none>
```

---

### Imperative Command from file with custom key name

```sh
mkdir conffile

# create file
cat > conffile/config-file.yaml <<'EOF'
APP_MODE: "prod"
LOG_LEVEL: "info"
application.yml: |
  server:
    port: 8080
EOF

kubectl create configmap config-file-custom-key --from-file=application.yml=./conffile/config-file.yaml
# configmap/config-file-custom-key created

kubectl get cm
# NAME                     DATA   AGE
# config-file-custom-key   1      10s

kubectl describe cm config-file-custom-key
# Name:         config-file-custom-key
# Namespace:    default
# Labels:       <none>
# Annotations:  <none>

# Data
# ====
# application.yml:
# ----
# APP_MODE: "prod"\r
# LOG_LEVEL: "info"\r
# application.yml: |\r
#   server:\r
#     port: 8080


# BinaryData
# ====

# Events:  <none>
```

---

### Imperative Command From multiple files in a directory

```sh
mkdir confdir
# create files
cat > confdir/dev.yaml <<'EOF'
APP_MODE: "dev"
LOG_LEVEL: "info"
application.yml: |
  server:
    port: 8080
EOF

cat > confdir/prod.yaml <<'EOF'
APP_MODE: "prod"
LOG_LEVEL: "info"
application.yml: |
  server:
    port: 80
EOF

kubectl create configmap config-dir --from-file=confdir/
# configmap/config-dir created

kubectl get cm
# NAME                     DATA   AGE
# config-dir               2      12s

kubectl describe cm config-dir
# Name:         config-dir
# Namespace:    default
# Labels:       <none>
# Annotations:  <none>

# Data
# ====
# dev.yaml:
# ----
# APP_MODE: "dev"\r
# LOG_LEVEL: "info"\r
# application.yml: |\r
#   server:\r
#     port: 8080\r


# prod.yaml:
# ----
# APP_MODE: "prod"\r
# LOG_LEVEL: "info"\r
# application.yml: |\r
#   server:\r
#     port: 80


# BinaryData
# ====

# Events:  <none>
```

---

### Imperative Command From an env file

```sh
mkdir conf_env
cat > conf_env/dev.env <<EOF
APP_MODE="dev"
LOG_LEVEL="info"
PORT=8080
EOF

kubectl create cm config-env --from-env-file=conf_env/dev.env
# configmap/config-env created

kubectl get cm
# NAME                     DATA   AGE
# config-env               3      11s

kubectl describe cm config-env
# Name:         config-env
# Namespace:    default
# Labels:       <none>
# Annotations:  <none>

# Data
# ====
# APP_MODE:
# ----
# "dev"

# LOG_LEVEL:
# ----
# "info"

# PORT:
# ----
# 8080


# BinaryData
# ====

# Events:  <none>
```

---

### Imperative Command From multple env files

- Cannot overlap

```sh
mkdir conf_env

cat > conf_env/dev.env <<EOF
APP_MODE="dev"
LOG_LEVEL="info"
PORT=8080
EOF

cat > conf_env/prod.env <<EOF
APP_MODE="prod"
LOG_LEVEL="info"
PORT=80
EOF

kubectl create cm config-multipl-env --from-env-file=conf_env/dev.env --from-env-file=conf_env/prod.env
# error: cannot add key "APP_MODE", another key by that name already exists in Data for ConfigMap "config-multipl-env"

cat > conf_env/app.env <<EOF
LOG_LEVEL="info"
PORT=8080
EOF

cat > conf_env/more.env <<EOF
LOG_ERROR="error"
TIER="frontend"
EOF

kubectl create cm config-multipl-env --from-env-file=conf_env/app.env --from-env-file=conf_env/more.env
# configmap/config-multipl-env created

kubectl get cm config-multipl-env
# NAME                 DATA   AGE
# config-multipl-env   4      43

kubectl describe cm config-multipl-env
# Name:         config-multipl-env
# Namespace:    default
# Labels:       <none>
# Annotations:  <none>

# Data
# ====
# LOG_ERROR:
# ----
# "error"

# LOG_LEVEL:
# ----
# "info"

# PORT:
# ----
# 8080

# TIER:
# ----
# "frontend"


# BinaryData
# ====

# Events:  <none>
```

---

### Declarative File

```yaml
# conf_yaml/config-yaml.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: config-yaml
data:
  APP_MODE: "dev"
  LOG_LEVEL: "info"

  # file-like keys
  application.yml: |
    server:
      port: 8080
```

```sh
kubectl create -f conf_yaml/config-yaml.yaml
# configmap/config-yaml created

kubectl get cm
# NAME               DATA   AGE
# config-yaml        3      13s

kubectl describe cm config-yaml
# Name:         config-yaml
# Namespace:    default
# Labels:       <none>
# Annotations:  <none>

# Data
# ====
# APP_MODE:
# ----
# dev

# LOG_LEVEL:
# ----
# info

# application.yml:
# ----
# server:
#   port: 8080



# BinaryData
# ====

# Events:  <none>
```

---

### Edit ConfigMap

```sh

# edit: add application.yml
kubectl edit cm config-literal
# configmap/config-literal edited

kubectl describe cm config-literal
# Name:         config-literal
# Namespace:    default
# Labels:       <none>
# Annotations:  <none>

# Data
# ====
# APP_MODE:
# ----
# prod

# application.yml:
# ----
# server:
#   port: 8080



# BinaryData
# ====

# Events:  <none>
```

---

### Delete ConfigMap

```sh
kubectl delete cm config-literal config-dir config-env config-file config-file-custom-key config-multipl-env config-yaml
# configmap "config-literal" deleted from default namespace
# configmap "config-dir" deleted from default namespace
# configmap "config-env" deleted from default namespace
# configmap "config-file" deleted from default namespace
# configmap "config-file-custom-key" deleted from default namespace
# configmap "config-multipl-env" deleted from default namespace
# configmap "config-yaml" deleted from default namespace

# confirm
kubectl get cm
```

---
