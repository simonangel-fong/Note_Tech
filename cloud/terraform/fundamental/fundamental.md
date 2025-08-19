# Terraform - Fundamental

[Back](../index.md)

- [Terraform - Fundamental](#terraform---fundamental)
  - [Terraform](#terraform)
    - [Installation](#installation)
    - [Command: console](#command-console)
  - [HCL](#hcl)
  - [Files and Directories](#files-and-directories)
  - [Worksapce](#worksapce)
  - [Debugging Mode](#debugging-mode)

---

## Terraform

- `Infrastructure as code`
  - a method of managing and provisioning **computing resources** using **code**, rather than manual configuration tools or physical hardware.
- **Automation** of your infrastructure
- Keep your infrastructure **in a certain state** (**compliant**)
  - e.g. 2 web instances with 2 volumes, and 1 load balancer
- Make your infrastructure **auditable**
  - You can keep your infrastructure **change history** in a `version control` system like GIT

---

- vs other automation tools

- `Ansible`, `Chef`, `Puppet`, `Saltstack` have a focus on **automating** the **installation and conguration of software**
  - Keeping the machines **in compliance**, in a certain state
- `Terraform` can **automate** provisioning of the **infrastructure** itself
  - eg. Using the `AWS`, `DigitalOcean`, `Azure API`
- **Works well with** automation software like `ansible` to install software **after** the **infrastructure is provisioned**先创建基础设施，再自动安装。

- Rel:
  - https://developer.hashicorp.com/terraform/language

---

### Installation

- Website: https://www.terraform.io/

- 1. Download and unzip
- 2. Place the directory containing `terraform.exe` in a path.
- 3. Add terraform into `PATH`.
  - Control Panel > System and Security > System > Advanced system settings
  - Environment Variables > User variables for Administrator
  - Select `Path` and click `Edit`
  - Click `New` and paste the path.
- 4. Test in terminal: `terraform version`

---

### Command: console

- `terraform console`
  - provides an interactive console for evaluating expressions.
- Unavailabel when a specific provider is defined.

```sh
terraform console
```

---

## HCL

- `HCL`
  - `HashiCorp Conguration Language`
- Terraform file extension:

  - `.tf`

- `Terraform language`

  - used for **declaring resources**, which represent **infrastructure objects**.
  - **declarative**, describing an **intended goal** rather than the steps to reach that goal.
  - The **ordering** of blocks and the files they are organized into are generally **not significant**;
  - Terraform **only** considers implicit and explicit relationships between resources **when determining an order of operations**.

- `Terraform configuration`
  - a **complete document** in the **Terraform language** that tells Terraform **how to manage** a given collection of **infrastructure**.
  - A **configuration** can consist of **multiple** files and directories.

---

- Basic elements:

```conf
<BLOCK TYPE> "<BLOCK LABEL>" "<BLOCK LABEL>" {
  # Block body
  <IDENTIFIER> = <EXPRESSION> # Argument
}
```

- `Blocks`
  - containers for other content and usually **represent the configuration** of some kind of object, like a resource.
  - `Blocks` have **a** `block type`, can have zero or **more** `labels`, and have **a** `body` that contains any number of `arguments` and `nested blocks`.
  - Most of Terraform's **features are controlled by top-level blocks** in a configuration file.
- `Arguments`
  - **assign** a value to a name.
  - appear within blocks.
- `Expressions`
  - represent a **value**, either literally or by referencing and combining other values.
  - They appear as **values** for `arguments`, or within other expressions.

---

## Files and Directories

- File **Extension**

  - **Code** in the Terraform language is **stored in plain text files** with the `.tf` file extension.
  - There is also a **JSON-based variant** of the language that is named with the `.tf.json` file extension.

- `Configuration files`

  - Files containing **Terraform code**

- **Text Encoding**

  - `Configuration files` must always use **`UTF-8` encoding**
  - **by convention** usually use **Unix-style line endings (LF)** rather than Windows-style line endings (CRLF), though both are accepted.

- `module`

  - a collection of `.tf` and/or `.tf.json` files kept together **in a directory**.

- `Terraform module`

  - **only** consists of the **top-level configuration files in a directory**;
    - **nested directories** are treated as **completely separate modules**, and are **not automatically included** in the configuration.
  - Terraform **evaluates** **all** of the `configuration files` **in a module**, effectively treating the entire module **as a single document**.
    - **Separating** various blocks **into different files** is purely for the convenience of readers and maintainers, and **has no effect on the module's behavior**.
  - can **use module calls** to explicitly **include** other modules into the configuration.
    - These `child modules` can come from **local directories** (nested in the parent module's directory, or anywhere else on disk), or from **external sources** like the `Terraform Registry`.

- `Root Module`

  - Terraform always runs in the context of **a single root module**.
  - A complete Terraform configuration consists of **a** `root module` and the **tree of** `child modules` (which includes the modules called by the root module, any modules called by those modules, etc.).

- In Terraform CLI, the `root module` is the **working directory** where Terraform is **invoked**.

---

## Worksapce

- Workspace

  - By default, tf starts with a single workspace.
  - isolate the states
    - when creating a new workspace, an **empty** state will be created.
    - however, still using the **same state** and **same backend configuration** (technically equivalent of **renaming** state file)
  - isolate the resouces
    - the command `terraform apply` in new workspace will **recreate** all resources, whose **state** will be managed in this **workspace**.

- Varaible `terraform.workspace`

  - used to avoid naming conllisions
  - used to control resource creation with condition

```hcl
# avoid naming collision
resource "aws_ssm_parameter" "my-parameter"{
  name = "/myapp/myname-${terraform.workspace}"
}

# conditional
resource "aws_instance" "myinstance" {
  count = terraform.workspace == "default" ? 1 :0
}
```

- **Not Fit**

  - workspace cannot be used for a "fully isolated" setup for multiple environment (staging / testing / prod)

- Common Commands

| CMD                                   | DESC                   |
| ------------------------------------- | ---------------------- |
| `terraform workspace new wsp_name`    | Create a new workspace |
| `terraform workspace select wsp_name` | Switch to a workspace  |

- Use Case

  - useful when needint to test something in the code without making changes to the existing resources.
    - create a workspace to test app and infrastructures before implementing them on existing resources.

- Real world Practises
  - use re-usable modules + multiple remote backend with multi-account strategy
    - staging env:
      - S3 backend with staging AWS account
    - prod env:
      - S3 backend with prod AWS account

---

## Debugging Mode

- TF just hangs
- set `TF_LOG` environment variable to enable more loggin.

```sh
# Linux
terraform apply -var TF_LOG=DEBUG

# windows Powershell
$Env:TF_LOG="DEBUG"
```

- Valid log levels:
  - `TRACE`
  - `DEBUG`
  - `INFO`
  - `WARN`
  - `ERROR`
