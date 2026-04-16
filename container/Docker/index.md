# Docker

[Back](../../index.md)

- [Fundamental](./fundamental/fundamental.md)
- [Docker Image](./image/image/image.md)
- [Docker Container](./container/container.md)
  - [`ENTRYPOINT` vs `CMD` vs `RUN`](./image/entrypoint_cmd_run/entrypoint_cmd_run.md)
- [Docker Network](./docker_network/docker_network.md)
- [Docker Compose](./compose/compose.md)

---

## Commands

### Container Lifecycle

- ref: https://docs.docker.com/reference/cli/docker/

| Command                         | Description                                                       |
| ------------------------------- | ----------------------------------------------------------------- |
| `docker create image_name`      | Create a new container, setting up fs snapshot for a container    |
| `docker start image_name`       | Start one or more stopped containers, executing startup command   |
| `docker run image_name`         | **Create** and **run** a new container from an image              |
| `docker run image_name command` | Create and run a new container from an image with default command |
| `docker run -it image_name sh`  | Starts a new shell session after create and run a new container   |
| `docker ps`                     | List containers                                                   |
| `docker stop container_id`      | Stop one or more running containers, sending terminate signal     |
| `docker kill container_id`      | Kill one or more running containers, sending sigkill signal       |
| `docker system prune`           | Remove all unused containers, networks, images                    |
| `docker logs container_id`      | RFetch the logs of a container                                    |

---

## Volume

| Command                         | Description                            |
| ------------------------------- | -------------------------------------- |
| `docker volume ls`              | List volumes                           |
| `docker volume create vol_name` | Create a volume                        |
| `docker volume update`          | Update a volume (cluster volumes only) |
| `docker volume rm vol_name`     | Remove one or more volumes             |

---



---

## Hands-on

- [Installation on Ubuntu](./installation_ubuntu/installation_ubuntu.md)
- [Hello world](./lab/hello_world.md)
- [Upload Docker Image to AWS ECR](./lab/upload_ecr.md)
- [Oracle Database](./oracle_db.md)
- [Project: node.js app](./pro_nodejs/pro_nodejs.md)
- [Project: Docker Compose with Multiple local containers](./pro_compose_multicon/pro_compose_multicon.md)
- [Deploy Oracle Database 19c using Docker on RHEL 8.10](./deploy_oracle19c_docker_rhel8.md)
