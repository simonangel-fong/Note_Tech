# Terraform - Fundamental: Loop

[Back](../index.md)

- [Terraform - Fundamental: Loop](#terraform---fundamental-loop)
  - [Loop](#loop)
  - [Dynamic block](#dynamic-block)
  - [Lab: for loop](#lab-for-loop)
  - [Lab: for\_each loop](#lab-for_each-loop)

---

## Loop

- `for` loop

  - loop over varaibles
  - output as list or map
  - example
    - `[for s in ["a", "b","c"]:upper(s)]`

- `for_each` loop

```terraform
resource "aws_security_group" "sg"{

    dynamic "ingress"{
        for_each = [22, 443]
        content {
            from_port = ingress.value
            to_port = ingress.value
            protocal = "tcp"
        }
    }
}
```

---

- for loop example

- `vars.tf`

```terraform
variable "list1" {
    type = list(string)
    default = [1, 10, 9, 101, 3]
}

variable "list2" {
    type = list(string)
    default = ["apple", "pear", "banana", "mango"]
}

variable "map1" {
    type = map(number)
    default = {
        "apple" = 5
        "banana" = 10
        "pear" = 3
        "mango" = 0
    }
}
```

- terraform console

```sh
[for s in ["a","b","c"]: s]
# [
#   "a",
#   "b",
#   "c",
# ]

[for s in ["a","b","c"]: upper(s)]
# [
#   "A",
#   "B",
#   "C",
# ]

[for s in var.list1: s + 1]
# [
#   2,
#   11,
#   10,
#   102,
#   4,
# ]

[for s in var.list2: upper(s)]
# [
#   "APPLE",
#   "PEAR",
#   "BANANA",
#   "MANGO",
# ]

[for k,v in var.map1: k]
# [
#   "apple",
#   "banana",
#   "mango",
#   "pear",
# ]

[for k,v in var.map1: v]
# [
#   5,
#   10,
#   0,
#   3,
# ]

# output as a map
{for k,v in var.map1: v => k}
# {
#   "0" = "mango"
#   "10" = "banana"
#   "3" = "pear"
#   "5" = "apple"
# }
```

---

## Dynamic block

- can iterate over blocks

---

## Lab: for loop

```terraform
# vars.tf
variable "project_tags" {
    type    = map(string)
    default = {
        Component   = "Frontend"
        Environment = "Production"
    }
}

resource "aws_ebs_volume" "ebs_vol"{
    # define tags with a map var
    tags = {for k, v in merge({Name = "myVolume}, var.project_tags): k => lower(v)}
}
```

---

## Lab: for_each loop

```terraform
variable "port_list" {
    type    = list(number)
    default = [22, 443, 80, 81, 8080]
}

resource "aws_security_group" "sg"{

    dynamic "ingress"{
        for_each = var.port_list
        content {
            from_port = ingress.value
            to_port = ingress.value
            protocal = "tcp"
        }
    }
}
```

```terraform
variable "port_map" {
    type    = map(list(string))
    default = {
        "22" = ["127.0.0.1/32","192.168.0.0/24"]
        "443" = ["0.0.0.0/0"]
    }
}

resource "aws_security_group" "sg"{

    dynamic "ingress"{
        for_each = var.port_map
        content {
            from_port = ingress.key
            to_port = ingress.key
            cidr_blocks = ingress.value
            protocal = "tcp"
        }
    }
}
```
