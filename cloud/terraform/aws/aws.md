# Terraform - AWS

[Back](../index.md)

- [Terraform - AWS](#terraform---aws)
  - [Terraform Registry](#terraform-registry)
  - [Demo: Spinning up an instance in AWS](#demo-spinning-up-an-instance-in-aws)

---

## Terraform Registry

- All:
  - https://registry.terraform.io/
- AWS Doc:
  - https://registry.terraform.io/providers/hashicorp/aws/latest/docs

---

## Demo: Spinning up an instance in AWS

- Create an AWS user and get access key.
- Configure AWS cli locally with this user.

```sh
aws configure
# AWS Access Key ID:
# AWS Secret Access Key:
# Default region name [us-east-1]: us-east-1
# Default output format [json]:
```

- Create `instance.tf`

```conf
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "example" {
  ami           = "ami-0ccb559bf2fde32a9"
  instance_type = "t2.micro"
    tags = {
    Name = "HelloWorld"
  }
}
```

- Lauch

```sh
# initializes a working directory containing Terraform configuration files.
terraform init
# command executes the actions proposed in a Terraform plan.
terraform apply
```

- Update the instance type to `t3.micro`
- Apply

  - `terraform apply`

- Destroy infra

```sh
# destroy all remote objects managed by a particular Terraform configuration.
terraform destroy
```

---
