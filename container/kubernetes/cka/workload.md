# CKA - Workload

[Back](../index.md)

- [CKA - Workload](#cka---workload)
  - [POD, Deployment, STS](#pod-deployment-sts)
    - [Task: Pod - Log](#task-pod---log)
    - [Task: Pod - log](#task-pod---log-1)
    - [Task: Pod - Multiple Containers](#task-pod---multiple-containers)
    - [Task: Pod - multiple container](#task-pod---multiple-container)
    - [Task: Pod - Sidecar Pod](#task-pod---sidecar-pod)
    - [Task: Pod - volume + sidecar](#task-pod---volume--sidecar)
    - [Task: Deployment - scale](#task-deployment---scale)
    - [Task: Deployment - scale](#task-deployment---scale-1)
    - [Task: Deployment Rollback](#task-deployment-rollback)
    - [Task: StatefulSets \& Headless Services](#task-statefulsets--headless-services)
  - [ConfigMap \& Secret](#configmap--secret)
    - [Task: ConfigMap](#task-configmap)
    - [Task: ConfigMaps \& Secrets](#task-configmaps--secrets)
  - [HPA](#hpa)
    - [Task: Autoscaling](#task-autoscaling)
  - [Helm](#helm)
    - [Task: Deploy with helm](#task-deploy-with-helm)
    - [Task: Helm](#task-helm)
  - [Kustomize](#kustomize)
    - [Task: Kustomize](#task-kustomize)
  - [Resources](#resources)
    - [Task: Limit range](#task-limit-range)
    - [Task: query resource usage](#task-query-resource-usage)
    - [Task: Query pod 的 CPU](#task-query-pod-的-cpu)

---

## POD, Deployment, STS

### Task: Pod - Log

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

### Task: Pod - log

1. monitor the log of the fnf pod and filter any lines containing the error file-not-found.
2. /opt/cka/answers/sorted_log.log

---

- Solution

```sh
k get pod fnf

k logs fnf | grep "file-not-found" > /opt/cka/answers/sorted_log.log
```

---

### Task: Pod - Multiple Containers

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

### Task: Deployment - scale

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
k get deploy -n king-of-lions --record "version 1"
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

## ConfigMap & Secret

### Task: ConfigMap

CKA EXAM OBJECTIVE: Use ConfigMaps and Secrets to configure applications
Task :

1. Create a ConfigMap called metal-cm containing the file ~/index.html
2. To the deployment "enter-sandman" add the metal-cm configmap mounted to the path /var/www/index.html
3. Create the deployment in the metallica Namespace.

- setup env

```sh
tee ~/cka/workload/index.html<<EOF
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

## HPA

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

## Helm

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
helm install traefik-app traefik/traefik -n traefik --create-namespace --set experimental.kubernetesGateway.enabled=true
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

## Kustomize

### Task: Kustomize

You have base manifests for an app in /home/student/kustomize/base.
Use Kustomize to deploy a production variant of this app:

. The production variant should add the label environment: production to all resources.
. It should prefix resource names with `prod-'
. It should use Nginx image tag 1.21 instead of the base's 1.19

- Setup env

```sh
# base manifest
sudo mkdir -pv /home/student/kustomize/base

sudo vi /home/student/kustomize/base/deployment.yaml
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
sudo vi /home/student/kustomize/base/kustomization.yaml
resources:
- deployment.yaml
```

---

- Solution

- ref: https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/

```sh
# create overlay dir
sudo mkdir -pv /home/student/kustomize/overlay-prod
# mkdir: created directory '/home/student/kustomize/overlay-prod'

# edit yaml
sudo vi /home/student/kustomize/overlay-prod/kustomization.yaml
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
kubectl apply -k /home/student/kustomize/overlay-prod/
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

## Resources

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
3. Write the name of the Pod consuming the most CPU resources to /opt/cka/answers/cpu_pod_01.txt

- Setup env

```sh
k create ns integration
k run intensive --image=busybox -l app=intensive -n integration -- sleep infinity
```

---

- Solution

```sh
k top pod -l app=intensive --sort-by cpu


```

---

### Task: Query pod 的 CPU

设置配置环境：
[candidate@node-1] $ kubectl config use-context k8s

Task
通过 pod label name=cpu-loader，找到运行时占用大量 CPU 的 pod，
并将占用 CPU 最高的 pod 名称写入文件 /opt/KUTR000401/KUTR00401.txt（已存在）。Copy

```sh
kubectl top pod -l name=cpu-loader --sort-by=cpu -A
```

---
