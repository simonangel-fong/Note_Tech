# Istio - Sidecar Mode

[Back](../index.md)

- [Istio - Sidecar Mode](#istio---sidecar-mode)
  - [Sidecar Mode](#sidecar-mode)
    - [Envoy Proxy](#envoy-proxy)
    - [how it works](#how-it-works)
  - [Imperative Method](#imperative-method)
  - [Declarative Method](#declarative-method)
  - [Lab: Sidecar Injection](#lab-sidecar-injection)
    - [Enable a namespace](#enable-a-namespace)
    - [Enable by command `istioctl kube-inject`](#enable-by-command-istioctl-kube-inject)
    - [Enable by a label](#enable-by-a-label)

---

## Sidecar Mode

- `sidecar proxy`
  - Istio service mesh model
  - Each application Pod gets an extra container
    - implemented by `Envoy proxy`

- `sidecar injection`
  - adds a proxy(`envoy proxy`) to the workload

---

### Envoy Proxy

- `Envoy Proxy`
  - a high-performance, open-source `proxy server` designed for cloud-native applications and microservices.

- a foundational component for `Istio`

- Originally built at `Lyft`, it serves as a universal `data plane` that **abstracts** the network, handling critical tasks like traffic routing, load balancing, security, and observability independent of application code.

- roles:
  - **Traffic Management**:
    - **Routes** requests, performs advanced **load balancing** (like `circuit breaking` and auto-retries), and balances traffic across distributed environments.
    - `circuit breaker`:
      - a design pattern used to **prevent cascading failures**.
  - **Observability**:
    - Generates detailed **statistics** and **logs** for all network traffic, making it easier to trace requests and debug issues in complex systems.
  - **Security**:
    - Handles **TLS termination**, enforces `mutual TLS (mTLS)` for secure communication channels, and applies **rate limiting** policies.

---

- How It Works

- `Envoy` operates primarily at the `L3/L4 network layer` while also offering robust `L7 (application)` capabilities.
  - It uses a **pluggable filter chain architecture** that can process protocols like `HTTP/1.1`, `HTTP/2`, `HTTP/3`, `gRPC`, and raw `TCP`/`UDP`.
- It is typically deployed in **two main ways**:
  - `Sidecar Proxy`:
    - Deployed as a **separate container** or **process** alongside a primary application service to **intercept all inbound and outbound network traffic**.
  - `Edge Proxy`:
    - Acts as an **API gateway** or **"front proxy"** at the boundary of a network, **intercepting requests** from the outside world and directing them into an internal network.

---

### how it works

- The application does not directly talk to another application.
  - Instead, traffic goes **through the proxy**.

```txt
Pod: frontend
+-------------------------+
| frontend app container  |
| Envoy sidecar proxy     |
+-------------------------+

Pod: backend
+-------------------------+
| backend app container   |
| Envoy sidecar proxy     |
+-------------------------+

frontend app
   |
   v
frontend Envoy proxy
   |
   v
backend Envoy proxy
   |
   v
backend app
```

---

## Imperative Method

| Command                                                                    | Description                                                     |
| -------------------------------------------------------------------------- | --------------------------------------------------------------- |
| `kubectl label namespace <namespace> istio-injection=enabled`              | Enable automatic sidecar injection for a namespace.             |
| `kubectl label namespace <namespace> istio-injection=disabled --overwrite` | Disable automatic sidecar injection for a namespace.            |
| `kubectl label namespace <namespace> istio-injection-`                     | Remove the `istio-injection` label from a namespace.            |
| `kubectl label namespace <namespace> istio.io/rev=<revision>`              | Enable revision-based sidecar injection                         |
| `kubectl label namespace <namespace> istio.io/rev-`                        | Remove the revision-based injection label.                      |
| `kubectl label namespace <namespace> istio-injection- istio.io/rev-`       | Remove both classic and revision-based injection labels         |
| `istioctl kube-inject -f <file>.yaml \| kubectl apply -f -`                | Manually inject the Istio sidecar into a manifest and apply it. |
| `kubectl label pod <pod> sidecar.istio.io/inject="false" -n <namespace>`   | Disable sidecar injection for a specific Pod template/resource  |

- Common workflow

```sh
# new workload
kubectl create namespace team-a
kubectl label namespace team-a istio-injection=enabled
kubectl apply -n team-a -f app.yaml
kubectl get pod -n team-a

# existing workload
kubectl label namespace team-a istio-injection=enabled --overwrite
kubectl rollout restart deployment my-app -n team-a
kubectl get pod -n team-a
```

## Declarative Method

- `istioctl kube-inject`

```yaml
# web.yaml
# kubectl run web --image nginx --dry-run=client -o yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: web
  name: web
spec:
  containers:
    - image: nginx
      name: web
      resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```

```sh
KUBECONFIG=./kubeconfig istioctl kube-inject -f web.yaml | KUBECONFIG=./kubeconfig kubectl apply -f -
# pod/web created

KUBECONFIG=./kubeconfig kubectl get po web
# NAME   READY   STATUS    RESTARTS   AGE
# web    2/2     Running   0          43s
```

- using label `sidecar.istio.io/inject: "true"`

```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: web-pod
    sidecar.istio.io/inject: "true"
  name: web-pod
spec:
  containers:
    - image: nginx
      name: web-pod
      resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```

---

## Lab: Sidecar Injection

### Enable a namespace

```sh
KUBECONFIG=./kubeconfig istioctl analyze -n default
# Info [IST0102] (Namespace default) The namespace is not enabled for Istio injection. Run 'kubectl label namespace default istio-injection=enabled' to enable it, or 'kubectl label namespace default istio-injection=disabled' to explicitly mark it as not needing injection.

# enable sidecar injection
KUBECONFIG=./kubeconfig kubectl label namespace default istio-injection=enabled
# namespace/default labeled

# confirm
KUBECONFIG=./kubeconfig kubectl get ns default --show-labels
# NAME      STATUS   AGE   LABELS
# default   Active   81m   istio-injection=enabled,kubernetes.io/metadata.name=default

KUBECONFIG=./kubeconfig istioctl analyze -n default
# ✔ No validation issues found when analyzing namespace: default.


# Deploy sample application
KUBECONFIG=./kubeconfig kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.30/samples/bookinfo/platform/kube/bookinfo.yaml
# service/details created
# serviceaccount/bookinfo-details created
# deployment.apps/details-v1 created
# service/ratings created
# serviceaccount/bookinfo-ratings created
# deployment.apps/ratings-v1 created
# service/reviews created
# serviceaccount/bookinfo-reviews created
# deployment.apps/reviews-v1 created
# deployment.apps/reviews-v2 created
# deployment.apps/reviews-v3 created
# service/productpage created
# serviceaccount/bookinfo-productpage created
# deployment.apps/productpage-v1 created

# confirm sidecar
KUBECONFIG=./kubeconfig kubectl get pods
# NAME                              READY   STATUS    RESTARTS   AGE
# details-v1-764c46cfdb-t475m       2/2     Running   0          31s
# productpage-v1-85664dccbc-7q2f9   2/2     Running   0          30s
# ratings-v1-779fdc7f86-flllf       2/2     Running   0          31s
# reviews-v1-85964f9f98-nrwbn       2/2     Running   0          31s
# reviews-v2-6f7fbdc6fd-g7tvv       2/2     Running   0          31s
# reviews-v3-689b477554-kc6tm       2/2     Running   0          31s

# confirm that the Bookinfo application is running,
KUBECONFIG=./kubeconfig kubectl exec "$(KUBECONFIG=./kubeconfig kubectl get pod -l app=ratings -o jsonpath='{.items[0].metadata.name}')" -c ratings -- curl -sS productpage:9080/productpage | grep -o "<title>.*</title>"
# <title>Simple Bookstore App</title>

KUBECONFIG=./kubeconfig kubectl describe po details-v1-764c46cfdb-fvvxp | grep -B2 "Container ID"
# Init Containers:
#   istio-init:
#     Container ID:  containerd://5d0f3254e065202bb69ee838db303aba6ee07b0c169ad74290331c443436d1c8
# --
#       /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-mn4px (ro)
#   istio-proxy:
#     Container ID:  containerd://2870c0e05d7ee4b30b0122d89065e7ab1ff429b1192b59ffba8d74670beefc53
# --
# Containers:
#   details:
#     Container ID:   containerd://7057084c3c2b0f39c8976157fb8d70e8889981323b700bba62eec85bb2841d77
```

---

### Enable by command `istioctl kube-inject`

- Disable

```sh
# disable
KUBECONFIG=./kubeconfig kubectl label namespace default istio-injection-
# namespace/default unlabeled

# confrm ns not enabled
KUBECONFIG=./kubeconfig istioctl analyze -n default
# Info [IST0102] (Namespace default) The namespace is not enabled for Istio injection. Run 'kubectl label namespace default istio-injection=enabled' to enable it, or 'kubectl label namespace default istio-injection=disabled' to explicitly mark it as not needing injection.
```

- Enable a deployment

```sh
KUBECONFIG=./kubeconfig kubectl create deploy web --image=nginx --dry-run=client -o yaml > web.yaml

cat web.yaml
# apiVersion: apps/v1
# kind: Deployment
# metadata:
#   labels:
#     app: web
#   name: web
# spec:
#   replicas: 1
#   selector:
#     matchLabels:
#       app: web
#   strategy: {}
#   template:
#     metadata:
#       labels:
#         app: web
#     spec:
#       containers:
#       - image: nginx
#         name: nginx
#         resources: {}
# status: {}

KUBECONFIG=./kubeconfig istioctl kube-inject -f web.yaml | KUBECONFIG=./kubeconfig kubectl apply -f -
# deployment.apps/web created

 KUBECONFIG=./kubeconfig kubectl get pod
# NAME                  READY   STATUS    RESTARTS   AGE
# web-577fccc77-jsjb4   2/2     Running   0          26s
```

---

### Enable by a label

```yaml
# web-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: web-pod
    sidecar.istio.io/inject: "true"
  name: web-pod
spec:
  containers:
    - image: nginx
      name: web-pod
      resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```

```sh
KUBECONFIG=./kubeconfig kubectl get pod web-pod
# NAME      READY   STATUS    RESTARTS   AGE
# web-pod   2/2     Running   0          17s
```
