## Types of Networks in Docker

- Default network for container

| Driver  | Description                                                                  |
| ------- | ---------------------------------------------------------------------------- |
| bridge  | The **default** network driver.                                              |
| host    | Remove network isolation between the **container** and the **Docker host**.  |
| none    | **Completely isolate** a container from the host and other containers.       |
| overlay | Overlay networks **connect multiple** Docker daemons together.               |
| ipvlan  | IPvlan networks provide **full control** over both IPv4 and IPv6 addressing. |
| macvlan | Assign a MAC address to a container.                                         |

---

### Host Network

- It **removes** the network **isolation** between the `container` and the `host`.
- The `container` uses the `host`'s network **namespace**, **IP** address, and network **ports**.
- This can be useful if a container **needs to access host `network interfaces`** or very **low latency** is required for network access.

---

### None Network

- It provides **complete isolation** from **all other** networks.
- Containers on **none** network have **no** `network interfaces`.
- Handy to use for running containers that do **not need any access** to the network.

---

### Overlay Network

- designed for **multi-host networking** in a `Docker swarm cluster`.
- Allows containers running on different `Docker hosts` to **communicate with each other**.
- It creates a **virtual overlay network** across several hosts.

---

### Macvlan Network

- **Assigns** a `MAC address` to the `container`, thus making it appear on the network as **if it were an actual device**.
- This is useful in scenarios where you need to **integrate** `Docker containers` into **existing networks** that require specific `MAC addresses` or when the containers are supposed to communicate directly with some `physical devices`.

---

### IPvlan Network

- It provides finer control of `IPv4` and `IPv6` addressing for containers.
- It provides different **modes** like `L2` or `L3` to serve different isolation and routing needs.

---

## Docker Commands

| Command                                             | Description                                                         |
| --------------------------------------------------- | ------------------------------------------------------------------- |
| `docker network ls`                                 | List all Docker networks                                            |
| `docker network inspect network_name`               | Show detailed info about a specific network                         |
| `docker network create network_name`                | Create a default (bridge) network                                   |
| `docker network create -d bridge network_name`      | Create a custom bridge network                                      |
| `docker network create -d overlay network_name`     | Create an overlay network (used in Swarm)                           |
| `docker network create -d macvlan network_name`     | Create a macvlan network for bridging to host network               |
| `docker network create -d transparent network_name` | Create a transparent bridge network on Windows (for VM integration) |
| `docker network rm network_name`                    | Remove a Docker network (only if no containers are using it)        |
| `docker network prune`                              | Remove unused networks to free up resources                         |

- Connect/Disconnect Containers to/from Networks

| Command                                                 | Description                              |
| ------------------------------------------------------- | ---------------------------------------- |
| `docker network connect network_name container_name`    | Connect a running container to a network |
| `docker network disconnect network_name container_name` | Disconnect a container from a network    |

---

- Create a Transparent Network on Windows

```sh
docker network create -d transparent `
  --subnet=192.168.128.0/24 `
  --gateway=192.168.128.1 `
  -o com.docker.network.windowsshim.interface="VMware Network Adapter VMnet2" `
  pxe_net
```

- Create a Macvlan Network

```sh
docker network create --driver macvlan `
  --subnet=192.168.128.0/24 `
  --gateway=192.168.128.1 `
  -o parent=eth0 `
  pxe_net
```

---

### Bridge Network (Default)

- **Default network** created automatically when installing Docker.
- Offers an essential **isolation** between `containers` on the same `host`.
- allows it to **communicate between `containers` on the same network** by their **IP addresses** or **names** of the `containers`.
- possible for `containers` to **use the `host`'s network connection** to obtain access to **external networks**.

- By default, Docker uses the `172.17.0.0/16` subnet for its **default bridge network**.
  - This means containers connected to the default bridge network will typically be assigned IP addresses within this range.

---

### Lab: Bridge Network

```sh
# list all network
docker network ls
# NETWORK ID     NAME             DRIVER    SCOPE
# 64ccce4b39fe   bridge           bridge    local
# 00ff80315dde   host             host      local
# dfae2c7dc626   none             null      local

# inspect bridge
docker network inspect bridge
# [
#     {
#         "Name": "bridge",
#         "Id": "64ccce4b39fea1c2c9ff29d9c39c2edce435d6c506a53a012dc5b33e69ec7aff",
#         "Created": "2025-04-20T01:21:41.301203897Z",
#         "Scope": "local",
#         "Driver": "bridge",
#         "EnableIPv6": false,
#         "IPAM": {
#             "Driver": "default",
#             "Options": null,
#             "Config": [
#                 {
#                     "Subnet": "172.17.0.0/16",
#                     "Gateway": "172.17.0.1"
#                 }
#             ]
#         },
#         "Internal": false,
#         "Attachable": false,
#         "Ingress": false,
#         "ConfigFrom": {
#             "Network": ""
#         },
#         "ConfigOnly": false,
#         "Containers": {},
#         "Options": {
#             "com.docker.network.bridge.default_bridge": "true",
#             "com.docker.network.bridge.enable_icc": "true",
#             "com.docker.network.bridge.enable_ip_masquerade": "true",
#             "com.docker.network.bridge.host_binding_ipv4": "0.0.0.0",
#             "com.docker.network.bridge.name": "docker0",
#             "com.docker.network.driver.mtu": "1500"
#         },
#         "Labels": {}
#     }
# ]
```

---

- Create a container using bridge network

```sh
# run 2 containers
docker run -d --name myapp01 -p 8081:8080 myapp:v1
docker run -d --name myapp02 -p 8082:8080 myapp:v1

docker ps

docker inspect myapp01
docker inspect myapp02
# confirm ip
curl localhost:8081/api/info
curl localhost:8082/api/info

# confirm 2 apps in the same bridge network can communicate with each other
docker exec -it myapp01 sh
curl ip_myapp01:8080/api/info
curl ip_myapp02:8080/api/info

# clear
docker rm -f myapp01 myapp02
```

---

- Create a custom defined network

```sh
docker network create my-bridge-net --subnet 10.0.0.0/19 --gateway 10.0.0.1
# confirm
docker network ls

# inspect
docker inspact my-bridge-net
```

- Create container using custom network

```sh
docker run -d --name myapp01 -p 8081:8080 --network my-bridge-net myapp:v1
docker run -d --name myapp02 -p 8082:8080 --network my-bridge-net myapp:v1

# confrim
curl localhost:8081/api/info
curl localhost:8082/api/info

docker exec -it myapp01 sh
# using dns to access app
curl myapp02:8080/api/info

# clean
docker rm -f myapp01 myapp02
```

- Delete custom network

```sh
docker network rm my-bridge-net
docker network ls
```

---

- Compose method

- `compose.bridge.yaml`

```yaml
services:
  myapp01:
    image: myapp:v1
    ports:
      - 8081:8080
    networks:
      - my-bridge-net
  myapp02:
    image: myapp:v1
    ports:
      - 8082:8080
    networks:
      - my-bridge-net

networks:
  my-bridge-net:
    driver: bridge
    ipam:
      - subnet: "10.0.0.0/19"
        gateway: "10.0.0.1"
```

```sh
docker compose -f compose.bridge.yaml up -d
curl localhost:8081/api/info
curl localhost:8082/api/info

docker compose -f compose.bridge.yaml down
```