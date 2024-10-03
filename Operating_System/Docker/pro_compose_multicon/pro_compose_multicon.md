# Project: Docker Compose with Multiple local containers

[Back](../index.md)

- [Project: Docker Compose with Multiple local containers](#project-docker-compose-with-multiple-local-containers)
  - [Goal](#goal)
  - [Web App](#web-app)
    - [Node JS app](#node-js-app)
    - [Dockerfile](#dockerfile)
  - [Docker Compose](#docker-compose)
    - [Yaml File](#yaml-file)
    - [Start Docker compose](#start-docker-compose)

---

| Command                     | Description                                     |
| --------------------------- | ----------------------------------------------- |
| `docker compose up`         | Create and start containers                     |
| `docker compose up -d`      | Detached mode: Run containers in the background |
| `docker compose up --build` | Build images before starting containers         |
| `docker compose down`       | Stop and remove containers, networks            |

---

## Goal

- Count number of visit

  - node app + redis

- solution 1:

  - node app and redis in one container
  - problem:
    - when traffic increases, more container need to be introduced to respond to incoming requests. Some values in redis of different container cannot be sync.

- Solution 2:
  - node app in container; redis in one container
  - when scale up, only the node app container needs to be scaled up. The only one container for redis keep the consisitency.

---

## Web App

### Node JS app

- `package.json`

```json
{
  "dependencies": {
    "express": "*",
    "redis": "2.8.0"
  },
  "scripts": {
    "start": "node index.js"
  }
}
```

- `index.js`

```js
const express = require("express");
const redis = require("redis");

const app = express();
// specify the redis container by it name defined in the docker compose file
const client = redis.createClient({
  host: "redis-server",
  port: 6379, // default port for redis
});

client.set("visits", 0);

app.get("/", (req, res) => {
  client.get("visits", (err, visits) => {
    res.send("Number of visits is " + visits);
    client.set("visits", parseInt(visits) + 1);
  });
});

app.listen(8081, () => {
  console.log("Listening on port 8081");
});
```

---

### Dockerfile

- `Dockerfile`

```dockerfile
# base image
FROM node:alpine

# install dependencies
WORKDIR '/app'

COPY package.json .
RUN npm install

COPY . .

# startup commands
CMD ["npm", "start"]

```

---

## Docker Compose

### Yaml File

- `docker-compose.yml`

```yml
services:
  redis-server:
    image: "redis"
  node-app:
    build: .
    ports:
      - "8081:8081"
```

---

### Start Docker compose

```sh
docker compose up
docker compose up -d
docker ps

docker compose down
docker ps
```

---

---

[TOP](#project-docker-compose-with-multiple-local-containers)
