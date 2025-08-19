# Terraform workflow

[Back](../index.md)

- [Terraform workflow](#terraform-workflow)
  - [Workflow](#workflow)

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
