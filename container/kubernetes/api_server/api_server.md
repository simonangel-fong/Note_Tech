# Kubernetes - API Server

[Back](../index.md)

- [Kubernetes - API Server](#kubernetes---api-server)
  - [API Server](#api-server)
  - [common command](#common-command)

---

## API Server

- responsible for:

  - authenticate a user
  - validate a request
  - retrieve and update data from `ETCD`
    - get the data from the `etcd server`
    - update the data from the `etcd server`
  - scheduler
    - scheduler keep monitering services and communicate with `API server`
    - if necessary, `api server` update the `etcd cluster`
    - `api server` then pass the information to the appropriate `worker node`.
  - kubelet
    - `api server` communicate with kubelet on `workder node` for the updated status.

- Ways to invoke api
  - `kubectl` command
  - send post request `curl -X POST /api/v1/nampespaces/default/pods ...`

---

## common command

| CMD | DESC |
| --- | ---- |
|     |      |

```sh
kubectl get pods -n kube-system
# NAME                                     READY   STATUS    RESTARTS        AGE
# ...
# kube-apiserver-docker-desktop            1/1     Running   123 (29m ago)   147d
# ...
```
