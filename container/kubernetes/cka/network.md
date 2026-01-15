# CKA - Network

[Back](../index.md)

- [CKA - Network](#cka---network)
  - [NetworkPolicy](#networkpolicy)
    - [Task: NetworkPolicy](#task-networkpolicy)
    - [Task: NetworkPolicy](#task-networkpolicy-1)
  - [Service](#service)
    - [Task: svc + Deploy](#task-svc--deploy)
  - [Ingress](#ingress)
    - [Task: Ingress + SVC](#task-ingress--svc)
    - [Task: ingress + svc](#task-ingress--svc-1)
  - [CoreDNS](#coredns)
    - [Task: CoreDNS config error](#task-coredns-config-error)
    - [Task: \*\*\*CoreDNS map DNS to IP](#task-coredns-map-dns-to-ip)
  - [Gateway API](#gateway-api)
    - [Task: API GATEWAY + Routhttp](#task-api-gateway--routhttp)

---

## NetworkPolicy

### Task: NetworkPolicy

CKA EXAM OBJECTIVE: Define and enforce Network Policies
Task :

1. In namespace cherry you'll find two deployments named pit and stem. Both deployments are exposed via a service.
2. Make a NetworkPolicy named cherry-control that:
3. that prevents outgoing traffic from deployment pit ...
4. ... EXCEPT to that of deployment stem.

```sh
k create ns cherry
k create deploy pit -n cherry --image=nginx
k expose deploy pit -n cherry --port=80
k create deploy stem -n cherry --image=nginx
k expose deploy stem -n cherry --port=80

k get all -n cherry
```

---

- Solution

```yaml
# task-networkpolicy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: cherry-control
  namespace: cherry
spec:
  podSelector:
    matchLabels:
      app: pit
  policyTypes:
    - Egress
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: stem
```

```sh
k apply -f task-networkpolicy.yaml
# networkpolicy.networking.k8s.io/cherry-control created

k describe networkpolicy cherry-control -n cherry
# Name:         cherry-control
# Namespace:    cherry
# Created on:   2026-01-11 17:01:03 -0500 EST
# Labels:       <none>
# Annotations:  <none>
# Spec:
#   PodSelector:     app=pit
#   Not affecting ingress traffic
#   Allowing egress traffic:
#     To Port: <any> (traffic allowed to all ports)
#     To:
#       PodSelector: app=stem
#   Policy Types: Egress
```

---

### Task: NetworkPolicy

Create a new NetworkPolicy named allow-port-from-namespace in the existing namespace fubar.
Ensure that the new NetworkPolicy allows Pods in namespace internal to connect to port 9000 of Pods in namespace fubar.
Further ensure that the new NetworkPolicy:
✑ does not allow access to Pods, which don't listen on port 9000
✑ does not allow access from Pods, which are not in namespace internal

- Setup environment

```sh
kubectl create ns fubar
kubectl create ns internal
```

---

- Solution

```yaml
# networkpolicy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-port-from-namespace
  namespace: fubar
spec:
  podSelector: {} # all pod in the ns
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector: # ns
            matchLabels:
              kubernetes.io/metadata.name: internal # use target ns name
      ports:
        - protocol: TCP
          port: 9000 # only listened port
```

```sh
kubectl apply -f networkpolicy.yaml
# networkpolicy.networking.k8s.io/allow-port-from-namespace created

# confirm
kubectl describe ns internal
# Name:         internal
# Labels:       kubernetes.io/metadata.name=internal
# Annotations:  <none>
# Status:       Active
# No resource quota.
# No LimitRange resource.

kubectl describe networkpolicy allow-port-from-namespace -n fubar
# Name:         allow-port-from-namespace
# Namespace:    fubar
# Created on:   2026-01-09 00:16:16 -0500 EST
# Labels:       <none>
# Annotations:  <none>
# Spec:
#   PodSelector:     <none> (Allowing the specific traffic to all pods in this namespace)
#   Allowing ingress traffic:
#     To Port: 9000/TCP
#     From:
#       NamespaceSelector: kubernetes.io/metadata.name=internal
#   Not affecting egress traffic
#   Policy Types: Ingress
```

---

## Service

### Task: svc + Deploy

Reconfigure the existing deployment front-end and add a port specification named http
exposing port 80/tcp of the existing container nginx.
Create a new service named front-end-svc exposing the container port http.
Configure the new service to also expose the individual Pods via a NodePort on the nodes on which they are scheduled.

- Setup environment

```sh
kubectl create deploy front-end --image=nginx --port=80 --replicas=4
kubectl rollout status deploy/front-end
# deployment "front-end" successfully rolled out
```

---

- Solution

- ref: https://kubernetes.io/docs/tasks/access-application-cluster/service-access-application-cluster/

```sh
# ##############################
# Collect info
# ##############################
kubectl get deploy front-end
kubectl get deploy front-end -o yaml

# ##############################
# Solution: update deployment
# ##############################
# output and save the manifest
kubectl get deploy front-end -o yaml > front-end.yaml.bak

# update deploy
kubectl edit deploy front-end
# kind: Deployment
# spec:
#     spec:
#       containers:
#       - image: nginx
#         name: nginx
#         ports:
#         - name: http
#           containerPort: 80
#           protocol: TCP
# deployment.apps/front-end edited

# confirm config
kubectl get deploy front-end -o yaml
# spec:
#   containers:
#   - image: nginx
#     name: nginx
#     ports:
#     - containerPort: 80
#       name: http
#       protocol: TCP

# ##############################
# Solution: Create svc
# ##############################
kubectl expose deploy front-end --name=front-end-svc --type=NodePort --port=80 --target-port=http --protocol=TCP
# service/front-end-svc exposed

# check endpoint ip = pod ip
kubectl describe svc front-end-svc
# Endpoints:                10.244.1.115:80,10.244.1.118:80,10.244.1.116:80 + 1 more...

# confirm the pod ips
kubectl get pod -l app=front-end -o custom-columns=Name:metadata.name,IP:status.podIP
# Name                         IP
# front-end-69c7557dd4-ck89j   10.244.1.116
# front-end-69c7557dd4-jcpb7   10.244.1.115
# front-end-69c7557dd4-qkppv   10.244.1.118
# front-end-69c7557dd4-vbtwf   10.244.1.117
```

---

## Ingress

### Task: Ingress + SVC

create an Ingress resource named luau that routes traffic on the path /aloha to the aloha service on port 54321

---

- Solution

```yaml
# task-ingress02.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: luau
spec:
  rules:
    - http:
        paths:
          - path: /aloha
            pathType: Prefix
            backend:
              service:
                name: aloha
                port:
                  number: 54321
```

```sh
k apply -f task-ingress02.yaml
# ingress.networking.k8s.io/luau created

k describe ing luau
# Name:             luau
# Labels:           <none>
# Namespace:        default
# Address:
# Ingress Class:    traefik-app
# Default backend:  <default>
# Rules:
#   Host        Path  Backends
#   ----        ----  --------
#   *
#               /aloha   aloha:54321 (<error: services "aloha" not found>)
# Annotations:  <none>
# Events:       <none>
```

---

### Task: ingress + svc

如下创建一个新的 nginx Ingress 资源：
名称: ping
Namespace: ing-internal01
使用服务端口 8080 在路径 /hello 上公开服务 hello

可以使用以下命令检查服务 hello 的可用性，该命令应返回 hello：
curl -kL <INTERNAL_IP>/hello

- Env config

```sh
kubectl create ns ing-internal
# namespace/ing-internal created

kubectl create deploy hello -n ing-internal --image=nginx --port=80
# deployment.apps/hello created
kubectl expose deploy hello -n ing-internal --name=hello --port=8080 --target-port=80
# service/hello exposed

# confirm
kubectl run env-test -n ing-internal --rm -it --image=curlimages/curl --restart=Never -- curl -s http://hello:8080

```

---

- Solution

- ref: https://kubernetes.io/docs/concepts/services-networking/ingress/

```sh
# ##############################
# Collect info
# ##############################
# check ingressclass
kubectl get ingressclass
# No resources found

kubectl get svc -n ing-internal
# NAME    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
# hello   ClusterIP   10.100.201.36   <none>        8080/TCP   8m44s
curl -kL 10.100.201.36/hello

kubectl create ing ping -n ing-internal --rule="/hello=hello:8080" --dry-run=client -o yaml > ing.yaml
# apiVersion: networking.k8s.io/v1
# kind: Ingress
# metadata:
#   name: ping
#   namespace: ing-internal
# spec:
#   rules:
#   - http:
#       paths:
#       - path: /hello
#         pathType: Prefix
#         backend:
#           service:
#             name: hello
#             port:
#               number: 8080

# create manifest
kubectl apply -f ing.yaml
# ingress.networking.k8s.io/ping created

# confirm
kubectl get ingress -n ing-internal
# NAME   CLASS    HOSTS   ADDRESS   PORTS   AGE
# ping   <none>   *                 80      112s

# confirm
kubectl describe ing ping -n ing-internal
# Name:             ping
# Labels:           <none>
# Namespace:        ing-internal
# Address:
# Ingress Class:    <none>
# Default backend:  <default>
# Rules:
#   Host        Path  Backends
#   ----        ----  --------
#   *
#               /hello   hello:8080 (10.244.2.81:80)
# Annotations:  <none>
# Events:       <none>


# confirm
kubectl get svc hello -n ing-internal -o wide
# NAME    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE   SELECTOR
# hello   ClusterIP   10.100.58.252   <none>        8080/TCP   29m   app=hello
kubectl get pod -n ing-internal -l app=hello -o wide
# NAME                     READY   STATUS    RESTARTS   AGE   IP            NODE     NOMINATED NODE   READINESS GATES
# hello-5f8f7fff68-vkf6d   1/1     Running   0          29m   10.244.2.81   node02   <none>           <none>

```

---

## CoreDNS

### Task: CoreDNS config error

DNS lookups are failing in the cluster.
Inverstigate and repair CoreDNS.

---

- Solution

```sh
# troubleshooting

# list all dns pod
kubectl get pod -n kube-system | grep coredns

kubectl logs -n kube-system coredns-***
# locate the error
# locate the configuration file with cm
# commonly, it is the error in the configuration file

# edit the configmap
kubectl edit configmap coredns -n kube-system
# correct the file

# remove the pod
kubectl delete pod corddns-***

# confirm new pod is correct
kubect get pod -n kube-system | grep coredns


```

---

### Task: \*\*\*CoreDNS map DNS to IP

Cluster workloads need to resolve a custom domain internally.
Configure CoreDNS such that any DNS query for `myapp.internal` returns the IP address `10.10.10.10`.
After configuration, pods in the cluster should be able to esolve myapp. internal' to '10.10.10.10'.

---

- Solution

- ref: https://kubernetes.io/docs/tasks/administer-cluster/dns-custom-nameservers/

```sh
# update coredns configmap
kubectl -n kube-system edit configmap coredns
#         hosts {
#           10.10.10.10 myapp.internal
#           fallthrough
#         }
# configmap/coredns edited

# remove the old dns pod
kubectl get pod -n kube-system | grep dns
# coredns-66bc5c9577-n9hg7               1/1     Running   1 (21h ago)   38h
# coredns-66bc5c9577-zrj2k               1/1     Running   1 (21h ago)   38h

kubectl delete pod coredns-66bc5c9577-n9hg7 coredns-66bc5c9577-zrj2k -n kube-system
# pod "coredns-66bc5c9577-n9hg7" deleted from kube-system namespace
# pod "coredns-66bc5c9577-zrj2k" deleted from kube-system namespace

# confirm new dns pod created
kubectl get pod -n kube-system | grep dns
# coredns-66bc5c9577-tcbx4               1/1     Running   0             48s
# coredns-66bc5c9577-vwg9j               1/1     Running   0             48s

# test
kubectl run --rm -it dns-client --image=busybox --restart=Never -- nslookup myapp.internal
# Server:         10.96.0.10
# Address:        10.96.0.10:53


# Name:   myapp.internal
# Address: 10.10.10.10

```

---

## Gateway API

### Task: API GATEWAY + Routhttp

Your cluster uses the Gateway API for ingress traffic.
A service named web-service is running in the default namespace on port 80.
A Gateway API-compatible controller is already installed, and a
GatewayClass named example-gw-class is available in the cluster.

Objective:
Use Gateway API resources to expose web-service externally on HTTP port 80,
routed via the hostname web.example.com.

- setup env

```sh
kubectl create deploy web --image=nginx --replicas=2

kubectl expose deploy web --name=web-service  --port=80 --target-port=80
```

---

- Solution

```yaml
# task-gwapi.yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: web-gateway
spec:
  gatewayClassName: example-gw-class
  listeners:
    - name: http
      protocol: HTTP
      port: 80
      hostname: "web.example.com"
      allowedRoutes:
        namespaces:
          from: Same
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: web-httproute
spec:
  parentRefs:
    - name: web-gateway
      sectionName: http
  hostnames:
    - "web.example.com"
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /
      backendRefs:
        - name: web-service
          port: 80
```

```sh
kubectl apply -f task-gwapi.yaml
# gateway.gateway.networking.k8s.io/web-gateway created
# httproute.gateway.networking.k8s.io/web-httproute created

# get svc port
kubectl get svc -n

```

---
