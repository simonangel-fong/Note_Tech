# Kubernetes: Storage - Use `Secret` as Volume

[Back](../../index.md)

- [Kubernetes: Storage - Use `Secret` as Volume](#kubernetes-storage---use-secret-as-volume)
  - [Use `Secret Volume`](#use-secret-volume)
  - [Lab: TLS secret for nginx https](#lab-tls-secret-for-nginx-https)
    - [Optional: Creating a generic (opaque) secret](#optional-creating-a-generic-opaque-secret)
    - [Explore secret within the container](#explore-secret-within-the-container)

---

## Use `Secret Volume`

- default permissions

  - `0600` / `rw-------`

- The files in a `secret volume` are stored in an **in-memory filesystem (tmpfs)**

  - they are less likely to be compromised.

- example

```yaml
# specify keys
spec:
  volumes:
    - name: cert-and-key
      secret:
        secretName: tls-secret
        items:
          - key: tls.crt
            path: tls.crt
          - key: tls.key
            path: tls.key
            mode: 0600 # read only
  containers:
    volumeMounts:
      - name: tls-secret
        mountPath: /etc/certs
        readOnly: true
```

---

## Lab: TLS secret for nginx https

```sh
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout tls.key \
  -out tls.crt \
  -subj "/CN=localhost"

ls -l tls.crt  tls.key
# -rw-r--r-- 1 ubuntuadmin ubuntuadmin 1115 Dec 26 21:24 tls.crt
# -rw------- 1 ubuntuadmin ubuntuadmin 1704 Dec 26 21:24 tls.key

kubectl create secret tls nginx-tls-secret \
  --cert tls.crt \
  --key tls.key
# secret/nginx-tls-secret created

kubectl describe secret nginx-tls-secret
# Name:         nginx-tls-secret
# Namespace:    default
# Labels:       <none>
# Annotations:  <none>

# Type:  kubernetes.io/tls

# Data
# ====
# tls.crt:  1115 bytes
# tls.key:  1704 bytes

tee nginx-config.yaml<<EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
data:
  nginx.conf: |
    server {
        listen 443 ssl;
        server_name localhost;

        ssl_certificate /etc/nginx/ssl/tls.crt;
        ssl_certificate_key /etc/nginx/ssl/tls.key;

        location / {
            root /usr/share/nginx/html;
            index index.html;
        }
    }
EOF

kubectl apply -f nginx-config.yaml
# configmap/nginx-config created

kubectl describe configmap/nginx-config
# Name:         nginx-config
# Namespace:    default
# Labels:       <none>
# Annotations:  <none>

# Data
# ====
# nginx.conf:
# ----
# server {
#     listen 443 ssl;
#     server_name localhost;

#     ssl_certificate /etc/nginx/ssl/tls.crt;
#     ssl_certificate_key /etc/nginx/ssl/tls.key;

#     location / {
#         root /usr/share/nginx/html;
#         index index.html;
#     }
# }



# BinaryData
# ====

# Events:  <none>

tee nginx-https.yaml<<EOF
apiVersion: v1
kind: Pod
metadata:
  name: nginx-https
spec:
  volumes:
  - name: config-volume
    configMap:
      name: nginx-config
  - name: ssl-certs
    secret:
      secretName: nginx-tls-secret

  containers:
  - name: nginx
    image: nginx:latest
    ports:
    - containerPort: 443
    volumeMounts:
    - name: config-volume
      mountPath: /etc/nginx/conf.d/default.conf
      subPath: nginx.conf
    - name: ssl-certs
      mountPath: "/etc/nginx/ssl"
      readOnly: true
EOF

kubectl apply -f nginx-https.yaml
# pod/nginx-https created

kubectl get pod
# NAME          READY   STATUS    RESTARTS   AGE
# nginx-https   1/1     Running   0          12s

kubectl port-forward pod/nginx-https 8443:443
# Forwarding from 127.0.0.1:8443 -> 443
# Forwarding from [::1]:8443 -> 443

# confirm with detail
curl -vk https://localhost:8443
# * Host localhost:8443 was resolved.
# * IPv6: ::1
# * IPv4: 127.0.0.1
# *   Trying [::1]:8443...
# * Connected to localhost (::1) port 8443
# * ALPN: curl offers h2,http/1.1
# * TLSv1.3 (OUT), TLS handshake, Client hello (1):
# * TLSv1.3 (IN), TLS handshake, Server hello (2):
# * TLSv1.3 (IN), TLS handshake, Encrypted Extensions (8):
# * TLSv1.3 (IN), TLS handshake, Certificate (11):
# * TLSv1.3 (IN), TLS handshake, CERT verify (15):
# * TLSv1.3 (IN), TLS handshake, Finished (20):
# * TLSv1.3 (OUT), TLS change cipher, Change cipher spec (1):
# * TLSv1.3 (OUT), TLS handshake, Finished (20):
# * SSL connection using TLSv1.3 / TLS_AES_256_GCM_SHA384 / X25519 / RSASSA-PSS
# * ALPN: server accepted http/1.1
# * Server certificate:
# *  subject: CN=localhost
# *  start date: Dec 27 02:24:49 2025 GMT
# *  expire date: Dec 27 02:24:49 2026 GMT
# *  issuer: CN=localhost
# *  SSL certificate verify result: self-signed certificate (18), continuing anyway.
# *   Certificate level 0: Public key type RSA (2048/112 Bits/secBits), signed using sha256WithRSAEncryption
# * using HTTP/1.x
# > GET / HTTP/1.1
# > Host: localhost:8443
# > User-Agent: curl/8.5.0
# > Accept: */*
# >
# * TLSv1.3 (IN), TLS handshake, Newsession Ticket (4):
# * TLSv1.3 (IN), TLS handshake, Newsession Ticket (4):
# * old SSL session ID is stale, removing
# < HTTP/1.1 200 OK
# < Server: nginx/1.29.4
# < Date: Sat, 27 Dec 2025 02:46:47 GMT
# < Content-Type: text/html
# < Content-Length: 615
# < Last-Modified: Tue, 09 Dec 2025 18:28:10 GMT
# < Connection: keep-alive
# < ETag: "69386a3a-267"
# < Accept-Ranges: bytes
# <
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
# * Connection #0 to host localhost left intact
```

---

### Optional: Creating a generic (opaque) secret

```sh
kubectl create secret generic kiada-tls --from-file tls.crt=tls.crt --from-file tls.key=tls.key
```

---

### Explore secret within the container

```sh
kubectl exec nginx-https -- cat /etc/nginx/ssl/tls.crt
# -----BEGIN CERTIFICATE-----
# MIIDCTCCAfGgAwIBAgIUUvY2Z/sV1TfyjJVUxemQ8wCi6AMwDQYJKoZIhvcNAQEL
# BQAwFDESMBAGA1UEAwwJbG9jYWxob3N0MB4XDTI1MTIyNzAyMjQ0OVoXDTI2MTIy
# NzAyMjQ0OVowFDESMBAGA1UEAwwJbG9jYWxob3N0MIIBIjANBgkqhkiG9w0BAQEF
# AAOCAQ8AMIIBCgKCAQEAjS7ZlByawDIPLe+yFQdU5iCw2y5wmPKuVLvaOgS0Z11
# ...

kubectl exec nginx-https -- cat /etc/nginx/ssl/tls.key
# -----BEGIN PRIVATE KEY-----
# MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCNLtmUHJrAMg8t
# 77IVB1TmILDbLnCY8q5Uu9o6BLRnXUOT4RspPj3LZODuxuQlW1APLMNaJjZZDKAH
# +K0OVTk+RJLBjPL4fn3QZgBBfGa1RGoK2dvqRG62pJ/0g9RGWrZxmx3ntGfW11Zs
# ...
```
