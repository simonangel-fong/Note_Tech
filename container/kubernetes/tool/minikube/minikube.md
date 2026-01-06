# Kubernetest Solution - Minikube

[Back](../../index.md)

- [Kubernetest Solution - Minikube](#kubernetest-solution---minikube)
  - [Minikube](#minikube)

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
