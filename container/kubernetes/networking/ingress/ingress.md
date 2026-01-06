# Kubernetes Networking: Ingress

[Back](../../index.md)

- [Kubernetes Networking: Ingress](#kubernetes-networking-ingress)
  - [Ingress](#ingress)
    - [Ingress Controller](#ingress-controller)
    - [Default Backend](#default-backend)
    - [Imperative Commands](#imperative-commands)
    - [Lab: Install `Nginx Ingress Controller`](#lab-install-nginx-ingress-controller)
    - [Lab: Create ingress](#lab-create-ingress)
    - [Lab: Multiple Paths with services](#lab-multiple-paths-with-services)
  - [TLS](#tls)
    - [TLS passthrough](#tls-passthrough)
    - [Terminating TLS at the ingress](#terminating-tls-at-the-ingress)
    - [Lab: enable TLS in ingress](#lab-enable-tls-in-ingress)
  - [Customizing Ingress using annotations](#customizing-ingress-using-annotations)
    - [Lab: Cookie-based session affinity](#lab-cookie-based-session-affinity)
  - [Ingress class](#ingress-class)
  - [Custom Resources as Backend](#custom-resources-as-backend)

---

## Ingress

- Limitation of service:

  - becomes problematic with large numbers of `services`, since each service needs its own public IP address.

- `Ingress`

  - an API object that **manages external access** to `services` within a Kubernetes cluster, typically using `HTTP` and `HTTPS` protocols.
  - used to expose multiple services with a single IP address

- Additional features:

  - **HTTP authentication**,
  - **cookie-based session affinity**,
  - **URL rewriting**

- An `Ingress object` **typically handles traffic** for **all** `Service objects` in a particular `Kubernetes namespace`.

  - **multiple** `Ingresses` are also an **option**.

- each `Ingress object` gets its own **IP address**

  - some **ingress implementations** use a **shared entrypoint** for all `Ingress objects`

- **Note that** the `proxy` **doesn’t** send the request to the `service IP`, but **directly to the pod**.

![pic](./pic/ingress_pod.png)

- `ingress` **forward the request** based on the **path** to different `services`

---

### Ingress Controller

- `Ingress Controller`

  - a cluster add-on component
  - a specialized, **Layer 7 load balancer** and **reverse proxy** that manages external traffic into cluster, routing it to the correct **internal services** based on rules.
  - link between the `Ingress object` and the actual **physical ingress** (the reverse proxy)
  - popular e.g., nginx, haproxy, trafik

- **Common Controllers**

  - Google Kubernetes Engine: `GLBC (GCE L7 Load Balancer)`
  - AWS: `AWS Load Balancer Controller`
  - Azure: `AGIC (Application Gateway Ingress Controller)`

- Nginx ingress controller: https://kubernetes.github.io/ingress-nginx/deploy/

---

### Default Backend

- If the client request **doesn’t match any rules** defined in the `Ingress object`, the response **404 Not Found** is normally returned.
- can define a `default backend` to which the ingress should forward the request if no rules are matched.

  - The default backend serves as a catch-all rule.

- `spec.defaultBackend` field

```yaml
spec:
  defaultBackend:
    service:
      name: fun404
      port:
        name: http
  rules:
    # ...
```

---

### Imperative Commands

| CMD                                                             | DESC                                                    |
| --------------------------------------------------------------- | ------------------------------------------------------- |
| `kubectl explain ingress`                                       | Show ingress API structure                              |
| `kubectl get ingress`                                           | List all ingress resources in current namespace         |
| `kubectl get ingress -A`                                        | List ingress in all namespaces                          |
| `kubectl describe ingress <name>`                               | Show rules, backend services, TLS, annotations          |
| `kubectl create ingress <name> --rule=host/path=svc:port`       | Create ingress imperatively                             |
| `kubectl edit ingress <name>`                                   | Edit ingress live                                       |
| `kubectl delete ingress <name>`                                 | Delete an ingress                                       |
| `kubectl logs -n ingress-nginx deploy/ingress-nginx-controller` | View ingress controller logs                            |
| `kubectl get svc -n ingress-nginx`                              | View ingress controller service (LoadBalancer/NodePort) |

---

### Lab: Install `Nginx Ingress Controller`

```sh
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.14.1/deploy/static/provider/cloud/deploy.yaml
# namespace/ingress-nginx created
# serviceaccount/ingress-nginx created
# serviceaccount/ingress-nginx-admission created
# role.rbac.authorization.k8s.io/ingress-nginx created
# role.rbac.authorization.k8s.io/ingress-nginx-admission created
# clusterrole.rbac.authorization.k8s.io/ingress-nginx created
# clusterrole.rbac.authorization.k8s.io/ingress-nginx-admission created
# rolebinding.rbac.authorization.k8s.io/ingress-nginx created
# rolebinding.rbac.authorization.k8s.io/ingress-nginx-admission created
# clusterrolebinding.rbac.authorization.k8s.io/ingress-nginx created
# clusterrolebinding.rbac.authorization.k8s.io/ingress-nginx-admission created
# configmap/ingress-nginx-controller created
# service/ingress-nginx-controller created
# service/ingress-nginx-controller-admission created
# deployment.apps/ingress-nginx-controller created
# job.batch/ingress-nginx-admission-create created
# job.batch/ingress-nginx-admission-patch created
# ingressclass.networking.k8s.io/nginx created
# validatingwebhookconfiguration.admissionregistration.k8s.io/ingress-nginx-admission created

# confirm
get pods --namespace=ingress-nginx
# NAME                                        READY   STATUS    RESTARTS   AGE
# ingress-nginx-controller-59bc454dc9-mdqtz   1/1     Running   0          51s
```

- Local testing

```sh
kubectl create deployment demo --image=httpd --port=80
# deployment.apps/demo created
kubectl expose deployment demo
# service/demo exposed

kubectl get svc
# NAME                        TYPE           CLUSTER-IP       EXTERNAL-IP        PORT(S)          AGE
# demo                        ClusterIP      10.105.59.62     <none>             80/TCP           9s

kubectl create ingress demo-localhost --class=nginx --rule="demo.localdev.me/*=demo:80"
# ingress.networking.k8s.io/demo-localhost created

kubectl port-forward --namespace=ingress-nginx service/ingress-nginx-controller 8080:80
# Forwarding from 127.0.0.1:8080 -> 80
# Forwarding from [::1]:8080 -> 80

# test
curl --resolve demo.localdev.me:8080:127.0.0.1 http://demo.localdev.me:8080
# <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
# <html>
# <head>
# <title>It works! Apache httpd</title>
# </head>
# <body>
# <p>It works!</p>
# </body>
# </html>
```

---

### Lab: Create ingress

```yaml
# demo-ingress-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-ingress-pod
  labels:
    app: nginx
spec:
  containers:
    - name: nginx
      image: nginx
```

```yaml
# demo-ingress-svc.yaml
apiVersion: v1
kind: Service
metadata:
  name: demo-ingress-svc
spec:
  type: ClusterIP
  selector:
    app: nginx
  ports:
    - name: http
      protocol: TCP
      port: 8080
      targetPort: 80
```

```yaml
# demo-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: demo-ingress
spec:
  ingressClassName: nginx
  rules:
    - host: demo-host
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: demo-ingress-svc # match svc
                port:
                  name: http # match port name in svc
```

```sh
kubectl apply -f demo-ingress-pod.yaml
# pod/demo-ingress-pod created

kubectl get pod
# NAME               READY   STATUS    RESTARTS   AGE    IP          NODE             NOMINATED NODE   READINESS GATES
# demo-ingress-pod   1/1     Running   0          117s   10.1.3.51   docker-desktop   <none>           <none>

kubectl apply -f demo-ingress-svc.yaml
# service/demo-ingress-svc created

kubectl get svc
# NAME               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
# demo-ingress-svc   ClusterIP   10.102.160.76   <none>        8080/TCP   13s

kubectl get ep demo-ingress-svc
# NAME               ENDPOINTS      AGE
# demo-ingress-svc   10.1.3.51:80   59s

kubectl apply -f demo-ingress.yaml
# ingress.networking.k8s.io/demo-ingress created

kubectl get ingress
# NAME             CLASS    HOSTS              ADDRESS     PORTS   AGE
# demo-ingress     <none>   demo-host                      80      24s

kubectl describe ingress demo-ingress
# Name:             demo-ingress
# Labels:           <none>
# Namespace:        default
# Address:          localhost
# Ingress Class:    nginx
# Default backend:  <default>
# Rules:
#   Host        Path  Backends
#   ----        ----  --------
#   demo-host
#               /   demo-ingress-svc:http (10.1.3.51:80)
# Annotations:  <none>
# Events:
#   Type    Reason  Age                From                      Message
#   ----    ------  ----               ----                      -------
#   Normal  Sync    10m (x2 over 10m)  nginx-ingress-controller  Scheduled for sync

kubectl get ing demo-ingress -o yaml
# apiVersion: networking.k8s.io/v1
# kind: Ingress
# metadata:
#   creationTimestamp: "2025-12-30T00:05:27Z"
#   generation: 1
#   name: demo-ingress
#   namespace: default
#   resourceVersion: "2783549"
#   uid: 766ec7e5-2cd1-4065-9f80-f4c0c6653d41
# spec:
#   ingressClassName: nginx
#   rules:
#   - host: demo-host
#     http:
#       paths:
#       - backend:
#           service:
#             name: demo-ingress-svc
#             port:
#               name: http
#         path: /
#         pathType: Prefix
# status:
#   loadBalancer:
#     ingress:
#     - hostname: localhost

```

- Confirm

```sh
kubectl port-forward --namespace=ingress-nginx service/ingress-nginx-controller 8080:80
# Forwarding from 127.0.0.1:8080 -> 80
# Forwarding from [::1]:8080 -> 80

curl http://demo-host:8080 --resolve demo-host:8080:127.0.0.1
# <!DOCTYPE html>
# <html>
# <head>
# <title>Welcome to nginx!</title>
# <style>
# html { color-scheme: light dark; }
# body { width: 35em; margin: 0 auto;
# font-family: Tahoma, Verdana, Arial, sans-serif; }
# </style>
# </head>
# <body>
# <h1>Welcome to nginx!</h1>
# <p>If you see this page, the nginx web server is successfully installed and
# working. Further configuration is required.</p>

# <p>For online documentation and support please refer to
# <a href="http://nginx.org/">nginx.org</a>.<br/>
# Commercial support is available at
# <a href="http://nginx.com/">nginx.com</a>.</p>

# <p><em>Thank you for using nginx.</em></p>
# </body>
# </html>
```

---

### Lab: Multiple Paths with services

- Deployment nginx

```yaml
# demo-ingress-path-deploy-nginx.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx
          ports:
            - containerPort: 80
```

```yaml
# demo-ingress-path-deploy-httpd.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: httpd
spec:
  replicas: 3
  selector:
    matchLabels:
      app: httpd
  template:
    metadata:
      labels:
        app: httpd
    spec:
      containers:
        - name: httpd
          image: httpd
          ports:
            - containerPort: 80
```

```sh
kubectl apply -f demo-ingress-path-deploy-nginx.yaml
# deployment.apps/nginx created

kubectl apply -f demo-ingress-path-deploy-httpd.yaml
# deployment.apps/httpd created

kubectl get deploy
# NAME    READY   UP-TO-DATE   AVAILABLE   AGE
# httpd   3/3     3            3           16s
# nginx   3/3     3            3           2m47s

kubectl get pod
# NAME                     READY   STATUS    RESTARTS   AGE
# httpd-75d67b6665-bjfrg   1/1     Running   0          56s
# httpd-75d67b6665-g22p7   1/1     Running   0          56s
# httpd-75d67b6665-zfk7b   1/1     Running   0          56s
# nginx-7ccccd94f7-8kb7x   1/1     Running   0          3m26s
# nginx-7ccccd94f7-c79hb   1/1     Running   0          3m26s
# nginx-7ccccd94f7-w66xb   1/1     Running   0          3m26s
```

```yaml
# demo-ingress-path-svc-nginx.yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx
spec:
  type: ClusterIP
  selector:
    app: nginx
  ports:
    - name: http
      protocol: TCP
      port: 8080
      targetPort: 80
```

```yaml
# demo-ingress-path-svc-httpd.yaml
apiVersion: v1
kind: Service
metadata:
  name: httpd
spec:
  type: ClusterIP
  selector:
    app: httpd
  ports:
    - name: http
      protocol: TCP
      port: 8080
      targetPort: 80
```

```sh
kubectl apply -f demo-ingress-path-svc-nginx.yaml
# service/nginx created

kubectl apply -f demo-ingress-path-svc-httpd.yaml
# service/httpd created

kubectl get ep nginx httpd
# NAME    ENDPOINTS                                AGE
# nginx   10.1.3.52:80,10.1.3.53:80,10.1.3.54:80   2m44s
# httpd   10.1.3.55:80,10.1.3.56:80,10.1.3.57:80   36s
```

---

```yaml
# demo-ingress-path-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-path
spec:
  ingressClassName: nginx
  rules:
    - host: host-path
      http:
        paths:
          - path: /httpd
            pathType: Prefix
            backend:
              service:
                name: httpd # match svc
                port:
                  name: http # match port name in svc
          - path: /
            pathType: Prefix
            backend:
              service:
                name: nginx # match svc
                port:
                  name: http # match port name in svc
```

```sh
kubectl apply -f demo-ingress-path-ingress.yaml
# ingress.networking.k8s.io/ingress-path created

kubectl get ing ingress-path
# NAME           CLASS   HOSTS       ADDRESS     PORTS   AGE
# ingress-path   nginx   host-path   localhost   80      32s

kubectl describe ing ingress-path
# Name:             ingress-path
# Labels:           <none>
# Namespace:        default
# Address:
# Ingress Class:    nginx
# Default backend:  <default>
# Rules:
#   Host        Path  Backends
#   ----        ----  --------
#   host-path
#               /httpd   httpd:http (10.1.3.57:80,10.1.3.55:80,10.1.3.56:80)
#               /        nginx:http (10.1.3.52:80,10.1.3.54:80,10.1.3.53:80)
# Annotations:  <none>
# Events:
#   Type    Reason  Age   From                      Message
#   ----    ------  ----  ----                      -------
#   Normal  Sync    13s   nginx-ingress-controller  Scheduled for sync
```

- confirm

```sh
kubectl port-forward --namespace=ingress-nginx service/ingress-nginx-controller 8080:80
# Forwarding from 127.0.0.1:8080 -> 80
# Forwarding from [::1]:8080 -> 80

curl http://host-path:8080 --resolve host-path:8080:127.0.0.1
# <!DOCTYPE html>
# <html>
# <head>
# <title>Welcome to nginx!</title>
# <style>
# html { color-scheme: light dark; }
# body { width: 35em; margin: 0 auto;
# font-family: Tahoma, Verdana, Arial, sans-serif; }
# </style>
# </head>
# <body>
# <h1>Welcome to nginx!</h1>
# <p>If you see this page, the nginx web server is successfully installed and
# working. Further configuration is required.</p>

# <p>For online documentation and support please refer to
# <a href="http://nginx.org/">nginx.org</a>.<br/>
# Commercial support is available at
# <a href="http://nginx.com/">nginx.com</a>.</p>

# <p><em>Thank you for using nginx.</em></p>
# </body>
# </html>

curl "http://host-path:8080/httpd" --resolve host-path:8080:127.0.0.1
# <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
# <html><head>
# <title>404 Not Found</title>
# </head><body>
# <h1>Not Found</h1>
# <p>The requested URL was not found on this server.</p>
# </body></html>

```

---

## TLS

- two ways to add HTTPS support
  - either allow `HTTPS` to **pass through** the `ingress proxy` and have the backend pod **terminate** the `TLS` connection
  - have the `proxy` **terminate** and **connect** to the backend pod through `HTTP`.

---

### TLS passthrough

- If the `ingress controller` **supports** TLS passthrough, you can usually configure it by adding `annotations` to the `Ingress object`

- Example: Nginx Ingress Controller

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: demo-passthrough
  annotations:
    nginx.ingress.kubernetes.io/ssl-passthrough: "true"
spec:
```

---

### Terminating TLS at the ingress

- Most `ingress controller` implementations **support TLS termination** at the `ingress proxy`.
  - The `proxy` **terminates the TLS connection** between the client and itself and **forwards the HTTP request unencrypted** to the backend pod.

---

### Lab: enable TLS in ingress

- Create cert and private key

```sh
openssl req -x509 -newkey rsa:4096 -keyout tls.key -out tls.crt \-sha256 -days 7300 -nodes \
-subj '/CN=*.mysite.com' \
-addext 'subjectAltName = DNS:*.mysite.com'
```

- Create tls secret

```sh
kubectl create secret tls tls-mysite-com \
  --cert tls.crt \
  --key tls.key
```

- Adding the TLS secret to the Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: demo-ingress-tls
spec:
  tls:
    - secretName: tls-mysite-com # match the name of secret
      hosts:
        - "*.mysite.com" # match the host in cert
  rules:
```

---

## Customizing Ingress using annotations

- depends on the ingress controller implementation.
- Nginx:
  - https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/

---

### Lab: Cookie-based session affinity

- Service support the IP-based session affinity(Layer 4)
- Ingress support the Cookie-based session affinity( Layer 7 http)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: kiada
  annotations:
    nginx.ingress.kubernetes.io/affinity: cookie # enables cookie-based session affinity
    nginx.ingress.kubernetes.io/session-cookie-name: SESSION_COOKIE # sets the cookie name
spec:
# ...
```

- Test

```sh
curl -I http://kiada.example.com --resolve kiada.example.com:80


# include this cookie in request header
# request is always forwarded to the same pod
curl -H "Cookie: SESSION_COOKIE=1638781091" http://kiada.exampl
```

---

## Ingress class

- A cluster can use multiple ingress class
- An ingress object specify the ingress class in the `ingressClassName` field
- default IngressClass
  - `ingressclass.kubernetes.io/is-default-class:true`

```sh
kubectl get ingressclasses
# NAME    CONTROLLER             PARAMETERS   AGE
# nginx   k8s.io/ingress-nginx   <none>       5h7m

kubectl get ingressclasses nginx -o yaml
# apiVersion: networking.k8s.io/v1
# kind: IngressClass
# metadata:
#   annotations:
#     kubectl.kubernetes.io/last-applied-configuration: |
#       {"apiVersion":"networking.k8s.io/v1","kind":"IngressClass","metadata":{"annotations":{},"labels":{"app.kubernetes.io/component":"controller","app.kubernetes.io/instance":"ingress-nginx","app.kubernetes.io/name":"ingress-nginx","app.kubernetes.io/part-of":"ingress-nginx","app.kubernetes.io/version":"1.14.1"},"name":"nginx"},"spec":{"controller":"k8s.io/ingress-nginx"}}
#   creationTimestamp: "2025-12-29T23:00:55Z"
#   generation: 1
#   labels:
#     app.kubernetes.io/component: controller
#     app.kubernetes.io/instance: ingress-nginx
#     app.kubernetes.io/name: ingress-nginx
#     app.kubernetes.io/part-of: ingress-nginx
#     app.kubernetes.io/version: 1.14.1
#   name: nginx
#   resourceVersion: "2777695"
#   uid: 7788ee00-8598-4d8c-8851-3aa28910f190
# spec:
#   controller: k8s.io/ingress-nginx
```

---

## Custom Resources as Backend

- depends on the ingress controllers
- e.g, The Citrix ingress controller provides the HTTPRoute custom object type, which allows you to configure where the ingress should route HTTP requests.

- example

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
spec:
  ingressClassName: citrix
  rules:
    - host: example.com
      http:
        paths:
          - pathType: ImplementationSpecific
            backend: #A
              resource: #A
                apiGroup: citrix.com #B
                kind: HTTPRoute #B
                name: my-example-route
```
