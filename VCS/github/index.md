# GitHub

[All Notes](../../index.md)

- GitHub Action
  - [Copy Direcotry to a remote repository](./github_action/lab_copy_repo.md)

---

## OIDC with AWS

- Ref:

  - https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws

- IAM
  - Identity providers
  - Create provider
    - Provider URL: `https://token.actions.githubusercontent.com`
    - Audience: `sts.amazonaws.com` if you are using the official action.

---

### Create AWS IAM role

- `GitHubActionRole-*`
  - `ACCOUNT_ID`
  - `USER_NAME`: GitHub user
  - `REPO_NAME`: Repo name

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::<ACCOUNT_ID>:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:USER_NAME/REPO_NAME:*"
        }
      }
    }
  ]
}
```

---

### Add Policy

- AmazonVPCFullAccess

- Add inline policy for S3 bucket backend
  - `BUCKET`: bucket name
  - `KEY_PREFIX`: S3 bucket key

```json
{
  "Version": "2012-10-17",
  "Statement": [
    /* --- S3: state bucket --- */
    {
      "Sid": "S3ListBucket",
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket",
        "s3:GetBucketLocation",
        "s3:ListBucketMultipartUploads"
      ],
      "Resource": "arn:aws:s3:::<BUCKET>",
      "Condition": {
        "StringLike": {
          "s3:prefix": ["<KEY_PREFIX>/*", "<KEY_PREFIX>"]
        }
      }
    },
    {
      "Sid": "S3ObjectRW",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:GetObjectVersion",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:AbortMultipartUpload",
        "s3:ListMultipartUploadParts"
      ],
      "Resource": "arn:aws:s3:::<BUCKET>/<KEY_PREFIX>/*"
    }
  ]
}
```

---

### GitHub Actions Step

- `AWS_TF_ROLE_ARN`: the arn of OIDC role

```yaml
- name: Configure AWS credentials (OIDC)
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: ${{ secrets.AWS_TF_ROLE_ARN }}
    aws-region: ${{ env.TF_VAR_region }}
```
