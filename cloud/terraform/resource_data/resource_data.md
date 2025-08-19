# Terraform - Resource & Data source

[Back](../index.md)

- [Terraform - Resource \& Data source](#terraform---resource--data-source)
  - [Resource](#resource)
  - [Data Source](#data-source)
  - [Lab: Ubuntu AMI Data](#lab-ubuntu-ami-data)

---

## Resource

- `Resource`

  - used to represent the infrastructure objects managed by terraform.

- During `terraform apply`, terraform will

  - **Refresh** the data sources
  - **Create resources** defined in `*.tf` files but not in the state file.
  - **Destroy resources** exist in the state file but not in `*.tf` files.
  - **Update resrouces** with different arguments in `*.tf` files than on the infrastructure.
    - **Destroy and re-create mode**:
      - most case, due to the limitation of the provider API.
      - ie.update user data will destroy first before recreate instance
    - **In-place updates mode**:
      - possible if provider API supports.
      - ie. update of security group without destroy

- reference of a resource:
  - `RESOURCE_TYPE.NAME.ATTRIBUTE`

---

## Data Source

- `Data source`

  - used to fetch or compute the data managed outside of terraform.
  - ie, AMI id, vpc id.
  - represents the existing infrastructure objects not managed by terraform.

- reference of a data source:
  - `data.RESOURCE_TYPE.NAME.ATTRIBUTE`

---

## Lab: Ubuntu AMI Data

```terraform
provider "aws" {
  region = "ca-central-1"
}

data "aws_ami" "ubuntu_ami" {
  most_recent = true

  region = "ca-central-1"

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

output "ami_id" {
  value = data.aws_ami.ubuntu_ami.image_id
}


resource "aws_instance" "ec2_instance" {
  instance_type = "t2.micro"
  ami           = data.aws_ami.ubuntu_ami.id
}
```
