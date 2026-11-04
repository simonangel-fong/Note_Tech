# System Design: Fundamental - Load Balancing

[Back](../system_design.md)

- [System Design: Fundamental - Load Balancing](#system-design-fundamental---load-balancing)
  - [Load Balancing](#load-balancing)
    - [Benefits](#benefits)
    - [Algorithms](#algorithms)
    - [Redundant Load Balancers](#redundant-load-balancers)

---

## Load Balancing

- `Load Balancer (LB)`
  - helps to **spread the traffic across** a cluster of servers to improve responsiveness and **availability** of applications, websites or databases.
  - **keeps track of the status** of all the resources while distributing requests.
    - If a server is **not available** to take new requests or is **not responding** or has elevated **error rate**, LB will **stop sending traffic** to such a server.
  - improve overall `availability` by
    - reducing individual server load
    - preventing any one application server from becoming **a single point of failure**

- sits between the **client** and the **server**
  - accepting **incoming network** and **application traffic**
  - distributing the traffic across **multiple backend servers** using various algorithms.

---

- add LBs at three places
  - Between the **user** and the **web server**
  - Between **web servers** and an **internal platform layer**, like application servers or cache servers
  - Between **internal platform layer** and **database**.

![lb](./img/lb.png)

---

### Benefits

- Users experience **faster, uninterrupted service**.
- Service providers experience **less downtime** and **higher throughput**.
- Load balancing makes it easier for system administrators to handle incoming requests while decreasing wait time for users.
- **Smart load balancers** provide benefits like **predictive analytics** that determine traffic bottlenecks before they happen.
  - As a result, the smart load balancer gives an organization **actionable insights**. These are key to automation and can help drive business decisions.
- System administrators experience fewer failed or stressed components.
  - Instead of a single device performing a lot of work, load balancing has several devices perform a little bit of work.

---

### Algorithms

- How does the load balancer choose the backend server?
  - two factors:
    - They will first ensure that the server they choose is actually **responding** appropriately to requests
    - then use a pre-configured **algorithm** to select one from the set of healthy servers.

- `Health Checks`
  - only forward traffic to “healthy” backend servers.
  - To monitor the health of a backend server, “health checks” regularly **attempt to connect to backend servers** to ensure that servers are listening.
    - If a server fails a health check, it is **automatically removed** from the pool, and traffic will **not be forwarded** to it until it responds to the health checks again.

- common algorithms

- `Least Connection Method`:
  - directs traffic to the server **with the fewest active connections**.
  - when there are a **large number** of **persistent** client connections which are **unevenly distributed** between the servers.
- `Least Response Time Method`:
  - directs traffic to the server with the **fewest active connections** and the **lowest average response time**.
- `Least Bandwidth Method`
  - selects the server that is currently serving the **least amount of traffic** measured in megabits per second (Mbps).
- `Round Robin Method`:
  - cycles through a list of servers and sends each new request to the next server.
  - When it reaches the end of the list, it starts over at the beginning.
    - It is **most useful** when the servers are of **equal specification** and there are not many persistent connections.
- `Weighted Round Robin Method`:
  - The **weighted round-robin** scheduling is designed to better **handle servers with different processing capacities**.
  - Each server is assigned a **weight** (an integer value that indicates the processing capacity).
    - Servers with **higher** weights receive new connections **before** those with **less** weights and servers with higher weights get more connections than those with less weights
- `IP Hash`:
  - Under this method, a **hash of the IP address of the client** is calculated to redirect the request to a server.

---

### Redundant Load Balancers

- a **second** load balancer can be connected to the first to form a cluster.
  - Each LB monitors the health of the other
  - both of them are equally capable of serving traffic and failure detection,
  - in the event the main load balancer fails, the **second** load balancer **takes over**

---
