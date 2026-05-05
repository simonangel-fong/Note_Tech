# Terraform - Import

[Back](../index.md)

- [Terraform - Import](#terraform---import)
  - [Terraform Import](#terraform-import)
    - [Commands](#commands)
    - [Declarative](#declarative)
  - [Best Practices](#best-practices)
  - [Lab: Import](#lab-import)
    - [`resource` block + `terraform import` command](#resource-block--terraform-import-command)
    - [`resource` block + `import{}` block](#resource-block--import-block)
    - [`import{}` block + `terraform plan -generate-config-out`](#import-block--terraform-plan--generate-config-out)

---

## Terraform Import

- `terraform import`
  - brings **existing infrastructure** into `Terraform state` so Terraform can start managing it.
  - imports the resource into the state file
  - does not automatically create full Terraform code
  - After importing, **always run** `terraform plan`

- **Features**
  - **Tracks manually created** cloud resources in Terraform
  - Supports importing into `root modules` and `child modules`
  - Supports resources using `count` and `for_each`
  - Helps **migrate existing infrastructure** to `Infrastructure as Code`
  - Supports **declarative** `import blocks` in newer Terraform versions

- **Use Cases**
  - **Import** manually created AWS resources into Terraform
  - **Migrate** old infrastructure to Terraform without recreating it
  - **Recover** resources missing from Terraform state
  - Bring production resources under IaC management gradually
  - **Refactor** infrastructure into Terraform modules

---

### Commands

| command                                             | description                                                 |
| --------------------------------------------------- | ----------------------------------------------------------- |
| `terraform state pull > backup.tfstate`             | Backup the current Terraform state                          |
| `terraform import <resource_address> <resource_id>` | Import an existing resource into Terraform state            |
| `terraform state show <resource_address>`           | Show imported resource details from state                   |
| `terraform plan`                                    | Check if Terraform wants to change the imported resource    |
| `terraform apply`                                   | Apply changes after confirming the plan is safe             |
| `terraform state list`                              | List all resources currently tracked in state               |
| `terraform state rm <resource_address>`             | Remove a resource from state without deleting it from cloud |
| `terraform refresh`                                 | Update state based on real infrastructure; use carefully    |

---

### Declarative

```hcl
import {
  to = aws_s3_bucket.logs
  id = "my-existing-bucket"
}

resource "aws_s3_bucket" "logs" {
  bucket = "my-existing-bucket"
}
```

Then run:

```sh
terraform plan
terraform apply
```

---

## Best Practices

- Common steps
  1. **Backup** state before importing
  2. **Write the matching resource block** before import
  3. Check the provider documentation for the correct resource ID
  4. **Import** one resource at a time
  5. Run `terraform plan` after every import.
     - **No Change**

- Dos and donts
  - Do not import the same cloud resource into multiple Terraform addresses
  - Avoid mixing import work with new infrastructure changes
  - Use remote backend and state locking for team or production environments

---

## Lab: Import

### `resource` block + `terraform import` command

```hcl
resource "aws_vpc" "main" {
  count      = 1
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "my-vpc-${count.index}"
  }
}
```

```sh
cd infra
terraform init
terraform fmt && terraform validate

terraform state list
# none

# backup
terraform state pull > backup.tfstate

terraform import aws_vpc.main[0] vpc-09ba80f07e9c0937a
# aws_vpc.main[0]: Importing from ID "vpc-09ba80f07e9c0937a"...
# aws_vpc.main[0]: Import prepared!
#   Prepared aws_vpc for import
# aws_vpc.main[0]: Refreshing state... [id=vpc-09ba80f07e9c0937a]

# Import successful!

# The resources that were imported are shown above. These resources are now in
# your Terraform state and will henceforth be managed by Terraform.

# confirm
terraform state list
# aws_vpc.main[0]

# confirm: no changes
terraform plan
# aws_vpc.main[0]: Refreshing state... [id=vpc-09ba80f07e9c0937a]

# No changes. Your infrastructure matches the configuration.

# Terraform has compared your real infrastructure against your configuration and found no differences, so no changes are needed.
```

---

### `resource` block + `import{}` block

```hcl
resource "aws_vpc" "main" {
  count      = 2  # update count
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "my-vpc-${count.index}"
  }
}

import {
  id = "vpc-03c724534178bc067"
  to = aws_vpc.main[1]
}
```

```sh
# update state file
terraform refresh
# aws_vpc.main[1]: Preparing import... [id=vpc-03c724534178bc067]
# aws_vpc.main[1]: Refreshing state... [id=vpc-03c724534178bc067]
# aws_vpc.main[0]: Refreshing state... [id=vpc-09ba80f07e9c0937a]

# confirm
terraform state list
# aws_vpc.main[0]
# aws_vpc.main[1]

terraform plan
# aws_vpc.main[1]: Refreshing state... [id=vpc-03c724534178bc067]
# aws_vpc.main[0]: Refreshing state... [id=vpc-09ba80f07e9c0937a]

# No changes. Your infrastructure matches the configuration.

# Terraform has compared your real infrastructure against your configuration and found no differences, so no changes are needed.

terraform apply
# aws_vpc.main[1]: Refreshing state... [id=vpc-03c724534178bc067]
# aws_vpc.main[0]: Refreshing state... [id=vpc-09ba80f07e9c0937a]

# No changes. Your infrastructure matches the configuration.

# Terraform has compared your real infrastructure against your configuration and found no differences, so no changes are needed.

# Apply complete! Resources: 0 added, 0 changed, 0 destroyed.
```

---

### `import{}` block + `terraform plan -generate-config-out`

- add

```hcl
import {
  id = "vpc-030987a3bede89b90"
  to = aws_vpc.app
}
```

```sh
terraform plan -generate-config-out=generated.tf

terraform refresh
# aws_vpc.app: Preparing import... [id=vpc-030987a3bede89b90]
# aws_vpc.app: Refreshing state... [id=vpc-030987a3bede89b90]
# aws_vpc.main[1]: Refreshing state... [id=vpc-03c724534178bc067]
# aws_vpc.main[0]: Refreshing state... [id=vpc-09ba80f07e9c0937a]

terraform plan
# aws_vpc.main[0]: Refreshing state... [id=vpc-09ba80f07e9c0937a]
# aws_vpc.main[1]: Refreshing state... [id=vpc-03c724534178bc067]
# aws_vpc.app: Refreshing state... [id=vpc-030987a3bede89b90]

# No changes. Your infrastructure matches the configuration.

# Terraform has compared your real infrastructure against your configuration and found no differences, so no changes are needed.
```
