# Lab: `nginx` Server with `ingress`

[Back](../../index.md)

- [Lab: `nginx` Server with `ingress`](#lab-nginx-server-with-ingress)
  - [Creating index.html, ConfigMap, and Deployment](#creating-indexhtml-configmap-and-deployment)
  - [Create Ingress](#create-ingress)
  - [Create TLS Ingress](#create-tls-ingress)

---

## Creating index.html, ConfigMap, and Deployment

```sh
mkdir -pv ~/web-app/html
# mkdir: created directory '/home/ubuntuadmin/web-app/html'

tee ~/web-app/html/index_a.html<<EOF
{"url":"index a"}
EOF

tee ~/web-app/html/index_b.html<<EOF
{"url":"index b"}
EOF

tee ~/web-app/html/index_c.html<<EOF
{"url":"index c"}
EOF

kubectl create ns web-ns
# namespace/web-ns created

kubectl create cm web-cm-page -n web-ns --from-file=index_a=/home/ubuntuadmin/web-app/html/index_a.html --from-file=index_b=/home/ubuntuadmin/web-app/html/index_b.html --from-file=index_c=/home/ubuntuadmin/web-app/html/index_c.html
# configmap/web-cm-page created

kubectl describe cm web-cm-page -n web-ns
# Name:         web-cm-page
# Namespace:    web-ns
# Labels:       <none>
# Annotations:  <none>

# Data
# ====
# index_a:
# ----
# {"url":"index a"}


# index_b:
# ----
# {"url":"index b"}


# index_c:
# ----
# {"url":"index c"}



# BinaryData
# ====

# Events:  <none>

tee ~/web-app/web-deploy.yaml<<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deploy-a
  namespace: web-ns
spec:
  replicas: 2
  selector:
    matchLabels:
      app: web-deploy-a
  template:
    metadata:
      labels:
        app: web-deploy-a
    spec:
      volumes:
      - name: cm-vol
        configMap:
          name: web-cm-page
          items:
          - key: index_a
            path: index.html
      containers:
      - image: nginx
        name: nginx
        volumeMounts:
        - name: cm-vol
          mountPath: /usr/share/nginx/html
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deploy-b
  namespace: web-ns
spec:
  replicas: 2
  selector:
    matchLabels:
      app: web-deploy-b
  template:
    metadata:
      labels:
        app: web-deploy-b
    spec:
      volumes:
      - name: cm-vol
        configMap:
          name: web-cm-page
          items:
          - key: index_b
            path: index.html
      containers:
      - image: nginx
        name: nginx
        volumeMounts:
        - name: cm-vol
          mountPath: /usr/share/nginx/html
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deploy-c
  namespace: web-ns
spec:
  replicas: 2
  selector:
    matchLabels:
      app: web-deploy-c
  template:
    metadata:
      labels:
        app: web-deploy-c
    spec:
      volumes:
      - name: cm-vol
        configMap:
          name: web-cm-page
          items:
          - key: index_c
            path: index.html
      containers:
      - image: nginx
        name: nginx
        volumeMounts:
        - name: cm-vol
          mountPath: /usr/share/nginx/html
EOF

kubectl apply -f ~/web-app/web-deploy.yaml
# deployment.apps/web-deploy-a created
# deployment.apps/web-deploy-b created
# deployment.apps/web-deploy-c created

tee ~/web-app/web-svc.yaml<<EOF
apiVersion: v1
kind: Service
metadata:
  name: web-svc-a
  namespace: web-ns
spec:
  selector:
    app: web-deploy-a
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: web-svc-b
  namespace: web-ns
spec:
  selector:
    app: web-deploy-b
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: web-svc-c
  namespace: web-ns
spec:
  selector:
    app: web-deploy-c
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
EOF

kubectl apply -f ~/web-app/web-svc.yaml
# service/web-svc-a created
# service/web-svc-b created
# service/web-svc-c created

# testing
kubectl run curltest --rm -it --image=curlimages/curl -n web-ns --restart=Never -- sh -c "curl http://web-svc-a; curl http://web-svc-b; curl http://web-svc-c"
# {"url":"index a"}
# {"url":"index b"}
# {"url":"index c"}
# pod "curltest" deleted
```

---

## Create Ingress

```sh
kubectl get ingressclass
# NAME    CONTROLLER                     PARAMETERS   AGE
# nginx   nginx.org/ingress-controller   <none>       5d13h

# install ingress
tee ~/web-app/web-ingress.yaml<<'EOF'
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-ing
  namespace: web-ns
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: app.mysite.com
    http:
      paths:
      - pathType: Prefix
        path: "/"
        backend:
          service:
            name: web-svc-a
            port:
              number: 80
  - host: web.mysite.com
    http:
      paths:
      - path: /bar
        pathType: Prefix
        backend:
          service:
            name: web-svc-c
            port:
              number: 80
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-svc-b
            port:
              number: 80
EOF

kubectl apply -f ~/web-app/web-ingress.yaml
# ingress.networking.k8s.io/web-ing created

kubectl get ingress -n web-ns
# NAME      CLASS   HOSTS                           ADDRESS   PORTS   AGE
# web-ing   nginx   app.mysite.com,web.mysite.com             80      7s
```

- Test

```sh
# get node ip
kubectl get node -o wide
# NAME           STATUS   ROLES           AGE     VERSION    INTERNAL-IP      EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION      CONTAINER-RUNTIME
# controlplane   Ready    control-plane   5d23h   v1.32.11   192.168.10.150   <none>        Ubuntu 24.04.3 LTS   6.14.0-37-generic   containerd://1.7.28
# node01         Ready    <none>          5d23h   v1.32.11   192.168.10.151   <none>        Ubuntu 24.04.3 LTS   6.14.0-37-generic   containerd://1.7.28
# node02         Ready    <none>          5d23h   v1.32.11   192.168.10.152   <none>        Ubuntu 24.04.3 LTS   6.14.0-37-generic   containerd://1.7.28

# get ingress svc ip and port
kubectl -n ingress-nginx get svc ingress-nginx-controller
# NAME                       TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
# ingress-nginx-controller   LoadBalancer   10.102.142.89   <pending>     80:31043/TCP,443:32723/TCP   7h53m

# Internal Test
kubectl run curltest --rm -it --image=curlimages/curl -n web-ns --restart=Never -- sh -c "curl -s -H 'Host: app.mysite.com' http://10.102.142.89; curl -s -H 'Host: web.mysite.com' http://10.102.142.89; curl -s -H 'Host: web.mysite.com' http://10.102.142.89/bar/"
# {"url":"index a"}
# {"url":"index b"}
# {"url":"index c"}
# pod "curltest" deleted

# External Test
curl -H "Host: app.mysite.com" http://192.168.10.150:31043/
# {"url":"index a"}
curl -H "Host: web.mysite.com" http://192.168.10.150:31043/
# {"url":"index b"}
curl -H "Host: web.mysite.com" http://192.168.10.150:31043/bar
# {"url":"index c"}

```

---

## Create TLS Ingress

```sh
# create key and crt: app.tls-domain.com
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout app.tls.key \
  -out app.tls.crt \
  -subj "/CN=app.tls-domain.com" \
  -addext "subjectAltName=DNS:app.tls-domain.com"

# create key and crt: web.tls-domain.com
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout web.tls.key \
  -out web.tls.crt \
  -subj "/CN=web.tls-domain.com" \
  -addext "subjectAltName=DNS:web.tls-domain.com"

# create secret
kubectl create secret tls tls-app-tls-domain --cert=app.tls.crt --key=app.tls.key
# secret/tls-app-tls-domain created
kubectl create secret tls tls-web-tls-domain --cert=web.tls.crt --key=web.tls.key
# secret/tls-web-tls-domain created

# create ingress
tee ~/web-app/web-ingress-tls.yaml<<'EOF'
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-ing-tls
  namespace: web-ns
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  tls:
  - hosts:
      - app.tls-domain.com
    secretName: tls-app-tls-domain
  - hosts:
      - web.tls-domain.com
    secretName: tls-web-tls-domain
  rules:
  - host: app.tls-domain.com
    http:
      paths:
      - pathType: Prefix
        path: "/"
        backend:
          service:
            name: web-svc-a
            port:
              number: 80
  - host: web.tls-domain.com
    http:
      paths:
      - path: /bar
        pathType: Prefix
        backend:
          service:
            name: web-svc-c
            port:
              number: 80
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-svc-b
            port:
              number: 80
EOF

kubectl apply -f ~/web-app/web-ingress-tls.yaml
# ingress.networking.k8s.io/web-ing-tls created

kubectl get ingress -n web-ns
# NAME          CLASS   HOSTS                                   ADDRESS   PORTS     AGE
# web-ing-tls   nginx   app.tls-domain.com,web.tls-domain.com             80, 443   3m
```

- Testing

```sh
# get node ip
kubectl get node -o wide
# NAME           STATUS   ROLES           AGE     VERSION    INTERNAL-IP      EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION      CONTAINER-RUNTIME
# controlplane   Ready    control-plane   5d23h   v1.32.11   192.168.10.150   <none>        Ubuntu 24.04.3 LTS   6.14.0-37-generic   containerd://1.7.28
# node01         Ready    <none>          5d23h   v1.32.11   192.168.10.151   <none>        Ubuntu 24.04.3 LTS   6.14.0-37-generic   containerd://1.7.28
# node02         Ready    <none>          5d23h   v1.32.11   192.168.10.152   <none>        Ubuntu 24.04.3 LTS   6.14.0-37-generic   containerd://1.7.28

# get ingress svc ip and port
kubectl -n ingress-nginx get svc ingress-nginx-controller
# NAME                       TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
# ingress-nginx-controller   LoadBalancer   10.102.142.89   <pending>     80:31043/TCP,443:32723/TCP   7h53m

# Internal Test
kubectl run curltest --rm -it --image=curlimages/curl -n web-ns --restart=Never -- sh -c 'curl -k -H "Host: app.tls-domain.com" https://10.102.142.89/; curl -k -H "Host: web.tls-domain.com" https://10.102.142.89/; curl -k -H "Host: web.tls-domain.com" https://10.102.142.89/bar/'
# {"url":"index a"}
# {"url":"index b"}
# {"url":"index c"}
# pod "curltest" deleted

# External Test
curl -k -H "Host: app.tls-domain.com" https://192.168.10.151:32723/
# {"url":"index a"}
curl -k -H "Host: web.tls-domain.com" https://192.168.10.151:32723/
# {"url":"index b"}
curl -k -H "Host: web.tls-domain.com" https://192.168.10.151:32723/bar
# {"url":"index c"}

```

---
