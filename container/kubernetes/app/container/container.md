# Kubernetes - Application: Pod - Container

[Back](../../index.md)

- [Kubernetes - Application: Pod - Container](#kubernetes---application-pod---container)
  - [Container](#container)
    - [A pod to contain just a single container](#a-pod-to-contain-just-a-single-container)
    - [running only one process in each container.](#running-only-one-process-in-each-container)
    - [a pod combines multiple containers](#a-pod-combines-multiple-containers)
    - [one service each pod](#one-service-each-pod)
  - [Types of Pod](#types-of-pod)
    - [Single Container Pod](#single-container-pod)
    - [Multi Container Pod](#multi-container-pod)
  - [Entrypoint](#entrypoint)

---

## Container

- a `pod` is a **co-located group** of `containers` and the basic building block in Kubernetes.
- a **single** `pod` instance **never spans** **multiple** `nodes`.

---

### A pod to contain just a single container

### running only one process in each container.

- `Containers` are designed to run **only a single** `process`, not counting any `child processes` that it spawns.

  - `Container` only **restarts** when the `root process` dies.
  - e.g., container_w (process_w) writes log; Container_r (Process_r) reads log.
    - If process_w dies, only requires container_w restart.
  - Otherwise, hard to manage
    - e.g., One container (2 processes) read and write log. If either process dies, whether the whole container restarts.

- Therefore, one container should not have multiple processes.

---

### a pod combines multiple containers

- `pod`:

  - a design to run related processes together even when divided into multiple containers.
    - workload needs **multiple** `processes`; However, a **single** `container` should not have multiple `processes`.
    - `processces` in **multiple** `containers` within the **same** `pod` can **conmunicate** with each other and share resources.
  - A `pod` makes these **interconnected** `containers` manageable as one unit.

- All `containers` in a `pod` **share**:

  - the **same** `Network namespace` and thus the `network interfaces`, `IP address(es)` and `port space`
    - 2 `containers` cannot bind to the same `port`
    - Inter-container communication is enbled through the loopback device.
    - External communication is enbled by the shared network interfaces and ports.
  - the same **system hostname**, because sharing the `UTS namespace`
  - the same single **process tree**, because using the single `PID namespace`.

- each `container` always has its **own** `Mount namespace`
  - container has its own file system.
  - if **sharing file system** is required, can mount a **shared volumes** with individual `mount namespace`

---

### one service each pod

- Benefit:
  - the pod serves as the basic unit of horizontal scaling. 
  - K8s scales the pod.

---

## Types of Pod

- There are two types of Pods
  - Single container pod
  - Multi container pod

---

### Single Container Pod

- `Single Container Pod`
  - created with the `kubctl run` command, where you have **a** defined image on the Docker registry which we will pull while creating **a pod**.

```sh
kubectl run pod_name --image=registry_image_name
# example
kubectl run tomcat --image = tomcat:8.0
```

- by creating the **yaml** file and then running the `kubectl create` command.

```yaml
# tomcat.yml
apiVersion: v1
kind: Pod
metadata:
   name: Tomcat
spec:
   containers:
   - name: Tomcat
    image: tomcat: 8.0
    ports:
  containerPort: 7500
   imagePullPolicy: Always
```

```sh
kubectl create -f tomcat.yml
```

---

### Multi Container Pod

- `Multi container pods` are created using **yaml mail** with the definition of the containers.
  - use the same network and UTS namespaces
    - see the same system hostname
    - use the same network interfaces, share the same IP address and port space

```yaml
apiVersion: v1
kind: Pod
metadata:
   name: Tomcat
spec:
   containers:
   - name: Tomcat
    image: tomcat: 8.0
    ports:
containerPort: 7500
   imagePullPolicy: Always
   - name: Database
   Image: mongoDB
   Ports:
containerPort: 7501
   imagePullPolicy: Always
```

> create one pod with two containers inside it, one for tomcat and the other for MongoDB.

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
