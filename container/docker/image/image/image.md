# Docker - Image

[Back](../../index.md)

- [Docker - Image](#docker---image)
  - [Docker Image](#docker-image)
  - [Dockerfile Instructions](#dockerfile-instructions)
  - [Example](#example)
  - [Example: Create Container manually](#example-create-container-manually)
  - [Layered architecture](#layered-architecture)
    - [Characteristics](#characteristics)
    - [Common Mistake](#common-mistake)
  - [Multi-stage](#multi-stage)
  - [ENTRYPOINT/CMD:](#entrypointcmd)
  - [HEALTHCHECK](#healthcheck)
  - [Image tag](#image-tag)
  - [Save and Load](#save-and-load)

---

| Command                                          | Description                                           |
| ------------------------------------------------ | ----------------------------------------------------- |
| `docker build`                                   | Build an image from a Dockerfile                      |
| `docker build -t dockerID/ProjectName:Version .` | Build and tag an image from a Dockerfile              |
| `docker image ls`                                | List images                                           |
| `docker image rm`                                | Remove one or more images                             |
| `docker image prune -f`                          | Remove unused images                                  |
| `docker image history img_id`                    | Show the history of an image                          |
| `docker image pull img_tag`                      | Download an image from a registry                     |
| `docker image push img_tag`                      | Upload an image to a registry                         |
| `docker image tag old_tag new_tag`               | Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE |
| `docker container commit con_name img_tag`       | Create a new image from a container's changes         |

- Alias

| Command                | Description     |
| ---------------------- | --------------- |
| `docker images`        | List Images     |
| `docker rmi img_name`  | Remove an image |
| `docker pull img_name` | Pull an image   |

---

## Docker Image

- `Docker Image`:
  - a **snapshot** or blueprint of the libraries and dependencies required inside a container for an application to run, along with **startup command**.

  - = file system snapshot + startup command

- Steps:
  - create docker file
  - Docker Clent(CLI)
  - Docker Server
    - build a Usable Image according to the docker file

- Flow to create a dockerfile:
  - specify base image
  - run commands to install additional programs
  - specify startup commands.

---

## Dockerfile Instructions

- `Docker File`:
  - a **text document** that contains all instructions to **automatically** assemble an **image**.

- Dockerfile Instructions
  - not case-sensitive
    - convention is for them to be **UPPERCASE**
  - run in a `Dockerfile` **in order**.
  - Comment: `#`

- Leading whitespace is ignored.
  - Whitespace in instruction **arguments**, however, **isn't ignored**.

```Dockerfile
          # this is a comment-line
    RUN echo hello
RUN echo world

# equivalent
# this is a comment-line
RUN echo hello
RUN echo world

# not ignored
RUN echo "\
     hello\
     world"

```

- `FROM` instruction
  - specifies the **base image**
  - must begin with a `FROM` instruction
    - may only be **preceded** by one or more `ARG` instructions, which declare arguments that are used in `FROM` lines in the `Dockerfile`.

---

| Instruction   | Description                                                 |
| ------------- | ----------------------------------------------------------- |
| `FROM`        | Create a new build stage from a base image.                 |
| `MAINTAINER`  | Specify the author of an image.                             |
| `SHELL`       | Set the default shell of an image.                          |
| `LABEL`       | Add metadata to an image.                                   |
| `EXPOSE`      | Describe which ports your application is listening on.      |
| `USER`        | Set user and group ID.                                      |
| `HEALTHCHECK` | Check a container's health on startup.                      |
| `ONBUILD`     | Specify instructions for when the image is used in a build. |
| `STOPSIGNAL`  | Specify the system call signal for exiting a container.     |

- ENV, var, command

| Instruction  | Description                 |
| ------------ | --------------------------- |
| `ARG`        | Use build-time variables.   |
| `ENV`        | Set environment variables.  |
| `RUN`        | Execute build commands.     |
| `CMD`        | Specify default commands.   |
| `ENTRYPOINT` | Specify default executable. |

- File, volume

| Instruction | Description                                |
| ----------- | ------------------------------------------ |
| `WORKDIR`   | Change working directory.                  |
| `COPY`      | Copy files and directories.                |
| `ADD`       | Add local or remote files and directories. |
| `VOLUME`    | Create volume mounts.                      |

- format of the Dockerfile
  - `INSTRUCTION arguments`

---

## Example

- Goal:
  - create an Redis image from scrath

```sh
mkdir redis-image
cd redis-image
touch Dockerfile
```

- Dockerfile:

```yaml
# base image
FROM alpine

# install dependcy
RUN apk add --update redis

# startup commands
CMD ["redis-server"]
```

- Build image

```sh
# in the redis-image folder
docker build .

# list all image
docker image ls

# run new image
docker run image_id

```

---

## Example: Create Container manually

- Creating container using no dockerfile

- Terminal A:

```sh
winpty docker run -it alpine sh
apk add --update redis
```

- Terminal B:

```sh
docker ps
docker commit -c "CMD 'redis-server'" container_id
# return the hash of image

docker run image_hash
```

---

## Layered architecture

- `Layered architecture`
  - how Docker images are built as a **stack of immutable layers**, where **each layer represents a change** (like installing packages, copying files, or setting environment variables).
  - benefits: efficiency, speed, and reusability.

- `layer`
  - a **read-only filesystem snapshot** created from each instruction in a `Dockerfile`.
  - Each instruction creates a new layer.
  - When you run a container:
    - Docker adds a **thin writable layer on top**
    - All lo**wer layers** remain **read-only**

---

### Characteristics

1. **Immutable Layers**
   - Once created, a **layer never changes**
   - If something changes → a new layer is created

2. **Layer Caching**
   - Docker **caches layers** during build
     - If **nothing** changes, Docker **reuses** `cached layers`, making rebuilds much faster.
     - But if you modify a layer: **All layers after** it must rebuild

3. **Layer Reuse** (Storage Efficiency)
   - Multiple images can **share layers**.
   - e.g., base image

4. Copy-on-Write (CoW)
   - When a container modifies a file:
   - It **copies the file** from a `read-only layer` to the `writable layer`, then modifies it

---

### Common Mistake

- **Too Many Layers**
  - Each RUN, COPY, ADD adds a layer
  - Can **increase image size**

- **Cache Busting Mistakes**

```dockerfile
# mistake
# if changed, following layer rebuild
COPY . /app
RUN pip install -r requirements.txt

# better
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /app
```

- **Large Layers (Inefficient Images)**
  - Installing **unnecessary packages** increases layer size
  - Use:
    - `--no-install-recommends`
    - Multi-stage builds

---

## Multi-stage

- `Docker multi-stage build`
  - a method for optimizing Dockerfiles to create **smaller**, more **secure**, and more **efficient** container images.
  - It allows you to use **multiple** `FROM` statements in a **single** `Dockerfile`, where each stage begins a new build environment.

- **building an app** often needs:
  - compilers (e.g., gcc, maven, npm)
  - dev dependencies
  - temporary files
- runtime container **does NOT need these**.

- **Without multi-stage:**
  - ship everything → large image, security risk
- **With multi-stage:**
  - build in one stage
  - copy only the final artifact → small, secure image

```txt
[ Stage 1: Build ]  --->  [ Stage 2: Runtime ]
   (heavy tools)              (lightweight)
```

```dockerfile
# Uses full Node.js environment
FROM node:18 AS builder
WORKDIR /app
COPY . .
# Installs dependencies, Builds static files
RUN npm install && npm run build

# Lightweight image
FROM nginx:alpine
# Only gets /app/build: just static files + nginx
COPY --from=builder /app/build /usr/share/nginx/html
```

---

## ENTRYPOINT/CMD:

- `ENTRYPOINT`: sets the **process executed** when container **starts**
- `CMD`: set the **default command** to run when a container **starts**

---

## HEALTHCHECK

- `HEALTHCHECK`: a command that Docker **runs inside the container** periodically to **determine health**.
  - `start-period`: Grace period after container starts
  - `interval`: How often to run check
  - `timeout`: Max time for a check
  - `retries`: How many failures before marking unhealthy

| Health States | Description                 |
| ------------- | --------------------------- |
| healthy       | check passed                |
| unhealthy     | check failed multiple times |
| starting      | still initializing          |

```dockerfile
HEALTHCHECK CMD curl -f http://localhost/ || exit 1

HEALTHCHECK --interval=30s \
            --timeout=5s \
            --retries=3 \
            --start-period=10s \
            CMD curl -f http://localhost/ || exit 1
```

- works with app

```py
@app.get("/health")
def health():
    return {"status": "ok"}
```

---

## Image tag

- for version control
  - default: `latest`
- best practices:
  - specify a tag
  - git SHA tags

---

## Save and Load

- `docker save`: Save one or more images to a tar archive
- `docker load`: Load an image from a tar archive or STDIN

- Use cases:
  - move image to another machine (offline)
  - backup an image
  - share image without Docker registry (like ECR/Docker Hub)

- example

```sh
docker save -o myimage.tar myimage:latest

docker load -i myimage.tar
```
