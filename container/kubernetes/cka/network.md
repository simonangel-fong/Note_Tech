# CKA - Network

[Back](../index.md)

- [CKA - Network](#cka---network)
  - [NetworkPolicy](#networkpolicy)
    - [Task: NetworkPolicy](#task-networkpolicy)
    - [Task: NetworkPolicy](#task-networkpolicy-1)
    - [Task: Network Policy](#task-network-policy)
    - [Task: netpol](#task-netpol)
  - [Service](#service)
    - [Task: svc + Deploy](#task-svc--deploy)
  - [Ingress](#ingress)
    - [Task: Ingress + SVC](#task-ingress--svc)
    - [Task: ingress + svc](#task-ingress--svc-1)
    - [Task: Ingres + svc](#task-ingres--svc)
    - [Task: ing + svc](#task-ing--svc)
  - [CoreDNS](#coredns)
    - [Task: CoreDNS config error](#task-coredns-config-error)
    - [Task: \*\*\*CoreDNS map DNS to IP](#task-coredns-map-dns-to-ip)
    - [Task: \*\*\*svc \& ip.pod lookup](#task-svc--ippod-lookup)
  - [Gateway API](#gateway-api)
    - [Task: \*API GATEWAY + Routhttp](#task-api-gateway--routhttp)
    - [Task: Service](#task-service)
    - [Task: \*\*\*tls gateway](#task-tls-gateway)
    - [Task: Create Gateway API](#task-create-gateway-api)
    - [Task: \*\*\*TLS Gateway](#task-tls-gateway-1)
    - [Task: Gateway API + httproute](#task-gateway-api--httproute)
    - [Task: \*\*\*Migrate from Ingress to Gateway API](#task-migrate-from-ingress-to-gateway-api)

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

### Task: Network Policy

We have `frontend` and `backend` Deploy in separate NS (`frontend` and `backend`). They need to communicate.
Analyze: Inspect the `frontend` and `backend` Deployments to understand their communication requirements.
Apply: From the NetworkPolicy YAML files in the ./netpol/ folder, choose one to apply.
It must:
Allow communication between frontend and backend.
Be as restrictive as possible (least permissive)
Do not delete or change the existing "deny-all" netpol's.
Failure to follow these rules may result in a score reduction or zero.

- setup env

```sh
kubectl create ns frontend
kubectl create deploy frontend -n frontend --image=nginx
kubectl expose deploy frontend -n frontend --name=frontend --port=80

kubectl create ns backend
kubectl create deploy backend -n backend --image=nginx
kubectl expose deploy backend -n backend --name=backend --port=80

mkdir netpol

cat <<'EOF' > ./netpol/deny-all.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
  namespace: frontend
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
  namespace: backend
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
EOF

kubectl apply -f ./netpol/deny-all.yaml
```

---

- Solution

```sh

```

---

### Task: netpol

We have deployed a new pod called np-test-1 and a service called np-test-service. Incoming connections to this service are not working. Troubleshoot and fix it.
Create NetworkPolicy, by the name ingress-to-nptest that allows incoming connections to the service over port 80.

Important: Don't delete any current objects deployed.

```sh
k run np-test-1 --image=nginx
k expose pod np-test-1 --name=np-test-service --port=80
```

---

- solution:

```yaml
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ingress-to-nptest
  namespace: default
spec:
  podSelector:
    matchLabels:
      run: np-test-1
  policyTypes:
    - Ingress
  ingress:
    - ports:
        - protocol: TCP
          port: 80
```

---

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

### Task: Ingres + svc

Create a new Ingress resource echo in echo-sound namespace
Exposing Service echoserver-service on http://example.org/echo using Service port 8080
The availability of Service echoserver-service can be checked

using the following command, which should return 200:
[candidate@cka2025] $ curl -o /dev/null -s -w "%(http_code)\n" http://example.org/echo

- Setup environment

```sh
kubectl create ns echo-sound
kubectl create deploy web --image=nginx -n echo-sound
kubectl expose deploy web --name=echoserver-service -n echo-sound --port=8080 --target-port=80
```

---

- Solution:

```yaml
# echo-ing.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: echo
  namespace: echo-sound
spec:
  rules:
    - host: example.org
      http:
        paths:
          - path: /echo
            pathType: Prefix
            backend:
              service:
                name: echoserver-service
                port:
                  number: 8080
```

```sh
kubectl apply -f ing.yaml

# confirm
kubectl get ing -n echo-sound
# NAME   CLASS    HOSTS         ADDRESS   PORTS   AGE
# echo   <none>   example.org             80      3m30s

kubectl describe ing echo -n echo-sound
# Name:             echo
# Labels:           <none>
# Namespace:        echo-sound
# Address:
# Ingress Class:    <none>
# Default backend:  <default>
# Rules:
#   Host         Path  Backends
#   ----         ----  --------
#   example.org
#                /echo   echoserver-service:8080 (10.244.1.12:80)
# Annotations:   <none>
# Events:        <none>
```

---

### Task: ing + svc

A Deployment named webapp-deploy is running in the ingress-ns namespace and is exposed via a Service named webapp-svc.

Create an Ingress resource called webapp-ingress in the same namespace that will route traffic to the service. The Ingress must:

Use pathType: Prefix
Route requests sent to path / to the backend service
Forward traffic to port 80 of the service
Be configured for the host kodekloud-ingress.app
Test app availablility using the following command:

curl -s http://kodekloud-ingress.app/

- Setup env

```sh
k create ns ingress-ns
k create deploy webapp-deploy -n ingress-ns --image=nginx
k expose deploy webapp-deploy -n ingress-ns --name=webapp-svc --port=80
```

---

- Solution

```sh
k get ingressclass
# NAME    CONTROLLER                     PARAMETERS   AGE
# nginx   nginx.org/ingress-controller   <none>       44h
```

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: webapp-ingress
  namespace: ingress-ns
spec:
  ingressClassName: nginx
  rules:
    - host: kodekloud-ingress.app
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: webapp-svc
                port:
                  number: 80
```

```sh
k apply -f ing.yaml

k describe ing -n ingress-ns
# Name:             webapp-ingress
# Labels:           <none>
# Namespace:        ingress-ns
# Address:
# Ingress Class:    nginx
# Default backend:  <default>
# Rules:
#   Host                   Path  Backends
#   ----                   ----  --------
#   kodekloud-ingress.app
#                          /   webapp-svc:80 (10.244.196.143:80)
# Annotations:             <none>
# Events:
#   Type    Reason          Age    From                      Message
#   ----    ------          ----   ----                      -------
#   Normal  AddedOrUpdated  4m58s  nginx-ingress-controller  Configuration for ingress-ns/webapp-ingress was added or updated
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

### Task: \*\*\*svc & ip.pod lookup

Create an nginx pod named nginx-resolver using the nginx image and expose it internally using a ClusterIP service called nginx-resolver-service.

From within the cluster, verify:

DNS resolution of the service name

Network reachability of the pod using its IP address

Use the busybox:1.28 image to perform the lookups.

Save the service DNS lookup output to ~/nginx.svc and the pod IP lookup output to ~/nginx.pod.

---

- solution

```sh
kubectl run nginx-resolver --image=nginx
# pod/nginx-resolver created

kubectl expose pod nginx-resolver --name=nginx-resolver-service --port=80
# service/nginx-resolver-service exposed

kubectl run --rm -it test --image=busybox:1.28 --restart=Never -- nslookup nginx-resolver-service > ~/nginx.svc

# confirm
cat ~/nginx.svc
# Server:    10.96.0.10
# Address 1: 10.96.0.10 kube-dns.kube-system.svc.cluster.local

# Name:      nginx-resolver-service
# Address 1: 10.100.179.14 nginx-resolver-service.default.svc.cluster.local
# pod "test" deleted

kubectl get pod -o wide
# NAME                                        READY   STATUS    RESTARTS       AGE     IP               NODE     NOMINATED NODE   READINESS GATES
# nginx-resolver                              1/1     Running   0              4m45s   10.244.196.145   node01   <none>           <none>


kubectl run --rm -it test --image=busybox:1.28 --restart=Never -- nslookup 10-244-196-145.default.pod > ~/nginx.pod

cat ~/nginx.pod
# Server:    10.96.0.10
# Address 1: 10.96.0.10 kube-dns.kube-system.svc.cluster.local

# Name:      10-244-196-145.default.pod
# Address 1: 10.244.196.145 10-244-196-145.nginx-resolver-service.default.svc.cluster.local
# pod "test" deleted
```

---

## Gateway API

### Task: \*API GATEWAY + Routhttp

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

### Task: Service

Reconfigure the existing Deployment front-end in namespace sp-culator to expose port 80/tcp of the existing container nginx.
Create a new Service named front-end-svc exposing the container port 80/tcp.
Configure the new Service to also expose the individual pods via & NodePort

- Set

```sh
kubectl create ns sp-culator

tee env-deploy.yaml<<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: front-end
  namespace: sp-culator
spec:
  replicas: 2
  selector:
    matchLabels:
      app: front-end
  template:
    metadata:
      labels:
        app: front-end
    spec:
      containers:
      - name: nginx
        image: nginx
EOF

kubectl apply -f env-deploy.yaml

```

---

- Solution

```sh
kubectl edit deploy front-end -n sp-culator
#         ports:
#         - containerPort: 80
# deployment.apps/front-end edited

kubectl expose deploy front-end -n sp-culator --name=front-end-svc --type=NodePort --port=80 --target-port=80
# service/front-end-svc exposed

kubectl describe svc front-end-svc -n sp-culator
# Name:                     front-end-svc
# Namespace:                sp-culator
# Labels:                   <none>
# Annotations:              <none>
# Selector:                 app=front-end
# Type:                     NodePort
# IP Family Policy:         SingleStack
# IP Families:              IPv4
# IP:                       10.110.48.218
# IPs:                      10.110.48.218
# Port:                     <unset>  80/TCP
# TargetPort:               80/TCP
# NodePort:                 <unset>  31117/TCP
# Endpoints:                10.244.2.12:80,10.244.1.11:80,10.244.2.11:80
# Session Affinity:         None
# External Traffic Policy:  Cluster
# Internal Traffic Policy:  Cluster
# Events:                   <none>
```

---

### Task: \*\*\*tls gateway

Migrate an existing web application from Ingress to Gateway API.
We must maintain HTTPSaccess.
A GatewayClass named `nginx` is installed in the cluster.

First, create a Gateway named `web-gateway` with hostname `gateway.web.k8s.local` that maintains the existing TLS and listener configuration from the **existing ingress** resource named `web`.

Next, create an `HTTPRoute` named **web-route** with hostname `gateway.web.k8s.local` that maintains the existing routing rules from the current **Ingress resource** named `web`.

You can test your Gateway API configuration with the following command:
[candidate@cka2025] $ curl https: //gateway.web.k8s.local
Finally, delete the existing Ingress resource named web.

- Setup ENv

```sh
kubectl create deploy web-app --image=nginx
kubectl expose deploy web-app --port=80 --name=web-svc

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout tls.key -out tls.crt \
  -subj "/CN=gateway.web.k8s.local" \
  -addext "subjectAltName=DNS:gateway.web.k8s.local"

kubectl create secret tls web-tls --cert=tls.crt --key=tls.key

tee ing.yaml<<'EOF'
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-gateway
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - gateway.web.k8s.local
    secretName: web-tls
  rules:
  - host: gateway.web.k8s.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-svc
            port:
              number: 80
EOF

kubectl apply -f ing.yaml

```

---

- SOlution
- ref: https://gateway-api.sigs.k8s.io/guides/tls/

```sh
tee
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: web-gateway
  namespace: default
spec:
  gatewayClassName: nginx
  listeners:
  - name: https
    protocol: HTTPS
    port: 443
    hostname: gateway.web.k8s.local
    tls:
      mode: Terminate
      certificateRefs:
      - kind: Secret
        name: web-tls

# http
cat <<'EOF' | kubectl apply -f -
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: web-route
  namespace: default
spec:
  hostnames:
  - gateway.web.k8s.local
  parentRefs:
  - name: web-gateway
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /
    backendRefs:
    - name: web-svc
      port: 80
EOF


```

---

### Task: Create Gateway API

Create a Kubernetes Gateway resource with the following specifications:

Name: web-gateway
Namespace: nginx-gateway
Gateway Class Name: nginx
Listeners:
Protocol: HTTP
Port: 80
Name: http

---

- Solution

```yaml
# gtw.yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: web-gateway
  namespace: nginx-gateway
spec:
  gatewayClassName: nginx
  listeners:
    - name: http
      protocol: HTTP
      port: 80
      allowedRoutes:
        namespaces:
          from: Same
```

```sh
k apply -f gtw.yaml
# gateway.gateway.networking.k8s.io/web-gateway created

# confirm
k get gtw web-gateway -n nginx-gateway
# NAME          CLASS   ADDRESS   PROGRAMMED   AGE
# web-gateway   nginx             True         77s

k describe gtw web-gateway -n nginx-gateway
# Name:         web-gateway
# Namespace:    nginx-gateway
# Labels:       <none>
# Annotations:  <none>
# API Version:  gateway.networking.k8s.io/v1
# Kind:         Gateway
# Metadata:
#   Creation Timestamp:  2026-01-18T02:46:52Z
#   Generation:          1
#   Resource Version:    20952
#   UID:                 a8bb2632-d268-4858-855b-567213e94d9a
# Spec:
#   Gateway Class Name:  nginx
#   Listeners:
#     Allowed Routes:
#       Namespaces:
#         From:  Same
#     Name:      http
#     Port:      80
#     Protocol:  HTTP
# Status:
#   Conditions:
#     Last Transition Time:  2026-01-18T02:46:52Z
#     Message:               The Gateway is accepted
#     Observed Generation:   1
#     Reason:                Accepted
#     Status:                True
#     Type:                  Accepted
#     Last Transition Time:  2026-01-18T02:46:52Z
#     Message:               The Gateway is programmed
#     Observed Generation:   1
#     Reason:                Programmed
#     Status:                True
#     Type:                  Programmed
#   Listeners:
#     Attached Routes:  0
#     Conditions:
#       Last Transition Time:  2026-01-18T02:46:52Z
#       Message:               The Listener is accepted
#       Observed Generation:   1
#       Reason:                Accepted
#       Status:                True
#       Type:                  Accepted
#       Last Transition Time:  2026-01-18T02:46:52Z
#       Message:               The Listener is programmed
#       Observed Generation:   1
#       Reason:                Programmed
#       Status:                True
#       Type:                  Programmed
#       Last Transition Time:  2026-01-18T02:46:52Z
#       Message:               All references are resolved
#       Observed Generation:   1
#       Reason:                ResolvedRefs
#       Status:                True
#       Type:                  ResolvedRefs
#       Last Transition Time:  2026-01-18T02:46:52Z
#       Message:               No conflicts
#       Observed Generation:   1
#       Reason:                NoConflicts
#       Status:                False
#       Type:                  Conflicted
#     Name:                    http
#     Supported Kinds:
#       Group:  gateway.networking.k8s.io
#       Kind:   HTTPRoute
#       Group:  gateway.networking.k8s.io
#       Kind:   GRPCRoute
# Events:       <none>

```

---

### Task: \*\*\*TLS Gateway

Modify the existing web-gateway on cka5673 namespace to handle HTTPS traffic on port 443 for kodekloud.com, using a TLS certificate stored in a secret named kodekloud-tls.

- Setup env

```sh
kubectl create ns cka5673
# simulate tls secret
mkdir -p ~/cka5673-gw && cd ~/cka5673-gw

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout tls.key -out tls.crt \
  -subj "/CN=kodekloud.com/O=kodekloud"

kubectl -n cka5673 create secret tls kodekloud-tls --cert=tls.crt --key=tls.key
```

```yaml
# gtw.yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: web-gateway
  namespace: cka5673
spec:
  gatewayClassName: nginx
  listeners:
    - name: http
      protocol: HTTP
      port: 80
      allowedRoutes:
        namespaces:
          from: Same
```

```sh
k apply -f gtw.yaml

k get gtw -n cka5673
# NAME          CLASS   ADDRESS   PROGRAMMED   AGE
# web-gateway   nginx             True         13s
```

---

- solution
  - ref: https://gateway-api.sigs.k8s.io/guides/tls/#listeners-and-tls

```sh
# check secret
kubectl get secret -n cka5673
# NAME                          TYPE                DATA   AGE
# kodekloud-tls                 kubernetes.io/tls   2      7m46s

k get gtw -n cka5673
# NAME          CLASS   ADDRESS   PROGRAMMED   AGE
# web-gateway   nginx             True         13s

# output and backup old gtw
k get gtw web-gateway -n cka5673 -o yaml > gtw-tls.yaml
k get gtw web-gateway -n cka5673 -o yaml > gtw.yaml.bak

vi gtw-tls.yaml
# apiVersion: gateway.networking.k8s.io/v1
# kind: Gateway
# metadata:
#   name: web-gateway
#   namespace: cka5673
# spec:
#   gatewayClassName: nginx
#   listeners:
#   - name: https
#     protocol: HTTPS
#     port: 443
#     hostname: kodekloud.com
#     tls:
#       certificateRefs:
#       - kind: Secret
#         name: kodekloud-tls

# replace
k replace --force -f gtw-tls.yaml
# gateway.gateway.networking.k8s.io/web-gateway replaced

k get gtw -n cka5673
# NAME          CLASS   ADDRESS   PROGRAMMED   AGE
# web-gateway   nginx             True         18s

k describe gtw web-gateway -n cka5673
# Name:         web-gateway
# Namespace:    cka5673
# Labels:       <none>
# Annotations:  <none>
# API Version:  gateway.networking.k8s.io/v1
# Kind:         Gateway
# Metadata:
#   Creation Timestamp:  2026-01-19T05:52:11Z
#   Generation:          1
#   Resource Version:    50069
#   UID:                 bb4a24f8-4ed0-45ec-9b10-e2e4ffa7ecab
# Spec:
#   Gateway Class Name:  nginx
#   Listeners:
#     Allowed Routes:
#       Namespaces:
#         From:  Same
#     Hostname:  kodekloud.com
#     Name:      https
#     Port:      443
#     Protocol:  HTTPS
#     Tls:
#       Certificate Refs:
#         Group:
#         Kind:   Secret
#         Name:   kodekloud-tls
#       Mode:     Terminate
# Status:
#   Conditions:
#     Last Transition Time:  2026-01-19T05:52:11Z
#     Message:               The Gateway is accepted
#     Observed Generation:   1
#     Reason:                Accepted
#     Status:                True
#     Type:                  Accepted
#     Last Transition Time:  2026-01-19T05:52:11Z
#     Message:               The Gateway is programmed
#     Observed Generation:   1
#     Reason:                Programmed
#     Status:                True
#     Type:                  Programmed
#   Listeners:
#     Attached Routes:  0
#     Conditions:
#       Last Transition Time:  2026-01-19T05:52:11Z
#       Message:               The Listener is accepted
#       Observed Generation:   1
#       Reason:                Accepted
#       Status:                True
#       Type:                  Accepted
#       Last Transition Time:  2026-01-19T05:52:11Z
#       Message:               The Listener is programmed
#       Observed Generation:   1
#       Reason:                Programmed
#       Status:                True
#       Type:                  Programmed
#       Last Transition Time:  2026-01-19T05:52:11Z
#       Message:               All references are resolved
#       Observed Generation:   1
#       Reason:                ResolvedRefs
#       Status:                True
#       Type:                  ResolvedRefs
#       Last Transition Time:  2026-01-19T05:52:11Z
#       Message:               No conflicts
#       Observed Generation:   1
#       Reason:                NoConflicts
#       Status:                False
#       Type:                  Conflicted
#     Name:                    https
#     Supported Kinds:
#       Group:  gateway.networking.k8s.io
#       Kind:   HTTPRoute
#       Group:  gateway.networking.k8s.io
#       Kind:   GRPCRoute
# Events:       <none>

```

---

### Task: Gateway API + httproute

Configure the web-route to split traffic between web-service and web-service-v2.The configuration should ensure that 80% of the traffic is routed to web-service and 20% is routed to web-service-v2.

Note: web-gateway, web-service, and web-service-v2 have already been created and are available on the cluster.

- setup env

```sh
k create deploy web --image=nginx
k expose deploy web --name=web-service --port=80
k create deploy web-v2 --image=nginx
k expose deploy web-v2 --name=web-service-v2 --port=80

tee gtw.yaml<<EOF
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: web-gateway
  namespace: default
spec:
  gatewayClassName: nginx
  listeners:
  - name: http
    protocol: HTTP
    port: 80
    allowedRoutes:
      namespaces:
        from: Same
EOF

k apply -f gtw.yaml

k get gtw
# NAME          CLASS   ADDRESS   PROGRAMMED   AGE
# web-gateway   nginx             True         8s
```

---

- solution

```sh
tee httproute.yaml<<EOF
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: web-route
  namespace: default
spec:
  parentRefs:
  - name: web-gateway
    namespace: default
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /
    backendRefs:
    - name: web-service
      port: 80
      weight: 80
    - name: web-service-v2
      port: 80
      weight: 20

EOF

k apply -f httproute.yaml
# httproute.gateway.networking.k8s.io/web-route created

k describe gtw web-route
# Name:         web-route
# Namespace:    default
# Labels:       <none>
# Annotations:  <none>
# API Version:  gateway.networking.k8s.io/v1
# Kind:         HTTPRoute
# Metadata:
#   Creation Timestamp:  2026-01-22T01:06:42Z
#   Generation:          1
#   Resource Version:    65276
#   UID:                 a89623d7-4a70-4c74-b47a-84c283090742
# Spec:
#   Parent Refs:
#     Group:      gateway.networking.k8s.io
#     Kind:       Gateway
#     Name:       web-gateway
#     Namespace:  default
#   Rules:
#     Backend Refs:
#       Group:
#       Kind:    Service
#       Name:    web-service
#       Port:    80
#       Weight:  80
#       Group:
#       Kind:    Service
#       Name:    web-service-v2
#       Port:    80
#       Weight:  20
#     Matches:
#       Path:
#         Type:   PathPrefix
#         Value:  /

```

---

### Task: \*\*\*Migrate from Ingress to Gateway API

You have an existing web application deployed in a Kubernetes cluster using an Ingress resource named `web`. You must migrate the existing Ingress configuration to the new Kubernetes Gateway API, maintaining theexisting HTTPS access configuration

Tasks
Create a Gateway Resource named `web-gateway` with hostname `gateway.web.k8s.local` that maintains the exisiting TLS and listener configuration from the existing Ingress resource named web

Create a HTTPRoute resource named `web-route` with hostname `gateway.web.k8s.local` that maintains the existing routing rules from the current Ingress resource named web.

Note: A GatewayClass named nginx is already installed in the cluster

- Setup env

```sh
mkdir ingress-migrate
cd ingress-migrate

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout tls.key -out tls.crt \
  -subj "/CN=gateway.web.k8s.local" \
  -addext "subjectAltName=DNS:gateway.web.k8s.local"

kubectl create secret tls web-tls --cert=tls.crt --key=tls.key

kubectl create deploy web-deploy --image=nginx --replicas=3
kubectl expose deploy web-deploy --name=web-svc --port=80

tee ingress.yaml<<EOF
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web
spec:
  ingressClassName: nginx
  tls:
  - hosts:
      - gateway.web.k8s.local
    secretName: web-tls
  rules:
  - http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-svc
            port:
              number: 80
EOF

kubectl apply -f ingress.yaml
```

---

- Solution

```sh
cat > gtw.yaml<<EOF
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: web-gateway
spec:
  gatewayClassName: nginx
  listeners:
  - name: https
    protocol: HTTPS
    port: 443
    tls:
      certificateRefs:
      - kind: Secret
        name: web-tls
    hostname: "gateway.web.k8s.local"
    allowedRoutes:
      namespaces:
        from: Same
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: web-route
spec:
  parentRefs:
  - name: web-gateway
    sectionName: https
  hostnames:
  - "gateway.web.k8s.local"
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /
    backendRefs:
    - name: web-svc
      port: 80

EOF

kubectl apply -f gtw.yaml

kd gtw web-gateway
# Name:         web-gateway
# Namespace:    default
# Labels:       <none>
# Annotations:  <none>
# API Version:  gateway.networking.k8s.io/v1
# Kind:         Gateway
# Metadata:
#   Creation Timestamp:  2026-01-25T23:15:29Z
#   Generation:          1
#   Resource Version:    88371
#   UID:                 fb04dda5-cf98-45f8-810a-39c0de8e63c2
# Spec:
#   Gateway Class Name:  nginx
#   Listeners:
#     Allowed Routes:
#       Namespaces:
#         From:  Same
#     Hostname:  gateway.web.k8s.local
#     Name:      https
#     Port:      443
#     Protocol:  HTTPS
#     Tls:
#       Certificate Refs:
#         Group:
#         Kind:   Secret
#         Name:   web-tls
#       Mode:     Terminate

kd httproute web-route
# Name:         web-route
# Namespace:    default
# Labels:       <none>
# Annotations:  <none>
# API Version:  gateway.networking.k8s.io/v1
# Kind:         HTTPRoute
# Metadata:
#   Creation Timestamp:  2026-01-25T23:15:29Z
#   Generation:          1
#   Resource Version:    88370
#   UID:                 f5a9a4c8-3100-4b63-bd95-b67bf8303c6c
# Spec:
#   Hostnames:
#     gateway.web.k8s.local
#   Parent Refs:
#     Group:         gateway.networking.k8s.io
#     Kind:          Gateway
#     Name:          web-gateway
#     Section Name:  https
#   Rules:
#     Backend Refs:
#       Group:
#       Kind:    Service
#       Name:    web-svc
#       Port:    80
#       Weight:  1
#     Matches:
#       Path:
#         Type:   PathPrefix
#         Value:  /
```
