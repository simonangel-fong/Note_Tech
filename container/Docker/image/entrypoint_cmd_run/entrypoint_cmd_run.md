# Docker - Image: `ENTRYPOINT` vs `CMD` vs `RUN`

[Back](../../index.md)

- [Docker - Image: `ENTRYPOINT` vs `CMD` vs `RUN`](#docker---image-entrypoint-vs-cmd-vs-run)
  - [`ENTRYPOINT`, `CMD`, `RUN`](#entrypoint-cmd-run)
    - [Comparison](#comparison)
  - [Lab: `CMD` only](#lab-cmd-only)
  - [Lab: `ENTRYPOINT` only](#lab-entrypoint-only)
  - [Lab: `ENTRYPOINT` \& `CMD`](#lab-entrypoint--cmd)

---

## `ENTRYPOINT`, `CMD`, `RUN`

- `ENTRYPOINT`:

  - the **instruction** that defines the **executable** that always starts as `PID 1(Docker namespace)` when the container starts.
  - can pair with `CMD` for default **args**.

- `CMD`:

  - the **instruction** that sets the **default command** or **default arguments** used at **container start**.
  - If `ENTRYPOINT` **exists**, `CMD` is its **default args**;
    - otherwise `CMD` is the **command**.

- `RUN`
  - the **instruction** that **executes during image build** to bake changes into **layers** (install packages, compile, etc.).
  - Doesn’t run when the container starts.

---

### Comparison

| Concept      | When it runs    | Primary role                              | Typical override                                 |
| ------------ | --------------- | ----------------------------------------- | ------------------------------------------------ |
| `RUN`        | Build time      | Build the image (make filesystem changes) | **Not** applicable at **runtime**; rebuild image |
| `ENTRYPOINT` | Container start | Fix the main **executable** (`PID 1`)     | `docker run --entrypoint ...`                    |
| `CMD`        | Container start | Default **command**/**args**              | Extra args or command at end of `docker run`     |

---

## Lab: `CMD` only

```Dockerfile
FROM alpine:latest
RUN apk add --no-cache bash
CMD ["echo", "Messge from CMD"]
```

```sh
docker build -t demo_cmd .

# run cmd
docker run --rm demo_cmd
# Messge from CMD

# run override
docker run --rm demo_cmd echo "This is overridden"
# This is overridden
```

---

## Lab: `ENTRYPOINT` only

```Dockerfile
FROM alpine:latest
RUN apk add --no-cache bash
ENTRYPOINT ["echo"]
```

```sh
docker build -t demo_entrypoint .

# pass arg with command
docker run --rm demo_entrypoint "Message from ENTRYPOINT"
# Message from ENTRYPOINT

# overriden entrypoint
docker run --rm --entrypoint /bin/bash demo_entrypoint -c "echo override entrypint"
# override entrypint
```

---

## Lab: `ENTRYPOINT` & `CMD`

```Dockerfile
FROM alpine:latest
RUN apk add --no-cache bash
ENTRYPOINT ["echo"]
CMD ["cmd","&","entrypoint"]
```

```sh
docker build -t demo_cmd_entrypoint .

# run entrypoin + cmds
docker run --rm demo_cmd_entrypoint
# cmd & entrypoint

# override cmds
docker run --rm demo_cmd_entrypoint "override cmd"
# override cmd

# override entrypoint & cmd
docker run --rm --entrypoint /bin/bash demo_cmd_entrypoint -c "echo 'override entrypoint & cmd'"
# override entrypoint & cmd
```
