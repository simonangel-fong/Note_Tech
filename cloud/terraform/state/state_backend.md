# Terraform - Backend

[Back](../index.md)

- [Terraform - Backend](#terraform---backend)
  - [Backend](#backend)
    - [Defautl Backend](#defautl-backend)
    - [Remote Backend](#remote-backend)
    - [Partial configuration for Backend: `terraform init -backend-config`](#partial-configuration-for-backend-terraform-init--backend-config)
  - [Lab: S3 as backend](#lab-s3-as-backend)
    - [Specify variables using a config file](#specify-variables-using-a-config-file)
    - [Specify variables using Cli](#specify-variables-using-cli)
    - [Refer to the existing remote backend](#refer-to-the-existing-remote-backend)

---

## Backend

- `backend`
  - determines where the `terraform.tfstate` file is stored and how state locking is handled.

---

### Defautl Backend

- Default backend:
  - `local`: stores state as a local file on disk.

```hcl
terraform {
  backend "local" {}
}
```

---

### Remote Backend

- `remote backend`
  - a configured, **shared location** for storing the `terraform.tfstate` file
  - a centralized, secure, and durable remote service
    - e.g., AWS S3, Azure Blob Storage, HCP Terraform.

- Benefits:
  - **Collaboration**:
    - Multiple team members can work on the same infrastructure, ensuring everyone uses the latest state.
  - **State Locking**:
    - Prevents concurrent modifications that could corrupt the state file.
  - **Security & Persistence**:
    - Stores state files away from local machines, often with encryption at rest.
  - **Version Control**:
    - Facilitates tracking changes over time and rolling back in case of failures.

- **Common backend types:**
  - **Local Storage**: The default backend for Terraform, where the state file is stored and managed in the local machine that runs Terraform
  - **AWS S3 Bucket**: The state file is stored and managed in an AWS S3 bucket.
  - **Azure Blob Storage**:The state file is stored and managed in Azure Blob Storage.
  - **Google Cloud Storage bucket**: The state file is stored and managed in a Google Cloud Storage bucket.
  - **Remote**:Stores state snapshots and executes Terraform CLI operations for HCP Terraform or supported Terraform CI/CD platform, like Spacelift
  - **Http**: Stores and manage state files in a server by fetching via GET, updating via POST, and deleting with DELETE.

- **S3 example**

```hcl
terraform {
  backend "s3" {
    bucket = ""
    key = ""
    region = ""
  }
}
```

---

### Partial configuration for Backend: `terraform init -backend-config`

- Partial configuration
  - When some or all of the arguments are omitted.
  - can be used to refer to different backend configuration

- 3 ways to pass configurations
  - interactive way, tf will ask
  - key/value pairs
  - a file

```sh
# key/value pairs
terraform init -backend-config="bucket=mybucket" \
  -backend-config="key=mykey"
  -backend-config="region=myregion"

# for dev
terraform init -backend-config=dev.config
# for test
terraform init -backend-config=test.config
# for prod
terraform init -backend-config=prod.config
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
