# Terraform - Data Source

[Back](../index.md)

- [Terraform - Data Source](#terraform---data-source)
  - [Data Source](#data-source)
    - [Custom Condition Checks](#custom-condition-checks)
  - [Common Data Source](#common-data-source)

---

## Data Source

- `Data sources`

  - allow Terraform to use **information defined outside** of Terraform, defined by another separate Terraform configuration, or modified by functions.

- many `data sources` correspond to an **infrastructure object type** that is accessed via a **remote network API**
- some specialized `data sources` operate only within **Terraform itself**, calculating some results and exposing them for use elsewhere.

- How it works

  - Terraform **reads** `data resources` during the **planning phase** when possible, but **announces** in the plan when it must defer reading resources until the **apply phase** to preserve the order of operations.

- declared using a `data block`

```terraform
data data_source ds_name {
    # query constraints
}
```

- cause Terraform to **read from a given data source** ("data_source") and **export** the result under the given **local name** ("ds_name").

  - The name is used to **refer to this resource** from elsewhere in the same Terraform module, but has no significance outside of the scope of a module.
  - **data source** + **name** = **identifier** for a given resource
  - must be **unique** within a module.

---

### Custom Condition Checks

- can use `precondition` and `postcondition blocks` to **specify assumptions and guarantees** about how the data source operates.

```terraform
data "aws_ami" "example" {
  id = var.aws_ami_id

  lifecycle {
    # The AMI ID must refer to an existing AMI that has the tag "nomad-server".
    postcondition {
      condition     = self.tags["Component"] == "nomad-server"
      error_message = "tags[\"Component\"] must be \"nomad-server\"."
    }
  }
}

```

## Common Data Source

- Example:

```terraform
# caller identity details, such as account ID and ARN, for the current AWS account.
data "aws_caller_identity" "current" {}

# current AWS region
data "aws_region" "current" {}

# list of availability zones available in the current AWS region
data "aws_availability_zones" "current" {}
```

- get the terraform remote state

```terraform
# get an existing remote s3 state
data "terraform_remote_state" "s3_remote_state"{
    backend = "s3"

    config = {
        bucket  = "bucket_name"
        key     = "key_name"
        region  = "region_name"
    }
}

# output vpc
output "remote_state_vpc_id" {
    value = data.terraform_remote_state.s3_remote_state.vpc_id
}
```
