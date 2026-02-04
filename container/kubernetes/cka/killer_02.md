# killer02

[Back](../index.md)

- [killer02](#killer02)
  - [!!Q1: dns - miss + gap](#q1-dns---miss--gap)
  - [Q2: static pod](#q2-static-pod)
  - [!!Q3: kubelet pki - gap](#q3-kubelet-pki---gap)
  - [!Q4: probe - miss](#q4-probe---miss)
  - [Q5: cheap sheet](#q5-cheap-sheet)
  - [Q6: kubelet, cf](#q6-kubelet-cf)
  - [Q07: etcd backup/restore](#q07-etcd-backuprestore)
    - [Etcd Restore](#etcd-restore)
  - [Q08: kube-system](#q08-kube-system)
  - [!Q09: schedule - miss](#q09-schedule---miss)
  - [!Q10: sc,pvc,job - miss](#q10-scpvcjob---miss)
  - [!Q11: secret mount - miss](#q11-secret-mount---miss)
  - [Q12: tain/toleration](#q12-taintoleration)
  - [!Q13: sidecar,volMount - miss](#q13-sidecarvolmount---miss)
  - [!!Q14: svc-cidr, CNI plugin](#q14-svc-cidr-cni-plugin)
  - [!Q15: event, crictl - miss](#q15-event-crictl---miss)
  - [!!Q16: api resource, count resource - miss](#q16-api-resource-count-resource---miss)
  - [!!Q16: kustomize, operator - gap](#q16-kustomize-operator---gap)

---

## !!Q1: dns - miss + gap

Solve this question on: ssh cka6016

The Deployment controller in Namespace lima-control communicates with various cluster internal endpoints by using their DNS FQDN values.

Update the ConfigMap used by the Deployment with the correct FQDN values for:

DNS_1: Service kubernetes in Namespace default

DNS_2: Headless Service department in Namespace lima-workload

DNS_3: Pod section100 in Namespace lima-workload. It should work even if the Pod IP changes

DNS_4: A Pod with IP 1.2.3.4 in Namespace kube-system

Ensure the Deployment works with the updated values.

---

- Solution

```sh
# lookup default svc
nslookup kubernetes.default.svc.cluster.local

# DNS_1:
kubernetes.default.svc.cluster.local

# DNS_2:
nslookup department.lima-workload.svc.cluster.local

k get po section100 -n lima-workload -o yaml
# apiVersion: v1
# kind: Pod
# metadata:
#   name: section100
#   namespace: lima-workload
#   labels:
#     name: section
# spec:
#   hostname: section100  # set hostname
#   subdomain: section    # set subdomain to same name as service
#   containers:
#     - image: httpd:2-alpine
#       name: pod
# DNS_3:
nslookup section100.section.lima-workload.svc.cluster.local

# DNS_4:
nslookup 1-2-3-4.kube-system.pod.cluster.local


k -n lima-control edit cm control-config
# apiVersion: v1
# data:
#   DNS_1: kubernetes.default.svc.cluster.local                  # UPDATE
#   DNS_2: department.lima-workload.svc.cluster.local            # UPDATE
#   DNS_3: section100.section.lima-workload.svc.cluster.local    # UPDATE
#   DNS_4: 1-2-3-4.kube-system.pod.cluster.local                 # UPDATE
# kind: ConfigMap

kubectl -n lima-control rollout restart deploy controller
```

---

## Q2: static pod

Solve this question on: ssh cka2560

Create a Static Pod named my-static-pod in Namespace default on the controlplane node. It should be of image nginx:1-alpine and have resource requests for 10m CPU and 20Mi memory.

Create a NodePort Service named static-pod-service which exposes that static Pod on port 80.

ℹ️ For verification check if the new Service has one Endpoint. It should also be possible to access the Pod via the cka2560 internal IP address, like using curl 192.168.100.31:NODE_PORT

---

- solution:

```sh
k run my-static-pod --image=nginx:1-alpine -o yaml --dry-run=client > my-static-pod.yaml

vi my-static-pod.yaml
# apiVersion: v1
# kind: Pod
# metadata:
#   creationTimestamp: null
#   labels:
#     run: my-static-pod
#   name: my-static-pod
# spec:
#   containers:
#   - image: nginx:1-alpine
#     name: my-static-pod
#     resources:
#       requests:
#         cpu: 10m
#         memory: 20Mi
#   dnsPolicy: ClusterFirst
#   restartPolicy: Always
# status: {}

cp my-static-pod.yaml /etc/kubernetes/manifests/my-static-pod.yaml

k get po -n default

k expose pod my-static-pod-cka2560 --name static-pod-service --type=NodePort --port 80
```

---

## !!Q3: kubelet pki - gap

Solve this question on: ssh cka5248

Node cka5248-node1 has been added to the cluster using kubeadm and TLS bootstrapping.

Find the Issuer and Extended Key Usage values on cka5248-node1 for:

Kubelet Client Certificate, the one used for outgoing connections to the kube-apiserver
Kubelet Server Certificate, the one used for incoming connections from the kube-apiserver
Write the information into file /opt/course/3/certificate-info.txt.

ℹ️ You can connect to the worker node using ssh cka5248-node1 from cka5248

---

- solution

```sh
ssh cka5248-node1
sudo -i

ls /var/lib/kubelet/pki
# /var/lib/kubelet/pki/kubelet-client-2024-10-29-14-24-14.pem
# /var/lib/kubelet/pki/kubelet.crt
# /var/lib/kubelet/pki/kubelet.key
# /var/lib/kubelet/pki/kubelet-client-current.pem

openssl x509 -noout -text -in /var/lib/kubelet/pki/kubelet-client-current.pem | grep Issuer
# Issuer: CN = kubernetes
openssl x509 -noout -text -in /var/lib/kubelet/pki/kubelet-client-current.pem | grep "Extended Key Usage" -A1
#   X509v3 Extended Key Usage:
#                 TLS Web Client Authentication

openssl x509 -noout -text -in /var/lib/kubelet/pki/kubelet.crt | grep Issuer
        # Issuer: CN = cka5248-node1-ca@1730211854

openssl x509 -noout -text -in /var/lib/kubelet/pki/kubelet.crt | grep "Extended Key Usage" -A1
            # X509v3 Extended Key Usage:
            #     TLS Web Server Authentication
sudo vi /opt/course/3/certificate-info.txt
# Issuer: CN = kubernetes
# X509v3 Extended Key Usage: TLS Web Client Authentication
# Issuer: CN = cka5248-node1-ca@1730211854
# X509v3 Extended Key Usage: TLS Web Server Authentication
```

---

## !Q4: probe - miss

Solve this question on: ssh cka3200

Do the following in Namespace default:

Create a Pod named ready-if-service-ready of image nginx:1-alpine

Configure a LivenessProbe which simply executes command true

Configure a ReadinessProbe which does check if the url http://service-am-i-ready:80 is reachable, you can use wget -T2 -O- http://service-am-i-ready:80 for this

Start the Pod and confirm it isn't ready because of the ReadinessProbe.

Then:

Create a second Pod named am-i-ready of image nginx:1-alpine with label id: cross-server-ready

The already existing Service service-am-i-ready should now have that second Pod as endpoint

Now the first Pod should be in ready state, check that

---

- Solution

```sh
tee >q04.yaml<<EOF
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: ready-if-service-ready
  name: ready-if-service-ready
spec:
  containers:
  - image: nginx:1-alpine
    name: ready-if-service-ready
    resources: {}
    livenessProbe:                                      # add from here
      exec:
        command:
        - 'true'
    readinessProbe:
      exec:
        command:
        - sh
        - -c
        - 'wget -T2 -O- http://service-am-i-ready:80'   # to here

EOF

k apply -f q04.yaml

k describe pod ready-if-service-ready

k run am-i-ready --image=nginx:1-alpine --labels="id=cross-server-ready"
```

---

## Q5: cheap sheet

Solve this question on: ssh cka8448

Create two bash script files which use kubectl sorting to:

Write a command into /opt/course/5/find_pods.sh which lists all Pods in all Namespaces sorted by their AGE (metadata.creationTimestamp)

Write a command into /opt/course/5/find_pods_uid.sh which lists all Pods in all Namespaces sorted by field metadata.uid

---

- Solution

```sh
vi /opt/course/5/find_pods.sh
# kubectl get pod -A --sort-by=.metadata.creationTimestamp

vi /opt/course/5/find_pods_uid.sh
# kubectl get pod -A --sort-by=.metadata.uid
```

---

## Q6: kubelet, cf

Solve this question on: ssh cka1024

There seems to be an issue with the kubelet on controlplane node cka1024, it's not running.

Fix the kubelet and confirm that the node is available in Ready state.

Create a Pod called success in default Namespace of image nginx:1-alpine.

ℹ️ The node has no taints and can schedule Pods without additional tolerations

---

- solution

```sh
# list node
k get node
# E0423 12:27:08.326639   12871 memcache.go:265] "Unhandled Error" err="couldn't get current server API group list: Get \"https://192.168.100.41:6443/api?timeout=32s\": dial tcp 192.168.100.41:6443: connect: connection refused"

sudo -i
# check kubelet
service kubelet status
# ○ kubelet.service - kubelet: The Kubernetes Node Agent
#      Loaded: loaded (/usr/lib/systemd/system/kubelet.service; enabled; preset: enabled)
#     Drop-In: /usr/lib/systemd/system/kubelet.service.d
#              └─10-kubeadm.conf
#      Active: inactive (dead) since Sun 2025-03-23 08:16:52 UTC; 1 month 0 days ago
# Process: 13014 ExecStart=/usr/local/bin/kubelet $KUBELET_KUBECONFIG_ARGS

# try restart
service kubelet start
service kubelet status

# confirm executable path: diff from "Process: 13014 ExecStart=/usr/local/bin/kubelet"
whereis kubelet
# kubelet: /usr/bin/kubelet

# fix: correct cf
vim /usr/lib/systemd/system/kubelet.service.d/10-kubeadm.conf
# ExecStart=/usr/bin/kubelet

# reload and restart
systemctl daemon-reload
service kubelet restart
service kubelet status

# confirm
k get node
# NAME      STATUS   ROLES           AGE   VERSION
# cka1024   Ready    control-plane   31d   v1.33.1

k run success --image nginx:1-alpine
k get pod success -o wide
```

---

## Q07: etcd backup/restore

Solve this question on: ssh cka2560

You have been tasked to perform the following etcd operations:

Run etcd --version and store the output at /opt/course/7/etcd-version

Make a snapshot of etcd and save it at /opt/course/7/etcd-snapshot.db

---

- Solution

```sh
# try: etcd is not installed as a process
etcd --version
# Command 'etcd' not found, but can be installed with:
# apt install etcd-server

# check kube-system po
k -n kube-system get pod
# NAME                              READY   STATUS    RESTARTS      AGE
# etcd-cka2560                      1/1     Running   0             13m

# get version via po
k -n kube-system exec etcd-cka2560 -- etcd --version

sudo -i
# get authentication data
vim /etc/kubernetes/manifests/etcd.yaml

ETCDCTL_API=3 etcdctl snapshot save /opt/course/7/etcd-snapshot.db \
--cacert /etc/kubernetes/pki/etcd/ca.crt \
--cert /etc/kubernetes/pki/etcd/server.crt \
--key /etc/kubernetes/pki/etcd/server.key
```

---

### Etcd Restore

```sh
# stop all controlplane components by remove manifests
cd /etc/kubernetes/manifests/
mv * ..

# confirm static po is removed
watch crictl ps

# restore
etcdctl snapshot restore /opt/course/7/etcd-snapshot.db \
--data-dir /var/lib/etcd-snapshot \
--cacert /etc/kubernetes/pki/etcd/ca.crt \
--cert /etc/kubernetes/pki/etcd/server.crt \
--key /etc/kubernetes/pki/etcd/server.key

# update etcd manifest the location
vim /etc/kubernetes/etcd.yaml
  # volumes:
  # - hostPath:
  #     path: /etc/kubernetes/pki/etcd
  #     type: DirectoryOrCreate
  #   name: etcd-certs
  # - hostPath:
  #     path: /var/lib/etcd-snapshot                # change
  #     type: DirectoryOrCreate

# move manifest back to path
mv ../*.yaml .

# confirm
kubectl get node
```

---

## Q08: kube-system

Solve this question on: ssh cka8448

Check how the controlplane components kubelet, kube-apiserver, kube-scheduler, kube-controller-manager and etcd are started/installed on the controlplane node.

Also find out the name of the DNS application and how it's started/installed in the cluster.

Write your findings into file /opt/course/8/controlplane-components.txt. The file should be structured like:

- /opt/course/8/controlplane-components.txt

kubelet: [TYPE]
kube-apiserver: [TYPE]
kube-scheduler: [TYPE]
kube-controller-manager: [TYPE]
etcd: [TYPE]
dns: [TYPE] [NAME]
Choices of [TYPE] are: not-installed, process, static-pod, pod

---

- Solution

```sh
# check kubelet is a process
ps aux | grep kubelet
service kubelet status

# check in the default manifests directory:
ls /etc/kubernetes/manifests/
# /etc/kubernetes/manifests/
# /etc/kubernetes/manifests/kube-controller-manager.yaml
# /etc/kubernetes/manifests/etcd.yaml
# /etc/kubernetes/manifests/kube-apiserver.yaml
# /etc/kubernetes/manifests/kube-scheduler.yaml

# check all Pods running on in the kube-system Namespace:
k -n kube-system get pod -o wide

# check dns
k -n kube-system get deploy
# NAME      READY   UP-TO-DATE   AVAILABLE   AGE
# coredns   2/2     2            2           68m

vi /opt/course/8/controlplane-components.txt
# kubelet: process
# kube-apiserver: static-pod
# kube-scheduler: static-pod
# kube-controller-manager: static-pod
# etcd: static-pod
# dns: pod coredns
```

---

## !Q09: schedule - miss

Solve this question on: ssh cka5248

Temporarily stop the kube-scheduler, this means in a way that you can start it again afterwards.

Create a single Pod named manual-schedule of image httpd:2-alpine, confirm it's created but not scheduled on any node.

Now you're the scheduler and have all its power, manually schedule that Pod on node cka5248. Make sure it's running.

Start the kube-scheduler again and confirm it's running correctly by creating a second Pod named manual-schedule2 of image httpd:2-alpine and check if it's running on cka5248-node1.

---

- solution

```sh
# check scheduler is in static po
k get node
kubectl -n kube-system get pod | grep schedule

# manually stop by removing manifest
cd /etc/kubernetes/manifests/
mv kube-scheduler.yaml ..

# confirm
crictl ps --name schedule
kubectl -n kube-system get pod | grep schedule

# Create a Pod
k run manual-schedule --image=httpd:2-alpine
# pod/manual-schedule created

k get pod manual-schedule -o wide
# NAME              READY   STATUS    RESTARTS   AGE   IP       NODE    ...
# manual-schedule   0/1     Pending   0          14s   <none>   <none>  ...

# Manually schedule the Pod
k get pod manual-schedule -o yaml > 9.yaml

vi 9.yaml
# spec:
#   nodeName: cka5248       # ADD the controlplane node name

k -f 9.yaml replace --force
# confirm
k get pod manual-schedule -o wide
# NAME              READY   STATUS    ...   NODE
# manual-schedule   1/1     Running   ...   cka5248


# start scheduler
cd /etc/kubernetes/manifests/
mv ../kube-scheduler.yaml .

# create pod
k run manual-schedule2 --image=httpd:2-alpine

```

---

## !Q10: sc,pvc,job - miss

There is a backup Job which needs to be adjusted to use a PVC to store backups.

Create a StorageClass named local-backup which uses provisioner: rancher.io/local-path and volumeBindingMode: WaitForFirstConsumer. To prevent possible data loss the StorageClass should keep a PV retained even if a bound PVC is deleted.

Adjust the Job at /opt/course/10/backup.yaml to use a PVC which request 50Mi storage and uses the new StorageClass.

Deploy your changes, verify the Job completed once and the PVC was bound to a newly created PV.

ℹ️ To re-run a Job, delete it and create it again

ℹ️ The abbreviation PV stands for PersistentVolume and PVC for PersistentVolumeClaim

---

- Solution

```sh
# Create StorageClass
tee >vim sc.yaml<<EOF
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-backup
provisioner: rancher.io/local-path
reclaimPolicy: Retain
volumeBindingMode: WaitForFirstConsumer
EOF

k -f sc.yaml apply

k get sc
# NAME           PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      ...
# local-backup   rancher.io/local-path   Retain          WaitForFirstConsumer   ...
# local-path     rancher.io/local-path   Delete          WaitForFirstConsumer   ...

# update yaml
vi /opt/course/10/backup.yaml
# apiVersion: v1
# kind: PersistentVolumeClaim
# metadata:
#   name: backup-pvc
#   namespace: project-bern            # use same Namespace
# spec:
#   storageClassName: local-backup     # use the new StorageClass
#   accessModes:
#     - ReadWriteOnce
#   resources:
#     requests:
#       storage: 50Mi                  # request the required size
# ---
# apiVersion: batch/v1
# kind: Job
# metadata:
#   name: backup
#   namespace: project-bern
# spec:
#   backoffLimit: 0
#   template:
#     spec:
#       volumes:
#         - name: backup
#           persistentVolumeClaim:     # CHANGE
#             claimName: backup-pvc    # CHANGE
#       containers:
#         - name: bash
#           image: bash:5
#           command:
#             - bash
#             - -c
#             - |
#               set -x
#               touch /backup/backup-$(date +%Y-%m-%d-%H-%M-%S).tar.gz
#               sleep 15
#           volumeMounts:
#             - name: backup
#               mountPath: /backup
#       restartPolicy: Never

k apply -f backup.yaml

 k -n project-bern get job,pod,pvc,pv
# NAME               STATUS    COMPLETIONS   DURATION   AGE
# job.batch/backup   Running   0/1           13s        13s

# NAME               READY   STATUS    RESTARTS   AGE
# pod/backup-q7dgx   1/1     Running   0          13s

# NAME         STATUS   VOLUME                                     CAPACITY   ...
# backup-pvc   Bound    pvc-dbccec94-cc31-4e30-b5fe-7cb42a85fe7a   50Mi       ...

# NAME          CAPACITY   ...  RECLAIM POLICY  STATUS  CLAIM                     ...
# pvc-dbcce...  50Mi       ...  Retain          Bound   project-bern/backup-pvc   ...
```

---

## !Q11: secret mount - miss

Solve this question on: ssh cka2560

Create Namespace secret and implement the following in it:

Create Pod secret-pod with image busybox:1. It should be kept running by executing sleep 1d or something similar

Create the existing Secret /opt/course/11/secret1.yaml and mount it readonly into the Pod at /tmp/secret1

Create a new Secret called secret2 which should contain user=user1 and pass=1234. These entries should be available inside the Pod's container as environment variables APP_USER and APP_PASS

---

- solution

```sh
# update ns
vi /opt/course/11/secret1.yaml
# metadata:
#   creationTimestamp: null
#   name: secret1
#   namespace: secret           # UPDATE

k -f /opt/course/11/secret1.yaml create

k -n secret create secret generic secret2 --from-literal=user=user1 --from-literal=pass=1234


# create po
tee >11.yaml<<EOF
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: secret-pod
  name: secret-pod
  namespace: secret                       # important if not automatically added
spec:
  containers:
  - args:
    - sh
    - -c
    - sleep 1d
    image: busybox:1
    name: secret-pod
    env:                                  # add
    - name: APP_USER                      # add
      valueFrom:                          # add
        secretKeyRef:                     # add
          name: secret2                   # add
          key: user                       # add
    - name: APP_PASS                      # add
      valueFrom:                          # add
        secretKeyRef:                     # add
          name: secret2                   # add
          key: pass                       # add
    volumeMounts:                         # add
    - name: secret1                       # add
      mountPath: /tmp/secret1             # add
      readOnly: true                      # add
  volumes:                                # add
  - name: secret1                         # add
    secret:                               # add
      secretName: secret1                 # add
EOF

k -f 11.yaml create

k -n secret exec secret-pod -- env | grep APP
k -n secret exec secret-pod -- ls /tmp/secret1
```

---

## Q12: tain/toleration

Solve this question on: ssh cka5248

Create a Pod of image httpd:2-alpine in Namespace default.

The Pod should be named pod1 and the container should be named pod1-container.

This Pod should only be scheduled on controlplane nodes.

Do not add new labels to any nodes.

---

- Solution

```sh
➜ candidate@cka5248:~$ k get node
# NAME            STATUS   ROLES           AGE   VERSION
# cka5248         Ready    control-plane   90m   v1.33.1
# cka5248-node1   Ready    <none>          85m   v1.33.1

➜ candidate@cka5248:~$ k describe node cka5248 | grep Taint -A1
# Taints:             node-role.kubernetes.io/control-plane:NoSchedule
# Unschedulable:      false

k get node cka5248 --show-labels

tee >12.yaml<<EOF
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: pod1
  name: pod1
spec:
  containers:
  - image: httpd:2-alpine
    name: pod1-container                       # change
  tolerations:                                 # add
  - effect: NoSchedule                         # add
    key: node-role.kubernetes.io/control-plane # add
  nodeSelector:                                # add
    node-role.kubernetes.io/control-plane: ""  # add
EOF
```

---

## !Q13: sidecar,volMount - miss

Solve this question on: ssh cka3200

Create a Pod with multiple containers named multi-container-playground in Namespace default:

It should have a volume attached and mounted into each container. The volume shouldn't be persisted or shared with other Pods

Container c1 with image nginx:1-alpine should have the name of the node where its Pod is running on available as environment variable MY_NODE_NAME

Container c2 with image busybox:1 should write the output of the date command every second in the shared volume into file date.log. You can use while true; do date >> /your/vol/path/date.log; sleep 1; done for this.

Container c3 with image busybox:1 should constantly write the content of file date.log from the shared volume to stdout. You can use tail -f /your/vol/path/date.log for this.

---

- solution

```sh
tee >13.yaml<<EOF
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: multi-container-playground
  name: multi-container-playground
spec:
  volumes:                                                                        # add
    - name: vol                                                                   # add
      emptyDir: {}                                                                # add
  containers:
  - image: nginx:1-alpine
    name: c1                                                                      # change
    env:                                                                          # add
    - name: MY_NODE_NAME                                                          # add
      valueFrom:                                                                  # add
        fieldRef:                                                                 # add
          fieldPath: spec.nodeName                                                # add
    volumeMounts:                                                                 # add
    - name: vol                                                                   # add
      mountPath: /vol                                                             # add
  - image: busybox:1                                                              # add
    name: c2                                                                      # add
    command: ["sh", "-c", "while true; do date >> /vol/date.log; sleep 1; done"]  # add
    volumeMounts:                                                                 # add
    - name: vol                                                                   # add
      mountPath: /vol                                                             # add
  - image: busybox:1                                                              # add
    name: c3                                                                      # add
    command: ["sh", "-c", "tail -f /vol/date.log"]                                # add
    volumeMounts:                                                                 # add
    - name: vol                                                                   # add
      mountPath: /vol                                                             # add
EOF
```

---

## !!Q14: svc-cidr, CNI plugin

Solve this question on: ssh cka8448

You're ask to find out following information about the cluster:

How many controlplane nodes are available?

How many worker nodes (non controlplane nodes) are available?

What is the Service CIDR?

Which Networking (or CNI Plugin) is configured and where is its config file?

Which suffix will static pods have that run on cka8448?

Write your answers into file /opt/course/14/cluster-info, structured like this:

- /opt/course/14/cluster-info

1: [ANSWER]
2: [ANSWER]
3: [ANSWER]
4: [ANSWER]
5: [ANSWER]

---

- solution

```sh
k get node
# NAME      STATUS   ROLES           AGE   VERSION
# cka8448   Ready    control-plane   71m   v1.33.1

# Service CIDR
cat /etc/kubernetes/manifests/kube-apiserver.yaml | grep range
    # - --service-cluster-ip-range=10.96.0.0/12

# Networking (or CNI Plugin)
cd /etc/cni/net.d/

ls
# /etc/cni/net.d/.kubernetes-cni-keep
# /etc/cni/net.d/10-weave.conflist
# /etc/cni/net.d/87-podman-bridge.conflist

# suffix
/opt/course/14/cluster-info
# # How many controlplane nodes are available?
# 1: 1

# # How many worker nodes (non controlplane nodes) are available?
# 2: 0

# # What is the Service CIDR?
# 3: 10.96.0.0/12

# # Which Networking (or CNI Plugin) is configured and where is its config file?
# 4: Weave, /etc/cni/net.d/10-weave.conflist

# # Which suffix will static pods have that run on cka8448?
# 5: -cka8448
```

---

## !Q15: event, crictl - miss

Solve this question on: ssh cka6016

Write a kubectl command into /opt/course/15/cluster_events.sh which shows the latest events in the whole cluster, ordered by time (metadata.creationTimestamp)

Delete the kube-proxy Pod and write the events this caused into /opt/course/15/pod_kill.log on cka6016

Manually kill the containerd container of the kube-proxy Pod and write the events into /opt/course/15/container_kill.log

---

- solution

```sh
vi /opt/course/15/cluster_events.sh
# kubectl get events -A --sort-by=.metadata.creationTimestamp




# Delete the kube-proxy Pod
k -n kube-system get pod -l k8s-app=kube-proxy -owide
# NAME               READY   ...     NODE      NOMINATED NODE   READINESS GATES
# kube-proxy-lf2fs   1/1     ...     cka6016   <none>           <none>

k -n kube-system delete pod kube-proxy-lf2fs
# pod "kube-proxy-lf2fs" deleted

# check ev: kill, create, and start
kubectl get events -A --sort-by=.metadata.creationTimestamp

vi /opt/course/15/pod_kill.log
# kube-system   12s         Normal    Killing             pod/kube-proxy-lf2fs                    Stopping container kube-proxy
# kube-system   12s         Normal    SuccessfulCreate    daemonset/kube-proxy                    Created pod: kube-proxy-wb4tb
# kube-system   11s         Normal    Scheduled           pod/kube-proxy-wb4tb                    Successfully assigned kube-system/kube-proxy-wb4tb to cka6016
# kube-system   11s         Normal    Pulled              pod/kube-proxy-wb4tb                    Container image "registry.k8s.io/kube-proxy:v1.33.1" already present on machine
# kube-system   11s         Normal    Created             pod/kube-proxy-wb4tb                    Created container kube-proxy
# kube-system   11s         Normal    Started             pod/kube-proxy-wb4tb                    Started container kube-proxy
# default       10s         Normal    Starting            node/cka6016



# Manually kill the containerd container
crictl ps | grep kube-proxy
# 2fd052f1fcf78       505d571f5fd56       57 seconds ago      Running             kube-proxy                0                   3455856e0970c       kube-proxy-wb4tb

# remove
crictl rm --force 2fd052f1fcf78
crictl ps | grep kube-proxy
# 6bee4f36f8410       505d571f5fd56       5 seconds ago       Running             kube-proxy                0                   3455856e0970c       kube-proxy-wb4tb

# get ev: create and start
kubectl get events -A --sort-by=.metadata.creationTimestamp
vi /opt/course/15/container_kill.log
# kube-system   21s         Normal    Created             pod/kube-proxy-wb4tb                    Created container kube-proxy
# kube-system   21s         Normal    Started             pod/kube-proxy-wb4tb                    Started container kube-proxy
# default       90s         Normal    Starting            node/cka6016
# default       20s         Normal    Starting            node/cka6016
```

---

## !!Q16: api resource, count resource - miss

Solve this question on: ssh cka3200

Write the names of all namespaced Kubernetes resources (like Pod, Secret, ConfigMap...) into /opt/course/16/resources.txt.

Find the project-\* Namespace with the highest number of Roles defined in it and write its name and amount of Roles into /opt/course/16/crowded-namespace.txt.

---

- Solution:

```sh
k api-resources --namespaced -o name > /opt/course/16/resources.txt

# get ns
k get ns --sort-by=.metadata.name

# count on by one
k -n project-jinan get role --no-headers | wc -l
# No resources found in project-jinan namespace.
# 0

➜ candidate@cka3200:~$ k -n project-miami get role --no-headers | wc -l
# 300

➜ candidate@cka3200:~$ k -n project-melbourne get role --no-headers | wc -l
# 2

➜ candidate@cka3200:~$ k -n project-seoul get role --no-headers | wc -l
# 10

➜ candidate@cka3200:~$ k -n project-toronto get role --no-headers | wc -l
# No resources found in project-toronto namespace.
# 0
```

---

## !!Q16: kustomize, operator - gap

Solve this question on: ssh cka6016

There is Kustomize config available at /opt/course/17/operator. It installs an operator which works with different CRDs. It has been deployed like this:

kubectl kustomize /opt/course/17/operator/prod | kubectl apply -f -

Perform the following changes in the Kustomize base config:

- The operator needs to list certain CRDs. Check the logs to find out which ones and adjust the permissions for Role operator-role
- Add a new Student resource called student4 with any name and description
- Deploy your Kustomize config changes to prod.

---

```sh
# get the base manifest
k kustomize base

# get prod manifest:  namespace: operator-prod
k kustomize prod
#  namespace: operator-prod


k -n operator-prod get pod
# NAME                        READY   STATUS    RESTARTS   AGE
# operator-7f4f58d4d9-v6ftw   1/1     Running   0          6m9s

# Check the logs: sa no permission
k -n operator-prod logs operator-7f4f58d4d9-v6ftw
# + true
# + kubectl get students
# Error from server (Forbidden): students.education.killer.sh is forbidden: User "system:serviceaccount:operator-prod:operator" cannot list resource "students" in API group "education.killer.sh" in the namespace "operator-prod"
# + kubectl get classes
# Error from server (Forbidden): classes.education.killer.sh is forbidden: User "system:serviceaccount:operator-prod:operator" cannot list resource "classes" in API group "education.killer.sh" in the namespace "operator-prod"
# + sleep 10
# + true

# add rbac in base
vi base/rbac.yaml
# apiVersion: rbac.authorization.k8s.io/v1
# kind: Role
# metadata:
#   name: operator-role
#   namespace: default
# rules:
# - apiGroups:
#   - education.killer.sh
#   resources:
#   - students
#   - classes
#   verbs:
#   - list
# ---
# apiVersion: rbac.authorization.k8s.io/v1
# kind: RoleBinding
# metadata:
#   name: operator-rolebinding
#   namespace: default
# subjects:
#   - kind: ServiceAccount
#     name: operator
#     namespace: default
# roleRef:
#   kind: Role
#   name: operator-role
#   apiGroup: rbac.authorization.k8s.io

# deploy
kubectl kustomize

# confirm
k -n operator-prod logs operator-7f4f58d4d9-v6ftw
# + kubectl get students
# NAME       AGE
# student1   22m
# student2   22m
# student3   22m
# + kubectl get classes
# NAME       AGE
# advanced   20m



# Create new Student resource
vi base/students.yaml
# apiVersion: education.killer.sh/v1
# kind: Student
# metadata:
#   name: student3
# spec:
#   name: Carol Williams
#   description: A student excelling in container orchestration and management
# ---
# apiVersion: education.killer.sh/v1
# kind: Student
# metadata:
#   name: student4
# spec:
#   name: Some Name
#   description: Some Description

# deploy
kubectl apply -k /opt/course/17/operator/prod

# confirm
k -n operator-prod get student
# NAME       AGE
# student1   28m
# student2   28m
# student3   27m
# student4   43s
```

---
