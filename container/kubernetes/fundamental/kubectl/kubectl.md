# Kubernetes - kubectl

[Back](../../index.md)

- [Kubernetes - kubectl](#kubernetes---kubectl)
  - [`kubectl`](#kubectl)
  - [Minikube](#minikube)

---

## `kubectl`

- `kubectl`:
  - the command line utilities
  - used to **deploy and manage applications** on a kubernetes cluster, to get cluster information, get the status of nodes in the cluster and many other things.

| CMD                    | DESC                                   |
| ---------------------- | -------------------------------------- |
| `kubectl run app_name` | deploy an application on the cluster   |
| `kubectl cluster-info` | view information about the cluster     |
| `kubectl get nodes`    | list all the nodes part of the cluster |

---

## Minikube

- `Minikube`
  - a lightweight tool that allows you to **run a single-node Kubernetes cluster** locally on your personal machine.
  - It's ideal for **learning**, development, and testing Kubernetes concepts without needing a full cloud setup.

| **Command**                     | **Description**                                             |
| ------------------------------- | ----------------------------------------------------------- |
| `minikube status`               | Shows the status of the cluster and its components          |
| `minikube start`                | Starts a local Kubernetes cluster                           |
| `minikube stop`                 | Stops the running cluster                                   |
| `minikube delete`               | Deletes the cluster                                         |
| `minikube dashboard`            | Opens the Kubernetes Dashboard UI in a browser              |
| `minikube service list`         | Lists the URLs for the services                             |
| `minikube service service_name` | Opens a Kubernetes service in the default browser           |
| `minikube ip`                   | Displays the IP address of the Minikube VM                  |
| `minikube ssh`                  | Opens an SSH session into the Minikube VM                   |
| `minikube tunnel`               | Creates a network route to access LoadBalancer services     |
| `minikube addons list`          | Lists available Minikube add-ons                            |
| `minikube addons enable add_on` | Enables a specific add-on (e.g., metrics-server, dashboard) |
