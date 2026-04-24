# Jenkins - K8s

[Back](../index.md)

- [Jenkins - K8s](#jenkins---k8s)
  - [Setup Pod](#setup-pod)
  - [Setup Service Account](#setup-service-account)
  - [Install Jenkins with Helm](#install-jenkins-with-helm)

---

## Setup Pod

```sh
ssh -o 'ProxyJump=aadmin@10.0.0.50' 'ubuntuadmin@192.168.100.150'

kubectl cluster-info
# Kubernetes control plane is running at https://192.168.49.2:8443
# CoreDNS is running at https://192.168.49.2:8443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

minikube ip
# 192.168.49.2

kubectl get pods -A | grep jenkins
# jenkins                jenkins-0                                           2/2     Running     16 (28m ago)    10d

kubectl get deploy -A | grep jenkins
# none

kubectl get sa -A | grep jenkins
# jenkins                default                                       10d
# jenkins                jenkins                                       10d
```

---

## Setup Service Account

```sh
cat > jenkins-rbac.yaml<<'EOF'
apiVersion: v1
kind: ServiceAccount
metadata:
  name: jenkins
  namespace: jenkins
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: jenkins-agent-manager
  namespace: jenkins
rules:
  - apiGroups: [""]
    resources: ["pods", "pods/log", "pods/exec", "secrets", "events"]
    verbs: ["create", "delete", "get", "list", "watch", "patch", "update"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: jenkins-agent-manager-binding
  namespace: jenkins
subjects:
  - kind: ServiceAccount
    name: jenkins
    namespace: jenkins
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: jenkins-agent-manager
EOF
```

---

## Install Jenkins with Helm

- Env:
  - cluster: minikube
  - Installation method: helm

- values.yaml

```yaml
controller:
  admin:
    username: admin
    password: admin123

  serviceType: ClusterIP

  ingress:
    enabled: true
    ingressClassName: nginx
    hostName: homelab-jenkins.arguswatcher.net
    path: /
    pathType: Prefix

  # Do not run builds on the controller
  numExecutors: 0

  installPlugins:
    - kubernetes
    - workflow-aggregator
    - git
    - configuration-as-code

  initializeOnce: true

  JCasC:
    # must be true if you want Helm-defined agent pod templates
    defaultConfig: true

persistence:
  enabled: true
  size: 2Gi

agent:
  enabled: true

  # optional tuning
  maxRequestsPerHostStr: "32"
  retentionTimeout: "5"
  waitForPodSec: "120"

  podTemplates:
    python: |
      - name: python
        label: jenkins-python
        serviceAccount: jenkins
        containers:
          - name: python
            image: python:3.12
            command: "/bin/sh -c"
            args: "cat"
            ttyEnabled: true
            resourceRequestCpu: "200m"
            resourceRequestMemory: "256Mi"
            resourceLimitCpu: "500m"
            resourceLimitMemory: "512Mi"

    maven: |
      - name: maven
        label: jenkins-maven
        serviceAccount: jenkins
        containers:
          - name: maven
            image: maven:3.9.9-eclipse-temurin-17
            command: "/bin/sh -c"
            args: "cat"
            ttyEnabled: true
            resourceRequestCpu: "500m"
            resourceRequestMemory: "512Mi"
            resourceLimitCpu: "1"
            resourceLimitMemory: "1Gi"
```
