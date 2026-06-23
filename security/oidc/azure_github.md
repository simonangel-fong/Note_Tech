# `OIDC`: `GitHub Actions` with `Azure`

[Back](../README.md)

- [`OIDC`: `GitHub Actions` with `Azure`](#oidc-github-actions-with-azure)
  - [GitHub Actions with Azure via `OIDC`](#github-actions-with-azure-via-oidc)
  - [Configuration in Azure](#configuration-in-azure)
    - [Portal Method](#portal-method)
    - [AZ CLI](#az-cli)
    - [Enable Access to Terraform Backend Storage](#enable-access-to-terraform-backend-storage)
  - [GitHub Configuration](#github-configuration)

---

## GitHub Actions with Azure via `OIDC`

```txt
[ GitHub Actions Runner ]
          │
          │  (1. Workflow has permissions: id-token: write)
          │
          ├──(2. Request OIDC JWT)──────────────> [ GitHub OIDC Provider ]
          │
          │ <──(3. Issues signed OIDC JWT)────────┘
          │
          ├──(4. Login to Azure:
          │        OIDC JWT + Azure Client ID + Tenant ID)
          │─────────────────────────────────────> [ Microsoft Entra ID ]
          │                                      (Validates issuer, audience,
          │                                       subject claim, client ID,
          │                                       and federated credential)
          │
          │ <──(5. Issues short-lived Azure access token)
          │
          └──(6. Call Azure Resource Manager APIs)
                 using access token
                 + target subscription/resource scope
                 + Azure RBAC permissions
          ──────────────────────────────────────> [ Azure Resources ]
```

- **1. GitHub Actions Runner requests OIDC token**:
  - The `workflow runner` **requests** an `OIDC JWT` from `GitHub’s OIDC provider` using the workflow’s `id-token: write` permission.
  - The goal is to **obtain a short-lived identity token** for this workflow run.

- **2. GitHub OIDC Provider issues signed JWT**:
  - `GitHub’s OIDC provider` **issues a signed JWT** containing claims such as _repository_, _branch_, _workflow_, _audience_, and _subject_.
  - The goal is to **prove the workflow’s identity** to an external cloud provider.

- **3. Runner sends token to Microsoft Entra ID**
  - The `runner` **sends** the `GitHub OIDC JWT`, `Azure client ID`, and `tenant ID` to `Microsoft Entra ID`.
  - The goal is to exchange the GitHub identity token for an Azure access token.

- **4. Microsoft Entra ID validates federated trust**:
  - `Microsoft Entra ID` **validates** the _JWT signature, issuer, audience, subject claims, client ID_, and configured `federated identity credential`.
  - The goal is to confirm that this `GitHub workflow` is **trusted to authenticate** as the Azure identity.

- **5. Microsoft Entra ID issues access token**:
  - `Microsoft Entra ID` **issues a short-lived** `Azure access token` for the trusted application or managed identity.
  - The goal is to allow the workflow to authenticate to Azure **without using a long-lived secret**.

- **6. Runner accesses Azure resources**:
  - The `runner` uses the `Azure access token` to call `Azure Resource Manager APIs` against the target subscription or resource scope.
  - The goal is to deploy or manage Azure resources, subject to Azure `RBAC permissions`.

---

## Configuration in Azure

### Portal Method

- **1. Create a Microsoft Entra Application**

1. Navigate to the `Microsoft Entra` **admin cente**r.
2. Go to **Identity** > **Applications** > **App registrations** and click **New registration**.
3. Name the **application** (e.g., github-storage-oidc) and click **Register**.
4. Note down:
   - `Application (client) ID`
   - `Directory (tenant) ID`

---

- **2. Configure the Federated Identity Credential**

1. Inside new `App Registration`, click on `Certificates & secrets` from the left menu.
2. Select the `Federated credentials` tab and click **Add credential**.
3. Select your **external provider** (e.g., **GitHub Actions**) from the dropdown list.
4. Fill out the required parameters:
   - Organization/Owner: external organization name.
   - Repository: project repository name.
   - Entity Type: Select Environment, Branch, or Tag based on the security needs.
   - Audience: Default is typically api://AzureADTokenExchange.

---

- **3. Assign Role-Based Access Control (RBAC) to the Storage Account**

1. Navigate to your `Azure Storage Account` in the Azure Portal.
2. Click on `Access Control (IAM)` on the left-hand navigation sidebar.
3. Click **Add** > **Add role assignment**.
4. Assign the **specific role** needed for storage actions. For managing storage data (like backend states), choose `Storage Blob Data Contributor`.
5. Under Assign access to, choose `User, group, or service principal` and select the name of the `Entra App Registration`.

---

### AZ CLI

```sh
# ########################################
# 1. Create a Microsoft Entra Application
# ########################################
# app name
APP_NAME="demo-storage-web-host"


# Create a Microsoft Entra Application
az ad app create --display-name "$APP_NAME"
# confirm
az ad app list --display-name "$APP_NAME" --query "[].appId" -o tsv
APP_ID=$(az ad app list --display-name "$APP_NAME" --query "[].appId" -o tsv | tr -d '\r' | xargs) && echo $APP_ID
# az ad app delete --id "$APP_ID"

# Create a Service Principal in Microsoft Entra Application
az ad sp create --id "$APP_ID"
# confirm
SP_ID=$(az ad sp show --id "$APP_ID" --query id -o tsv | tr -d '\r' | xargs) && echo $SP_ID
# az ad sp delete --id "$SP_ID"

# ##################################################
# 2. Configure the Federated Identity Credential
# ##################################################
# GitHb Owner
GH_OWNER="simonangel-fong"
# repo name
GH_REPO="Terraform_Demo_Azure_Storage_Web_Hosting"


# Create Federated Identity Credential
az ad app federated-credential create --id "$APP_ID" --parameters '{
  "name": "gh-deploy",
  "issuer": "https://token.actions.githubusercontent.com",
  "subject": "repo:'"$GH_OWNER"'/'"$GH_REPO"':ref:refs/heads/master",
  "audiences": ["api://AzureADTokenExchange"]
}'
# confirm
az ad app federated-credential list --id "$APP_ID" --query "[].id" -o tsv
# az ad app federated-credential delete --id "$APP_ID" --federated-credential-id $(az ad app federated-credential list --id "$APP_ID" --query "[].id" -o tsv | tr -d '\r' | xargs)

# ######################################################################
# Assign Role-Based Access Control (RBAC) to the Storage Account
# ######################################################################
# subscription id
SUB_ID=$(az account show --query id -o tsv | tr -d '\r' | xargs) && echo $SUB_ID
# resource group name
RG_NAME=$(echo -n "demo-storage-web-host-dev" | tr -d '\r') && echo $RG_NAME
# storage account name
SA_NAME=$(echo -n "demostoragewebhost" | tr -d '\r') && echo $SA_NAME


# app role
az role assignment create \
  --assignee "$APP_ID" \
  --role "Storage Blob Data Contributor" \
  --scope "/subscriptions/$SUB_ID/resourceGroups/$RG_NAME/providers/Microsoft.Storage/storageAccounts/$SA_NAME"
```

---

### Enable Access to Terraform Backend Storage

```sh
# Subscription id
SUB_ID=$(az account show --query id -o tsv | tr -d '\r') && echo $SUB_ID

# App id
APP_ID=$(az ad app list --display-name "$APP_NAME" --query "[].appId" -o tsv | tr -d '\r' | xargs) && echo $APP_ID

# Service Principal id
SP_OBJECT_ID=$(az ad sp show --id "$APP_ID" --query id -o tsv | tr -d '\r' | xargs) && echo $SP_OBJECT_ID

# TF Resource Group
TF_RG_NAME=$(echo -n "rg-tfstate-ca" | tr -d '\r')
# TF Storage Account
TF_SA_NAME=$(echo -n "tfstatesf7592" | tr -d '\r')

az role assignment create \
  --assignee-object-id "$SP_OBJECT_ID" \
  --assignee-principal-type ServicePrincipal \
  --role "Storage Blob Data Contributor" \
  --scope "/subscriptions/$SUB_ID/resourceGroups/$TF_RG_NAME/providers/Microsoft.Storage/storageAccounts/$TF_SA_NAME"

```

---

## GitHub Configuration

```sh
# AZURE_CLIENT_ID
APP_ID=$(az ad app list --display-name "$APP_NAME" --query "[].appId" -o tsv) && echo $APP_ID
gh secret set AZURE_CLIENT_ID

# AZURE_TENANT_ID
TENANT_ID=$(az account show --query tenantId -o tsv) && echo $TENANT_ID
gh secret set AZURE_TENANT_ID

# AZURE_SUBSCRIPTION_ID
SUB_ID=$(az account show --query id -o tsv | tr -d '\r' | xargs) && echo $SUB_ID
gh secret set AZURE_SUBSCRIPTION_ID
```

---
