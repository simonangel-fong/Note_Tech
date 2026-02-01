# Lab: `nginx` Server with `gateway api`

[Back](../../index.md)

- [Lab: `nginx` Server with `gateway api`](#lab-nginx-server-with-gateway-api)
  - [Creating index.html, ConfigMap, and Deployment](#creating-indexhtml-configmap-and-deployment)
  - [Configure Gateway API](#configure-gateway-api)

---

## Creating index.html, ConfigMap, and Deployment

```sh
mkdir -pv ~/web-app
# mkdir: created directory '/home/ubuntuadmin/web-app'

kubectl create ns web-ns
# namespace/web-ns created

tee ~/web-app/index.html<<EOF
<!DOCTYPE html>
<html>
  <head>
    <title>nginx page</title>
  </head>
  <body>
    <h1>Nginx Server</h1>
    <p>This is an nginx page.</p>
</body>
</html>
EOF

kubectl create cm web-cm-index-page -n web-ns --from-file=/home/ubuntuadmin/web-app/index.html
# configmap/web-cm-index-page created

kubectl describe cm web-cm-index-page -n web-ns
# Name:         web-cm-index-page
# Namespace:    web-ns
# Labels:       <none>
# Annotations:  <none>

# Data
# ====
# index.html:
# ----
# <!DOCTYPE html>
# <html>
#   <head>
#     <title>nginx page</title>
#   </head>
#   <body>
#     <h1>Nginx Server</h1>
#     <p>This is an nginx page.</p>
# </body>
# </html>



# BinaryData
# ====

# Events:  <none>

tee ~/web-app/web-deploy.yaml<<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deploy
  namespace: web-ns
spec:
  replicas: 2
  selector:
    matchLabels:
      app: web-deploy
  template:
    metadata:
      labels:
        app: web-deploy
    spec:
      volumes:
      - name: cm-vol
        configMap:
          name: web-cm-index-page
          items:
          - key: index.html
            path: index.html
      containers:
      - image: nginx
        name: nginx
        volumeMounts:
        - name: cm-vol
          mountPath: /usr/share/nginx/html
EOF

kubectl apply -f ~/web-app/web-deploy.yaml
# deployment.apps/web-deploy created

tee ~/web-app/web-svc.yaml<<EOF
apiVersion: v1
kind: Service
metadata:
  name: web-svc
  namespace: web-ns
spec:
  selector:
    app: web-deploy
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
EOF

kubectl apply -f ~/web-app/web-svc.yaml
# service/web-svc created

# testing
kubectl run svc-test --rm -it --image=alpine -n web-ns --restart=Never -- sh
# / # wget http://web-svc
# Connecting to web-svc (10.100.255.88:80)
# saving to 'index.html'
# index.html           100% |**************************************************|   157  0:00:00 ETA
# 'index.html' saved
# / # cat index.html
# <!DOCTYPE html>
# <html>
#   <head>
#     <title>nginx page</title>
#   </head>
#   <body>
#     <h1>Nginx Server</h1>
#     <p>This is an nginx page.</p>
# </body>
# </html>
# / #
```

---

## Configure Gateway API

```sh
# confirm gateway class
kubectl get gatewayclass
# NAME    CONTROLLER                                   ACCEPTED   AGE
# nginx   gateway.nginx.org/nginx-gateway-controller   True       4d22h

# create gateway
tee ~/web-app/web-gw.yaml<<EOF
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
        from: All
EOF

kubectl apply -f ~/web-app/web-gw.yaml
# gateway.gateway.networking.k8s.io/web-gateway created

# confirm
kubectl get gtw -n nginx-gateway
# NAME          CLASS   ADDRESS   PROGRAMMED   AGE
# web-gateway   nginx             True         14s

tee ~/web-app/web-route.yaml<<EOF
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: web-route
  namespace: web-ns
spec:
  parentRefs:
  - name: web-gateway
    namespace: nginx-gateway
  hostnames:
  - "web.mysite.com"
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /
    backendRefs:
    - name: web-svc
      port: 80
EOF

kubectl apply -f ~/web-app/web-route.yaml
# httproute.gateway.networking.k8s.io/web-route created

# confirm
kubectl get httproute -n web-ns
# NAME        HOSTNAMES            AGE
# web-route   ["web.mysite.com"]   58s

# get node ip
kubectl get node -o wide
# NAME           STATUS   ROLES           AGE   VERSION    INTERNAL-IP      EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION      CONTAINER-RUNTIME
# controlplane   Ready    control-plane   5d    v1.32.11   192.168.10.150   <none>        Ubuntu 24.04.3 LTS   6.14.0-37-generic   containerd://1.7.28
# node01         Ready    <none>          5d    v1.32.11   192.168.10.151   <none>        Ubuntu 24.04.3 LTS   6.14.0-37-generic   containerd://1.7.28
# node02         Ready    <none>          5d    v1.32.11   192.168.10.152   <none>        Ubuntu 24.04.3 LTS   6.14.0-37-generic   containerd://1.7.28

# get gateway service port: 30603
kubectl get svc -n nginx-gateway
# NAME                TYPE           CLUSTER-IP       EXTERNAL-IP      PORT(S)        AGE
# nginx-gateway       ClusterIP      10.110.3.253     <none>           443/TCP        4d23h
# web-gateway-nginx   LoadBalancer   10.101.172.191   192.168.10.201   80:30603/TCP   20m

# test: using gateway service: ip + nodeport
curl -i -H 'Host: web.mysite.com' http://192.168.10.151:30603/
# HTTP/1.1 200 OK
# Server: nginx
# Date: Thu, 22 Jan 2026 06:01:15 GMT
# Content-Type: text/html
# Content-Length: 157
# Connection: keep-alive
# Last-Modified: Thu, 22 Jan 2026 05:41:25 GMT
# ETag: "6971b885-9d"
# Accept-Ranges: bytes

# <!DOCTYPE html>
# <html>
#   <head>
#     <title>nginx page</title>
#   </head>
#   <body>
#     <h1>Nginx Server</h1>
#     <p>This is an nginx page.</p>
# </body>
# </html>

# test: using metalLB
curl -i -H 'Host: web.mysite.com' http://192.168.10.201/
# HTTP/1.1 200 OK
# Server: nginx
# Date: Thu, 22 Jan 2026 06:18:24 GMT
# Content-Type: text/html
# Content-Length: 157
# Connection: keep-alive
# Last-Modified: Thu, 22 Jan 2026 05:41:25 GMT
# ETag: "6971b885-9d"
# Accept-Ranges: bytes

# <!DOCTYPE html>
# <html>
#   <head>
#     <title>nginx page</title>
#   </head>
#   <body>
#     <h1>Nginx Server</h1>
#     <p>This is an nginx page.</p>
# </body>
# </html>
```

---
