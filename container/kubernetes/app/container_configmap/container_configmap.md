# Kubernetes - Pod: ConfigMap

[Back](../../index.md)

- [Kubernetes - Pod: ConfigMap](#kubernetes---pod-configmap)
  - [ConfigMap](#configmap)
    - [ConfigMap object](#configmap-object)
    - [use `configMap` as Environment Variables](#use-configmap-as-environment-variables)
    - [Use as `ConfigMap Volume`](#use-as-configmap-volume)
  - [Imperative Command](#imperative-command)
  - [Declarative File](#declarative-file)
    - [Create](#create)
  - [Using Configmaps as environment variables in a Pod](#using-configmaps-as-environment-variables-in-a-pod)
  - [Lab: Create ConfigMap](#lab-create-configmap)
    - [Imperative Command from Literals](#imperative-command-from-literals)
    - [Imperative Command from file](#imperative-command-from-file)
    - [Imperative Command from file with custom key name](#imperative-command-from-file-with-custom-key-name)
    - [Imperative Command From multiple files in a directory](#imperative-command-from-multiple-files-in-a-directory)
    - [Imperative Command From an env file](#imperative-command-from-an-env-file)
    - [Imperative Command From multple env files](#imperative-command-from-multple-env-files)
    - [Declarative File](#declarative-file-1)
    - [Edit ConfigMap](#edit-configmap)
    - [Delete ConfigMap](#delete-configmap)
  - [Lab: Use ConfigMap as Environment variables](#lab-use-configmap-as-environment-variables)
    - [Create ConfigMap](#create-configmap)
    - [Bulk Import](#bulk-import)
    - [Import a Key](#import-a-key)
  - [Lab: using `configMap` volume](#lab-using-configmap-volume)
    - [Create html files](#create-html-files)
    - [Error: Create pod without optional](#error-create-pod-without-optional)
    - [Create pod with optional](#create-pod-with-optional)
    - [Creating `configMap` Volume](#creating-configmap-volume)
    - [Load All keys](#load-all-keys)
    - [Specify a key](#specify-a-key)

---

## ConfigMap

- `ConfigMap`

  - an API object used to **store non-confidential data** in **key-value pairs**.
  - `Pods` can **consume** `ConfigMaps` as **environment variables**, command-line **arguments**, or as configuration **files** in a volume.
    - setting **configuration data** separately from **application code**.
  - If the data is to store are **confidential**,
    - use a `Secret` rather than a `ConfigMap`
    - use **additional (third party) tools** to keep your data private.

- Role:
  - allows to decouple **environment-specific configuration** from your container **images**, so that the applications are easily **portable**.
- Limitation:

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

### use `configMap` as Environment Variables

---

### Use as `ConfigMap Volume`

- file permission
  - default:
    - `rw-r--r--` (`0644`)
    - rw-r--r-- (0644)
- files in the `configMap` volume are `symbolic links` with permission `0777`

- edit `configMap` volume

  - the **files** in the `configMap` volume are **automatically updated**.
  - It can take up to **a minute** for the files to be **updated**

- edit `configMap` env

  - **can’t** be updated while the container is **running**.
  - if container restarts, **new** `config map` values will apply to new container

- `immutable` field
  - specify whether the CM is mutable.

---

- Example: Using subPath to mount a single file from the volume

```yaml
spec:
  volumes:
  - name: nginx-config
    configMap:
      name: nginx-config
      optional: true    # optional
  containers:
  - name: nginx
    image: nginx
    volumeMounts:
    - name: nginx-config
      mountPath: /usr/share/nginx/html
```

---

- `ConfigMap volumes` use `symbolic links` to provide **atomic updates**
  - Kubernetes ensures that **all files** in a `configMap volume` are **updated atomically**, meaning that all updates are done **instantaneously**.
  - by the use of symbolic file links
- the **file paths** that the application reads point to **actual files** via **two successive** `symbolic links`.

---

## Imperative Command

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

## Declarative File

### Create

- `app-config.yaml`

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

```sh
kubectl apply -f app-config.yaml
```

---

## Using Configmaps as environment variables in a Pod

- Import value

```yaml
kind: Pod
spec:
  containers:
    - name: app
      env:
        - name: APP_MODE
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: APP_MODE
```

---

- bulk import:

```yaml
kind: Pod
spec:
  containers:
    - name: app
      envFrom:
        - configMapRef:
            name: mapp-config
```

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

## Lab: Use ConfigMap as Environment variables

### Create ConfigMap

```sh
kubectl create cm app-config --from-literal=APP_MODE=prod --from-literal=LOG_LEVEL=info
# configmap/app-config created
```

### Bulk Import

- `pod-conf-bulk.yaml`

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-conf-bulk
spec:
  containers:
    - name: myapp
      command: ["sh", "-c", "env | grep -E 'APP_MODE|LOG_LEVEL' && sleep 2000"]
      image: busybox:latest
      envFrom:
        - configMapRef:
            name: app-config
```

```sh
kubectl create -f pod-conf-bulk.yaml
# pod/pod-conf-bulk created

kubectl get pod
# NAME            READY   STATUS    RESTARTS   AGE
# pod-conf-bulk   1/1     Running   0          13s

kubectl logs pod/pod-conf-bulk
# APP_MODE=prod
# LOG_LEVEL=info

kubectl delete pod/pod-conf-bulk
# pod "pod-conf-bulk" deleted from default namespace
```

---

### Import a Key

- `pod-conf-key.yaml`

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-conf-key
spec:
  containers:
    - name: myapp
      image: busybox
      command: ["sh", "-c", "env | grep -E 'APP_MODE|LOG_LEVEL' && sleep 2000"]
      env:
        - name: APP_MODE
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: APP_MODE
```

```sh
kubectl create -f pod-conf-key.yaml
# pod/pod-conf-key created

kubectl get pod
# NAME            READY   STATUS    RESTARTS   AGE
# pod-conf-bulk   1/1     Running   0          13s

kubectl logs pod/pod-conf-key
# APP_MODE=prod

kubectl delete pod/pod-conf-key
# pod "pod-conf-key" deleted from default namespace
```

---

## Lab: using `configMap` volume

### Create html files

```sh
mkdir demo-configmap-volume
cd demo-configmap-volume

# Create index.html
tee index.html<<EOF
<html>
<title>Home</title>
<body>
  <h1> Home </h1>
  <p> This is home page </p>
</body>
</html>
EOF

# Create error.html
tee error.html<<EOF
<html>
<title>Error</title>
<body>
  <h1> Error </h1>
  <p> This is Error page </p>
</body>
</html>
EOF
```

---

### Error: Create pod without optional

```sh
# create pod definition
tee demo-configmap-volume-pod.yaml<<EOF
apiVersion: v1
kind: Pod
metadata:
  name: demo-configmap-volume-pod
spec:
  volumes:
  - name: nginx-config
    configMap:
      name: nginx-config

  containers:
  - name: nginx
    image: nginx
    volumeMounts:
    - name: nginx-config
      mountPath: /usr/share/nginx/html
EOF
```

- Create pod before configMap creation

```sh
kubectl apply -f demo-configmap-volume-pod.yaml
# pod/demo-configmap-volume-pod created

kubectl get pod
# NAME                        READY   STATUS              RESTARTS   AGE
# demo-configmap-volume-pod   0/1     ContainerCreating   0          4s

kubectl describe pod demo-configmap-volume-pod
# Events:
#   Type     Reason       Age                From               Message
#   ----     ------       ----               ----               -------
#   Normal   Scheduled    25s                default-scheduler  Successfully assigned default/demo-configmap-volume-pod to docker-desktop
#   Warning  FailedMount  10s (x6 over 25s)  kubelet            MountVolume.SetUp failed for volume "nginx-config" : configmap "nginx-config" not found
```

> Volume is created before pod creation
> pod creation failed because volume creation caused by configmap not found.

---

### Create pod with optional

```sh
# pod definition with optional
tee demo-configmap-volume-pod-optional.yaml<<EOF
apiVersion: v1
kind: Pod
metadata:
  name: demo-configmap-volume-pod-optional
spec:
  volumes:
  - name: nginx-config
    configMap:
      name: nginx-config
      optional: true    # optional
  containers:
  - name: nginx
    image: nginx
    volumeMounts:
    - name: nginx-config
      mountPath: /usr/share/nginx/html
EOF

kubectl apply -f demo-configmap-volume-pod-optional.yaml
# pod/demo-configmap-volume-pod-optional created

kubectl get pod
# NAME                                 READY   STATUS    RESTARTS   AGE
# demo-configmap-volume-pod-optional   1/1     Running   0          8s

# test
kubectl port-forward demo-configmap-volume-pod-optional 8000:80
# Forwarding from 127.0.0.1:8000 -> 80
# Forwarding from [::1]:8000 -> 80

# error: because no home page
curl 127.0.0.1:8000
# <html>
# <head><title>403 Forbidden</title></head>
# <body>
# <center><h1>403 Forbidden</h1></center>
# <hr><center>nginx/1.29.4</center>
# </body>
# </html>
```

> pod created but has no html files

---

### Creating `configMap` Volume

```sh
kubectl create cm nginx-config --from-file=index.html --from-file=error.html
# configmap/nginx-config created

kubectl get cm
# NAME               DATA   AGE
# nginx-config       2      9s

kubectl describe cm nginx-config
# Name:         nginx-config
# Namespace:    default
# Labels:       <none>
# Annotations:  <none>

# Data
# ====
# error.html:
# ----
# <html>\r
# <title>Error</title>\r
# <body>\r
#   <h1> Error </h1>\r
#   <p> This is Error page </p>\r
# </body>\r
# </html>

# index.html:
# ----
# <html>\r
# <title>Home</title>\r
# <body>\r
# <h1> Home </h1>\r
# <p> This is home page </p>\r
# </body>\r
# </html>


# BinaryData
# ====

# Events:  <none>
```

---

### Load All keys

- recreate pod

```sh
kubectl replace --force -f demo-configmap-volume-pod-optional.yaml
# pod "demo-configmap-volume-pod-optional" deleted from default namespace
# pod/demo-configmap-volume-pod-optional replaced

kubectl port-forward demo-configmap-volume-pod-optional 8000:80
# Forwarding from 127.0.0.1:8000 -> 80
# Forwarding from [::1]:8000 -> 80

curl localhost:8000
# <html>
# <title>Home</title>
# <body>
# <h1> Home </h1>
# <p> This is home page </p>
# </body>
# </html>

curl localhost:8000/error.html
# <html>
# <title>Error</title>
# <body>
#   <h1> Error </h1>
#   <p> This is Error page </p>
# </body>
# </html>
```

---

### Specify a key

```sh
tee demo-configmap-volume-pod-key.yaml<<EOF
apiVersion: v1
kind: Pod
metadata:
  name: demo-configmap-volume-pod-key
spec:
  volumes:
  - name: nginx-config
    configMap:
      name: nginx-config
      optional: true    # optional
      items:
        - key: index.html
          path: index.html
  containers:
  - name: nginx
    image: nginx
    volumeMounts:
    - name: nginx-config
      mountPath: /usr/share/nginx/html
EOF

kubectl apply -f demo-configmap-volume-pod-key.yaml
# pod/demo-configmap-volume-pod-key created

kubectl get pod
# NAME                                 READY   STATUS    RESTARTS   AGE
# demo-configmap-volume-pod-key        1/1     Running   0          7s

kubectl port-forward demo-configmap-volume-pod-key 8080:80
# Forwarding from 127.0.0.1:8080 -> 80
# Forwarding from [::1]:8080 -> 80

# confirm: index pass
curl localhost:8080
# <html>
# <title>Home</title>
# <body>
# <h1> Home </h1>
# <p> This is home page </p>
# </body>
# </html>

# confirm: error not pass
url localhost:8080/error.html
# <html>
# <head><title>404 Not Found</title></head>
# <body>
# <center><h1>404 Not Found</h1></center>
# <hr><center>nginx/1.29.4</center>
# </body>
# </html>
```

- Exlpore file in container

```sh
# confirm symbolic link
kubectl exec -it demo-configmap-volume-pod-key -- ls -l /usr/share/nginx/html/index.html
# lrwxrwxrwx 1 root root 17 Dec 27 00:28 /usr/share/nginx/html/index.html -> ..data/index.html
```
