# Kubernetes - Storage: CSI (Container Storage Interface)

[Back](../../index.md)

- [Kubernetes - Storage: CSI (Container Storage Interface)](#kubernetes---storage-csi-container-storage-interface)
  - [CSI (Container Storage Interface)](#csi-container-storage-interface)
  - [Install csi-driver](#install-csi-driver)

---

## CSI (Container Storage Interface)

- `CSI (Container Storage Interface)`
  - a standard that lets storage vendors create plugins for Kubernetes, enabling it to use various block and file storage systems (like Amazon EBS, NFS, etc.) without needing code changes in Kubernetes core, making storage management standardized, extensible, and independent of Kubernetes releases for provisioning, attaching, and mounting volumes for stateful apps.

## Install csi-driver

```sh
git clone https://github.com/kubernetes-csi/csi-driver-host-path.git
cd csi-driver-host-path

./deploy/kubernetes-latest/deploy.sh

kubectl apply -f ./examples/csi-storageclass.yaml
# storageclass.yaml
# storageclass.storage.k8s.io/csi-hostpath-sc created
```

---
