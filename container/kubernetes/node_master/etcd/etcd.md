# Kubernetes Cluster - `etcd`

[Back](../../index.md)

- [Kubernetes Cluster - `etcd`](#kubernetes-cluster---etcd)
  - [`etcd`](#etcd)
    - [How it Works - `kubectl apply`](#how-it-works---kubectl-apply)
    - [How it Works - `kubectl get`](#how-it-works---kubectl-get)
    - [Install Configuration](#install-configuration)
  - [Starting etcd clusters](#starting-etcd-clusters)
    - [Single-node etcd cluster](#single-node-etcd-cluster)
    - [Multi-node etcd cluster](#multi-node-etcd-cluster)
  - [CLI: `etcdctl`](#cli-etcdctl)
    - [Common Commands](#common-commands)
    - [Lab: `etcdctl`](#lab-etcdctl)
      - [etcd info](#etcd-info)
      - [Key-value](#key-value)
  - [Backing up an etcd cluster](#backing-up-an-etcd-cluster)
  - [Restoring an etcd cluster](#restoring-an-etcd-cluster)
    - [Lab: Install `etcdctl`](#lab-install-etcdctl)
  - [Lab: Backup \& Restore `etcd`](#lab-backup--restore-etcd)
    - [Create Resources Before Backup](#create-resources-before-backup)
    - [Lab: Backup a Snapshot](#lab-backup-a-snapshot)
    - [Change Resources After Backup](#change-resources-after-backup)
    - [Restore a Snapshot](#restore-a-snapshot)
  - [Security](#security)
    - [Lab: etcd security](#lab-etcd-security)
      - [Plain Text Data Storage: Demo](#plain-text-data-storage-demo)
      - [TLS Encryption: Demo](#tls-encryption-demo)

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

- ETCD can be deployed
  - **internally** (as a Kubernetes `pod`)
  - or **externally** (as a standalone `service`).

---

- Important roles:
  - **Consistency**: `etcd` ensures that all `API servers` see the **same state**, even in multi-master setups.(implementing **locks** within the cluster)
  - **Fault Tolerance**: `etcd clusters` **replicate data** across multiple members to survive node failures.
  - **Performance**: optimized for fast reads/writes of **small JSON objects**, which is ideal for Kubernetes metadata.

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

### Install Configuration

1. Identity and storage

| Options            | Description                                                                     |
| ------------------ | ------------------------------------------------------------------------------- |
| `--name`           | Name of this etcd member. It should match the name used in `--initial-cluster`. |
| `--data-dir`       | Directory where etcd stores its database files.                                 |
| `--snapshot-count` | Number of committed transactions before etcd creates a database snapshot.       |

2. Client communication
   Used for communication between kube-apiserver and etcd.

| Options                   | Description                                                                          |
| ------------------------- | ------------------------------------------------------------------------------------ |
| `--listen-client-urls`    | URLs where etcd listens for client traffic, commonly on port `2379`.                 |
| `--advertise-client-urls` | Client URLs that this etcd member advertises to clients, such as the kube-apiserver. |

3. Peer communication and cluster membership
   Used for communication between etcd members.

| Options                         | Description                                                                               |
| ------------------------------- | ----------------------------------------------------------------------------------------- |
| `--listen-peer-urls`            | URLs where etcd listens for peer-to-peer traffic, commonly on port `2380`.                |
| `--initial-advertise-peer-urls` | Peer URL this etcd member advertises to other etcd members during cluster initialization. |
| `--initial-cluster`             | Initial etcd cluster membership list, mapping member names to peer URLs.                  |

4. Client TLS security
   Used to secure kube-apiserver ↔ etcd traffic.

| Options              | Description                                                                           |
| -------------------- | ------------------------------------------------------------------------------------- |
| `--cert-file`        | Server certificate used by etcd for client-facing HTTPS connections.                  |
| `--key-file`         | Private key for the etcd server certificate used for client-facing HTTPS connections. |
| `--client-cert-auth` | Requires clients to authenticate with a valid client certificate.                     |
| `--trusted-ca-file`  | CA certificate used to verify client certificates.                                    |

5. Peer TLS security
   Used to secure etcd member ↔ etcd member traffic.

| Options                   | Description                                                         |
| ------------------------- | ------------------------------------------------------------------- |
| `--peer-cert-file`        | Certificate used by etcd for peer-to-peer TLS communication.        |
| `--peer-key-file`         | Private key for the etcd peer certificate.                          |
| `--peer-client-cert-auth` | Requires peer etcd members to authenticate with valid certificates. |
| `--peer-trusted-ca-file`  | CA certificate used to verify peer etcd member certificates.        |

6. Metrics and monitoring

| Options                 | Description                                               |
| ----------------------- | --------------------------------------------------------- |
| `--listen-metrics-urls` | URLs where etcd exposes metrics, commonly on port `2381`. |

7. Integrity and watch behavior

| Options                                         | Description                                                   |
| ----------------------------------------------- | ------------------------------------------------------------- |
| `--experimental-initial-corrupt-check`          | Enables an initial data corruption check when etcd starts.    |
| `--experimental-watch-progress-notify-interval` | Interval for sending watch progress notifications to clients. |

---

- example:

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: etcd
      image: registry.k8s.io/etcd:3.5.24-0
      imagePullPolicy: IfNotPresent
      command:
        - etcd
        - --advertise-client-urls=https://192.168.10.150:2379
        - --cert-file=/etc/kubernetes/pki/etcd/server.crt
        - --client-cert-auth=true
        - --data-dir=/var/lib/etcd
        - --experimental-initial-corrupt-check=true
        - --experimental-watch-progress-notify-interval=5s
        - --initial-advertise-peer-urls=https://192.168.10.150:2380
        - --initial-cluster=controlplane=https://192.168.10.150:2380
        - --key-file=/etc/kubernetes/pki/etcd/server.key
        - --listen-client-urls=https://127.0.0.1:2379,https://192.168.10.150:2379
        - --listen-metrics-urls=http://127.0.0.1:2381
        - --listen-peer-urls=https://192.168.10.150:2380
        - --name=controlplane
        - --peer-cert-file=/etc/kubernetes/pki/etcd/peer.crt
        - --peer-client-cert-auth=true
        - --peer-key-file=/etc/kubernetes/pki/etcd/peer.key
        - --peer-trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
        - --snapshot-count=10000
        - --trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
      volumeMounts:
        - mountPath: /var/lib/etcd
          name: etcd-data
        - mountPath: /etc/kubernetes/pki/etcd
          name: etcd-certs
  volumes:
    - hostPath:
        path: /etc/kubernetes/pki/etcd
        type: DirectoryOrCreate
      name: etcd-certs
    - hostPath:
        path: /var/lib/etcd
        type: DirectoryOrCreate
      name: etcd-data
```

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

## CLI: `etcdctl`

- `etcdctl`:
  - the **primary command-line client** for interacting with etcd over a network.
  - It is used for **day-to-day operations** such as managing keys and values, administering the cluster, checking health, and more.

- `etcdutl`:
  - an **administration utility** designed to **operate** directly on `etcd data files`,
  - including **migrating data** between etcd versions, **defragmenting** the database, **restoring** snapshots, and **validating** data consistency.

---

### Common Commands

- General

| Command                               | Description                                                                    |
| ------------------------------------- | ------------------------------------------------------------------------------ |
| `etcdctl version`                     | Show the etcdctl client version.                                               |
| `ETCDCTL_API=3 etcdctl version`       | Use etcdctl API version 3, which is the common version for modern Kubernetes.  |
| `etcdctl endpoint health`             | Check whether the etcd endpoint is healthy.                                    |
| `etcdctl endpoint status`             | Show etcd endpoint status, including leader, version, DB size, and raft index. |
| `etcdctl endpoint status -w table`    | Show endpoint status in table format. Easier to read.                          |
| `etcdctl member list`                 | List etcd cluster members.                                                     |
| `etcdctl member list -w table`        | List etcd members in table format.                                             |
| `etcdctl alarm list`                  | List etcd alarms, such as `NOSPACE`.                                           |
| `etcdctl alarm disarm`                | Clear active alarms after fixing the root cause.                               |
| `etcdctl defrag`                      | Defragment etcd database to reclaim space. Use carefully.                      |
| `etcdctl compact <revision>`          | Compact old revisions to reduce stored history.                                |
| `etcdctl lease list`                  | List leases.                                                                   |
| `etcdctl lease timetolive <lease-id>` | Show TTL information for a lease.                                              |

- Snapshot

| Command                                            | Description                                                                  |
| -------------------------------------------------- | ---------------------------------------------------------------------------- |
| `etcdctl snapshot status /backup/etcd.db -w table` | Check snapshot information, such as hash, revision, and size.                |
| `etcdctl snapshot save /backup/etcd.db`            | Save an etcd snapshot backup.                                                |
| `etcdctl snapshot restore /backup/etcd.db`         | Restore etcd data from a snapshot. Usually done outside the running cluster. |

- Key-value management

| Command                                                     | Description                                                                        |
| ----------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `etcdctl get / --prefix --keys-only`                        | List all keys in etcd. Be careful in production because this can return many keys. |
| `etcdctl get /registry --prefix --keys-only`                | List Kubernetes-related keys stored under `/registry`.                             |
| `etcdctl get /registry/pods --prefix --keys-only`           | List pod keys stored in etcd.                                                      |
| `etcdctl get /registry/namespaces --prefix --keys-only`     | List namespace keys stored in etcd.                                                |
| `etcdctl get /registry/services/specs --prefix --keys-only` | List service keys stored in etcd.                                                  |
| `etcdctl get <key>`                                         | Get the value of a specific key.                                                   |
| `etcdctl put <key> <value>`                                 | Create or update a key-value pair.                                                 |
| `etcdctl del <key>`                                         | Delete a key. Dangerous in Kubernetes etcd.                                        |
| `etcdctl watch <key>`                                       | Watch changes to a specific key.                                                   |
| `etcdctl watch <prefix> --prefix`                           | Watch changes under a key prefix.                                                  |

---

### Lab: `etcdctl`

#### etcd info

```sh
etcdctl version
# etcdctl version: 3.4.30
# API version: 3.4

# Check whether the etcd endpoint is healthy.
sudo -i ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379  \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt    \
  --cert=/etc/kubernetes/pki/etcd/server.crt  \
  --key=/etc/kubernetes/pki/etcd/server.key   \
  endpoint health
# https://127.0.0.1:2379 is healthy: successfully committed proposal: took = 11.80875ms

# Show etcd endpoint status
sudo -i ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379  \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt    \
  --cert=/etc/kubernetes/pki/etcd/server.crt  \
  --key=/etc/kubernetes/pki/etcd/server.key   \
  endpoint status
# https://127.0.0.1:2379, 6778ae6450f78ed5, 3.5.24, 26 MB, true, false, 12, 63315, 63315

# status in table format
sudo -i ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379  \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt    \
  --cert=/etc/kubernetes/pki/etcd/server.crt  \
  --key=/etc/kubernetes/pki/etcd/server.key   \
  endpoint status -w table
# +------------------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
# |        ENDPOINT        |        ID        | VERSION | DB SIZE | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS |
# +------------------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
# | https://127.0.0.1:2379 | 6778ae6450f78ed5 |  3.5.24 |   26 MB |      true |      false |        12 |      63846 |              63846 |        |
# +------------------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+

# List etcd cluster members.
sudo -i ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379  \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt    \
  --cert=/etc/kubernetes/pki/etcd/server.crt  \
  --key=/etc/kubernetes/pki/etcd/server.key   \
  member list
# 6778ae6450f78ed5, started, controlplane, https://192.168.10.150:2380, https://192.168.10.150:2379, false


# List etcd members in table format.
sudo -i ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379  \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt    \
  --cert=/etc/kubernetes/pki/etcd/server.crt  \
  --key=/etc/kubernetes/pki/etcd/server.key   \
  member list -w table
# +------------------+---------+--------------+-----------------------------+-----------------------------+------------+
# |        ID        | STATUS  |     NAME     |         PEER ADDRS          |        CLIENT ADDRS         | IS LEARNER |
# +------------------+---------+--------------+-----------------------------+-----------------------------+------------+
# | 6778ae6450f78ed5 | started | controlplane | https://192.168.10.150:2380 | https://192.168.10.150:2379 |      false |
# +------------------+---------+--------------+-----------------------------+-----------------------------+------------+

# List etcd alarms
sudo -i ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379  \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt    \
  --cert=/etc/kubernetes/pki/etcd/server.crt  \
  --key=/etc/kubernetes/pki/etcd/server.key   \
  alarm list
# none


```

---

#### Key-value

```sh
# list every key stored in etcd —
sudo -i ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379  \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt    \
  --cert=/etc/kubernetes/pki/etcd/server.crt  \
  --key=/etc/kubernetes/pki/etcd/server.key   \
  get / --prefix --keys-only
# /registry/apiextensions.k8s.io/customresourcedefinitions/adminnetworkpolicies.policy.networking.k8s.io
# /registry/apiextensions.k8s.io/customresourcedefinitions/apiservers.operator.tigera.io
# /registry/apiextensions.k8s.io/customresourcedefinitions/backendtlspolicies.gateway.networking.k8s.io
# /registry/apiextensions.k8s.io/customresourcedefinitions/baselineadminnetworkpolicies.policy.networking.k8s.io
# /registry/apiextensions.k8s.io/customresourcedefinitions/bfdprofiles.metallb.io
# /registry/apiextensions.k8s.io/customresourcedefinitions/bgpadvertisements.metallb.io
# ...

# List pod keys stored in etcd
sudo -i ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379  \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt    \
  --cert=/etc/kubernetes/pki/etcd/server.crt  \
  --key=/etc/kubernetes/pki/etcd/server.key   \
  get /registry/namespaces --prefix --keys-only
# /registry/namespaces/calico-system
# /registry/namespaces/default
# /registry/namespaces/ingress-nginx
# /registry/namespaces/kube-node-lease
# /registry/namespaces/kube-public
# /registry/namespaces/kube-system
# /registry/namespaces/local-path-storage
# /registry/namespaces/metallb-system
# /registry/namespaces/nginx-gateway
# /registry/namespaces/tigera-operator
# ...

# List pod keys store
sudo -i ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379  \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt    \
  --cert=/etc/kubernetes/pki/etcd/server.crt  \
  --key=/etc/kubernetes/pki/etcd/server.key   \
  get /registry/namespaces/nginx-gateway
# /registry/namespaces/nginx-gateway
# k8s

# v1      Namespace�
# �
# nginx-gateway␦"*$4f5a093c-3bc8-48b4-a58f-759a3cdea7b42ܜ��Z,
# nginx-gatewayb�tadata.name
# 0kubectl.kubernetes.io/last-applied-configuration\{"apiVersion":"v1","kind":"Namespace","metadata":{"annotations":{},"name":"nginx-gateway"}}
# ��
# kubectl-client-side-applyUpdate␦vܜ��FieldsV1:�
# �{"f:metadata":{"f:annotations":{".":{},"f:kubectl.kubernetes.io/last-applied-configuration":{}},"f:labels":{".":{},"f:kubernetes.io/metadata.name":{}}}}B


# kubernetes␦
# Active␦"

# put a key
sudo -i ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379  \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt    \
  --cert=/etc/kubernetes/pki/etcd/server.crt  \
  --key=/etc/kubernetes/pki/etcd/server.key   \
  put myKey "my key"
# OK

# confirm
sudo -i ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379  \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt    \
  --cert=/etc/kubernetes/pki/etcd/server.crt  \
  --key=/etc/kubernetes/pki/etcd/server.key   \
  get myKey
# myKey
# my key

# delete
sudo -i ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379  \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt    \
  --cert=/etc/kubernetes/pki/etcd/server.crt  \
  --key=/etc/kubernetes/pki/etcd/server.key   \
  del myKey
# 1

# confirm
sudo -i ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379  \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt    \
  --cert=/etc/kubernetes/pki/etcd/server.crt  \
  --key=/etc/kubernetes/pki/etcd/server.key   \
  get myKey
# none
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

---

## Security

- main concerns:
- **Plain Text Data storage**
  - By **default**, `etcd` store data **in plain text**.
    - sensitive data, like Sectets, can be read directly from the disk.
  - Attack
    - if an attacker gets access to etcd, the secrets in plain text can be read.

---

- **TLS encryption**
  - The data in-transit between `API server` and `ETCD` can also be **intercepted**
  - mitigation: start etcd with cert file

  ```sh
  etcd  \
  --cert-file=/etc/kubernetes/pki/etcd/server.crt   \
  --key-file=/etc/kubernetes/pki/etcd/server.key
  ```

---

- **Authentication**
  - Without authentication, any client can connect to etcd and modify data.
  - mitigation: enable authentication

- Types of Authentication

  | Feature        | Username / Passwords                    | Certificates                                        |
  | -------------- | --------------------------------------- | --------------------------------------------------- |
  | Security Level | Lower                                   | Higher (certificates are harder to forge)           |
  | Ease of Use    | Easier to configure and manage          | More complex to set up and maintain                 |
  | Best Use Case  | Simple setups, development environments | Production environments, high-security applications |

- How trust is established:
- using `mTLS (Mutual Transport Layer Security)`
  - a security protocol that requires both parties in a network connection to verify their identities to each other
  - A `CA (Certificate Authority)` signs both the server and client certs
  - `etcd` **trusts** any client whose `cert` was signed by that `CA`
  - The client **trusts** etcd because its `cert` was also signed by the same `CA`
  - `Private keys` never leave their respective machines

- Mitigation: enable mtls

```sh
etcd    \
# enforce mTLS
--client-cert-auth=true             \
# trust this CA
--trusted-ca-file=etcd/ca.crt       \
# etcd's identity
--cert-file=etcd/server.crt         \
# etcd's private key
--key-file=etcd/server.key          \
# peer CA
--peer-trusted-ca-file=etcd/ca.crt  \
# peer identity
--peer-cert-file=etcd/peer.crt      \
# peer private key
--peer-key-file=etcd/peer.key
```

---

### Lab: etcd security

#### Plain Text Data Storage: Demo

```sh
# put a key-value item
sudo -i ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379  \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt    \
  --cert=/etc/kubernetes/pki/etcd/server.crt  \
  --key=/etc/kubernetes/pki/etcd/server.key   \
  put myKey "plain text storage"
# OK

# confirm
sudo -i ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379  \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt    \
  --cert=/etc/kubernetes/pki/etcd/server.crt  \
  --key=/etc/kubernetes/pki/etcd/server.key   \
  get myKey
# myKey
# plain text storage

# search key at etcd data dir
sudo -i grep -R "myKey" /var/lib/etcd/member
# grep: /var/lib/etcd/member/wal/0000000000000001-00000000000091dd.wal: binary file matches
# grep: /var/lib/etcd/member/snap/db: binary file matches
```

---

#### TLS Encryption: Demo

- Note: by default, the kubeadm enable cert-file and key-file for tls

```sh
k logs etcd-controlplane  -n kube-system | grep secure
# {"level":"info","ts":"2026-06-05T17:55:56.632538Z","caller":"embed/serve.go:275","msg":"serving client traffic securely","traffic":"grpc+http","address":"127.0.0.1:2379"}
# {"level":"info","ts":"2026-06-05T17:55:56.632792Z","caller":"embed/serve.go:275","msg":"serving client traffic securely","traffic":"grpc+http","address":"192.168.10.150:2379"}
```

- The following show the idea for unencrypted case.

```sh
# confirm etcd is running on port 2379 for client
sudo -i ss -tlnp | grep 2379
# LISTEN 0      4096   192.168.10.150:2379       0.0.0.0:*    users:(("etcd",pid=71680,fd=8))
# LISTEN 0      4096        127.0.0.1:2379       0.0.0.0:*    users:(("etcd",pid=71680,fd=7))

# put a key-value item
sudo -i ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379  \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt    \
  --cert=/etc/kubernetes/pki/etcd/server.crt  \
  --key=/etc/kubernetes/pki/etcd/server.key   \
  put myKey "plain text storage"


# new tab: tcpdump
tcpdump -i lo -X port 2379
```
