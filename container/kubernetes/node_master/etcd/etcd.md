# Kubernetes Cluster - `etcd`

[Back](../../index.md)

- [Kubernetes Cluster - `etcd`](#kubernetes-cluster---etcd)
  - [`etcd`](#etcd)
    - [CLI: `etcdctl`](#cli-etcdctl)
    - [How it Works - `kubectl apply`](#how-it-works---kubectl-apply)
    - [How it Works - `kubectl get`](#how-it-works---kubectl-get)
  - [Common commands](#common-commands)
  - [Starting etcd clusters](#starting-etcd-clusters)
    - [Single-node etcd cluster](#single-node-etcd-cluster)
    - [Multi-node etcd cluster](#multi-node-etcd-cluster)
  - [Backing up an etcd cluster](#backing-up-an-etcd-cluster)
  - [Restoring an etcd cluster](#restoring-an-etcd-cluster)
    - [Lab: Install `etcdctl`](#lab-install-etcdctl)
  - [ETCD Deployment Type](#etcd-deployment-type)
  - [Lab: Backup \& Restore `etcd`](#lab-backup--restore-etcd)
    - [Create Resources Before Backup](#create-resources-before-backup)
    - [Lab: Backup a Snapshot](#lab-backup-a-snapshot)
    - [Change Resources After Backup](#change-resources-after-backup)
    - [Restore a Snapshot](#restore-a-snapshot)

---

## `etcd`

- `etcd`

  - A `control plane` component that is a a distributed, consistent **key-value store** to **persist** the **cluster data**.
  - acts as the **single source of truth** for the cluster.

- **Everything** is created or changed in Kubernetes is **stored** in `etcd`

  - **Cluster state**: what nodes exist, their health, etc.
  - **Workloads**: Deployments, Pods, ReplicaSets, DaemonSets.
  - **Configuration**: ConfigMaps, Secrets.
  - **Networking**: Services, Endpoints, network policies.
  - **Access control**: Roles and RoleBindings.

- Port:

  - `2379`
    - client communication
    - Used by the Kubernetes `API Server` (and any other client) to **read/write data**.
    - https://etcd_server:2379
  - `2380`
    - peer communication
    - Used for etcd members to talk to each other in an `etcd` cluster.
    - https://etcd_server:2380

- Ensure that the `leader` **periodically send heartbeats** on time to all `followers` to keep the cluster stable
- should run `etcd` **as a cluster** with an **odd number** of members.

---

- Important roles:
  - **Consistency**: `etcd` ensures that all `API servers` see the **same state**, even in multi-master setups.(implementing **locks** within the cluster)
  - **Fault Tolerance**: `etcd clusters` **replicate data** across multiple members to survive node failures.
  - **Performance**: optimized for fast reads/writes of **small JSON objects**, which is ideal for Kubernetes metadata.

---

### CLI: `etcdctl`

- `etcdctl`:

  - the **primary command-line client** for interacting with etcd over a network.
  - It is used for **day-to-day operations** such as managing keys and values, administering the cluster, checking health, and more.

- `etcdutl`:
  - an **administration utility** designed to **operate** directly on `etcd data files`,
  - including **migrating data** between etcd versions, **defragmenting** the database, **restoring** snapshots, and **validating** data consistency.

---

### How it Works - `kubectl apply`

- issue **apply** YAML (`kubectl apply -f yaml_file`) send request goes to `API Server`.
- `API Server` **validates** and **writes** the **desired state** into `etcd`.
- `Controllers`, `schedulers`, and other `control plane` components take actions to make the actual cluster **match** the **desired state**.

---

### How it Works - `kubectl get`

- When launching the command `kubectl get pods`, the request is sent to the `API Server` via a REST API call.

  - kubectl is just a `thin client` — it **doesn’t** talk to `etcd` or nodes **directly**.

- The `API Server` **checks** authentication and authorization, RBAC.

  - If you don’t have permission to get pods, it denies the request.

- The `API Server` looks up the current cluster state from `etcd`
  - the API Server also uses its **local cache** that is always consistent with the latest state.
- The `API Server` **returns** the requested objects

---

## Common commands

```sh
kubectl get pods -n kube-system
# NAME                                     READY   STATUS    RESTARTS        AGE
# ...
etcd-docker-desktop                      1/1     Running   124 (41s ago)   147d
# ...

```

- version 2

| CMD                      | DESC |
| ------------------------ | ---- |
| `etcdctl backup`         |      |
| `etcdctl cluster-health` |      |
| `etcdctl mk`             |      |
| `etcdctl mkdir`          |      |
| `etcdctl set`            |      |

- version 3

| CMD                       | DESC |
| ------------------------- | ---- |
| `etcdctl snapshot save`   |      |
| `etcdctl endpoint health` |      |
| `etcdctl get`             |      |
| `etcdctl put`             |      |

- Command to get the version os API
  - `export ETCDCTL_API=3`

---

## Starting etcd clusters

### Single-node etcd cluster

- `single-node etcd cluster`
  - only for **testing purposes**.

```sh
# PRIVATE_IP is set to your etcd client IP
etcd --listen-client-urls=http://$PRIVATE_IP:2379 --advertise-client-urls=http://$PRIVATE_IP:2379
```

---

### Multi-node etcd cluster

- For **durability** and **high availability**, run etcd as a `multi-node cluster` in **production** and back it up periodically.
- A `five-member cluster` is **recommended** in production.

- **by default**
  - `kubeadm` tool sets up `etcd` **static pods**
- external `etcd cluster`

  - can deploy a **separate cluster** and instruct `kubeadm` to use that `etcd cluster` as the `control plane`'s **backing store**.

- Example: start a Kubernetes API server with five-member etcd cluster

```sh
etcd --listen-client-urls=http://$IP1:2379,http://$IP2:2379,http://$IP3:2379,http://$IP4:2379,http://$IP5:2379 \
  --advertise-client-urls=http://$IP1:2379,http://$IP2:2379,http://$IP3:2379,http://$IP4:2379,http://$IP5:2379
```

---

## Backing up an etcd cluster

- A `snapshot` may either
  - be **created from a live member** with the `etcdctl snapshot save` command
  - or by **copying** the `member/snap/db` file from an etcd data directory that is **not currently used** by an `etcd process`.

---

## Restoring an etcd cluster

- **Caution**

  - If any `API servers` are **running** in the cluster, **should not** attempt to **restore** instances of `etcd`.

- **Should**
  - **stop** all `API server` instances
  - **restore** state in all `etcd` instances
  - **restart** all `API server` instances

---

### Lab: Install `etcdctl`

```sh
# install
sudo apt install etcd-client

# confirm
etcdctl version
# etcdctl version: 3.4.30
# API version: 3.4
```

---

## ETCD Deployment Type

- ETCD can be deployed

  - **internally** (as a Kubernetes `pod`)
  - or **externally** (as a standalone `service`).

- COmmand to confirm:
  - `kubectl get pods -n kube-system `

---

## Lab: Backup & Restore `etcd`

### Create Resources Before Backup

```sh
kubectl create deploy before --image=nginx --replicas=2
# deployment.apps/before created

kubectl get deploy
# NAME     READY   UP-TO-DATE   AVAILABLE   AGE
# before   2/2     2            2           24s
```

---

### Lab: Backup a Snapshot

- Get `etcd` configuration

```sh
sudo cat /etc/kubernetes/manifests/etcd.yaml
# apiVersion: v1
# kind: Pod
# metadata:
#   name: etcd
#   namespace: kube-system
# spec:
#   containers:
#   - command:
#     - etcd
#     - --advertise-client-urls=https://192.168.10.150:2379
#     - --cert-file=/etc/kubernetes/pki/etcd/server.crt
#     - --data-dir=/var/lib/etcd
#     - --key-file=/etc/kubernetes/pki/etcd/server.key
#     - --listen-client-urls=https://127.0.0.1:2379,https://192.168.10.150:2379
#     - --trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt

# backup etcd to /opt/etcd-backup.db
sudo -i ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379  \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt    \
  --cert=/etc/kubernetes/pki/etcd/server.crt  \
  --key=/etc/kubernetes/pki/etcd/server.key   \
  snapshot save /opt/etcd-backup.db
# {"level":"info","ts":1768457316.0622098,"caller":"snapshot/v3_snapshot.go:119","msg":"created temporary db file","path":"/opt/etcd-backup.db.part"}
# {"level":"info","ts":"2026-01-15T01:08:36.065703-0500","caller":"clientv3/maintenance.go:212","msg":"opened snapshot stream; downloading"}
# {"level":"info","ts":1768457316.0657685,"caller":"snapshot/v3_snapshot.go:127","msg":"fetching snapshot","endpoint":"https://127.0.0.1:2379"}
# {"level":"info","ts":"2026-01-15T01:08:36.090634-0500","caller":"clientv3/maintenance.go:220","msg":"completed snapshot read; closing"}
# {"level":"info","ts":1768457316.0953746,"caller":"snapshot/v3_snapshot.go:142","msg":"fetched snapshot","endpoint":"https://127.0.0.1:2379","size":"2.7 MB","took":0.033098198}
# {"level":"info","ts":1768457316.0954528,"caller":"snapshot/v3_snapshot.go:152","msg":"saved","path":"/opt/etcd-backup.db"}
# Snapshot saved at /opt/etcd-backup.db

# confirm
export ETCDCTL_API=3
sudo etcdctl --write-out=table snapshot status /opt/etcd-backup.db
# +----------+----------+------------+------------+
# |   HASH   | REVISION | TOTAL KEYS | TOTAL SIZE |
# +----------+----------+------------+------------+
# | c3a39352 |     1744 |       1764 |     3.3 MB |
# +----------+----------+------------+------------+
```

---

### Change Resources After Backup

```sh
kubectl delete deploy before
# deployment.apps "before" deleted

kubectl create deploy after --image=nginx --replicas=2
# deployment.apps/after created

kubectl get deploy
# NAME    READY   UP-TO-DATE   AVAILABLE   AGE
# after   2/2     2            2           12s
```

---

### Restore a Snapshot

```sh
sudo rm -rf /var/lib/etcd-restore
sudo ETCDCTL_API=3 etcdctl snapshot restore /opt/etcd-backup.db --data-dir=/var/lib/etcd-restore
# {"level":"info","ts":1768460423.4175081,"caller":"snapshot/v3_snapshot.go:306","msg":"restoring snapshot","path":"/opt/etcd-backup.db","wal-dir":"/var/lib/etcd-restore/member/wal","data-dir":"/var/lib/etcd-restore","snap-dir":"/var/lib/etcd-restore/member/snap"}
# {"level":"info","ts":1768460423.4347312,"caller":"membership/cluster.go:392","msg":"added member","cluster-id":"cdf818194e3a8c32","local-member-id":"0","added-peer-id":"8e9e05c52164694d","added-peer-peer-urls":["http://localhost:2380"]}
# {"level":"info","ts":1768460423.440487,"caller":"snapshot/v3_snapshot.go:326","msg":"restored snapshot","path":"/opt/etcd-backup.db","wal-dir":"/var/lib/etcd-restore/member/wal","data-dir":"/var/lib/etcd-restore","snap-dir":"/var/lib/etcd-restore/member/snap"}

sudo vi /etc/kubernetes/manifests/etcd.yaml
# find:
# - name: etcd-data
#   hostPath:
#     path: /var/lib/etcd
# update:
# - name: etcd-data
#   hostPath:
#     path: /var/lib/etcd-restore

# confirm the "before" deployment restored
kubectl get deploy
# NAME     READY   UP-TO-DATE   AVAILABLE   AGE
# before   2/2     2            2           7m44s

```
