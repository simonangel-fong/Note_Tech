# Azure - Install

[Back](./index.md)

- [Azure - Install](#azure---install)
  - [Azure CLI](#azure-cli)

---

## Azure CLI

```sh
winget install --exact --id Microsoft.AzureCLI

az login

az account list --output table
# Name                  CloudName    SubscriptionId                        TenantId                              State    IsDefault
# --------------------  -----------  ------------------------------------  ------------------------------------  -------  -----------
# Azure subscription 1  AzureCloud                                                                               Enabled  True

az account set --subscription "Azure subscription 1"

az group list --output table
```
