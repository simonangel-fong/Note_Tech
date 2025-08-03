# Terraform - AWS: EC2

[Back](../../index.md)

- [Terraform - AWS: EC2](#terraform---aws-ec2)
  - [EC2 instance with Public IP](#ec2-instance-with-public-ip)
  - [Nginx Web Server](#nginx-web-server)
  - [EC2 Template](#ec2-template)

---

## EC2 instance with Public IP

---

## Nginx Web Server

- User data
- templatefile with variable

```hcl
user_data = templatefile("${path.module}/templates/script.tpl", {
    "bucketname" = var.bucket_name
})
```

```sh
apt update
apt install -y nginx aws-cli

rm /var/www/html/index # remove default file
aws s3 sync s3://${bucket_name} /var/www/html/
```

---

Legacy: Can use provisioner

https://developer.hashicorp.com/terraform/language/resources/provisioners/syntax

---

## EC2 Template
