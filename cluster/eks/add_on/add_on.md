# EKS - Add-ons

[Back](../index.md)

---

## Add-ons

- Query EKS addon

| CMD                                                                                                           | DESC                                                                                                 |
| ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `aws eks list-addons --cluster-name <cluster-name>`                                                           | List installed EKS add-ons in a cluster                                                              |
| `aws eks describe-addon --cluster-name <cluster-name> --addon-name <addon-name>`                              | Show details about one installed add-on                                                              |
| `aws eks describe-addon --cluster-name <cluster-name> --addon-name <addon-name> --query "addon.status"`       | Show only the add-on status                                                                          |
| `aws eks describe-addon --cluster-name <cluster-name> --addon-name <addon-name> --query "addon.addonVersion"` | Show the installed add-on version.                                                                   |
| `aws eks describe-addon-configuration --addon-name <addon-name> --addon-version <addon-version>`              | Show the configuration schema for an add-on version. Useful before setting `--configuration-values`. |

- Query Addon

| CMD                                                                                        | DESC                                                                       |
| ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------- |
| `aws eks describe-addon-versions`                                                          | List available EKS add-ons and versions.                                   |
| `aws eks describe-addon-versions --kubernetes-version <version>`                           | List available add-ons compatible with a specific Kubernetes version.      |
| `aws eks describe-addon-versions --addon-name <addon-name>`                                | List available versions for a specific add-on.                             |
| `aws eks describe-addon-versions --addon-name <addon-name> --kubernetes-version <version>` | List versions of one add-on compatible with a specific Kubernetes version. |

- Create & Delete

| CMD                                                                                                                   | DESC                                                                               |
| --------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `aws eks create-addon --cluster-name <cluster-name> --addon-name <addon-name>`                                        | Install an EKS add-on into the cluster.                                            |
| `aws eks create-addon --cluster-name <cluster-name> --addon-name <addon-name> --addon-version <addon-version>`        | Install a specific version of an add-on.                                           |
| `aws eks create-addon --cluster-name <cluster-name> --addon-name <addon-name> --service-account-role-arn <role-arn>`  | Install an add-on with an IAM role for its Kubernetes service account.             |
| `aws eks create-addon --cluster-name <cluster-name> --addon-name <addon-name> --configuration-values '<json-string>'` | Install an add-on with custom configuration values.                                |
| `aws eks delete-addon --cluster-name <cluster-name> --addon-name <addon-name>`                                        | Delete an installed EKS add-on.                                                    |
| `aws eks delete-addon --cluster-name <cluster-name> --addon-name <addon-name> --preserve`                             | Delete the EKS add-on object but preserve the Kubernetes resources in the cluster. |

- Update

| CMD                                                                                                                   | DESC                                                                  |
| --------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| `aws eks list-updates --name <cluster-name> --addon-name <addon-name>`                                                | List update operations for a specific add-on.                         |
| `aws eks describe-update --name <cluster-name> --addon-name <addon-name> --update-id <update-id>`                     | Check the status of an add-on update.                                 |
| `aws eks update-addon --cluster-name <cluster-name> --addon-name <addon-name>`                                        | Update an installed add-on.                                           |
| `aws eks update-addon --cluster-name <cluster-name> --addon-name <addon-name> --addon-version <addon-version>`        | Update an add-on to a specific version.                               |
| `aws eks update-addon --cluster-name <cluster-name> --addon-name <addon-name> --configuration-values '<json-string>'` | Update custom configuration for an add-on.                            |
| `aws eks update-addon --cluster-name <cluster-name> --addon-name <addon-name> --resolve-conflicts PRESERVE`           | Update add-on while preserving existing configuration where possible. |
| `aws eks update-addon --cluster-name <cluster-name> --addon-name <addon-name> --resolve-conflicts OVERWRITE`          | Update add-on and overwrite conflicting configuration.                |
