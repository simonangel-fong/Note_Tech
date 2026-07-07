# EKS - Group Node

[Back](../index.md)

---

## Group Node

- Query

| CMD                                                                                                                     | DESC                                                    |
| ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| `aws eks list-nodegroups --cluster-name <cluster-name>`                                                                 | List managed node groups in an EKS cluster.             |
| `aws eks describe-nodegroup --cluster-name <cluster-name> --nodegroup-name <nodegroup-name>`                            | Show detailed information about one managed node group. |
| `aws eks describe-nodegroup --cluster-name <cluster-name> --nodegroup-name <nodegroup-name> --query "nodegroup.status"` | Show only the node group status                         |

- Create and remove

| CMD                                                                                                                                                                                                                                        | DESC                                                              |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------- |
| `aws eks create-nodegroup --cluster-name <cluster-name> --nodegroup-name <nodegroup-name> --node-role <node-role-arn> --subnets <subnet-id-1> <subnet-id-2>`                                                                               | Create a managed node group for an EKS cluster.                   |
| `aws eks create-nodegroup --cluster-name <cluster-name> --nodegroup-name <nodegroup-name> --node-role <node-role-arn> --subnets <subnet-id-1> <subnet-id-2> --instance-types t3.medium --scaling-config minSize=1,maxSize=3,desiredSize=2` | Create a node group with specific instance type and scaling size. |
| `aws eks create-nodegroup --cluster-name <cluster-name> --nodegroup-name <nodegroup-name> --node-role <node-role-arn> --subnets <subnet-id-1> <subnet-id-2> --capacity-type SPOT`                                                          | Create a Spot managed node group.                                 |
| `aws eks wait nodegroup-active --cluster-name <cluster-name> --nodegroup-name <nodegroup-name>`                                                                                                                                            | Wait until the node group becomes `ACTIVE`.                       |
| `aws eks wait nodegroup-deleted --cluster-name <cluster-name> --nodegroup-name <nodegroup-name>`                                                                                                                                           | Wait until the node group is deleted.                             |
| `aws eks delete-nodegroup --cluster-name <cluster-name> --nodegroup-name <nodegroup-name>`                                                                                                                                                 | Delete a managed node group.                                      |

- k8s node labels

| CMD                                                                                                                                                                          | DESC                                               |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| `aws eks update-nodegroup-config --cluster-name <cluster-name> --nodegroup-name <nodegroup-name> --labels addOrUpdateLabels=env=dev,team=platform`                           | Add or update Kubernetes labels on the node group. |
| `aws eks update-nodegroup-config --cluster-name <cluster-name> --nodegroup-name <nodegroup-name> --labels removeLabels=env,team`                                             | Remove labels from the node group.                 |
| `aws eks update-nodegroup-config --cluster-name <cluster-name> --nodegroup-name <nodegroup-name> --taints addOrUpdateTaints=[{key=workload,value=batch,effect=NO_SCHEDULE}]` | Add or update taints on the node group.            |
| `aws eks update-nodegroup-config --cluster-name <cluster-name> --nodegroup-name <nodegroup-name> --taints removeTaints=[{key=workload,value=batch,effect=NO_SCHEDULE}]`      | Remove taints from the node group.                 |

- Update

| CMD                                                                                                                                                  | DESC                                                                        |
| ---------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| `aws eks list-updates --name <cluster-name> --nodegroup-name <nodegroup-name>`                                                                       | List update operations for a node group.                                    |
| `aws eks describe-update --name <cluster-name> --nodegroup-name <nodegroup-name> --update-id <update-id>`                                            | Check the status of a node group update.                                    |
| `aws eks update-nodegroup-config --cluster-name <cluster-name> --nodegroup-name <nodegroup-name> --scaling-config minSize=1,maxSize=5,desiredSize=3` | Update node group scaling configuration.                                    |
| `aws eks update-nodegroup-version --cluster-name <cluster-name> --nodegroup-name <nodegroup-name>`                                                   | Update the node group to the latest AMI release for its Kubernetes version. |
| `aws eks update-nodegroup-version --cluster-name <cluster-name> --nodegroup-name <nodegroup-name> --kubernetes-version <version>`                    | Update the node group Kubernetes version.                                   |

- tag

| CMD                                                                                           | DESC                                |
| --------------------------------------------------------------------------------------------- | ----------------------------------- |
| `aws eks list-tags-for-resource --resource-arn <nodegroup-arn>`                               | List tags on a node group resource. |
| `aws eks tag-resource --resource-arn <nodegroup-arn> --tags Environment=dev,Project=eks-demo` | Add tags to a node group.           |
| `aws eks untag-resource --resource-arn <nodegroup-arn> --tag-keys Environment Project`        | Remove tags from a node group.      |
