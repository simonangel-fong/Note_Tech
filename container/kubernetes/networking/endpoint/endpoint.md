# K8s - Endpoint

[Back](../../index.md)

- [K8s - Endpoint](#k8s---endpoint)
  - [endpoints object](#endpoints-object)
  - [Imperative Commands](#imperative-commands)
  - [Lab: Get Endpoint](#lab-get-endpoint)
  - [EndpointSlice object](#endpointslice-object)
    - [Imperative Command](#imperative-command)
  - [Lab: Get EndpointSlices](#lab-get-endpointslices)
  - [Managing service endpoints manually](#managing-service-endpoints-manually)
  - [Lab: Create service withtout label selector](#lab-create-service-withtout-label-selector)

---

## endpoints object

- `endpoints`

  - the object to which a `service` forwards traffic can be anything
    that **has an IP address**.

- fully managed by Kubernetes.

  - created by Kubernetes when creating the associated Service objects.
  - Each time a new `pod` **appears or disappears** that **matches** the Service’s `label selector`, Kubernetes **updates** the `Endpoints
object` to **add or remove** the endpoint associated with the pod.

- Endpoint in service

  - `Services` do **not** **send traffic** to `Pods` directly.
  - They send traffic to the `Endpoints object` that contains the real `Pod IPs`.

- Each `Endpoints object` contains a list of `IP` and `port` combinations

---

## Imperative Commands

| CMD                                       | DESC                                                           |
| ----------------------------------------- | -------------------------------------------------------------- |
| `kubectl get endpoints` /`kubectl get ep` | List all Endpoints objects in the current namespace            |
| `kubectl get endpoints --all-namespaces`  | List endpoints across all namespaces                           |
| `kubectl get endpoints -l app=nginx`      | Filter endpoints by label                                      |
| `kubectl get endpoints -o wide`           | Show endpoints with IP:Port details                            |
| `kubectl describe endpoints <name>`       | View detailed endpoint info (ready/not-ready addresses, ports) |
| `kubectl get endpoints <svc>`             | Show which pod IPs are backing a Service                       |
| `kubectl get endpoints <svc> -o yaml`     | Export endpoints manifest                                      |
| `kubectl edit endpoints <name>`           | Live-edit endpoints object                                     |
| `kubectl delete endpoints <name>`         | Delete an Endpoints object                                     |

- incorrect command: `kubectl get endpoint`
  - `endpoints` must be with `s`

---

## Lab: Get Endpoint

```sh
kubectl get svc
# NAME                TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
# demo-nodeport-svc   NodePort    10.102.182.197   <none>        8080:30977/TCP   3h10m

kubectl get endpoints
# Warning: v1 Endpoints is deprecated in v1.33+; use discovery.k8s.io/v1 EndpointSlice
# NAME                ENDPOINTS                   AGE
# demo-nodeport-svc   10.1.3.20:80,10.1.3.21:80   3h7m

kubectl describe endpoints demo-nodeport-svc
# Warning: v1 Endpoints is deprecated in v1.33+; use discovery.k8s.io/v1 EndpointSlice
# Name:         demo-nodeport-svc
# Namespace:    default
# Labels:       endpoints.kubernetes.io/managed-by=endpoint-controller
# Annotations:  endpoints.kubernetes.io/last-change-trigger-time: 2025-12-28T20:44:02Z
# Subsets:
#   Addresses:          10.1.3.20,10.1.3.21
#   NotReadyAddresses:  <none>
#   Ports:
#     Name  Port  Protocol
#     ----  ----  --------
#     http  80    TCP

# Events:  <none>

kubectl get endpoints demo-nodeport-svc -o yaml
# Warning: v1 Endpoints is deprecated in v1.33+; use discovery.k8s.io/v1 EndpointSlice
# apiVersion: v1
# kind: Endpoints
# metadata:
#   annotations:
#     endpoints.kubernetes.io/last-change-trigger-time: "2025-12-28T20:44:02Z"
#   creationTimestamp: "2025-12-28T20:44:02Z"
#   labels:
#     endpoints.kubernetes.io/managed-by: endpoint-controller
#   name: demo-nodeport-svc
#   namespace: default
#   resourceVersion: "2664611"
#   uid: ffd1ea32-ea57-453a-b9c5-8a0a3b68155c
# subsets:
# - addresses:
#   - ip: 10.1.3.20
#     nodeName: docker-desktop
#     targetRef:
#       kind: Pod
#       name: nginx-c8585b9f-jxt4k
#       namespace: default
#       uid: 16e36478-091d-4a1d-b609-91c9c8e037c0
#   - ip: 10.1.3.21
#     nodeName: docker-desktop
#     targetRef:
#       kind: Pod
#       name: nginx-c8585b9f-zrrbv
#       namespace: default
#       uid: e631f551-40c7-420a-add7-8535b5598e02
#   ports:
#   - name: http
#     port: 80
#     protocol: TCP
```

---

## EndpointSlice object

- `EndpointSlice object`

  - **splits** the `endpoints` of a single service into **multiple slices**.

- `EndpointSlices` are created and managed **automatically**.

- `Endpoints object` contains **multiple** `endpoint subsets`
  - each `EndpointSlice` contains **only one**.
- If two groups of `pods` expose the service on **different ports**,
  - they appear in two different `EndpointSlice objects`.
- an `EndpointSlice object` supports a **maximum** of **1000** `endpoints`
  - by default Kubernetes only adds up to **100** `endpoints` to **each slice**.
- The number of `ports` in a `slice` is also **limited to 100.**

---

### Imperative Command

| CMD                                                              | DESC                                        |
| ---------------------------------------------------------------- | ------------------------------------------- |
| `kubectl get endpointslices` /`kubectl get endpointslice`        | List all EndpointSlice objects              |
| `kubectl get endpointslices --all-namespaces`                    | List slices across all namespaces           |
| `kubectl get endpointslices -l kubernetes.io/service-name=myapp` | Get EndpointSlices of a **Service**         |
| `kubectl describe endpointslice <name>`                          | Show detailed endpoint readiness & topology |
| `kubectl get endpointslice <name> -o yaml`                       | Export EndpointSlice manifest               |
| `kubectl delete endpointslice <name>`                            | Delete an EndpointSlice                     |
| `kubectl create endpointslice <name> --dry-run=client -o yaml`   | Generate slice manifest                     |
| `kubectl edit endpointslice <name>`                              | Live-edit an EndpointSlice                  |

---

## Lab: Get EndpointSlices

```sh
kubectl get endpointslices
# NAME                      ADDRESSTYPE   PORTS   ENDPOINTS             AGE
# demo-nodeport-svc-l6zl8   IPv4          80      10.1.3.20,10.1.3.21   5h54m

# list slices for a service
kubectl get endpointslices -l kubernetes.io/service-name=demo-nodeport-svc
# NAME                      ADDRESSTYPE   PORTS   ENDPOINTS             AGE
# demo-nodeport-svc-l6zl8   IPv4          80      10.1.3.20,10.1.3.21   6h2m

# show details for a svc
kubectl describe endpointslice demo-nodeport-svc
# Name:         demo-nodeport-svc-l6zl8
# Namespace:    default
# Labels:       endpointslice.kubernetes.io/managed-by=endpointslice-controller.k8s.io
#               kubernetes.io/service-name=demo-nodeport-svc
# Annotations:  endpoints.kubernetes.io/last-change-trigger-time: 2025-12-28T20:44:02Z
# AddressType:  IPv4
# Ports:
#   Name  Port  Protocol
#   ----  ----  --------
#   http  80    TCP
# Endpoints:
#   - Addresses:  10.1.3.20
#     Conditions:
#       Ready:    true
#     Hostname:   <unset>
#     TargetRef:  Pod/nginx-c8585b9f-jxt4k
#     NodeName:   docker-desktop
#     Zone:       <unset>
#   - Addresses:  10.1.3.21
#     Conditions:
#       Ready:    true
#     Hostname:   <unset>
#     TargetRef:  Pod/nginx-c8585b9f-zrrbv
#     NodeName:   docker-desktop
#     Zone:       <unset>
# Events:         <none>

```

---

## Managing service endpoints manually

- When you create a `Service object` with a `label selector`, Kubernetes **automatically creates and manages** the `Endpoints` and `EndpointSlice` objects and uses the `selector` to **determine** the `service endpoints`.
- can also manage `endpoints` **manually** by creating the `Service` object **without** a `label selector`.

  - must create the `Endpoints` object yourself.
  - don’t need to create the `EndpointSlice` objects because Kubernetes mirrors the `Endpoints` object to create corresponding `EndpointSlices`.

- use case:
  - make an existing **external service** accessible to pods in cluster **under a different name**. This way, the `service` can be **found** through the `cluster DNS` and `environment variables`.

---

## Lab: Create service withtout label selector

```yaml
apiVersion: v1
kind: Service
metadata:
  name: external-service
spec:
  ports:
    - name: http
      port: 80
```

- Creating an Endpoints object

```yaml
apiVersion: v1
kind: Endpoints
metadata:
  name: external-service # match service name
subsets:
  - addresses:
      - ip: 1.1.1.1 # the ip outside the cluster
      - ip: 2.2.2.2 # the ip outside the cluster
    ports:
      - name: http
        port: 88
```
