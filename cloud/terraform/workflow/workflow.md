# Terraform workflow

[Back](../index.md)

- [Terraform workflow](#terraform-workflow)
  - [Workflow](#workflow)
    - [Common Commands](#common-commands)

---

## Workflow

- Workflow
  - write -> Plan -> Apply
  - `terraform init` -> `terraform validate` -> `terraform plan` -> `terraform apply`

- Plan with a planfile is recommended `terraform plan planfile`
  - a way to save the changes to be applied.

- Common CICD:
  - `terraform init`
  - `terraform validate`
  - `terraform plan planfile`
  - `terraform apply planfile -auto-approve`

---

- For a specific resource
  - When working for a big project that includs a large mount of resource, the terrafor plan step might take a long time.
  - To speed up without checking all of the resources, `terraform apply -target resource_type.resource_name plan_file` can be used.
  - **ONLY USE in DEV**

---

### Common Commands

| Command                                          | Description                                                                 |
| ------------------------------------------------ | --------------------------------------------------------------------------- |
| `terraform fmt`                                  | Rewrites Terraform configuration files to a canonical format.               |
| `terraform validate`                             | Checks whether the configuration files are valid.                           |
| `terraform plan`                                 | Creates an execution plan showing the changes that Terraform plans to make. |
| `terraform plan -out plan_file`                  | Save the generated plan to a file on disk                                   |
| `terraform apply`                                | Creates and executes a new execution plan with an interative prompt         |
| `terraform apply -target module.module_name`     | Apply only a module                                                         |
| `terraform apply plan_file`                      | Apply a plan from a file                                                    |
| `terraform apply -auto-approve`                  | Skips interactive approval of the plan                                      |
| `terraform destroy`                              | Destroys the Terraform-managed infrastructure.                              |
| `terraform destroy -auto-approve`                | Skips interactive approval of the plan                                      |
| `terraform destroy -target aws_instance.example` | Destroys a specific infrastructure.                                         |
| `terraform refresh`                              | Updates the state file against real resources in a provider.                |
| `terraform state`                                | Advanced state management commands for your Terraform state.                |
| `terraform output`                               | Displays outputs from your Terraform state data.                            |
