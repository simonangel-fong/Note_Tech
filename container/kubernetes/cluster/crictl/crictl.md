# Kubernetes - crictl

[Back](../../index.md)

- [Kubernetes - crictl](#kubernetes---crictl)
  - [`crictl`](#crictl)
    - [Imperative Command](#imperative-command)
  - [Lab: crictl](#lab-crictl)
    - [List pod](#list-pod)
    - [List Container](#list-container)

---

## `crictl`

### Imperative Command

| Command            | Description                          |
| ------------------ | ------------------------------------ |
| `crictl version`   | Display runtime version information. |
| `crictl --version` | Display crictl version.              |

- Image

| Command                | Description                             |
| ---------------------- | --------------------------------------- |
| `crictl image`         | List images                             |
| `crictl pull NAME:TAG` | Pull an image from a registry           |
| `crictl imagefsinfo`   | Show image filesystem info              |
| `crictl inspecti`      | Return the status of one or more images |
| `crictl rmi IMAGE-ID`  | Remove one or more images               |
| `crictl rmi -a`        | Remove all images                       |
| `crictl rmi -q`        | Remove all unused images                |

- Container Info

| Command                                             | Description                                                                |
| --------------------------------------------------- | -------------------------------------------------------------------------- |
| `crictl ps`                                         | Lists running containers.                                                  |
| `crictl ps -a`                                      | Lists all containers, including exited ones.                               |
| `crictl ps -l`                                      | Lists the most recently created container                                  |
| `crictl ps --image IMAGE`                           | Filter containers by image                                                 |
| `crictl ps --label key1=value1 --label key2=value2` | Filter containers by key=value label.                                      |
| `crictl ps --name NAME`                             | Filter containers by container name.                                       |
| `crictl ps --namespace NS`                          | Filter containers by namespace.                                            |
| `crictl ps --state STATE`                           | Filter containers by container state, created, running, exited or unknown. |
| `crictl stats`                                      | List container(s) resource usage statistics                                |
| `crictl stats -a`                                   | List all container(s) resource usage statistics                            |
| `crictl stats --id ID`                              | List container usage statistics matching id filter                         |
| `crictl stats --label KEY=VALUE`                    | List container usage statistics matching label filter                      |
| `crictl stats --pod POD_ID`                         | List container usage statistics matching pod id filter                     |
| `crictl stats -w`                                   | Watch pod resources                                                        |
| `crictl logs CONTAINER-ID`                          | Show the logs of a container                                               |
| `crictl logs CONTAINER-ID -t`                       | Show the logs of a container with timestamps                               |
| `crictl logs CONTAINER-ID -f`                       | Follow log output                                                          |
| `crictl logs CONTAINER-ID --tail N`                 | Show last N line of logs                                                   |
| `crictl logs CONTAINER-ID  --since timestamp`       | Show logs since timestamp                                                  |
| `crictl logs CONTAINER-ID  --since 30m`             | Show logs in last 30 minutes                                               |

- Container Management

| Command                                                      | Description                           |
| ------------------------------------------------------------ | ------------------------------------- |
| `crictl create`                                              | Create a new container                |
| `crictl start CONTAINER-ID`                                  | Start one or more created containers  |
| `crictl stop CONTAINER-ID`                                   | Stop one or more running containers   |
| `crictl update CONTAINER-ID`                                 | Update one or more running containers |
| `crictl attach CONTAINER-ID`                                 | Attach to a running container         |
| `crictl rm CONTAINER-ID`                                     | Remove one or more containers         |
| `crictl rm CONTAINER-ID --force`/`crictl rm CONTAINER-ID -f` | Force removal of the container        |

- Execute command in a container

| Command                                                  | Description                                                          |
| -------------------------------------------------------- | -------------------------------------------------------------------- |
| `crictl exec CONTAINER-ID COMMAND ARG`                   | Run a command in a running container                                 |
| `crictl exec -it CONTAINER-ID COMMAND ARG`               | Run a command in a running container, with pseudo-TTY and open STDIN |
| `crictl exec CONTAINER-ID COMMAND ARG --ignore-errors`   | Run a command in a running container, ignore errors                  |
| `crictl exec CONTAINER-ID COMMAND ARG --image IMG`       | Run a command in a running container matching image filter           |
| `crictl exec CONTAINER-ID COMMAND ARG --label KEY=VALUE` | Run a command in a running container matching label filter           |
| `crictl exec CONTAINER-ID COMMAND ARG --name NAME`       | Run a command in a running container matching name filter            |
| `crictl exec CONTAINER-ID COMMAND ARG --pod POD`         | Run a command in a running container matching pod filter             |
| `crictl exec CONTAINER-ID COMMAND ARG --state STATE`     | Run a command in a running container matching state filter           |

- Pod Info

| Command                                               | Description                                       |
| ----------------------------------------------------- | ------------------------------------------------- |
| `crictl pods`                                         | Lists running pod.                                |
| `crictl pods --lastest`/`crictl pods -l`              | Lists the most recently created pod.              |
| `crictl pods --label key1=value1 --label key2=value2` | Filter pod by key=value label.                    |
| `crictl pods --name NAME`                             | Filter pod by container name.                     |
| `crictl pods --namespace NS`                          | Filter pod by namespace.                          |
| `crictl pods --state STATE`                           | Filter pod by container state: ready or notready. |

- Pod Management

| Command                                             | Description                            |
| --------------------------------------------------- | -------------------------------------- |
| `crictl runp`                                       | Run a new pod                          |
| `crictl stopp POD-ID`                               | Stop one or more running pods          |
| `crictl port-forward POD-ID LOCAL_PORT:REMOTE_PORT` | Forward local port to a pod            |
| `crictl statsp`                                     | List pod statistics.                   |
| `crictl statsp --id ID`                             | List pod statistics with id filter.    |
| `crictl statsp --label KEY=VALUE`                   | List pod statistics with label filter. |
| `crictl statsp --watch`                             | Watch pod resources.                   |

---

## Lab: crictl

### List pod

```sh
sudo crictl pods
# POD ID              CREATED             STATE               NAME                                      NAMESPACE           ATTEMPT             RUNTIME
# 7e6062a1631dd       21 minutes ago      Ready               csi-node-driver-wswt4                     calico-system       7                   (default)
# 7616d45f5922e       21 minutes ago      Ready               whisker-684c89ddf6-pxbdk                  calico-system       7                   (default)
# fa20fa61ff061       21 minutes ago      Ready               calico-apiserver-6c78765b56-mdmmw         calico-system       7                   (default)
# e45b83ce7408e       21 minutes ago      Ready               calico-kube-controllers-cd4494644-vjb6m   calico-system       7                   (default)
# 0aca30eb3a043       21 minutes ago      Ready               calico-apiserver-6c78765b56-6vjhz         calico-system       7                   (default)
# f17aef575721a       21 minutes ago      Ready               goldmane-56f8bf7d87-jgjk9                 calico-system       7                   (default)
# 59ab0bd558c1a       21 minutes ago      Ready               coredns-668d6bf9bc-m8qmh                  kube-system         7                   (default)
# 20a1c4fe37b4a       21 minutes ago      Ready               coredns-668d6bf9bc-7g786                  kube-system         7                   (default)
# b5f40984f1387       22 minutes ago      Ready               calico-node-cdq6h                         calico-system       7                   (default)
# b5ca315d95bcf       22 minutes ago      Ready               kube-proxy-5kcw4                          kube-system         7                   (default)
# 1f3dc39586941       22 minutes ago      Ready               calico-typha-5f9f778ddd-wn6np             calico-system       7                   (default)
# 01f15c23ac078       22 minutes ago      Ready               kube-scheduler-controlplane               kube-system         7                   (default)
# d64ea9fd7fdd7       22 minutes ago      Ready               kube-controller-manager-controlplane      kube-system         7                   (default)
# a10c2a719d577       22 minutes ago      Ready               kube-apiserver-controlplane               kube-system         7                   (default)
# 2f9eaee27e6bf       22 minutes ago      Ready               etcd-controlplane                         kube-system         7                   (default)
```

---

### List Container

```sh
sudo crictl ps
# CONTAINER           IMAGE               CREATED             STATE               NAME                        ATTEMPT             POD ID              POD                                       NAMESPACE
# 6e60084f900ca       ac46eecb3d7f8       25 minutes ago      Running             calico-apiserver            8                   fa20fa61ff061       calico-apiserver-6c78765b56-mdmmw         calico-system
# 24a5f47f3baba       ac46eecb3d7f8       25 minutes ago      Running             calico-apiserver            8                   0aca30eb3a043       calico-apiserver-6c78765b56-6vjhz         calico-system
# 785f938752e49       a06d58cceef55       25 minutes ago      Running             csi-node-driver-registrar   7                   7e6062a1631dd       csi-node-driver-wswt4                     calico-system
# a9095d6c20a30       6f60b868a2970       25 minutes ago      Running             calico-csi                  7                   7e6062a1631dd       csi-node-driver-wswt4                     calico-system
# e719f1892cca0       fd911f8f9ea58       25 minutes ago      Running             whisker-backend             7                   7616d45f5922e       whisker-684c89ddf6-pxbdk                  calico-system
# 418c3f95843e1       a4bcedf3b244f       25 minutes ago      Running             whisker                     7                   7616d45f5922e       whisker-684c89ddf6-pxbdk                  calico-system
# f098ec835c092       95bc8e4bc61e7       26 minutes ago      Running             calico-kube-controllers     7                   e45b83ce7408e       calico-kube-controllers-cd4494644-vjb6m   calico-system
# c28db89bd042a       6eaae458d5f11       26 minutes ago      Running             goldmane                    7                   f17aef575721a       goldmane-56f8bf7d87-jgjk9                 calico-system
# 67c3bf85136a2       c69fa2e9cbf5f       26 minutes ago      Running             coredns                     7                   59ab0bd558c1a       coredns-668d6bf9bc-m8qmh                  kube-system
# a67e574b92fb2       c69fa2e9cbf5f       26 minutes ago      Running             coredns                     7                   20a1c4fe37b4a       coredns-668d6bf9bc-7g786                  kube-system
# b314b9ffb0b9b       f8495fa3f644a       26 minutes ago      Running             calico-node                 7                   b5f40984f1387       calico-node-cdq6h                         calico-system
# ef7d8e6ede7bb       4d8fb2dc57519       26 minutes ago      Running             kube-proxy                  7                   b5ca315d95bcf       kube-proxy-5kcw4                          kube-system
# ec2fc68ca8f42       0aa5de4a226c8       26 minutes ago      Running             calico-typha                7                   1f3dc39586941       calico-typha-5f9f778ddd-wn6np             calico-system
# f24a63f0dc0a6       0175d0a8243db       26 minutes ago      Running             kube-controller-manager     7                   d64ea9fd7fdd7       kube-controller-manager-controlplane      kube-system
# 29f82a5d26059       7757c58248a29       26 minutes ago      Running             kube-apiserver              7                   a10c2a719d577       kube-apiserver-controlplane               kube-system
# 1f90bc9300705       23d6a1fb92fda       26 minutes ago      Running             kube-scheduler              7                   01f15c23ac078       kube-scheduler-controlplane               kube-system
# a9f8c7eb2fb26       8cb12dd0c3e42       26 minutes ago      Running             etcd                        7                   2f9eaee27e6bf       etcd-controlplane                         kube-system
```
