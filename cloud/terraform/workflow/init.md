# Terraform - Init

[Back](../index.md)

- [Terraform - Init](#terraform---init)
  - [Init](#init)
    - [Common Commands](#common-commands)

---

## Init

- `terraform init`
  - initializes a new or existing working directory.

---

### Common Commands

| Command                         | Description                                                         |
| ------------------------------- | ------------------------------------------------------------------- |
| `terraform init`                | **initializes** a working directory.                                |
| `terraform init -migrate-state` | copy existing state to the new backend **with interactive prompts** |
| `terraform init -force-copy`    | force to copy existing state to the new backend **without prompt**  |
| `terraform init -reconfigure`   | re-initializes disregarding any existing configuration              |
| `terraform init -upgrade`       | updating all modules to the latest available source code            |

- **reconfigure:**
  - if **previous** backend is **corrupt or inaccessible** (e.g., a deleted S3 bucket)
  - if switching environments in a CI/CD pipeline and want to point to a **new backend without moving data**.

- **migrate-state**
  - when moving from **local state** to a **remote backend** (like S3 or Azure Blob)
  - when **renaming a backend key/bucket**.

- **upgrade**
  - when adding modules
