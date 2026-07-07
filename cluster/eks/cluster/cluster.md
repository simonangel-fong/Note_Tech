# EKS cluster - AWS CLI

[Back](../index.md)

---

## AWS CLI

### Cluster

| CMD                                                                         | DESC                                                     |
| --------------------------------------------------------------------------- | -------------------------------------------------------- |
| `aws eks list-clusters`                                                     | List EKS clusters in the current AWS account and Region. |
| `aws eks list-clusters --region us-east-1`                                  | List EKS clusters in a specific Region.                  |
| `aws eks describe-cluster --name <cluster-name>`                            | Show detailed information about one EKS cluster.         |
| `aws eks describe-cluster --name <cluster-name> --query "cluster.status"`   | Show only the cluster status.                            |
| `aws eks describe-cluster --name <cluster-name> --query "cluster.endpoint"` | Show the Kubernetes API server endpoint.                 |

- local config

| CMD                                                                        | DESC                                                                  |
| -------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| `aws eks update-kubeconfig --name <cluster-name>`                          | Update local kubeconfig so `kubectl` can connect to the EKS cluster.  |
| `aws eks update-kubeconfig --name <cluster-name> --region us-east-1`       | Update kubeconfig for a cluster in a specific Region.                 |
| `aws eks update-kubeconfig --name <cluster-name> --alias <alias-name>`     | Add the cluster to kubeconfig using a shorter or custom context name. |
| `aws eks update-kubeconfig --name <cluster-name> --profile <profile-name>` | Update kubeconfig using a specific AWS CLI profile.                   |

- crud

| CMD                                                                                                                                                  | DESC                                                     |
| ---------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| `aws eks create-cluster --name <cluster-name> --role-arn <cluster-role-arn> --resources-vpc-config subnetIds=<subnet-ids>,securityGroupIds=<sg-ids>` | Create an EKS control plane.                             |
| `aws eks list-updates --name <cluster-name>`                                                                                                         | List recent update operations for the cluster.           |
| `aws eks describe-update --name <cluster-name> --update-id <update-id>`                                                                              | Check the status of a specific cluster update.           |
| `aws eks update-cluster-version --name <cluster-name> --kubernetes-version <version>`                                                                | Upgrade the EKS control plane Kubernetes version.        |
| `aws eks update-cluster-config --name <cluster-name> --resources-vpc-config endpointPublicAccess=true,endpointPrivateAccess=false`                   | Configure public/private Kubernetes API endpoint access. |
| `aws eks delete-cluster --name <cluster-name>`                                                                                                       | Delete the EKS control plane.                            |

- tag

| CMD                                                                                     | DESC                                  |
| --------------------------------------------------------------------------------------- | ------------------------------------- |
| `aws eks list-tags-for-resource --resource-arn <cluster-arn>`                           | List tags on an EKS cluster resource. |
| `aws eks tag-resource --resource-arn <cluster-arn> --tags Environment=dev,Project=demo` | Add tags to an EKS cluster.           |
| `aws eks untag-resource --resource-arn <cluster-arn> --tag-keys Environment Project`    | Remove tags from an EKS cluster.      |
