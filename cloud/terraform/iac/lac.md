# Terraform - IaC

[Back](../index.md)

- [Terraform - IaC](#terraform---iac)
  - [IaC](#iac)
  - [Terraform](#terraform)
    - [Terraform provider versioning](#terraform-provider-versioning)
  - [Provisioner](#provisioner)

---

## IaC

- `Infrastructure As Code (IaC)`

  - instead of using UI, use code to manage infrastractures.

- Benefits
  - support code reusability
  - code can be instegrated with git/VCS to control version
  - enable code review
  - enable audit log

---

## Terraform

- Language
  - `HCL (Hashicorp Configuration Language)`
- Resole dependency

  - tf reads all `.tf` files and create a `resource graph` to determine the sequence of managing resources.

- tf workflow:

  - define resource with `.tf`
  - `terraform plan` to preview what will be applied
  - `terraform apply` to implement resource management.
    - **only the updated resources** need to be **changed**

- `Terraform core` contains

  - the language interpreter
  - CLI
  - how to interact with `providers`, not cloud provider API.

- `Terraform registry`

  - a platform to found different provders that support terraform.
  - https://registry.terraform.io/

- `Terraform providers`

  - contains the code to interact with API of cloud provider.
  - **shipped separately** whith their own **version numbering**
    - must be **installed separately** using `terraform init`
    - By default, tf download the **latest available version** of provider.
    - Good practices:
      - specify the provider with version in the `terraform {}` block.

```hcl
# AWS provider
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

# custom provider
terraform {
    required_providers{
        mycloud = {
            version = ">= 1.0.0"
            source = "mycorp/mycloud"   # tf cloud's private registry
        }
    }

    required_version = ">= 0.14"
}
```

---

- Provider Configuration

```terraform
provider "aws" {
    region = "us-east-1"
}
```

- Using alias meta-argument with multiple providers

```terraform
provider "aws" {
    region = "us-east-1"
}

provider "aws" {
    alias = "eu"        # using alias
    region = "eu-west-1"
}

resource "aws_instance" "myinstance"{
    provider = aws.eu
}

module "mymodule" {
    source = "./mymodule"
    providers = {
        aws = aws.eu
    }
}
```

---

### Terraform provider versioning

- Terraform provider versioning follows semantic versioning:
  - `MAJOR.MINOR.PATCH`
    - `MAJOR`: new breaking changes
    - `MINOR`: new features
    - `PATCH`: bug fixes only

---

## Provisioner

- `Provisioner`

  - enable actions that cannot be directly expressed through resource configurations.
  - separate flows that cannot be fully controlled by terraform.
  - add a considerate amount of complexity and uncertainty
    - if something are misconfigured, it might lead time out, making a tf workflow fail.
  - requires more coordination
    - ie, a script for apt update requires:
      - sg
      - internet access
      - VPN, if internet is not available

- Types of provisioner

  - `Local-provisioner`
    - execute scripts/commands locally.
  - `Remote-provisioner`
    - execute scripts/commands remotely, like on a VM.
  - `Packer`
    - used to build and launch AMI.
  - `Cloud init`
    - using user_data and AWS API to pass a script required only at creation.

- **!ONLY USE Provisioner AS LAST RESORT**.
