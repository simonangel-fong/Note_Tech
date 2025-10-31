# Kubernetes - Pod: Secret

[Back](../../index.md)

- [Kubernetes - Pod: Secret](#kubernetes---pod-secret)
  - [Secret](#secret)
    - [Types of Secrets](#types-of-secrets)
  - [Imperative Commands](#imperative-commands)
  - [Declarative method (YAML)](#declarative-method-yaml)
    - [Create Secret](#create-secret)
    - [Using a Secret from a Pod](#using-a-secret-from-a-pod)
    - [For pulling private images](#for-pulling-private-images)
  - [Lab: Create Secret](#lab-create-secret)
    - [Imperative Method From Literal](#imperative-method-from-literal)
    - [Imperative Method From a file](#imperative-method-from-a-file)
    - [Imperative Method From Directory](#imperative-method-from-directory)
    - [Imperative Method From env file](#imperative-method-from-env-file)
    - [Declarative File](#declarative-file)
    - [Edit Secret](#edit-secret)
    - [Delete Secret](#delete-secret)
  - [Lab: Use Secret as Environment variables](#lab-use-secret-as-environment-variables)
    - [Create Secret](#create-secret-1)
    - [Import a Key from one Secret](#import-a-key-from-one-secret)
    - [Bulk Import](#bulk-import)

---

- Video:
  - https://www.youtube.com/watch?v=MTnQW9MxnRI

## Secret

- `Secret`

  - an object that contains a small amount of **sensitive data** such as a password, a token, or a key.

- `Secrets` are **base64-encoded**, not **encrypted** by default.

  - Enable a**t-rest encryption** (KMS) and **restrict RBAC**.

- Role in the cluster

  - **Decouple** **sensitive config** from **app code**/manifests.
  - **Least privilege**: **access controlled** with **RBAC** and namespaces.
  - **Multiple** consumption modes: as env vars, as files (volume), or for pulling private images.
  - Types indicate intent/validation (e.g., Opaque, kubernetes.io/tls, kubernetes.io/dockerconfigjson).

- Common use cases
  - App **credentials** (DB user/password, API tokens).
  - **TLS** keypairs for HTTPS (kubernetes.io/tls).
  - Private **image pulls** (imagePullSecrets).
  - **SSH keys** or CA bundles mounted into Pods.

---

### Types of Secrets

- `docker-registry type secret`:

  - for accessing a container registry.
  - `kubectl create secret docker-registry`:
    - Create a secret for use with a Docker registry.

- `generic type secret`:

  - indicate an Opaque secret type.
  - `kubectl create secret generic`:
    - Create a secret from a local file, directory, or literal value

- `tls type secret`:
  - holds TLS certificate and its associated key.
  - `kubectl create secret tls`:
    - Create a TLS secret

---

## Imperative Commands

- Create Generic

| CMD                                                                                          | DESC                                                            |
| -------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| `kubectl create secret generic sec_name --from-literal=key=valule --from-literal=key=valule` | Create a generic Secret from literal key–values.                |
| `kubectl create secret generic sec_name --from-file=key=./fname --from-file=key=./fname`     | Create a Secret from one or more files (keys become filenames). |
| `kubectl create secret generic sec_name --from-env-file=./env_file`                          | Create a Secret from a `.env` file (KEY=VALUE per line).        |

- Create tls

| CMD                                                               | DESC                                                    |
| ----------------------------------------------------------------- | ------------------------------------------------------- |
| `kubectl create secret tls sec_name --cert=./fname --key=./fname` | Create a TLS Secret (requires `tls.crt` and `tls.key`). |

- Create docker-registry

| CMD                                                                                                                                           | DESC                                          |
| --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| `kubectl create secret docker-registry sec_name --docker-server=ghcr.io --docker-username=uname --docker-password=token --docker-email=email` | Create a Docker registry (image pull) Secret. |

- Manage

| CMD                                                                                                | DESC                                                          |
| -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| `kubectl get secret`                                                                               | List Secrets in the current namespace.                        |
| `kubectl get secret sec_name -o yaml`                                                              | Output the Secret manifest (base64-encoded data).             |
| `kubectl create secret generic sec_name --from-literal=K=V --dry-run=client -o yaml > secret.yaml` | Generate YAML from an imperative command (useful for GitOps). |
| `kubectl describe secret sec_name`                                                                 | Show details/keys (not the decoded values).                   |
| `kubectl edit secret sec_name`                                                                     | Open the Secret for inline editing.                           |
| `kubectl delete secret sec_name`                                                                   | Delete a Secret.                                              |

---

## Declarative method (YAML)

### Create Secret

- use `stringData` for cleartext

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
  namespace: default
type: Opaque
stringData:
  DB_USER: alice
  DB_PASS: S3cr3t!
```

---

- In linux, use `echo secret_value | base64` to encode the value
- Use `data` for base64 value

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
data:
  DB_USER: YWxpY2U=
  DB_PASS: UzNjcjN0IQ==
```

---

### Using a Secret from a Pod

```yaml
kind: Pod
spec:
  containers:
    - name: app
      env:
        - name: DB_USER
          valueFrom:
            secretKeyRef:
              name: app-secret
              key: DB_USER
```

---

### For pulling private images

```yaml
kind: Pod
spec:
  imagePullSecrets:
    - name: regcred
  containers:
```

---

## Lab: Create Secret

### Imperative Method From Literal

```sh
kubectl create secret generic secret-literal --from-literal=DB_USER=myuser --from-literal=DB_PWD=mypwd
# secret/secret-literal created

kubectl get secret
# NAME             TYPE     DATA   AGE
# secret-literal   Opaque   2      21s

kubectl describe secret secret-literal
# Name:         secret-literal
# Namespace:    default
# Labels:       <none>
# Annotations:  <none>

# Type:  Opaque

# Data
# ====
# DB_PWD:   5 bytes
# DB_USER:  6 bytes
```

---

### Imperative Method From a file

```sh
mkdir secret_file
cat > secret_file/dev.yaml <<EOF
DB_DEV_USER: devuser
DB_DEV_PWD: devpwd
EOF

kubectl create secret generic secret-file --from-file=secret_file/dev.yaml
# secret/secret-file created

# confirm
kubectl get secret secret-file
# NAME          TYPE     DATA   AGE
# secret-file   Opaque   2      35s

kubectl describe secret secret-file
# Name:         secret-file
# Namespace:    default
# Labels:       <none>
# Annotations:  <none>

# Type:  Opaque

# Data
# ====
# dev.yaml:  38 bytes
```

---

### Imperative Method From Directory

```sh
mkdir secret_dir
cat > secret_dir/dev.yaml <<EOF
DB_DEV_USER: devuser
DB_DEV_PWD: devpwd
EOF

cat > secret_dir/prod.yaml <<EOF
DB_PROD_USER: produser
DB_PROD_PWD: prodpwd
EOF

kubectl create secret generic secret-dir --from-file=./secret_dir
# secret/secret-dir created

# confirm
kubectl get secret secret-dir
# NAME         TYPE     DATA   AGE
# secret-dir   Opaque   2      15s

kubectl describe secret secret-dir
# Name:         secret-dir
# Namespace:    default
# Labels:       <none>
# Annotations:  <none>

# Type:  Opaque

# Data
# ====
# dev.yaml:   38 bytes
# prod.yaml:  42 bytes
```

---

### Imperative Method From env file

```sh
mkdir secret_env
cat > secret_env/app.env <<EOF
DB_USER=user
DB_PWD=pwd
EOF

kubectl create secret generic secret-env --from-env-file=./secret_env/app.env
# secret/secret-env created

kubectl get secret secret-env
# NAME         TYPE     DATA   AGE
# secret-env   Opaque   2      19s

kubectl describe secret secret-env
# Name:         secret-env
# Namespace:    default
# Labels:       <none>
# Annotations:  <none>

# Type:  Opaque

# Data
# ====
# DB_PWD:   3 bytes
# DB_USER:  4 bytes
```

---

### Declarative File

```yaml
# secret_yaml/secret-yaml.yaml
apiVersion: v1
kind: Secret
metadata:
  name: secret-yaml
stringData:
  DB_USER: "user"
  DB_PWD: "pwd"
```

```sh
kubectl create -f secret_yaml/secret-yaml.yaml
# secret/secret-yaml created

kubectl get secret secret-yaml
# NAME          TYPE     DATA   AGE
# secret-yaml   Opaque   2      23

kubectl describe secret secret-yaml
# Name:         secret-yaml
# Namespace:    default
# Labels:       <none>
# Annotations:  <none>

# Type:  Opaque

# Data
# ====
# DB_PWD:   3 bytes
# DB_USER:  4 bytes
```

---

### Edit Secret

```sh
# edit: add DB_CONF: bXl1c2Vy
kubectl edit secret secret-literal
# secret/secret-literal edited

kubectl describe secret secret-literal
Name:         secret-literal
Namespace:    default
Labels:       <none>
Annotations:  <none>

Type:  Opaque

Data
====
DB_CONF:  6 bytes
DB_PWD:   5 bytes
DB_USER:  6 bytes
```

---

### Delete Secret

```sh
kubectl delete secret secret-dir secret-env secret-file secret-literal secret-yaml
# secret "secret-dir" deleted from default namespace
# secret "secret-env" deleted from default namespace
# secret "secret-file" deleted from default namespace
# secret "secret-literal" deleted from default namespace
# secret "secret-yaml" deleted from default namespace

# confirm
kubectl get secret
```

---

## Lab: Use Secret as Environment variables

### Create Secret

```sh
kubectl create secret generic app-secret --from-literal=DB_USER=user --from-literal=DB_PWD=pwd
# secret/app-secret created
```

---

### Import a Key from one Secret

- `pod-secret-key.yaml`

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-secret-key
spec:
  containers:
    - name: myapp
      command: ["sh", "-c", "env | grep -E 'DB_USER|DB_PWD' && sleep 2000"]
      image: busybox:latest
      env:
      - name: DB_USER
        valueFrom:
          secretKeyRef:
            name: app-secret
            key: DB_USER
```

```sh
kubectl create -f pod-secret-key.yaml
# pod/pod-secret-key created

kubectl get pod
# NAME             READY   STATUS    RESTARTS   AGE
# pod-secret-key   1/1     Running   0          18s

kubectl logs pod/pod-secret-key
# DB_USER=user

kubectl delete pod/pod-secret-key
# pod "pod-secret-key" deleted from default namespace
```
---

### Bulk Import

- `pod-secret-bulk.yaml`

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-secret-bulk
spec:
  containers:
  - name: myapp
    command: ["sh", "-c", "env | grep -E 'DB_USER|DB_PWD' && sleep 2000"]
    image: busybox:latest
    envFrom:
    - secretRef:
        name: app-secret
```

```sh
kubectl create -f pod-secret-bulk.yaml
# pod/pod-secret-bulk created

kubectl get pod
# NAME              READY   STATUS    RESTARTS   AGE
# pod-secret-bulk   1/1     Running   0          13s

kubectl logs pod/pod-secret-bulk
# DB_PWD=pwd
# DB_USER=user

kubectl delete pod/pod-secret-bulk
# pod "pod-secret-bulk" deleted from default namespace
```
