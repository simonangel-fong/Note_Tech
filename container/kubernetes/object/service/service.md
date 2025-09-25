# Kubernetes - Services

[Back](../index.md)

- [Kubernetes - Services](#kubernetes---services)
  - [ClusterIP](#clusterip)
  - [Load Balancer](#load-balancer)
  - [Common Commands](#common-commands)

---



- Service Types

  - `NodePort`
  - `ClusterIP`
  - `Load Balancer`

---


---


## ClusterIP

- `ClusterIP`

  - default type of service
  - exposes the `service` within the defined Kubernetes `cluster`.
  - enable communication between `services`
  - a type of Service that provides an **internal, cluster-wide IP address** to enable **communication** between different **components** (typically Pods) within the **same** Kubernetes `cluster`.
  - forward the requests to one of the pods under the service **randomly**

- The service canbe aacessed by other pods using the cluster IP/service name

---

- Definition

```yaml
apiVersion: v1
kind: Service
metadata:
  name: back-end
spec:
  type: ClusterIP
  ports:
    - targetPort: 80 # the port exposed on backend
      port: 80 # the port exposed on service
  selector: # link the service to the pods
    app: myapp
    type: back-end
```

- Create

```sh
kubectl create -f service-cip-def.yaml

kubectl get svc
```

---

## Load Balancer

- `LoadBalancer`
  - a type of Service that provides **external access** to applications running in a Kubernetes cluster.
  - Only works with supported cloud platforms.

---

- Definition

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myservice
spec:
  type: LoadBalancer
  ports:
    - targetPort: 80
      port: 80
      nodePort: 30008
```

---

## Common Commands

- how many services exist on system
  - `kubectl get svc`
- the type of default `kubernetes` service
  - ClusterIP
- what targetPort the default `kubernetes` is configured
  - `kubectl describe svc kubernetes`
  - 6443/TCP
- how many labels are configured on the default `kubernetes` service
  - `kubectl describe svc kubernetes`, labels
- how many endpoint are attached on the default `kubernetes` service
  - `kubectl describe svc kubernetes`, Endpoints
