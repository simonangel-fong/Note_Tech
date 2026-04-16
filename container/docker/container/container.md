# Docker - Container

[Back](../index.md)

- [Docker - Container](#docker---container)
  - [Container](#container)
  - [What happens if `docker run`](#what-happens-if-docker-run)
  - [Isolation](#isolation)
  - [STDIN](#stdin)
  - [Port Mapping](#port-mapping)
  - [Volume Mapping](#volume-mapping)
  - [Environment Variable](#environment-variable)

---

## Container

| Command                                                 | Description                                                     |
| ------------------------------------------------------- | --------------------------------------------------------------- |
| `docker container ls`                                   | List containers                                                 |
| `docker container ls -a`                                | List all containers                                             |
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

| Command                         | Description                                      |
| ------------------------------- | ------------------------------------------------ |
| `docker run image_name`         | Create and run a new container from an image     |
| `docker run image_name COMMAND` | Create and run a new container and run a command |
| `docker ps`                     | List containers                                  |
| `docker rm con_name`            | Remove a container                               |
| `docker exec con_name COMMAND`  | Execute a command in a running container         |
| `docker attach con_name`        | Attach a container                               |
| `docker inspect obj_name`       | Show detailed information on Docker objects      |
| `docker logs con_name`          | Show logs of the container                       |

---

## What happens if `docker run`

When you execute `docker run`, `Docker` performs a sequence of actions:

1. **Check local image**
   Docker looks for the specified `image` on your local machine.
2. **Pull from registry (if needed)**
   If the `image` is not found locally, Docker downloads it from `Docker Hub` or another configured registry.
3. **Create a container**
   A new `container` is created from the `image` (each docker run creates a new container).
4. **Execute the default command**
   Docker runs the predefined command inside the container.
5. **Container lifecycle tied to process**
   If the process is **running** → container is **running**
   If the process **stops** → container **stops**
6. **Repeat behavior**
   Running the same command again:

- Reuses the local image (no download)
- Creates a new container instance

---

- **Example**

```sh
docker run dockerinaction/hello_world
```

**First run:**

1. Docker checks for `dockerinaction/hello_world` locally → not found
2. Downloads image from Docker Hub
3. Creates a container
4. Runs: `echo "hello world"`
5. Process exits → container stops

**Second run**:

1. Image already exists locally → no download
2. Docker creates another new container
3. Executes the same command → prints hello world again

---

## Isolation

vm vs container

![pic](./pic/container_computer_stack.png)

![pic](./pic/contianer_process.png)

Features used to build containers:

- `PID namespace`: **Process** identifiers and capabilities
- `IPC namespace`: **Process** communication over shared memory
- `UTS namespace`: **Host and domain** name
- `NET namespace`: **Network** access and structure
- `USR namespace`: **User names** and identifiers
- `MNT namespace`: **Filesystem** access and structure
- `chroot syscall`: Controls the location of the **filesystem root**
- `cgroups`: Resource protection
- `CAP drop`: Operating system feature restrictions
- `Security modules`: Mandatory access controls

---

## STDIN

using `-i` and `-t`

- Options:
  - `-i`/`--interactive`: Keep `STDIN` open even if not attached
  - `-t`/`--tty`: Allocate a pseudo-terminal

---

## Port Mapping

The reason why port mapping is needed:

- Container has its own IP different from the host IP
- To enable accessibility of the app, must map the ports in the container to the port on the host machine.

- `-p host_port:container_port`

---

## Volume Mapping

Why:

- images are built as a stack of immutable image layers.
- Container run on a writable but ephemeral container layer.
- to persist the data in teh writable layer, must map the mount.

- `-v host_vol_path:con_vol_path`

---

## Environment Variable

- `-e ENV_VAR=value`
- `docker insepct con_name`: inspect env var

---
