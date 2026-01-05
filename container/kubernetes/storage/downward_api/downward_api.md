# Kubernetes: Storage - Downward API

[Back](../../index.md)

- [Kubernetes: Storage - Downward API](#kubernetes-storage---downward-api)
  - [Downward API](#downward-api)
    - [Common feilds](#common-feilds)

---

## Downward API

- `Downward API`

  - a Kubernetes mechanism that allows a `container` to **consume information** about itself or its host without using the Kubernetes client or API server.
  - a way to **inject values** from the pod’s `metadata`, `spec`, or `status` fields down into the container.

- 2 types of injection:
  - as env ver
    - pod’s general metadata: `spec.containers.env.fieldRef`
    - resource constraints: `spec.containers.env.resourceFieldRef`
  - as file: `spec.volumes.downwardAPI`

---

### Common feilds

- Available from `fieldRef` field

| fieldRef Fields               | env   | vol   | DESC                                     |
| ----------------------------- | ----- | ----- | ---------------------------------------- |
| `metadata.name`               | Y     | Y     | pod’s name.                              |
| `metadata.namespace`          | Y     | Y     | pod’s namespace.                         |
| `metadata.uid`                | Y     | Y     | pod’s uid.                               |
| `metadata.labels`             | **N** | Y     | pod’s labels.                            |
| `metadata.labels['key']`      | Y     | Y     | value of the specified label.            |
| `metadata.annotations`        | **N** | Y     | pod’s annotations.                       |
| `metadata.annotations['key']` | Y     | Y     | The value of the specified annotation.   |
| `spec.nodeName`               | Y     | **N** | name of the worker node the pod runs on. |
| `spec.serviceAccountName`     | Y     | **N** | name of the pod’s service account.       |
| `status.podIP`                | Y     | **N** | pod’s IP address.                        |
| `status.hostIP`               | Y     | **N** | worker node’s IP address.                |

- Available from `resourceFieldRef` field

| resourceFieldRef Fields      | env | vol | DESC                                   |
| ---------------------------- | --- | --- | -------------------------------------- |
| `requests.cpu`               | Y   | Y   | container’s CPU request.               |
| `requests.memory`            | Y   | Y   | container’s memory request.            |
| `requests.ephemeral-storage` | Y   | Y   | container’s ephemeral storage request. |
| `limits.cpu`                 | Y   | Y   | container’s CPU limit.                 |
| `limits.memory`              | Y   | Y   | container’s memory limit.              |
| `limits.ephemeral-storage`   | Y   | Y   | container’s ephemeral storage limit.   |

- For **resource fields**, the `containerName` field must be specified because volumes are defined at the **pod level** and it isn’t obvious which container’s resources are being referenced.

---
