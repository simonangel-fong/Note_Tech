# Kubernetes - Pod

[Back](../../index.md)

- [Kubernetes - Pod](#kubernetes---pod)
  - [Pod](#pod)
    - [Types of Pod](#types-of-pod)
      - [Single Container Pod](#single-container-pod)
      - [Multi Container Pod](#multi-container-pod)
  - [Common Commands](#common-commands)
  - [Lab: Create a pod using CLI](#lab-create-a-pod-using-cli)
  - [Lab: Pod Creation using Yaml File](#lab-pod-creation-using-yaml-file)

---

## Pod

- `pod`
  - a collection of **containers** and its **storage** inside a **node** of a Kubernetes cluster.
- It is possible to create a pod with **multiple containers** inside it.
  - For example, keeping a database container and data container in the same pod.

---

### Types of Pod

- There are two types of Pods
  - Single container pod
  - Multi container pod

---

#### Single Container Pod

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
kubectl create f tomcat.yml
```

---

#### Multi Container Pod

- `Multi container pods` are created using **yaml mail** with the definition of the containers.

```sh
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

## Common Commands

| **Command**                               | **Description**                                             |
| ----------------------------------------- | ----------------------------------------------------------- |
| `kubectl get pods`                        | List all pods in the current namespace                      |
| `kubectl get pods -A`                     | List pods across **all namespaces**                         |
| `kubectl run pod_name --image=image_name` | Create a pod using a specified image (for testing)          |
| `kubectl apply -f yaml_file`              | Create or update a pod from YAML manifest                   |
| `kubectl describe pod pod_name`           | Show detailed information about a specific pod              |
| `kubectl get pod pod_name -o yaml`        | View full YAML configuration of a pod                       |
| `kubectl logs pod_name`                   | View logs from a pod's main container                       |
| `kubectl logs pod_name -c container_name` | View logs for a specific container in a multi-container pod |
| `kubectl exec -it pod_name -- commands`   | Execute a command inside the pod (e.g., get a shell)        |
| `kubectl delete pod pod_name`             | Delete a specific pod                                       |

---

## Lab: Create a pod using CLI

```sh
# create
kubectl run nginx --image=nginx
# pod/nginx created

# confirm
kubectl get pods
# NAME    READY   STATUS    RESTARTS   AGE
# nginx   1/1     Running   0          45s

kubectl get pods -o wide
# NAME    READY   STATUS    RESTARTS   AGE     IP            NODE       NOMINATED NODE   READINESS GATES
# nginx   1/1     Running   0          4m13s   10.244.0.11   minikube   <none>

# show detail information
kubectl describe pod nginx
# Name:             nginx
# Namespace:        default
# Priority:         0
# Service Account:  default
# Node:             minikube/192.168.49.2
# Start Time:       Fri, 02 May 2025 13:13:50 -0400
# Labels:           run=nginx
# IP:               10.244.0.11
# ...
```

---

## Lab: Pod Creation using Yaml File

- Define `pod-def.yaml`

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  # user custom label
  labels:
    app: myapp
    tier: front-end
spec:
  # a list
  containers:
    - name: nginx-container
      image: nginx
```

- Create pod

```sh
kubectl create -f pod-def.yaml
# pod/myapp-pod created

# confirm
kubectl get pods
# NAME        READY   STATUS    RESTARTS   AGE
# myapp-pod   1/1     Running   0          12s

# view detailed info
kubectl describe pod myapp-pod
# Name:             myapp-pod
# Namespace:        default
# Priority:         0
# Service Account:  default
# Node:             minikube/192.168.49.2
# Start Time:       Fri, 02 May 2025 14:29:58 -0400
# Labels:           app=myapp
#                   type=front-end
# Annotations:      <none>
# Status:           Running
# IP:               10.244.0.12
# ...

# cleanup
kubectl delete pod myapp-pod
# pod "myapp-pod" deleted

kubectl get pods
# No resources found in default namespace.
```
