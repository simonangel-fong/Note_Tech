# Kubernetes: Container - Lifecycle Hook

[Back](../../index.md)

- [Kubernetes: Container - Lifecycle Hook](#kubernetes-container---lifecycle-hook)
  - [Lifecycle Hook](#lifecycle-hook)
  - [Post-start Hooks](#post-start-hooks)
    - [`exec hook`:](#exec-hook)
    - [`httpGet hook`](#httpget-hook)
    - [Lab: post-start hooks](#lab-post-start-hooks)
  - [Pre-Stop Hooks](#pre-stop-hooks)
      - [Lab: pre-stop hooks - Graceful shutdown](#lab-pre-stop-hooks---graceful-shutdown)

---

## Lifecycle Hook

- `lifecycle hooks`

  - used to run additional processes every time a container starts and just before it stops.
  - only be applied to `regular containers` and not to `init containers`.
  - not support `tcpSocket` handlers.

- use cases:

  - execute a command **inside** the container
  - send an HTTP GET request to the application in the container.

- vs `init container`

  - `lifecycle hooks`:
    - **container level**, specified per `container`
  - `init container`:
    - specified at the **pod level**

- `Post-start hooks`
  - executed when the container **starts**
  - invoked **immediately** after the container is **created**
- `Pre-stop hooks`
  - executed shortly **before** the container **stops**.
  - when the container **shutdown is initiated**.

---

## Post-start Hooks

- affects

  - Run command **asynchronously** with the **main container process**
    - the `container` **remains** in the `Waiting` state and the phase of the `pod` is `Pending` until the `hook` invocation is **completed**.
  - if the hook can’t be executed or returns a `non-zero exit code`, the entire `container` is **restarted**.
    - pod status: `PostStartHookError`
    - warning event: `FailedPostStartHook`

- log file

  - if fails, **error** logged in the `event`
    - use `kubectl describe` to check **failed event**
  - if successes, output **not logged** anywhere
    - must log to a file instead of the standard or error output
    - `kubectl exec my-pod -- cat logfile.txt`

- **exclusive** 2 types:

  - `exec hook`
  - `httpGet hook`

- **can’t** specify **both** an `exec` and an `httpGet` post-start hook for a container.

---

### `exec hook`:

- `exec hook`:

  - used to execute an **additional process** as the main process starts
  - can’t define multiple commands in a lifecycle hook

    - can use `sh -c "lines of commands"`

- Manifest file

```yaml
# exec
spec:
  containers:
    lifecycle:
      postStart:
        exec:
          command: []
```

---

### `httpGet hook`

- `httpGet hook`:

  - used to **send the request** to a process running in the container **itself**, a **different** container in the pod, or a different **host** altogether.
  - `host` field
    - defaults to the pod IP.
    - Don’t set it to localhost, because the request is sent from the host node, not from within the container.
  - risk:
    - might cause the container to enter an **endless restart loop**. Never configure this type of lifecycle hook to target the same container or any other container in the same pod.
    - Kubernetes doesn’t treat the hook as failed if the HTTP server responds with `status code` such as 404 Not Found.

- benefit:

  - excute additional task without the change of the code or image.

- Manifest file

```yaml
# http get
spec:
  containers:
    lifecycle:
      postStart:
        httpGet:
          host: myservice.example.com
          port: 80
          path: /container-started
```

---

### Lab: post-start hooks

```yaml
# demo-post-start.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-post-start
spec:
  containers:
    - image: nginx
      name: nginx
      lifecycle:
        postStart:
          exec:
            command: ["echo1", "/usr/share/nginx/html"]
```

```sh
kubectl apply -f demo-post-start.yaml
# pod/demo-post-start created

kubectl describe pod/demo-post-start
# Events:
#   Type     Reason               Age                From               Message
#   ----     ------               ----               ----               -------
#   Normal   Scheduled            42s                default-scheduler  Successfully assigned default/demo-post-start to docker-desktop
#   Normal   Pulled               41s                kubelet            Successfully pulled image "nginx" in 1.038s (1.038s including waiting). Image size: 59795293 bytes.
#   Normal   Pulled               37s                kubelet            Successfully pulled image "nginx" in 990ms (990ms including waiting). Image size: 59795293 bytes.
#   Normal   Pulling              21s (x3 over 42s)  kubelet            Pulling image "nginx"
#   Normal   Created              20s (x3 over 39s)  kubelet            Created container: nginx
#   Normal   Started              20s (x3 over 39s)  kubelet            Started container nginx
#   Warning  FailedPostStartHook  20s (x3 over 39s)  kubelet            PostStartHook failed
#   Normal   Killing              20s (x3 over 39s)  kubelet            FailedPostStartHook
#   Normal   Pulled               20s                kubelet            Successfully pulled image "nginx" in 770ms (770ms including waiting). Image size: 59795293 bytes.
#   Warning  BackOff              7s (x4 over 36s)   kubelet            Back-off restarting failed container nginx in pod demo-post-start_default(2527e295-4db9-40b8-908e-fbda4f4120ed)
```

---

## Pre-Stop Hooks

- `pre-stop hook`
  - executed immediately before a container is terminated.
    - `TERM` signal is not sent **until** the pre-stop hook **completes**
  - used to initiate a `graceful shutdown`
- When container **termination** is initiated, the `liveness` and other `probes` are **no longer invoked**.

- the `container` is **terminated** regardless of the result of the `pre-stop hook`

  - a failure to execute the command or a non-zero exit code **does not prevent** the container from being **terminated**.

- Log file:
  - only log in the `FailedPreStopHook` event

---

- Manifest file

```yaml
# exec
spec:
  containers:
    lifecycle:
      preStop:
        exec:
          command: []

# http get
spec:
  containers:
    lifecycle:
      preStop:
        httpGet:
          host: myservice.example.com
          port: 80
          path: /container-started
```

---

#### Lab: pre-stop hooks - Graceful shutdown

```yaml
# demo-pre-stop.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-pre-stop
spec:
  containers:
    - image: nginx
      name: nginx
      lifecycle:
        preStop:
          exec:
            command: ["nginx", "-s", "quit"]
```

---
