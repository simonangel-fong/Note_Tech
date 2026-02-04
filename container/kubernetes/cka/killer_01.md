# killer01

[Back](../index.md)

- [killer01](#killer01)
  - [!!Q1: config - miss](#q1-config---miss)
  - [Q2: helm](#q2-helm)
  - [Q3: scale out](#q3-scale-out)
  - [!!Q4: resource - gap](#q4-resource---gap)
  - [!!Q5: kustomize - gap](#q5-kustomize---gap)
  - [Q6: pv, pvc, deploy](#q6-pv-pvc-deploy)
  - [!!!Q7: top - miss](#q7-top---miss)
  - [!!!Q8: upgrade - miss](#q8-upgrade---miss)
  - [!Q9: sa, api - gap](#q9-sa-api---gap)
  - [Q10: sa, role](#q10-sa-role)
  - [Q11: ds, resources](#q11-ds-resources)
  - [!Q12: sidecar, pod anti-a - gap](#q12-sidecar-pod-anti-a---gap)
  - [!!Q13: gateway - no try](#q13-gateway---no-try)
  - [!!Q14: openssl,certs - gap](#q14-opensslcerts---gap)
  - [!!Q15: netpol - miss](#q15-netpol---miss)
  - [!!Q16: coredns, cm - gap](#q16-coredns-cm---gap)
  - [!Q17: crictl - miss](#q17-crictl---miss)
  - [Preivew 01: manifest, openssl](#preivew-01-manifest-openssl)
    - [!Preview 02: svc, iptables - gap](#preview-02-svc-iptables---gap)
    - [!!Preview 03: service, cidr - gap](#preview-03-service-cidr---gap)

---

## !!Q1: config - miss

Solve this question on: ssh cka9412

You're asked to extract the following information out of kubeconfig file /opt/course/1/kubeconfig on cka9412:

Write all kubeconfig context names into /opt/course/1/contexts, one per line

Write the name of the current context into /opt/course/1/current-context

Write the client-certificate of user account-0027 base64-decoded into /opt/course/1/cert

---

- Solution:

```sh
# 1
kubectl --kubeconfig=/opt/course/1/kubeconfig config get-contexts -o name

# 2
kubectl --kubeconfig=/opt/course/1/kubeconfig config current-context

# 3
echo crt | base64 -d > /opt/course/1/cert
```

---

## Q2: helm

Solve this question on: ssh cka7968

Install the MinIO Operator using Helm in Namespace minio. Then configure and create the Tenant CRD:

Create Namespace minio

Install Helm chart minio/operator into the new Namespace. The Helm Release should be called minio-operator

Update the Tenant resource in /opt/course/2/minio-tenant.yaml to include enableSFTP: true under features

Create the Tenant resource from /opt/course/2/minio-tenant.yaml

ℹ️ It is not required for MinIO to run properly. Installing the Helm Chart and the Tenant resource as requested is enough

---

- Solution

```sh
# 1
kubectl create namespace minio

# 2
helm repo list
helm search repo
helm install minio-operator minio/operator -n minio
# confirm
helm -n minio list
kubectl -n minio get pods

#2
vi /opt/course/2/minio-tenant.yaml
# features:
#   enableSFTP: true

kubectl apply -f /opt/course/2/minio-tenant.yaml

# confirm
kubectl -n minio get tenant
```

---

## Q3: scale out

Solve this question on: ssh cka3962

There are two Pods named o3db-\* in Namespace project-h800. The Project H800 management asked you to scale these down to one replica to save resources.

---

```sh
kubectl -n project-h800 get pod

# confirm sts
k -n project-h800 get deploy,ds,sts | grep o3db
# confirm label is correct
 k -n project-h800 get pod --show-labels | grep o3db

k scale sts o3db --replicas=1


```

---

## !!Q4: resource - gap

Solve this question on: ssh cka2556

Check all available Pods in the Namespace project-c13 and find the names of those that would probably be terminated first if the nodes run out of resources (cpu or memory).

Write the Pod names into /opt/course/4/pods-terminated-first.txt.

---

- Solution:

- 考察点：
  - 不是实际使用，
  - 而是po.resources, 如果po没有声明resources，则在资源紧张时，先下线。

```sh
# 方法1
k describe po -n project-c13 | less
# 手动查看没有声明resources

# 方法2：利用describe node 列出所有pod，然后帅选
k describe node | grep project-c13 | grep (0%)

```

---

## !!Q5: kustomize - gap

Solve this question on: ssh cka5774

Previously the application api-gateway used some external autoscaler which should now be replaced with a HorizontalPodAutoscaler (HPA). The application has been deployed to Namespaces api-gateway-staging and api-gateway-prod like this:

kubectl kustomize /opt/course/5/api-gateway/staging | kubectl apply -f -
kubectl kustomize /opt/course/5/api-gateway/prod | kubectl apply -f -
Using the Kustomize config at /opt/course/5/api-gateway do the following:

Remove the ConfigMap horizontal-scaling-config completely
Add HPA named api-gateway for the Deployment api-gateway with min 2 and max 4 replicas. It should scale at 50% average CPU utilisation
In prod the HPA should have max 6 replicas
Apply your changes for staging and prod so they're reflected in the cluster

---

- Solution

```sh
cd /opt/course/5/api-gateway

ls
# base  prod  staging

# investigate the base dir: namespace is customized
k kustomize base
# metadata:
#   name: api-gateway
#   namespace: NAMESPACE_REPLACE

# investigate the staging dir: override namespace
k kustomize staging
# metadata:
#   name: api-gateway
#   namespace: api-gateway-staging

# investigate the prod dir: namespace is override
k kustomize prod
# metadata:
#   name: api-gateway
#   namespace: api-gateway-prod

# task:  remove the ConfigMap from base, staging and prod
vi base/api-gateway.yaml
vi staging/api-gateway.yaml
vi prod/api-gateway.yaml

# in base, add the requested HPA
vi base/api-gateway.yaml
# apiVersion: autoscaling/v2
# kind: HorizontalPodAutoscaler
# metadata:
#   name: api-gateway
# spec:
#   scaleTargetRef:
#     apiVersion: apps/v1
#     kind: Deployment
#     name: api-gateway
#   minReplicas: 2
#   maxReplicas: 4
#   metrics:
#     - type: Resource
#       resource:
#         name: cpu
#         target:
#           type: Utilization
#           averageUtilization: 50

# In prod, max replicas set to 6
vi prod/api-gateway.yaml
# apiVersion: autoscaling/v2
# kind: HorizontalPodAutoscaler
# metadata:
#   name: api-gateway
# spec:
#   maxReplicas: 6

# apply the changes
k kustomize staging | kubectl apply -f -
k kustomize prod | kubectl apply -f -

# delete the remote ConfigMaps manually
k -n api-gateway-staging delete cm
# confirm
k -n api-gateway-prod get cm
```

---

## Q6: pv, pvc, deploy

Solve this question on: ssh cka7968

Create a new PersistentVolume named safari-pv. It should have a capacity of 2Gi, accessMode ReadWriteOnce, hostPath /Volumes/Data and no storageClassName defined.

Next create a new PersistentVolumeClaim in Namespace project-t230 named safari-pvc . It should request 2Gi storage, accessMode ReadWriteOnce and should not define a storageClassName. The PVC should bound to the PV correctly.

Finally create a new Deployment safari in Namespace project-t230 which mounts that volume at /tmp/safari-data. The Pods of that Deployment should be of image httpd:2-alpine.

---

- solution:

```sh
tee q06.yaml<<EOF
kind: PersistentVolume
apiVersion: v1
metadata:
 name: safari-pv
spec:
 capacity:
  storage: 2Gi
 accessModes:
  - ReadWriteOnce
 hostPath:
  path: "/Volumes/Data"
---
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: safari-pvc
  namespace: project-t230
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
     storage: 2Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: safari
  name: safari
  namespace: project-t230
spec:
  replicas: 1
  selector:
    matchLabels:
      app: safari
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: safari
    spec:
      volumes:                                      # add
      - name: data                                  # add
        persistentVolumeClaim:                      # add
          claimName: safari-pvc                     # add
      containers:
      - image: httpd:2-alpine
        name: container
        volumeMounts:                               # add
        - name: data                                # add
          mountPath: /tmp/safari-data               # add
EOF

k apply -f 6_dep.yaml

# confirm
k -n project-t230 describe pod safari-b499cc5b9-x7d7h | grep -A2 Mounts:
```

---

## !!!Q7: top - miss

Solve this question on: ssh cka5774

The metrics-server has been installed in the cluster. Write two bash scripts which use kubectl:

Script /opt/course/7/node.sh should show resource usage of nodes
Script /opt/course/7/pod.sh should show resource usage of Pods and their containers

---

- Solution:
- !!! **Pods and their containers**

```sh
sudo echo "kubectl top node" > /opt/course/7/node.sh

sudo echo "kubectl top pod --containers=true" > /opt/course/7/pod.sh

```

---

## !!!Q8: upgrade - miss

Solve this question on: ssh cka3962

Your coworker notified you that node cka3962-node1 is running an older Kubernetes version and is not even part of the cluster yet.

Update the node's Kubernetes to the exact version of the controlplane

Add the node to the cluster using kubeadm

ℹ️ You can connect to the worker node using ssh cka3962-node1 from cka3962

---

- solution
- 未加入集群时，kubelet是不启动的
- 思路：
  - 确认adm,let,ctl 版本
  - 升级
  - join
  - 确认

```sh
ssh cka3962

# get kubeadm version: v1.34.1
k get node
# NAME      STATUS   ROLES           AGE   VERSION
# cka3962   Ready    control-plane   19h   v1.34.1

ssh cka3962-node1
sudo -i

# ##############################
# confirm kubectl kubelet kubeadm
# ##############################
# get
kubectl version
# Client Version: v1.33.5
# Kustomize Version: v5.6.0

kubelet --version
# Kubernetes v1.33.5

# already installed v1.34.1
kubeadm version
# kubeadm version: &version.Info{Major:"1", Minor:"34", EmulationMajor:"", EmulationMinor:"", MinCompatibilityMajor:"", MinCompatibilityMinor:"", GitVersion:"v1.34.1", GitCommit:"93248f9ae092f571eb870b7664c534bfc7d00f03", GitTreeState:"clean", BuildDate:"2025-09-09T19:43:15Z", GoVersion:"go1.24.6", Compiler:"gc", Platform:"linux/amd64"}

# command responde: this node is not yet part of the cluster. Hence there is nothing to update.
kubeadm upgrade node
# error: couldn't create a Kubernetes client from file "/etc/kubernetes/kubelet.conf": failed to load admin kubeconfig: open /etc/kubernetes/kubelet.conf: no such file or directory
# To see the stack trace of this error execute with --v=5 or higher

# ##############################
# update kubectl kubelet
# ##############################
apt update

# get available version
sudo apt-cache madison kubectl kubelet

apt-get install kubectl='1.34.1-1.1' kubelet='1.34.1-1.1'

kubectl version

kubelet --version
# Kubernetes v1.34.1

# ##############################
# restart kubelet
# ##############################
systemctl restart kubelet
systemctl status kubelet


# ##############################
# join worker node
# ##############################
ssh cka3962

kubeadm token create --print-join-command


ssh cka3962-node1
kubeadm join

# confirm kubelet is active
systemctl status kubelet
# ● kubelet.service - kubelet: The Kubernetes Node Agent
#  Active: active (running) since Fri 2025-09-19 13:15:32 UTC; 13s ago

ssh cka3962
k get node
# NAME            STATUS   ROLES           AGE   VERSION
# cka3962         Ready    control-plane   19h   v1.34.1
# cka3962-node1   Ready    <none>          24s   v1.34.1
```

---

## !Q9: sa, api - gap

Solve this question on: ssh cka9412

There is ServiceAccount secret-reader in Namespace project-swan. Create a Pod of image nginx:1-alpine named api-contact which uses this ServiceAccount.

Exec into the Pod and use curl to manually query all Secrets from the Kubernetes Api.

Write the result into file /opt/course/9/result.json.

---

- solution:
- https://kubernetes.io/docs/tasks/run-application/access-api-from-pod/

```sh
k create ns project-swan
k get sa -n project-swan

k run api-contact --image=nginx:1-alpine -n project-swan
k set sa po api-contact secret-reader -n project-swan
k describe po api-contact -n project-swan | grep -i account

# curl in pod
k ex
APISERVER=https://kubernetes.default.svc

# Path to ServiceAccount token
SERVICEACCOUNT=/var/run/secrets/kubernetes.io/serviceaccount

# Read this Pod's namespace
NAMESPACE=$(cat ${SERVICEACCOUNT}/namespace)

# Read the ServiceAccount bearer token
TOKEN=$(cat ${SERVICEACCOUNT}/token)

# Reference the internal certificate authority (CA)
CACERT=${SERVICEACCOUNT}/ca.crt

# Explore the API with TOKEN
curl --cacert ${CACERT} --header "Authorization: Bearer ${TOKEN}" -X GET ${APISERVER}/api/v1/secrets
```

---

## Q10: sa, role

Solve this question on: ssh cka3962

Create a new ServiceAccount processor in Namespace project-hamster. Create a Role and RoleBinding, both named processor as well. These should allow the new SA to only create Secrets and ConfigMaps in that Namespace.

---

- Solution:

```sh
k -n project-hamster create sa processor
k -n project-hamster create role processor --verb=create --resource=secret --resource=configmap
k -n project-hamster create rolebinding processor --role processor --serviceaccount project-hamster:processor
```

---

## Q11: ds, resources

Solve this question on: ssh cka2556

Use Namespace project-tiger for the following. Create a DaemonSet named ds-important with image httpd:2-alpine and labels id=ds-important and uuid=18426a0b-5f59-4e10-923f-c0e078e82462. The Pods it creates should request 10 millicore cpu and 10 mebibyte memory. The Pods of that DaemonSet should run on all nodes, also controlplanes.

---

- solution

```sh
k -n project-tiger create deployment --image=httpd:2.4-alpine ds-important --dry-run=client -o yaml > q11.yaml

tee > q11.yaml<<EOF
apiVersion: apps/v1
kind: DaemonSet                                     # change from Deployment to Daemonset
metadata:
  creationTimestamp: null
  labels:                                           # add
    id: ds-important                                # add
    uuid: 18426a0b-5f59-4e10-923f-c0e078e82462      # add
  name: ds-important
  namespace: project-tiger                          # important
spec:
  selector:
    matchLabels:
      id: ds-important                              # add
      uuid: 18426a0b-5f59-4e10-923f-c0e078e82462    # add
  template:
    metadata:
      labels:
        id: ds-important                            # add
        uuid: 18426a0b-5f59-4e10-923f-c0e078e82462  # add
    spec:
      containers:
      - image: httpd:2-alpine
        name: ds-important
        resources:
          requests:                                 # add
            cpu: 10m                                # add
            memory: 10Mi                            # add
      tolerations:                                  # add
      - effect: NoSchedule                          # add
        key: node-role.kubernetes.io/control-plane  # add
EOF

k create -f q11.yaml

k get pod -l id=ds-important -o wide -n project-tiger
```

---

## !Q12: sidecar, pod anti-a - gap

Solve this question on: ssh cka2556

Implement the following in Namespace project-tiger:

Create a Deployment named deploy-important with 3 replicas
The Deployment and its Pods should have label id=very-important
First container named container1 with image nginx:1-alpine
Second container named container2 with image google/pause
There should only ever be one Pod of that Deployment running on one worker node, use topologyKey: kubernetes.io/hostname for this
ℹ️ Because there are two worker nodes and the Deployment has three replicas the result should be that the third Pod won't be scheduled. In a way this scenario simulates the behaviour of a DaemonSet, but using a Deployment with a fixed number of replicas

---

- Solution
- one pod per node: `podAntiAffinity` label == self label

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    id: very-important # change
  name: deploy-important
  namespace: project-tiger # important
spec:
  replicas: 3 # change
  selector:
    matchLabels:
      id: very-important # change
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        id: very-important # change
    spec:
      containers:
        - image: nginx:1-alpine
          name: container1 # change
          resources: {}
        - image: google/pause # add
          name: container2 # add
      affinity: # add
        podAntiAffinity: # add
          requiredDuringSchedulingIgnoredDuringExecution: # add
            - labelSelector: # add
                matchExpressions: # add
                  - key: id # add
                    operator: In # add
                    values: # add
                      - very-important # add
              topologyKey: kubernetes.io/hostname # add
```

---

## !!Q13: gateway - no try

Solve this question on: ssh cka7968

The team from Project r500 wants to replace their Ingress (networking.k8s.io) with a Gateway Api (gateway.networking.k8s.io) solution. The old Ingress is available at /opt/course/13/ingress.yaml.

Perform the following in Namespace project-r500 and for the already existing Gateway:

Create a new HTTPRoute named traffic-director which replicates the routes from the old Ingress
Extend the new HTTPRoute with path /auto which forwards to mobile backend if the User-Agent is exactly mobile and to desktop backend otherwise
The existing Gateway is reachable at http://r500.gateway:30080 which means your implementation should work for these commands:

curl r500.gateway:30080/desktop
curl r500.gateway:30080/mobile
curl r500.gateway:30080/auto -H "User-Agent: mobile"
curl r500.gateway:30080/auto

---

- solution
- 读懂题目
  - mobile -> mobile
  - dt -> dt
  - auto + m -> mobile
  - auto -> dt
- 多条件

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: traffic-director
  namespace: project-r500
spec:
  parentRefs:
    - name: main
  hostnames:
    - "r500.gateway"
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /desktop
      backendRefs:
        - name: web-desktop
          port: 80
    - matches:
        - path:
            type: PathPrefix
            value: /mobile
      backendRefs:
        - name: web-mobile
          port: 80
    # NEW FROM HERE ON
    - matches:
        - path:
            type: PathPrefix
            value: /auto
          headers:
            - type: Exact
              name: user-agent
              value: mobile
      backendRefs:
        - name: web-mobile
          port: 80
    - matches:
        - path:
            type: PathPrefix
            value: /auto
      backendRefs:
        - name: web-desktop
          port: 80
```

---

## !!Q14: openssl,certs - gap

Solve this question on: ssh cka9412

Perform some tasks on cluster certificates:

Check how long the kube-apiserver server certificate is valid using openssl or cfssl. Write the expiration date into /opt/course/14/expiration.

Run the kubeadm command to list the expiration dates and confirm both methods show the same one
Write the kubeadm command that would renew the kube-apiserver certificate into /opt/course/14/kubeadm-renew-certs.sh

---

- Solution

```sh
# find pki
ls /etc/kubernetes/pki/apiserver.crt
# /etc/kubernetes/pki/apiserver.crt

openssl x509 -noout -text -in /etc/kubernetes/pki/apiserver.crt | grep Validity -A2
# Validity
#     Not Before: Jan 17 04:55:56 2026 GMT
#     Not After : Jan 17 05:00:56 2027 GMT

sudo echo "Jan 17 05:00:56 2027" > /opt/course/14/expiration


sudo kubeadm certs check-expiration | grep api
# apiserver                  Jan 17, 2027 05:00 UTC   348d            ca                      no

kubeadm certs renew apiserver
```

---

## !!Q15: netpol - miss

Solve this question on: ssh cka7968

There was a security incident where an intruder was able to access the whole cluster from a single hacked backend Pod.

To prevent this create a NetworkPolicy called np-backend in Namespace project-snake. It should allow the backend-\* Pods only to:

Connect to db1-_ Pods on port 1111
Connect to db2-_ Pods on port 2222
Use the app Pod labels in your policy.

ℹ️ All Pods in the Namespace run plain Nginx images. This allows simple connectivity tests like: k -n project-snake exec POD_NAME -- curl POD_IP:PORT

ℹ️ For example, connections from backend-_ Pods to vault-_ Pods on port 3333 should no longer work

---

- Solution:
  - check target label
  - check allow label
  - identify what rule
  - identify how many rules
  - identify and/or rules
  - identify port

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: np-backend
  namespace: project-snake
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
    - Egress # policy is only about Egress
  egress:
    - # first rule
      to: # first condition "to"
        - podSelector:
            matchLabels:
              app: db1
      ports: # second condition "port"
        - protocol: TCP
          port: 1111
    - # second rule
      to: # first condition "to"
        - podSelector:
            matchLabels:
              app: db2
      ports: # second condition "port"
        - protocol: TCP
          port: 2222
```

---

## !!Q16: coredns, cm - gap

Solve this question on: ssh cka5774

The CoreDNS configuration in the cluster needs to be updated:

Make a backup of the existing configuration Yaml and store it at /opt/course/16/coredns_backup.yaml. You should be able to fast recover from the backup
Update the CoreDNS configuration in the cluster so that DNS resolution for SERVICE.NAMESPACE.custom-domain will work exactly like and in addition to SERVICE.NAMESPACE.cluster.local
Test your configuration for example from a Pod with busybox:1 image. These commands should result in an IP address:

nslookup kubernetes.default.svc.cluster.local
nslookup kubernetes.default.svc.custom-domain

---

- solution

```sh
k -n kube-system get cm coredns -o yaml > /opt/course/16/coredns_backup.yaml

k -n kube-system edit cm coredns
# find:
# kubernetes cluster.local in-addr.arpa ip6.arpa {
# replace:
# kubernetes cluster.local custom-domain in-addr.arpa ip6.arpa {

k -n kube-system rollout restart deploy coredns

k run test --rm -it --image=busybox:1 --restart=Never -- sh -c "nslookup kubernetes.default.svc.cluster.local; nslookup kubernetes.default.svc.custom-domain"
# Server:         10.96.0.10
# Address:        10.96.0.10:53

# Name:   kubernetes.default.svc.cluster.local
# Address: 10.96.0.1


# Server:         10.96.0.10
# Address:        10.96.0.10:53

# Name:   kubernetes.default.svc.custom-domain
# Address: 10.96.0.1


# pod "test" deleted
```

---

## !Q17: crictl - miss

Solve this question on: ssh cka2556

In Namespace project-tiger create a Pod named tigers-reunite of image httpd:2-alpine with labels pod=container and container=pod. Find out on which node the Pod is scheduled. Ssh into that node and find the containerd container belonging to that Pod.

Using command crictl:

Write the ID of the container and the info.runtimeType into /opt/course/17/pod-container.txt

Write the logs of the container into /opt/course/17/pod-container.log

ℹ️ You can connect to a worker node using ssh cka2556-node1 or ssh cka2556-node2 from cka2556

---

- solution:

```sh
# create po
k -n project-tiger run tigers-reunite --image=httpd:2-alpine --labels "pod=container,container=pod"

# find node
k -n project-tiger get pod -o wide

ssh cka2556-node1

sudo -i
# get con id
crictl ps --name tigers-reunite

# get runtime
crictl inspect ba62e5d465ff0 | grep runtimeType

```

---

## Preivew 01: manifest, openssl

Preview Question 1 | ETCD Information
Solve this question on: ssh cka9412

The cluster admin asked you to find out the following information about etcd running on cka9412:

Server private key location
Server certificate expiration date
Is client certificate authentication enabled
Write these information into /opt/course/p1/etcd-info.txt

---

- Solution:

```sh
# check etcd pod: etcd using static po
k -n kube-system get pod
# NAME                              READY   STATUS    RESTARTS     AGE
# etcd-cka9412                      1/1     Running   0            9d

# query etcd manifest
sudo cat /etc/kubernetes/manifests/etcd.yaml
    # - --cert-file=/etc/kubernetes/pki/etcd/server.crt
    # - --client-cert-auth=true
    # - --key-file=/etc/kubernetes/pki/etcd/server.key

# get expired day:
openssl x509  -noout -text -in /etc/kubernetes/pki/etcd/server.crt
        # Validity
        #     Not Before: Oct 29 14:14:27 2024 GMT
        #     Not After : Oct 29 14:19:27 2025 GMT

vi /opt/course/p1/etcd-info.txt
# Server private key location: /etc/kubernetes/pki/etcd/server.key
# Server certificate expiration date: Oct 29 14:19:27 2025 GMT
# Is client certificate authentication enabled: yes
```

---

### !Preview 02: svc, iptables - gap

Solve this question on: ssh cka3962

You're asked to confirm that kube-proxy is running correctly. For this perform the following in Namespace project-hamster:

Create Pod p2-pod with image nginx:1-alpine

Create Service p2-service which exposes the Pod internally in the cluster on port 3000->80

Write the iptables rules of node cka3962 belonging the created Service p2-service into file /opt/course/p2/iptables.txt

Delete the Service and confirm that the iptables rules are gone again

---

- Solution:

```sh
# create pod
k -n project-hamster run p2-pod --image=nginx:1-alpine

# create svc
k -n project-hamster expose pod p2-pod --name p2-service --port 3000 --target-port 80

# on every node
iptables-save | grep p2-service

```

---

### !!Preview 03: service, cidr - gap

Preview Question 3 | Change Service CIDR
Solve this question on: ssh cka9412

Create a Pod named check-ip in Namespace default using image httpd:2-alpine

Expose it on port 80 as a ClusterIP Service named check-ip-service. Remember/output the IP of that Service

Change the Service CIDR to 11.96.0.0/12 for the cluster

Create a second Service named check-ip-service2 pointing to the same Pod

ℹ️ The second Service should get an IP address from the new CIDR range

---

- solution:

```sh
k run check-ip --image=httpd:2-alpine

k get svc
# NAME               TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
# check-ip-service   ClusterIP   10.97.6.41   <none>        80/TCP    3s

vim /etc/kubernetes/manifests/kube-apiserver.yaml
# - --service-cluster-ip-range=11.96.0.0/12             # change

vim /etc/kubernetes/manifests/kube-controller-manager.yaml
# - --service-cluster-ip-range=11.96.0.0/12         # change


cat <<'EOF' | k apply -f -
apiVersion: networking.k8s.io/v1
kind: ServiceCIDR
metadata:
  name: svc-cidr-new
spec:
  cidrs:
  - 11.96.0.0/12
EOF

k get servicecidr
# NAME           CIDRS          AGE
# kubernetes     10.96.0.0/12   32d
# svc-cidr-new   11.96.0.0/12   4s
```

---
