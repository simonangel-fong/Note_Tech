# CKA

[Back](../index.md)

- [CKA](#cka)
  - [权限控制 RBAC](#权限控制-rbac)
  - [查看 pod 的 CPU](#查看-pod-的-cpu)
  - [配置网络策略 NetworkPolicy](#配置网络策略-networkpolicy)
  - [4、暴露服务 service](#4暴露服务-service)
  - [5、创建 Ingress](#5创建-ingress)
  - [6、扩容 deployment 副本数量](#6扩容-deployment-副本数量)
  - [7、调度 pod 到指定节点](#7调度-pod-到指定节点)
  - [8 查看可用节点数量](#8-查看可用节点数量)
  - [9 创建多容器的 pod](#9-创建多容器的-pod)
  - [10.创建 PV](#10创建-pv)
  - [11.创建 PVC](#11创建-pvc)
  - [12.查看 pod 日志](#12查看-pod-日志)
  - [13. 使用 sidecar 代理容器日志](#13-使用-sidecar-代理容器日志)
  - [14.升级集群](#14升级集群)
  - [15.备份还原 etcd](#15备份还原-etcd)
  - [16. 排查集群中故障节点](#16-排查集群中故障节点)
  - [17.节点维护](#17节点维护)

---

## 权限控制 RBAC

设置配置环境：
[candidate@node-1] $ kubectl config use-context k8s

Context
为部署流水线创建一个新的 ClusterRole 并将其绑定到范围为特定的 namespace 的特定 ServiceAccount。

Task
创建一个名为 deployment-clusterrole 且仅允许创建以下资源类型的新 ClusterRole：
Deployment
StatefulSet
DaemonSet
在现有的 namespace app-team1 中创建一个名为 cicd-token 的新 ServiceAccount。
限于 namespace app-team1 中，将新的 ClusterRole deployment-clusterrole 绑定到新的 ServiceAccount cicd-token。Copy

---

```sh
# create cluster role
kubectl create clusterrole deployment-clusterrole --resource=deployment,statefulsets,daemonsets --verb=create

# create sa
kubectl create sa cicd-token -n app-team1

# cluster role binding
kubectl create rolebinding cicd-token-rolebinding --clusterrole=deployment-clusterrole --serviceaccount=cicd-token -n app-team1

# confirm
kubectl -n app-team1 describe rolebinding cicd-token-rolebinding

```

---

## 查看 pod 的 CPU

设置配置环境：
[candidate@node-1] $ kubectl config use-context k8s

Task
通过 pod label name=cpu-loader，找到运行时占用大量 CPU 的 pod，
并将占用 CPU 最高的 pod 名称写入文件 /opt/KUTR000401/KUTR00401.txt（已存在）。Copy

```sh
kubectl top pod -l name=cpu-loader --sort-by=cpu -A
```

---

## 配置网络策略 NetworkPolicy

设置配置环境：
[candidate@node-1] $ kubectl config use-context hk8s

Task
在现有的 namespace my-app 中创建一个名为 allow-port-from-namespace 的新 NetworkPolicy。
确保新的 NetworkPolicy 允许 namespace echo 中的 Pods 连接到 namespace my-app 中的 Pods 的 9000 端口。

进一步确保新的 NetworkPolicy：
不允许对没有在监听 端口 9000 的 Pods 的访问
不允许非来自 namespace echo 中的 Pods 的访问

```sh
# env
kubectl create ns my-app

```

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-port-from-namespace
  namespace: my-app
spec:
  podSelector: {} # all pod in the ns
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector: # ns
            matchLabels:
              kubernetes.io/metadata.name: echo # use ns name
      ports:
        - protocol: TCP
          port: 9000 # port
```

---

## 4、暴露服务 service

- Question
  设置配置环境：
  [candidate@node-1] $ kubectl config use-context k8s

Task
请重新配置现有的 deployment front-end 以及添加名为 http 的端口规范来公开现有容器 nginx 的端口 80/tcp。
创建一个名为 front-end-svc 的新 service，以公开容器端口 http。
配置此 service，以通过各个 Pod 所在的节点上的 NodePort 来公开他们。Copy

---

- prepare environment

```sh
kubectl create deploy front-end --image=nginx --port=80 --replicas=5
kubectl rollout status deploy/front-end
# deployment "front-end" successfully rolled out
```

- Answer

```sh
# ##############################
# Collect info
# ##############################
kubectl get deploy front-end
kubectl get deploy front-end -o yaml

# ##############################
# Solution: update deployment
# ##############################
# output the manifest
kubectl get deploy front-end -o yaml > app.yaml
#         ports:
#         - containerPort: 80
#           protocol: TCP

# update manifest
vi app.yaml
#         ports:
#         - containerPort: 80
#           name: http
#           protocol: TCP

# replace with manifest
kubectl replace --force -f app.yaml

# confirm rollout
kubectl rollout status deploy/front-end
# confirm config
kubectl get deploy front-end -o yaml
#         ports:
#         - containerPort: 80
#           name: http
#           protocol: TCP

# ##############################
# Solution: Create svc
# ##############################
kubectl expose deploy front-end --name=front-end-svc --type=NodePort --port=80 --target-port=80
# service/front-end-svc exposed

# check endpoint ip = pod ip
kubectl describe svc front-end-svc | grep -i endpoints
# Endpoints:                10.244.2.79:80,10.244.1.99:80,10.244.1.97:80

kubectl get pod -o custom-columns=Name:metadata.name,IP:status.podIP
# Name                         IP
# front-end-7c6b5dd47c-gtpzs   10.244.2.79
# front-end-7c6b5dd47c-gw9dc   10.244.1.97
# front-end-7c6b5dd47c-k4k4c   10.244.1.99
# front-end-7c6b5dd47c-n2msr   10.244.1.98
# front-end-7c6b5dd47c-rsq7l   10.244.2.80
```

---

## 5、创建 Ingress

设置配置环境：
[candidate@node-1] $ kubectl config use-context k8s

Task
如下创建一个新的 nginx Ingress 资源：
名称: ping
Namespace: ing-internal
使用服务端口 5678 在路径 /hello 上公开服务 hello

可以使用以下命令检查服务 hello 的可用性，该命令应返回 hello：
curl -kL <INTERNAL_IP>/helloCopy

---

- Env config

```sh
kubectl create ns ing-internal
# namespace/ing-internal created
kubectl get ns ing-internal
# NAME           STATUS   AGE
# ing-internal   Active   3m12s

kubectl create deploy hello -n ing-internal --image=nginx --port=80
# deployment.apps/hello created
kubectl expose deploy hello -n ing-internal --name=hello --port=8080 --target-port=80
# service/hello exposed

# confirm
kubectl run env-test -n ing-internal --rm -it --image=curlimages/curl --restart=Never -- curl -s http://hello:8080
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
# pod "env-test" deleted
```

- Solution

```sh
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
#       - backend:
#           service:
#             name: hello
#             port:
#               number: 8080
#         path: /hello
#         pathType: Prefix

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

## 6、扩容 deployment 副本数量

设置配置环境：
[candidate@node-1] $ kubectl config use-context k8s

Task
将 deployment presentation 扩展至 4 个 podsCopy

---

- Configure Exam Environment

```sh
kubectl create deploy presentation --image=nginx
# deployment.apps/presentation created

# confirm
kubectl get deploy presentation
# NAME           READY   UP-TO-DATE   AVAILABLE   AGE
# presentation   1/1     1            1           10s
```

- Solution

```sh
kubectl scale deploy presentation --replicas=4
# deployment.apps/presentation scaled

# confirm
kubectl rollout status deploy presentation
# deployment "presentation" successfully rolled out
kubectl get deploy presentation -o wide
# NAME           READY   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS   IMAGES   SELECTOR
# presentation   4/4     4            4           3m54s   nginx        nginx    app=presentation
```

---

## 7、调度 pod 到指定节点

设置配置环境：
[candidate@node-1] $ kubectl config use-context k8s

Task
按如下要求调度一个 pod：
名称：nginx-kusc00401
Image：nginx
Node selector：disktype=ssd

---

- Solution

```sh
# ##############################
# Collect Info
# ##############################
kubectl get node --show-labels
# NAME           STATUS   ROLES           AGE   VERSION   LABELS
# controlplane   Ready    control-plane   42d   v1.33.6   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=controlplane,kubernetes.io/os=linux,node-role.kubernetes.io/control-plane=,node.kubernetes.io/exclude-from-external-load-balancers=
# node01         Ready    <none>          42d   v1.33.6   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=node01,kubernetes.io/os=linux
# node02         Ready    <none>          42d   v1.33.6   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,disk=ssd,kubernetes.io/arch=amd64,kubernetes.io/hostname=node02,kubernetes.io/os=linux,node-role=front-end,ssd=

# add node label
kubectl label node node02 disktype=ssd
# node/node02 labeled

# confirm
kubectl get node -l disktype=ssd
# NAME     STATUS   ROLES    AGE   VERSION
# node02   Ready    <none>   42d   v1.33.6

kubectl run nginx-kusc00401 --image=nginx --dry-run=client -o yaml > nodeSelector-pod.yaml

vi nodeSelector-pod.yaml
# apiVersion: v1
# kind: Pod
# metadata:
#   name: nginx-kusc00401
# spec:
#   nodeSelector:
#     disktype: ssd
#   containers:
#   - name: nginx
#     image: nginx

# create pod
kubectl apply -f nodeSelector-pod.yaml
# pod/nginx-kusc00401 created

# confirm
kubectl get pod nginx-kusc00401 -o wide
# NAME              READY   STATUS    RESTARTS   AGE   IP            NODE     NOMINATED NODE   READINESS GATES
# nginx-kusc00401   1/1     Running   0          81s   10.244.2.85   node02   <none>           <none>
```

---

## 8 查看可用节点数量

设置配置环境：
[candidate@node-1] $ kubectl config use-context k8s

Task
检查有多少 nodes 已准备就绪（不包括被打上 Taint：NoSchedule 的节点），
并将数量写入 /opt/KUSC00402/kusc00402.txtCopy

---

- Configure Environment

```sh
kubectl taint node node01 app=db:NoSchedule
# node/node01 tainted

# confirm
kubectl describe node node01 | grep Taints
# Taints:             app=db:NoSchedule
```

- Solution

```sh
kubectl describe node | grep Taints
# Taints:             node-role.kubernetes.io/control-plane:NoSchedule
# Taints:             app=db:NoSchedule
# Taints:             <none>

kubectl describe node | grep Taints | grep -vc NoSchedule > /opt/KUSC00402/kusc00402.txt
# 1

# confirm
cat /opt/KUSC00402/kusc00402.txt
```

---

## 9 创建多容器的 pod

设置配置环境：
[candidate@node-1] $ kubectl config use-context k8s

Task
按如下要求调度一个 Pod：
名称：kucc8
app containers: 2
container 名称/images：

- nginx
- redis

---

- Solution:

```sh
kubectl run kucc8 --image=nginx --dry-run=client -o yaml > multi-con.yaml

vi multi-con.yaml
# apiVersion: v1
# kind: Pod
# metadata:
#   name: kucc8
# spec:
#   containers:
#   - name: nginx
#     image: nginx
#   - name: redis
#     image: redis

kubectl apply -f multi-con.yaml
# pod/kucc8 created

# confirm
kubectl get pod kucc8
```

---

## 10.创建 PV

设置配置环境：
[candidate@node-1] $ kubectl config use-context hk8s

Task
创建名为 app-config 的 persistent volume，容量为 1Gi，访问模式为 ReadWriteMany。
volume 类型为 hostPath，位于 /srv/app-config

---

```yaml
# pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: app-config
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteMany
  hostPath:
    path: "/srv/app-config"
```

```sh
kubectl apply -f pv.yaml
# persistentvolume/app-config created

kubectl get pv app-config
# NAME         CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM   STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
# app-config   1Gi        RWX            Retain           Available                          <unset>                          27s

kubectl describe pv app-config
# Name:            app-config
# Labels:          <none>
# Annotations:     <none>
# Finalizers:      [kubernetes.io/pv-protection]
# StorageClass:
# Status:          Available
# Claim:
# Reclaim Policy:  Retain
# Access Modes:    RWX
# VolumeMode:      Filesystem
# Capacity:        1Gi
# Node Affinity:   <none>
# Message:
# Source:
#     Type:          HostPath (bare host directory volume)
#     Path:          /srv/app-configCopy
#     HostPathType:
# Events:            <none>
```

---

## 11.创建 PVC

设置配置环境：
[candidate@node-1] $ kubectl config use-context ok8s

Task
创建一个新的 PersistentVolumeClaim：
名称: pv-volume
Class: csi-hostpath-sc
容量: 10Mi

创建一个新的 Pod，来将 PersistentVolumeClaim 作为 volume 进行挂载：
名称：web-server
Image：nginx:1.16
挂载路径：/usr/share/nginx/html

配置新的 Pod，以对 volume 具有 ReadWriteOnce 权限。

最后，使用 kubectl edit 或 kubectl patch 将 PersistentVolumeClaim 的容量扩展为 70Mi，并记录此更改。

---

- Solution

```yaml
# pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pv-volume
spec:
  storageClassName: csi-hostpath-sc
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Mi
```

```sh
kubectl apply -f pvc.yaml
# persistentvolumeclaim/pv-volume created

kubectl get pvc
# NAME                 STATUS    VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS      VOLUMEATTRIBUTESCLASS   AGE
# pv-volume            Bound     pvc-20bb7ba7-c811-47c6-85fb-13881c9af538   10Mi       RWO            csi-hostpath-sc   <unset>                 4m
```

```yaml
# pvc-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-server
spec:
  volumes:
    - name: pv-storage
      persistentVolumeClaim:
        claimName: pv-volume
  containers:
    - name: nginx
      image: nginx:1.16
      volumeMounts:
        - mountPath: "/usr/share/nginx/html"
          name: pv-storage
```

```sh
kubectl apply -f pvc-pod.yaml
# pod/web-server created

kubectl get pod web-server
# NAME         READY   STATUS    RESTARTS   AGE
# web-server   1/1     Running   0          24s

kubectl describe pod web-server
# Containers:
#   nginx:
#     Mounts:
#       /usr/share/nginx/html from pv-storage (rw)
# Volumes:
#   pv-storage:
#     Type:       PersistentVolumeClaim (a reference to a PersistentVolumeClaim in the same namespace)
#     ClaimName:  pv-volume
```

- update

```sh
kubectl edit pvc pv-volume --record
# spec:
#   resources:
#     requests:
#       storage: 70Mi
# persistentvolumeclaim/pv-volume edited

# confirm
kubectl get pvc pv-volume
# NAME        STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS      VOLUMEATTRIBUTESCLASS   AGE
# pv-volume   Bound    pvc-20bb7ba7-c811-47c6-85fb-13881c9af538   70Mi       RWO            csi-hostpath-sc   <unset>                 12m

kubectl describe pvc pv-volume
# Capacity:      70Mi
# Events:
#   Type     Reason                    Age                    From                                                                           Message
#   ----     ------                    ----                   ----                                                                           -------
#   Normal   Resizing                  26s                    external-resizer hostpath.csi.k8s.io                                           External resizer is resizing volume pvc-20bb7ba7-c811-47c6-85fb-13881c9af538
#   Normal   FileSystemResizeRequired  25s                    external-resizer hostpath.csi.k8s.io                                           Require file system resize of volume on node
```

---

## 12.查看 pod 日志

设置配置环境：
[candidate@node-1] $ kubectl config use-context k8s

Task
监控 pod foo 的日志并：
提取与错误 RLIMIT_NOFILE 相对应的日志行
将这些日志行写入 /opt/KUTR00101/foo

---

- Config env

```sh
kubectl run foo --image=busybox -- sleep infinity
# pod/foo created

kubectl exec -it foo -- ulimit -n
```

- Solution

```sh
kubectl logs foo | grep "RLIMIT_NOFILE" > /opt/KUTR00101/foo
```

---

## 13. 使用 sidecar 代理容器日志

设置配置环境：
[candidate@node-1] $ kubectl config use-context k8s

Context
将一个现有的 Pod 集成到 Kubernetes 的内置日志记录体系结构中（例如 kubectl logs）。
添加 streaming sidecar 容器是实现此要求的一种好方法。

Task
使用 busybox Image 来将名为 sidecar 的 sidecar 容器添加到现有的 Pod 11-factor-app 中。
新的 sidecar 容器必须运行以下命令：
/bin/sh -c tail -n+1 -f /var/log/11-factor-app.log
使用挂载在/var/log 的 Volume，使日志文件 11-factor-app.log 可用于 sidecar 容器。
除了添加所需要的 volume mount 以外，请勿更改现有容器的规格。

---

- Config env

```yaml
# 11-factor-app.yaml
apiVersion: v1
kind: Pod
metadata:
  name: 11-factor-app
spec:
  containers:
    - name: count
      image: busybox
      command:
        - "/bin/sh"
        - "-c"
      args:
        - |
          i=0;
          while true;
          do
           echo "$i: $(date)" >> /var/log/11-factor-app.log;
           i=$((i+1));
           sleep 1;
          done
```

```sh
kubectl apply -f 11-factor-app.yaml
# pod/11-factor-app created

kubectl get pod
# NAME                   READY   STATUS    RESTARTS      AGE
# 11-factor-app          1/1     Running   0             3m54s

kubectl exec -it 11-factor-app -- cat /var/log/11-factor-app.log
# 0: Thu Jan  8 20:45:44 UTC 2026
# 1: Thu Jan  8 20:45:45 UTC 2026
# 2: Thu Jan  8 20:45:46 UTC 2026
# 3: Thu Jan  8 20:45:47 UTC 2026
# 4: Thu Jan  8 20:45:49 UTC 2026
```

```sh
kubectl get pod 11-factor-app -o yaml > sidecar.yaml

# backup
cp sidecar.yaml sidecar.yaml.bak
vi sidecar.yaml
```

```yaml
# sidecar.yaml
apiVersion: v1
kind: Pod
metadata:
  name: 11-factor-app
spec:
  volumes:
    - name: varlog
      emptyDir: {}
  containers:
    - name: count
      image: busybox
      volumeMounts:
        - name: varlog
          mountPath: /var/log
      command:
        - "/bin/sh"
        - "-c"
      args:
        - |
          i=0;
          while true;
          do
           echo "$i: $(date)" >> /var/log/11-factor-app.log;
           i=$((i+1));
           sleep 1;
          done
    - name: sidecar
      image: busybox
      volumeMounts:
        - name: varlog
          mountPath: /var/log
      command:
        - "/bin/sh"
        - "-c"
      args:
        - |
          tail -n+1 -f /var/log/11-factor-app.log
```

```sh
kubectl delete pod 11-factor-app --grace-period=1
# pod "11-factor-app" deleted

kubectl apply -f sidecar.yaml
# pod/11-factor-app replaced

kubectl get pod 11-factor-app
# NAME            READY   STATUS    RESTARTS   AGE
# 11-factor-app   2/2     Running   0          17s

# confirm
kubectl logs 11-factor-app -c sidecar
# 0: Thu Jan  8 20:53:07 UTC 2026
# 1: Thu Jan  8 20:53:09 UTC 2026
# 2: Thu Jan  8 20:53:10 UTC 2026
# 3: Thu Jan  8 20:53:11 UTC 2026
# 4: Thu Jan  8 20:53:12 UTC 2026
# 5: Thu Jan  8 20:53:13 UTC 2026
# 6: Thu Jan  8 20:53:14 UTC 2026
# 7: Thu Jan  8 20:53:15 UTC 2026
# 8: Thu Jan  8 20:53:16 UTC 2026

```

---

## 14.升级集群

设置配置环境：
[candidate@node-1] $ kubectl config use-context mk8s

Task
现有的 Kubernetes 集群正在运行版本 1.24.2。仅将 master 节点上的所有 Kubernetes 控制平面和节点组件升级到版本 1.24.3。

确保在升级之前 drain master 节点，并在升级后 uncordon master 节点。

可以使用以下命令，通过 ssh 连接到 master 节点：
ssh master01
可以使用以下命令，在该 master 节点上获取更高权限：
sudo -i

另外，在主节点上升级 kubelet 和 kubectl。
请不要升级工作节点，etcd，container 管理器，CNI 插件， DNS 服务或任何其他插件。Copy

---

- Preparation

```sh
# get current version
kubectl version
# Client Version: v1.33.6
# Kustomize Version: v5.6.0
# Server Version: v1.33.6

# kubeadm version
kubeadm version
# kubeadm version: &version.Info{Major:"1", Minor:"33", EmulationMajor:"", EmulationMinor:"", MinCompatibilityMajor:"", MinCompatibilityMinor:"", GitVersion:"v1.33.6", GitCommit:"1e09fec02ac194c1044224e45e60d249e98cd092", GitTreeState:"clean", BuildDate:"2025-11-11T19:13:44Z", GoVersion:"go1.24.9", Compiler:"gc", Platform:"linux/amd64"}

# get nodes
kubectl get node
# NAME           STATUS   ROLES           AGE   VERSION
# controlplane   Ready    control-plane   44d   v1.33.6
# node01         Ready    <none>          43d   v1.33.6
# node02         Ready    <none>          43d   v1.33.6

# drain master
kubectl drain controlplane --ignore-daemonsets --delete-emptydir-data
# node/controlplane already cordoned
# Warning: ignoring DaemonSet-managed Pods: kube-flannel/kube-flannel-ds-vjfmq, kube-system/kube-proxy-8rr2r
# evicting pod kube-system/coredns-674b8bbfcf-4chqx
# evicting pod kube-system/coredns-674b8bbfcf-tx5xf
# pod/coredns-674b8bbfcf-tx5xf evicted
# pod/coredns-674b8bbfcf-4chqx evicted
# node/controlplane drained

kubectl describe node controlplane | grep Unschedulable
# Unschedulable:      true
```

- Upgrading control plane nodes

```sh
# Find the latest patch release
sudo apt update
apt-cache madison kubeadm
#  kubeadm | 1.34.3-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
#  kubeadm | 1.34.2-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
#  kubeadm | 1.34.1-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
#  kubeadm | 1.34.0-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages

# Upgrade kubeadm: replace version
sudo apt-mark unhold kubeadm && \
sudo apt-get update && sudo apt-get install -y kubeadm='1.34.3-1.1' && \
sudo apt-mark hold kubeadm

# confirm
kubeadm version
# kubeadm version: &version.Info{Major:"1", Minor:"34", EmulationMajor:"", EmulationMinor:"", MinCompatibilityMajor:"", MinCompatibilityMinor:"", GitVersion:"v1.34.3", GitCommit:"df11db1c0f08fab3c0baee1e5ce6efbf816af7f1", GitTreeState:"clean", BuildDate:"2025-12-09T15:05:15Z", GoVersion:"go1.24.11", Compiler:"gc", Platform:"linux/amd64"}


# Verify the upgrade plan
sudo kubeadm upgrade plan
# [preflight] Running pre-flight checks.
# [upgrade/config] Reading configuration from the "kubeadm-config" ConfigMap in namespace "kube-system"...
# [upgrade/config] Use 'kubeadm init phase upload-config kubeadm --config your-config-file' to re-upload it.
# [upgrade] Running cluster health checks
# [upgrade] Fetching available versions to upgrade to
# [upgrade/versions] Cluster version: 1.33.6
# [upgrade/versions] kubeadm version: v1.34.3
# I0108 20:37:17.267120  133354 version.go:260] remote version is much newer: v1.35.0; falling back to: stable-1.34
# [upgrade/versions] Target version: v1.34.3
# [upgrade/versions] Latest version in the v1.33 series: v1.33.7

# Components that must be upgraded manually after you have upgraded the control plane with 'kubeadm upgrade apply':
# COMPONENT   NODE           CURRENT   TARGET
# kubelet     controlplane   v1.33.6   v1.33.7
# kubelet     node01         v1.33.6   v1.33.7
# kubelet     node02         v1.33.6   v1.33.7

# Upgrade to the latest version in the v1.33 series:

# COMPONENT                 NODE           CURRENT    TARGET
# kube-apiserver            controlplane   v1.33.6    v1.33.7
# kube-controller-manager   controlplane   v1.33.6    v1.33.7
# kube-scheduler            controlplane   v1.33.6    v1.33.7
# kube-proxy                               1.33.6     v1.33.7
# CoreDNS                                  v1.12.0    v1.12.1
# etcd                      controlplane   3.5.24-0   3.5.24-0

# You can now apply the upgrade by executing the following command:

#         kubeadm upgrade apply v1.33.7

# _____________________________________________________________________

# Components that must be upgraded manually after you have upgraded the control plane with 'kubeadm upgrade apply':
# COMPONENT   NODE           CURRENT   TARGET
# kubelet     controlplane   v1.33.6   v1.34.3
# kubelet     node01         v1.33.6   v1.34.3
# kubelet     node02         v1.33.6   v1.34.3

# Upgrade to the latest stable version:

# COMPONENT                 NODE           CURRENT    TARGET
# kube-apiserver            controlplane   v1.33.6    v1.34.3
# kube-controller-manager   controlplane   v1.33.6    v1.34.3
# kube-scheduler            controlplane   v1.33.6    v1.34.3
# kube-proxy                               1.33.6     v1.34.3
# CoreDNS                                  v1.12.0    v1.12.1
# etcd                      controlplane   3.5.24-0   3.6.5-0

# You can now apply the upgrade by executing the following command:

#         kubeadm upgrade apply v1.34.3

# _____________________________________________________________________


# The table below shows the current state of component configs as understood by this version of kubeadm.
# Configs that have a "yes" mark in the "MANUAL UPGRADE REQUIRED" column require manual config upgrade or
# resetting to kubeadm defaults before a successful upgrade can be performed. The version to manually
# upgrade to is denoted in the "PREFERRED VERSION" column.

# API GROUP                 CURRENT VERSION   PREFERRED VERSION   MANUAL UPGRADE REQUIRED
# kubeproxy.config.k8s.io   v1alpha1          v1alpha1            no
# kubelet.config.k8s.io     v1beta1           v1beta1             no
# _____________________________________________________________________


# upgrade
sudo kubeadm upgrade apply v1.34.3
# [upgrade] SUCCESS! A control plane node of your cluster was upgraded to "v1.34.3".
# [upgrade] Now please proceed with upgrading the rest of the nodes by following the right order.

# confirm: server version
kubectl version
# Client Version: v1.33.6
# Kustomize Version: v5.6.0
# Server Version: v1.34.3

```

- upgrade kubelet 和 kubectl

```sh
kubectl drain controlplane --ignore-daemonsets
# node/controlplane cordoned
# Warning: ignoring DaemonSet-managed Pods: kube-flannel/kube-flannel-ds-vjfmq, kube-system/kube-proxy-mlgw2
# node/controlplane drained

# confirm
kubectl describe node controlplane | grep Unschedulable
# Unschedulable:      true

sudo apt-cache madison kubelet
# kubelet | 1.34.3-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
# kubelet | 1.34.2-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
# kubelet | 1.34.1-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
# kubelet | 1.34.0-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages

apt-cache madison kubectl
# kubectl | 1.34.3-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
# kubectl | 1.34.2-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
# kubectl | 1.34.1-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages
# kubectl | 1.34.0-1.1 | https://pkgs.k8s.io/core:/stable:/v1.34/deb  Packages


# Upgrade the kubelet and kubectl
sudo apt-mark unhold kubelet kubectl && \
sudo apt-get update && sudo apt-get install -y kubelet='1.34.3-1.1' kubectl='1.34.3-1.1' && \
sudo apt-mark hold kubelet kubectl

# Restart the kubelet:
sudo systemctl daemon-reload
sudo systemctl restart kubelet

# Uncordon the node
kubectl uncordon controlplane
# node/controlplane uncordoned

# confirm
kubectl describe node controlplane | grep Unschedulable
# Unschedulable:      false

# confirm
kubectl version
# Client Version: v1.34.3
# Kustomize Version: v5.7.1
# Server Version: v1.34.3

kubectl get nodes
# NAME           STATUS   ROLES           AGE   VERSION
# controlplane   Ready    control-plane   44d   v1.34.3
# node01         Ready    <none>          44d   v1.33.6
# node02         Ready    <none>          43d   v1.33.6
```

---

## 15.备份还原 etcd

设置配置环境
此项目无需更改配置环境。但是，在执行此项目之前，请确保您已返回初始节点。
[candidate@master01] $ exit #注意，这个之前是在 master01 上，所以要 exit 退到 node01，如果已经是 node01 了，就不要再 exit 了。

Task
首先，为运行在 https://11.0.1.111:2379 上的现有 etcd 实例创建快照并将快照保存到 /var/lib/backup/etcd-snapshot.db
（注意，真实考试中，这里写的是 https://127.0.0.1:2379）
为给定实例创建快照预计能在几秒钟内完成。 如果该操作似乎挂起，则命令可能有问题。用 CTRL + C 来取消操作，然后重试。

然后还原位于/data/backup/etcd-snapshot-previous.db 的现有先前快照。
提供了以下 TLS 证书和密钥，以通过 etcdctl 连接到服务器。

CA 证书: /opt/KUIN00601/ca.crt
客户端证书: /opt/KUIN00601/etcd-client.crt
客户端密钥: /opt/KUIN00601/etcd-client.keyCopy

---

- ref:

- Backup

```sh
sudo mkdir -pv /var/lib/backup/
# mkdir: created directory '/var/lib/backup/'

export ETCDCTL_API=3

sudo -i ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key snapshot save /var/lib/backup/etcd-snapshot.db
# {"level":"info","ts":1767926465.3337407,"caller":"snapshot/v3_snapshot.go:119","msg":"created temporary db file","path":"/var/lib/backup/etcd-snapshot.db.part"}
# {"level":"info","ts":"2026-01-08T21:41:05.351464-0500","caller":"clientv3/maintenance.go:212","msg":"opened snapshot stream; downloading"}
# {"level":"info","ts":1767926465.3517191,"caller":"snapshot/v3_snapshot.go:127","msg":"fetching snapshot","endpoint":"https://127.0.0.1:2379"}
# {"level":"info","ts":"2026-01-08T21:41:05.790886-0500","caller":"clientv3/maintenance.go:220","msg":"completed snapshot read; closing"}
# {"level":"info","ts":1767926465.8104656,"caller":"snapshot/v3_snapshot.go:142","msg":"fetched snapshot","endpoint":"https://127.0.0.1:2379","size":"8.7 MB","took":0.471495617}
# {"level":"info","ts":1767926465.8106403,"caller":"snapshot/v3_snapshot.go:152","msg":"saved","path":"/var/lib/backup/etcd-snapshot.db"}
# Snapshot saved at /var/lib/backup/etcd-snapshot.db

# Verify the snapshot:
sudo -i ETCDCTL_API=3 etcdctl --write-out=table snapshot status /var/lib/backup/etcd-snapshot.db
# +----------+----------+------------+------------+
# |   HASH   | REVISION | TOTAL KEYS | TOTAL SIZE |
# +----------+----------+------------+------------+
# | 765f9b29 |   454115 |       1907 |     8.7 MB |
# +----------+----------+------------+------------+
```

- Restore

```sh
sudo -i ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key snapshot restore /var/lib/backup/etcd-snapshot.db
# {"level":"info","ts":1767926957.5838912,"caller":"snapshot/v3_snapshot.go:306","msg":"restoring snapshot","path":"/var/lib/backup/etcd-snapshot.db","wal-dir":"default.etcd/member/wal","data-dir":"default.etcd","snap-dir":"default.etcd/member/snap"}
# {"level":"info","ts":1767926957.6159048,"caller":"mvcc/kvstore.go:388","msg":"restored last compact revision","meta-bucket-name":"meta","meta-bucket-name-key":"finishedCompactRev","restored-compact-revision":452894}
# {"level":"info","ts":1767926957.6326818,"caller":"membership/cluster.go:392","msg":"added member","cluster-id":"cdf818194e3a8c32","local-member-id":"0","added-peer-id":"8e9e05c52164694d","added-peer-peer-urls":["http://localhost:2380"]}
# {"level":"info","ts":1767926957.6468241,"caller":"snapshot/v3_snapshot.go:326","msg":"restored snapshot","path":"/var/lib/backup/etcd-snapshot.db","wal-dir":"default.etcd/member/wal","data-dir":"default.etcd","snap-dir":"default.etcd/member/snap"}
```

---

## 16. 排查集群中故障节点

设置配置环境：
[candidate@node-1] $ kubectl config use-context wk8s

Task
名为 node02 的 Kubernetes worker node 处于 NotReady 状态。
调查发生这种情况的原因，并采取相应的措施将 node 恢复为 Ready 状态，确保所做的任何更改永久生效。

可以使用以下命令，通过 ssh 连接到 node02 节点：
ssh node02
可以使用以下命令，在该节点上获取更高权限：
sudo -i

---

- Prepare Exam Environment

```sh
ssh node02
sudo systemctl stop kubelet
sudo systemctl status kubelet
# ○ kubelet.service - kubelet: The Kubernetes Node Agent
#      Loaded: loaded (/usr/lib/systemd/system/kubelet.service; enabled; preset: enabled)
#     Drop-In: /usr/lib/systemd/system/kubelet.service.d
#              └─10-kubeadm.conf
#      Active: inactive (dead) since Thu 2026-01-08 22:07:20 EST; 14s ago
#    Duration: 2w 1d 5h 28min 15.575s
#        Docs: https://kubernetes.io/docs/
#     Process: 1294 ExecStart=/usr/bin/kubelet $KUBELET_KUBECONFIG_ARGS $KUBELET_CONFIG_ARGS $KUBEL>
#    Main PID: 1294 (code=exited, status=0/SUCCESS)
#         CPU: 4h 2min 16.574s
```

- Solution

```sh
ssh node01

kubectl get node
# NAME           STATUS     ROLES           AGE   VERSION
# controlplane   Ready      control-plane   44d   v1.34.3
# node01         Ready      <none>          44d   v1.33.6
# node02         NotReady   <none>          44d   v1.33.6

kubectl describe node node02
# Conditions:
#   Type                 Status    LastHeartbeatTime                 LastTransitionTime                Reason              Message
#   ----                 ------    -----------------                 ------------------                ------              -------
#   NetworkUnavailable   False     Mon, 05 Jan 2026 01:16:38 -0500   Mon, 05 Jan 2026 01:16:38 -0500   FlannelIsUp         Flannel is running on this node
#   MemoryPressure       Unknown   Thu, 08 Jan 2026 22:15:24 -0500   Thu, 08 Jan 2026 22:17:49 -0500   NodeStatusUnknown   Kubelet stopped posting node status.
#   DiskPressure         Unknown   Thu, 08 Jan 2026 22:15:24 -0500   Thu, 08 Jan 2026 22:17:49 -0500   NodeStatusUnknown   Kubelet stopped posting node status.
#   PIDPressure          Unknown   Thu, 08 Jan 2026 22:15:24 -0500   Thu, 08 Jan 2026 22:17:49 -0500   NodeStatusUnknown   Kubelet stopped posting node status.
#   Ready                Unknown   Thu, 08 Jan 2026 22:15:24 -0500   Thu, 08 Jan 2026 22:17:49 -0500   NodeStatusUnknown   Kubelet stopped posting node status.
# Events:
#   Type     Reason                   Age                  From             Message
#   ----     ------                   ----                 ----             -------
#   Normal   Starting                 9m5s                 kubelet          Starting kubelet.
#   Warning  InvalidDiskCapacity      9m5s                 kubelet          invalid capacity 0 on image filesystem
#   Normal   NodeAllocatableEnforced  9m4s                 kubelet          Updated Node Allocatable limit across pods
#   Normal   NodeHasSufficientMemory  9m4s (x2 over 9m4s)  kubelet          Node node02 status is now: NodeHasSufficientMemory
#   Normal   NodeHasNoDiskPressure    9m4s (x2 over 9m4s)  kubelet          Node node02 status is now: NodeHasNoDiskPressure
#   Normal   NodeHasSufficientPID     9m4s (x2 over 9m4s)  kubelet          Node node02 status is now: NodeHasSufficientPID
#   Normal   NodeReady                9m4s                 kubelet          Node node02 status is now: NodeReady
#   Normal   NodeNotReady             94s (x2 over 11m)    node-controller  Node node02 status is now: NodeNotReady
```

- Diagnose

```sh
ssh node02

sudo -i

# check log
journalctl -u kubelet -xe --no-pager | tail -n 60
# Jan 08 22:10:18 node02 kubelet[1346259]: I0108 22:10:18.971510 1346259 memory_manager.go:186] "Starting memorymanager" policy="None"
# Jan 08 22:10:18 node02 kubelet[1346259]: I0108 22:10:18.971570 1346259 state_mem.go:35] "Initializing new in-memory state store"
# Jan 08 22:10:18 node02 kubelet[1346259]: I0108 22:10:18.973184 1346259 state_mem.go:75] "Updated machine memory state"
# Jan 08 22:10:18 node02 kubelet[1346259]: E0108 22:10:18.991945 1346259 manager.go:517] "Failed to read data from checkpoint" err="checkpoint is not found" checkpoint="kubelet_internal_checkpoint"
# Jan 08 22:10:18 node02 kubelet[1346259]: I0108 22:10:18.993449 1346259 eviction_manager.go:189] "Eviction manager: starting control loop"
# Jan 08 22:10:18 node02 kubelet[1346259]: I0108 22:10:18.993493 1346259 container_log_manager.go:189] "Initializing container log rotate workers" workers=1 monitorPeriod="10s"
# Jan 08 22:10:18 node02 kubelet[1346259]: E0108 22:10:18.997433 1346259 eviction_manager.go:267] "eviction manager: failed to check if we have separate container filesystem. Ignoring." err="no imagefs label for configured runtime"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:18.998332 1346259 plugin_manager.go:118] "Starting Kubelet Plugin Manager"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.003216 1346259 kuberuntime_manager.go:1746] "Updating runtime config through cri with podcidr" CIDR="10.244.2.0/24"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.048343 1346259 kubelet_network.go:61] "Updating Pod CIDR" originalPodCIDR="" newPodCIDR="10.244.2.0/24"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.052192 1346259 kubelet_node_status.go:501] "Fast updating node status as it just became ready"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.151261 1346259 apiserver.go:52] "Watching apiserver"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.205231 1346259 kubelet_node_status.go:75] "Attempting to register node" node="node02"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.257612 1346259 desired_state_of_world_populator.go:158] "Finished populating initial desired state of world"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.276066 1346259 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolume started for volume \"registration-dir\" (UniqueName: \"kubernetes.io/host-path/104d8b4b-29e4-41b8-95bf-b950562bec3c-registration-dir\") pod \"csi-hostpathplugin-0\" (UID: \"104d8b4b-29e4-41b8-95bf-b950562bec3c\") " pod="default/csi-hostpathplugin-0"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.276302 1346259 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolume started for volume \"dev-dir\" (UniqueName: \"kubernetes.io/host-path/104d8b4b-29e4-41b8-95bf-b950562bec3c-dev-dir\") pod \"csi-hostpathplugin-0\" (UID: \"104d8b4b-29e4-41b8-95bf-b950562bec3c\") " pod="default/csi-hostpathplugin-0"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.276485 1346259 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolume started for volume \"run\" (UniqueName: \"kubernetes.io/host-path/e3bf33b9-857b-4cb2-a892-5e32c9818991-run\") pod \"kube-flannel-ds-xpvg6\" (UID: \"e3bf33b9-857b-4cb2-a892-5e32c9818991\") " pod="kube-flannel/kube-flannel-ds-xpvg6"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.287285 1346259 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolume started for volume \"xtables-lock\" (UniqueName: \"kubernetes.io/host-path/e3bf33b9-857b-4cb2-a892-5e32c9818991-xtables-lock\") pod \"kube-flannel-ds-xpvg6\" (UID: \"e3bf33b9-857b-4cb2-a892-5e32c9818991\") " pod="kube-flannel/kube-flannel-ds-xpvg6"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.287577 1346259 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolume started for volume \"socket-dir\" (UniqueName: \"kubernetes.io/host-path/104d8b4b-29e4-41b8-95bf-b950562bec3c-socket-dir\") pod \"csi-hostpathplugin-0\" (UID: \"104d8b4b-29e4-41b8-95bf-b950562bec3c\") " pod="default/csi-hostpathplugin-0"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.288596 1346259 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolume started for volume \"xtables-lock\" (UniqueName: \"kubernetes.io/host-path/f2c5d99e-11bd-40d1-adc1-1addb0f95798-xtables-lock\") pod \"kube-proxy-sx5wr\" (UID: \"f2c5d99e-11bd-40d1-adc1-1addb0f95798\") " pod="kube-system/kube-proxy-sx5wr"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.296105 1346259 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolume started for volume \"lib-modules\" (UniqueName: \"kubernetes.io/host-path/f2c5d99e-11bd-40d1-adc1-1addb0f95798-lib-modules\") pod \"kube-proxy-sx5wr\" (UID: \"f2c5d99e-11bd-40d1-adc1-1addb0f95798\") " pod="kube-system/kube-proxy-sx5wr"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.296480 1346259 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolume started for volume \"cni-plugin\" (UniqueName: \"kubernetes.io/host-path/e3bf33b9-857b-4cb2-a892-5e32c9818991-cni-plugin\") pod \"kube-flannel-ds-xpvg6\" (UID: \"e3bf33b9-857b-4cb2-a892-5e32c9818991\") " pod="kube-flannel/kube-flannel-ds-xpvg6"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.306376 1346259 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolume started for volume \"plugins-dir\" (UniqueName: \"kubernetes.io/host-path/104d8b4b-29e4-41b8-95bf-b950562bec3c-plugins-dir\") pod \"csi-hostpathplugin-0\" (UID: \"104d8b4b-29e4-41b8-95bf-b950562bec3c\") " pod="default/csi-hostpathplugin-0"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.310969 1346259 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolume started for volume \"csi-data-dir\" (UniqueName: \"kubernetes.io/host-path/104d8b4b-29e4-41b8-95bf-b950562bec3c-csi-data-dir\") pod \"csi-hostpathplugin-0\" (UID: \"104d8b4b-29e4-41b8-95bf-b950562bec3c\") " pod="default/csi-hostpathplugin-0"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.313071 1346259 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolume started for volume \"cni\" (UniqueName: \"kubernetes.io/host-path/e3bf33b9-857b-4cb2-a892-5e32c9818991-cni\") pod \"kube-flannel-ds-xpvg6\" (UID: \"e3bf33b9-857b-4cb2-a892-5e32c9818991\") " pod="kube-flannel/kube-flannel-ds-xpvg6"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.317281 1346259 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolume started for volume \"var-lib-calico\" (UniqueName: \"kubernetes.io/host-path/462c6931-5abd-4b32-a1fb-2018c5ae055f-var-lib-calico\") pod \"tigera-operator-7d4578d8d-8vf9w\" (UID: \"462c6931-5abd-4b32-a1fb-2018c5ae055f\") " pod="tigera-operator/tigera-operator-7d4578d8d-8vf9w"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.317415 1346259 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolume started for volume \"mountpoint-dir\" (UniqueName: \"kubernetes.io/host-path/104d8b4b-29e4-41b8-95bf-b950562bec3c-mountpoint-dir\") pod \"csi-hostpathplugin-0\" (UID: \"104d8b4b-29e4-41b8-95bf-b950562bec3c\") " pod="default/csi-hostpathplugin-0"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.363982 1346259 kubelet_node_status.go:124] "Node was previously registered" node="node02"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.364443 1346259 kubelet_node_status.go:78] "Successfully registered node" node="node02"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.691938 1346259 csi_plugin.go:106] kubernetes.io/csi: Trying to validate a new CSI Driver with name: hostpath.csi.k8s.io endpoint: /var/lib/kubelet/plugins/csi-hostpath/csi.sock versions: 1.0.0
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.697336 1346259 csi_plugin.go:119] kubernetes.io/csi: Register new plugin with name: hostpath.csi.k8s.io at endpoint: /var/lib/kubelet/plugins/csi-hostpath/csi.sock
# Jan 08 22:16:57 node02 systemd[1]: Stopping kubelet.service - kubelet: The Kubernetes Node Agent...
# ░░ Subject: A stop job for unit kubelet.service has begun execution
# ░░ Defined-By: systemd
# ░░ Support: http://www.ubuntu.com/support
# ░░
# ░░ A stop job for unit kubelet.service has begun execution.
# ░░
# ░░ The job identifier is 67933.
# Jan 08 22:16:57 node02 kubelet[1346259]: I0108 22:16:57.312242 1346259 dynamic_cafile_content.go:175] "Shutting down controller" name="client-ca-bundle::/etc/kubernetes/pki/ca.crt"
# Jan 08 22:16:57 node02 systemd[1]: kubelet.service: Deactivated successfully.
# ░░ Subject: Unit succeeded
# ░░ Defined-By: systemd
# ░░ Support: http://www.ubuntu.com/support
# ░░
# ░░ The unit kubelet.service has successfully entered the 'dead' state.
# Jan 08 22:16:57 node02 systemd[1]: Stopped kubelet.service - kubelet: The Kubernetes Node Agent.
# ░░ Subject: A stop job for unit kubelet.service has finished
# ░░ Defined-By: systemd
# ░░ Support: http://www.ubuntu.com/support
# ░░
# ░░ A stop job for unit kubelet.service has finished.
# ░░
# ░░ The job identifier is 67933 and the job result is done.
# Jan 08 22:16:57 node02 systemd[1]: kubelet.service: Consumed 26.274s CPU time, 89.4M memory peak, 0B memory swap peak.
# ░░ Subject: Resources consumed by unit runtime
# ░░ Defined-By: systemd
# ░░ Support: http://www.ubuntu.com/support
# ░░
# ░░ The unit kubelet.service completed and consumed the indicated resources.

# check kubelet
systemctl status kubelet --no-pager
# ○ kubelet.service - kubelet: The Kubernetes Node Agent
#      Loaded: loaded (/usr/lib/systemd/system/kubelet.service; enabled; preset: enabled)
#     Drop-In: /usr/lib/systemd/system/kubelet.service.d
#              └─10-kubeadm.conf
#      Active: inactive (dead) since Thu 2026-01-08 22:16:57 EST; 5min ago
#    Duration: 6min 40.143s
#        Docs: https://kubernetes.io/docs/
#     Process: 1346259 ExecStart=/usr/bin/kubelet $KUBELET_KUBECONFIG_ARGS $KUBELET_CONFIG_ARGS $KUBELET_KUBEADM_ARGS $KUBELET_EXTRA_ARGS (code=exited, status=0/SUCCESS)
#    Main PID: 1346259 (code=exited, status=0/SUCCESS)
#         CPU: 26.274s

# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.317415 1346259 reconciler_common.go:251] …
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.363982 1346259 kubelet_node_status.…ode02"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.364443 1346259 kubelet_node_status.…ode02"
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.691938 1346259 csi_plugin.go:106] k… 1.0.0
# Jan 08 22:10:19 node02 kubelet[1346259]: I0108 22:10:19.697336 1346259 csi_plugin.go:119] k…i.sock
# Jan 08 22:16:57 node02 systemd[1]: Stopping kubelet.service - kubelet: The Kubernetes Node …ent...
# Jan 08 22:16:57 node02 kubelet[1346259]: I0108 22:16:57.312242 1346259 dynamic_cafile_conte…a.crt"
# Jan 08 22:16:57 node02 systemd[1]: kubelet.service: Deactivated successfully.
# Jan 08 22:16:57 node02 systemd[1]: Stopped kubelet.service - kubelet: The Kubernetes Node Agent.
# Jan 08 22:16:57 node02 systemd[1]: kubelet.service: Consumed 26.274s CPU time, 89.4M memory… peak.
# Hint: Some lines were ellipsized, use -l to show in full.


# check container runtime
systemctl status containerd --no-pager
# ● containerd.service - containerd container runtime
#      Loaded: loaded (/usr/lib/systemd/system/containerd.service; enabled; preset: enabled)
#      Active: active (running) since Wed 2025-12-24 16:39:07 EST; 2 weeks 1 day ago
#        Docs: https://containerd.io
#    Main PID: 1279 (containerd)
#       Tasks: 123
#      Memory: 119.0M (peak: 353.0M)
#         CPU: 1h 41min 10.049s
#      CGroup: /system.slice/containerd.service
#              ├─   1279 /usr/bin/containerd
#              ├─ 998698 /usr/bin/containerd-shim-runc-v2 -namespace k8s.io -id 074b829e17d42c30e1d…
#              ├─1106965 /usr/bin/containerd-shim-runc-v2 -namespace k8s.io -id 886323e8aff112d8ecf…
#              ├─1111471 /usr/bin/containerd-shim-runc-v2 -namespace k8s.io -id 2650b7b8f91b24f236c…
#              ├─1136983 /usr/bin/containerd-shim-runc-v2 -namespace k8s.io -id 5c4eb6a2c3e8029c9b7…
#              ├─1174159 /usr/bin/containerd-shim-runc-v2 -namespace k8s.io -id 62aa1841e5f52ebc830…
#              ├─1323970 /usr/bin/containerd-shim-runc-v2 -namespace k8s.io -id 64f4f2986757ee970ff…
#              ├─1323972 /usr/bin/containerd-shim-runc-v2 -namespace k8s.io -id 6248e8312b504aa68af…
#              └─1324433 /usr/bin/containerd-shim-runc-v2 -namespace k8s.io -id c353def57aea55f5a2b…

# Jan 08 20:44:33 node02 containerd[1279]: time="2026-01-08T20:44:33.882044101-05:00" level=i…fully"
# Jan 08 20:44:33 node02 containerd[1279]: time="2026-01-08T20:44:33.883482261-05:00" level=i…6ec\""
# Jan 08 20:44:33 node02 containerd[1279]: time="2026-01-08T20:44:33.919718776-05:00" level=i…fully"
# Jan 08 20:44:33 node02 containerd[1279]: time="2026-01-08T20:44:33.919773879-05:00" level=i…fully"
# Jan 08 20:44:33 node02 containerd[1279]: time="2026-01-08T20:44:33.921404147-05:00" level=i…6ec\""
# Jan 08 20:44:33 node02 containerd[1279]: time="2026-01-08T20:44:33.921463749-05:00" level=i…6ec\""
# Jan 08 20:44:33 node02 containerd[1279]: time="2026-01-08T20:44:33.961157008-05:00" level=i…fully"
# Jan 08 20:44:33 node02 containerd[1279]: time="2026-01-08T20:44:33.968244305-05:00" level=w…atus."
# Jan 08 20:44:33 node02 containerd[1279]: time="2026-01-08T20:44:33.968527616-05:00" level=i…fully"
# Jan 08 22:10:19 node02 containerd[1279]: time="2026-01-08T22:10:19.033113557-05:00" level=i…nfig."
# Hint: Some lines were ellipsized, use -l to show in full.
```

- Solution

```sh
# check kubelet
sudo systemctl enable kubelet --now

# confirm
sudo systemctl status kubelet
# ● kubelet.service - kubelet: The Kubernetes Node Agent
#      Loaded: loaded (/usr/lib/systemd/system/kubelet.service; enabled; preset: enabled)
#     Drop-In: /usr/lib/systemd/system/kubelet.service.d
#              └─10-kubeadm.conf
#      Active: active (running) since Thu 2026-01-08 22:10:17 EST; 8s ago
#        Docs: https://kubernetes.io/docs/
#    Main PID: 1346259 (kubelet)
#       Tasks: 14 (limit: 2205)
#      Memory: 88.5M (peak: 89.4M)
#         CPU: 3.515s
#      CGroup: /system.slice/kubelet.service
#              └─1346259 /usr/bin/kubelet --bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.>
```

- Confirm

```sh
ssh node01

# confirm
kubectl get node
# NAME           STATUS   ROLES           AGE   VERSION
# controlplane   Ready    control-plane   44d   v1.34.3
# node01         Ready    <none>          44d   v1.33.6
# node02         Ready    <none>          44d   v1.33.6
```

---

## 17.节点维护

设置配置环境：
[candidate@node-1] $ kubectl config use-context ek8s

Task
将名为 node02 的 node 设置为不可用，并重新调度该 node 上所有运行的 pods。Copy

---

- Setup Exam environment

```sh
kubectl create deploy web --image=nginx --replicas=6
```

---

- Answer

```sh
# info: node
kubectl get node -o wide
# NAME           STATUS   ROLES           AGE   VERSION   INTERNAL-IP      EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION      CONTAINER-RUNTIME
# controlplane   Ready    control-plane   44d   v1.34.3   192.168.10.150   <none>        Ubuntu 24.04.3 LTS   6.14.0-37-generic   containerd://1.7.28
# node01         Ready    <none>          44d   v1.33.6   192.168.10.151   <none>        Ubuntu 24.04.3 LTS   6.14.0-37-generic   containerd://1.7.28
# node02         Ready    <none>          44d   v1.33.6   192.168.10.152   <none>        Ubuntu 24.04.3 LTS   6.14.0-36-generic   containerd://1.7.28

# info: pods
kubectl get pod -o wide
# NAME                   READY   STATUS    RESTARTS   AGE     IP             NODE     NOMINATED NODE   READINESS GATES
# csi-hostpathplugin-0   8/8     Running   0          9m23s   10.244.2.117   node02   <none>           <none>
# web-64c966cf88-5h65m   1/1     Running   0          27s     10.244.1.102   node01   <none>           <none>
# web-64c966cf88-9vb5l   1/1     Running   0          27s     10.244.2.130   node02   <none>           <none>
# web-64c966cf88-gbvbp   1/1     Running   0          27s     10.244.2.128   node02   <none>           <none>
# web-64c966cf88-k5xwd   1/1     Running   0          27s     10.244.1.103   node01   <none>           <none>
# web-64c966cf88-mhrsr   1/1     Running   0          27s     10.244.1.104   node01   <none>           <none>
# web-64c966cf88-sfhmv   1/1     Running   0          27s     10.244.2.129   node02   <none>           <none>

# cordon a node
kubectl cordon node02
# node/node02 cordoned

# drain workload
kubectl drain node02 --ignore-daemonsets --delete-emptydir-data --force
# node/node02 already cordoned
# Warning: ignoring DaemonSet-managed Pods: kube-flannel/kube-flannel-ds-xpvg6, kube-system/kube-proxy-sx5wr
# evicting pod tigera-operator/tigera-operator-7d4578d8d-8vf9w
# evicting pod ing-internal/hello-5f8f7fff68-82dwv
# evicting pod default/web-64c966cf88-sfhmv
# evicting pod default/web-64c966cf88-9vb5l
# evicting pod db/mongo-689485f9f7-ld59l
# evicting pod default/csi-hostpathplugin-0
# evicting pod default/web-64c966cf88-gbvbp
# I0108 22:38:00.684453  171955 request.go:752] "Waited before sending request" delay="1.002110385s" reason="client-side throttling, not priority and fairness" verb="GET" URL="https://192.168.10.150:6443/api/v1/namespaces/tigera-operator/pods/tigera-operator-7d4578d8d-8vf9w"
# pod/tigera-operator-7d4578d8d-8vf9w evicted
# pod/web-64c966cf88-gbvbp evicted
# pod/web-64c966cf88-sfhmv evicted
# pod/web-64c966cf88-9vb5l evicted
# pod/mongo-689485f9f7-ld59l evicted
# pod/hello-5f8f7fff68-82dwv evicted
# pod/csi-hostpathplugin-0 evicted
# node/node02 drained

# verify
kubectl get node
# NAME           STATUS                     ROLES           AGE   VERSION
# controlplane   Ready                      control-plane   44d   v1.34.3
# node01         Ready                      <none>          44d   v1.33.6
# node02         Ready,SchedulingDisabled   <none>          44d   v1.33.6

kubectl get pod | grep node02
# NAME                   READY   STATUS              RESTARTS   AGE    IP             NODE     NOMINATED NODE   READINESS GATES
# csi-hostpathplugin-0   0/8     ContainerCreating   0          48s    <none>         node01   <none>           <none>
# web-64c966cf88-5h65m   1/1     Running             0          103s   10.244.1.102   node01   <none>           <none>
# web-64c966cf88-8jh54   1/1     Running             0          55s    10.244.1.108   node01   <none>           <none>
# web-64c966cf88-9nsj9   1/1     Running             0          56s    10.244.1.106   node01   <none>           <none>
# web-64c966cf88-jw42h   1/1     Running             0          55s    10.244.1.107   node01   <none>           <none>
# web-64c966cf88-k5xwd   1/1     Running             0          103s   10.244.1.103   node01   <none>           <none>
# web-64c966cf88-mhrsr   1/1     Running             0          103s   10.244.1.104   node01   <none>           <none>
```
