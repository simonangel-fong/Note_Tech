# Docker

[Back](../../index.md)

- [Docker Image](./image/image/image.md)
  - [Entrypoint](./image/entrypoint/entrypoint.md)

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

###

| Command                                | Description                                 |
| -------------------------------------- | ------------------------------------------- |
| `docker exec`                          | Execute a command in a running container    |
| `docker exec -it container_id command` | Execute a command in a running container    |
| `docker exec -it container_id sh`      | starts a new shell session in the container |

---

## Image

| Command                         | Description                                           |
| ------------------------------- | ----------------------------------------------------- |
| `docker image ls`               | List images                                           |
| `docker build -t tag_name path` | Build and tag an image from a Dockerfile              |
| `docker image tag`              | Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE |
| `docker image rm`               | Remove one or more images                             |
| `docker image prune`            | Remove unused images                                  |
| `docker image pull`             | Download an image from a registry                     |
| `docker image push`             | Upload an image to a registry                         |

---

## Container

| Command                                                 | Description                                                     |
| ------------------------------------------------------- | --------------------------------------------------------------- |
| `docker container ls`                                   | List containers                                                 |
| `docker container stats name`                           | Display a live stream of container(s) resource usage statistics |
| `docker container port con_name`                        | List port mappings or a specific mapping for the container      |
| `docker container logs con_name`                        | Fetch the logs of a container                                   |
| `docker container cp`                                   | Copy files/folders between a container and the local filesystem |
| `docker container create`                               | Create a new container                                          |
| `docker container create -i -t --name con_name img_tag` | Create a new container, with TTL,STDIN, and name                |
| `docker container rename old_name new_name`             | Rename a container                                              |
| `docker container update con_name`                      | Update configuration of one or more containers                  |
| `docker container start con_name`                       | Start one or more stopped containers                            |
| `docker container pause con_name`                       | Pause all processes within one or more containers               |
| `docker container unpause con_name`                     | Unpause all processes within one or more containers             |
| `docker container stop con_name`                        | Stop one or more running containers                             |
| `docker container kill con_name`                        | Kill one or more running containers                             |
| `docker container rm con_name`                          | Remove one or more containers                                   |
| `docker container exec con_name`                        | Execute a command in a running container                        |

- Alias

| Command       | Description                                  |
| ------------- | -------------------------------------------- |
| `docker run`  | Create and run a new container from an image |
| `docker ps`   | List containers                              |
| `docker exec` | Execute a command in a running container     |

---

## Volume

| Command                         | Description                            |
| ------------------------------- | -------------------------------------- |
| `docker volume ls`              | List volumes                           |
| `docker volume create vol_name` | Create a volume                        |
| `docker volume update`          | Update a volume (cluster volumes only) |
| `docker volume rm vol_name`     | Remove one or more volumes             |

---

## Compose

| Command                 | Description                                |
| ----------------------- | ------------------------------------------ |
| `docker compose ls`     | List running compose projects              |
| `docker compose ps`     | List containers                            |
| `docker compose images` | List images used by the created containers |
| `docker compose build`  | Build or rebuild services                  |
| `docker compose up`     | Create and start containers                |
| `docker compose down`   | Stop and remove containers, networks       |
| `docker compose rm`     | Removes stopped service containers         |
| `docker compose exec`   | Execute a command in a running container   |
| `docker compose logs`   | View output from containers                |

---

- [Hello world](./lab/hello_world.md)
- [Upload Docker Image to AWS ECR](./lab/upload_ecr.md)
- [Oracle Database](./oracle_db.md)

---

- [Project: node.js app](./pro_nodejs/pro_nodejs.md)
- [Project: Docker Compose with Multiple local containers](./pro_compose_multicon/pro_compose_multicon.md)

---

- [Deploy Oracle Database 19c using Docker on RHEL 8.10](./deploy_oracle19c_docker_rhel8.md)

- [Installation on Ubuntu](./installation_ubuntu/installation_ubuntu.md)

---

## Docker Network

- [Docker Network](./docker_network/docker_network.md)
