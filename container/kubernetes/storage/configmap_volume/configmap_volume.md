# Kubernetes: Storage - Use `ConfigMap` as Volume

[Back](../../index.md)

- [Kubernetes: Storage - Use `ConfigMap` as Volume](#kubernetes-storage---use-configmap-as-volume)
  - [Use `ConfigMap Volume`](#use-configmap-volume)
  - [Lab: using `configMap` volume](#lab-using-configmap-volume)
    - [Create html files](#create-html-files)
    - [Error: Create pod without optional](#error-create-pod-without-optional)
    - [Create pod with optional](#create-pod-with-optional)
    - [Creating `configMap` Volume](#creating-configmap-volume)
    - [Load All keys](#load-all-keys)
    - [Specify a key](#specify-a-key)

---

## Use `ConfigMap Volume`

- file permission
  - default:
    - `rw-r--r--` (`0644`)
    - rw-r--r-- (0644)
- files in the `configMap` volume are `symbolic links` with permission `0777`

- edit `configMap` volume

  - the **files** in the `configMap` volume are **automatically updated**.
  - It can take up to **a minute** for the files to be **updated**

- edit `configMap` env

  - **can’t** be updated while the container is **running**.
  - if container restarts, **new** `config map` values will apply to new container

- `immutable` field
  - specify whether the CM is mutable.

---

- Example: Using subPath to mount a single file from the volume

```yaml
spec:
  volumes:
    - name: nginx-config
      configMap:
        name: nginx-config
        optional: true # optional
  containers:
    - name: nginx
      image: nginx
      volumeMounts:
        - name: nginx-config
          mountPath: /usr/share/nginx/html
```

---

- `ConfigMap volumes` use `symbolic links` to provide **atomic updates**
  - Kubernetes ensures that **all files** in a `configMap volume` are **updated atomically**, meaning that all updates are done **instantaneously**.
  - by the use of symbolic file links
- the **file paths** that the application reads point to **actual files** via **two successive** `symbolic links`.

---

## Lab: using `configMap` volume

### Create html files

```sh
mkdir demo-configmap-volume
cd demo-configmap-volume

# Create index.html
tee index.html<<EOF
<html>
<title>Home</title>
<body>
  <h1> Home </h1>
  <p> This is home page </p>
</body>
</html>
EOF

# Create error.html
tee error.html<<EOF
<html>
<title>Error</title>
<body>
  <h1> Error </h1>
  <p> This is Error page </p>
</body>
</html>
EOF
```

---

### Error: Create pod without optional

```sh
# create pod definition
tee demo-configmap-volume-pod.yaml<<EOF
apiVersion: v1
kind: Pod
metadata:
  name: demo-configmap-volume-pod
spec:
  volumes:
  - name: nginx-config
    configMap:
      name: nginx-config

  containers:
  - name: nginx
    image: nginx
    volumeMounts:
    - name: nginx-config
      mountPath: /usr/share/nginx/html
EOF
```

- Create pod before configMap creation

```sh
kubectl apply -f demo-configmap-volume-pod.yaml
# pod/demo-configmap-volume-pod created

kubectl get pod
# NAME                        READY   STATUS              RESTARTS   AGE
# demo-configmap-volume-pod   0/1     ContainerCreating   0          4s

kubectl describe pod demo-configmap-volume-pod
# Events:
#   Type     Reason       Age                From               Message
#   ----     ------       ----               ----               -------
#   Normal   Scheduled    25s                default-scheduler  Successfully assigned default/demo-configmap-volume-pod to docker-desktop
#   Warning  FailedMount  10s (x6 over 25s)  kubelet            MountVolume.SetUp failed for volume "nginx-config" : configmap "nginx-config" not found
```

> Volume is created before pod creation
> pod creation failed because volume creation caused by configmap not found.

---

### Create pod with optional

```sh
# pod definition with optional
tee demo-configmap-volume-pod-optional.yaml<<EOF
apiVersion: v1
kind: Pod
metadata:
  name: demo-configmap-volume-pod-optional
spec:
  volumes:
  - name: nginx-config
    configMap:
      name: nginx-config
      optional: true    # optional
  containers:
  - name: nginx
    image: nginx
    volumeMounts:
    - name: nginx-config
      mountPath: /usr/share/nginx/html
EOF

kubectl apply -f demo-configmap-volume-pod-optional.yaml
# pod/demo-configmap-volume-pod-optional created

kubectl get pod
# NAME                                 READY   STATUS    RESTARTS   AGE
# demo-configmap-volume-pod-optional   1/1     Running   0          8s

# test
kubectl port-forward demo-configmap-volume-pod-optional 8000:80
# Forwarding from 127.0.0.1:8000 -> 80
# Forwarding from [::1]:8000 -> 80

# error: because no home page
curl 127.0.0.1:8000
# <html>
# <head><title>403 Forbidden</title></head>
# <body>
# <center><h1>403 Forbidden</h1></center>
# <hr><center>nginx/1.29.4</center>
# </body>
# </html>
```

> pod created but has no html files

---

### Creating `configMap` Volume

```sh
kubectl create cm nginx-config --from-file=index.html --from-file=error.html
# configmap/nginx-config created

kubectl get cm
# NAME               DATA   AGE
# nginx-config       2      9s

kubectl describe cm nginx-config
# Name:         nginx-config
# Namespace:    default
# Labels:       <none>
# Annotations:  <none>

# Data
# ====
# error.html:
# ----
# <html>\r
# <title>Error</title>\r
# <body>\r
#   <h1> Error </h1>\r
#   <p> This is Error page </p>\r
# </body>\r
# </html>

# index.html:
# ----
# <html>\r
# <title>Home</title>\r
# <body>\r
# <h1> Home </h1>\r
# <p> This is home page </p>\r
# </body>\r
# </html>


# BinaryData
# ====

# Events:  <none>
```

---

### Load All keys

- recreate pod

```sh
kubectl replace --force -f demo-configmap-volume-pod-optional.yaml
# pod "demo-configmap-volume-pod-optional" deleted from default namespace
# pod/demo-configmap-volume-pod-optional replaced

kubectl port-forward demo-configmap-volume-pod-optional 8000:80
# Forwarding from 127.0.0.1:8000 -> 80
# Forwarding from [::1]:8000 -> 80

curl localhost:8000
# <html>
# <title>Home</title>
# <body>
# <h1> Home </h1>
# <p> This is home page </p>
# </body>
# </html>

curl localhost:8000/error.html
# <html>
# <title>Error</title>
# <body>
#   <h1> Error </h1>
#   <p> This is Error page </p>
# </body>
# </html>
```

---

### Specify a key

```sh
tee demo-configmap-volume-pod-key.yaml<<EOF
apiVersion: v1
kind: Pod
metadata:
  name: demo-configmap-volume-pod-key
spec:
  volumes:
  - name: nginx-config
    configMap:
      name: nginx-config
      optional: true    # optional
      items:
        - key: index.html
          path: index.html
  containers:
  - name: nginx
    image: nginx
    volumeMounts:
    - name: nginx-config
      mountPath: /usr/share/nginx/html
EOF

kubectl apply -f demo-configmap-volume-pod-key.yaml
# pod/demo-configmap-volume-pod-key created

kubectl get pod
# NAME                                 READY   STATUS    RESTARTS   AGE
# demo-configmap-volume-pod-key        1/1     Running   0          7s

kubectl port-forward demo-configmap-volume-pod-key 8080:80
# Forwarding from 127.0.0.1:8080 -> 80
# Forwarding from [::1]:8080 -> 80

# confirm: index pass
curl localhost:8080
# <html>
# <title>Home</title>
# <body>
# <h1> Home </h1>
# <p> This is home page </p>
# </body>
# </html>

# confirm: error not pass
url localhost:8080/error.html
# <html>
# <head><title>404 Not Found</title></head>
# <body>
# <center><h1>404 Not Found</h1></center>
# <hr><center>nginx/1.29.4</center>
# </body>
# </html>
```

- Exlpore file in container

```sh
# confirm symbolic link
kubectl exec -it demo-configmap-volume-pod-key -- ls -l /usr/share/nginx/html/index.html
# lrwxrwxrwx 1 root root 17 Dec 27 00:28 /usr/share/nginx/html/index.html -> ..data/index.html
```
