# Kubernetes: Container - Readiness Probe

[Back](../../index.md)

- [Kubernetes: Container - Readiness Probe](#kubernetes-container---readiness-probe)
  - [Readiness Probe](#readiness-probe)
    - [Declarative Manifest](#declarative-manifest)
    - [Readiness Probe Types](#readiness-probe-types)
  - [Lab: Readiness Probe - httpGet](#lab-readiness-probe---httpget)

---

## Readiness Probe

- `readiness probes`
  - used to **periodically check** whether an **application is ready to accept connections**.
  - periodically determine the **readiness status** of the `pod`.
    - If the probe is **successful**, the pod is considered ready
    - if it fails, **removed** as an `endpoint` from the services to which it belongs, `service` **doesn’t forward** connections to the pod
- **developer** decides what `readiness` means in the **context of their application**.

- When `startup probe` is defined, the **initial delay** for the `readiness probe` **begins** when the `startup probe` **succeeds**.

  - When the container is **ready**, the `pod` becomes an `endpoint` of the `services` whose **label selector it matches**.
  - When it’s no longer ready, it’s **removed** from those services.

- `Pods` don’t become `service endpoints` until they’re ready.

---

- **Debatable use case**: use `readiness probe` to check dependency
  - e.g., check the database / cache db ready
  - it makes sense to check if the underlying services are down.
  - however, it also raises problem that once the dependent services are not ready, all the pods are removed from the endpionts, leading that the current pods are unavailabe and take time (successThrehold\*periodSeconds) to recover.
  - As a rule of thumb, `readiness probes` **shouldn’t** test **external dependencies**, but **can test** dependencies **within the same pod**.

---

### Declarative Manifest

- `initialDelaySeconds` field
  - time after starting the container
- `periodSeconds` field
- `failureThreshold` field
- `timeoutSeconds` field
- `successThreshold` field

- `publishNotReadyAddresses` field:
  - `true`:
    - When requires all pods in a group to get `A`, `AAAA`, and `SRV` records **even though they aren’t ready**
    - **nonready pods** are marked as **ready** in both the `Endpoints` and `EndpointSlice` objects.
    - Components like the cluster DNS treat them as ready.

---

### Readiness Probe Types

- `exec probe`
  - executes a process in the container.
  - The `exit code` used to terminate the process **determines** whether the container is **ready** or not.
- ` httpGet probe`

  - sends a `GET` request to the container via HTTP or HTTPS.
  - The **response code** determines the container’s readiness status.
    - successful: `response code` > 200 and < 400
    - fails: `response code` is anything else; or the connection attempt fails

- `tcpSocket probe`
  - **opens a TCP connection** to a specified port on the container.
  - If the connection is established, the container is considered ready.

---

## Lab: Readiness Probe - httpGet

```yaml
# demo-readiness-probe-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-readiness-probe-pod
  labels:
    app: readiness
spec:
  containers:
    - name: nginx
      image: nginx
      readinessProbe:
        httpGet:
          path: /healthz
          port: 80
          scheme: HTTP
        initialDelaySeconds: 5
        periodSeconds: 10
        timeoutSeconds: 2
        failureThreshold: 3
```

```sh
kubectl apply -f demo-readiness-probe-pod.yaml
# pod/demo-readiness-probe-pod created

kubectl get pod
# NAME                       READY   STATUS    RESTARTS      AGE
# demo-readiness-probe-pod   0/1     Running   0             93s

kubectl describe pod demo-readiness-probe-pod
# Labels:           app=readiness
# Containers:
#   nginx:
#     Ready:          False
#     Readiness:      http-get http://:80/ delay=5s timeout=2s period=10s #success=1 #failure=3
# Events:
#   Type     Reason     Age                From               Message
#   ----     ------     ----               ----               -------
#   Normal   Created    110s               kubelet            Created container: nginx
#   Normal   Started    110s               kubelet            Started container nginx
#   Warning  Unhealthy  0s (x11 over 98s)  kubelet            Readiness probe failed: HTTP probe failed with statuscode: 404
```

```yaml
# demo-readiness-probe-svc.yaml
apiVersion: v1
kind: Service
metadata:
  name: demo-readiness-probe-svc
spec:
  type: ClusterIP
  selector:
    app: readiness
  ports:
    - name: http
      protocol: TCP
      port: 8080
      targetPort: 80
```

```sh
kubectl apply -f demo-readiness-probe-svc.yaml
# service/demo-readiness-probe-svc created

kubectl get svc
# NAME                        TYPE           CLUSTER-IP       EXTERNAL-IP        PORT(S)          AGE
# demo-readiness-probe-svc    ClusterIP      10.104.231.1     <none>             8080/TCP         86s

kubectl describe endpointslices demo-readiness-probe-svc
# Name:         demo-readiness-probe-svc-bzspz
# Namespace:    default
# Labels:       endpointslice.kubernetes.io/managed-by=endpointslice-controller.k8s.io
#               kubernetes.io/service-name=demo-readiness-probe-svc
# Annotations:  endpoints.kubernetes.io/last-change-trigger-time: 2025-12-29T21:07:51Z
# AddressType:  IPv4
# Ports:
#   Name  Port  Protocol
#   ----  ----  --------
#   http  80    TCP
# Endpoints:
#   - Addresses:  10.1.3.44
#     Conditions:
#       Ready:    false
#     Hostname:   <unset>
#     TargetRef:  Pod/demo-readiness-probe-pod
#     NodeName:   docker-desktop
#     Zone:       <unset>
# Events:         <none>
```

> endpointslice shows pod but not ready

---

- update yaml

```yaml
# demo-readiness-probe-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-readiness-probe-pod
  labels:
    app: readiness
spec:
  containers:
    - name: nginx
      image: nginx
      readinessProbe:
        httpGet:
          path: / # update path
          port: 80
          scheme: HTTP
        initialDelaySeconds: 5
        periodSeconds: 10
        timeoutSeconds: 2
        failureThreshold: 3
```

```sh
kubectl replace --force -f demo-readiness-probe-pod.yaml
# pod "demo-readiness-probe-pod" deleted from default namespace
# pod/demo-readiness-probe-pod replaced

# confirm
kubectl describe pod/demo-readiness-probe-pod
# Name:             demo-readiness-probe-pod
# Status:           Running
# Containers:
#   nginx:
#     Ready:          False
#     Readiness:      http-get http://:80/ delay=5s timeout=2s period=10s #success=1 #failure=3

kubectl describe svc demo-readiness-probe-svc
# Name:                     demo-readiness-probe-svc
# Namespace:                default
# Labels:                   <none>
# Annotations:              <none>
# Selector:                 app=readiness
# Type:                     ClusterIP
# IP Family Policy:         SingleStack
# IP Families:              IPv4
# IP:                       10.104.231.1
# IPs:                      10.104.231.1
# Port:                     http  8080/TCP
# TargetPort:               80/TCP
# Endpoints:                10.1.3.46:80
# Session Affinity:         None
# Internal Traffic Policy:  Cluster
# Events:                   <none>


kubectl describe endpointslices demo-readiness-probe-svc
# Name:         demo-readiness-probe-svc-bzspz
# Namespace:    default
# Labels:       endpointslice.kubernetes.io/managed-by=endpointslice-controller.k8s.io
#               kubernetes.io/service-name=demo-readiness-probe-svc
# Annotations:  endpoints.kubernetes.io/last-change-trigger-time: 2025-12-29T21:15:31Z
# AddressType:  IPv4
# Ports:
#   Name  Port  Protocol
#   ----  ----  --------
#   http  80    TCP
# Endpoints:
#   - Addresses:  10.1.3.46
#     Conditions:
#       Ready:    true
#     Hostname:   <unset>
#     TargetRef:  Pod/demo-readiness-probe-pod
#     NodeName:   docker-desktop
#     Zone:       <unset>
# Events:         <none>
```
