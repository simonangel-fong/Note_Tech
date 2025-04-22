# Docker - Hello World

[Back](../index.md)

---

## Install Docker Desktop

- ref: https://www.docker.com/products/docker-desktop/

---

## Django application

- repo: https://github.com/simonangel-fong/Django_Simple_CRUD.git

---

## Define Docker File

- Document code:
- https://hub.docker.com/_/python

- Create a Dockerfile in your Python app project

```dockerfile
FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./your-daemon-or-script.py" ]
```

---

tutorial code

```dockerfile
FROM python:3.8-buster

ENV PYTHONBUFFERED-1

WORKDIR /django

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD python manage.py runserver 0.0.0.0:8000

```

---

- Create a docker-compose.yml file

```yml

version: "3.8"

services:
 app:
  build: . 
  volumes: 
   - .:/django
  ports:
    - 8000:8000
  image: app:django
  container_name: my_first_django_container
  command: python manage.py runserver 0.0.0.0:8000

```

---

- Docker command

In the path with manage.py

```sh
# to build the docker image
docker-compose build
```

then check the docker image in the docker desktop

- Run docker

```sh
docker-compose up
```

Check the Containers tab in docker desktop.

---
