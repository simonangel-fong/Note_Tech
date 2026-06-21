# Azure - Storage: Blob Storage

[Back](../index.md)

---

## Blob Storage

- `Binary Large Object(Blob)`
  - any binary data
  - e.g., images, videos, audio, or log files

- `Blob storage`
  - stores **unstructured data** (like images, videos, and backups) as **individual objects** alongside rich metadata.

- `container`
  - organizes a set of blobs (files) in Azure Blob Storage, acting much like a **folder** in a file system.

- ≈ AWS

| Concept        | Azure Blob Storage | Amazon S3                      |
| -------------- | ------------------ | ------------------------------ |
| Top-Level Root | Storage Account    | AWS Account / Global Namespace |
| Data Folder    | Container          | Bucket                         |
| Individual     | FileBlob           | Object                         |

---

### Redundancy

- Redundancy
  - azure keeps 3 copies by default
- Global Redundancy
  - can choose global redundancy
  - keeps 6 copies
    - 3 locally, 3 in another region

---

### Access Tiers

- tiers:
  - `Hot`
    - dafualt
    - balanced access
  - `Cool`:
    - cheaper storage
    - expensive read/write operations
  - `Cold`:
    - much cheaper storage
    - more expensive read/write operations
  - `Archive`:
    - cannot get immediate access
    - cheapest storage
    - most expensive operations.

---

## Common Commands

- Storage Account

| Command                                                                                   | Description                   |
| ----------------------------------------------------------------------------------------- | ----------------------------- |
| `az storage account create --name <acc_name> --location canadacentral --sku Standard_LRS` | Create a storage account.     |
| `az storage account list`                                                                 | List storage accounts.        |
| `az storage account show --name <acc_name>`                                               | Show storage account details. |
| `az storage account show-connection-string --name <acc_name>`                             | Show the connection string.   |

- Container

| Command                                                                                     | Description                           |
| ------------------------------------------------------------------------------------------- | ------------------------------------- |
| `az storage container create --name <con_name> --account-name <acc_name> --auth-mode login` | Create a blob container.              |
| `az storage container list --account-name <acc_name> --auth-mode login`                     | List containers in a storage account. |
| `az storage container show --name <con_name> --account-name <acc_name> --auth-mode login`   | Show container details.               |
| `az storage container delete --name <con_name> --account-name <acc_name> --auth-mode login` | Delete a container.                   |

- blob file

| Command                                                                                                                                                  | Description                                |
| -------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| `az storage blob upload --account-name <acc_name> --container-name <con_name> --name <blob-name> --file <file-path> --auth-mode login`                   | Upload one file as a blob.                 |
| `az storage blob upload-batch --account-name <acc_name> --destination <con_name> --source ./dist --auth-mode login`                                      | Upload a local folder to a blob container. |
| `az storage blob list --account-name <acc_name> --container-name <con_name> --auth-mode login -o table`                                                  | List blobs in a container.                 |
| `az storage blob show --account-name <acc_name> --container-name <con_name> --name <blob-name> --auth-mode login`                                        | Show details for one blob.                 |
| `az storage blob download --account-name <acc_name> --container-name <con_name> --name <blob-name> --file <local-download-path> --auth-mode login`       | Download one blob.                         |
| `az storage blob download-batch --account-name <acc_name> --source <con_name> --destination ./downloaded --auth-mode login`                              | Download multiple blobs from a container.  |
| `az storage blob delete --account-name <acc_name> --container-name <con_name> --name <blob-name> --auth-mode login`                                      | Delete one blob.                           |
| `az storage blob delete-batch --account-name <acc_name> --source <con_name> --pattern "*.log" --auth-mode login`                                         | Delete multiple blobs matching a pattern.  |
| `az storage blob exists --account-name <acc_name> --container-name <con_name> --name <blob-name> --auth-mode login`                                      | Check whether a blob exists.               |
| `az storage blob url --account-name <acc_name> --container-name <con_name> --name <blob-name> --auth-mode login`                                         | Get the blob URL.                          |
| `az storage blob metadata show --account-name <acc_name> --container-name <con_name> --name <blob-name> --auth-mode login`                               | Show blob metadata.                        |
| `az storage blob metadata update --account-name <acc_name> --container-name <con_name> --name <blob-name> --metadata env=dev app=demo --auth-mode login` | Set custom metadata on a blob.             |

- Permission

| Command                                                                                                                                                                       | Description                                                       |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| `az storage container set-permission --name <con_name> --account-name <acc_name> --public-access blob --auth-mode login`                                                      | Allow public read access to individual blobs.                     |
| `az storage container set-permission --name <con_name> --account-name <acc_name> --public-access container --auth-mode login`                                                 | Allow public read and list access to the container.               |
| `az storage container set-permission --name <con_name> --account-name <acc_name> --public-access off --auth-mode login`                                                       | Make the container private again.                                 |
| `az storage container show-permission --name <con_name> --account-name <acc_name> --auth-mode login`                                                                          | Show public access setting for a container.                       |
| `az storage blob set-tier --account-name <acc_name> --container-name <con_name> --name <blob-name> --tier Cool --auth-mode login`                                             | Change blob access tier, for example Hot, Cool, Cold, or Archive. |
| `az storage blob copy start --account-name <acc_name> --destination-container <con_name> --destination-blob <new-blob-name> --source-uri <source-blob-url> --auth-mode login` | Start copying a blob.                                             |
| `az storage blob snapshot --account-name <acc_name> --container-name <con_name> --name <blob-name> --auth-mode login`                                                         | Create a blob snapshot.                                           |
| `az storage blob service-properties show --account-name <acc_name> --auth-mode login`                                                                                         | Show Blob service-level settings.                                 |
| `az storage account delete --name <acc_name> --resource-group rg-storage-demo`                                                                                                | Delete the storage account.                                       |
| `az group delete --name rg-storage-demo`                                                                                                                                      | Delete the whole resource group and all resources inside it.      |

---

```sh
az storage account create -n mysa454325245 -g azure-study -l canadacentral --sku Standard_LRS

az storage account list -o table

az storage account show --name mysa454325245

az storage account show-connection-string --name mysa454325245

az storage container create --name my-container --account-name mysa454325245 --auth-mode login
# {
#   "created": true
# }

az storage container list --account-name mysa454325245 --auth-mode login
# Name          Lease Status    Last Modified
# ------------  --------------  -------------------------
# my-container                  2026-06-21T17:07:46+00:00

az storage container show --name my-container --account-name mysa454325245 --auth-mode login -o table
# Name          Lease Status    Last Modified
# ------------  --------------  -------------------------
# my-container  unlocked        2026-06-21T17:07:46+00:00

az storage container delete --name my-container --account-name mysa454325245 --auth-mode login

az storage account delete -n mysa454325245
```
