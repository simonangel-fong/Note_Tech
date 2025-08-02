# Terraform - Remote Backend

[Back](../index.md)

- [Terraform - Remote Backend](#terraform---remote-backend)
  - [Backend](#backend)
  - [Lab: S3 as backend](#lab-s3-as-backend)
    - [Specify variables using a config file](#specify-variables-using-a-config-file)
    - [Specify variables using Cli](#specify-variables-using-cli)

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
