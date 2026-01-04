


## Kubernetes Operators

- `Kubernetes operator`

  - an **application-specific controller** that **automates** the deployment and management of an application running on Kubernetes.
  - must install them separately.

- Each `operator` **extends the Kubernetes API** with its own set of **custom object types** that you use to deploy and configure the application.
  - When an instance of this **custom object type** is **created** using the Kubernetes API, the `operator` creates the `Deployments` or `StatefulSets` that create the Pods in which the application runs.

![pic](./pic/operator.png)
