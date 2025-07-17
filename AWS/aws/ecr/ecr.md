# AWS - ECR

[Back](../index.md)

- [AWS - ECR](#aws---ecr)
  - [Create an ECR Repository](#create-an-ecr-repository)

---

## Create an ECR Repository

```sh
# ca-central-1
aws ecr create-repository --repository-name docker-getting-started --region ca-central-1

# Retrieve an authentication token and authenticate Docker client to registry.
aws ecr get-login-password --region ca-central-1 | docker login --username <username> --password-stdin <ecr_pwd>

# Find Account ID
aws sts get-caller-identity --query Account --output text

# Using an image built from a local Dockerfile
docker build -t <img_name> .
# tag
docker tag <tag_name>:latest <ecr_pwd>/<img_name>:latest

# Using an image pull from DockerHub
docker pull <hub_img_name>
# tag
docker tag <hub_img_name>:latest <ecr_pwd>/<img_name>:latest

# confirm
docker image ls
# push
docker push <ecr_pwd>/<img_name>:latest
```
