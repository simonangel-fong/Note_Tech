# Docker - Image

[Back](../../index.md)

- [Docker - Image](#docker---image)
  - [Docker Image](#docker-image)
  - [Dockerfile Instructions](#dockerfile-instructions)
  - [Example](#example)
  - [Example: Create Container manually](#example-create-container-manually)

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
