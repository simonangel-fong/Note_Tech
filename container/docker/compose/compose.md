# Docker - Compose

[Back](../index.md)

- [Docker - Compose](#docker---compose)
  - [Compose](#compose)
  - [Compose](#compose-1)
  - [Docker compose file](#docker-compose-file)
  - [Docker Compose profiles](#docker-compose-profiles)

---

## Compose

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

## Docker compose file

```yaml
services:
  # The web application service
  web:
    build: . # Build the image from a Dockerfile in the current directory
    ports:
      - "8000:5000" # Map host port 8000 to container port 5000
    environment:
      - DATABASE_URL=postgres://user:password@db:5432/myapp
    depends_on:
      - db # Ensure 'db' service starts before 'web'

  # The database service
  db:
    image: postgres:15-alpine
    volumes:
      - db_data:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: myapp

volumes:
  db_data: # Named volume to persist database data
```

## Docker Compose profiles

- `Docker Compose profiles`
  - let you **selectively start only certain services** in a `docker-compose.yml` file.

```yaml
services:
  web:
    image: nginx

  db:
    image: mysql

  adminer:
    image: adminer
    profiles: ["dev"]
```

```sh
# without profile
docker compose up 
# web + db

# with profile
docker compose --profile dev up
# web db adminer
```