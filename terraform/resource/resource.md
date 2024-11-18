# Terraform - Language: Resource

[Back](../index.md)

- [Terraform - Language: Resource](#terraform---language-resource)
  - [Resources](#resources)
  - [Resource Blocks](#resource-blocks)
    - [Resource Types](#resource-types)
    - [Providers](#providers)
    - [Resource Arguments](#resource-arguments)
    - [Documentation for Resource Types](#documentation-for-resource-types)
  - [Meta-Arguments](#meta-arguments)
  - [Removing Resources](#removing-resources)

---

## Resources

- `Resources`

  - the most important element in the Terraform language.
  - Each `resource block` **describes** one or more **infrastructure objects**, such as virtual networks, compute instances, or higher-level components such as DNS records.

- `Resource Blocks`

  - used to document the syntax for declaring resources.

- `Resource Behavior`

  - **explains** in more detail **how** Terraform **handles** resource declarations **when applying** a configuration.

- `Meta-Arguments section`

  - used to document **special arguments** that can be used with **every resource type**, including depends_on, count, for_each, provider, and lifecycle.

- `Provisioners`
  - used to document **configuring post-creation actions** for a resource using the provisioner and connection blocks.
  - Since `provisioners` are non-declarative and potentially unpredictable, we strongly recommend that you treat them as a last resort.

---

## Resource Blocks

- **Resource Syntax**
- `resource block`

  - declares a **resource** of a specific **type** with a specific **local name**.
  - Terraform **uses the name when referring to the resource** in the same module, but it has no meaning outside that module's scope.

- The resource **type** and **name** must be **unique** within a module because they serve as an **identifier** for a given resource.
- **Resource names** must

  - start with a **letter** or **underscore**
  - may contain only **letters**, **digits**, **underscores**, and **dashes**.

- Example:

```conf
# declear an ec2 instance

resource "aws_instance" "web" {
  ami = "ami-a1b2c3d4"
  instance_type = "t2.micro"
}
```

- Within the `block body` (between `{` and `}`) are the **configuration arguments** for the resource itself.

  - The **arguments** often depend on the **resource type**. In this example, both ami and instance_type are special arguments for the aws_instance resource type.

---

### Resource Types

- Each `resource` is **associated** with a single resource **type**, which determines the kind of infrastructure object it manages and what arguments and other attributes the resource supports.

### Providers

- `Providers`

  - a **plugin** for Terraform that offers a collection of **resource types**.

- Each resource **type** is implemented by a `provider`.
- A `provider` provides resources to manage a single cloud or on-premises **infrastructure platform**.
- Providers are **distributed separately** from Terraform, but Terraform can automatically install most providers when initializing a working directory.
- To manage resources, a Terraform `module` **must specify** the required `providers`.

- Most `providers` need some **configuration to access** their remote `API`, which is provided by the `root module`.

- Based on a resource **type's name**, Terraform can usually **determine which provider to use**.
  - **By convention**, resource **type names** **start** with their provider's **preferred local name**.
  - When using **multiple** configurations of a provider or **non**-preferred local provider names, you must use the `provider meta-argument` to **manually** choose a provider configuration.

### Resource Arguments

- Most of the **arguments** within the body of a resource block are specific to the selected **resource type**.

  - The resource type's documentation lists which arguments are available and how their values should be formatted.

  - The **values** for resource arguments can make full use of **expressions** and other **dynamic Terraform language features**.

- `Meta-arguments` are defined by Terraform and **apply across all** resource types.

---

### Documentation for Resource Types

- Every Terraform `provider` has its **own documentation**, describing its resource types and their arguments.

- Some provider documentation is still part of Terraform's core documentation, but the `Terraform Registry` is the **main home** for all publicly available `provider` docs.

---

## Meta-Arguments

- The Terraform language defines the following meta-arguments:
  - `depends_on`:for specifying **hidden dependencies**
  - `count`: for creating **multiple** resource instances according to a count
  - `for_each`: to create multiple instances according to a **map**, or **set** of strings
  - `provider`: for selecting a `non-default provider` configuration
  - `lifecycle`: for lifecycle customizations
  - `provisioner`: for taking **extra actions after resource creation**

---

## Removing Resources

- To remove a resource from Terraform, simply **delete** the `resource block` from your Terraform configuration.

  - By **default**, after you **remove** the `resource block`, Terraform will **plan to destroy** any real infrastructure object managed by that resource.

- Sometimes you may wish to remove a resource from your Terraform configuration **without destroying the real infrastructure object** it manages. In this case, the resource will be **removed** from the `Terraform state`, but the real infrastructure object will not be destroyed.

- To declare that a resource was removed from Terraform configuration but that its managed object should not be destroyed, remove the resource block from your configuration and replace it with a removed block:

```conf
removed {
  from = aws_instance.example

  lifecycle {
    destroy = false
  }
}
```

---

[TOP](#terraform---language-resource)
