# Terraform - Interpolation

[Back](../index.md)

- [Terraform - Interpolation](#terraform---interpolation)
  - [Interpolation](#interpolation)
    - [Variables](#variables)
    - [Math](#math)
    - [Conditional](#conditional)

---

## Interpolation

- In Terraform, it is allowed to interpolate other values using `${}`

- Interpolation types:
  - Variables: `${var.variable_name}`
  - Resources: `${aws_instance.name.id}`
  - Data Source: `${data.template_file.name.rendered}`

---

### Variables

| Variable Type       | Syntax                                 | Example                                                                           |
| ------------------- | -------------------------------------- | --------------------------------------------------------------------------------- |
| String              | `var.VAR_NAME`                         | `${var.aws_region}`                                                               |
| Map                 | `var.MAP_NAME["key_name"]`             | `${var.amis["us-east-1"]}`/`${lookup(var.amis, var.aws_region)}`                  |
| List                | `var.LIST_NAME`,`var.LIST_NAME[index]` | `${var.subnets[i]}`,`${join(",",var.subnets)}`                                    |
| Outputs of a module | `module.NAME.output`                   | `${module.aws_vpc.vpcid}`                                                         |
| Count informatnion  | count.FIELD                            | `${count.index}`                                                                  |
| Path information    | `path.TYPE`                            | `path.cwd`(current dir), `path.module`(module path),`path.root`(root module path) |
| Meta information    | `terraform.FIELD`                      | `terraform.env`(active workspace)                                                 |

---

### Math

- `${2 + 3 * 4}`

---

### Conditional

- Syntax:

```terraform
condition ? trueval : falseval
```

- Example

```terraform
resource "aws_instance" "myinstance"{

    count = ${var.env == "prod" ? 2 : 1}    # if the env is prod, then provision 2 instances, otherwise just 1.
}
```

- Operators
  - `==`
  - `!=`
  - `<`, `<=`
  - `>`,`>=`
  - `&&`, `||`, `!`
