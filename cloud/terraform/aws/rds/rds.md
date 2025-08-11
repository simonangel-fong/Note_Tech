# Terraform - AWS: RDS

[Back](../../index.md)

- [Terraform - AWS: RDS](#terraform---aws-rds)
  - [RDS](#rds)
    - [Parameter Group](#parameter-group)
    - [Subnet Group](#subnet-group)
    - [RDS Instance](#rds-instance)

---

## RDS

- `RDS (Relational Database Services)`

  - a managed database solution
  - ie.:
    - setup replication (high availability)
    - automated snapshots for backups
    - automated security updates
    - instance replacement for vertical scaling

- Supported DB:

  - MySQL
  - MariaDB
  - PostgreSQL
  - MSSQL
  - Oracle

- Steps to create an RDS instance
  1. Create a subnet group, where the db resides
  2. Create a parameter group, to specify parameters to change DB settings
  3. Create a security group, to control incoming traffic.
  - The common destination is the subnet where the db resides.
  4. Create the RDS instance

---

### Parameter Group

- `DB parameter group`

  - acts as a container for **engine configuration values** that are **applied** to one or more **DB instances**.

- If you create a DB instance **without specifying** a `DB parameter group`, the DB instance uses a **default** `DB parameter group`.

- Example

```terraform
resource "aws_db_parameter_group" "default" {
  name   = "rds-pg"
  family = "mysql5.6"

  parameter {
    name  = "character_set_server"
    value = "utf8"
  }

  parameter {
    name  = "character_set_client"
    value = "utf8"
  }
}
```

---

### Subnet Group

- Usually a group of private subnets

- Example

```terraform
resource "aws_docdb_subnet_group" "default" {
  name       = "main"
  subnet_ids = [aws_subnet.frontend.id, aws_subnet.backend.id]

  tags = {
    Name = "My docdb subnet group"
  }
}
```

---

### RDS Instance

```terraform
resource "aws_db_instance" "default" {
  db_name              = "mydb"

  allocated_storage    = 10             # storage
  engine               = "mysql"
  engine_version       = "8.0"
  instance_class       = "db.t3.micro"
  username             = "foo"
  password             = "foobarbaz"

  db_subnet_group_name = ${aws_docdb_subnet_group.default.name}
  parameter_group_name = ${aws_db_parameter_group.default.name}

  multi_az                  = "false"   # true for HA
  vpc_security_group_ids    = ${aws_security_group.allow-mysql.id}

  backup_retention_period = 30      # The backup retention period.
}
```
