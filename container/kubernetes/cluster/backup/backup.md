# Backup

- Backup Candidate:
  - Resource Configuration
  - etcd Cluster
  - Persistent Volumes

---

- Resource Configuration
  - usually is the yaml files
    - usually store on git repo
  - output from the API server
    - `kubectl get all --all-namespace -o yaml > all-deploy-services.yaml`

---

- etcd cluster
  - store the state of the cluster
    - location: `etcd.service.--data-dir`
  - can take a snapshot database
    - `etcdctl snapshot save snapshot.db`
    - `etcdctl snapshot status snapshot.db`
  - restore:
    - `systemctl stop kube-apiserver`
    - add the backup as a new etcd
      - `etcdctl snapstho restore snapshot.db --data-dir /var/lib/etcd-from-backup`
    - update etcd
      - `etcd.service`
    - restart
      - `systemctl daemon-reload`
      - `systemctl restart etcd`
      - `systemctl start kube-apiserver`

```sh

etcdctl version

# Backing Up ETCD
# Using etcdctl (Snapshot-based Backup)
# To take a snapshot from a running etcd server, use:
ETCDCTL_API=3 etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  snapshot save /opt/snapshot-pre-boot.db

Required Options
--endpoints points to the etcd server (default: localhost:2379)

--cacert path to the CA cert

--cert path to the client cert

--key path to the client key


Using etcdutl (File-based Backup)
For offline file-level backup of the data directory:

etcdutl backup \
  --data-dir /var/lib/etcd \
  --backup-dir /backup/etcd-backup
This copies the etcd backend database and WAL files to the target location.

Checking Snapshot Status
You can inspect the metadata of a snapshot file using:

etcdctl snapshot status /backup/etcd-snapshot.db \
  --write-out=table
This shows details like size, revision, hash, total keys, etc. It is helpful to verify snapshot integrity before restore.

Restoring ETCD
Using etcdutl
To restore a snapshot to a new data directory:

etcdutl snapshot restore /opt/snapshot-pre-boot.db --data-dir /var/lib/etcd-restored

To use a backup made with etcdutl backup, simply copy the backup contents back into /var/lib/etcd and restart etcd.

Notes
etcdctl snapshot save is used for creating .db snapshots from live etcd clusters.

etcdctl snapshot status provides metadata information about the snapshot file.

etcdutl snapshot restore is used to restore a .db snapshot file.

etcdutl backup performs a raw file-level copy of etcd’s data and WAL files without needing etcd to be running.

```

| Command           | Description      |
| ----------------- | ---------------- |
| `etcdctl version` | Get etcd version |


https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/#backing-up-an-etcd-cluster

https://github.com/etcd-io/website/blob/main/content/en/docs/v3.5/op-guide/recovery.md

https://www.youtube.com/watch?v=qRPNuT080Hk



---

## Install 

- Install Go

```sh
sudo apt install golang

go version
# go version go1.23.8 linux/amd64
```

??

```sh
sudo apt install etcd-client
```


```sh
git clone -b v3.4.37 https://github.com/etcd-io/etcd.git
cd etcd

# Run the build script
./build

# Add the full path
sudo export PATH="$PATH:`pwd`/bin"

etcd --version
# WARNING: Package "github.com/golang/protobuf/protoc-gen-go/generator" is deprecated.
#         A future release of golang/protobuf will delete this package,
#         which has long been excluded from the compatibility promise.

# etcd Version: 3.4.37
# Git SHA: 1a36b4853
# Go Version: go1.23.8
# Go OS/Arch: linux/amd64

etcdctl version
# etcdctl version: 3.4.37
# API version: 3.4
```