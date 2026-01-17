# Kubernetes

[Back](../../index.md)

- [Kubernetes](#kubernetes)
  - [Cluster](#cluster)
  - [Node](#node)
  - [Master Node / Control plane](#master-node--control-plane)
  - [Worker Node](#worker-node)
  - [Container](#container)
  - [Workload](#workload)
  - [Security](#security)
  - [Configuration](#configuration)
  - [Installation](#installation)
  - [CKA](#cka)

---

## Cluster

- [Fundamental](./cluster/fundamental/fundamental.md)
  - [Architecture](./cluster/architecture/architecture.md)
  - [YAML File](./cluster/yaml/yaml.md)
  - [`kubectl`](./cluster/kubectl/kubectl.md)
    - [KubeConfig](./cluster/kube_config/kube_config.md)

- [Upgrade](./cluster/upgrade/upgrade.md)
- [Backup](./cluster/backup/backup.md)
- [Logging](./cluster/logging/logging.md)

- [API Object](./api_object/api_object/api_object.md)
  - [Namespace](./api_object/namespace/namespace.md)
  - [Label and Selector](./api_object/label_selector/label_selector.md)
  - [Annotation](./api_object/annotation/annotation.md)
  - [Custom Resource Definition(CRD)](./api_object/crd/crd.md)

---

## Node

- [`Node`](./node/node/node.md)
- [`Taints` and `Tolerations`](./node/taint_toleration/taint_toleration.md)
- [Cordon & Drain](./node/cordon/cordon.md)

---

## Master Node / Control plane

- [API Server](./node_master/api_server/api_server.md)
- [`etcd`](./node_master/etcd/etcd.md)
- [Controller Manager](./node_master/controller_manager/controller_manager.md)
- [Scheduler](./node_master/scheduler/scheduler.md)
  - [Manual Scheduler](./node_master/scheduler_manual/scheduler_manual.md)
- [Install Master Node](./node_master/install_master/install_master.md)

---

## Worker Node

- [`kubelet`](./node_worker/kubelet/kubelet.md)
  - [`Static Pod`](./node_worker/kubelet/static_pod.md)
- [`kube-proxy`](./node_worker/kube_proxy/kube_proxy.md)

---

## Container

- [Container](./container/container/container.md)
  - [Image](./container/image/image.md)
  - [Back-off Mechanism & Restart Policy](./container/backoff_restart/backoff_restart.md)
  - [`Liveness Probe`](./container/liveness_probe/liveness_probe.md)
  - [`Startup Probe`](./container/startup_probe/startup_probe.md)
  - [`Readiness Probes`](./container/readiness_probe/readiness_probe.md)
  - [`Lifecycle Hook`](./container/lifecycle_hook/lifecycle_hook.md)
  - [Command & Arg & ENV](./container/cmd_arg_env/cmd_arg_env.md)
  - [Resources Request, Limit, Quota](./container/resource/resource.md)

- **Multiple Containers**:
  - [`Co-located Containers`](./container/colocated/colocated.md)
  - [`Init Containers`](./container/init/init.md)
  - [`Sidecar Containers`](./container/sidecar/sidecar.md)

- **Storage**:
  - [Docker Storage](./storage/docker_storage/docker_storage.md)
  - [CSI (Container Storage Interface)](./storage/csi/csi.md)
  - [`Pod Volume`](./storage/volume/volume.md)
  - [Common Volume Types](./storage/volume_type/volume_type.md)
    - [`emptyDir`](./storage/empty_dir/empty_dir.md)
    - [`hostPath`](./storage/host_path/host_path.md)
    - [`Persistent Volume` & `Persistent Volume Claim`](./storage/pv_pvc/pv_pvc.md)
    - [`Node Local Persistent Volume`](./storage/node_local_pv/node_local_pv.md)
    - [Dynamic Volume Provisioning & `StorageClass`](./storage/dynamic_pv_storageclass/dynamic_pv_storageclass.md)

- **Injected Data**
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

- **Networking**
  - [Networking Fundamental](./networking/networking_fundamental/networking_fundamental.md)
  - [Container Network Interface (CNI)](./networking/cni/cni.md)
  - [Cluster DNS](./networking/dns/dns.md)
  - [`Service`](./networking/service/service.md)
    - [`Endpoint` & `EndpointSlice`](./networking/endpoint/endpoint.md)
    - [`Topology-Aware Routing`](./networking/tar/tar.md)
    - Service Types:
      - [`ClusterIP`](./networking/clusterip/clusterip.md)
      - [`NodePort`](./networking/nodeport/nodeport.md)
      - [`LoadBalancer`](./networking/loadbalancer/loadbalancer.md)
      - [`Headless Service`](./networking/headless_svc/headless_svc.md)

  - [`Ingress`](./networking/ingress/ingress.md)
  - [`Gateway API` & `GatewayClass`](./networking/gw_api/gw_api.md)

---

## Workload

- [`Pod`](./pod/pod/pod.md)
  - [Lifecycle](./pod/lifecycle/lifecycle.md)
  - [`PriorityClass`](./pod/priorityclass/priorityclass.md)
  - [Affinity](./pod/affinity/affinity.md)

- [`ReplicaSet`](./workload/replicaset/replicaset.md)
- [`Deployment`](./workload/deployment/deployment.md)
  - [Deployment Rollout & Rollback](./workload/deployment/rollout_rollback.md)
  - [Common Deployment Strategies](./workload/deployment/strategy.md)
- [`StatefulSets`](./workload/statefulset/statefulset.md)
  - [StatefulSets Rollout & Rollback](./workload/statefulset/rollout_rollback.md)
- [`DaemonSets`](./workload/daemonset/daemonset.md)
  - [DaemonSets Rollout & Rollback](./workload/daemonset/rollout_rollback.md)
- [`Job`](./workload/job/job.md)
- [`CronJob`](./workload/cronjob/cronjob.md)
- [Operator](./workload/operator/operator.md)
- [Troubleshooting](./workload/debuging/debuging.md)

- Scaling
  - [Scaling](./scaling/scaling/scaling.md)
  - [Horizontal Pod Autoscaler (HPA)](./scaling/hpa/hpa.md)
  - [Vertical Pod Autoscaling (VPA)](./scaling/vpa/vpa.md)

---

## Security

- [Security Fundamental](./security/fundamental/fundamental.md)

- [Admission Controller](./security/admission_controller/admission_controller.md)

- [Network Policy](./security/network_policy/network_policy.md)
- [User](./security/user/user.md)
  - [ServiceAccount](./security/svc_account/svc_account.md)
- [Authentication](./security/authentication/authentication.md)
- [Authorization](./security/authorization/authorization.md)
  - [`Role-based access control (RBAC)`](./security/rbac/rbac.md)
- [Security Context](./security/security_context/security_context.md)
  - [Docker Security](./security/docker_security/docker_security.md)
- [Pod Security Standards](./security/pod_security/pod_security.md)

---

## Configuration

- [`Helm Charts`](./config/helm/helm.md)
- [`Kustomize`](./config/kustomize/kustomize.md)

---

## Installation

- [`minikube`](./install/minikube/minikube.md)
- [`minikube` Installation: RHEL9](./install/minikube_rhel9/minikube_rhel9.md)
- [`minikube` Installation: Ubuntu](./install/minikube_ubuntu/minikube_ubuntu.md)
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

---

## CKA

- [Curriculum](./cka/exam.md)
  - [Network](./cka/network.md)
  - [Storage](./cka/storage.md)
  - [workload](./cka/workload.md)
  - [Security](./cka/security.md)
  - [Cluster](./cka/cluster.md)

- Common Command

```sh
kubectl config set-context --current --namespace=<your-namespace-name>
```
