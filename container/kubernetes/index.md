# Kubernetes

[Back](../../index.md)

---

## Container

- [Container](./container/container/container.md)

  - [Back-off Mechanism & Restart Policy](./container/backoff_restart/backoff_restart.md)
  - [`Liveness Probe`](./container/liveness_probe/liveness_probe.md)
  - [`Startup Probe`](./container/startup_probe/startup_probe.md)
  - [`Lifecycle Hook`](./container/lifecycle_hook/lifecycle_hook.md)
  - [Command & Arg & ENV](./container/cmd_arg_env/cmd_arg_env.md)

- Multiple Containers:

  - [`Co-located Containers`](./container/colocated/colocated.md)
  - [`Init Containers`](./container/init/init.md)
  - [`Sidecar Containers`](./container/sidecar/sidecar.md)

- Storage:
  - [Docker Storage](./storage/docker_storage/docker_storage.md)
  - [`Pod Volume`](./storage/volume/volume.md)
  - [Common Volume Types](./storage/volume_type/volume_type.md)
    - [`emptyDir`](./storage/empty_dir/empty_dir.md)
    - [`hostPath`](./storage/host_path/host_path.md)
    - [`Persistent Volume` & `Persistent Volume Claim`](./storage/pv_pvc/pv_pvc.md)
    - [`Node Local Persistent Volume`](./storage/node_local_pv/node_local_pv.md)
    - [Dynamic Volume Provisioning & `StorageClass`](./storage/dynamic_pv_storageclass/dynamic_pv_storageclass.md)
- Injected Data
  - [`ConfigMap`](./storage/configmap/configmap.md)
    - [Use `ConfigMap` as Environment Variable](./storage/configmap_env/configmap_env.md)
    - [Use `ConfigMap` as Volume](./storage/configmap_volume/configmap_volume.md)
  - [`Secret`](./storage/secret/secret.md)
    - [Use `Secret` as Environment variables](./storage/secret_env/secret_env.md)
    - [Use `Secret` as Volume](./storage/secret_volume/secret_volume.md)
  - [`Downward API`](./storage/downward_api/downward_api.md)
    - [Use `Downward API` as Environment Variables](./storage/downward_api_env/downward_api_env.md)
    - [Use `Downward API` as Volume](./storage/downward_api_volume/downward_api_volume.md)
  - [`Projected Volumes`](./storage/projected_volume/projected_volume.md)

---

## Workload

- [`Pod`](./pod/pod/pod.md)
  - [Lifecycle](./pod/lifecycle/lifecycle.md)
- [`ReplicaSet`](./replicaset/replicaset.md)
- [`Deployment`](./deployment/deployment.md)
  - [Deployment Rollout & Rollback](./deployment/rollout_rollback.md)
  - [Common Deployment Strategies](./deployment/strategy.md)
- [`StatefulSets`](./statefulset/statefulset.md)
  - [StatefulSets Rollout & Rollback](./statefulset/rollout_rollback.md)
- [`DaemonSets`](./daemonset/daemonset.md)
  - [DaemonSets Rollout & Rollback](./daemonset/rollout_rollback.md)
- [`Job`](./job/job.md)
- [`CronJob`](./cronjob/cronjob.md)

---

- [Operator](./operator/operator.md)

---

- [Fundamental](./fundamental/fundamental/fundamental.md)

  - [API Object](./fundamental/api_object/api_object.md)
  - [YAML File](./fundamental/yaml/yaml.md)
  - [`kubectl`](./fundamental/kubectl/kubectl.md)
  - [`Minikube`](./fundamental/minikube/minikube.md)

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

- [Cluster](./cluster/cluster.md)
  - [Namespace](./management/namespace/namespace.md)
  - [Label and Selector](./management/label_selector/label_selector.md)
  - [Annotation](./object/annotation/annotation.md)

---

- [Static Pod](./app/static_pod/static_pod.md)
- [Scaling](./pod/scaling/scaling.md)
  - [Horizontal Scaling](./pod/scaling_horizontal/scaling_horizontal.md)
  - [Vertical Scaling](./pod/scaling_vertical/scaling_vertical.md)
- [!PriorityClass](./app/pod_priorityclass/pod_priorityclass.md)
- [Resources Limit](./pod/pod_resource_limit/pod_resource_limit.md)

- [Troubleshooting](./debuging/debuging.md)

---

- [Admission Controller](./adm_ctl/adm_ctl.md)

---

- [Release](./release/release.md)
- [Upgrade](./release/release.md)
- [Backup](./backup/backup.md)
- [Install Master](./install_master/install_master.md)
- [Install Worker](./install_worker/install_worker.md)

- [Security]

  - [AUthentication](./authentication/authentication.md)
  - [KubeConfig](./kube_config/kube_config.md)
  - [Authorization](./authorization/authorization.md)
  - [ClusterRole](./cluster_role/cluster_role.md)
  - [ServiceAccount](./svc_account/svc_account.md)
  - [Secure Image](./image/image.md)
  - [Security Context](./security_context/security_context.md)
  - [Network Policy](./network_policy/network_policy.md)
  - [Custom Resource Definition(CRD)](./crd/crd.md)

- Management

  - [Monitor & Logging](./management/monitoring/monitoring.md)

---

- [Node](./node/node/node.md)
  - [Scheduler](./node/scheduler/scheduler.md)
    - [Manual Scheduler](./node/scheduler_manual/scheduler_manual.md)
  - [Taints and Tolerations](./node/taint_toleration/taint_toleration.md)
  - [Node Selector](./node/node_selector/node_selector.md)
  - [Node Affinity](./node/node_affinity/node_affinity.md)
  - [Node Cordon](./node/node_cordon/node_cordon.md)

---

- [Networking](./networking/networking.md)

  - [Service](./networking/service/service.md)

    - [ClusterIP](./networking/svr_clusterip/svr_clusterip.md)
    - [NodePort](./networking/svr_nodeport/svr_nodeport.md)
    - [LoadBalancer](./networking/svr_loadbalancer/svr_loadbalancer.md)

  - [Endpoint](./networking/endpoint/endpoint.md)
  - [Pod Networking](./networking/pod/pod.md)
  - [Service Networking](./networking/service/service.md)
  - [Cluster DNS](./networking/dns/dns.md)
  - [Ingress](./networking/ingress/ingress.md)
  - [Gateway API](./networking/gw_api/gw_api.md)

---

- [HELM](./helm/helm.md)
- [Kustomize](./kustomize/kustomize.md)

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

https://docs.linuxfoundation.org/tc-docs/certification/tips-cka-and-ckad
