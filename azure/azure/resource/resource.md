# Azure - Resource

[Back](../index.md)

- [Azure - Resource](#azure---resource)
  - [Resources \& Resource Groups](#resources--resource-groups)
  - [Common Commands](#common-commands)

---

## Resources & Resource Groups

```txt
Management Group: Personal-Learning
└── Subscription: Azure-Free-Trial
    └── Resource Group: rg-nginx-dev
        ├── Virtual Network
        ├── Subnet
        ├── Network Security Group
        ├── Public IP
        ├── Network Interface
        └── Virtual Machine running Nginx
```

---

- `resource`
  - one actual **Azure service** instance.

- `Resource Group`
  - a logical container for `resources`.
    - used to group related resources together, usually by application, environment, or project.
    - all services in a `resource group` have a **similar lifecycle**
  - associated with a region
  - any `resources` must belong to **one and only one** `resource group`
  - ~=`AWS tag-based` project grouping
    - like a project folder

---

- `Subscription`
  - the billing, quota, and access boundary.
  - Resources are created inside a subscription.
    - any `resources` must exist inside one `subscription`
  - controls:
    - billing
    - quotas
    - RBAC permissions
    - policies
    - resource limits
  - associated with a **payment method**
  - cannot nest another `subscription`
  - ~= `AWS accounts`
  - use cases:
    - separate business units within one ogranization.
    - separate by geography

- `subscription plan`
  - a billing and management boundary
  - free plan
  - pay as you go
  - enterprise agreement
  - Free credits

---

- `Management Group`
  - used to group subscriptions into a hierachy and manage them at scale
  - can nest another `Management Group`
  - ~=≈ `AWS Organizations` / `Organizational Units`
  - used for:
    - governance
    - policy assignment
    - RBAC inheritance
    - compliance rules
    - large enterprise structure
  - `subscription` can belong to 0 / 1 `Management Group`, no more.
  - One `Management Group` can have zero or multiple `subscriptions`

- `root management group` / `Tenant root group`:
  - the top-level container
    - can nest another `Management Group`
    - can have no more than 5 layers `Management Group`
  - By default, **no user** has default access to manage the `root management group`.

---

## Common Commands

| Command                                                      | Description                                              |
| ------------------------------------------------------------ | -------------------------------------------------------- |
| `az login`                                                   | Log in to Azure from CLI.                                |
| `az account show`                                            | Show the current active Azure subscription.              |
| `az account list -o table`                                   | List available subscriptions.                            |
| `az account set --subscription <subscription-id>`            | Set the active subscription.                             |
| `az group create --name rg-vm-demo --location canadacentral` | Create a resource group for the VM.                      |
| `az group list -o table`                                     | List resource groups.                                    |
| `az group delete`                                            | Delete the whole resource group and resources inside it. |
