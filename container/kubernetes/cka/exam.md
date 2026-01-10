# CKA - Exame

[Back](../index.md)

---

## Exam Details

- The exams are **delivered online** and consist of performance-based tasks (problems) to be solved on the command line running Linux.
- The exams consist of **15-20** performance-based **tasks**.
- Candidates have **2 hours** to complete the CKA and CKAD exam.
- The exams are proctored remotely via streaming audio, video, and screen sharing feeds.
- Results will be emailed 24 hours from the time that the exam is completed.

- https://syscheck.bridge.psiexams.com/

---

### Resources Allowed

- Kubernetes Documentation: https://kubernetes.io/docs
  - Note that using the search function on https://kubernetes.io/docs/ is allowed, but you must not open external search results.
- Kubernetes Blog https://kubernetes.io/blog/
- Helm Documentation https://helm.sh/docs
- Task-specific documentation provided in the Quick Reference box. This includes links to documentation for various tools that might be needed to solve a task.
- CKA only: Gateway API Documentation https://gateway-api.sigs.k8s.io

---

## CKA - Curriculum

### 20% - Servicing and Networking

- Understand connectivity between Pods
- Define and enforce **Network Policies**
  - ref: https://kubernetes.io/docs/concepts/services-networking/network-policies/
- Use ClusterIP, NodePort, LoadBalancer service types and endpoints
- Use the Gateway API to manage Ingress traffic
- Know how to use Ingress controllers and Ingress resources
- Understand and use CoreDNS

---

### 25% - Cluster Architecture, Installation and Configuration

- Manage role based access control (RBAC)
- Prepare underlying infrastructure for installing a Kubernetes cluster
- Create and manage Kubernetes clusters using kubeadm
- Manage the lifecycle of Kubernetes clusters
- Implement and configure a highly-available control plane
- Use Helm and Kustomize to install cluster components
- Understand extension interfaces (CNI, CSI, CRI, etc.)
- Understand CRDs, install and configure operators

---

### 10% - Storage

- Implement storage classes and dynamic volume provisioning
- Configure volume types, access modes and reclaim policies
- Manage persistent volumes and persistent volume claims

---

### 15% - Workloads and Scheduling

- Understand application deployments and how to perform rolling update and rollbacks
- Use ConfigMaps and Secrets to configure applications
- Configure workload autoscaling
- Understand the primitives used to create robust, self-healing, application deployments
- Configure Pod admission and scheduling (limits, node affinity, etc.)

---

### 30% - Troubleshooting

- Troubleshoot clusters and nodes
- Troubleshoot cluster components
- Monitor cluster and application resource usage
- Manage and evaluate container output streams
- Troubleshoot services and networking
