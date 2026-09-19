# Istio Ambient - Authentication

[Back](../index.md)

- [Istio Ambient - Authentication](#istio-ambient---authentication)
  - [Authentication](#authentication)
  - [Mutual TLS authentication](#mutual-tls-authentication)
  - [PeerAuthentication](#peerauthentication)
    - [Declarative](#declarative)
  - [Lab: Global Authentication policy](#lab-global-authentication-policy)
  - [Lab: Namespace-wide policy](#lab-namespace-wide-policy)
  - [Lab: Workload policy](#lab-workload-policy)
  - [Lab: Mutual TLS Migration](#lab-mutual-tls-migration)
    - [setup](#setup)
    - [Enabel namespace mtls](#enabel-namespace-mtls)
    - [Enabel global mtls](#enabel-global-mtls)
    - [Migrate legacy](#migrate-legacy)

---

## Authentication

- `Istio` provides two types of **authentication**:
  - `Peer authentication`:
    - used for **service-to-service authentication** to verify the client making the connection.
    - Istio offers `mutual TLS` as a full stack solution for transport authentication, which can be enabled without requiring service code changes.
  - `Request authentication`:
    - Used for **end-user authentication** to verify the credential attached to the request.
    - Istio enables **request-level authentication** with `JSON Web Token (JWT)` validation

---

## Mutual TLS authentication

- `Policy Enforcement Points (PEPs)`
  - the implementation of Envoy proxies for **service-to-service communication**

- `mutual TLS authentication`
  - used by workloads to send requests to another workloads
  - the request is handled as follows:
    - 1. Istio **re-routes the outbound traffic** from a client to the client’s local `sidecar Envoy`.
    - 2. The `client side Envoy` starts a `mutual TLS` **handshake** with the `server side Envoy`.
      - During the handshake, the `client side Envoy` also does a **secure naming check** to verify that the service account presented in the server certificate is authorized to run the target service.
    - 3. The `client side Envoy` and the `server side Envoy` **establish** a `mutual TLS` connection, and `Istio` **forwards the traffic** from the `client side Envoy` to the `server side Envoy`.
    - 4. The `server side Envoy` **authorizes** the request.
      - If authorized, it **forwards the traffic** to the backend service through local TCP connections.

---

- `permissive mode` in mTLS
  - allows a service to **accept** both **plaintext traffic** and **mutual TLS traffic** at the same time.
  - provides greater flexibility for the on-boarding process.
    - The server’s installed Istio sidecar takes mutual TLS traffic immediately without breaking existing plaintext traffic.

---

- **By default**, `Istio`
  - **tracks** the server workloads migrated to Istio proxies
  - **configures** client proxies to send
    - **mutual TLS traffic** to those workloads automatically
    - **plain text traffic** to workloads **without** sidecars.

---

## PeerAuthentication

- `PeerAuthentication`
  - defines `mutual TLS (mTLS)` requirements for incoming connections.
  - in `sidecar` mode:
    - determines whether or not `mTLS` is **allowed or required** for connections to an `Envoy proxy sidecar`.
  - `ambient` mode:
    - security is transparently enabled for a pod by the `ztunnel node agent`.
      - `DISABLE` mode is not supported.
      - `STRICT` mode is useful to ensure that connections that bypass the mesh are not possible.

- **Policy precedence**
  - A **workload**-specific peer authentication policy **takes precedence over** a **namespace**-wide policy.

---

### Declarative

| Field           | Description                                                            |
| --------------- | ---------------------------------------------------------------------- |
| `selector`      | determines the workloads to apply the `PeerAuthentication` on.         |
| `mtls`          | Mutual TLS settings for workload. If not defined, inherit from parent. |
| `portLevelMtls` | Port specific mutual TLS settings.                                     |

- `selector`
  - If **not set**, the policy will be applied to **all workloads** in the same namespace as the policy.
  - If it is in the `root namespace`, it would be applied to **all workloads in the mesh**.

- `mtls.mode`

| Name                  | Description                                                                |
| --------------------- | -------------------------------------------------------------------------- |
| `UNSET`               | Inherit from **parent**, if has one. Otherwise treated as `PERMISSIVE`.    |
| `DISABLE`             | Connection is **not tunneled**.                                            |
| `PERMISSIVE`(default) | Connection can be **either plaintext or mTLS tunnel**.                     |
| `STRICT`              | Connection is an **mTLS tunnel** (TLS with client cert must be presented). |

---

- sample:

```yaml
#
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
  namespace: foo
spec:
  mtls:
    mode: STRICT # require mTLS traffic
```

```yaml
---
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
  namespace: foo
spec:
  # selector not set: apply all
  mtls:
    mode: PERMISSIVE #  allow both mTLS and plaintext traffic
---
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: finance
  namespace: foo
spec:
  selector:
    matchLabels:
      app: finance # applied to finance workload
  mtls:
    mode: STRICT # require mTLS
```

```yaml
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
  namespace: foo
spec:
  selector:
    matchLabels:
      app: finance # applied to finance workload
  mtls:
    mode: STRICT # require mTLS
  portLevelMtls:
    8080:
      mode: DISABLE #  leaves the port 8080 to plaintext.
```

```yaml
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
  namespace: foo
spec:
  selector:
    matchLabels:
      app: finance
  mtls:
    mode: UNSET # inherits mTLS mode from namespace (or mesh) settings
  portLevelMtls:
    8080:
      mode: DISABLE
```

---

## Lab: Global Authentication policy

- enable global mTLS in root namespace

```sh
kubectl apply -f - <<EOF
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: "default"
  namespace: "istio-system"
spec:
  mtls:
    mode: STRICT
EOF
# peerauthentication.security.istio.io/default created

k get pa -n istio-system
# NAME      MODE     AGE
# default   STRICT   38s

kubectl delete peerauthentication -n istio-system default
```

---

## Lab: Namespace-wide policy

- enable namespace mTLS

```sh
k create ns foo
# namespace/foo created
kubectl apply -f - <<EOF
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: "default"
  namespace: "foo"
spec:
  mtls:
    mode: STRICT
EOF
# peerauthentication.security.istio.io/default created

k get pa -n foo
# NAME      MODE     AGE
# default   STRICT   100s

k delete pa default -n foo
```

---

## Lab: Workload policy

- Enable mutual TLS per workload

```sh
k create ns bar
# namespace/bar created
k run nginx --image=nginx -n bar
# pod/nginx created

cat <<EOF | kubectl apply -n bar -f -
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: "nginx"
  namespace: "bar"
spec:
  selector:
    matchLabels:
      run: nginx
  mtls:
    mode: STRICT
EOF
# peerauthentication.security.istio.io/nginx created
```

---

## Lab: Mutual TLS Migration

### setup

```sh
# ##############################
# sidecar apps
# ##############################
kubectl create ns foo
kubectl label namespace foo istio-injection=enabled --overwrite
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.31/samples/httpbin/httpbin.yaml -n foo
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.31/samples/curl/curl.yaml -n foo

kubectl create ns bar
kubectl label namespace bar istio-injection=enabled --overwrite
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.31/samples/httpbin/httpbin.yaml -n bar
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.31/samples/curl/curl.yaml -n bar

# ##############################
# legacy
# ##############################
kubectl create ns legacy
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.31/samples/curl/curl.yaml -n legacy

# ##############################
# test connection: http
# ##############################
for from in "foo" "bar" "legacy"; do for to in "foo" "bar"; do kubectl exec "$(kubectl get pod -l app=curl -n ${from} -o jsonpath={.items..metadata.name})" -c curl -n ${from} -- curl http://httpbin.${to}:8000/ip -s -o /dev/null -w "curl.${from} to httpbin.${to}: %{http_code}\n"; done; done
# curl.foo to httpbin.foo: 200
# curl.foo to httpbin.bar: 200
# curl.bar to httpbin.foo: 200
# curl.bar to httpbin.bar: 200
# curl.legacy to httpbin.foo: 200
# curl.legacy to httpbin.bar: 200
```

---

### Enabel namespace mtls

```sh
# ##############################
# enable mtls in foo ns
# ##############################
kubectl apply -n foo -f - <<EOF
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
spec:
  mtls:
    mode: STRICT
EOF

# ##############################
# test connection http: legacy t0 foo fails
# ##############################
for from in "foo" "bar" "legacy"; do for to in "foo" "bar"; do kubectl exec "$(kubectl get pod -l app=curl -n ${from} -o jsonpath={.items..metadata.name})" -c curl -n ${from} -- curl http://httpbin.${to}:8000/ip -s -o /dev/null -w "curl.${from} to httpbin.${to}: %{http_code}\n"; done; done
# curl.foo to httpbin.foo: 200
# curl.foo to httpbin.bar: 200
# curl.bar to httpbin.foo: 200
# curl.bar to httpbin.bar: 200
# curl.legacy to httpbin.foo: 000
# command terminated with exit code 56
# curl.legacy to httpbin.bar: 200
```

---

### Enabel global mtls

```sh
kubectl apply -n istio-system -f - <<EOF
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
spec:
  mtls:
    mode: STRICT
EOF

# ##############################
# test connection http: legacy both fails
# ##############################
for from in "foo" "bar" "legacy"; do for to in "foo" "bar"; do kubectl exec "$(kubectl get pod -l app=curl -n ${from} -o jsonpath={.items..metadata.name})" -c curl -n ${from} -- curl http://httpbin.${to}:8000/ip -s -o /dev/null -w "curl.${from} to httpbin.${to}: %{http_code}\n"; done; done
# curl.foo to httpbin.foo: 200
# curl.foo to httpbin.bar: 200
# curl.bar to httpbin.foo: 200
# curl.bar to httpbin.bar: 200
# curl.legacy to httpbin.foo: 000
# command terminated with exit code 56
# curl.legacy to httpbin.bar: 000
# command terminated with exit code 56
```

---

### Migrate legacy

```sh
k get ns legacy --show-labels
# NAME     STATUS   AGE     LABELS
# legacy   Active   7m27s   kubernetes.io/metadata.name=legacy

k label ns legacy istio-injection=enabled
k get ns legacy --show-labels
# NAME     STATUS   AGE     LABELS
# legacy   Active   8m24s   istio-injection=enabled,kubernetes.io/metadata.name=legacy

k rollout restart deploy curl -n legacy
# deployment.apps/curl restarted

# confirm sidecar injection
k get po -n legacy
# NAME                    READY   STATUS    RESTARTS   AGE
# curl-7bc4dd6cb4-gs4d4   2/2     Running   0          48s

# ##############################
# test connection http: legacy succeed
# ##############################
for from in "foo" "bar" "legacy"; do for to in "foo" "bar"; do kubectl exec "$(kubectl get pod -l app=curl -n ${from} -o jsonpath={.items..metadata.name})" -c curl -n ${from} -- curl http://httpbin.${to}:8000/ip -s -o /dev/null -w "curl.${from} to httpbin.${to}: %{http_code}\n"; done; done
# curl.foo to httpbin.foo: 200
# curl.foo to httpbin.bar: 200
# curl.bar to httpbin.foo: 200
# curl.bar to httpbin.bar: 200
# curl.legacy to httpbin.foo: 200
# curl.legacy to httpbin.bar: 200
```
