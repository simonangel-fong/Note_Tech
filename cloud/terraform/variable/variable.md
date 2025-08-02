# Terraform - Language: Variable

[Back](../index.md)

- [Terraform - Language: Variable](#terraform---language-variable)
  - [Variable](#variable)
  - [Input Variables](#input-variables)
    - [Declaring an Input Variable](#declaring-an-input-variable)
    - [Arguments](#arguments)
      - [Type Constraints](#type-constraints)
      - [Type Example](#type-example)
      - [Custom Validation Rules](#custom-validation-rules)
    - [Using Input Variable Values](#using-input-variable-values)
    - [Assigning Values to Root Module Variables](#assigning-values-to-root-module-variables)
      - [Variables on the Command Line](#variables-on-the-command-line)
      - [Variable Definitions (`.tfvars`) Files](#variable-definitions-tfvars-files)
      - [Environment Variables](#environment-variables)
  - [Output Values](#output-values)
      - [Declaring an Output Value](#declaring-an-output-value)
  - [Local Values](#local-values)
    - [Declaring a Local Value](#declaring-a-local-value)
    - [Using Local Values](#using-local-values)

---

## Variable

- `Variable`

  - Terraform blocks for requesting or publishing named **values**.

- `Input Variables`

  - serve as **parameters** for a `Terraform module`, so users can **customize** behavior without editing the source.

- `Output Values`

  - are like **return values** for a `Terraform module`.

- `Local Values`
  - a convenience feature for assigning a short name to an expression.
  - like a function's **temporary local variables**.

---

## Input Variables

- `Input Variables`

  - used to **customize aspects** of Terraform modules without altering the module's own source code.
  - allows to **share** modules across different Terraform configurations, making your module **composable** and **reusable**.

- When variables are **declared in the root module** of the configuration, you can set their values using **CLI options** and **environment variables**.
- When you declare them **in child modules**, the **calling** module should **pass values** in the module block.

---

### Declaring an Input Variable

- Each input variable accepted by a module must be declared using a `variable` block
- Variable Name

  - The `label` after the `variable` keyword is a **name** for the variable, which must be **unique** among all variables **in the same module**.
  - The name of a variable can be any valid identifier except the following: source, version, providers, count, for_each, lifecycle, depends_on, locals.

- Example

```conf
variable "image_id" {
  type = string
}

variable "availability_zone_names" {
  type    = list(string)
  default = ["us-west-1a"]
}

variable "docker_ports" {
  type = list(object({
    internal = number
    external = number
    protocol = string
  }))
  default = [
    {
      internal = 8300
      external = 8300
      protocol = "tcp"
    }
  ]
}
```

---

### Arguments

- **optional arguments** for variable declarations:

| optional arguments | desc                                                                         |
| ------------------ | ---------------------------------------------------------------------------- |
| `default`          | default value .                                                              |
| `type`             | specifies what value types are accepted for the variable.                    |
| `description`      | specifies the input variable's documentation.                                |
| `validation`       | A block to define validation rules, usually in addition to type constraints. |
| `sensitive`        | Limits Terraform UI output when the variable is used in configuration.       |
| `nullable`         | Specify if the variable can be null within the module.                       |

#### Type Constraints

- allow Terraform to return a helpful error message if the wrong type is used.
- If no type constraint is set then a value of **any type is accepted**.
- supported types:
  - `any`:indicate that any type is acceptable.
  - `string`
  - `number`
  - `bool`
  - `set(<TYPE>)`
  - `list(<TYPE>)`
  - `tuple([<TYPE>, ...])`
  - `map(<TYPE>)`
  - `object({<ATTR NAME> = <TYPE>, ... })`

---

#### Type Example

- `main.tf`

```conf
# define a variable

variable "mystr" {
  type    = string
  default = "hello terrform"
}

variable "mymap" {
  type = map(string)
  default = {
    mykey = "my value"
  }
}

variable "mylist" {
  type    = list(any)
  default = [1, 2, 3]
}
```

- Terraform Console

```sh
terrafor console
# > var.mystr
# "hello terrform"
# > var.mymap
# tomap({
#   "mykey" = "my value"
# })
# > var.mymap["mykey"]
# "my value"
# > var.mylist
# tolist([
#   1,
#   2,
#   3,
# ])
# > var.mylist[0]
# 1
```

---

#### Custom Validation Rules

- can specify `custom validation rules` for a particular variable by adding a validation block within the corresponding variable block.
- The example below checks whether the AMI ID has the correct syntax.

```conf
variable "image_id" {
  type        = string
  description = "The id of the machine image (AMI) to use for the server."

  validation {
    condition     = length(var.image_id) > 4 && substr(var.image_id, 0, 4) == "ami-"
    error_message = "The image_id value must be a valid AMI id, starting with \"ami-\"."
  }
}
```

---

### Using Input Variable Values

- Within the module that declared a variable, its value can be **accessed** from within expressions as `var.<NAME>`, where `<NAME>` matches the label given in the declaration block.
- Note: Input variables are created by a variable block, but you **reference them as attributes** on an object named `var`.
- The **value** assigned to a variable can **only be accessed** in expressions **within the module** where it was declared.

```conf
resource "aws_instance" "example" {
  instance_type = "t2.micro"
  ami           = var.image_id
}
```

---

### Assigning Values to Root Module Variables

#### Variables on the Command Line

- To **specify** individual variables on the **command line**, use the `-var` option when running the terraform plan and terraform apply commands:
- You can use the `-var` option multiple times in a single command to set **several different variables**.

```sh
terraform apply -var="image_id=ami-abc123"
terraform apply -var='image_id_list=["ami-abc123","ami-def456"]' -var="instance_type=t2.micro"
terraform apply -var='image_id_map={"us-east-1":"ami-abc123","us-east-2":"ami-def456"}'
# The above examples show appropriate syntax for Unix-style shells, such as on Linux or macOS.
```

---

#### Variable Definitions (`.tfvars`) Files

- A `variable definitions file` uses the same basic syntax as Terraform language files, but **consists only of variable name assignments**:

```conf
image_id = "ami-abc123"
availability_zone_names = [
  "us-east-1a",
  "us-west-1c",
]
```

- To set lots of variables, it is more convenient to specify their values in a `variable definitions file` (with a filename ending in either `.tfvars` or `.tfvars.json`) and then **specify that file** on the command line with `-var-file`:

```sh
# Linux, Mac OS, and UNIX:
terraform apply -var-file="testing.tfvars"

# PowerShell:
terraform apply -var-file='testing.tfvars'

# Windows cmd.exe:
terraform apply -var-file="testing.tfvars"
```

---

- Terraform also **automatically** **loads** a number of `variable definitions files` if they are present:

  - **Files** named exactly `terraform.tfvars` or `terraform.tfvars.json`.
  - **Any files** with names ending in `.auto.tfvars` or `.auto.tfvars.json`.

- Files whose names end with `.json` are parsed instead as **JSON objects**, with the root object properties corresponding to variable names:

```json
{
  "image_id": "ami-abc123",
  "availability_zone_names": ["us-west-1a", "us-west-1c"]
}
```

---

#### Environment Variables

- As a fallback for the other ways of defining variables, Terraform **searches** the environment of its own process for **environment variables** named `TF_VAR_` followed by the name of a declared variable.

  - This can be **useful** when running Terraform in **automation**, or when running a sequence of Terraform commands in succession with the same variables. For example, at a bash prompt on a Unix system:

```sh
export TF_VAR_image_id=ami-abc123
terraform plan
```

- On operating systems where environment variable names are case-sensitive, Terraform matches the variable name exactly as given in configuration, and so the required environment variable name will usually have **a mix of upper and lower case letters** as in the above example.

---

## Output Values

- `Output values`
  - make information about your infrastructure **available on the command line**
  - can **expose** information for other Terraform configurations to use.
  - are similar to **return values in programming languages**.

#### Declaring an Output Value

- Each output value exported by a module must be declared **using an output block**.
- name
  - a valid identifier
  - The label immediately after the `output` keyword
- In a `root module`, this name is displayed to the user;
- in a `child module`, it can be used to access the output's value.

```conf
output "instance_ip_addr" {
    value = aws_instance.server.private_ip
    # In this example, the expression refers to the private_ip attribute exposed by an aws_instance resource defined elsewhere in this module (not shown).
}
```

---

## Local Values

- `local value`
  - assigns a name **to an expression**, so you can use the name multiple times within a module instead of repeating the expression.
- `Local values` are like a function's **temporary local** variables.

### Declaring a Local Value

- A set of related local values can be declared together in a single locals block:

```conf
locals {
  service_name = "forum"
  owner        = "Community Team"
}
```

- The expressions in local values are **not limited to literal constants**;
  - they can also **reference other values** in the module in order to transform or combine them, including variables, resource attributes, or other local values:

```conf
locals {
  # Ids for multiple sets of EC2 instances, merged together
  instance_ids = concat(aws_instance.blue.*.id, aws_instance.green.*.id)
}

locals {
  # Common tags to be assigned to all resources
  common_tags = {
    Service = local.service_name
    Owner   = local.owner
  }
}
```

---

### Using Local Values

- Once a local value is declared, you can reference it in expressions as `local.<NAME>`.

- Note: Local values are created by a locals block (plural), but you reference them as attributes on an object named local (singular). Make sure to leave off the "s" when referencing a local value!
- A local value can only be accessed in expressions within the module where it was declared.

```conf
resource "aws_instance" "example" {
  # ...

  tags = local.common_tags
}
```

---

[TOP](#terraform---language-variable)
