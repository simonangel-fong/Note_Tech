# CKA - Network

[Back](../index.md)

- [CKA - Network](#cka---network)
  - [NetworkPolicy](#networkpolicy)
    - [Task](#task)
      - [Solution](#solution)
  - [Service](#service)
    - [Task](#task-1)
      - [Solution](#solution-1)
  - [Ingress](#ingress)
    - [Task](#task-2)
    - [Solution](#solution-2)

---

## NetworkPolicy

### Task

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

#### Solution

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

### Task

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

#### Solution

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

### Task

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

### Solution

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
