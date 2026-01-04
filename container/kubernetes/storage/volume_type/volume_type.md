# Kubernetes - Storage: Volume Types

[Back](../../index.md)

- [Kubernetes - Storage: Volume Types](#kubernetes---storage-volume-types)
  - [Volume Types](#volume-types)

---

## Volume Types

- `emptyDir`
  - A simple **directory** that allows the `pod` to store data **for the duration of its life cycle**.
  - The directory is created **just before** the `pod` **starts** and is **initially empty**.
- `hostPath`
  - Used for **mounting files** from the `worker node’s` **filesystem** into the `pod`.
- `configMap`, `secret`, `downwardAPI`, and the projected volume type
  - Special types of volumes used to **expose information** about the pod and other **Kubernetes objects** through files.
  - typically used to **configure the application** running in the `pod`.
- `persistentVolumeClaim`
  - A portable way to **integrate external storage** into pods.
  - points to a `PersistentVolumeClaim` **object** that **points** to a `PersistentVolume` object that finally references the actual storage.
- `nfs`
  - An **NFS share** mounted into the pod.
- `gcePersistentDisk(Google Compute Engine Persistent Disk)`, `awsElasticBlockStore (Amazon Web Services Elastic Block Store)`, `azureFile (Microsoft Azure File Service)`, `azureDisk (Microsoft Azure Data Disk)`
  - Used for mounting **cloud provider**-specific storage.
- `cephfs`, `cinder`, `fc`, `flexVolume`, `flocker`, `glusterfs`, `iscsi`, `portworxVolume`, `quobyte`, `rbd`, `scaleIO`, `storageos`, `photonPersistentDisk`, `vsphereVolume`
  - Used for mounting other types of **network storage**.
- `csi`
  - A pluggable way of **adding storage via** the `Container Storage Interface`.
  - allows anyone to implement their own storage driver that is then referenced in the csi volume definition.

---
