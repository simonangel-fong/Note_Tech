# Kubernetes - Pod: Secret

[Back](../../index.md)

- [Kubernetes - Pod: Secret](#kubernetes---pod-secret)
  - [Secret](#secret)
    - [ConfigMap vs secret](#configmap-vs-secret)
    - [Types of Secrets](#types-of-secrets)
    - [Use `secret` as env](#use-secret-as-env)
    - [Use as `secret volume`](#use-as-secret-volume)
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
  - [Lab: TLS secret for nginx https](#lab-tls-secret-for-nginx-https)
    - [Optional: Creating a generic (opaque) secret](#optional-creating-a-generic-opaque-secret)
    - [Explore secret within the container](#explore-secret-within-the-container)

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

- a `secret` is **distributed** only to the `node` that runs the `pod` that needs the `secret`.

  - `secrets` on the `worker nodes` themselves are always **stored in memory** and **never** written to physical storage.

- the **maximum size** of a secret is approximately `1MB`

---

### ConfigMap vs secret

- fields

| configMap    | Secret                   | DESC                                            |
| ------------ | ------------------------ | ----------------------------------------------- |
| `binaryData` | `data`                   | Base64-encoded strings                          |
| `data`       | `stringData`(Write-only) | plain text strings                              |
| `immutable`  | `immutable`              | boolean value indicating whether can be updated |
| N/A          | `type`                   | type of secret                                  |

- `stringData` field in secrets
  - used to store plain text values
  - write-only
  - add plaintext values to the secret without having to encode them manually.
    - When reading back the `Secret` object, any values are added to `stringData` will be included in the `data` field as **Base64-encoded strings**.

---

### Types of Secrets

| Type                                  | Desc                                                           |
| ------------------------------------- | -------------------------------------------------------------- |
| `Opaque`                              | default type; contain secret data stored under arbitrary keys. |
| `bootstrap.kubernetes.io/token`       | tokens that are used when bootstrapping new cluster nodes      |
| `kubernetes.io/basic-auth`            | the credentials required for basic authentication.             |
| `kubernetes.io/dockercfg`             | credentials required for accessing a Docker image registry     |
| `kubernetes.io/dockerconfigjson`      | the credentials for accessing a Docker registry(new format)    |
| `kubernetes.io/service-account-token` | token that identifies a Kubernetes service account.            |
| `kubernetes.io/ssh-auth`              | the private key used for SSH authentication.                   |
| `kubernetes.io/tls`                   | a TLS certificate and the associated private key.              |

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

### Use `secret` as env

- Note that exposure of `secret` as env var could be a risk.
  - recommend to use `secret volume`

```yaml
# specify keys
spec:
  containers:
  - name: busybox
    env:
    - name: TLS_CERT
        valueFrom:
          secretKeyRef:
            name: tls-secret
            key: tls.crt

```

---

### Use as `secret volume`

- default permissions

  - `0600` / `rw-------`

- The files in a `secret volume` are stored in an **in-memory filesystem (tmpfs)**

  - they are less likely to be compromised.

- example

```yaml
# specify keys
spec:
  volumes:
    - name: cert-and-key
      secret:
        secretName: tls-secret
        items:
          - key: tls.crt
            path: tls.crt
          - key: tls.key
            path: tls.key
            mode: 0600 # read only
  containers:
    volumeMounts:
      - name: tls-secret
        mountPath: /etc/certs
        readOnly: true
```

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

---

## Lab: TLS secret for nginx https

```sh
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout tls.key \
  -out tls.crt \
  -subj "/CN=localhost"

ls -l tls.crt  tls.key
# -rw-r--r-- 1 ubuntuadmin ubuntuadmin 1115 Dec 26 21:24 tls.crt
# -rw------- 1 ubuntuadmin ubuntuadmin 1704 Dec 26 21:24 tls.key

kubectl create secret tls nginx-tls-secret \
  --cert tls.crt \
  --key tls.key
# secret/nginx-tls-secret created

kubectl describe secret nginx-tls-secret
# Name:         nginx-tls-secret
# Namespace:    default
# Labels:       <none>
# Annotations:  <none>

# Type:  kubernetes.io/tls

# Data
# ====
# tls.crt:  1115 bytes
# tls.key:  1704 bytes

tee nginx-config.yaml<<EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
data:
  nginx.conf: |
    server {
        listen 443 ssl;
        server_name localhost;

        ssl_certificate /etc/nginx/ssl/tls.crt;
        ssl_certificate_key /etc/nginx/ssl/tls.key;

        location / {
            root /usr/share/nginx/html;
            index index.html;
        }
    }
EOF

kubectl apply -f nginx-config.yaml
# configmap/nginx-config created

kubectl describe configmap/nginx-config
# Name:         nginx-config
# Namespace:    default
# Labels:       <none>
# Annotations:  <none>

# Data
# ====
# nginx.conf:
# ----
# server {
#     listen 443 ssl;
#     server_name localhost;

#     ssl_certificate /etc/nginx/ssl/tls.crt;
#     ssl_certificate_key /etc/nginx/ssl/tls.key;

#     location / {
#         root /usr/share/nginx/html;
#         index index.html;
#     }
# }



# BinaryData
# ====

# Events:  <none>

tee nginx-https.yaml<<EOF
apiVersion: v1
kind: Pod
metadata:
  name: nginx-https
spec:
  volumes:
  - name: config-volume
    configMap:
      name: nginx-config
  - name: ssl-certs
    secret:
      secretName: nginx-tls-secret

  containers:
  - name: nginx
    image: nginx:latest
    ports:
    - containerPort: 443
    volumeMounts:
    - name: config-volume
      mountPath: /etc/nginx/conf.d/default.conf
      subPath: nginx.conf
    - name: ssl-certs
      mountPath: "/etc/nginx/ssl"
      readOnly: true
EOF

kubectl apply -f nginx-https.yaml
# pod/nginx-https created

kubectl get pod
# NAME          READY   STATUS    RESTARTS   AGE
# nginx-https   1/1     Running   0          12s

kubectl port-forward pod/nginx-https 8443:443
# Forwarding from 127.0.0.1:8443 -> 443
# Forwarding from [::1]:8443 -> 443

# confirm with detail
curl -vk https://localhost:8443
# * Host localhost:8443 was resolved.
# * IPv6: ::1
# * IPv4: 127.0.0.1
# *   Trying [::1]:8443...
# * Connected to localhost (::1) port 8443
# * ALPN: curl offers h2,http/1.1
# * TLSv1.3 (OUT), TLS handshake, Client hello (1):
# * TLSv1.3 (IN), TLS handshake, Server hello (2):
# * TLSv1.3 (IN), TLS handshake, Encrypted Extensions (8):
# * TLSv1.3 (IN), TLS handshake, Certificate (11):
# * TLSv1.3 (IN), TLS handshake, CERT verify (15):
# * TLSv1.3 (IN), TLS handshake, Finished (20):
# * TLSv1.3 (OUT), TLS change cipher, Change cipher spec (1):
# * TLSv1.3 (OUT), TLS handshake, Finished (20):
# * SSL connection using TLSv1.3 / TLS_AES_256_GCM_SHA384 / X25519 / RSASSA-PSS
# * ALPN: server accepted http/1.1
# * Server certificate:
# *  subject: CN=localhost
# *  start date: Dec 27 02:24:49 2025 GMT
# *  expire date: Dec 27 02:24:49 2026 GMT
# *  issuer: CN=localhost
# *  SSL certificate verify result: self-signed certificate (18), continuing anyway.
# *   Certificate level 0: Public key type RSA (2048/112 Bits/secBits), signed using sha256WithRSAEncryption
# * using HTTP/1.x
# > GET / HTTP/1.1
# > Host: localhost:8443
# > User-Agent: curl/8.5.0
# > Accept: */*
# >
# * TLSv1.3 (IN), TLS handshake, Newsession Ticket (4):
# * TLSv1.3 (IN), TLS handshake, Newsession Ticket (4):
# * old SSL session ID is stale, removing
# < HTTP/1.1 200 OK
# < Server: nginx/1.29.4
# < Date: Sat, 27 Dec 2025 02:46:47 GMT
# < Content-Type: text/html
# < Content-Length: 615
# < Last-Modified: Tue, 09 Dec 2025 18:28:10 GMT
# < Connection: keep-alive
# < ETag: "69386a3a-267"
# < Accept-Ranges: bytes
# <
# <!DOCTYPE html>
# <html>
# <head>
# <title>Welcome to nginx!</title>
# <style>
# html { color-scheme: light dark; }
# body { width: 35em; margin: 0 auto;
# font-family: Tahoma, Verdana, Arial, sans-serif; }
# </style>
# </head>
# <body>
# <h1>Welcome to nginx!</h1>
# <p>If you see this page, the nginx web server is successfully installed and
# working. Further configuration is required.</p>

# <p>For online documentation and support please refer to
# <a href="http://nginx.org/">nginx.org</a>.<br/>
# Commercial support is available at
# <a href="http://nginx.com/">nginx.com</a>.</p>

# <p><em>Thank you for using nginx.</em></p>
# </body>
# </html>
# * Connection #0 to host localhost left intact
```

---

### Optional: Creating a generic (opaque) secret

```sh
kubectl create secret generic kiada-tls --from-file tls.crt=tls.crt --from-file tls.key=tls.key
```

---

### Explore secret within the container

```sh
kubectl exec nginx-https -- cat /etc/nginx/ssl/tls.crt
# -----BEGIN CERTIFICATE-----
# MIIDCTCCAfGgAwIBAgIUUvY2Z/sV1TfyjJVUxemQ8wCi6AMwDQYJKoZIhvcNAQEL
# BQAwFDESMBAGA1UEAwwJbG9jYWxob3N0MB4XDTI1MTIyNzAyMjQ0OVoXDTI2MTIy
# NzAyMjQ0OVowFDESMBAGA1UEAwwJbG9jYWxob3N0MIIBIjANBgkqhkiG9w0BAQEF
# AAOCAQ8AMIIBCgKCAQEAjS7ZlByawDIPLe+yFQdU5iCw2y5wmPKuVLvaOgS0Z11
# ...

kubectl exec nginx-https -- cat /etc/nginx/ssl/tls.key
# -----BEGIN PRIVATE KEY-----
# MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCNLtmUHJrAMg8t
# 77IVB1TmILDbLnCY8q5Uu9o6BLRnXUOT4RspPj3LZODuxuQlW1APLMNaJjZZDKAH
# +K0OVTk+RJLBjPL4fn3QZgBBfGa1RGoK2dvqRG62pJ/0g9RGWrZxmx3ntGfW11Zs
# ...
```
