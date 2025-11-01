# Kubernetes

[Back](../../index.md)

---

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

- Management

  - [Namespace](./management/namespace/namespace.md)
  - [Label and Selector](./management/label_selector/label_selector.md)
  - [Monitor & Logging](./management/monitoring/monitoring.md)

---

- [Scheduler](./scheduler/scheduler/scheduler.md)

  - [Manual Scheduler](./scheduler/man_scheduler/man_scheduler.md)
  - [Taints and Tolerations](./scheduler/taint_toleration/taint_toleration.md)
  - [Node Selector](./scheduler/node_sel/node_sel.md)
  - [Node Affinity](./scheduler/node_aff/node_aff.md)
  - [Resources Limit](./scheduler/res_limit/res_limit.md)
  - [DaemonSets](./scheduler/daemon_set/daemon_set.md)

---

- Networking
  - [Service](./networking/service/service.md)
    - [NodePort](./networking/svr_nodeport/svr_nodeport.md)
    - [ClusterIP](./networking/svr_clusterip/svr_clusterip.md)
    - [LoadBalancer](./networking/svr_loadbalancer/svr_loadbalancer.md)

---

- [Node](./node/node/node.md)

---

- [Pod](./pod/pod/pod.md)

  - [Container Management](./pod/container/container.md)
    - [ConfigMap](./pod/container_configmap/container_configmap.md)
    - [Secret](./pod/container_secret/container_secret.md)
    - [Multi-containers](./pod/container_multi/container_multi.md)
  - [Static Pod](./pod/static_pod/static_pod.md)
  - [ReplicaSet](./pod/replicaset/replicaset.md)
  - [Deployment](./pod/deploy/deploy.md)
    - [Rolling update and roll back](./pod/deploy_rolling/deploy_rolling.md)
  - [Scaling](./pod/scaling/scaling.md)
    - [Horizontal Scaling](./pod/scaling_horizontal/scaling_horizontal.md)
    - [Vertical Scaling](./pod/scaling_vertical/scaling_vertical.md)
  - [!PriorityClass](./pod/pod_priorityclass/pod_priorityclass.md)

---

- Security

  - [Admission Controller](./security/admission_controller/admission_controller.md)

---

- Installation

  - [RHEL9: `minikube` installation](./install/minikube_rhel9/minikube_rhel9.md)
  - [Ubuntu: `minikube` installation](./install/minikube_ubuntu/minikube_ubuntu.md)
  - [Windows: `Docker Desktop` enable `Kubernetes`](./install/kube_docker_desktop_win/kube_docker_desktop_win.md)

---

todo list:

- Cluster
  - Encrypting Confidential Data at Rest
    - ref: https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/
- Rel:
  - https://kubernetes.io/docs/concepts/overview/components/
- https://scriptwang.github.io/blog/#/blog/2021-06-14_K8S%E5%8E%9F%E7%90%86%E6%9E%B6%E6%9E%84%E4%B8%8E%E5%AE%9E%E6%88%98%EF%BC%88%E5%9F%BA%E7%A1%80%E7%AF%87%EF%BC%89
