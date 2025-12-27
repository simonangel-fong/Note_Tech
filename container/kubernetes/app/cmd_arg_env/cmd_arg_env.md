# Kubernetes - Pod: Container - Command, Arg, and Env

[Back](../../index.md)

- [Kubernetes - Pod: Container - Command, Arg, and Env](#kubernetes---pod-container---command-arg-and-env)
  - [Command and Arg](#command-and-arg)
    - [Lab: Container `command`](#lab-container-command)
    - [Lab: Container `command` \& `args`](#lab-container-command--args)
    - [Lab: Container `command` \& `args`: Multi-line arguments](#lab-container-command--args-multi-line-arguments)
    - [Lab: Container `command` \& `args`: Shell script](#lab-container-command--args-shell-script)
  - [Environment Variables](#environment-variables)
      - [Lab: List all env](#lab-list-all-env)
      - [Lab: Container `command`, `args`, `env`](#lab-container-command-args-env)
    - [`container.env`: Define specific Variables](#containerenv-define-specific-variables)
      - [Lab: Import a key from ConfigMap](#lab-import-a-key-from-configmap)
      - [Lab: Import key from a non-existing ConfigMap - `optional`](#lab-import-key-from-a-non-existing-configmap---optional)
    - [`envFrom`: Builk Import](#envfrom-builk-import)
      - [Lab: Builk Import from ConfigMap](#lab-builk-import-from-configmap)
      - [Lab: Builk Import from ConfigMap - `optional`](#lab-builk-import-from-configmap---optional)

---

## Command and Arg

- the equivalent **pod manifest field** for each of **Dockerfile directives**:

| Dockerfile   | Pod manifest | Description                                    |
| ------------ | ------------ | ---------------------------------------------- |
| `ENTRYPOINT` | `command`    | the executable file that runs in the container |
| `CMD`        | `args`       | Additional arguments                           |

---

### Lab: Container `command`

```yaml
# demo-command.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-command
spec:
  containers:
    - name: nginx
      image: nginx
    - name: busybox
      image: busybox
      command:
        - echo
        - "demo command"
```

- Create pod

```sh
kubectl apply -f demo-command.yaml
# pod/demo-command created

kubectl logs demo-command -c busybox
# demo command
```

---

### Lab: Container `command` & `args`

```yaml
# demo-command-arg.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-command-arg
spec:
  containers:
    - name: nginx
      image: nginx
    - name: busybox
      image: busybox
      command:
        - echo
      args:
        - "demo command & arg"
```

- Create pod

```sh
kubectl apply -f demo-command-arg.yaml
# pod/demo-command-arg created

kubectl logs demo-command-arg -c busybox
# demo command & arg
```

---

### Lab: Container `command` & `args`: Multi-line arguments

```yaml
# demo-command-arg-multi-line.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-command-arg-multi-line
spec:
  containers:
    - name: nginx
      image: nginx
    - name: busybox
      image: busybox
      command:
        - echo
      args:
        - |
          demo
          this is a multi-line argument
```

- Create pod

```sh
kubectl apply -f demo-command-arg-multi-line.yaml
# pod/demo-command-arg-multi-line created

# confirm
kubectl logs demo-command-arg-multi-line -c busybox
# demo
# this is a multi-line argument
```

---

### Lab: Container `command` & `args`: Shell script

```yaml
# demo-command-arg-shell-script.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-command-arg-shell-script
spec:
  containers:
    - name: busybox
      image: busybox
      command:
        - sh
      args:
        - "-c"
        - |
          echo "Demo command & args - shell script";
          while true; do
            echo $(date);
            sleep 1;
          done
```

- Create pod

```sh
kubectl apply -f demo-command-arg-shell-script.yaml
# pod/demo-command-arg-shell-script created

kubectl logs demo-command-arg-shell-script -f
# Demo command & args - shell script
# Fri Dec 26 17:46:40 UTC 2025
# Fri Dec 26 17:46:43 UTC 2025
# Fri Dec 26 17:46:44 UTC 2025
# Fri Dec 26 17:46:45 UTC 2025
# Fri Dec 26 17:46:46 UTC 2025
# Fri Dec 26 17:46:47 UTC 2025
# Fri Dec 26 17:46:48 UTC 2025
```

---

## Environment Variables

- the way to inject data as envrionment variables
  - specific keys:
    - `spec.containers.env.valueFrom` field
      - from `configMap` oject: `configMapKeyRef`
      - from `secret` oject: `secretKeyRef`
      - from pod’s general metadata: `fieldRef`
      - from resource constraints: `resourceFieldRef`

---

#### Lab: List all env

```sh
kubectl run demo-env --image=nginx
# pod/demo-env created

kubectl exec demo-env -- env
# PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
# HOSTNAME=demo-env
# KUBERNETES_SERVICE_PORT_HTTPS=443
# KUBERNETES_PORT=tcp://10.96.0.1:443
# KUBERNETES_PORT_443_TCP=tcp://10.96.0.1:443
# KUBERNETES_PORT_443_TCP_PROTO=tcp
# KUBERNETES_PORT_443_TCP_PORT=443
# KUBERNETES_PORT_443_TCP_ADDR=10.96.0.1
# KUBERNETES_SERVICE_HOST=10.96.0.1
# KUBERNETES_SERVICE_PORT=443
# NGINX_VERSION=1.29.4
# NJS_VERSION=0.9.4
# NJS_RELEASE=1~trixie
# PKG_RELEASE=1~trixie
# DYNPKG_RELEASE=1~trixie
# HOME=/root
```

---

#### Lab: Container `command`, `args`, `env`

```yaml
# demo-cmd-arg-env.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-cmd-arg-env
spec:
  containers:
    - name: busybox
      image: busybox
      env:
        - name: MY_MSG
          value: demo command, args, and env
      command:
        - sh
      args:
        - "-c"
        - |
          echo "this is the massage: $MY_MSG"
          echo "this is contianer env: $$HOSTNAME"   

          REF_VAR="this is the massage: $MY_MSG;this is contianer env: $$HOSTNAM"    # $$ENV_VAR
          echo $REF_VAR

          sleep 600
```

```sh
kubectl apply -f demo-cmd-arg-env.yaml
# pod/demo-cmd-arg-env created

kubectl logs demo-cmd-arg-env
```

---

### `container.env`: Define specific Variables

- `env` field

  - used to write **key-value pairs** with **hardcoded values**

- `env.value` field:
  - a hardcoding value
- `env.valueFrom` field:

  - specify the source of a value
  - `configMapKeyRef` field: import a key from a configMap oject
  - `optional` field: container can be **executed** even if the **config map or key** is **missing**.

---

- a pod manifest env can reference to another pod manifest env
  - pod env: `$(VAR_NAME)`
- a pod manifest env **can’t** reference environment variables defined in the container image.

- When you want a variable to contain the literal string `$(VAR_NAME)` and don’t want Kubernetes to resolve it, use a double dollar sign as in `$$(VAR_NAME)`.

---

#### Lab: Import a key from ConfigMap

```yaml
# demo_env_configmap.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-env-configmap
spec:
  containers:
    - name: busybox
      image: busybox
      command:
        - sh
      args:
        - "-c"
        - |
          echo $VAR_MSG; sleep 500
      env:
        - name: VAR_MSG
          valueFrom:
            configMapKeyRef:
              name: my-configmap
              key: MESSAGE
```

- Create

```sh
kubectl create cm my-configmap --from-literal MESSAGE="my message"
# configmap/my-configmap create

kubectl apply -f demo_env_configmap.yaml
# pod/demo-env-configmap created

# confirm
kubectl logs demo-env-configmap
# my message
```

---

#### Lab: Import key from a non-existing ConfigMap - `optional`

```yaml
# demo-env-nonexist-configmap.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-env-nonexist-configmap
spec:
  containers:
    - name: busybox
      image: busybox
      env:
        - name: VAR_A
          valueFrom:
            configMapKeyRef:
              name: no-configmap
              key: VAR_A
      command:
        - sh
      args:
        - "-c"
        - |
          echo "Demo configMapKeyRef=non-existed"; 
          echo "env var VAR_A: $VAR_A"; 
          echo "env var VAR_B: $VAR_B"; 
          sleep 500
```

- Create

```sh
# confirm no exist
kubectl get cm

kubectl apply -f demo-env-nonexist-configmap.yaml
# pod/demo-env-nonexist-configmap created

# confirm error
kubectl get pod
# NAME                          READY   STATUS                       RESTARTS   AGE
# demo-env-nonexist-configmap   0/1     CreateContainerConfigError   0          30s

kubectl describe pod demo-env-nonexist-configmap
# Events:
#   Type     Reason     Age               From               Message
#   ----     ------     ----              ----               -------
#   Normal   Scheduled  48s               default-scheduler  Successfully assigned default/demo-env-nonexist-configmap to docker-desktop
#   Normal   Pulled     47s               kubelet            Successfully pulled image "busybox" in 1.142s (1.142s including waiting). Image size: 2224358 bytes.
#   Normal   Pulled     45s               kubelet            Successfully pulled image "busybox" in 808ms (808ms including waiting). Image size: 2224358 bytes.
#   Normal   Pulled     32s               kubelet            Successfully pulled image "busybox" in 803ms (803ms including waiting). Image size: 2224358 bytes.
#   Normal   Pulled     17s               kubelet            Successfully pulled image "busybox" in 629ms (629ms including waiting). Image size: 2224358 bytes.
#   Normal   Pulling    5s (x5 over 48s)  kubelet            Pulling image "busybox"
#   Warning  Failed     4s (x5 over 47s)  kubelet            Error: configmap "bulk-configmap" not found

```

```yaml
# demo-env-nonexist-configmap-optional.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-env-nonexist-configmap-optional
spec:
  containers:
    - name: busybox
      image: busybox
      env:
        - name: VAR_A
          valueFrom:
            configMapKeyRef:
              name: no-configmap
              key: VAR_A
              optional: true
      command:
        - sh
      args:
        - "-c"
        - |
          echo "Demo configMapKeyRef.optional"; 
          echo "env var VAR_A: $VAR_A"; 
          echo "env var VAR_B: $VAR_B"; 
          sleep 500
```

```sh
kubectl apply -f demo-env-nonexist-configmap-optional.yaml
# pod/demo-env-nonexist-configmap-optional created

kubectl get pod
# NAME                                   READY   STATUS    RESTARTS   AGE
# demo-env-nonexist-configmap-optional   1/1     Running   0          31s

kubectl logs demo-env-nonexist-configmap-optional
# Demo configMapKeyRef.optional
# env var VAR_A:
# env var VAR_B:
```

---

### `envFrom`: Builk Import

- `envFrom`

  - populate environment variables from the contents of `ConfigMaps`, `Secrets`, and runtime **Pod properties**.

- `envFrom.configMapRef` field:

  - bulk import from a configmap

- Can work with `env`

  - `envFrom`: bulk import
  - `env`: specify particular entries
  - env var in the `env` field **takes precedence over** those the `envFrom` field.

- Can import multiple configMap objects
  - If **two** `config maps` contain the **same key**, the **last** one takes **precedence**

---

#### Lab: Builk Import from ConfigMap

```yaml
# demo_env_bulk_configmap.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-env-bulk-configmap
spec:
  containers:
    - name: busybox
      image: busybox
      envFrom:
        - configMapRef:
            name: bulk-configmap
      command:
        - sh
      args:
        - "-c"
        - |
          echo $VAR_A; 
          echo $VAR_B; 
          sleep 500
```

- Create

```sh
kubectl create cm bulk-configmap --from-literal VAR_A="value a" --from-literal VAR_B="value b"
# configmap/bulk-configmap created

kubectl get cm bulk-configmap
# NAME             DATA   AGE
# bulk-configmap   2      17s

kubectl describe cm bulk-configmap
# Name:         bulk-configmap
# Namespace:    default
# Labels:       <none>
# Annotations:  <none>

# Data
# ====
# VAR_A:
# ----
# value a

# VAR_B:
# ----
# value b


# BinaryData
# ====

# Events:  <none>

kubectl apply -f demo_env_bulk_configmap.yaml
# pod/demo-env-bulk-configmap created

# confirm
kubectl logs demo-env-bulk-configmap
# value a
# value b
```

---

#### Lab: Builk Import from ConfigMap - `optional`

- no optional

```yaml
# demo-envfrom-nonexist-configmap.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-envfrom-nonexist-configmap
spec:
  containers:
    - name: busybox
      image: busybox
      envFrom:
        - configMapRef:
            name: no-configmap
      command:
        - sh
      args:
        - "-c"
        - |
          echo "Demo envFrom.configMapRef.optional==false"; 
          echo "env var VAR_A: $VAR_A"; 
          echo "env var VAR_B: $VAR_B"; 
          sleep 500
```

```sh
kubectl apply -f demo-envfrom-nonexist-configmap.yaml
# pod/demo-envfrom-nonexist-configmap created

kubectl get pod
# NAME                              READY   STATUS                       RESTARTS   AGE
# demo-envfrom-nonexist-configmap   0/1     CreateContainerConfigError   0          90s

kubectl describe pod demo-envfrom-nonexist-configmap
# Events:
#   Type     Reason     Age                  From               Message
#   ----     ------     ----                 ----               -------
#   ...
#   Warning  Failed     2s (x11 over 2m18s)  kubelet            Error: configmap "no-configmap" not found
```

---

- with optional

```yaml
# demo-envfrom-nonexist-configmap-optional.yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-envfrom-nonexist-configmap-optional
spec:
  containers:
    - name: busybox
      image: busybox
      envFrom:
        - configMapRef:
            name: no-configmap
            optional: true # optional
      command:
        - sh
      args:
        - "-c"
        - |
          echo "Demo envFrom.configMapRef.optional==false"; 
          echo "env var VAR_A: $VAR_A"; 
          echo "env var VAR_B: $VAR_B"; 
          sleep 500
```

```sh
kubectl apply -f demo-envfrom-nonexist-configmap-optional.yaml
# pod/demo-envfrom-nonexist-configmap-optional created

kubectl get pod
# NAME                                       READY   STATUS    RESTARTS   AGE
# demo-envfrom-nonexist-configmap-optional   1/1     Running   0          34s

kubectl logs demo-envfrom-nonexist-configmap-optional
# Demo envFrom.configMapRef.optional==true
# env var VAR_A:
# env var VAR_B:
```
