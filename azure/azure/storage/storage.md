# Azure - Storage

[Back](../index.md)

- [Azure - Storage](#azure---storage)
  - [Common Services](#common-services)

---

## Common Services

- `Storage Account`
  - the management boundary for Azure Storage.
    - create one first, then create storage services inside it.
  - managed storage objects by providing:
    - namespace,
    - networking rules,
    - access control,
    - redundancy settings,
    - and billing boundary.

- `Azure Storage(GPv2)` / `Standard storage`
  - 4 types of data:
    - container
    - file
    - queue
    - table

- Common Services:
  - `Managed Disks`:
    - block storage volumes for Azure VMs.
    - ≈ `Amazon EBS`
  - `Azure Files`:
    - managed shared file storage.
    - shares files that can be mounted using SMB or NFS.
    - ≈ `Amazon EFS` / `FSx`
  - `Blob Storage`: object storage
    - block storage for VMs
    - `container`: top-level object grouping.
    - ≈ Amazon S3
  - `Queue Storage`:
    - a simple message queue.
    - ≈ Amazon SQS
  - `Table Storage`:
    - a simple NoSQL key-value/table storage service.
    - ≈ DynamoDB

---
