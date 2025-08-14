# Terraform - State

[Back](../index.md)

- [Terraform - State](#terraform---state)
  - [States](#states)
    - [Lab: manipulate state](#lab-manipulate-state)
    - [Purpose](#purpose)
    - [State Storage](#state-storage)
    - [State Locking](#state-locking)
    - [Common Commands](#common-commands)
  - [Backend](#backend)
  - [Lab: S3 as backend](#lab-s3-as-backend)
    - [Specify variables using a config file](#specify-variables-using-a-config-file)
    - [Specify variables using Cli](#specify-variables-using-cli)
    - [Refer to the existing remote backend](#refer-to-the-existing-remote-backend)

---

## States

- `State`

  - used to **map real world resources** to your **configuration**, keep **track of metadata**, and to improve performance for large infrastructures.
    - the bindings between **objects in a remote system** and **resource instances declared in your configuration**.
    - When Terraform **creates** a remote object in response to a change of **configuration**, it will **record the identity of that remote object** against a particular resource instance, and then potentially **update or delete** that object in response to future **configuration changes**.
  - used to **determine which changes to make to your infrastructure**.

- `state file`

  - By default, a local file named `terraform.tfstate`
  - recommend storing it in HCP Terraform to version, encrypt, and securely share it with your team.
  - In `JSON` format
  - use `terraform state` command for modifications

- one-to-one mapping

  - **guaranteed** by Terraform being the one to **create** each object and **record its identity** in the state, or to **destroy** an object and then **remove the binding** for it.
  - It is the user's responsibility to ensure the one-to-one rule when the manual modification is applied with command `terraform import` or `terraform state rm`

- Format

  - `State` snapshots are stored in `JSON` format and new Terraform versions are generally **backward compatible** with state snapshots produced by earlier versions.


---

### Lab: manipulate state

- apply
- state list
- state show
- state mv
- state rm
- terraform import 

---

- Common use cases required to modify the state:
  - upgrade the tf version
  - rename a resource without recreating it
  - Change a key in a for_each withou recreating the resources
  - Change position of a resource in a list (resource[0], resource[1])
  - Stop managing a resource without destroying it.

---

### Purpose

- Terraform state is **required**.

- **Mapping to the Real World**

  - Terraform requires **some sort of database** to map Terraform **config** to the **real world**.
  - Not all resources support tags as identifier. Therefore, tf has to use its own state structure.

- **Metadata**

  - Terraform must also **track metadata**
    - i.e.,resource **dependencies**, a pointer to the provider configuration
  - To ensure correct operation, Terraform **retains a copy of the most recent set of dependencies** within the state.

- **Performance**

  - Terraform stores **a cache of the attribute values for all resources** in the state for a performance improvement.
  - default behavior:
    - for every plan and apply, Terraform will **sync** all resources in your state.
    - For larger infrastructures, querying every resource is too slow.
    - In these scenarios, the **cached state** is treated as the **record of truth**.

- **Syncing**
  - When working in a team, the state is used to keep operations will be applied to the same remote objects.
  - `Remote state` is the **recommended** solution to this problem.
    - Terraform can use `remote locking` as a measure to **avoid two or more different users accidentally running Terraform at the same time**, and thus **ensure** that each Terraform run begins **with the most recent updated state**.

---

### State Storage

- `Backends` determine where state is stored.
  - For example, the **local** (default) backend stores state in a local JSON file on disk. The Consul backend stores the state within Consul. Both of these backends happen to provide locking: **local** via **system APIs** and `Consul` via **locking APIs**.
- When using a **non-local backend**, Terraform will **not persist the state** anywhere on disk **except** in the case of a **non-recoverable error** where writing the state to the backend failed.
- In the case of an **error persisting the state to the backend**, Terraform will write the state **locally**.

  - This is to prevent data loss.
  - If this happens, the end user must **manually push the state to the remote backend** once the error is resolved.

- **Manual State Pull/Push**

| CMD                           | Desc                                                                                                  |
| ----------------------------- | ----------------------------------------------------------------------------------------------------- |
| `terraform state pull`        | manually retrieve the state from the remote state                                                     |
| `terraform state push`        | manually write the state to the remote state. (extremely dangerous and should be avoided if possible) |
| `terraform state push -force` | manually write the state to the remote state. (extremely dangerous and should be avoided if possible) |

- Even if using the -force flag, we recommend making a backup of the state with terraform state pull prior to forcing the overwrite.

---

### State Locking

- `State locking`

  - automatically **lock the state** for all operations that could write state.
    - If state locking fails, Terraform does not continue.
  - prevents others from acquiring the lock and potentially **corrupting** your state.

- `-lock=false` flag:

  - disable state locking
  - not recommend

- If **acquiring the lock** takes **longer** than expected, Terraform outputs a **status message**.

  - If Terraform does **not output** a message, state locking is **still occurring** if your backend supports it.

- S3: supported
  - `use_lockfile`:
    - Optional
    - Whether to use a lockfile for locking the state file.
    - Defaults to `false`.

```terraform
terraform {
 backend "s3" {
    bucket         = "your-terraform-state-bucket"
    key            = "path/to/your/statefile.tfstate"
    region         = "us-east-1"
    encrypt        = true
    use_lockfile   = true # Enables S3 native locking
  }
}
```

---

### Common Commands

| Command                              | Description                                                                                        |
| ------------------------------------ | -------------------------------------------------------------------------------------------------- |
| `terraform state list`               | Lists all resources in the Terraform state.                                                        |
| `terraform state show resource_name` | Displays detailed information about a specific resource in the Terraform state.                    |
| `terraform state mv`                 | Moves an item in the Terraform state. Useful for renaming resources without destroying/recreating. |
| `terraform state pull`               | Pulls the current state and outputs it to stdout.                                                  |
| `terraform state push`               | Updates remote state file with local state data.                                                   |
| `terraform state rm`                 | Removes items from the Terraform state.                                                            |
| `terraform state replace-provider`   | Updates the provider for a resource in the state.                                                  |
|                                      |                                                                                                    |

- `terraform state mv resource_old_label resource_new_label`
  - useful when just rename the resource label

---

## Backend

- `Terraform` uses **persisted state data** to **keep track of the resources** it manages.

- By **default**,

  - `Terraform` uses a backend called `local`
    - The local backend type stores state as a local file on disk.

- local file name: `terraform.tfstate`

  - created only when first apply

- When **applying** a plan that you previously saved to a file, Terraform uses the **backend configuration** stored in that file instead of the current backend settings.

- `backend block`

  - used to **store state** in a remote object.
  - used to specify **where** and **how** the backend **stores** configuration state.

- When you **change a backend's configuration**, you must run `terraform init` again to **validate** and **configure** the backend before you can perform any plans, applies, or state operations.

- When you **change backends**, Terraform gives you the option to **migrate** your state to the new backend.
  - This lets you adopt backends without losing any existing state.
  - Important: Before migrating to a new backend, we strongly recommend manually backing up your state by copying your terraform.tfstate file to another location.

---

- Common backend types:
  - **Local Storage**: The default backend for Terraform, where the state file is stored and managed in the local machine that runs Terraform
  - **AWS S3 Bucket**: The state file is stored and managed in an AWS S3 bucket.
  - **Azure Blob Storage**:The state file is stored and managed in Azure Blob Storage.
  - **Google Cloud Storage bucket**: The state file is stored and managed in a Google Cloud Storage bucket.
  - **Remote**:Stores state snapshots and executes Terraform CLI operations for HCP Terraform or supported Terraform CI/CD platform, like Spacelift
  - **Http**: Stores and manage state files in a server by fetching via GET, updating via POST, and deleting with DELETE.

---

- Partial configuration
  - When some or all of the arguments are omitted.

```sh
terraform init -backend-config=state.config
```

---

## Lab: S3 as backend

- `provider.tf`

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Configuring a remote backend
  backend "s3" {
    bucket = ""
    region = ""
    key    = ""
    dynamodb_table  = ""    # backend lock in dynamodb
  }
}
```

---

### Specify variables using a config file

- `state.config`

```config
# state.config
bucket = "your-bucket"
key    = "your-state.tfstate"
region = "eu-central-1"
profile= "Your_Profile"
```

- init with config file

```sh
`terraform init -backend-config="./state.config"`
```

---

### Specify variables using Cli

- if not using state.config, can use Command-line key/value pairs

```sh
# cli
terraform init \
    -backend-config="address=demo.consul.io" \
    -backend-config="path=example_app/terraform_state" \
    -backend-config="scheme=https"
```

---

### Refer to the existing remote backend

```terraform
data "terraform_remote_state" "network" {
  backend = "s3"
  config = {
    bucket = "terraform-state-prod"
    key    = "network/terraform.tfstate"
    region = "us-east-1"
  }
}
```
