[Back](../../index.md)

---

## Entrypoint




| Docker       | Pod       |
| ------------ | --------- |
| `Entrypoint` | `command` |
| `CMD`        | `args`    |

- `Entrypoint` and `CMD`:

  - Specify the command to run at container startup
  - the same
    - `CMD ["startup.sh"]` == `ENTRYPOINT ["startup.sh"]`

- Can be overridden:

```Dockerfile
FROM debian:buster
COPY . /app
RUN apt-get update
CMD ["cmd1"]
```

```sh
docker run my-container cmd2
```

```Dockerfile
FROM debian:buster
COPY . /app
RUN apt-get update
ENTRYPOINT ["entrypoint.sh"]
```

```sh
docker run
```

---

- When being used in the same Dockerfile
  - `ENTRYPOINT`: the executable
  - `CMD`: the options

```Dockerfile
FROM debian:buster
COPY . /app
RUN apt-get update
ENTRYPOINT ["entrypoint.sh"]
CMD ["param1","param2"]
```

==> `entrypoin.sh param1 param2`

- Cannot be overriden

```sh
docker run my-container cmd2
# == entrypoint.sh cmd2
```
