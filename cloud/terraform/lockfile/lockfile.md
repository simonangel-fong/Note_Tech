# Terraform - Fundamental: Lockfile

[Back](../index.md)

- [Terraform - Fundamental: Lockfile](#terraform---fundamental-lockfile)
  - [Lockfile](#lockfile)

---

## Lockfile

- `lockfile`
  - used to track the versions of providers and modules.
  - created when the command `terraform init` is issued.
    - file name: `.terraform.lock.hcl`
  - updated when the provider is changed.
  - lockfile should be committed to git
    - the re-run of terraform will use the same provider/module, especially when terraform is ran by other members.
