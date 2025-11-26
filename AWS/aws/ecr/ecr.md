# AWS - ECR

[Back](../index.md)

- [AWS - ECR](#aws---ecr)
  - [Push Image from Docker client to ECR Repository](#push-image-from-docker-client-to-ecr-repository)
  - [Common Commands - Repo](#common-commands---repo)
  - [Common Commands - Image](#common-commands---image)
  - [Lab: Create, Tag, and Delete an ECR Repository](#lab-create-tag-and-delete-an-ecr-repository)
  - [Lab: Autenticate, Push, Scan, and Delete Image](#lab-autenticate-push-scan-and-delete-image)

---

## Push Image from Docker client to ECR Repository

- Container images can be pushed to an `Amazon ECR` repository with the `docker push` command.

- `Amazon ECR` repository must **exist before** pushing the image.

---

## Common Commands - Repo

- Repository management:

| Command                                                                                                               | Description                                   |
| --------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| `aws ecr describe-repositories`                                                                                       | List repositories in the region.              |
| `aws ecr create-repository --repository-name repo_name`                                                               | Create a repo.                                |
| `aws ecr put-image-scanning-configuration --repository-name repo_name --image-scanning-configuration scanOnPush=true` | Toggle scan-on-push after creation.           |
| `aws ecr put-image-tag-mutability --repository-name repo_name --image-tag-mutability IMMUTABLE`                       | Make tags immutable (prevents overwrites).    |
| `aws ecr delete-repository --repository-name repo_name --force`                                                       | Delete a repo (`--force` removes all images). |

- Repository policy

| Command                                                                                      | Description                   |
| -------------------------------------------------------------------------------------------- | ----------------------------- |
| `aws ecr get-repository-policy --repository-name repo_name`                                  | Show the current repo policy. |
| `aws ecr set-repository-policy --repository-name repo_name --policy-text json_file`          | Apply a repo resource policy. |
| `aws ecr delete-repository-policy --repository-name repo_name`                               | Remove the repo policy.       |
| `aws ecr get-lifecycle-policy --repository-name repo_name`                                   | Show lifecycle policy.        |
| `aws ecr put-lifecycle-policy --repository-name repo_name --lifecycle-policy-text json_file` | Add/update lifecycle policy . |
| `aws ecr delete-lifecycle-policy --repository-name repo_name`                                | Delete lifecycle policy.      |

- Tag

| Command                                                                  | Description                         |
| ------------------------------------------------------------------------ | ----------------------------------- |
| `aws ecr list-tags-for-resource --resource-arn repo_arn`                 | List AWS tags on the repo resource. |
| `aws ecr tag-resource --resource-arn repo_arn --tags Key=Env,Value=Prod` | Add AWS tags to the repo.           |
| `aws ecr untag-resource --resource-arn repo_arn --tag-keys Env`          | Remove AWS tags from the repo.      |

---

## Common Commands - Image

- Authenticate Docker to your ECR registry (required before push/pull):
  - `aws ecr get-login-password | docker login --username AWS --password-stdin <acct>.dkr.ecr.<region>.amazonaws.com`

| Command                                                                                    | Description                                                                   |
| ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------- |
| `aws ecr list-images --repository-name repo_name`                                          | List image IDs (tags/digests) in a repo.                                      |
| `aws ecr describe-images --repository-name repo_name`                                      | Detailed image metadata (tags, digests, sizes, pushedAt, scan findings refs). |
| `aws ecr start-image-scan --repository-name repo_name --image-id imageTag=tag`             | Manually trigger a vulnerability scan (if supported).                         |
| `aws ecr describe-image-scan-findings --repository-name repo_name --image-id imageTag=tag` | View vulnerability scan findings.                                             |
| `aws ecr batch-delete-image --repository-name repo_name --image-ids imageTag=tag`          | Delete image(s) by tag or digest.                                             |

---

## Lab: Create, Tag, and Delete an ECR Repository

```sh
# list repo
aws ecr describe-repositories --region ca-central-1
# {
#     "repositories": []
# }

# create image
aws ecr create-repository --region ca-central-1 --repository-name ecr-demo-project/nginx-repo
# confirm
aws ecr describe-repositories --region ca-central-1 --repository-name ecr-demo-project/nginx-repo

# tag
aws ecr list-tags-for-resource --resource-arn arn:aws:ecr:ca-central-1:099139718958:repository/ecr-demo-project/nginx-repo
aws ecr tag-resource --resource-arn arn:aws:ecr:ca-central-1:099139718958:repository/ecr-demo-project/nginx-repo --tags Key=Env,Value=Prod Key=Tier,Value=Frontend
aws ecr list-tags-for-resource --resource-arn arn:aws:ecr:ca-central-1:099139718958:repository/ecr-demo-project/nginx-repo
# {
#     "tags": [
#         {
#             "Key": "Env",
#             "Value": "Prod"
#         },
#         {
#             "Key": "Tier",
#             "Value": "Frontend"
#         }
#     ]
# }

aws ecr untag-resource --resource-arn arn:aws:ecr:ca-central-1:099139718958:repository/ecr-demo-project/nginx-repo --tag-keys Env
# {
#     "tags": [
#         {
#             "Key": "Tier",
#             "Value": "Frontend"
#         }
#     ]
# }

# delete repo
aws ecr delete-repository --repository-name ecr-demo-project/nginx-repo --force
# confirm
aws ecr describe-repositories --region ca-central-1
# {
#     "repositories": []
# }
```

---

## Lab: Autenticate, Push, Scan, and Delete Image

- Create repo

```sh
aws ecr create-repository --region ca-central-1 --repository-name ecr-demo-project/nginx-repo
```

- Authenticate

```sh
# Find Account ID
aws sts get-caller-identity --query Account --output text
# account_id

# Authenticate Docker to ECR
aws ecr get-login-password --region region_name | docker login --username AWS --password-stdin "aws_account_id.dkr.ecr.region_name.amazonaws.com"
# Login Succeeded

aws ecr list-images --repository-name ecr-demo-project/nginx-repo
# {
#     "imageIds": []
# }
```

- Build and push

```sh
# pull image from DockerHub
docker pull nginx
# confirm
docker images nginx:latest

# tag
docker tag nginx:latest 099139718958.dkr.ecr.ca-central-1.amazonaws.com/ecr-demo-project/nginx-repo:latest
# confirm
docker images 099139718958.dkr.ecr.ca-central-1.amazonaws.com/ecr-demo-project/nginx-repo:latest
# REPOSITORY                                                                    TAG       IMAGE ID       CREATED        SIZE
# 099139718958.dkr.ecr.ca-central-1.amazonaws.com/ecr-demo-project/nginx-repo   latest    1beed3ca46ac   23 hours ago   225MB

# push
docker push 099139718958.dkr.ecr.ca-central-1.amazonaws.com/ecr-demo-project/nginx-repo:latest

# list image
aws ecr list-images --repository-name ecr-demo-project/nginx-repo
# {
#     "imageIds": [
#         {
#             "imageDigest": "sha256:bd1578eec775d0b28fd7f664b182b7e1fb75f1dd09f92d865dababe8525dfe8b",
#             "imageTag": "latest"
#         }
#     ]
# }

# show metadata
aws ecr describe-images --repository-name ecr-demo-project/nginx-repo
```

- Scan

```sh
# scan
aws ecr start-image-scan --repository-name ecr-demo-project/nginx-repo --image-id imageTag=latest
# "imageScanStatus": {
#     "status": "PENDING"
# }

# show scan result
aws ecr describe-image-scan-findings --repository-name ecr-demo-project/nginx-repo --image-id imageTag=latest
# "imageScanCompletedAt": "2025-11-04T22:26:03-05:00",
# "vulnerabilitySourceUpdatedAt": "2025-11-04T22:26:03-05:00",
# "findingSeverityCounts": {
#     "HIGH": 1
# }
```

- Pull

```sh
docker pull 099139718958.dkr.ecr.ca-central-1.amazonaws.com/ecr-demo-project/nginx-repo:latest
docker run --rm -d --name ecr-nginx -p 8000:80 099139718958.dkr.ecr.ca-central-1.amazonaws.com/ecr-demo-project/nginx-repo:latest
docker rm -f ecr-nginx
# ecr-nginx
```

- Delete

```sh
aws ecr batch-delete-image --repository-name ecr-demo-project/nginx-repo --image-ids imageTag=latest
aws ecr list-images --repository-name ecr-demo-project/nginx-repo
# {
#     "imageIds": []
# }
```

- Delete repo

```sh
# delete
aws ecr delete-repository --repository-name ecr-demo-project/nginx-repo --force

# confirm
aws ecr describe-repositories
```
