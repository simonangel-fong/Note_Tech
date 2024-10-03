# Docker - Image

[Back](../index.md)

- [Docker - Image](#docker---image)
  - [Docker Image](#docker-image)
  - [Example](#example)
  - [Example: Create Container manually](#example-create-container-manually)

---

| Command                                          | Description                                           |
| ------------------------------------------------ | ----------------------------------------------------- |
| `docker build`                                   | Build an image from a Dockerfile                      |
| `docker build -t dockerID/ProjectName:Version .` | Build and tag an image from a Dockerfile              |
| `docker image ls`                                | List images                                           |
| `docker image rm`                                | Remove one or more images                             |
| `docker image prune`                             | Remove unused images                                  |
| `docker image history`                           | Show the history of an image                          |
| `docker image pull`                              | Download an image from a registry                     |
| `docker image push`                              | Upload an image to a registry                         |
| `docker image tag`                               | Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE |
| `docker container commit`                        | Create a new image from a container's changes         |

## Docker Image

- `Docker Image`:

  - a **snapshot** or blueprint of the libraries and dependencies required inside a container for an application to run, along with **startup command**.

  - = file system snapshot + startup command

- `Docker File`:

  - a plain text file containing configuration to define how container should behave.

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

[TOP](#docker-image)
