# Terraform - AWS: ECS

[Back](../../index.md)

- [Terraform - AWS: ECS](#terraform---aws-ecs)
  - [DevOps Practices](#devops-practices)
  - [ECR](#ecr)
    - [Create ECR](#create-ecr)
    - [Docker Command](#docker-command)
  - [ECS](#ecs)
    - [Task](#task)

---

## DevOps Practices

- For VM, use tool like packer to build AMIs.
- For docker, use dockerfile to create docker images.

| DevOps Steps | Development                               | Production |
| ------------ | ----------------------------------------- | ---------- |
| Build        | Local build                               | Jenkins    |
| Push         | Local Development env with Docker Compose | ECR        |
| Run          | Local Development env with Docker Compose | ECS        |

---

## ECR

### Create ECR

```terraform
resource "aws_ecr_repository" "myapp" {
  name                 = "myapp"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

output "myapp-ecr-url" {
    value = aws_ecr_repository.myapp.repository_url
}
```

---

### Docker Command

```sh
# push image to ecr created by tf
aws ecr get-login
docker push ecr_url/myapp

# build with image on ecr
docker build -t ecr_url/myapp
```

---

## ECS

- ECS = EC2 + ECS agent

- Create ECS cluster

```terraform
resource "aws_ecs_cluster" "ecs_cluster" {
  name = "ecs_cluster"
}
```

- Create Launch Template + Autoscaling Group

```terraform
resource "aws_launch_template" "ecs_instance_template" {
  name_prefix   = "ecs_instance"
  image_id      = var.image_id
  instance_type = var.instance_type
}

resource "aws_autoscaling_group" "ecs_auto_group" {
  availability_zones = ["${var.aws_region}"]
  desired_capacity   = 1
  max_size           = 1
  min_size           = 1

  launch_template {
    id      = aws_launch_template.ecs_instance_template.id
    version = "$Latest"
  }
}
```

---

### Task

- Task definition: describe what to be run within docker container

  - specify Docker image
  - Max CPU usage, max memory usage
  - Whether containers should be linked. ie, link app with db
  - Environment variables

- Service definition: describe the container based on the task definition.
  - Service always running. if it stops, it will be restarted.
  - Service can be scaled
  - ELB can be added in front of a service
  - service can run over AZs
    - AZs + ELB = HA
