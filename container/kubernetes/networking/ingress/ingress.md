# Kubernetes - Ingress

[Back](../../index.md)

- [Kubernetes - Ingress](#kubernetes---ingress)
  - [Ingress](#ingress)
    - [Imperative Command](#imperative-command)
    - [Lab:](#lab)
    - [Lab: create ingress??](#lab-create-ingress)

---

## Ingress

- manages external access to services within the cluster, typically HTTP/HTTPS traffic.

  - It acts as a **smart router** or **entry point** for incoming requests from outside the cluster.

- Ingress Controll
  - handle the ingress deplpoyment
    - e.g., nginx, haproxy, trafik
  - by default, not a built-in component
- Ingress Resources
  - configure the rules of routing.
  - can be defined using definition file

---

- example: using nginx as ingress controller

```yaml
# empty configmap for further conf
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-configuration
---
# ingress controller: nginx
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-ingress-controller
spec:
  replicas: 1
  selector:
    matchLabels:
      name: nginx-ingress
  template:
    metadata:
    labels:
      name: nginx-ingress
  spec:
    containers:
      - name: nginx-ingress-controller
        image: quay.io/kubernetes-ingresscontroller/nginx-ingress-controller:0.21.0
    args:
      - /nginx-ingress-controller
      - --configmap=$(POD_NAMESPACE)/nginx-configuration
    env:
      - name: POD_NAME
        valueFrom:
          fieldRef:
            fieldPath: metadata.name
      - name: POD_NAMESPACE
        valueFrom:
          fieldRef:
            fieldPath: metadata.namespace
    ports:
      - name: http
        containerPort: 80
      - name: https
        containerPort: 443

---
# service in front of ingress
apiVersion: v1
kind: Service
metadata:
  name: nginx-ingress
spec:
  type: NodePort
  selector:
    name: nginx-ingress
  ports:
    - port: 80
      targetPort: 80
      protocol: TCP
      name: http
    - port: 443
      targetPort: 443
      protocol: TCP
      name: https
---
# sa to manage ingress access
apiVersion: v1
kind: ServiceAccount
metadata:
  name: nginx-ingress-serviceaccount
```

---

- Example: ingress resource(the routing rules)

```yaml
# route based on the path
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-wear-watch
spec:
  rules:
    - http:
        paths:
          - path: /wear
            backend:
              service:
                name: wear-service
                port: 80
          - path: /watch
            backend:
              service:
                name: watch-service
                port: 80
```

---

- Example: ingress resource(the routing rules)
  - route for 2 domain name

```yaml
# route based on domain name
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-wear-watch
spec:
  rules:
    # domain name
    - host: wear.my-online-store.com
      http:
        paths:
          - path: /wear
            backend:
              service:
                name: wear-service
                port: 80
    # domain name
    - host: watch.my-online-store.com
      http:
        paths:
          - path: /watch
            backend:
              service:
                name: watch-service
                port: 80
```

---

### Imperative Command

kubectl create ingress <ingress-name> --rule="host/path=service:port"
kubectl create ingress ingress-test --rule="wear.my-online-store.com/wear\*=wear-service:80"

---

### Lab:

```sh
# list ingress resources
kubectl get ingress -A
# NAMESPACE   NAME                 CLASS    HOSTS   ADDRESS          PORTS   AGE
# app-space   ingress-wear-watch   <none>   *       172.20.111.110   80      6m32s

# get details of ingress: host = *, any hosts
kubectl describe ingress ingress-wear-watch -n app-space
# Name:             ingress-wear-watch
# Labels:           <none>
# Namespace:        app-space
# Address:          172.20.111.110
# Ingress Class:    <none>
# Default backend:  <default>
# Rules:
#   Host        Path  Backends
#   ----        ----  --------
#   *
#               /wear    wear-service:8080 (172.17.0.4:8080)
#               /watch   video-service:8080 (172.17.0.5:8080)
# Annotations:  nginx.ingress.kubernetes.io/rewrite-target: /
#               nginx.ingress.kubernetes.io/ssl-redirect: false
# Events:
#   Type    Reason  Age                  From                      Message
#   ----    ------  ----                 ----                      -------
#   Normal  Sync    8m8s (x2 over 8m8s)  nginx-ingress-controller  Scheduled for sync



kubectl get svc pay-service -n critical-space
# NAME          TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
# pay-service   ClusterIP   172.20.22.82   <none>        8282/TCP   10m

kubectl create ingress critical-ingress --rule="/pay=pay-service:8282" -n critical-space -o yaml > pay-ingress.yaml

# add annotation
cat pay-ingress.yaml
# apiVersion: networking.k8s.io/v1
# kind: Ingress
# metadata:
#   creationTimestamp: "2025-12-04T02:55:00Z"
#   generation: 1
#   name: critical-ingress
#   namespace: critical-space
#   resourceVersion: "5829"
#   uid: b689ea3f-2910-4bde-9c44-802c8d108d2a
#   annotations:
#     nginx.ingress.kubernetes.io/rewrite-target: /
# spec:
#   rules:
#   - http:
#       paths:
#       - backend:
#           service:
#             name: pay-service
#             port:
#               number: 8282
#         path: /pay

kubectl create -f pay-ingress.yaml

kubectl describe ingress critical-ingress -n critical-space
# Name:             critical-ingress
# Labels:           <none>
# Namespace:        critical-space
# Address:          172.20.111.110
# Ingress Class:    <none>
# Default backend:  <default>
# Rules:
#   Host        Path  Backends
#   ----        ----  --------
#   *
#               /pay   pay-service:8282 (172.17.0.11:8080)
# Annotations:  <none>
# Events:
#   Type    Reason  Age                From                      Message
#   ----    ------  ----               ----                      -------
#   Normal  Sync    30s (x2 over 36s)  nginx-ingress-controller  Scheduled for sync
```

---

### Lab: create ingress??

```sh
# create ns for ingress
kubectl create ns ingress-nginx
# namespace/ingress-nginx created

# create configMap
kubectl create configmap ingress-nginx-controller -n ingress-nginx
# configmap/ingress-nginx-controller created

# create service account
kubectl create sa ingress-nginx -n ingress-nginx
# serviceaccount/ingress-nginx created
kubectl create sa ingress-nginx-admission -n ingress-nginx
# serviceaccount/ingress-nginx-admission created

# create ingress
kubectl create ingress ingress-wear
```
