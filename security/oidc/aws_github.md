# `OIDC`: `GitHub Actions` with `Azure`

[Back](../README.md)

- [`OIDC`: `GitHub Actions` with `Azure`](#oidc-github-actions-with-azure)
  - [GitHub Actions with AWS via OIDC](#github-actions-with-aws-via-oidc)
  - [In AWS, this trust is usually restricted with conditions such as token.actions.githubusercontent.com:aud and token.actions.githubusercontent.com:sub, often scoped to a specific GitHub organization, repository, branch, or environment.](#in-aws-this-trust-is-usually-restricted-with-conditions-such-as-tokenactionsgithubusercontentcomaud-and-tokenactionsgithubusercontentcomsub-often-scoped-to-a-specific-github-organization-repository-branch-or-environment)
  - [Configuration in AWS](#configuration-in-aws)
    - [Console Method](#console-method)
    - [AWS CLI](#aws-cli)
  - [GitHub Configuration](#github-configuration)

---

## GitHub Actions with AWS via OIDC

```txt
[ GitHub Actions Runner ]
          │
          │  (1. Workflow has permissions: id-token: write)
          │
          ├──(2. Request OIDC JWT)──────────────> [ GitHub OIDC Provider ]
          │
          │ <──(3. Issues signed OIDC JWT)────────┘
          │
          ├──(4. Assume AWS IAM Role:
          │        OIDC JWT + Role ARN)
          │─────────────────────────────────────> [ AWS STS ]
          │                                      (Validates issuer, audience,
          │                                       subject claim, OIDC provider,
          │                                       and IAM role trust policy)
          │
          │ <──(5. Issues temporary AWS credentials)
          │
          └──(6. Call AWS APIs)
                 using temporary credentials
                 + target AWS account/region/resource
                 + IAM role permissions
          ──────────────────────────────────────> [ AWS Resources ]
```

1. **GitHub Actions workflow enables OIDC token access:**
   - The workflow is configured with permissions: `id-token: write`.
   - The goal is to allow the runner to request an `OIDC JWT` from `GitHub` during the workflow run.
2. **GitHub Actions Runner requests OIDC token:**
   - The `workflow runner` **requests** an `OIDC JWT` from `GitHub’s OIDC provider`.
   - The goal is to obtain a **short-lived identity token** that represents this specific workflow run.
3. **GitHub OIDC Provider issues signed JWT:**
   - `GitHub’s OIDC provider` **issues** a `signed JWT` containing claims such as repository, branch, workflow, audience, and subject.
   - The goal is to prove the workflow’s identity to AWS.
4. **Runner requests AWS role assumption:**
   - The `runner` **sends** the `GitHub OIDC JWT` and target `IAM role ARN` to `AWS STS`.
   - The goal is to call `sts:AssumeRoleWithWebIdentity` and **exchange** the `GitHub identity token` for AWS credentials.
   - AWS STS returns temporary security credentials for identities authenticated through an OIDC-compatible provider.
5. **AWS STS validates federated trust:**
   - `AWS STS` **validates** the _JWT signature, issuer, audience, subject claim_, _configured IAM OIDC provider_, and the _target role’s trust policy_.
   - The goal is to **confirm** that this **GitHub workflow is trusted** to assume the specified AWS IAM role.
6. **AWS STS issues temporary credentials:**
   - `AWS STS` **issues temporary** `AWS credentials`, including an access key ID, secret access key, session token, and expiration time.
   - The goal is to allow the **workflow to authenticate** to AWS without using long-lived IAM user access keys.
7. **Runner accesses AWS resources:**
   - The `runner` **uses the temporary** `AWS credentials` to call AWS APIs against the target account, region, and resources.
   - The goal is to deploy or manage AWS resources, subject to the permissions attached to the assumed IAM role.

---

## In AWS, this trust is usually restricted with conditions such as token.actions.githubusercontent.com:aud and token.actions.githubusercontent.com:sub, often scoped to a specific GitHub organization, repository, branch, or environment.

## Configuration in AWS

### Console Method

- **1. Create an IAM OIDC Identity Provider**

1. Go to `IAM` > `Access management` > `Identity providers`.
2. Click **Add provider**.
   - Select provider type: `OpenID Connect`.
   - Configure:
     - Provider URL: `https://token.actions.githubusercontent.com`
     - Audience: `sts.amazonaws.com`
   - Click Add provider.

---

- **2. Create an IAM Role for GitHub Actions**

1. Go to `IAM` > `Access management` > `Roles`.
2. Click **Create role**.
   - Select Trusted entity type: `Web identity`.
   - Select:
     - Identity provider: `token.actions.githubusercontent.com`
     - Audience: `sts.amazonaws.com`
   - Click Next.
3. Attach `IAM Permissions` to the Role
   - Select the permission policy required by the workflow.
   - Use least-privilege permissions based on the target AWS resource.
     - e.g., `AmazonS3ReadOnlyAccess`, `AmazonEC2ContainerRegistryPowerUser`
     - Custom deployment policy for ECS, Lambda, S3, or Terraform backend access
   - Click Next.
4. Name and Create the IAM Role
   - Enter a role name. e.g., github-actions-oidc-role
5. Review the selected OIDC provider, audience, and permissions.
   - Click Create role.

---

- **3. Configure the Role Trust Policy**

1. Open the created `IAM Role`. Go to the `Trust relationships` tab.
2. Click **Edit trust policy**.
3. Add **conditions** to restrict access to the expected GitHub repository, branch, tag, or environment.
   - Example for a specific branch:
   ```json
   {
     "Effect": "Allow",
     "Principal": {
       "Federated": "arn:aws:iam::<account-id>:oidc-provider/token.actions.githubusercontent.com"
     },
     "Action": "sts:AssumeRoleWithWebIdentity",
     "Condition": {
       "StringEquals": {
         "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
       },
       "StringLike": {
         "token.actions.githubusercontent.com:sub": "repo:<ORG>/<REPO>:ref:refs/heads/main"
       }
     }
   }
   ```

---

### AWS CLI

```sh
# ########################################
# 1. Create IAM OIDC Identity Provider
# ########################################
# OIDC provider URL
OIDC_PROVIDER_URL="https://token.actions.githubusercontent.com"
# OIDC audience for AWS STS
OIDC_AUDIENCE="sts.amazonaws.com"

aws iam create-open-id-connect-provider \
  --url "$OIDC_PROVIDER_URL" \
  --client-id-list "$OIDC_AUDIENCE"

# confirm
aws iam list-open-id-connect-providers

# delete if needed
# aws iam delete-open-id-connect-provider \
#   --open-id-connect-provider-arn "$OIDC_PROVIDER_ARN"


# ########################################
# 2 Create IAM Role
# ########################################
# GitHub owner / organization
GH_OWNER="simonangel-fong"
# GitHub repository
GH_REPO="Terraform_Demo_AWS_Project"

# AWS account ID
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text) && echo $AWS_ACCOUNT_ID
# provider ARN
OIDC_PROVIDER_ARN="arn:aws:iam::$AWS_ACCOUNT_ID:oidc-provider/$OIDC_PROVIDER_HOST" && echo $OIDC_PROVIDER_ARN
# OIDC provider host
OIDC_PROVIDER_HOST="token.actions.githubusercontent.com"
# OIDC audience for AWS STS
OIDC_AUDIENCE="sts.amazonaws.com"

# Create IAM Role Trust Policy
cat > trust-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "$OIDC_PROVIDER_ARN"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "$OIDC_PROVIDER_HOST:aud": "$OIDC_AUDIENCE"
        },
        "StringLike": {
          "$OIDC_PROVIDER_HOST:sub": "repo:$GH_OWNER/$GH_REPO:ref:refs/heads/main"
        }
      }
    }
  ]
}
EOF

cat trust-policy.json

# IAM role name
ROLE_NAME="github-actions-oidc-role"
aws iam create-role \
  --role-name "$ROLE_NAME" \
  --assume-role-policy-document file://trust-policy.json

# confirm
aws iam get-role \
  --role-name "$ROLE_NAME" \
  --query "Role.Arn" \
  --output text

# delete if needed
# aws iam delete-role --role-name "$ROLE_NAME"

# ########################################
# 3. Attach IAM Permissions to the Role
# ########################################
# role ARN
ROLE_ARN=$(aws iam get-role --role-name "$ROLE_NAME" --query "Role.Arn" --output text) && echo $ROLE_ARN

# Example: read-only S3 access
aws iam attach-role-policy \
  --role-name "$ROLE_NAME" \
  --policy-arn "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"

# confirm attached policies
aws iam list-attached-role-policies \
  --role-name "$ROLE_NAME"

# detach if needed
# aws iam detach-role-policy \
#   --role-name "$ROLE_NAME" \
#   --policy-arn "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
```

---

## GitHub Configuration

```sh
# ########################################
# GitHub Secrets for AWS OIDC
# ########################################

# AWS IAM Role ARN
ROLE_ARN=$(aws iam get-role \
  --role-name "$ROLE_NAME" \
  --query "Role.Arn" \
  --output text | tr -d '\r' | xargs) && echo $ROLE_ARN

gh secret set AWS_ROLE_ARN --body "$ROLE_ARN"


# AWS Region
AWS_REGION="ca-central-1"

gh secret set AWS_REGION --body "$AWS_REGION"
```

---
