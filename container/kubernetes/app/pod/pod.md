# Kubernetes - Application: Pod

[Back](../../index.md)

- [Kubernetes - Application: Pod](#kubernetes---application-pod)
  - [Pod](#pod)
    - [Lifecycle](#lifecycle)
    - [How it works](#how-it-works)
    - [Imperative Commands](#imperative-commands)
    - [Declarative Commands](#declarative-commands)
    - [Lab: Create a pod using CLI](#lab-create-a-pod-using-cli)
    - [Lab: Pod Creation using Yaml File](#lab-pod-creation-using-yaml-file)
  - [Common Questions](#common-questions)
  - [Pod Network](#pod-network)
    - [Lab: testing pod-to-pod connectivity: one-off pod](#lab-testing-pod-to-pod-connectivity-one-off-pod)
    - [Lab: testing pod connectivity: port-forward](#lab-testing-pod-connectivity-port-forward)
  - [Log File](#log-file)
    - [Common Commands](#common-commands)
    - [Lab: Get and filter pod log file](#lab-get-and-filter-pod-log-file)
  - [Copy files to container](#copy-files-to-container)
  - [Execute Command on Container](#execute-command-on-container)
    - [Lab: Execute Command](#lab-execute-command)
    - [Lab: Multiple Container - log and exec](#lab-multiple-container---log-and-exec)
    - [Lab:](#lab)

---

## Pod

- `pod`
  - the **smallest deployable unit** in Kubernetes that represents a **single instance** of an **application**.
    - the smallest object that can be created in k8s
  - a collection of **containers** and its **storage** inside a **node** of a Kubernetes cluster.

---

### Lifecycle

- Pod Phases

  - `Pending`: The pod is **accepted** by Kubernetes, but containers **aren't created** or are **waiting for resources**.
  - `Running`: The pod is **bound to a node**, all containers are created, and **at least one** is running.
  - `Succeeded`: All containers **finished successfully** and **won't restart**.
  - `Failed`: All containers **terminated**, with at **least one failing**.
  - `Unknown`: The pod's state couldn't be **retrieved**.

- container states:
  - `Waiting`:
    - still running the operations it requires in order to complete start up
      - e.g.,
      - pulling the container image
      - applying Secret data
  - `Running`:
    - executing without issues.
  - `Terminated`:
    - have begun execution and then either ran to **completion** or **failed** for some reason.

---

### How it works

- command: `kubectl run mynginx --image=nginx`
  - `kubectl` CLI create pod object in API server via POST /api/pod
  - etcd
  - scheduler
  - kubelet
  - container runtime pull image and run container
  -

1. `kubectl` (client)

   - Reads `kubeconfig` (cluster endpoint + credentials).
   - Builds a Pod `manifest` (name mynginx, image nginx, default namespace, restartPolicy depending on version/flags).
   - Sends an HTTPS request to the API server via `POST .../api/v1/namespaces/<ns>/pods` with the Pod JSON/YAML.

2. `API Server` (kube-apiserver)

   - **Authenticates** you (TLS client cert / token / OIDC).
   - **Authorizes** the request (RBAC).
   - Runs admission control:
     - **Mutating** (e.g., default fields, inject sidecars if configured)
     - **Validating** (schema, policies, quota checks, PodSecurity, etc.)

3. `etcd`

   - **Stores** the Pod object (desired state + metadata).
   - Now the Pod exists but is typically **Pending** (no node assigned yet).

4. `Scheduler` (kube-scheduler)

   - Watches for Pods with:
     - `spec.nodeName` empty (unscheduled).
   - Runs **scheduling algorithm**:
     - **Filter nodes** (CPU/memory available, taints/tolerations, node selectors/affinity, required ports, etc.)
     - **Score** remaining nodes (spread, balance, affinity preferences, etc.)
   - **Chooses a node** and “binds” the Pod by updating it:
     - Sets `spec.nodeName = <chosen-node>`

5. `kubelet` (on the chosen node)

   - **Watches** the `API server` for Pods assigned to this node.
   - Sees `mynginx` and begins to make reality match desired state:
     - Prepares directories, volumes, secrets/configmaps (if any).
     - **Calls** the `container runtime` via `CRI`.

6. `Container runtime` (containerd / CRI-O)

   - **Pulls** the image (nginx) from a registry:
     - Handles image layers, caching, authentication (if private registry).
     - Creates the Pod sandbox (pause container) and networking.
     - Creates and starts the nginx container.

7. **CNI plugin** (networking)

   - Sets up Pod networking:
     - **Attaches** Pod to **cluster network**, assigns `Pod IP`.
     - Programs **routes/iptables/eBPF rules** depending on the `CNI` (Calico, Cilium, Flannel, etc.)

8. `kube-proxy` (service networking)

   - Programs node-level **forwarding rules** for `Services`.

9. Status updates back to API server
   - `kubelet` **reports** Pod status (via API server):
     - Pending → ContainerCreating → Running
   - Events are recorded (image pull, started container, etc.)

---

### Imperative Commands

| **Command**                                          | **Description**                                             |
| ---------------------------------------------------- | ----------------------------------------------------------- |
| `kubectl get pods`                                   | List all pods in the current namespace                      |
| `kubectl get pods -A`                                | List pods across **all namespaces**                         |
| `kubectl get pods -o wide`                           | List pods with extra details                                |
| `kubectl get pods --watch`                           | Streams updates as Pod states change.                       |
| `kubectl describe pod pod_name`                      | Show detailed information about a specific pod              |
| `kubectl logs pod_name`                              | View logs from a pod's main container                       |
| `kubectl logs pod_name -c container_name`            | View logs for a specific container in a multi-container pod |
| `kubectl exec -it pod_name -- commands`              | Execute a command inside the pod (e.g., get a shell)        |
| `kubectl delete pod pod_name`                        | Delete a specific pod                                       |
| `kubectl port-forward <pod> <local-port>:<pod-port>` | Forward ports from a Pod to your local machine.             |

- Run

| CMD                                                                                                   | DESC                                                          |
| ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| `kubectl run pod_name --image=image_name`                                                             | Create a pod using a specified image (for testing)            |
| `kubectl run pod_name --image=image_name --labels="key1=val1,key2=val2"`                              | Create pod with labels                                        |
| `kubectl run pod_name --image=image_name --port=8080`                                                 | Create pod with port                                          |
| `kubectl run pod_name --image=image_name --command -- sleep 1000`                                     | Create a pod with command                                     |
| `kubectl run pod_name --image=image_name --dry-run=client`                                            | simulate the creation of a resource without actually applying |
| `kubectl run pod_name --image=image_name --dry-run=client -o yaml`                                    | View full YAML configuration of a pod                         |
| `kubectl run pod_name --image=image_name --dry-run=client -o yaml -command -- sleep 1000 > yaml_file` | View full YAML configuration of a pod with command            |

- List Pod: `kubectl list pod`

  - NAME:
    - e.g., kiada-9d785b578-58vhc
  - READY
    - e.g., 1/1
    - the number of ready containers/the desired of containers
  - STATUS
    - e.g., Running
    - status of the pod
  - RESTARTS
    - e.g., 0
    - how many times the pod is restarted
    - indicate instability
  - AGE
    - e.g., 17s
    - Time since the **Deployment** object was created

- Common pod status:
  - `running`: pod is created and running
  - `Pending`: waiting for scheduling or image pull
  - `CrashLoopBackOff`: container keeps crashing
  - `ImagePullBackOff`: image pull failed
  - `Terminating`: Pod being replaced or deleted

---

### Declarative Commands

| CMD                                | DESC                                      |
| ---------------------------------- | ----------------------------------------- |
| `kubectl create -f yaml_file`      | Create a Pod from a YAML file or JSON.    |
| `kubectl apply -f yaml_file`       | Create or update a pod from YAML manifest |
| `kubectl get pod pod_name -o yaml` | View full YAML configuration of a pod     |

- yaml

```yaml
# nginx.yml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
    - name: nginx
      image: nginx:latest
      ports:
        containerPort: 7500
```

---

### Lab: Create a pod using CLI

```sh
# create
kubectl run nginx --image=nginx
# pod/nginx created

# confirm
kubectl get pods
# NAME    READY   STATUS    RESTARTS   AGE
# nginx   1/1     Running   0          45s

kubectl get pods -o wide
# NAME    READY   STATUS    RESTARTS   AGE     IP            NODE       NOMINATED NODE   READINESS GATES
# nginx   1/1     Running   0          4m13s   10.244.0.11   minikube   <none>

# show detail information
kubectl describe pod nginx
# Name:             nginx
# Namespace:        default
# Priority:         0
# Service Account:  default
# Node:             minikube/192.168.49.2
# Start Time:       Fri, 02 May 2025 13:13:50 -0400
# Labels:           run=nginx
# IP:               10.244.0.11
# ...

# output
kubectl get pod nginx -o yaml
# apiVersion: v1
# kind: Pod
# metadata:
#   creationTimestamp: "2025-09-19T15:33:27Z"
#   labels:
#     run: nginx
#   name: nginx
#   namespace: default
#   resourceVersion: "4279272"
#   uid: c9de93b7-53db-43f5-869a-6efe73484cb8
# spec:
#   containers:
#   - image: nginx
#     imagePullPolicy: Always
# ...

# output to a yaml file
kubectl get pod nginx -o yaml > nginx.yaml

# remove
kubectl delete pod nginx
# pod "nginx" deleted
```

---

### Lab: Pod Creation using Yaml File

- Define `pod-def.yaml`

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  # user custom label
  labels:
    app: myapp
    tier: front-end
spec:
  # a list
  containers:
    - name: nginx-container
      image: nginx
```

- Create pod

```sh
kubectl create -f pod-def.yaml
# pod/myapp-pod created

# confirm
kubectl get pods
# NAME        READY   STATUS    RESTARTS   AGE
# myapp-pod   1/1     Running   0          12s

# view detailed info
kubectl describe pod myapp-pod
# Name:             myapp-pod
# Namespace:        default
# Priority:         0
# Service Account:  default
# Node:             minikube/192.168.49.2
# Start Time:       Fri, 02 May 2025 14:29:58 -0400
# Labels:           app=myapp
#                   type=front-end
# Annotations:      <none>
# Status:           Running
# IP:               10.244.0.12
# ...

# cleanup
kubectl delete pod myapp-pod
# pod "myapp-pod" deleted

kubectl get pods
# No resources found in default namespace.
```

---

## Common Questions

| Q                                                                  | CMD                                                                                                        |
| ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| how many pods are running                                          | `kubectl get pods`                                                                                         |
| Create a new pod with nginx image                                  | `kubectl run nignx-pod --image=nignx`                                                                      |
| What is image used to create new pods                              | `kubectl describe pod nignx-pod`                                                                           |
| Which node is this pod running on                                  | `kubectl describe pod nignx-pod` / `kubectl get pods -o wide`                                              |
| How many containers are part of a pod                              | `kubectl get pod nignx-pod`, Containers                                                                    |
| What is the state of the container X in a pod Y                    | `kubectl describe pod nginx \| grep "State:"`                                                              |
| Why the container X in pod Y is in error                           | `kubectl describe pod nignx-pod`, Containers,State,Reason. / Events                                        |
| What does the READY columns in kubectl get pods                    | Running Containers in pod/Total container in pod                                                           |
| Delete a pod                                                       | `kubectl delete pod nignx-pod`                                                                             |
| Create a pod named redis and with image redis123, output yaml file | `kubectl run redis --image=redis123 --dry-run=client -o yaml > redis.yaml`, `kubectl create -f redis.yaml` |
| Change the image to redis, pod should be running                   | update yaml file, `kubectl apply -f redis.yaml`                                                            |

---

## Pod Network

- Methods to find the pod ip

  - `kubectl get pod NAME -o wide`
  - `kubectl describe pod NAME`
  - `kubectl get pod NAME -o yaml`

---

- Pod connection

  - By default
    - **Every** `Pod` can communicate with every other `Pod` without NAT (Network Address Translation).
      - Each pod is accessible for other pod whenever it is in the same node.
    - **Every** `Pod` is accessbile for **every** `node` in the cluster.
  - Can be customized by Nerwork rule

---

- Methods to connect to a pod:
  - ssh to node; connect from the node.
  - use one-off pod
    - `kubectl run --image=curlimages/curl -it --restart=Never --rm POD_NAME`
  - use port-forward proxy
    - `kubectl port forwarding pod POD_NAME PORT`
    - Multiple components involved underneath
      - curl -> kubectl -> API server -> kubelet on the node -> pod (using loopback device)

---

### Lab: testing pod-to-pod connectivity: one-off pod

```sh
# get ip
kubectl get pod -o wide
# NAME                   READY   STATUS    RESTARTS   AGE   IP          NODE             NOMINATED NODE   READINESS GATES
# web-64c966cf88-9cnn9   1/1     Running   0          18m   10.1.2.56   docker-desktop   <none>           <none>
# web-64c966cf88-x57zc   1/1     Running   0          18m   10.1.2.57   docker-desktop   <none>           <none>

# test pod with ip
kubectl run --image=curlimages/curl -it --restart=Never --rm one-off-pod -- curl 10.1.2.56
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
# pod "one-off-pod" deleted from default namespace
```

---

### Lab: testing pod connectivity: port-forward

```sh
kubectl get pod
# NAME                   READY   STATUS    RESTARTS   AGE
# web-64c966cf88-9cnn9   1/1     Running   0          56m
# web-64c966cf88-x57zc   1/1     Running   0          56m

kubectl port-forward pod web-64c966cf88-9cnn9 8081:80
# Forwarding from 127.0.0.1:8081 -> 80
# Forwarding from [::1]:8081 -> 80

curl 127.0.0.1:8081
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

## Log File

- `log file`

  - Kubernetes keeps a **separate log file** for **each** `container`.
  - default path:
    - `/var/log/containers` **on the node** that runs the container
  - `kubectl logs` only shows the log file of the **current** `primary container` of the pod.
    - use option `-p` for previous log
    - by default, return the log of the 1st container
      - use option `-c` for a specific container
  - When you **delete** a `pod`, all its `log files` are **also deleted**.
    - Further configuration is required if the log file needs to be stored centrally and permanently.

- `lof file` may also be **rotated** when they reach a **certain size**.

  - when the log is rotated, the streaming log `kubectl logs -f` needs to restart.

---

### Common Commands

| CMD                                                       | DESC                                     |
| --------------------------------------------------------- | ---------------------------------------- |
| `kubectl logs POD_NAME`                                   | display the log of the pod               |
| `kubectl logs POD_NAME -c CONTAINER`                      | display the log of a container in a pod  |
| `kubectl logs POD_NAME --all-containers`                  | display the log of ll container in a pod |
| `kubectl logs POD_NAME -f`                                | Stream log                               |
| `kubectl logs POD_NAME --timestamps=true`                 | display log with timestamps              |
| `kubectl logs POD_NAME --since=2m`                        | display log in the last two minutes      |
| `kubectl logs POD_NAME --since-time=2025-12-21T09:50:00Z` | print logs produced after a timestamp    |
| `kubectl logs POD_NAME --tail=10`                         | print last 10 lines                      |
| `kubectl logs POD_NAME --previous`                        | print previous log                       |

---

### Lab: Get and filter pod log file

```sh
kubectl get pod -o wide
# NAME                   READY   STATUS    RESTARTS   AGE    IP          NODE             NOMINATED NODE   READINESS GATES
# web-64c966cf88-9cnn9   1/1     Running   0          103m   10.1.2.56   docker-desktop   <none>           <none>
# web-64c966cf88-x57zc   1/1     Running   0          103m   10.1.2.57   docker-desktop   <none>           <none>

kubectl logs web-64c966cf88-9cnn9
# /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
# /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
# /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
# 10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
# 10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
# /docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
# /docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
# /docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
# /docker-entrypoint.sh: Configuration complete; ready for start up
# 2025/12/21 19:03:01 [notice] 1#1: using the "epoll" event method
# 2025/12/21 19:03:01 [notice] 1#1: nginx/1.29.4
# 2025/12/21 19:03:01 [notice] 1#1: built by gcc 14.2.0 (Debian 14.2.0-19)
# 2025/12/21 19:03:01 [notice] 1#1: OS: Linux 5.15.153.1-microsoft-standard-WSL2
# 2025/12/21 19:03:01 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576
# 2025/12/21 19:03:01 [notice] 1#1: start worker processes
# 2025/12/21 19:03:01 [notice] 1#1: start worker process 29
# 2025/12/21 19:03:01 [notice] 1#1: start worker process 30
# 2025/12/21 19:03:01 [notice] 1#1: start worker process 31
# 2025/12/21 19:03:01 [notice] 1#1: start worker process 32
# 2025/12/21 19:03:01 [notice] 1#1: start worker process 33
# 2025/12/21 19:03:01 [notice] 1#1: start worker process 34
# 2025/12/21 19:03:01 [notice] 1#1: start worker process 35
# 2025/12/21 19:03:01 [notice] 1#1: start worker process 36
# 2025/12/21 19:03:01 [notice] 1#1: start worker process 37
# 2025/12/21 19:03:01 [notice] 1#1: start worker process 38
# 2025/12/21 19:03:01 [notice] 1#1: start worker process 39
# 2025/12/21 19:03:01 [notice] 1#1: start worker process 40
# 10.1.2.61 - - [21/Dec/2025:19:21:50 +0000] "GET / HTTP/1.1" 200 615 "-" "curl/8.17.0" "-"
# 127.0.0.1 - - [21/Dec/2025:20:02:11 +0000] "GET / HTTP/1.1" 200 615 "-" "curl/8.5.0" "-"

kubectl logs web-64c966cf88-9cnn9 --timestamps=true
# 2025-12-21T19:03:00.937972766Z /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
# 2025-12-21T19:03:00.938002411Z /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
# 2025-12-21T19:03:00.941261602Z /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
# 2025-12-21T19:03:00.969406511Z 10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
# 2025-12-21T19:03:01.064370461Z 10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
# 2025-12-21T19:03:01.068851378Z /docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
# 2025-12-21T19:03:01.074121268Z /docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
# 2025-12-21T19:03:01.107634021Z /docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
# 2025-12-21T19:03:01.111841790Z /docker-entrypoint.sh: Configuration complete; ready for start up
# 2025-12-21T19:03:01.273753778Z 2025/12/21 19:03:01 [notice] 1#1: using the "epoll" event method
# 2025-12-21T19:03:01.273770621Z 2025/12/21 19:03:01 [notice] 1#1: nginx/1.29.4
# 2025-12-21T19:03:01.274093244Z 2025/12/21 19:03:01 [notice] 1#1: built by gcc 14.2.0 (Debian 14.2.0-19)
# 2025-12-21T19:03:01.274112273Z 2025/12/21 19:03:01 [notice] 1#1: OS: Linux 5.15.153.1-microsoft-standard-WSL2
# 2025-12-21T19:03:01.274117409Z 2025/12/21 19:03:01 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576
# 2025-12-21T19:03:01.274745064Z 2025/12/21 19:03:01 [notice] 1#1: start worker processes
# 2025-12-21T19:03:01.275196359Z 2025/12/21 19:03:01 [notice] 1#1: start worker process 29
# 2025-12-21T19:03:01.278268093Z 2025/12/21 19:03:01 [notice] 1#1: start worker process 30
# 2025-12-21T19:03:01.278289714Z 2025/12/21 19:03:01 [notice] 1#1: start worker process 31
# 2025-12-21T19:03:01.278291494Z 2025/12/21 19:03:01 [notice] 1#1: start worker process 32
# 2025-12-21T19:03:01.278292883Z 2025/12/21 19:03:01 [notice] 1#1: start worker process 33
# 2025-12-21T19:03:01.278294196Z 2025/12/21 19:03:01 [notice] 1#1: start worker process 34
# 2025-12-21T19:03:01.278295509Z 2025/12/21 19:03:01 [notice] 1#1: start worker process 35
# 2025-12-21T19:03:01.278296819Z 2025/12/21 19:03:01 [notice] 1#1: start worker process 36
# 2025-12-21T19:03:01.278298357Z 2025/12/21 19:03:01 [notice] 1#1: start worker process 37
# 2025-12-21T19:03:01.278299658Z 2025/12/21 19:03:01 [notice] 1#1: start worker process 38
# 2025-12-21T19:03:01.278300996Z 2025/12/21 19:03:01 [notice] 1#1: start worker process 39
# 2025-12-21T19:03:01.278999792Z 2025/12/21 19:03:01 [notice] 1#1: start worker process 40
# 2025-12-21T19:21:50.360384177Z 10.1.2.61 - - [21/Dec/2025:19:21:50 +0000] "GET / HTTP/1.1" 200 615 "-" "curl/8.17.0" "-"
# 2025-12-21T20:02:11.284262245Z 127.0.0.1 - - [21/Dec/2025:20:02:11 +0000] "GET / HTTP/1.1" 200 615 "-" "curl/8.5.0" "-"

kubectl logs web-64c966cf88-9cnn9 --tail=10
# 2025/12/21 19:03:01 [notice] 1#1: start worker process 33
# 2025/12/21 19:03:01 [notice] 1#1: start worker process 34
# 2025/12/21 19:03:01 [notice] 1#1: start worker process 35
# 2025/12/21 19:03:01 [notice] 1#1: start worker process 36
# 2025/12/21 19:03:01 [notice] 1#1: start worker process 37
# 2025/12/21 19:03:01 [notice] 1#1: start worker process 38
# 2025/12/21 19:03:01 [notice] 1#1: start worker process 39
# 2025/12/21 19:03:01 [notice] 1#1: start worker process 40
# 10.1.2.61 - - [21/Dec/2025:19:21:50 +0000] "GET / HTTP/1.1" 200 615 "-" "curl/8.17.0" "-"
# 127.0.0.1 - - [21/Dec/2025:20:02:11 +0000] "GET / HTTP/1.1" 200 615 "-" "curl/8.5.0" "-"

kubectl logs web-64c966cf88-9cnn9 --since=60m
# 127.0.0.1 - - [21/Dec/2025:20:02:11 +0000] "GET / HTTP/1.1" 200 615 "-" "curl/8.5.0" "-"
```

---

## Copy files to container

| CMD                                             | DESC                         |
| ----------------------------------------------- | ---------------------------- |
| `kubectl cp POD_NAME:container_path local_path` | copy container file to local |
| `kubectl cp local_path POD_NAME:container_path` | copy local file to container |

---

## Execute Command on Container

- double dash (`--`) in the command delimits **kubectl arguments** from the **command** to be executed in the container

| CMD                                | DESC                                                                    |
| ---------------------------------- | ----------------------------------------------------------------------- |
| `kubectl exec POD_NAME -- COMMAND` | Invoke a single command                                                 |
| `kubectl exec -it POD_NAME -- sh`  | Running an interactive shell                                            |
| `kubectl exec -it POD_NAME -- sh`  | Running an interactive shell                                            |
| `kubectl attach -i POD_NAME`       | attaches to the standard input, output and error streams of a container |

---

### Lab: Execute Command

```sh
kubectl get pod
# NAME                   READY   STATUS    RESTARTS   AGE
# web-64c966cf88-9cnn9   1/1     Running   0          123m
# web-64c966cf88-x57zc   1/1     Running   0          123m

kubectl exec web-64c966cf88-9cnn9 -- hostname
# web-64c966cf88-9cnn9
kubectl exec web-64c966cf88-9cnn9 -- curl -s localhost:80
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


kubectl exec -it web-64c966cf88-9cnn9 -- sh
```

---

### Lab: Multiple Container - log and exec

- multi-container-log-demo.yaml

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: multi-container-log-demo
spec:
  containers:
    - name: busybox
      image: busybox
      command: ["sh", "-c", "echo The app is running! && sleep 3600"]
    - name: redis
      image: redis
```

- Log

```sh
kubectl apply -f multi-container-log-demo.yaml
# pod/multi-container-log-demo created

kubectl logs multi-container-log-demo
# Defaulted container "busybox" out of: busybox, redis
# The app is running!

kubectl logs multi-container-log-demo -c busybox
# The app is running!

kubectl logs multi-container-log-demo -c redis
# Starting Redis Server
# 1:C 21 Dec 2025 21:48:21.004 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
# 1:C 21 Dec 2025 21:48:21.005 * Redis version=8.4.0, bits=64, commit=00000000, modified=1, pid=1, just started
# 1:C 21 Dec 2025 21:48:21.005 * Configuration loaded
# 1:M 21 Dec 2025 21:48:21.006 * monotonic clock: POSIX clock_gettime
# 1:M 21 Dec 2025 21:48:21.007 * Running mode=standalone, port=6379.
# 1:M 21 Dec 2025 21:48:21.009 * <bf> RedisBloom version 8.4.0 (Git=unknown)
# ...

kubectl logs multi-container-log-demo --all-containers
# The app is running!
# Starting Redis Server
# 1:C 21 Dec 2025 21:48:21.004 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
# 1:C 21 Dec 2025 21:48:21.005 * Redis version=8.4.0, bits=64, commit=00000000, modified=1, pid=1, just started
# 1:C 21 Dec 2025 21:48:21.005 * Configuration loaded
# 1:M 21 Dec 2025 21:48:21.006 * monotonic clock: POSIX clock_gettime
# 1:M 21 Dec 2025 21:48:21.007 * Running mode=standalone, port=6379.
# 1:M 21 Dec 2025 21:48:21.009 * <bf> RedisBloom version 8.4.0 (Git=unknown)
```

- Exec

```sh
kubectl exec -it multi-container-log-demo -c busybox -- hostname
# multi-container-log-demo

kubectl exec -it multi-container-log-demo -c redis -- redis-cli -v
# redis-cli 8.4.0
```

---

### Lab: 