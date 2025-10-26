# Kubernetes

[Back](../../index.md)

---

- Rel:
  - https://kubernetes.io/docs/concepts/overview/components/
- https://scriptwang.github.io/blog/#/blog/2021-06-14_K8S%E5%8E%9F%E7%90%86%E6%9E%B6%E6%9E%84%E4%B8%8E%E5%AE%9E%E6%88%98%EF%BC%88%E5%9F%BA%E7%A1%80%E7%AF%87%EF%BC%89

## Kubernetes

- [Fundamental](./fundamental/fundamental/fundamental.md)

  - [YAML File](./fundamental/yaml/yaml.md)
  - [`kubectl`](./fundamental/kubectl/kubectl.md)

- [Architecture](./architecture/architecture/architecture.md)
  - Master Node / Control plane
    - [`etcd`](./architecture/etcd/etcd.md)
    - [API Server](./architecture/api_server/api_server.md)
    - [Controller Manager](./architecture/controller_manager/controller_manager.md)
    - [Scheduler](./architecture/scheduler/scheduler.md)
  - Worker Node
    - [`kubelet`](./architecture/kubelet/kubelet.md)
    - [`kube-proxy`](./architecture/kube_proxy/kube_proxy.md)

---

- Basic Objects

  - [Node](./object/node/node.md)
  - [Pod](./object/pod/pod.md)
  - [Label and Selector](./object/lbl_slt/lbl_slt.md)
  - [ReplicaSet](./object/replica/replica.md)
  - [Deployment](./object/deployment/deployment.md)
  - [Service](./object/service/service.md)
  - [Namespace](./object/namespace/namespace.md)

- [Service](./service/service/service.md)

  - [NodePort](./service/nodeport/nodeport.md)
  - [ClusterIP](./service/clusterip/clusterip.md)
  - [LoadBalancer](./service/loadbalancer/loadbalancer.md)

- [Scheduler](./scheduler/scheduler/scheduler.md)

  - [Manual Scheduler](./scheduler/man_scheduler/man_scheduler.md)
  - [Taints and Tolerations](./scheduler/taint_toleration/taint_toleration.md)
  - [Node Selector](./scheduler/node_sel/node_sel.md)
  - [Node Affinity](./scheduler/node_aff/node_aff.md)
  - [Resources Limit](./scheduler/res_limit/res_limit.md)
  - [DaemonSets](./scheduler/daemon_set/daemon_set.md)

- Cluster-object
  - [PriorityClass](./priority_class/priority_class.md)

---

- [Monitor & Logging](./monitoring_logging/monitoring_logging.md)

---

- Node
  - [Static Pod](./node/static_pod/static_pod.md)

---

- Security

  - [Admission Controller](./security/admission_controller/admission_controller.md)

- [Networking](./networking/networking.md)
- [Microservices](./microservices/microservices.md)

- Setup Environment

  - [RHEL9: `minikube` installation](./install/minikube_rhel9/minikube_rhel9.md)
  - [Ubuntu: `minikube` installation](./install/minikube_ubuntu/minikube_ubuntu.md)
  - [Windows: `Docker Desktop` enable `Kubernetes`](./install/kube_docker_desktop_win/kube_docker_desktop_win.md)

---
