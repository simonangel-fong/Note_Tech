# Kubernetes: Container - Liveness Probe

[Back](../../index.md)

- [Kubernetes: Container - Liveness Probe](#kubernetes-container---liveness-probe)
  - [Liveness Probe](#liveness-probe)
    - [Manifest File](#manifest-file)
  - [Types of Liveness Probe](#types-of-liveness-probe)
    - [`HTTP GET` Type](#http-get-type)
    - [`TCP Socket` Probe](#tcp-socket-probe)
    - [`Exec` Probe](#exec-probe)
  - [Lab: Liveness Probe](#lab-liveness-probe)
  - [Lab: Liveness Probe - Failed](#lab-liveness-probe---failed)

---

## Liveness Probe

- `liveness probe`

  - used to **periodically check** whether an **application is still alive**
  - specify a `liveness probe` for each container in the pod.

- Work with `restart policy`

  - if the application doesn’t respond, an error occurs, or the response is negative,
    - the `container` is considered **unhealthy** and is **terminated**.
    - The `container` is then **restarted** if the `restart policy` allows it.

- limit:
  - **only** be used in the pod’s `regular containers`.
  - They **can’t be** defined in `init containers`.

---

### Manifest File

```yaml
spec:
  containers:
    # http get
    livenessProbe:
      httpGet:
      path: /
      port: 8080

    # tcp probe
    livenessProbe:
      tcpSocket:
        port: 5432

    # exec probe
    livenessProbe:
      exec:
        command:
        - /usr/bin/healthcheck
```

---

## Types of Liveness Probe

### `HTTP GET` Type

- `HTTP GET probe`
  - sends a `GET` request to the container’s **IP address**, on the network **port** and **path** you specify.
    - If the probe receives a response, and the response code **doesn’t represent an error** (`HTTP response code` is `2xx` or `3xx`), the probe is considered **successful**.
    - If the server returns an **error response code**, or if it doesn’t respond in time, the probe is considered to have **failed**.

---

### `TCP Socket` Probe

- `TCP Socket probe`
  - try with a **TCP connection** to the specified **port** of the container.
    - If the connection is **successfully established**, the probe is considered **successful**.
    - If the connection **can’t** be established in time, the probe is considered **failed**.

### `Exec` Probe

- `Exec probe`

  - **executes a command** inside the container and **checks the exit code** it terminates with.
    - If the exit code is `zero`, the probe is **successful**.
    - A `non-zero` exit code is considered a **failure**.
    - The probe is also considered to have **failed** if the command fails to **terminate in time**.

- default settings:
  - `initialDelaySeconds`: first request is sent `10s` after the container starts
  - `periodSeconds`: repeated every `5s`.
  - `timeoutSeconds`: timeout less then `2s`
  - `failureThreshold`: max failure less than 3 times

---

## Lab: Liveness Probe

```yaml
# demo-liveness-probe.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-liveness-probe
spec:
  containers:
    - name: nginx
      image: nginx
      ports:
        - name: http
          containerPort: 80
      livenessProbe:
        # HTTP GET probe
        httpGet:
          path: /
          port: http # use the port name define int ports
        initialDelaySeconds: 10
        periodSeconds: 5
        timeoutSeconds: 2
        failureThreshold: 3
    - name: redis
      image: redis
      livenessProbe:
        # exec probe
        exec:
          command:
            - "sh"
            - "-c"
            - "redis-cli ping" # Checks if Redis is alive
        initialDelaySeconds: 5 # Initial wait before the first probe
        periodSeconds: 5 # How often to perform the probe
        timeoutSeconds: 2 # Timeout for the probe command
        failureThreshold: 3
```

- run

```sh
kubectl apply -f demo-liveness-probe.yaml
# pod/demo-liveness-probe created

kubectl logs demo-liveness-probe -c nginx -f
# /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
# /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
# /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
# 10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
# 10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
# /docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
# /docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
# /docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
# /docker-entrypoint.sh: Configuration complete; ready for start up
# 2025/12/23 01:13:06 [notice] 1#1: using the "epoll" event method
# 2025/12/23 01:13:06 [notice] 1#1: nginx/1.29.4
# 2025/12/23 01:13:06 [notice] 1#1: built by gcc 14.2.0 (Debian 14.2.0-19)
# 2025/12/23 01:13:06 [notice] 1#1: OS: Linux 5.15.153.1-microsoft-standard-WSL2
# 2025/12/23 01:13:06 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576
# 2025/12/23 01:13:06 [notice] 1#1: start worker processes
# 2025/12/23 01:13:06 [notice] 1#1: start worker process 29
# 2025/12/23 01:13:06 [notice] 1#1: start worker process 30
# 2025/12/23 01:13:06 [notice] 1#1: start worker process 31
# 2025/12/23 01:13:06 [notice] 1#1: start worker process 32
# 2025/12/23 01:13:06 [notice] 1#1: start worker process 33
# 2025/12/23 01:13:06 [notice] 1#1: start worker process 34
# 2025/12/23 01:13:06 [notice] 1#1: start worker process 35
# 2025/12/23 01:13:06 [notice] 1#1: start worker process 36
# 2025/12/23 01:13:06 [notice] 1#1: start worker process 37
# 2025/12/23 01:13:06 [notice] 1#1: start worker process 38
# 2025/12/23 01:13:06 [notice] 1#1: start worker process 39
# 2025/12/23 01:13:06 [notice] 1#1: start worker process 40
# 10.1.0.1 - - [23/Dec/2025:01:13:19 +0000] "GET / HTTP/1.1" 200 615 "-" "kube-probe/1.34" "-"
# 10.1.0.1 - - [23/Dec/2025:01:13:24 +0000] "GET / HTTP/1.1" 200 615 "-" "kube-probe/1.34" "-"
# 10.1.0.1 - - [23/Dec/2025:01:13:29 +0000] "GET / HTTP/1.1" 200 615 "-" "kube-probe/1.34" "-"
# 10.1.0.1 - - [23/Dec/2025:01:13:34 +0000] "GET / HTTP/1.1" 200 615 "-" "kube-probe/1.34" "-"
# 10.1.0.1 - - [23/Dec/2025:01:13:39 +0000] "GET / HTTP/1.1" 200 615 "-" "kube-probe/1.34" "-"
# 10.1.0.1 - - [23/Dec/2025:01:13:44 +0000] "GET / HTTP/1.1" 200 615 "-" "kube-probe/1.34" "-"

kubectl describe pod demo-liveness-probe
# Containers:
#   nginx:
#     Liveness:       http-get http://:http/ delay=10s timeout=2s period=5s #success=1 #failure=3
#   redis:
#     Liveness:       exec [sh -c redis-cli ping] delay=5s timeout=2s period=5s #success=1 #failure=3

kubectl delete -f demo-liveness-probe.yaml
# pod "demo-liveness-probe" deleted from default namespace
```

---

## Lab: Liveness Probe - Failed

```yaml
# demo-liveness-probe-failure.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-liveness-probe-failure
spec:
  containers:
    - name: nginx
      image: nginx
      ports:
        - name: http
          containerPort: 80
      livenessProbe:
        # HTTP GET probe
        httpGet:
          path: /
          port: 8080
        initialDelaySeconds: 10
        periodSeconds: 5
        timeoutSeconds: 2
        failureThreshold: 3
    - name: redis
      image: redis
      livenessProbe:
        # exec probe
        exec:
          command:
            - "sh"
            - "-c"
            - "redis-cli ping1" # incorrect command
        initialDelaySeconds: 10
        periodSeconds: 5
        timeoutSeconds: 2
        failureThreshold: 3
```

- run

```sh
kubectl apply -f demo-liveness-probe-failure.yaml
# pod/demo-liveness-probe-failure created

kubectl get pod -w
# NAME                          READY   STATUS             RESTARTS      AGE
# demo-liveness-probe-failure   1/2     CrashLoopBackOff   5 (69s ago)   4m20s
# demo-liveness-probe-failure   2/2     Running            6 (93s ago)   4m44s
# demo-liveness-probe-failure   1/2     CrashLoopBackOff   6 (1s ago)    5m7s

kubectl logs demo-liveness-probe-failure -c nginx -f
# /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
# /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
# /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
# 10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
# 10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
# /docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
# /docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
# /docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
# /docker-entrypoint.sh: Configuration complete; ready for start up
# 2025/12/23 01:34:36 [notice] 1#1: using the "epoll" event method
# 2025/12/23 01:34:36 [notice] 1#1: nginx/1.29.4
# 2025/12/23 01:34:36 [notice] 1#1: built by gcc 14.2.0 (Debian 14.2.0-19)
# 2025/12/23 01:34:36 [notice] 1#1: OS: Linux 5.15.153.1-microsoft-standard-WSL2
# 2025/12/23 01:34:36 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576
# 2025/12/23 01:34:36 [notice] 1#1: start worker processes
# 2025/12/23 01:34:36 [notice] 1#1: start worker process 28
# 2025/12/23 01:34:36 [notice] 1#1: start worker process 29
# 2025/12/23 01:34:36 [notice] 1#1: start worker process 30
# 2025/12/23 01:34:36 [notice] 1#1: start worker process 31
# 2025/12/23 01:34:36 [notice] 1#1: start worker process 32
# 2025/12/23 01:34:36 [notice] 1#1: start worker process 33
# 2025/12/23 01:34:36 [notice] 1#1: start worker process 34
# 2025/12/23 01:34:36 [notice] 1#1: start worker process 35
# 2025/12/23 01:34:36 [notice] 1#1: start worker process 36
# 2025/12/23 01:34:36 [notice] 1#1: start worker process 37
# 2025/12/23 01:34:36 [notice] 1#1: start worker process 38
# 2025/12/23 01:34:36 [notice] 1#1: start worker process 39
# 2025/12/23 01:34:58 [notice] 1#1: signal 3 (SIGQUIT) received, shutting down
# 2025/12/23 01:34:58 [notice] 29#29: gracefully shutting down
# 2025/12/23 01:34:58 [notice] 29#29: exiting
# 2025/12/23 01:34:58 [notice] 29#29: exit
# 2025/12/23 01:34:58 [notice] 28#28: gracefully shutting down
# 2025/12/23 01:34:58 [notice] 30#30: gracefully shutting down
# 2025/12/23 01:34:58 [notice] 28#28: exiting
# 2025/12/23 01:34:58 [notice] 31#31: gracefully shutting down
# 2025/12/23 01:34:58 [notice] 30#30: exiting
# 2025/12/23 01:34:58 [notice] 31#31: exiting
# 2025/12/23 01:34:58 [notice] 28#28: exit
# 2025/12/23 01:34:58 [notice] 32#32: gracefully shutting down
# 2025/12/23 01:34:58 [notice] 32#32: exiting
# 2025/12/23 01:34:58 [notice] 30#30: exit
# 2025/12/23 01:34:58 [notice] 34#34: gracefully shutting down
# 2025/12/23 01:34:58 [notice] 31#31: exit
# 2025/12/23 01:34:58 [notice] 34#34: exiting
# 2025/12/23 01:34:58 [notice] 33#33: gracefully shutting down
# 2025/12/23 01:34:58 [notice] 33#33: exiting
# 2025/12/23 01:34:58 [notice] 32#32: exit
# 2025/12/23 01:34:58 [notice] 33#33: exit
# 2025/12/23 01:34:58 [notice] 34#34: exit
# 2025/12/23 01:34:58 [notice] 36#36: gracefully shutting down
# 2025/12/23 01:34:58 [notice] 36#36: exiting
# 2025/12/23 01:34:58 [notice] 36#36: exit
# 2025/12/23 01:34:58 [notice] 35#35: gracefully shutting down
# 2025/12/23 01:34:58 [notice] 35#35: exiting
# 2025/12/23 01:34:58 [notice] 35#35: exit
# 2025/12/23 01:34:58 [notice] 37#37: gracefully shutting down
# 2025/12/23 01:34:58 [notice] 37#37: exiting
# 2025/12/23 01:34:58 [notice] 37#37: exit
# 2025/12/23 01:34:58 [notice] 38#38: gracefully shutting down
# 2025/12/23 01:34:58 [notice] 38#38: exiting
# 2025/12/23 01:34:58 [notice] 38#38: exit
# 2025/12/23 01:34:58 [notice] 39#39: gracefully shutting down
# 2025/12/23 01:34:58 [notice] 39#39: exiting
# 2025/12/23 01:34:58 [notice] 39#39: exit
# 2025/12/23 01:34:58 [notice] 1#1: signal 17 (SIGCHLD) received from 32
# 2025/12/23 01:34:58 [notice] 1#1: worker process 32 exited with code 0
# 2025/12/23 01:34:58 [notice] 1#1: worker process 35 exited with code 0
# 2025/12/23 01:34:58 [notice] 1#1: signal 29 (SIGIO) received
# 2025/12/23 01:34:58 [notice] 1#1: signal 17 (SIGCHLD) received from 39
# 2025/12/23 01:34:58 [notice] 1#1: worker process 28 exited with code 0
# 2025/12/23 01:34:58 [notice] 1#1: worker process 29 exited with code 0
# 2025/12/23 01:34:58 [notice] 1#1: worker process 31 exited with code 0
# 2025/12/23 01:34:58 [notice] 1#1: worker process 37 exited with code 0
# 2025/12/23 01:34:58 [notice] 1#1: worker process 39 exited with code 0
# 2025/12/23 01:34:58 [notice] 1#1: signal 29 (SIGIO) received
# 2025/12/23 01:34:58 [notice] 1#1: signal 17 (SIGCHLD) received from 37
# 2025/12/23 01:34:58 [notice] 1#1: signal 17 (SIGCHLD) received from 36
# 2025/12/23 01:34:58 [notice] 1#1: worker process 36 exited with code 0
# 2025/12/23 01:34:58 [notice] 1#1: signal 29 (SIGIO) received
# 2025/12/23 01:34:58 [notice] 1#1: signal 17 (SIGCHLD) received from 38
# 2025/12/23 01:34:58 [notice] 1#1: worker process 38 exited with code 0
# 2025/12/23 01:34:58 [notice] 1#1: signal 29 (SIGIO) received
# 2025/12/23 01:34:58 [notice] 1#1: signal 17 (SIGCHLD) received from 34
# 2025/12/23 01:34:58 [notice] 1#1: worker process 34 exited with code 0
# 2025/12/23 01:34:58 [notice] 1#1: signal 29 (SIGIO) received
# 2025/12/23 01:34:58 [notice] 1#1: signal 17 (SIGCHLD) received from 30
# 2025/12/23 01:34:58 [notice] 1#1: worker process 30 exited with code 0
# 2025/12/23 01:34:58 [notice] 1#1: signal 29 (SIGIO) received
# 2025/12/23 01:34:58 [notice] 1#1: signal 17 (SIGCHLD) received from 33
# 2025/12/23 01:34:58 [notice] 1#1: worker process 33 exited with code 0
# 2025/12/23 01:34:58 [notice] 1#1: exit


kubectl get events -w
# LAST SEEN   TYPE      REASON      OBJECT                            MESSAGE
# 8m10s       Normal    Scheduled   pod/demo-liveness-probe-failure   Successfully assigned default/demo-liveness-probe-failure to docker-desktop
# 6m29s       Normal    Pulling     pod/demo-liveness-probe-failure   Pulling image "nginx"
# 8m8s        Normal    Pulled      pod/demo-liveness-probe-failure   Successfully pulled image "nginx" in 1.318s (1.318s including waiting). Image size: 59795293 bytes.
# 6m53s       Normal    Created     pod/demo-liveness-probe-failure   Created container: nginx
# 6m53s       Normal    Started     pod/demo-liveness-probe-failure   Started container nginx
# 8m7s        Normal    Pulling     pod/demo-liveness-probe-failure   Pulling image "redis"
# 8m7s        Normal    Pulled      pod/demo-liveness-probe-failure   Successfully pulled image "redis" in 909ms (909ms including waiting). Image size: 53003220 bytes.
# 8m6s        Normal    Created     pod/demo-liveness-probe-failure   Created container: redis
# 8m6s        Normal    Started     pod/demo-liveness-probe-failure   Started container redis
# 4m59s       Warning   Unhealthy   pod/demo-liveness-probe-failure   Liveness probe failed: Get "http://10.1.2.104:8080/": dial tcp 10.1.2.104:8080: connect: connection refused
# 3m4s        Normal    Killing     pod/demo-liveness-probe-failure   Container nginx failed liveness probe, will be restarted
# 7m43s       Normal    Pulled      pod/demo-liveness-probe-failure   Successfully pulled image "nginx" in 916ms (916ms including waiting). Image size: 59795293 bytes.
# 7m18s       Normal    Pulled      pod/demo-liveness-probe-failure   Successfully pulled image "nginx" in 1.027s (1.027s including waiting). Image size: 59795293 bytes.
# 6m53s       Normal    Pulled      pod/demo-liveness-probe-failure   Successfully pulled image "nginx" in 1.012s (1.012s including waiting). Image size: 59795293 bytes.
# 2m48s       Warning   BackOff     pod/demo-liveness-probe-failure   Back-off restarting failed container nginx in pod demo-liveness-probe-failure_default(573bb3ef-de6e-4030-bcde-c4217c3dfca6)
# 46m         Normal    Scheduled   pod/demo-liveness-probe           Successfully assigned default/demo-liveness-probe to docker-desktop
# 46m         Normal    Pulling     pod/demo-liveness-probe           Pulling image "nginx"
# 46m         Normal    Pulled      pod/demo-liveness-probe           Successfully pulled image "nginx" in 1.3s (1.3s including waiting). Image size: 59795293 bytes.
# 46m         Normal    Created     pod/demo-liveness-probe           Created container: nginx
# 46m         Normal    Started     pod/demo-liveness-probe           Started container nginx
# 46m         Normal    Pulling     pod/demo-liveness-probe           Pulling image "redis"
# 46m         Normal    Pulled      pod/demo-liveness-probe           Successfully pulled image "redis" in 956ms (956ms including waiting). Image size: 53003220 bytes.
# 46m         Normal    Created     pod/demo-liveness-probe           Created container: redis
# 46m         Normal    Started     pod/demo-liveness-probe           Started container redis
# 45m         Normal    Killing     pod/demo-liveness-probe           Stopping container nginx
# 45m         Normal    Killing     pod/demo-liveness-probe           Stopping container redis
# 27m         Normal    Scheduled   pod/demo-liveness-probe           Successfully assigned default/demo-liveness-probe to docker-desktop
# 27m         Normal    Pulling     pod/demo-liveness-probe           Pulling image "nginx"
# 27m         Normal    Pulled      pod/demo-liveness-probe           Successfully pulled image "nginx" in 1.148s (1.148s including waiting). Image size: 59795293 bytes.
# 27m         Normal    Created     pod/demo-liveness-probe           Created container: nginx
# 27m         Normal    Started     pod/demo-liveness-probe           Started container nginx
# 27m         Normal    Pulling     pod/demo-liveness-probe           Pulling image "redis"
# 27m         Normal    Pulled      pod/demo-liveness-probe           Successfully pulled image "redis" in 686ms (686ms including waiting). Image size: 53003220 bytes.
# 27m         Normal    Created     pod/demo-liveness-probe           Created container: redis
# 27m         Normal    Started     pod/demo-liveness-probe           Started container redis
# 16m         Normal    Killing     pod/demo-liveness-probe           Stopping container nginx
# 16m         Normal    Killing     pod/demo-liveness-probe           Stopping container redis
# 9m21s       Normal    Scheduled   pod/demo-liveness-probe           Successfully assigned default/demo-liveness-probe to docker-desktop

kubectl describe pod demo-liveness-probe-failure
# Containers:
#   nginx:
#     State:          Waiting
#       Reason:       CrashLoopBackOff
#     Last State:     Terminated
#       Reason:       Completed
#       Exit Code:    0
#       Started:      Mon, 22 Dec 2025 20:40:53 -0500
#       Finished:     Mon, 22 Dec 2025 20:41:14 -0500
#     Ready:          False
#     Restart Count:  7
#     Liveness:       http-get http://:8080/ delay=10s timeout=2s period=5s #success=1 #failure=3
#   redis:
#     State:          Running
#       Started:      Mon, 22 Dec 2025 20:32:56 -0500
#     Ready:          True
#     Restart Count:  0
#     Liveness:       exec [sh -c redis-cli ping1] delay=10s timeout=2s period=5s #success=1 #failure=3
```

---
