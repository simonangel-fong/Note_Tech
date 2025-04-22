# Docker Project: Node JS Web App

[Back](../index.md)

---

## Goal

- Create Node JS web app
- Create a Dockerfile
- Build image from Dockerfile
- Run image as container
- Connect to web app from a browser

---

## Node JS App

- `index.js`

```js
const express = require("express");

const app = express();

app.get("/", (req, res) => {
  res.send("<h1>Hi there!</h1>");
});

app.listen(8080, () => {
  console.log("Listening on port 8080");
});
```

- `package.json`

```json
{
  "dependencies": {
    "express": "*"
  },
  "scripts": {
    "start": "node index.js"
  }
}
```

---

## Dockerfile

```dockerfile
# base image
FROM node:alpine

# install dependencies
# create a work dir for files
WORKDIR /usr/app

# copy package.json only to cach and install npm
COPY ./package.json ./
RUN npm install

# copy all files in the current dir to pwd of container
COPY ./ ./

# startup command
CMD ["npm", "start"]

```

---

## Build and Run

```sh
docker build -t simonangelfong/simplenodejs .

# port forwarding / port mapping
docker run -p 8080:8080 simonangelfong/simplenodejs
```

---

[TOP](#docker-project-node-js-web-app)
