# Terraform - Common Commands

[Back](../index.md)

- [Terraform - Common Commands](#terraform---common-commands)
  - [Common Commands](#common-commands)

---

## Common Commands

- Init

| Command                         | Description                                                                   |
| ------------------------------- | ----------------------------------------------------------------------------- |
| `terraform init`                | initializes a working directory according to a Terraform configuration files. |
| `terraform init -migrate-state` | copy existing state to the new backend with interactive prompts               |
| `terraform init -force-copy`    | force to copy existing state to the new backend without prompt                |
| `terraform init -reconfigure`   | re-initializes disregarding any existing configuration                        |
| `terraform init -upgrade`       | updating all modules to the latest available source code                      |

- Workflow

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

- Other

| Command                                         | Description                                         |
| ----------------------------------------------- | --------------------------------------------------- |
| `terraform -h`                                  | Show help                                           |
| `terraform version`                             | Prints the Terraform version.                       |
| `terraform console`                             | Try expression in an interactive prompt.            |
| `terraform force-unlock`                        | Release a stuck lock                                |
| `terraform import RESOURCE_TYPE.ID RESOURCE_ID` | import existing infrastructure into Terraform state |
| `terraform providers`                           | Show the providers                                  |
| `terraform refresh`                             | Update the state to match resource objects          |
| `terraform show`                                | Show the current state                              |
| `terraform taint resource_name`                 | Mark a resource instance as not fully funciontal    |
| `terraform untaint resource_name`               | Remove the 'tainted' state from a resource instance |
| `terraform untaint resource_name`               | Remove the 'tainted' state from a resource instance |
