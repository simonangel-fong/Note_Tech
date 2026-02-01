# Kubernetes Networking: `Gateway API` & `GatewayClass`

[Back](../../index.md)

- [Kubernetes Networking: `Gateway API` \& `GatewayClass`](#kubernetes-networking-gateway-api--gatewayclass)
  - [Application - nginx app](#application---nginx-app)
  - [Gateway Class](#gateway-class)
  - [Lab: Simple Gateway](#lab-simple-gateway)
  - [Lab: Fanout - one gateway + multiple httproutes](#lab-fanout---one-gateway--multiple-httproutes)
  - [Lab: HTTP Host Routing - Fanout(1 gateway + multiple route)](#lab-http-host-routing---fanout1-gateway--multiple-route)
  - [HTTP Redirects](#http-redirects)
    - [Lab: HTTP-to-HTTPS redirects](#lab-http-to-https-redirects)
  - [HTTP Rewrites](#http-rewrites)
    - [Lab: Rewrites Host](#lab-rewrites-host)
  - [HTTP traffic splitting](#http-traffic-splitting)
    - [Lab: Traffic Splitting](#lab-traffic-splitting)
  - [HTTP query parameter matching](#http-query-parameter-matching)
    - [single query parameter](#single-query-parameter)
    - [multiple query parameters](#multiple-query-parameters)
    - [AND \& OR matching](#and--or-matching)
    - [Combining with other match types](#combining-with-other-match-types)
    - [Lab: Gateway - Query Parameter](#lab-gateway---query-parameter)
  - [TLS Configuration](#tls-configuration)
    - [Lab: Downstream TLS](#lab-downstream-tls)
  - [HTTP method matching](#http-method-matching)
    - [Lab: Method Matching](#lab-method-matching)

---

## Application - nginx app

```sh
mkdir -pv ~/web-app/html

tee ~/web-app/html/index_a.html<<EOF
{"index":"a"}
EOF

tee ~/web-app/html/index_b.html<<EOF
{"index":"b"}
EOF

tee ~/web-app/html/index_c.html<<EOF
{"index":"c"}
EOF

tee ~/web-app/html/index_d.html<<EOF
{"index":"d"}
EOF

kubectl create cm web-cm-page --from-file=index_a=/home/ubuntuadmin/web-app/html/index_a.html --from-file=index_b=/home/ubuntuadmin/web-app/html/index_b.html --from-file=index_c=/home/ubuntuadmin/web-app/html/index_c.html --from-file=index_d=/home/ubuntuadmin/web-app/html/index_d.html
# configmap/web-cm-page created

cat > ~/web-app/deploy.yaml<<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deploy-a
  labels:
    deploy: deploy-a
    app: web
spec:
  replicas: 2
  selector:
    matchLabels:
      deploy: deploy-a
      app: web
  template:
    metadata:
      labels:
        deploy: deploy-a
        app: web
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
  name: deploy-b
  labels:
    deploy: deploy-b
    app: web
spec:
  replicas: 2
  selector:
    matchLabels:
      deploy: deploy-b
      app: web
  template:
    metadata:
      labels:
        deploy: deploy-b
        app: web
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
  name: deploy-c
  labels:
    deploy: deploy-c
    app: web
spec:
  replicas: 2
  selector:
    matchLabels:
      deploy: deploy-c
      app: web
  template:
    metadata:
      labels:
        deploy: deploy-c
        app: web
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
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deploy-d
  labels:
    deploy: deploy-d
    app: web
spec:
  replicas: 2
  selector:
    matchLabels:
      deploy: deploy-d
      app: web
  template:
    metadata:
      labels:
        deploy: deploy-d
        app: web
    spec:
      volumes:
      - name: cm-vol
        configMap:
          name: web-cm-page
          items:
          - key: index_d
            path: index.html
      containers:
      - image: nginx
        name: nginx
        volumeMounts:
        - name: cm-vol
          mountPath: /usr/share/nginx/html
EOF

kubectl apply -f ~/web-app/deploy.yaml
# deployment.apps/deploy-a created
# deployment.apps/deploy-b created
# deployment.apps/deploy-c created
# deployment.apps/deploy-d created

kubectl get deploy -l app=web
# NAME       READY   UP-TO-DATE   AVAILABLE   AGE
# deploy-a   0/2     2            0           16s
# deploy-b   0/2     2            0           16s
# deploy-c   0/2     2            0           16s
# deploy-d   0/2     2            0           16s

cat > ~/web-app/svc.yaml<<EOF
apiVersion: v1
kind: Service
metadata:
  name: svc-a
  labels:
    svc: svc-a
    app: web
spec:
  selector:
    deploy: deploy-a
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: svc-b
  labels:
    svc: svc-b
    app: web
spec:
  selector:
    deploy: deploy-b
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: svc-c
  labels:
    svc: svc-c
    app: web
spec:
  selector:
    deploy: deploy-c
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: svc-d
  labels:
    svc: svc-d
    app: web
spec:
  selector:
    deploy: deploy-d
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
EOF

kubectl apply -f ~/web-app/svc.yaml
# service/svc-a created
# service/svc-b created
# service/svc-c created
# service/svc-d created

kubectl get svc -l app=web
# NAME    TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
# svc-a   ClusterIP   10.98.18.216     <none>        80/TCP    26m
# svc-b   ClusterIP   10.101.105.194   <none>        80/TCP    26m
# svc-c   ClusterIP   10.109.137.19    <none>        80/TCP    26m
# svc-d   ClusterIP   10.107.72.93     <none>        80/TCP    10s

```

- Test

```sh
kubectl run curltest --rm -it --image=curlimages/curl --restart=Never -- sh -c "curl svc-a; curl svc-b; curl svc-c; curl svc-d"
# {"index":"a"}
# {"index":"b"}
# {"index":"c"}
# {"index":"d"}
# pod "curltest" deleted
```

---

## Gateway Class

```sh
kubectl get gatewayclass
# NAME    CONTROLLER                                   ACCEPTED   AGE
# nginx   gateway.nginx.org/nginx-gateway-controller   True       20h

kubectl get svc -n nginx-gateway
# NAME                    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
# service/nginx-gateway   ClusterIP   10.111.194.40   <none>        443/TCP   20h
```

---

## Lab: Simple Gateway

```sh
cat > ~/web-app/gtw-simple.yaml <<EOF
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: gtw-simple
  labels:
    gtw: simple
    app: web
spec:
  gatewayClassName: nginx
  listeners:
  - name: http-lsnr
    protocol: HTTP
    port: 80
    allowedRoutes:
      namespaces:
        from: Same
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: gtw-simple-route
  labels:
    gtw: simple
    app: web
spec:
  parentRefs:
  - name: gtw-simple
  rules:
  - backendRefs:
    - name: svc-a
      port: 80
EOF

kubectl apply -f ~/web-app/gtw-simple.yaml
# gateway.gateway.networking.k8s.io/gtw-simple created
# httproute.gateway.networking.k8s.io/gtw-simple-route created

kubectl get gtw,httproute -l gtw
# NAME                                           CLASS   ADDRESS          PROGRAMMED   AGE
# gateway.gateway.networking.k8s.io/gtw-simple   nginx   192.168.10.211   True         4s

# NAME                                                   HOSTNAMES   AGE
# httproute.gateway.networking.k8s.io/gtw-simple-route               4s

```

- Testing

```sh
kubectl run curltest --rm -it --image=curlimages/curl --restart=Never -- sh -c 'curl -sS http://192.168.10.211/'
# {"index":"a"}
# pod "curltest" deleted

curl -sS http://192.168.10.211/
# {"index":"a"}
```

---

## Lab: Fanout - one gateway + multiple httproutes

1. url: `a.mysite.com` -> service `svc-a`
2. url: `b.mysite.com` -> service `svc-b`
3. url: `b.mysite.com/foo` -> service `svc-c`
4. url: `b.mysite.com/bar`, header `index:demo` -> service `svc-d`

```sh

cat > ~/web-app/gtw-fanout.yaml <<EOF
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: gtw-fanout
  labels:
    gtw: fanout
    app: web
spec:
  gatewayClassName: nginx
  listeners:
  - name: http
    protocol: HTTP
    port: 80
    allowedRoutes:
      namespaces:
        from: Same
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: route-a
  labels:
    host: a
    gtw: fanout
    app: web
spec:
  parentRefs:
  - name: gtw-fanout
    sectionName: http
  hostnames:
  - a.mysite.com
  rules:
  - backendRefs:
    - name: svc-a
      port: 80
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: route-b-default
  labels:
    host: b-default
    gtw: fanout
    app: web
spec:
  parentRefs:
  - name: gtw-fanout
    sectionName: http
  hostnames:
  - b.mysite.com
  rules:
  - backendRefs:
    - name: svc-b
      port: 80
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: route-b-foo
  labels:
    host: b-foo
    gtw: fanout
    app: web
spec:
  parentRefs:
  - name: gtw-fanout
    sectionName: http
  hostnames:
  - b.mysite.com
  rules:
  # /beta -> svc-c
  - matches:
    - path:
        type: PathPrefix
        value: /foo
    backendRefs:
    - name: svc-c
      port: 80
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: route-b-bar
  labels:
    host: b-bar
    gtw: fanout
    app: web
spec:
  parentRefs:
  - name: gtw-fanout
    sectionName: http
  hostnames:
  - b.mysite.com
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /bar
      headers:
      - name: index
        type: Exact
        value: demo
    backendRefs:
    - name: svc-d
      port: 80

EOF

kubectl apply -f ~/web-app/gtw-fanout.yaml
# gateway.gateway.networking.k8s.io/gtw-fanout created
# httproute.gateway.networking.k8s.io/route-a created
# httproute.gateway.networking.k8s.io/route-b-default created
# httproute.gateway.networking.k8s.io/route-b-foo created
# httproute.gateway.networking.k8s.io/route-b-bar created

kubectl get gtw,httproute -l gtw=fanout
# NAME                                           CLASS   ADDRESS          PROGRAMMED   AGE
# gateway.gateway.networking.k8s.io/gtw-fanout   nginx   192.168.10.212   True         14m

# NAME                                                  HOSTNAMES          AGE
# httproute.gateway.networking.k8s.io/route-a           ["a.mysite.com"]   14m
# httproute.gateway.networking.k8s.io/route-b-bar       ["b.mysite.com"]   14m
# httproute.gateway.networking.k8s.io/route-b-default   ["b.mysite.com"]   14m
# httproute.gateway.networking.k8s.io/route-b-foo       ["b.mysite.com"]   14m

```

- Testing

```sh
kubectl run curltest --rm -it --image=curlimages/curl --restart=Never -- sh
curl -sS -H "Host: a.mysite.com" http://192.168.10.212/
# {"index":"a"}

curl -sS -H "Host: b.mysite.com" http://192.168.10.212/
# {"index":"b"}

curl -sS -H "Host: b.mysite.com" http://192.168.10.212/foo
# <html>
# <head><title>404 Not Found</title></head>
# <body>
# <center><h1>404 Not Found</h1></center>
# <hr><center>nginx/1.29.4</center>
# </body>
# </html>

curl -sS -H "Host: b.mysite.com" -H "index: demo" http://192.168.10.212/bar
# <html>
# <head><title>404 Not Found</title></head>
# <body>
# <center><h1>404 Not Found</h1></center>
# <hr><center>nginx/1.29.4</center>
# </body>
# </html>

curl -sS http://192.168.10.212/
# {"index":"a"}
```

---

## Lab: HTTP Host Routing - Fanout(1 gateway + multiple route)

- url `host-a.mysite.com` -> `svc-a`
- url `host-b.mysite.com` -> `svc-b`
- url `host-c.mysite.com` -> `svc-c`

```sh
cat > ~/web-app/gtw-host.yaml <<EOF
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: gtw-host
  labels:
    gtw: host
    app: web
spec:
  gatewayClassName: nginx
  listeners:
  - name: http
    protocol: HTTP
    port: 80
    allowedRoutes:
      namespaces:
        from: Same
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: gtw-host-route-a
  labels:
    gtw: host
    app: web
spec:
  parentRefs:
  - name: gtw-host
    sectionName: http
  hostnames:
  - "host-a.mysite.com"
  rules:
  - backendRefs:
    - name: svc-a
      port: 80
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: gtw-host-route-b
  labels:
    gtw: host
    app: web
spec:
  parentRefs:
  - name: gtw-host
    sectionName: http
  hostnames:
  - "host-b.mysite.com"
  rules:
  - backendRefs:
    - name: svc-b
      port: 80
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: gtw-host-route-c
  labels:
    gtw: host
    app: web
spec:
  parentRefs:
  - name: gtw-host
    sectionName: http
  hostnames:
  - "host-c.mysite.com"
  rules:
  - backendRefs:
    - name: svc-c
      port: 80
EOF

kubectl apply -f ~/web-app/gtw-host.yaml
# gateway.gateway.networking.k8s.io/gtw-host created
# httproute.gateway.networking.k8s.io/gtw-host-route-a created
# httproute.gateway.networking.k8s.io/gtw-host-route-b created
# httproute.gateway.networking.k8s.io/gtw-host-route-c created

kubectl get gtw,httproute -l gtw=host
# NAME                                         CLASS   ADDRESS          PROGRAMMED   AGE
# gateway.gateway.networking.k8s.io/gtw-host   nginx   192.168.10.211   True         51s

# NAME                                                   HOSTNAMES               AGE
# httproute.gateway.networking.k8s.io/gtw-host-route-a   ["host-a.mysite.com"]   51s
# httproute.gateway.networking.k8s.io/gtw-host-route-b   ["host-b.mysite.com"]   51s
# httproute.gateway.networking.k8s.io/gtw-host-route-c   ["host-c.mysite.com"]   51s

curl -sS -H "Host: host-a.mysite.com" http://192.168.10.211/
# {"index":"a"}

curl -sS -H "Host: host-b.mysite.com" http://192.168.10.211/
# {"index":"b"}

curl -sS -H "Host: host-c.mysite.com" http://192.168.10.211/
# {"index":"c"}
```

---

## HTTP Redirects

- `Redirects`
  - return `HTTP 3XX` responses to a client, instructing it to **retrieve a different resource**.

- `rules.filters.RequestRedirect`:
  - used to redirects

  - `requestRedirect.statusCode=301`
    - issue a permanent redirect (301) from HTTP to HTTPS

---

### Lab: HTTP-to-HTTPS redirects

```sh
mkdir ~/web-app/tls

# create key and crt
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ~/web-app/tls/mysite-tls.key \
  -out ~/web-app/tls/mysite-tls.crt \
  -subj "/CN=*.mysite.com" \
  -addext "subjectAltName=DNS:*.mysite.com"

cd ~/web-app/tls

# confirm secret
kubectl create secret tls mysite-tls \
  --key=mysite-tls.key   \
  --cert=mysite-tls.crt
# secret/mysite-tls created

cat > ~/web-app/gtw-redirect-http.yaml<<EOF
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: gtw-redirect-http
  labels:
    gtw: redirect-http
    app: web
spec:
  gatewayClassName: nginx
  listeners:
  - name: https
    protocol: HTTPS
    port: 443
    hostname: redirect.mysite.com
    tls:
      mode: Terminate
      certificateRefs:
      - kind: Secret
        name: mysite-tls
  - name: http
    protocol: HTTP
    port: 80
    hostname: redirect.mysite.com
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: route-http-redirect
  labels:
    gtw: redirect-http
    app: web
spec:
  parentRefs:
  - name: gtw-redirect-http
    sectionName: http
  hostnames:
  - redirect.mysite.com
  rules:
  - filters:
    - type: RequestRedirect
      requestRedirect:
        scheme: https
        statusCode: 301
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: route-https
  labels:
    gtw: redirect-http
    app: web
spec:
  parentRefs:
  - name: gtw-redirect-http
    sectionName: https
  hostnames:
  - redirect.mysite.com
  rules:
  - backendRefs:
    - name: svc-d
      port: 80
EOF

kubectl apply -f ~/web-app/gtw-redirect-http.yaml
# gateway.gateway.networking.k8s.io/gtw-redirect-http created
# httproute.gateway.networking.k8s.io/route-http-redirect created
# httproute.gateway.networking.k8s.io/route-https created

kubectl get gtw,httproute -l gtw=redirect-http
# NAME                                                  CLASS   ADDRESS          PROGRAMMED   AGE
# gateway.gateway.networking.k8s.io/gtw-redirect-http   nginx   192.168.10.212   True         114s

# NAME                                                      HOSTNAMES                 AGE
# httproute.gateway.networking.k8s.io/route-http-redirect   ["redirect.mysite.com"]   114s
# httproute.gateway.networking.k8s.io/route-https           ["redirect.mysite.com"]   114s

curl -v -H "Host: redirect.mysite.com" http://192.168.10.212/
# *   Trying 192.168.10.212:80...
# * Connected to 192.168.10.212 (192.168.10.212) port 80
# > GET / HTTP/1.1
# > Host: redirect.mysite.com
# > User-Agent: curl/8.5.0
# > Accept: */*
# >
# < HTTP/1.1 301 Moved Permanently
# < Server: nginx
# < Date: Sat, 24 Jan 2026 01:08:06 GMT
# < Content-Type: text/html
# < Content-Length: 162
# < Connection: keep-alive
# < Location: https://redirect.mysite.com/
# <
# <html>
# <head><title>301 Moved Permanently</title></head>
# <body>
# <center><h1>301 Moved Permanently</h1></center>
# <hr><center>nginx</center>
# </body>
# </html>
# * Connection #0 to host 192.168.10.212 left intact

curl -k --resolve redirect.mysite.com:443:192.168.10.212 https://redirect.mysite.com/
# {"index":"d"}
```

---

## HTTP Rewrites

- `Rewrites`
  - modify components of a client request before proxying it upstream.

- `rules.filters.URLRewrite`:
  - used to rewrite the path

---

### Lab: Rewrites Host

```sh
cat > ~/web-app/gtw-rewrite-host.yaml<<EOF
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: gtw-rewrite-host
  labels:
    gtw: rewrite-host
    app: web
spec:
  gatewayClassName: nginx
  listeners:
  - name: http
    protocol: HTTP
    port: 80
    hostname: rewrite-a.mysite.com
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: route-rewrite-host
  labels:
    gtw: rewrite-host
    app: web
spec:
  parentRefs:
  - name: gtw-rewrite-host
  hostnames:
    - rewrite-a.mysite.com
  rules:
    - filters:
        - type: URLRewrite
          urlRewrite:
            hostname: rewrite-b.mysite.com
      backendRefs:
        - name: svc-c
          weight: 1
          port: 80
EOF

kubectl apply -f ~/web-app/gtw-rewrite-host.yaml
# gateway.gateway.networking.k8s.io/gtw-rewrite-host created
# httproute.gateway.networking.k8s.io/route-rewrite-host created

kubectl get gtw,httproute -l gtw=rewrite-host
# NAME                                                 CLASS   ADDRESS          PROGRAMMED   AGE
# gateway.gateway.networking.k8s.io/gtw-rewrite-host   nginx   192.168.10.214   True         14s

# NAME                                                     HOSTNAMES                  AGE
# httproute.gateway.networking.k8s.io/gtw-rewrite-host     ["rewrite-a.mysite.com"]   3m51s
# httproute.gateway.networking.k8s.io/route-rewrite-host   ["rewrite-a.mysite.com"]   14s

# test
url -sS -H "Host: rewrite-a.mysite.com" http://192.168.10.214/
# {"index":"c"}

```

---

## HTTP traffic splitting

- used to specify **weights** to shift traffic between different `backends`.
  - useful for splitting traffic during **rollouts**, **canarying changes**, or for emergencies.

- `backendRefs.weight`:
  - default: 1

- example:

```yaml
kind: HTTPRoute
spec:
  rules:
    - backendRefs:
        - name: foo-v1
          port: 8080
          weight: 90
        - name: foo-v2
          port: 8080
          weight: 10
```

---

- Canary traffic rollout

- T0: new version testing
  - only traffic with `traffic=test` route to new version

```yaml
kind: HTTPRoute
spec:
  rules:
    - backendRefs:
        - name: foo-v1
    - matches:
        - headers:
            - name: traffic
              value: test
      backendRefs:
        - name: foo-v2
```

- T1: Blue-green test
  - internal testing pass
  - new version start to accept traffic

```yaml
kind: HTTPRoute
spec:
  rules:
    - backendRefs:
        - name: foo-v1
          weight: 90
        - name: foo-v2 # new version
          weight: 10
```

- T2: Completing
  - complete the rollout
  - old version stop

```yaml
spec:
  rules:
    - backendRefs:
        - name: foo-v1
          weight: 0 # old version = 0
        - name: foo-v2
          weight: 1 # new version == 100%
```

---

### Lab: Traffic Splitting

```sh
cat > ~/web-app/gtw-split.yaml <<EOF
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: gtw-split
  labels:
    gtw: split
    app: web
spec:
  gatewayClassName: nginx
  listeners:
  - name: http
    protocol: HTTP
    port: 80
    hostname: split.mysite.com
    allowedRoutes:
      namespaces:
        from: Same
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: route-split
  labels:
    gtw: split
    app: web
spec:
  parentRefs:
  - name: gtw-split
    sectionName: http
  hostnames:
  - split.mysite.com
  rules:
  - backendRefs:
    - name: svc-a
      port: 80
      weight: 25
    - name: svc-b
      port: 80
      weight: 25
    - name: svc-c
      port: 80
      weight: 25
    - name: svc-d
      port: 80
      weight: 25
EOF

kubectl apply -f ~/web-app/gtw-split.yaml
# gateway.gateway.networking.k8s.io/gtw-split created
# httproute.gateway.networking.k8s.io/simple-split created

# confirm
kubectl get gtw,httproute -l gtw=split
# NAME                                          CLASS   ADDRESS          PROGRAMMED   AGE
# gateway.gateway.networking.k8s.io/gtw-split   nginx   192.168.10.212   True         30s

curl -H "Host: split.mysite.com" http://192.168.10.212/
# {"index":"d"}
curl -H "Host: split.mysite.com" http://192.168.10.212/
# {"index":"b"}
curl -H "Host: split.mysite.com" http://192.168.10.212/
# {"index":"a"}
curl -H "Host: split.mysite.com" http://192.168.10.212/
# {"index":"c"}
```

---

## HTTP query parameter matching

- used to match requests based on query parameters.
- splits traffic based on the value of the query parameter

### single query parameter

- Example:

```yaml
spec:
  rules:
    - matches:
        # /?animal=whale
        - queryParams:
            - name: animal
              value: whale
      backendRefs:
        - name: infra-backend-v1
    - matches:
        # /?animal=dolphin
        - queryParams:
            - name: animal
              value: dolphin
      backendRefs:
        - name: infra-backend-v2
```

---

### multiple query parameters

```yaml
spec:
  rules:
    - matches:
        # /?animal=dolphin&color=blue
        - queryParams:
            - name: animal
              value: dolphin
            - name: color
              value: blue
      backendRefs:
        - name: infra-backend-v3
          port: 8080
```

---

### AND & OR matching

- `rules.matches`: []

```yaml
spec:
  rules:
    - matches:
        # /?animal=dolphin&color=blue
        - queryParams:
            - name: animal
              value: dolphin
            - name: color
              value: blue
        # /?ANIMAL=Whale
        - queryParams:
            - name: ANIMAL
              value: Whale
      backendRefs:
        - name: infra-backend-v3
          port: 8080
```

---

### Combining with other match types

- `rules`: []

```yaml
spec:
  rules:
    # /path1?animal=whale
    - matches:
        - path:
            type: PathPrefix
            value: /path1
          queryParams:
            - name: animal
              value: whale
      backendRefs:
        - name: infra-backend-v1
          port: 8080
    # /?animal=whale {version=one}
    - matches:
        - headers:
            - name: version
              value: one
          queryParams:
            - name: animal
              value: whale
      backendRefs:
        - name: infra-backend-v2
          port: 8080
    # /path2?animal=whale {version=two}
    - matches:
        - path:
            type: PathPrefix
            value: /path2
          headers:
            - name: version
              value: two
          queryParams:
            - name: animal
              value: whale
      backendRefs:
        - name: infra-backend-v3
          port: 8080
```

---

### Lab: Gateway - Query Parameter

- url `para.mysite.com?index=b` -> backend: `svc-b`
- url `para.mysite.com?index=c` -> backend: `svc-c`
- else -> backend: `svc-c`

```sh
cat > ~/web-app/gtw-para.yaml <<EOF
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: gtw-para
  labels:
    gtw: para
    app: web
spec:
  gatewayClassName: nginx
  listeners:
  - name: http
    protocol: HTTP
    port: 80
    hostname: para.mysite.com
    allowedRoutes:
      namespaces:
        from: Same
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: gtw-para-route
  labels:
    gtw: para
    app: web
spec:
  parentRefs:
  - name: gtw-para
  hostnames:
  - para.mysite.com
  rules:
  - matches:
    - queryParams:
      - name: index
        value: b
    backendRefs:
    - name: svc-b
      port: 80
  - matches:
    - queryParams:
      - name: index
        value: c
    backendRefs:
    - name: svc-c
      port: 80
  - backendRefs:
    - name: svc-d
      port: 80
EOF

kubectl apply -f ~/web-app/gtw-para.yaml
# gateway.gateway.networking.k8s.io/gtw-para created
# httproute.gateway.networking.k8s.io/gtw-para-route created

# confirm
kubectl get gtw,httproute -l gtw=para
# NAME                                         CLASS   ADDRESS          PROGRAMMED   AGE
# gateway.gateway.networking.k8s.io/gtw-para   nginx   192.168.10.211   True         37s

# NAME                                                 HOSTNAMES   AGE
# httproute.gateway.networking.k8s.io/gtw-para-route               37s

curl -sS -H "Host: para.mysite.com" http://192.168.10.211/?index=b
# {"index":"b"}
curl -sS -H "Host: para.mysite.com" http://192.168.10.211/?index=c
# {"index":"c"}

curl -sS -H "Host: para.mysite.com" http://192.168.10.211/?index=err
# {"index":"d"}
curl -sS -H "Host: para.mysite.com" http://192.168.10.211/?err=true
# {"index":"d"}
curl -sS -H "Host: para.mysite.com" http://192.168.10.211/err
# <html>
# <head><title>404 Not Found</title></head>
# <body>
# <center><h1>404 Not Found</h1></center>
# <hr><center>nginx/1.29.4</center>
# </body>
# </html>
```

---

## TLS Configuration

- two connections:
  - `downstream`: the connection between the `client` and the `Gateway`.
  - `upstream`: the connection between the `Gateway` and `backend resources` specified by routes.

- downstream connections

| Listener Protocol | TLS Mode    | Route Type Supported |
| ----------------- | ----------- | -------------------- |
| TLS               | Passthrough | TLSRoute             |
| TLS               | Terminate   | TLSRoute (extended)  |
| HTTPS             | Terminate   | HTTPRoute            |
| GRPC              | Terminate   | GRPCRoute            |

- upstream connections
  - managed by `BackendTLSPolicy`

---

### Lab: Downstream TLS

```sh
mkdir ~/web-app/tls


# create key and crt
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ~/web-app/tls/tls.key \
  -out ~/web-app/tls/tls.crt \
  -subj "/CN=tls.mysite.com" \
  -addext "subjectAltName=DNS:tls.mysite.com"

cd ~/web-app/tls

# confirm secret
kubectl create secret tls tls-secret \
  --key=tls.key   \
  --cert=tls.crt
# secret/tls-secret created

cat > ~/web-app/gtw-tls.yaml <<EOF
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: gtw-tls
  labels:
    gtw: tls
    app: web
spec:
  gatewayClassName: nginx
  listeners:
  - name: https
    protocol: HTTPS
    port: 443
    hostname: tls.mysite.com
    tls:
      mode: Terminate
      certificateRefs:
      - kind: Secret
        name: tls-secret
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: route-tls
  labels:
    gtw: tls
    app: web
spec:
  hostnames:
  - tls.mysite.com
  parentRefs:
  - name: gtw-tls
    sectionName: https
  rules:
  - backendRefs:
    - name: svc-a
      port: 80
EOF

kubectl apply -f ~/web-app/gtw-tls.yaml
# gateway.gateway.networking.k8s.io/gtw-tls created
# httproute.gateway.networking.k8s.io/route-tls created

kubectl get gtw,httproute -l gtw=tls
# NAME                                        CLASS   ADDRESS          PROGRAMMED   AGE
# gateway.gateway.networking.k8s.io/gtw-tls   nginx   192.168.10.213   True         3m1s

# NAME                                            HOSTNAMES            AGE
# httproute.gateway.networking.k8s.io/route-tls   ["tls.mysite.com"]   3m1s

```

- Testing

```sh
kubectl get node -o wide
# NAME           STATUS   ROLES           AGE     VERSION    INTERNAL-IP      EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION      CONTAINER-RUNTIME
# controlplane   Ready    control-plane   6d17h   v1.32.11   192.168.10.150   <none>        Ubuntu 24.04.3 LTS   6.14.0-37-generic   containerd://1.7.28
# node01         Ready    <none>          6d17h   v1.32.11   192.168.10.151   <none>        Ubuntu 24.04.3 LTS   6.14.0-37-generic   containerd://1.7.28
# node02         Ready    <none>          6d17h   v1.32.11   192.168.10.152   <none>        Ubuntu 24.04.3 LTS   6.14.0-37-generic   containerd://1.7.28


curl -k --resolve tls.mysite.com:443:192.168.10.213 https://tls.mysite.com/
# {"index":"a"}
```

---

## HTTP method matching

- used to match requests based on the HTTP method.

### Lab: Method Matching

```sh
cat > ~/web-app/gtw-method.yaml <<EOF
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: gtw-method
  labels:
    gtw: method
    app: web
spec:
  gatewayClassName: nginx
  listeners:
  - name: http
    protocol: HTTP
    port: 80
    hostname: method.mysite.com
    allowedRoutes:
      namespaces:
        from: Same
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: route-method
  labels:
    gtw: method
    app: web
spec:
  hostnames:
  - method.mysite.com
  parentRefs:
  - name: gtw-method
    sectionName: http
  rules:
  - matches:
    - method: POST
    backendRefs:
    - name: svc-b
      port: 80
  - matches:
    - method: GET
    backendRefs:
    - name: svc-c
      port: 80
EOF

kubectl apply -f ~/web-app/gtw-method.yaml
# gateway.gateway.networking.k8s.io/gtw-method created
# httproute.gateway.networking.k8s.io/route-method created

kubectl get gtw,httproute -l gtw=method
# NAME                                           CLASS   ADDRESS          PROGRAMMED   AGE
# gateway.gateway.networking.k8s.io/gtw-method   nginx   192.168.10.213   True         31s

# NAME                                               HOSTNAMES               AGE
# httproute.gateway.networking.k8s.io/route-method   ["method.mysite.com"]   31s

curl -sS -H "Host: method.mysite.com" http://192.168.10.213/
# {"index":"c"}

# expected code: 405
curl -sS -X POST -H "Host: method.mysite.com" http://192.168.10.213/ -d 'hello=world'
# <html>
# <head><title>405 Not Allowed</title></head>
# <body>
# <center><h1>405 Not Allowed</h1></center>
# <hr><center>nginx/1.29.4</center>
# </body>
# </html>
```
