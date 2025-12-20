# Kubernetes

[Back](../../index.md)

---

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

## Application

- [Pod](./app/pod/pod.md)
- [Deployment](./app/deploy/deploy.md)
  - [Rolling update and roll back](./app/deploy_rolling/deploy_rolling.md)

---

- [Container Management](./pod/container/container.md)
  - [ConfigMap](./pod/container_configmap/container_configmap.md)
  - [Secret](./pod/container_secret/container_secret.md)
  - [Multi-containers](./pod/container_multi/container_multi.md)
- [ReplicaSet](./pod/replicaset/replicaset.md)
- [DaemonSets](./pod/daemonset/daemonset.md)
- [Static Pod](./pod/static_pod/static_pod.md)
- [Scaling](./pod/scaling/scaling.md)
  - [Horizontal Scaling](./pod/scaling_horizontal/scaling_horizontal.md)
  - [Vertical Scaling](./pod/scaling_vertical/scaling_vertical.md)
- [!PriorityClass](./pod/pod_priorityclass/pod_priorityclass.md)
- [Resources Limit](./pod/pod_resource_limit/pod_resource_limit.md)

- [Troubleshooting](./debuging/debuging.md)

---

- [Admission Controller](./adm_ctl/adm_ctl.md)

---

- [Cluster](./cluster/cluster.md)

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

  - [Namespace](./management/namespace/namespace.md)
  - [Label and Selector](./management/label_selector/label_selector.md)
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

- [Storage](./storage/storage/storage.md)

---

- [Networking](./networking/networking.md)

  - [Service](./networking/service/service.md)

    - [NodePort](./networking/svr_nodeport/svr_nodeport.md)
    - [ClusterIP](./networking/svr_clusterip/svr_clusterip.md)
    - [LoadBalancer](./networking/svr_loadbalancer/svr_loadbalancer.md)

  - [Pod Networking](./networking/pod/pod.md)
  - [Service Networking](./networking/service/service.md)
  - [Cluster DNS](./networking/dns/dns.md)
  - [Ingress](./networking/ingress/ingress.md)
  - [Gateway API](./networking/gw_api/gw_api.md)

---

- [HELM](./helm/helm.md)
- [Kustomize](./kustomize/kustomize.md)

---

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

| CMD                                         | DESC                          |
| ------------------------------------------- | ----------------------------- |
| `kubectl api-resources`                     | List all resources in k8s     |
| `kubectl explain resource_name`             | Show manual of a resource     |
| `kubectl explain resource_name --recursive` | Show all fields of a resource |
| `kubectl explain resource_name.field`       | Show a field of a resource    |

# JSON Path

- used to fileter info retrieved from API server

```sh
# output in json
kubectl get node -o json > node.json


# get image
kubectl get pods -o=jsonpath="{.items[0].spec.containers[0].image}"

# get metadata: name
kubectl get nodes -o=jsonpath='{.items[*].metadata.name}'

# get cpu
kubectl get nodes -o=jsonpath='{.items[*].status.capacity.cpu}'

# gen a report
kubectl get nodes -o=jsonpath='{.items[*].metadata.name} {.items[*].status.capacity.cpu}'
# master  node01
# 4 4

# loop
kubectl get nodes -o=jsonpath'{range .items[*]} {.metadata.name} {"\t"} {.status.capacity.cpu} {"\n"} {end}'

# custom columns
kubectl get nodes -o=custom-columns=NODE:.metadata.name,CPU:.status.capacity.cpu
# NODE             CPU
# docker-desktop   12

# sort
kubectl get nodes --sort-by=.metadata.name

kubectl get nodes --sort-by=.status.capacity.cpu
```

https://docs.linuxfoundation.org/tc-docs/certification/tips-cka-and-ckad


```sh
kubectl create deploy nginx --image=nginx --port=80
kubectl expose deploy nginx --type=LoadBalancer --name=nginx --port=8080 --target-port=80
kubectl get svc
# NAME         TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
# nginx        LoadBalancer   10.103.65.211   localhost     8080:31490/TCP   22s

kubectl port-forward service/nginx 8080:8080
curl http://localhost:8080/
# <!DOCTYPE html>
# <html>
# <head>
# <title>Welcome to nginx!</title>
# <style>
# html { color-scheme: light dark; }
# body { width: 35em; margin: 0 auto;
# font-family: Tahoma, Verdana, Arial, sans-serif; }
# </style>
# </head>
# <body>
# <h1>Welcome to nginx!</h1>
# <p>If you see this page, the nginx web server is successfully installed and
# working. Further configuration is required.</p>

# <p>For online documentation and support please refer to
# <a href="http://nginx.org/">nginx.org</a>.<br/>
# Commercial support is available at
# <a href="http://nginx.com/">nginx.com</a>.</p>

# <p><em>Thank you for using nginx.</em></p>
# </body>
# </html>
```