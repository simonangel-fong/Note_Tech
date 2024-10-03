# Docker

[Back](../../index.md)

- [Docker Image](./image/image.md)

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

---

- [Hello world](./lab/hello_world.md)
- [Oracle Database](./oracle_db.md)

---

- [Project: node.js app](./pro_nodejs/pro_nodejs.md)
- [Project: Docker Compose with Multiple local containers](./pro_compose_multicon/pro_compose_multicon.md)
