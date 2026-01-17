# Kubernetes - Pod: Static Pod

[Back](../../index.md)

- [Kubernetes - Pod: Static Pod](#kubernetes---pod-static-pod)
  - [Static Pod](#static-pod)
    - [vs DaemonSets](#vs-daemonsets)
    - [Designated Directory for manifest file](#designated-directory-for-manifest-file)
  - [Common Command](#common-command)
  - [Lab: Create \& Remove Static Pod](#lab-create--remove-static-pod)
  - [Lab: static pod - `apiserver`](#lab-static-pod---apiserver)
  - [Lab: Static Pod - `etcd`](#lab-static-pod---etcd)
  - [Lab: Static Pod - `schedule`](#lab-static-pod---schedule)
  - [Lab: Static Pod - `controller-manager`](#lab-static-pod---controller-manager)

---

## Static Pod

- `static pod`

  - A `Pod` **managed directly** by the `kubelet` on a node
    - not by the `API server`, `scheduler`, or `controllers`.
  - The `kubelet` periodically checks a **local directory** for `Pod manifest files` (YAML).
    - If a file **appears/changes**, the kubelet **creates/updates** the Pod on that node only.
    - If the `static pod` crashes, `kubelet` attempts ot restart it.

- vs common pod:

  - common pods managed by K8S cluster components
  - static pod managed by `kubelet`

- Feature:

  - **No scheduler**:
    - The Pod always runs on the node whose `kubelet` loaded the file.
  - **Mirror Pod**:
    - The `kubelet` creates a read-only “mirror” `Pod` object in the `API server` so kubectl get pods can show it. API 可见且只读
    - The Pod name gets a `-<nodeName>` suffix.
  - Lifecycle tied to file:
    - Add/modify/delete the **manifest file** → kubelet creates/updates/stops the **Pod**.
  - **No controllers**:
    - don’t get ReplicaSets, Jobs, rollouts, or auto-restarts by a `controller`
    - `kubelet` will **restart containers** if they crash per its restart policy, but there’s no higher-level management.
  - **Node-scoped**:
    - Each node can have different static Pods by placing different files on each node.

- Common use cases:
  - used by `kubeadm` to **bootstrap control-plane components** (kube-apiserver, kube-scheduler, etc.)
  - **Node-local agents/daemons** that must run even if the API server is down.

---

### vs DaemonSets

| Static Pods                             | DaemonSets                                                      |
| --------------------------------------- | --------------------------------------------------------------- |
| Ignored by `kube-scheduler`             | Ignored by `kube-scheduler`                                     |
| Managed by `kubelet`                    | Managed by `kube-apiserver`(DaemonSet Controller)               |
| Used to deploy control-plane components | Used to deploy agent on nodes (Monitoring, logging, networking) |

---

### Designated Directory for manifest file

- default location: `/etc/kubernetes/manifests`

---

- Identify the location:

```sh
cat /var/lib/kubelet/config.yaml | grep staticPodPath
# staticPodPath: /etc/kubernetes/manifests
```

---

- Specify a path in `kubectl` service

  - Service file:
    ```conf
    ExecStar=/usr/local/bin/kubelet
        --container-runtime=remote
        --container-runtime-ndpoints=unix:///var/run/containerd/containerd.sock
        --pod-manifest-path=/etc/kubernetes/manifests   # specify path
        --kubeconfig=/var/lib/kubelet/kubeconfig
        --network-plugin=cni
        --register-node=true
        --v=2
    ```

- Specify a conf file, then specify in the cf
  - Service file:
    ```conf
    ExecStar=/usr/local/bin/kubelet
        --container-runtime=remote
        --container-runtime-ndpoints=unix:///var/run/containerd/containerd.sock
        --config=kubeconfig.yaml   # specify a cf
        --kubeconfig=/var/lib/kubelet/kubeconfig
        --network-plugin=cni
        --register-node=true
        --v=2
    ```
  - config file:
    ```yaml
    staticPodPath: /etc/kubernetes/manifests
    ```

---

## Common Command

- Since it is managed by `kubelet` on each node,
  - `kubectl` is only used to read.

| Command                                     | Desc                                |
| ------------------------------------------- | ----------------------------------- |
| `docker ps`                                 | List the static pod on node         |
| `kubectl get pod -A \| grep -E *-node_name` | List the static pod in API endpoint |

---

## Lab: Create & Remove Static Pod

```yaml
# /etc/kubernetes/manifests/static-web.yaml
apiVersion: v1
kind: Pod
metadata:
  name: static-web
  labels:
    role: myrole
spec:
  containers:
    - name: web
      image: nginx
      ports:
        - name: web
          containerPort: 80
          protocol: TCP
```

```sh
# confirm: kubelet automatically create
# on controlplane node
kubectl get pod -A -l role=myrole -o wide
# NAMESPACE   NAME                      READY   STATUS    RESTARTS   AGE     IP            NODE           NOMINATED NODE   READINESS GATES
# default     static-web-controlplane   1/1     Running   0          2m43s   10.244.0.12   controlplane   <none>           <none>

```

- remove manifest

```sh
sudo rm /etc/kubernetes/manifests/static-web.yaml

# confirm
kubectl get pod -A -l role=myrole
# No resources found
```

---

## Lab: static pod - `apiserver`

```sh
# get manifest
sudo cat /etc/kubernetes/manifests/kube-apiserver.yaml
# apiVersion: v1
# kind: Pod
# metadata:
#   annotations:
#     kubeadm.kubernetes.io/kube-apiserver.advertise-address.endpoint: 192.168.10.150:6443
#   creationTimestamp: null
#   labels:
#     component: kube-apiserver
#     tier: control-plane
#   name: kube-apiserver
#   namespace: kube-system
# spec:
#   containers:
#   - command:
#     - kube-apiserver
#     - --advertise-address=192.168.10.150
#     - --allow-privileged=true
#     - --authorization-mode=Node,RBAC
#     - --client-ca-file=/etc/kubernetes/pki/ca.crt
#     - --enable-admission-plugins=NodeRestriction
#     - --enable-bootstrap-token-auth=true
#     - --etcd-cafile=/etc/kubernetes/pki/etcd/ca.crt
#     - --etcd-certfile=/etc/kubernetes/pki/apiserver-etcd-client.crt
#     - --etcd-keyfile=/etc/kubernetes/pki/apiserver-etcd-client.key
#     - --etcd-servers=https://127.0.0.1:2379
#     - --kubelet-client-certificate=/etc/kubernetes/pki/apiserver-kubelet-client.crt
#     - --kubelet-client-key=/etc/kubernetes/pki/apiserver-kubelet-client.key
#     - --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
#     - --proxy-client-cert-file=/etc/kubernetes/pki/front-proxy-client.crt
#     - --proxy-client-key-file=/etc/kubernetes/pki/front-proxy-client.key
#     - --requestheader-allowed-names=front-proxy-client
#     - --requestheader-client-ca-file=/etc/kubernetes/pki/front-proxy-ca.crt
#     - --requestheader-extra-headers-prefix=X-Remote-Extra-
#     - --requestheader-group-headers=X-Remote-Group
#     - --requestheader-username-headers=X-Remote-User
#     - --secure-port=6443
#     - --service-account-issuer=https://kubernetes.default.svc.cluster.local
#     - --service-account-key-file=/etc/kubernetes/pki/sa.pub
#     - --service-account-signing-key-file=/etc/kubernetes/pki/sa.key
#     - --service-cluster-ip-range=10.96.0.0/12
#     - --tls-cert-file=/etc/kubernetes/pki/apiserver.crt
#     - --tls-private-key-file=/etc/kubernetes/pki/apiserver.key
#     image: registry.k8s.io/kube-apiserver:v1.32.11
#     imagePullPolicy: IfNotPresent
#     livenessProbe:
#       failureThreshold: 8
#       httpGet:
#         host: 192.168.10.150
#         path: /livez
#         port: 6443
#         scheme: HTTPS
#       initialDelaySeconds: 10
#       periodSeconds: 10
#       timeoutSeconds: 15
#     name: kube-apiserver
#     readinessProbe:
#       failureThreshold: 3
#       httpGet:
#         host: 192.168.10.150
#         path: /readyz
#         port: 6443
#         scheme: HTTPS
#       periodSeconds: 1
#       timeoutSeconds: 15
#     resources:
#       requests:
#         cpu: 250m
#     startupProbe:
#       failureThreshold: 24
#       httpGet:
#         host: 192.168.10.150
#         path: /livez
#         port: 6443
#         scheme: HTTPS
#       initialDelaySeconds: 10
#       periodSeconds: 10
#       timeoutSeconds: 15
#     volumeMounts:
#     - mountPath: /etc/ssl/certs
#       name: ca-certs
#       readOnly: true
#     - mountPath: /etc/ca-certificates
#       name: etc-ca-certificates
#       readOnly: true
#     - mountPath: /etc/kubernetes/pki
#       name: k8s-certs
#       readOnly: true
#     - mountPath: /usr/local/share/ca-certificates
#       name: usr-local-share-ca-certificates
#       readOnly: true
#     - mountPath: /usr/share/ca-certificates
#       name: usr-share-ca-certificates
#       readOnly: true
#   hostNetwork: true
#   priority: 2000001000
#   priorityClassName: system-node-critical
#   securityContext:
#     seccompProfile:
#       type: RuntimeDefault
#   volumes:
#   - hostPath:
#       path: /etc/ssl/certs
#       type: DirectoryOrCreate
#     name: ca-certs
#   - hostPath:
#       path: /etc/ca-certificates
#       type: DirectoryOrCreate
#     name: etc-ca-certificates
#   - hostPath:
#       path: /etc/kubernetes/pki
#       type: DirectoryOrCreate
#     name: k8s-certs
#   - hostPath:
#       path: /usr/local/share/ca-certificates
#       type: DirectoryOrCreate
#     name: usr-local-share-ca-certificates
#   - hostPath:
#       path: /usr/share/ca-certificates
#       type: DirectoryOrCreate
#     name: usr-share-ca-certificates
# status: {}

# get api server pod
kubectl get pod kube-apiserver-controlplane -n kube-system -o wide
# NAME                          READY   STATUS    RESTARTS   AGE     IP               NODE           NOMINATED NODE   READINESS GATES
# kube-apiserver-controlplane   1/1     Running   0          2d19h   192.168.10.150   controlplane   <none>           <none>

kubectl describe pod kube-apiserver-controlplane -n kube-system
# Name:                 kube-apiserver-controlplane
# Namespace:            kube-system
# Priority:             2000001000
# Priority Class Name:  system-node-critical
# Node:                 controlplane/192.168.10.150
# Start Time:           Thu, 15 Jan 2026 11:45:30 -0500
# Labels:               component=kube-apiserver
#                       tier=control-plane
# Annotations:          kubeadm.kubernetes.io/kube-apiserver.advertise-address.endpoint: 192.168.10.150:6443
#                       kubernetes.io/config.hash: 0083078086eef218b6760a60bc533112
#                       kubernetes.io/config.mirror: 0083078086eef218b6760a60bc533112
#                       kubernetes.io/config.seen: 2026-01-12T19:08:51.371589737-05:00
#                       kubernetes.io/config.source: file
# Status:               Running
# SeccompProfile:       RuntimeDefault
# IP:                   192.168.10.150
# IPs:
#   IP:           192.168.10.150
# Controlled By:  Node/controlplane
# Containers:
#   kube-apiserver:
#     Container ID:  containerd://e32246e2c8f1b06c572dae61c39b16ff1849c7fe6acb2ccf437c04fcc1ddcd60
#     Image:         registry.k8s.io/kube-apiserver:v1.32.11
#     Image ID:      registry.k8s.io/kube-apiserver@sha256:41eaecaed9af0ca8ab36d7794819c7df199e68c6c6ee0649114d713c495f8bd5
#     Port:          <none>
#     Host Port:     <none>
#     Command:
#       kube-apiserver
#       --advertise-address=192.168.10.150
#       --allow-privileged=true
#       --authorization-mode=Node,RBAC
#       --client-ca-file=/etc/kubernetes/pki/ca.crt
#       --enable-admission-plugins=NodeRestriction
#       --enable-bootstrap-token-auth=true
#       --etcd-cafile=/etc/kubernetes/pki/etcd/ca.crt
#       --etcd-certfile=/etc/kubernetes/pki/apiserver-etcd-client.crt
#       --etcd-keyfile=/etc/kubernetes/pki/apiserver-etcd-client.key
#       --etcd-servers=https://127.0.0.1:2379
#       --kubelet-client-certificate=/etc/kubernetes/pki/apiserver-kubelet-client.crt
#       --kubelet-client-key=/etc/kubernetes/pki/apiserver-kubelet-client.key
#       --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
#       --proxy-client-cert-file=/etc/kubernetes/pki/front-proxy-client.crt
#       --proxy-client-key-file=/etc/kubernetes/pki/front-proxy-client.key
#       --requestheader-allowed-names=front-proxy-client
#       --requestheader-client-ca-file=/etc/kubernetes/pki/front-proxy-ca.crt
#       --requestheader-extra-headers-prefix=X-Remote-Extra-
#       --requestheader-group-headers=X-Remote-Group
#       --requestheader-username-headers=X-Remote-User
#       --secure-port=6443
#       --service-account-issuer=https://kubernetes.default.svc.cluster.local
#       --service-account-key-file=/etc/kubernetes/pki/sa.pub
#       --service-account-signing-key-file=/etc/kubernetes/pki/sa.key
#       --service-cluster-ip-range=10.96.0.0/12
#       --tls-cert-file=/etc/kubernetes/pki/apiserver.crt
#       --tls-private-key-file=/etc/kubernetes/pki/apiserver.key
#     State:          Running
#       Started:      Thu, 15 Jan 2026 14:21:48 -0500
#     Ready:          True
#     Restart Count:  0
#     Requests:
#       cpu:        250m
#     Liveness:     http-get https://192.168.10.150:6443/livez delay=10s timeout=15s period=10s #success=1 #failure=8
#     Readiness:    http-get https://192.168.10.150:6443/readyz delay=0s timeout=15s period=1s #success=1 #failure=3
#     Startup:      http-get https://192.168.10.150:6443/livez delay=10s timeout=15s period=10s #success=1 #failure=24
#     Environment:  <none>
#     Mounts:
#       /etc/ca-certificates from etc-ca-certificates (ro)
#       /etc/kubernetes/pki from k8s-certs (ro)
#       /etc/ssl/certs from ca-certs (ro)
#       /usr/local/share/ca-certificates from usr-local-share-ca-certificates (ro)
#       /usr/share/ca-certificates from usr-share-ca-certificates (ro)
# Conditions:
#   Type                        Status
#   PodReadyToStartContainers   True
#   Initialized                 True
#   Ready                       True
#   ContainersReady             True
#   PodScheduled                True
# Volumes:
#   ca-certs:
#     Type:          HostPath (bare host directory volume)
#     Path:          /etc/ssl/certs
#     HostPathType:  DirectoryOrCreate
#   etc-ca-certificates:
#     Type:          HostPath (bare host directory volume)
#     Path:          /etc/ca-certificates
#     HostPathType:  DirectoryOrCreate
#   k8s-certs:
#     Type:          HostPath (bare host directory volume)
#     Path:          /etc/kubernetes/pki
#     HostPathType:  DirectoryOrCreate
#   usr-local-share-ca-certificates:
#     Type:          HostPath (bare host directory volume)
#     Path:          /usr/local/share/ca-certificates
#     HostPathType:  DirectoryOrCreate
#   usr-share-ca-certificates:
#     Type:          HostPath (bare host directory volume)
#     Path:          /usr/share/ca-certificates
#     HostPathType:  DirectoryOrCreate
# QoS Class:         Burstable
# Node-Selectors:    <none>
# Tolerations:       :NoExecute op=Exists
# Events:
#   Type    Reason   Age                 From     Message
#   ----    ------   ----                ----     -------
#   Normal  Killing  27m                 kubelet  Stopping container kube-apiserver
#   Normal  Pulled   11m (x3 over 168m)  kubelet  Container image "registry.k8s.io/kube-apiserver:v1.32.11" already present on machine
#   Normal  Created  11m (x3 over 168m)  kubelet  Created container: kube-apiserver
#   Normal  Started  11m (x3 over 168m)  kubelet  Started container kube-apiserver
```

---

## Lab: Static Pod - `etcd`

```sh
# get manifest
sudo cat /etc/kubernetes/manifests/etcd.yaml
# apiVersion: v1
# kind: Pod
# metadata:
#   annotations:
#     kubeadm.kubernetes.io/etcd.advertise-client-urls: https://192.168.10.150:2379
#   creationTimestamp: null
#   labels:
#     component: etcd
#     tier: control-plane
#   name: etcd
#   namespace: kube-system
# spec:
#   containers:
#   - command:
#     - etcd
#     - --advertise-client-urls=https://192.168.10.150:2379
#     - --cert-file=/etc/kubernetes/pki/etcd/server.crt
#     - --client-cert-auth=true
#     - --data-dir=/var/lib/etcd
#     - --experimental-initial-corrupt-check=true
#     - --experimental-watch-progress-notify-interval=5s
#     - --initial-advertise-peer-urls=https://192.168.10.150:2380
#     - --initial-cluster=controlplane=https://192.168.10.150:2380
#     - --key-file=/etc/kubernetes/pki/etcd/server.key
#     - --listen-client-urls=https://127.0.0.1:2379,https://192.168.10.150:2379
#     - --listen-metrics-urls=http://127.0.0.1:2381
#     - --listen-peer-urls=https://192.168.10.150:2380
#     - --name=controlplane
#     - --peer-cert-file=/etc/kubernetes/pki/etcd/peer.crt
#     - --peer-client-cert-auth=true
#     - --peer-key-file=/etc/kubernetes/pki/etcd/peer.key
#     - --peer-trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
#     - --snapshot-count=10000
#     - --trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
#     image: registry.k8s.io/etcd:3.5.24-0
#     imagePullPolicy: IfNotPresent
#     livenessProbe:
#       failureThreshold: 8
#       httpGet:
#         host: 127.0.0.1
#         path: /livez
#         port: 2381
#         scheme: HTTP
#       initialDelaySeconds: 10
#       periodSeconds: 10
#       timeoutSeconds: 15
#     name: etcd
#     readinessProbe:
#       failureThreshold: 3
#       httpGet:
#         host: 127.0.0.1
#         path: /readyz
#         port: 2381
#         scheme: HTTP
#       periodSeconds: 1
#       timeoutSeconds: 15
#     resources:
#       requests:
#         cpu: 100m
#         memory: 100Mi
#     startupProbe:
#       failureThreshold: 24
#       httpGet:
#         host: 127.0.0.1
#         path: /readyz
#         port: 2381
#         scheme: HTTP
#       initialDelaySeconds: 10
#       periodSeconds: 10
#       timeoutSeconds: 15
#     volumeMounts:
#     - mountPath: /var/lib/etcd
#       name: etcd-data
#     - mountPath: /etc/kubernetes/pki/etcd
#       name: etcd-certs
#   hostNetwork: true
#   priority: 2000001000
#   priorityClassName: system-node-critical
#   securityContext:
#     seccompProfile:
#       type: RuntimeDefault
#   volumes:
#   - hostPath:
#       path: /etc/kubernetes/pki/etcd
#       type: DirectoryOrCreate
#     name: etcd-certs
#   - hostPath:
#       path: /var/lib/etcd-backup
#       type: DirectoryOrCreate
#     name: etcd-data
# status: {}

# get etcd pod
kubectl get pod etcd-controlplane -n kube-system -o wide
# NAME                READY   STATUS    RESTARTS   AGE   IP               NODE           NOMINATED NODE   READINESS GATES
# etcd-controlplane   1/1     Running   0          26m   192.168.10.150   controlplane   <none>           <none>


kubectl describe pod etcd-controlplane -n kube-system
# Name:                 etcd-controlplane
# Namespace:            kube-system
# Priority:             2000001000
# Priority Class Name:  system-node-critical
# Node:                 controlplane/192.168.10.150
# Start Time:           Thu, 15 Jan 2026 11:45:30 -0500
# Labels:               component=etcd
#                       tier=control-plane
# Annotations:          kubeadm.kubernetes.io/etcd.advertise-client-urls: https://192.168.10.150:2379
#                       kubernetes.io/config.hash: 0b48c0e83de95a80aa45cf5e61851e21
#                       kubernetes.io/config.mirror: 0b48c0e83de95a80aa45cf5e61851e21
#                       kubernetes.io/config.seen: 2026-01-15T11:57:10.271996980-05:00
#                       kubernetes.io/config.source: file
# Status:               Running
# SeccompProfile:       RuntimeDefault
# IP:                   192.168.10.150
# IPs:
#   IP:           192.168.10.150
# Controlled By:  Node/controlplane
# Containers:
#   etcd:
#     Container ID:  containerd://b30f0033d78c452b01274dea30363c0cd252dc286a64525608a58f38aa7d4c67
#     Image:         registry.k8s.io/etcd:3.5.24-0
#     Image ID:      registry.k8s.io/etcd@sha256:251e7e490f64859d329cd963bc879dc04acf3d7195bb52c4c50b4a07bedf37d6
#     Port:          <none>
#     Host Port:     <none>
#     Command:
#       etcd
#       --advertise-client-urls=https://192.168.10.150:2379
#       --cert-file=/etc/kubernetes/pki/etcd/server.crt
#       --client-cert-auth=true
#       --data-dir=/var/lib/etcd
#       --experimental-initial-corrupt-check=true
#       --experimental-watch-progress-notify-interval=5s
#       --initial-advertise-peer-urls=https://192.168.10.150:2380
#       --initial-cluster=controlplane=https://192.168.10.150:2380
#       --key-file=/etc/kubernetes/pki/etcd/server.key
#       --listen-client-urls=https://127.0.0.1:2379,https://192.168.10.150:2379
#       --listen-metrics-urls=http://127.0.0.1:2381
#       --listen-peer-urls=https://192.168.10.150:2380
#       --name=controlplane
#       --peer-cert-file=/etc/kubernetes/pki/etcd/peer.crt
#       --peer-client-cert-auth=true
#       --peer-key-file=/etc/kubernetes/pki/etcd/peer.key
#       --peer-trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
#       --snapshot-count=10000
#       --trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
#     State:          Running
#       Started:      Thu, 15 Jan 2026 11:58:06 -0500
#     Ready:          True
#     Restart Count:  0
#     Requests:
#       cpu:        100m
#       memory:     100Mi
#     Liveness:     http-get http://127.0.0.1:2381/livez delay=10s timeout=15s period=10s #success=1 #failure=8
#     Readiness:    http-get http://127.0.0.1:2381/readyz delay=0s timeout=15s period=1s #success=1 #failure=3
#     Startup:      http-get http://127.0.0.1:2381/readyz delay=10s timeout=15s period=10s #success=1 #failure=24
#     Environment:  <none>
#     Mounts:
#       /etc/kubernetes/pki/etcd from etcd-certs (rw)
#       /var/lib/etcd from etcd-data (rw)
# Conditions:
#   Type                        Status
#   PodReadyToStartContainers   True
#   Initialized                 True
#   Ready                       True
#   ContainersReady             True
#   PodScheduled                True
# Volumes:
#   etcd-certs:
#     Type:          HostPath (bare host directory volume)
#     Path:          /etc/kubernetes/pki/etcd
#     HostPathType:  DirectoryOrCreate
#   etcd-data:
#     Type:          HostPath (bare host directory volume)
#     Path:          /var/lib/etcd-backup
#     HostPathType:  DirectoryOrCreate
# QoS Class:         Burstable
# Node-Selectors:    <none>
# Tolerations:       :NoExecute op=Exists
# Events:            <none>
```

---

## Lab: Static Pod - `schedule`

```sh
# get manifest
sudo cat /etc/kubernetes/manifests/kube-scheduler.yaml
# apiVersion: v1
# kind: Pod
# metadata:
#   creationTimestamp: null
#   labels:
#     component: kube-scheduler
#     tier: control-plane
#   name: kube-scheduler
#   namespace: kube-system
# spec:
#   containers:
#   - command:
#     - kube-scheduler
#     - --authentication-kubeconfig=/etc/kubernetes/scheduler.conf
#     - --authorization-kubeconfig=/etc/kubernetes/scheduler.conf
#     - --bind-address=127.0.0.1
#     - --kubeconfig=/etc/kubernetes/scheduler.conf
#     - --leader-elect=true
#     image: registry.k8s.io/kube-scheduler:v1.32.11
#     imagePullPolicy: IfNotPresent
#     livenessProbe:
#       failureThreshold: 8
#       httpGet:
#         host: 127.0.0.1
#         path: /livez
#         port: 10259
#         scheme: HTTPS
#       initialDelaySeconds: 10
#       periodSeconds: 10
#       timeoutSeconds: 15
#     name: kube-scheduler
#     readinessProbe:
#       failureThreshold: 3
#       httpGet:
#         host: 127.0.0.1
#         path: /readyz
#         port: 10259
#         scheme: HTTPS
#       periodSeconds: 1
#       timeoutSeconds: 15
#     resources:
#       requests:
#         cpu: 100m
#     startupProbe:
#       failureThreshold: 24
#       httpGet:
#         host: 127.0.0.1
#         path: /livez
#         port: 10259
#         scheme: HTTPS
#       initialDelaySeconds: 10
#       periodSeconds: 10
#       timeoutSeconds: 15
#     volumeMounts:
#     - mountPath: /etc/kubernetes/scheduler.conf
#       name: kubeconfig
#       readOnly: true
#   hostNetwork: true
#   priority: 2000001000
#   priorityClassName: system-node-critical
#   securityContext:
#     seccompProfile:
#       type: RuntimeDefault
#   volumes:
#   - hostPath:
#       path: /etc/kubernetes/scheduler.conf
#       type: FileOrCreate
#     name: kubeconfig
# status: {}

# get scheduler pod
kubectl get pod kube-scheduler-controlplane -n kube-system
# NAME                          READY   STATUS    RESTARTS      AGE
# kube-scheduler-controlplane   1/1     Running   6 (51m ago)   2d19h

kubectl describe pod kube-scheduler-controlplane -n kube-system
# Name:                 kube-scheduler-controlplane
# Namespace:            kube-system
# Priority:             2000001000
# Priority Class Name:  system-node-critical
# Node:                 controlplane/192.168.10.150
# Start Time:           Thu, 15 Jan 2026 15:01:33 -0500
# Labels:               component=kube-scheduler
#                       tier=control-plane
# Annotations:          kubernetes.io/config.hash: 03251309c465d6762648423f73e80586
#                       kubernetes.io/config.mirror: 03251309c465d6762648423f73e80586
#                       kubernetes.io/config.seen: 2026-01-15T15:01:33.705577525-05:00
#                       kubernetes.io/config.source: file
# Status:               Running
# SeccompProfile:       RuntimeDefault
# IP:                   192.168.10.150
# IPs:
#   IP:           192.168.10.150
# Controlled By:  Node/controlplane
# Containers:
#   kube-scheduler:
#     Container ID:  containerd://14dd66b22aed2b1ca2dad6ddbdd9d0d931c208c6b41710ad1ea32a156356734f
#     Image:         registry.k8s.io/kube-scheduler:v1.32.11
#     Image ID:      registry.k8s.io/kube-scheduler@sha256:b3039587bbe70e61a6aeaff56c21fdeeef104524a31f835bcc80887d40b8e6b2
#     Port:          <none>
#     Host Port:     <none>
#     Command:
#       kube-scheduler
#       --authentication-kubeconfig=/etc/kubernetes/scheduler.conf
#       --authorization-kubeconfig=/etc/kubernetes/scheduler.conf
#       --bind-address=127.0.0.1
#       --kubeconfig=/etc/kubernetes/scheduler.conf
#       --leader-elect=true
#     State:          Running
#       Started:      Thu, 15 Jan 2026 15:01:34 -0500
#     Ready:          True
#     Restart Count:  0
#     Requests:
#       cpu:        100m
#     Liveness:     http-get https://127.0.0.1:10259/livez delay=10s timeout=15s period=10s #success=1 #failure=8
#     Readiness:    http-get https://127.0.0.1:10259/readyz delay=0s timeout=15s period=1s #success=1 #failure=3
#     Startup:      http-get https://127.0.0.1:10259/livez delay=10s timeout=15s period=10s #success=1 #failure=24
#     Environment:  <none>
#     Mounts:
#       /etc/kubernetes/scheduler.conf from kubeconfig (ro)
# Conditions:
#   Type                        Status
#   PodReadyToStartContainers   True
#   Initialized                 True
#   Ready                       True
#   ContainersReady             True
#   PodScheduled                True
# Volumes:
#   kubeconfig:
#     Type:          HostPath (bare host directory volume)
#     Path:          /etc/kubernetes/scheduler.conf
#     HostPathType:  FileOrCreate
# QoS Class:         Burstable
# Node-Selectors:    <none>
# Tolerations:       :NoExecute op=Exists
# Events:
#   Type     Reason     Age                  From     Message
#   ----     ------     ----                 ----     -------
#   Normal   Started    55m (x3 over 3h16m)  kubelet  Started container kube-scheduler
#   Warning  Unhealthy  54m (x32 over 3h3m)  kubelet  Readiness probe failed: HTTP probe failed with statuscode: 500
#   Normal   Killing    85s                  kubelet  Stopping container kube-scheduler
#   Warning  Unhealthy  85s                  kubelet  Readiness probe failed: Get "https://127.0.0.1:10259/readyz": dial tcp 127.0.0.1:10259: connect: connection refused
#   Normal   Pulled     25s                  kubelet  Container image "registry.k8s.io/kube-scheduler:v1.32.11" already present on machine
#   Normal   Created    25s                  kubelet  Created container: kube-scheduler
#   Normal   Started    25s                  kubelet  Started container kube-scheduler
```

---

## Lab: Static Pod - `controller-manager`

```sh
# get manifest
sudo cat /etc/kubernetes/manifests/kube-controller-manager.yaml
# apiVersion: v1
# kind: Pod
# metadata:
#   creationTimestamp: null
#   labels:
#     component: kube-controller-manager
#     tier: control-plane
#   name: kube-controller-manager
#   namespace: kube-system
# spec:
#   containers:
#   - command:
#     - kube-controller-manager
#     - --allocate-node-cidrs=true
#     - --authentication-kubeconfig=/etc/kubernetes/controller-manager.conf
#     - --authorization-kubeconfig=/etc/kubernetes/controller-manager.conf
#     - --bind-address=127.0.0.1
#     - --client-ca-file=/etc/kubernetes/pki/ca.crt
#     - --cluster-cidr=10.244.0.0/16
#     - --cluster-name=kubernetes
#     - --cluster-signing-cert-file=/etc/kubernetes/pki/ca.crt
#     - --cluster-signing-key-file=/etc/kubernetes/pki/ca.key
#     - --controllers=*,bootstrapsigner,tokencleaner
#     - --kubeconfig=/etc/kubernetes/controller-manager.conf
#     - --leader-elect=true
#     - --requestheader-client-ca-file=/etc/kubernetes/pki/front-proxy-ca.crt
#     - --root-ca-file=/etc/kubernetes/pki/ca.crt
#     - --service-account-private-key-file=/etc/kubernetes/pki/sa.key
#     - --service-cluster-ip-range=10.96.0.0/12
#     - --use-service-account-credentials=true
#     image: registry.k8s.io/kube-controller-manager:v1.32.11
#     imagePullPolicy: IfNotPresent
#     livenessProbe:
#       failureThreshold: 8
#       httpGet:
#         host: 127.0.0.1
#         path: /healthz
#         port: 10257
#         scheme: HTTPS
#       initialDelaySeconds: 10
#       periodSeconds: 10
#       timeoutSeconds: 15
#     name: kube-controller-manager
#     resources:
#       requests:
#         cpu: 200m
#     startupProbe:
#       failureThreshold: 24
#       httpGet:
#         host: 127.0.0.1
#         path: /healthz
#         port: 10257
#         scheme: HTTPS
#       initialDelaySeconds: 10
#       periodSeconds: 10
#       timeoutSeconds: 15
#     volumeMounts:
#     - mountPath: /etc/ssl/certs
#       name: ca-certs
#       readOnly: true
#     - mountPath: /etc/ca-certificates
#       name: etc-ca-certificates
#       readOnly: true
#     - mountPath: /usr/libexec/kubernetes/kubelet-plugins/volume/exec
#       name: flexvolume-dir
#     - mountPath: /etc/kubernetes/pki
#       name: k8s-certs
#       readOnly: true
#     - mountPath: /etc/kubernetes/controller-manager.conf
#       name: kubeconfig
#       readOnly: true
#     - mountPath: /usr/local/share/ca-certificates
#       name: usr-local-share-ca-certificates
#       readOnly: true
#     - mountPath: /usr/share/ca-certificates
#       name: usr-share-ca-certificates
#       readOnly: true
#   hostNetwork: true
#   priority: 2000001000
#   priorityClassName: system-node-critical
#   securityContext:
#     seccompProfile:
#       type: RuntimeDefault
#   volumes:
#   - hostPath:
#       path: /etc/ssl/certs
#       type: DirectoryOrCreate
#     name: ca-certs
#   - hostPath:
#       path: /etc/ca-certificates
#       type: DirectoryOrCreate
#     name: etc-ca-certificates
#   - hostPath:
#       path: /usr/libexec/kubernetes/kubelet-plugins/volume/exec
#       type: DirectoryOrCreate
#     name: flexvolume-dir
#   - hostPath:
#       path: /etc/kubernetes/pki
#       type: DirectoryOrCreate
#     name: k8s-certs
#   - hostPath:
#       path: /etc/kubernetes/controller-manager.conf
#       type: FileOrCreate
#     name: kubeconfig
#   - hostPath:
#       path: /usr/local/share/ca-certificates
#       type: DirectoryOrCreate
#     name: usr-local-share-ca-certificates
#   - hostPath:
#       path: /usr/share/ca-certificates
#       type: DirectoryOrCreate
#     name: usr-share-ca-certificates
# status: {}

# get controler manager pod
kubectl get pod  -n kube-system
# NAME                          READY   STATUS    RESTARTS      AGE
# kube-scheduler-controlplane   1/1     Running   6 (51m ago)   2d19h

# get controler manager
kubectl get pod kube-controller-manager-controlplane -n kube-system
# NAME                                   READY   STATUS    RESTARTS      AGE
# kube-controller-manager-controlplane   1/1     Running   6 (72m ago)   2d20h

kubectl describe pod kube-controller-manager-controlplane -n kube-system
# Name:                 kube-controller-manager-controlplane
# Namespace:            kube-system
# Priority:             2000001000
# Priority Class Name:  system-node-critical
# Node:                 controlplane/192.168.10.150
# Start Time:           Thu, 15 Jan 2026 14:59:44 -0500
# Labels:               component=kube-controller-manager
#                       tier=control-plane
# Annotations:          kubernetes.io/config.hash: 7940e8f3985459b0e0d57875b666666d
#                       kubernetes.io/config.mirror: 7940e8f3985459b0e0d57875b666666d
#                       kubernetes.io/config.seen: 2026-01-12T19:08:51.371591006-05:00
#                       kubernetes.io/config.source: file
# Status:               Running
# SeccompProfile:       RuntimeDefault
# IP:                   192.168.10.150
# IPs:
#   IP:           192.168.10.150
# Controlled By:  Node/controlplane
# Containers:
#   kube-controller-manager:
#     Container ID:  containerd://e4a03966937b79744de6defb325113fc2e5066c02c9fbd820a8d633c8c8913bf
#     Image:         registry.k8s.io/kube-controller-manager:v1.32.11
#     Image ID:      registry.k8s.io/kube-controller-manager@sha256:ce7b2ead5eef1a1554ef28b2b79596c6a8c6d506a87a7ab1381e77fe3d72f55f
#     Port:          <none>
#     Host Port:     <none>
#     Command:
#       kube-controller-manager
#       --allocate-node-cidrs=true
#       --authentication-kubeconfig=/etc/kubernetes/controller-manager.conf
#       --authorization-kubeconfig=/etc/kubernetes/controller-manager.conf
#       --bind-address=127.0.0.1
#       --client-ca-file=/etc/kubernetes/pki/ca.crt
#       --cluster-cidr=10.244.0.0/16
#       --cluster-name=kubernetes
#       --cluster-signing-cert-file=/etc/kubernetes/pki/ca.crt
#       --cluster-signing-key-file=/etc/kubernetes/pki/ca.key
#       --controllers=*,bootstrapsigner,tokencleaner
#       --kubeconfig=/etc/kubernetes/controller-manager.conf
#       --leader-elect=true
#       --requestheader-client-ca-file=/etc/kubernetes/pki/front-proxy-ca.crt
#       --root-ca-file=/etc/kubernetes/pki/ca.crt
#       --service-account-private-key-file=/etc/kubernetes/pki/sa.key
#       --service-cluster-ip-range=10.96.0.0/12
#       --use-service-account-credentials=true
#     State:          Running
#       Started:      Thu, 15 Jan 2026 14:06:45 -0500
#     Last State:     Terminated
#       Reason:       Error
#       Exit Code:    1
#       Started:      Thu, 15 Jan 2026 11:57:32 -0500
#       Finished:     Thu, 15 Jan 2026 14:06:44 -0500
#     Ready:          True
#     Restart Count:  6
#     Requests:
#       cpu:        200m
#     Liveness:     http-get https://127.0.0.1:10257/healthz delay=10s timeout=15s period=10s #success=1 #failure=8
#     Startup:      http-get https://127.0.0.1:10257/healthz delay=10s timeout=15s period=10s #success=1 #failure=24
#     Environment:  <none>
#     Mounts:
#       /etc/ca-certificates from etc-ca-certificates (ro)
#       /etc/kubernetes/controller-manager.conf from kubeconfig (ro)
#       /etc/kubernetes/pki from k8s-certs (ro)
#       /etc/ssl/certs from ca-certs (ro)
#       /usr/libexec/kubernetes/kubelet-plugins/volume/exec from flexvolume-dir (rw)
#       /usr/local/share/ca-certificates from usr-local-share-ca-certificates (ro)
#       /usr/share/ca-certificates from usr-share-ca-certificates (ro)
# Conditions:
#   Type                        Status
#   PodReadyToStartContainers   True
#   Initialized                 True
#   Ready                       True
#   ContainersReady             True
#   PodScheduled                True
# Volumes:
#   ca-certs:
#     Type:          HostPath (bare host directory volume)
#     Path:          /etc/ssl/certs
#     HostPathType:  DirectoryOrCreate
#   etc-ca-certificates:
#     Type:          HostPath (bare host directory volume)
#     Path:          /etc/ca-certificates
#     HostPathType:  DirectoryOrCreate
#   flexvolume-dir:
#     Type:          HostPath (bare host directory volume)
#     Path:          /usr/libexec/kubernetes/kubelet-plugins/volume/exec
#     HostPathType:  DirectoryOrCreate
#   k8s-certs:
#     Type:          HostPath (bare host directory volume)
#     Path:          /etc/kubernetes/pki
#     HostPathType:  DirectoryOrCreate
#   kubeconfig:
#     Type:          HostPath (bare host directory volume)
#     Path:          /etc/kubernetes/controller-manager.conf
#     HostPathType:  FileOrCreate
#   usr-local-share-ca-certificates:
#     Type:          HostPath (bare host directory volume)
#     Path:          /usr/local/share/ca-certificates
#     HostPathType:  DirectoryOrCreate
#   usr-share-ca-certificates:
#     Type:          HostPath (bare host directory volume)
#     Path:          /usr/share/ca-certificates
#     HostPathType:  DirectoryOrCreate
# QoS Class:         Burstable
# Node-Selectors:    <none>
# Tolerations:       :NoExecute op=Exists
# Events:
#   Type    Reason   Age                  From     Message
#   ----    ------   ----                 ----     -------
#   Normal  Started  72m (x3 over 3h33m)  kubelet  Started container kube-controller-manager
```
