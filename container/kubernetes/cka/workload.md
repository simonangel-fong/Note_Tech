# CKA - Workload

[Back](../index.md)

- [CKA - Workload](#cka---workload)
  - [POD, Deployment, STS](#pod-deployment-sts)
    - [Task: Pod - Log](#task-pod---log)
    - [Task: Pod - log](#task-pod---log-1)
    - [Task: Pod - Multiple Containers](#task-pod---multiple-containers)
    - [Task: Pod - multiple container](#task-pod---multiple-container)
    - [Task: Pod - Sidecar Pod](#task-pod---sidecar-pod)
    - [Task: Pod - Volume + Sidercar](#task-pod---volume--sidercar)
    - [Task: Pod - volume + sidecar](#task-pod---volume--sidecar)
    - [Task: Pod - volume + sidecar + env](#task-pod---volume--sidecar--env)
    - [Task: Deployment - scale](#task-deployment---scale)
    - [Task: Deployment - scale](#task-deployment---scale-1)
    - [Task: Deployment Rollback](#task-deployment-rollback)
    - [Task: StatefulSets \& Headless Services](#task-statefulsets--headless-services)
    - [Task: Deployment](#task-deployment)
    - [Task: svc - nodeport](#task-svc---nodeport)
    - [Task: svc](#task-svc)
    - [Task: troubleshooting pod](#task-troubleshooting-pod)
  - [ConfigMap \& Secret](#configmap--secret)
    - [Task: ConfigMap](#task-configmap)
    - [Task: CM](#task-cm)
    - [Task: ConfigMaps \& Secrets](#task-configmaps--secrets)
  - [Scaling](#scaling)
    - [Task: VPA](#task-vpa)
    - [Task: Autoscaling](#task-autoscaling)
    - [Task: HPA](#task-hpa)
    - [Task: HPA](#task-hpa-1)
  - [Helm](#helm)
    - [Task: Install Argo](#task-install-argo)
    - [Task: Deploy with helm](#task-deploy-with-helm)
    - [Task: Helm](#task-helm)
    - [Task: Upgrade Helm Release](#task-upgrade-helm-release)
  - [Kustomize](#kustomize)
    - [Task: Kustomize](#task-kustomize)
    - [Task: CRD](#task-crd)
    - [Task: list CRDs](#task-list-crds)
  - [Resources](#resources)
    - [Task: PriorityClass](#task-priorityclass)
    - [Task: Limit range](#task-limit-range)
    - [Task: query resource usage](#task-query-resource-usage)
    - [Task: Query pod 的 CPU](#task-query-pod-的-cpu)
    - [Task: Resources](#task-resources)

---

## POD, Deployment, STS

### Task: Pod - Log

Task
监控 pod foo 的日志并：
提取与错误 No such file or directory 相对应的日志行
将这些日志行写入 /tmp/KUTR00101/foo

---

- Config env

```sh
kubectl run foo --image=busybox -- cat /tmp/msg
# pod/foo created

kubectl exec -it foo -- ulimit -n
```

- Solution

```sh
kubectl logs foo | grep "RLIMIT_NOFILE" > /opt/KUTR00101/foo
```

---

### Task: Pod - log

1. monitor the log of the fnf pod and filter any lines containing the error "No such file or directory".
2. /tmp/cka/sorted_log.log

- Env

```sh
k run fnf --image=busybox -- cat /tmp/msg
```

---

- Solution

```sh
k get pod fnf

k logs fnf | grep "No such file or directory" > /opt/cka/answers/sorted_log.log
```

---

### Task: Pod - Multiple Containers

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

### Task: Pod - multiple container

CKA EXAM OBJECTIVE: Understand the primitives used to create robust, self-healing, application deployments.
Task :

1. Create a Pod named multicontainer that has two containers:
2. A container running the redis:6.2.6 image.
3. A container running the nginx:1.21.6 image.

---

- Solution

```yaml
# pod-multiple01.yaml
apiVersion: v1
kind: Pod
metadata:
  name: multicontainer
spec:
  containers:
    - name: redis
      image: redis:6.2.6
    - name: nginx
      image: nginx:1.21.6
```

```sh
kubectl apply -f pod-multiple01.yaml
# pod/multicontainer created

k describe pod multicontainer
# Containers:
#   nginx:
#     Container ID:   containerd://b275f940b9804b275dbfe06b14eb6f714ab26aaf5c7074834796748d6cccb6b6
#     Image:          nginx:1.21.6
#   redis:
#     Container ID:   containerd://5d18eaf6b0424a3c1eb7765005deb0424bee00e81bf114520d2ca33699edd233
#     Image:          redis:6.2.6
```

---

### Task: Pod - Sidecar Pod

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
# task-sidecar01-env.yaml
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
kubectl apply -f task-sidecar01-env.yaml
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

### Task: Pod - Volume + Sidercar

A legacy app needs to be integrated into the Kubernetes built-in logging architecture (i.e. kubectl logs). Adding a streaming co-located container is a good and common way to accomplish this requirement.

Task

Update the existing Deployment synergy-deployment, adding a co-located container named sidecar using the busybox:stable image to the existing Pod.
The new co-located container has to run the following command: `/bin/sh-c "tail -n+l -f /var/log/synergy-deployment.log"`
Use a Volume mounted at /var/log to make the log file synergy-deployment.log available to the co located container.
Do not modify the specification of the existing container other than adding the required.
Hint: Use a shared volume to expose the log file between the main application container and the sidecar

- Setup Env

```sh
tee env-deploy.yaml<<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: synergy-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: synergy
  template:
    metadata:
      labels:
        app: synergy
    spec:
      containers:
      - name: synergy
        image: busybox
        command: ["/bin/sh", "-c"]
        args:
          - |
            i=1;
            while true; do
              echo "$(date) synergy log line $i" >> /var/log/synergy-deployment.log;
              i=$((i+1));
              sleep 2;
            done
EOF

kubectl apply -f env-deploy.yaml
```

---

### Task: Pod - volume + sidecar

CKA EXAM OBJECTIVE: Configure volume types [ ... ]
Task:

1. Add a sidecar container using the busybox image to the existing Pod logger.
2. The container should be mounted at the path /var/log and run the command /bin/sh -c tail -f /var/log/log01.log

- setup env

```yaml
# task-sidecar-env.yaml
apiVersion: v1
kind: Pod
metadata:
  name: logger
spec:
  nodeName: node01
  containers:
    - name: writer
      image: busybox
      command:
        - "/bin/sh"
        - "-c"
      args:
        - |
          mkdir -pv /var/log
          i=0;
          while true;
          do
           echo "$i: $(date)" >> /var/log/log01.log;
           i=$((i+1));
           sleep 1;
          done
```

```sh
kubectl apply -f task-sidecar-env.yaml
```

---

- Solution

```yaml
# task-sidecar.yaml
apiVersion: v1
kind: Pod
metadata:
  name: logger
spec:
  nodeName: node01
  volumes:
    - name: pod-vol
      emptyDir: {}
  containers:
    - name: writer
      image: busybox
      volumeMounts:
        - name: pod-vol
          mountPath: /var/log
      command:
        - "/bin/sh"
        - "-c"
      args:
        - |
          mkdir -pv /var/log
          i=0;
          while true;
          do
           echo "$i: $(date)" >> /var/log/log01.log;
           i=$((i+1));
           sleep 1;
          done
    - name: reader
      image: busybox
      volumeMounts:
        - name: pod-vol
          mountPath: /var/log
      command:
        - "/bin/sh"
        - "-c"
      args:
        - |
          tail -f /var/log/log01.log
```

```sh
k apply -f task-sidecar.yaml
```

---

### Task: Pod - volume + sidecar + env

Create a Pod mc-pod in the mc-namespace namespace with three containers. The first container should be named mc-pod-1, run the nginx:1-alpine image, and set an environment variable NODE_NAME to the node name. The second container should be named mc-pod-2, run the busybox:1 image, and continuously log the output of the date command to the file /var/log/shared/date.log every second. The third container should have the name mc-pod-3, run the image busybox:1, and print the contents of the date.log file generated by the second container to stdout. Use a shared, non-persistent volume.

- Setup env

```sh
kubectl create namespace mc-namespace
```

---

- Solution:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mc-pod
  namespace: mc-namespace
spec:
  volumes:
    - name: shared-vol
      emptyDir: {}

  containers:
    - name: mc-pod-1
      image: nginx:1-alpine
      env:
        - name: NODE_NAME
          valueFrom:
            fieldRef:
              fieldPath: spec.nodeName
      volumeMounts:
        - name: shared-vol
          mountPath: /var/log/shared

    - name: mc-pod-2
      image: busybox:1
      command: ["/bin/sh", "-c"]
      args:
        - while true; do date >> /var/log/shared/date.log; sleep 1; done
      volumeMounts:
        - name: shared-vol
          mountPath: /var/log/shared

    - name: mc-pod-3
      image: busybox:1
      command: ["/bin/sh", "-c"]
      args:
        - tail -f /var/log/shared/date.log
      volumeMounts:
        - name: shared-vol
          mountPath: /var/log/shared
```

---

### Task: Deployment - scale

设置配置环境：
[candidate@node-1] $ kubectl config use-context k8s

Task
将 deployment presentation 扩展至 4 个 pods

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

### Task: Deployment - scale

Scale the dragon Deployment to 8 pods

- Setup env

```sh
kubectl create deploy dragon --image=nginx
```

---

- Solution

```sh
kubectl get deploy dragon
# NAME     READY   UP-TO-DATE   AVAILABLE   AGE
# dragon   1/1     1            1           6s

kubectl scale deploy dragon --replicas=8
# deployment.apps/dragon scaled

# confirm
kubectl get deploy dragon
# NAME     READY   UP-TO-DATE   AVAILABLE   AGE
# dragon   8/8     8            8           62s
```

---

### Task: Deployment Rollback

CKA EXAM OBJECTIVE: Understand application deployments and how to perform rolling update and rollbacks
Task:

1. There is an existing deployment named mufasa in namespace king-of-lions.
2. Check the deployment history and rollback to a version that actually works.

- Setup env

```sh
k create ns king-of-lions
k create deploy mufasa --image=nginx -n king-of-lions
k get deploy -n king-of-lions
```

---

- Solution

```sh
# check history
k rollout history deploy mufasa -n king-of-lions
# deployment.apps/mufasa
# REVISION  CHANGE-CAUSE
# 1         <none>


kubectl rollout undo deploy mufasa --to-revision=1 -n king-of-lions
```

---

### Task: StatefulSets & Headless Services

Deploy a StatefulSet named web with 2 replicas using the NGINX image.
Each pod should have its own 1Gi persistent volume for /usr/share/nginx/html.

Ensure that the StatefulSet pods have stable network identities and persistent storage that remains associated with the ordinal index (even if pods are rescheduled).

Create a Headless Service named web to facilitate stable networking for the StatefulSet

```yaml
# task-sts.yaml
apiVersion: v1
kind: Service
metadata:
  name: web
spec:
  ports:
    - name: http
      port: 80
  clusterIP: None
  selector:
    app: web
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  serviceName: web
  replicas: 2
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: nginx
          image: nginx
          ports:
            - name: http
              containerPort: 80
          volumeMounts:
            - name: pvc-sts
              mountPath: /usr/share/nginx/html
  volumeClaimTemplates:
    - metadata:
        name: pvc-sts
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 1Gi
```

```sh
kubectl apply -f task-sts.yaml
# service/web created
# statefulset.apps/web created

# confirm sts
kubectl get sts web -o wide
# NAME   READY   AGE   CONTAINERS   IMAGES
# web    2/2     44s   nginx        nginx

kubectl describe sts web
# Selector:           app=web
# Volume Claims:
#   Name:          pvc-sts
#   StorageClass:
#   Labels:        <none>
#   Annotations:   <none>
#   Capacity:      1Gi
#   Access Modes:  [ReadWriteOnce]

# confirm pvc
kubectl get pvc -l app=web
# NAME            STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
# pvc-sts-web-0   Bound    pvc-3232a60c-c69d-4d6a-a746-a62925e8fdbb   1Gi        RWO            local-path     <unset>                 14m
# pvc-sts-web-1   Bound    pvc-a0cf66e7-0c90-491d-928b-1733d5db1abe   1Gi        RWO            local-path     <unset>                 14m

# confirm svc
kubectl get svc web
# NAME   TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
# web    ClusterIP   None         <none>        80/TCP    2m15s

kubectl describe svc web
# Endpoints:                10.244.2.134:80,10.244.2.136:80

kubectl run --rm -it sts-test --image=busybox --restart=Never -- nslookup web.default
# Server:         10.96.0.10
# Address:        10.96.0.10:53

# Name:   web.default.svc.cluster.local
# Address: 10.244.2.136
# Name:   web.default.svc.cluster.local
# Address: 10.244.2.134
```

---

### Task: Deployment

Create a deployment named hr-web-app using the image kodekloud/webapp-color with 2 replicas.

---

- Solution

```sh
k create deploy hr-web-app --image=kodekloud/webapp-color --replicas=2
# deployment.apps/hr-web-app created

k get deploy -n default
# NAME         READY   UP-TO-DATE   AVAILABLE   AGE
# hr-web-app   2/2     2            2           35s
```

---

### Task: svc - nodeport

Expose the hr-web-app created in the previous task as a service named hr-web-app-service, accessible on port 30082 on the nodes of the cluster.

The web application listens on port 8080.

- Setup env

```sh
k create deploy hr-web-app --image=nginx --replicas=2
```

---

- Solution:

```sh
k get deploy hr-web-app
# NAME         READY   UP-TO-DATE   AVAILABLE   AGE
# hr-web-app   2/2     2            2           12s

kubectl expose deployment hr-web-app --type=NodePort --port=8080 --name=hr-web-app-service --dry-run=client -o yaml > svc.yaml

vi svc.yaml
# apiVersion: v1
# kind: Service
# metadata:
#   name: hr-web-app-service
# spec:
#   ports:
#   - port: 8080
#     protocol: TCP
#     targetPort: 8080
#     nodePort: 30082
#   selector:
#     app: hr-web-app
#   type: NodePort

k apply -f svc.yaml
# service/hr-web-app-service created

# confirm
k describe svc hr-web-app-service
# Name:                     hr-web-app-service
# Namespace:                default
# Labels:                   <none>
# Annotations:              <none>
# Selector:                 app=hr-web-app
# Type:                     NodePort
# IP Family Policy:         SingleStack
# IP Families:              IPv4
# IP:                       10.104.64.79
# IPs:                      10.104.64.79
# Port:                     <unset>  8080/TCP
# TargetPort:               8080/TCP
# NodePort:                 <unset>  30082/TCP
# Endpoints:                10.244.196.149:8080,10.244.140.77:8080
# Session Affinity:         None
# External Traffic Policy:  Cluster
# Internal Traffic Policy:  Cluster
# Events:                   <none>
```

---

### Task: svc

Create a service named messaging-service to expose the messaging pod within the cluster on port 6379. The messaging pod is running in the default namespace.

---

- solution

```sh
k expose pod messaging --name=messaging-service --port=6379 --type=ClusterIP
# service/messaging-service exposed

# confirm
k describe svc messaging-service
# Name:                     messaging-service
# Namespace:                default
# Labels:                   tier=msg
# Annotations:              <none>
# Selector:                 tier=msg
# Type:                     ClusterIP
# IP Family Policy:         SingleStack
# IP Families:              IPv4
# IP:                       172.20.133.163
# IPs:                      172.20.133.163
# Port:                     <unset>  6379/TCP
# TargetPort:               6379/TCP
# Endpoints:                172.17.0.10:6379
# Session Affinity:         None
# Internal Traffic Policy:  Cluster
# Events:                   <none>
```

---

### Task: troubleshooting pod

A new application orange is deployed. There is something wrong with it. Identify and fix the issue.

```sh
k get pod orange
# NAME     READY   STATUS       RESTARTS      AGE
# orange   0/1     Init:Error   2 (20s ago)   22s


k describe pod orange
# Init Containers:
#   init-myservice:
#     Container ID:  containerd://f4d945a07e1e05db42758f503897e8e796c8eb1d40d1179c19ff302364cc1fe8
#     Image:         busybox
#     Image ID:      docker.io/library/busybox@sha256:2383baad1860bbe9d8a7a843775048fd07d8afe292b94bd876df64a69aae7cb1
#     Port:          <none>
#     Host Port:     <none>
#     Command:
#       sh
#       -c
#       sleeeep 2;


k edt pod orange
# sleeeep 2; => sleep 2;

k replace --force -f /tmp_file

# confirm
k get pod orange
# NAME     READY   STATUS    RESTARTS   AGE
# orange   1/1     Running   0          14s
```

---

## ConfigMap & Secret

### Task: ConfigMap

CKA EXAM OBJECTIVE: Use ConfigMaps and Secrets to configure applications
Task :

1. Create a ConfigMap called metal-cm containing the file ~/index.html
2. To the deployment "enter-sandman" add the metal-cm configmap mounted to the path /var/www/index.html
3. Create the deployment in the metallica Namespace.

- setup env

```sh
tee ./index.html<<EOF
<html>
<title></title>
<body>
  <h1>home</h1>
</body>
</html>
EOF
```

---

- Solution

```sh
k create ns metallica

kubectl create configmap metal-cm -n metallica --from-file=index.html
# configmap/metal-cm created

k describe cm metal-cm
# Name:         metal-cm
# Namespace:    default
# Labels:       <none>
# Annotations:  <none>

# Data
# ====
# index.html:
# ----
# <html>
# <title></title>
# <body>
#   <h1>home</h1>
# </body>
# </html

```

```yaml
# deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: enter-sandman
  namespace: metallica
spec:
  replicas: 1
  selector:
    matchLabels:
      app: enter-sandman
  template:
    metadata:
      labels:
        app: enter-sandman
    spec:
      volumes:
        - name: pod-vol
          configMap:
            name: metal-cm
      containers:
        - image: nginx
          name: nginx
          volumeMounts:
            - name: pod-vol
              mountPath: "/var/www/"
```

```sh
k apply -f deploy.yaml

# confirm
k get pod -n metallica
# NAME                             READY   STATUS    RESTARTS   AGE
# enter-sandman-866c78fd8b-nrbsq   1/1     Running   0          4m38s

k describe pod enter-sandman-866c78fd8b-nrbsq -n metallica
# Containers:
#   nginx:
#     Mounts:
#       /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-bqg26 (ro)
#       /var/www/ from pod-vol (rw)
# Volumes:
#   pod-vol:
#     Type:      ConfigMap (a volume populated by a ConfigMap)
#     Name:      metal-cm
```

---

### Task: CM

An NGINX Deploy named nginx-static is Running in the nginx-static NS. It is configured using a CfgMap named nginx-
config. Update the nginx-config CfgMap to allow only TLSv1.3 connections. re-create, restart, or scale resources as necessary. By using command to test the changes:

[candidate@cka2025] $ curl -- tls-max 1.2 https://web.k8s.local
As TLSV1.2 should not be allowed anymore, the command should fail

- Setup env

```sh
# Namespace
kubectl create ns nginx-static

# Create a self-signed cert for web.k8s.local (TLS secret)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout tls.key -out tls.crt \
  -subj "/CN=web.k8s.local" \
  -addext "subjectAltName=DNS:web.k8s.local"

kubectl create secret tls web-tls --cert=tls.crt --key=tls.key -n nginx-static

# ConfigMap with nginx.conf (initially allows TLSv1.2 + TLSv1.3)
tee cm.yaml<<'EOF'
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
  namespace: nginx-static
data:
  nginx.conf: |
    events {}

    http {
      server {
        listen 443 ssl;
        server_name web.k8s.local;

        ssl_certificate     /etc/nginx/tls/tls.crt;
        ssl_certificate_key /etc/nginx/tls/tls.key;

        ssl_protocols TLSv1.2 TLSv1.3;

        location / {
          default_type text/plain;
          return 200 "nginx-static OK\n";
        }
      }
    }
EOF

kubectl apply -f cm.yaml
# configmap/nginx-config created

tee deploy.yaml<<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-static
  namespace: nginx-static
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx-static
  template:
    metadata:
      labels:
        app: nginx-static
    spec:
      hostNetwork: true
      dnsPolicy: ClusterFirstWithHostNet
      containers:
      - name: nginx
        image: nginx:1.25-alpine
        ports:
        - containerPort: 443
          hostPort: 443
        volumeMounts:
        - name: nginx-conf
          mountPath: /etc/nginx/nginx.conf
          subPath: nginx.conf
        - name: tls
          mountPath: /etc/nginx/tls
          readOnly: true
      volumes:
      - name: nginx-conf
        configMap:
          name: nginx-config
      - name: tls
        secret:
          secretName: web-tls
EOF

kubectl apply -f deploy.yaml
# deployment.apps/nginx-static created
```

---

- Solution

```sh
# remove TLSv1.2
kubectl edit cm nginx-config -n nginx-static
# configmap/nginx-config edited

# restart deployment to apply new cm
kubectl rollout restart deploy nginx-static -n nginx-static
# deployment.apps/nginx-static restarted
```

---

### Task: ConfigMaps & Secrets

CKA EXAM OBJECTIVE: Use ConfigMaps and Secrets to configure applications
Task:

1. You will adjust an existing pod named kiwi-secret-pod in namespace kiwi.
2. Make a new secret named juicysecret. It must contain the following key/value pairs:
3. username=kiwis, password=aredelicious
4. Make this content available in the pod kiwi-secret-pod as the following environment variables: USERKIWI and PASSKIWI.

- Setup env

```yaml
# task-secret-env.yaml
apiVersion: v1
kind: Pod
metadata:
  name: kiwi-secret-pod
  namespace: kiwi
spec:
  containers:
    - name: busybox
      image: busybox
      command:
        - "sh"
        - "-c"
      args:
        - |
          mkdir -pv /var/log
          touch /var/log/msg.txt
          while true; do
            echo "$(date) $USERKIWI:$PASSKIWI" >> /var/log/msg.txt;
            sleep 10;
          done
```

```sh
k create ns kiwi
k apply -f task-secret-env.yaml
k get pod -n kiwi
```

---

- Solution

```sh
k create secret generic juicysecret --from-literal=username="kiwis" --from-literal=password="aredelicious" -n kiwi

k describe secret juicysecret -n kiwi
```

```yaml
# task-secret-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: kiwi-secret-pod
  namespace: kiwi
spec:
  containers:
    - name: busybox
      image: busybox
      env:
        - name: USERKIWI
          valueFrom:
            secretKeyRef:
              name: juicysecret
              key: username
        - name: PASSKIWI
          valueFrom:
            secretKeyRef:
              name: juicysecret
              key: password
      command:
        - "sh"
        - "-c"
      args:
        - |
          mkdir -pv /var/log
          touch /var/log/msg.txt
          while true; do
            echo "$(date) $USERKIWI:$PASSKIWI" >> /var/log/msg.txt;
            sleep 10;
          done
```

```sh
k replace --force -f task-secret-pod.yaml
```

---

## Scaling

### Task: VPA

Deploy a Vertical Pod Autoscaler (VPA) with name analytics-vpa for the deployment named analytics-deployment in the default namespace.
The VPA should automatically adjust the CPU and memory requests of the pods to optimize resource utilization. Ensure that the VPA operates in Recreate mode, allowing it to evict and recreate pods with updated resource requests as needed.

- Setup env

```sh
k create deploy analytics-deployment --image=nginx --replicas=2
```

---

- Solution

```yaml
# vpa.yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: analytics-vpa
  namespace: default
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: analytics-deployment
  updatePolicy:
    updateMode: "Recreate"
  resourcePolicy:
    containerPolicies:
      - containerName: "*"
        controlledResources: ["cpu", "memory"]
```

```sh
k apply -f vpa.yaml
# verticalpodautoscaler.autoscaling.k8s.io/analytics-vpa created

# confirm
k get vpa
# NAME            MODE       CPU   MEM   PROVIDED   AGE
# analytics-vpa   Recreate                          69s

k describe vpa analytics-vpa
# Name:         analytics-vpa
# Namespace:    default
# Labels:       <none>
# Annotations:  <none>
# API Version:  autoscaling.k8s.io/v1
# Kind:         VerticalPodAutoscaler
# Metadata:
#   Creation Timestamp:  2026-01-18T03:05:30Z
#   Generation:          1
#   Resource Version:    23967
#   UID:                 bfb69d0a-48b5-4088-ab5b-57ff131414b5
# Spec:
#   Resource Policy:
#     Container Policies:
#       Container Name:  *
#       Controlled Resources:
#         cpu
#         memory
#   Target Ref:
#     API Version:  apps/v1
#     Kind:         Deployment
#     Name:         analytics-deployment
#   Update Policy:
#     Update Mode:  Recreate
# Events:           <none>
```

---

### Task: Autoscaling

Deploy a sample workload and configure Horizontal Pod Autoscaling for it. Specifically:
. Use the existing deployment `cpu-demo'
. Configure an HPA to scale this deployment from 1 up to 5 replicas when the average CPU utilization exceeds 50%.

- Setup Environment

```sh
kubectl create deploy cpu-demo --image=busybox -- sleep infinity
```

---

- Solution

```sh
kubectl autoscale deploy/cpu-demo --min=1 --max=5 --cpu=50%
# horizontalpodautoscaler.autoscaling/cpu-demo autoscaled

kubectl get hpa
# NAME       REFERENCE             TARGETS              MINPODS   MAXPODS   REPLICAS   AGE
# cpu-demo   Deployment/cpu-demo   cpu: <unknown>/50%   1         5         1          84s

kubectl describe hpa cpu-demo
# Metrics:                                               ( current / target )
#   resource cpu on pods  (as a percentage of request):  <unknown> / 50%
# Min replicas:                                          1
# Max replicas:                                          5


```

---

### Task: HPA

Create a Horizontal Pod Autoscaler (HPA) with name webapp-hpa for the deployment named kkapp-deploy in the default namespace with the webapp-hpa.yaml file located under the root folder.
Ensure that the HPA scales the deployment based on CPU utilization, maintaining an average CPU usage of 50% across all pods.
Configure the HPA to cautiously scale down pods by setting a stabilization window of 300 seconds to prevent rapid fluctuations in pod count.

Note: The kkapp-deploy deployment is created for backend; you can check in the terminal.

- Setup env

```sh
k create deploy kkapp-deploy --image=nginx --replicas=2
```

---

- Solution

```yaml
# webapp-hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: webapp-hpa
  namespace: default
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: kkapp-deploy
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 50
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
```

```sh
k apply -f  /root/webapp-hpa.yaml
# horizontalpodautoscaler.autoscaling/webapp-hpa created

k describe hpa webapp-hpa
# Name:                                                  webapp-hpa
# Namespace:                                             default
# Labels:                                                <none>
# Annotations:                                           <none>
# CreationTimestamp:                                     Sat, 17 Jan 2026 21:41:01 -0500
# Reference:                                             Deployment/kkapp-deploy
# Metrics:                                               ( current / target )
#   resource cpu on pods  (as a percentage of request):  <unknown> / 50%
# Min replicas:                                          2
# Max replicas:                                          10
# Behavior:
#   Scale Up:
#     Stabilization Window: 0 seconds
#     Select Policy: Max
#     Policies:
#       - Type: Pods     Value: 4    Period: 15 seconds
#       - Type: Percent  Value: 100  Period: 15 seconds
#   Scale Down:
#     Stabilization Window: 300 seconds
#     Select Policy: Max
#     Policies:
#       - Type: Percent  Value: 100  Period: 15 seconds
# Deployment pods:       0 current / 0 desired
# Events:                <none>
```

---

### Task: HPA

Create a new HorizontalPodAutoscaler (HPA) named apache-server in the autoscale namespace. This HPA must target the existing Deployment called apache-server in the autoscale namespace.
Set the HPA to target for 50% CPU usage per Pod.
.
Configure hpa to have at min 1 Pod and no more than 4 Pods[max]. Also, we have to set the downscale stabilization window to 30 seconds.

- Setup env

```sh
kubectl create ns autoscale
kubectl create deploy apache-server --image=nginx -n autoscale

kubectl -n autoscale set resources deploy/apache-server --requests=cpu=100m,memory=64Mi --limits=cpu=200m,memory=128Mi
```

---

- Solution

```sh
kubectl autoscale deployment apache-server -n autoscale --cpu-percent=50 --min=1 --max=4 > hpa.yaml

vi hpa.yaml
# apiVersion: autoscaling/v2
# kind: HorizontalPodAutoscaler
# metadata:
#   name: apache-server
#   namespace: autoscale
# spec:
#   scaleTargetRef:
#     apiVersion: apps/v1
#     kind: Deployment
#     name: apache-server
#   minReplicas: 1
#   maxReplicas: 4
#   metrics:
#   - type: Resource
#     resource:
#       name: cpu
#       target:
#         type: Utilization
#         averageUtilization: 30
#   behavior:
#     scaleDown:
#       stabilizationWindowSeconds: 30

kubectl apply -f hpa.yaml
# horizontalpodautoscaler.autoscaling/apache-server created

# confirm
kubectl get hpa -n autoscale
# NAME            REFERENCE                  TARGETS              MINPODS   MAXPODS   REPLICAS   AGE
# apache-server   Deployment/apache-server   cpu: <unknown>/30%   1         4         1          2m4s

kubectl describe hpa apache-server -n autoscale
# Name:                                                  apache-server
# Namespace:                                             autoscale
# Labels:                                                <none>
# Annotations:                                           <none>
# CreationTimestamp:                                     Fri, 16 Jan 2026 19:39:03 -0500
# Reference:                                             Deployment/apache-server
# Metrics:                                               ( current / target )
#   resource cpu on pods  (as a percentage of request):  <unknown> / 30%
# Min replicas:                                          1
# Max replicas:                                          4
# Behavior:
#   Scale Up:
#     Stabilization Window: 0 seconds
#     Select Policy: Max
#     Policies:
#       - Type: Pods     Value: 4    Period: 15 seconds
#       - Type: Percent  Value: 100  Period: 15 seconds
#   Scale Down:
#     Stabilization Window: 30 seconds
#     Select Policy: Max
#     Policies:
#       - Type: Percent  Value: 100  Period: 15 seconds
# Deployment pods:       1 current / 0 desired
# Conditions:
#   Type           Status  Reason                   Message
#   ----           ------  ------                   -------
#   AbleToScale    True    SucceededGetScale        the HPA controller was able to get the target's current scale
#   ScalingActive  False   FailedGetResourceMetric  the HPA was unable to compute the replica count: failed to get cpu utilization: unable to get metrics for resource cpu: unable to fetch metrics from resource metrics API: the server could not find the requested resource (get pods.metrics.k8s.io)
# Events:
#   Type     Reason                        Age                From                       Message
#   ----     ------                        ----               ----                       -------
#   Warning  FailedGetResourceMetric       14s (x2 over 29s)  horizontal-pod-autoscaler  failed to get cpu utilization: unable to get metrics for resource cpu: unable to fetch metrics from resource metrics API: the server could not find the requested resource (get pods.metrics.k8s.io)
#   Warning  FailedComputeMetricsReplicas  14s (x2 over 29s)  horizontal-pod-autoscaler  invalid metrics (1 invalid out of 1), first error is: failed to get cpu resource metric value: failed to get cpu utilization: unable to get metrics for resource cpu: unable to fetch metrics from resource metrics API: the server could not find the requested resource (get pods.metrics.k8s.io)
```

---

## Helm

### Task: Install Argo

Install Argo CD in cluster:
Add the official Argo CD Helm repository with the name argo. url: https://argoproj.github.io/argo-helm
The Argo CD CRDs have already been pre-installed in the cluster.
Generate a helm template of the Argo CD Helm chart version 7.7.3 for the **argocd NS** and save to /argo-helm.yaml
Configure the chart to not install CRDs.
Install Argo CD using Helm with release name argocd using the same version as above and configuration as used in the template 7.7.3.
Install it in the argocd ns and configure it to not install CRDs.

You do not need to configure access to the Argo CD server UI.

---

- Solution

- https://argoproj.github.io/argo-helm/

```sh
# add repo
helm repo add argo https://argoproj.github.io/argo-helm
# "argo" has been added to your repositories

helm repo list
# NAME    URL
# argo    https://argoproj.github.io/argo-helm


helm search repo argo
# NAME                            CHART VERSION   APP VERSION     DESCRIPTION
# argo/argo                       1.0.0           v2.12.5         A Helm chart for Argo Workflows
# argo/argo-cd                    9.3.4           v3.2.5          A Helm chart for Argo CD, a declarative, GitOps...
# argo/argo-ci                    1.0.0           v1.0.0-alpha2   A Helm chart for Argo-CI
# ...

# update
helm repo update
# Hang tight while we grab the latest from your chart repositories...
# ...Successfully got an update from the "argo" chart repository
# Update Complete. ⎈Happy Helming!⎈

# create ns
kubectl create ns argocd
# namespace/argocd created

# render Helm chart templates locally
helm template myargocd argo/argo-cd -n argocd --version 7.7.3 --set crds.install=false > ./argo-helm.yaml

helm install argocd argo/argo-cd --version 7.7.3 --namespace argocd --set crds.install=false
# NAME: argocd
# LAST DEPLOYED: Fri Jan 16 16:00:11 2026
# NAMESPACE: argocd
# STATUS: deployed
# REVISION: 1
# DESCRIPTION: Install complete
# TEST SUITE: None
# NOTES:

# Verify
helm -n argocd list
# NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART             APP VERSION
# argocd  argocd          1               2026-01-16 16:00:11.919253784 -0500 EST deployed        argo-cd-7.7.3     v2.13.0

kubectl -n argocd get pods

```

---

### Task: Deploy with helm

Use Helm to deploy the Traefik Ingress Controller on the cluster. url: https://traefik.github.io/charts
Install it in a dedicated namespace traefik with release name traefik.
Ensure that Traefik's support for the Kubernetes Gateway API is enabled via Helm values.

---

Could be from a url, could be from local

- Solution

```sh
# add repo url
helm repo add traekfik https://traefik.github.io/charts
# "traekfik" has been added to your repositories

# update repo
helm repo update
# Update Complete. ⎈Happy Helming!⎈

# install
helm install traefik-app traefik/traefik -n traefik --create-namespace --set providers.kubernetesGateway.enabled=true
# NAME: traefik-app
# LAST DEPLOYED: Sat Jan 10 15:14:18 2026
# NAMESPACE: traefik
# STATUS: deployed
# REVISION: 1
# TEST SUITE: None
# NOTES:
# traefik-app with docker.io/traefik:v3.6.6 has been deployed successfully on traefik namespace!

# confirm
helm list -A
# NAME            NAMESPACE       REVISION        UPDATED                                STATUS          CHART           APP VERSION
# traefik-app     traefik         1               2026-01-10 15:14:18.847579643 -0500 ESTdeployed        traefik-38.0.2  v3.6.6

# confirm values
helm get values traefik-app -n traefik
# USER-SUPPLIED VALUES:
# experimental:
#   kubernetesGateway:
#     enabled: true
```

> Additional feature of a helm release depends on the values
> `helm show values REPO/RELEASE > app.yaml`: output values and find the value

---

### Task: Helm

CKA EXAM OBJECTIVE: Use Helm to install cluster components
Task:

1. Modify the Helm chart configuration located at ~/ckad-helm-task to ensure the deployment creates 3 replicas of a pod ...
2. ... then install the chart into the cluster.
3. The resources will be created in the battleofhelmsdeep namespace.

- Solution

```sh
# find the value "template/deployment.yaml"
# {{replicaCount}}

# install
helm install NAME ~/ckad-helm-task --set replicaCount=3 -n NAMESPACE
```

---

### Task: Upgrade Helm Release

One co-worker deployed an nginx helm chart kk-mock1 in the kk-ns namespace on the cluster. A new update is pushed to the helm chart, and the team wants you to update the helm repository to fetch the new changes.

After updating the helm chart, upgrade the helm chart version to 18.1.15.

```sh
# get existing release
helm ls -A
# NAME            NAMESPACE       REVISION        UPDATED                                      STATUS          CHART           APP VERSION
# kk-mock1        kk-ns           1               2026-01-17 23:10:53.002548969 +0000 UTC      deployed        nginx-18.1.0    1.27.0

# get existing repo
helm repo ls
# NAME            URL
# kk-mock1        https://charts.bitnami.com/bitnami

# update repo
helm repo update kk-mock1 -n kk-ns

# search for available charts
helm search repo kk-mock1/nginx -n kk-ns

# Upgrade the helm chart to 18.1.15
helm upgrade kk-mock1 kk-mock1/nginx -n kk-ns --version=18.1.15

# confirm
helm ls -n kk-ns
```

---

## Kustomize

### Task: Kustomize

You have base manifests for an app in ~/kustomize/base.
Use Kustomize to deploy a production variant of this app:

. The production variant should add the label environment: production to all resources.
. It should prefix resource names with `prod-'
. It should use Nginx image tag 1.21 instead of the base's 1.19

- Setup env

```sh
# base manifest
sudo mkdir -pv ~/kustomize/base

sudo vi ~/kustomize/base/deployment.yaml
# apiVersion: apps/v1
# kind: Deployment
# metadata:
#   name: hello-app
#   labels:
#     app: hello
# spec:
#   selector:
#     matchLabels:
#       app: hello
#   template:
#     metadata:
#       labels:
#         app: hello
#     spec:
#       containers:
#       - name: hello
#         image: nginx:1.19
#         ports:
#         - containerPort: 80

# create kustomization
sudo vi ~/kustomize/base/kustomization.yaml
resources:
- deployment.yaml
```

---

- Solution

- ref: https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/

```sh
# create overlay dir
sudo mkdir -pv ~/kustomize/overlay-prod
# mkdir: created directory '~/kustomize/overlay-prod'

# edit yaml
sudo vi ~/kustomize/overlay-prod/kustomization.yaml
# resources:
# - ../base

# namePrefix: prod-
# labels:
#   - pairs:
#       environment: production

# images:
# - name: nginx
#   newTag: "1.21"

# apply kustomize
kubectl apply -k ~/kustomize/overlay-prod/
# deployment.apps/prod-hello-app created

# confirm
kubectl get deploy
# NAME             READY   UP-TO-DATE   AVAILABLE   AGE
# prod-hello-app   1/1     1            1           25s

kubectl describe deploy prod-hello-app
# Name:                   prod-hello-app
# Labels:                 app=hello
#                         environment=production
# Pod Template:
#   Labels:  app=hello
#   Containers:
#    hello:
#     Image:         nginx:1.21
```

---

### Task: CRD

Task:

Verify the cert-manager application which has been deployed in the cluster.

Create a list of all cert-manager Custom Resource Definitions (CRDs) and save it to ~/resources.yaml. make sure kubectl's default output format and use kubectl to list CRD's

Do not set an output format.
Failure to do so will result in a reduced score.
Using kubectl, extract the documentation for the subject specification field of the Certificate Custom Resource and save it to ~/subject.vaml.
You may use any output format that kubecl supports.

---

- Solution:

```sh
kubectl get crd | grep cert-manager
kubectl get crd | grep cert-manager > ~/resources.yaml

kubectl explain certificate.spec.subject > ~/subject.yaml
kubectl explain certificate.spec.subject --format=plain > ~/subject.yaml
```

---

### Task: list CRDs

On controlplane node, identify all CRDs related to VerticalPodAutoscaler and save their names into the file /root/vpa-crds.txt.

---

- Solution:

```sh
k get crds -A | grep -i VerticalPodAutoscaler
# verticalpodautoscalercheckpoints.autoscaling.k8s.io   2026-01-17T22:26:07Z
# verticalpodautoscalers.autoscaling.k8s.io             2026-01-17T22:26:07Z

k get crds -A | grep -i VerticalPodAutoscaler > /root/vpa-crds.txt

# confirm
sudo cat /root/vpa-crds.txt
```

---

- Solution

```sh
# get the list of crd with app
kubectl get crds | grep cert-manager

# output the list
kubectl get crds | grep cert-manager > ~/resources.yaml

# confirm
cat ~/resources.yaml

# ################

# get the app Certificate
kubectl get crd | grep certificate

# get the document using explain
kubectl explain certificate.**.spec.subject

# output
kubectl explain certificate.**.spec.subject > ~/subject.vaml

cat ~/subject.vaml

```

---

## Resources

### Task: PriorityClass

Create a new `PriorityClass` named **high-priority** for user-workloads with a value that is one less than the highest existing **user-defined** `priority class` value.
Patch the existing `Deployment` **busybox-logger** running in the **priority1** `namespace` to use the **high-priority** `priority class`.
Ensure that the busybox-logger Deployment rolls out successfully with the **new** `priority class` set.
It is expected that Pods from other Deployments running in the priority namespace are evicted.
Do not modify other Deployments running in the priority namespace.
Failure to do so may result in a reduced score.

- Seteup environment

```sh
tee env-setup.yaml<<'EOF'
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: low-user
value: 1000
globalDefault: false
---
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: medium-user
value: 5000
globalDefault: false
---
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: top-user
value: 10000
globalDefault: false
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: existing-app
  namespace: priority1
spec:
  replicas: 6
  selector:
    matchLabels:
      app: existing-app
  template:
    metadata:
      labels:
        app: existing-app
    spec:
      priorityClassName: low-user
      containers:
      - name: stress
        image: busybox:1.36
        command: ["sh", "-c", "while true; do echo filler-low; sleep 5; done"]
        resources:
          requests:
            cpu: "250m"
            memory: "128Mi"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: busybox-logger
  namespace: priority1
spec:
  replicas: 1
  selector:
    matchLabels:
      app: busybox-logger
  template:
    metadata:
      labels:
        app: busybox-logger
    spec:
      containers:
      - name: busybox
        image: busybox:1.36
        command: ["sh", "-c", "while true; do echo $(date) busybox-logger; sleep 2; done"]
        resources:
          requests:
            cpu: "200m"
            memory: "128Mi"

EOF
kubectl create ns priority1
kubectl apply -f env-setup.yaml
# priorityclass.scheduling.k8s.io/low-user created
# priorityclass.scheduling.k8s.io/medium-user created
# priorityclass.scheduling.k8s.io/top-user created
# deployment.apps/busybox-logger created
# deployment.apps/existing-app created

kubectl get priorityclass
# NAME                      VALUE        GLOBAL-DEFAULT   AGE     PREEMPTIONPOLICY
# low-user                  1000         false            16s     PreemptLowerPriority
# medium-user               5000         false            16s     PreemptLowerPriority
# system-cluster-critical   2000000000   false            3d19h   PreemptLowerPriority
# system-node-critical      2000001000   false            3d19h   PreemptLowerPriority
# top-user                  10000        false            16s     PreemptLowerPriority
```

---

- Solution

```sh
# collect info
kubectl get priorityclass
# NAME                      VALUE        GLOBAL-DEFAULT   AGE     PREEMPTIONPOLICY
# low-user                  1000         false            16s     PreemptLowerPriority
# medium-user               5000         false            16s     PreemptLowerPriority
# system-cluster-critical   2000000000   false            3d19h   PreemptLowerPriority
# system-node-critical      2000001000   false            3d19h   PreemptLowerPriority
# top-user                  10000        false            16s     PreemptLowerPriority

kubectl get deploy -n priority1
# NAME             READY   UP-TO-DATE   AVAILABLE   AGE
# busybox-logger   0/1     1            0           21s
# existing-app     6/6     6            6           21s
```

```yaml
# pc.yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 9999
globalDefault: false
```

```sh
kubectl apply -f pc.yaml
# priorityclass.scheduling.k8s.io/high-priority created

# confirm
k get pc  --sort-by='value'
# NAME                      VALUE        GLOBAL-DEFAULT   AGE     PREEMPTIONPOLICY
# low-user                  1000         false            2m15s   PreemptLowerPriority
# medium-user               5000         false            2m15s   PreemptLowerPriority
# high-priority             9999         false            56s     PreemptLowerPriority
# top-user                  10000        false            2m15s   PreemptLowerPriority
# system-cluster-critical   2000000000   false            3d20h   PreemptLowerPriority
# system-node-critical      2000001000   false            3d20h   PreemptLowerPriority

# confirm no priority class
kubectl get deploy busybox-logger -n priority1 -o yaml

# scale down to 0
kubectl scale deploy busybox-logger -n priority1 --replicas=0
# deployment.apps/busybox-logger scaled

kubectl get deploy busybox-logger -n priority1
# NAME             READY   UP-TO-DATE   AVAILABLE   AGE
# busybox-logger   0/0     0            0           7m36s

kubectl patch deploy busybox-logger -n priority1 -p '{"spec":{"template":{"spec":{"priorityClassName":"high-priority"}}}}'
# deployment.apps/busybox-logger patched

# confirm
kubectl get deploy busybox-logger -n priority1 -o yaml
# spec:
#   template:
#     spec:
#       priorityClassName: high-priority

# scale out
kubectl scale deploy busybox-logger -n priority1 --replicas=1

# confirm
k get deploy -n priority1
# NAME             READY   UP-TO-DATE   AVAILABLE   AGE
# busybox-logger   1/1     1            1           6m32s
# existing-app     5/6     6            5           6m32s
```

---

### Task: Limit range

In the namespace limit-test, enforce default resource limits and requests for containers:
· If a container has no CPU/memory requests/limits, assign a default request of 100m CPU and 50Mi memory, and a default
limit of 200m CPU and 100Mi memory. . Prevent any container in this namespace from requesting more than 500Mi memory.

- Setup env

```sh
kubectl create ns limit-test
```

---

- Solution

- ref: https://kubernetes.io/docs/concepts/policy/limit-range/

```yaml
# task-limitrange.yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: resource-constraint
  namespace: limit-test
spec:
  limits:
    - type: Container
      default:
        cpu: 200m
        memory: 100Mi
      defaultRequest:
        cpu: 100m
        memory: 50Mi

    - type: Pod
      max:
        memory: 500Mi
```

```sh
kubectl apply -f task-limitrange.yaml
# limitrange/resource-constraint created

kubectl describe ns limit-test
# Name:         limit-test
# Labels:       kubernetes.io/metadata.name=limit-test
# Annotations:  <none>
# Status:       Active

# No resource quota.

# Resource Limits
#  Type       Resource  Min  Max    Default Request  Default Limit  Max Limit/Request Ratio
#  ----       --------  ---  ---    ---------------  -------------  -----------------------
#  Container  cpu       -    -      100m             200m           -
#  Container  memory    -    -      50Mi             100Mi          -
#  Pod        memory    -    500Mi  -                -              -
```

---

### Task: query resource usage

CKA EXAM OBJECTIVE: Monitor cluster and application resource usage
Task :

1. Identify all Pods in the integration namespace with the label app=intensive
2. Determine which of these Pods is using the most CPU resources
3. Write the name of the Pod consuming the most CPU resources to /tmp/cka/cpu_pod_01.txt

- Setup env

```sh
k create ns integration
k run intensive --image=busybox -l app=intensive -n integration -- sleep infinity
```

---

- Solution

```sh
k top pod -n integration -l app=intensive --sort-by='cpu'
```

---

### Task: Query pod 的 CPU

设置配置环境：
[candidate@node-1] $ kubectl config use-context k8s

Task
通过 pod label name=cpu-loader，找到运行时占用大量 CPU 的 pod，
并将占用 CPU 最高的 pod 名称写入文件 /tmp/cka/cpu-loader.txt（已存在）。Copy

- env

```sh
k create deploy cpu-loader --image=busybox --replicas=4 -- sleep infinity
k label pod -l app=cpu-loader name=cpu-loader
```

```sh
k get pod -l name=cpu-loader
# NAME                          READY   STATUS    RESTARTS   AGE
# cpu-loader-546f8f548c-jc4wf   1/1     Running   0          110s

kubectl top pod -l name=cpu-loader --sort-by=cpu -A
# NAMESPACE   NAME                          CPU(cores)   MEMORY(bytes)
# default     cpu-loader-546f8f548c-kmzzf   0m           0Mi
# default     cpu-loader-546f8f548c-pmn87   0m           0Mi
# default     cpu-loader-546f8f548c-wbfsx   0m           0Mi
# default     cpu-loader-546f8f548c-xxb7x   0m           0Mi
```

---

### Task: Resources

Task

A WordPress application with 3 replicas in the relative-fawn namespace consists of: cpu 1 memory 2015360ki

Adjust all Pod resource requests as follows:
Divide node resources evenly across all 3 pods.
Give each Pod a fair share of CPU and memory.
Add enough overhead to keep the node stable.
Use the exact same requests for both containers and init containers.

You are not required to change any resource limits.
It may help to temporarily scale the WordPress Deployment to 0 replicas while updating the resource requests.

- After updates, confirm:
  - WordPress keeps 3 replicas.
  - All Pods are running and ready.

- Setup Env

```sh
kubectl label node node02 wpnode=true
kubectl create ns relative-fawn

tee env-deploy.yaml<<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: wordpress
  namespace: relative-fawn
spec:
  replicas: 3
  selector:
    matchLabels:
      app: wordpress
  template:
    metadata:
      labels:
        app: wordpress
    spec:
      nodeSelector:
        wpnode: "true"
      initContainers:
      - name: init-container
        image: busybox
        command: ["sh", "-c", "sleep 30"]
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
EOF

kubectl apply -f env-deploy.yaml
```

- Solution
  - find the node where the app is scheduled, find the capacity: cpu+memory
  - caculate:
    - save 25% for system
    - 75% / 3 =25% total cpu

```sh
# find the
kubectl -n relative-fawn get pod -o wide
# NAME                         READY   STATUS    RESTARTS   AGE     IP            NODE     NOMINATED NODE   READINESS GATES
# wordpress-6b77fdbd49-6gd4q   1/1     Running   0          5m19s   10.244.2.22   node02   <none>           <none>
# wordpress-6b77fdbd49-8d2qh   1/1     Running   0          5m19s   10.244.2.23   node02   <none>           <none>
# wordpress-6b77fdbd49-hkw7z   1/1     Running   0          5m19s   10.244.2.24   node02   <none>           <none>

# get the resource
kubectl describe node node02
# Capacity:
#   cpu:                1
#   ephemeral-storage:  30784420Ki
#   hugepages-1Gi:      0
#   hugepages-2Mi:      0
#   memory:             1965484Ki
```

- Caculation:
  - 1000m \* (1-25%) = 750
  - 750/3 = 250m
  - 2Gi \* (1-25%) = 1500Mi
  - 1500Mi / 3 = 500Mi

```sh
# scale down
kubectl scale deploy wordpress -n relative-fawn --replicas=0

k get deploy -n relative-fawn
# NAME        READY   UP-TO-DATE   AVAILABLE   AGE
# wordpress   0/0     0            0           13m

# update resource
k edit deploy wordpress -n relative-fawn

# confirm
k get deploy wordpress -n relative-fawn -o yaml
# containers:
#   name: nginx
#   resources:
#     requests:
#       cpu: 250m
#       memory: 800Mi
# initContainers:
#   name: init-container
#   resources:
#     requests:
#       cpu: 250m
#       memory: 800Mi

# scale out
kubectl scale deploy wordpress -n relative-fawn --replicas=3

# confirm
k get deploy wordpress -n relative-fawn
# NAME        READY   UP-TO-DATE   AVAILABLE   AGE
# wordpress   3/3     3            3           9m35s
```

---
