# AWS - Systems Manager(SSM)

[Back](../index.md)

- [AWS - Systems Manager(SSM)](#aws---systems-managerssm)
  - [`AWS Systems Manager`](#aws-systems-manager)
    - [Parameter Store](#parameter-store)
    - [Standard and advanced parameter tiers](#standard-and-advanced-parameter-tiers)
    - [Parameters Policies](#parameters-policies)
  - [Hands-on](#hands-on)
  - [Hands-on: integrate with lambda](#hands-on-integrate-with-lambda)

---

## `AWS Systems Manager`

- `AWS Systems Manager`

  - formerly known as "Amazon Simple Systems Manager (SSM)" and "Amazon EC2 Systems Manager (SSM)"
  - **View operational data** for groups of resources, so you can quickly identify and act on any **issues** that might impact applications that use those resources.

---

### Parameter Store

- `AWS Systems Manager Parameter Store` / `SSM Parameter Store`

  - Centralized storage and management of your **secrets** and **configuration** data such as passwords, database strings, and license codes.
  - You can **encrypt** values, or store as **plain text**, and secure **access** at every level.

- **Features**:

  - **Version** tracking of configurations / secrets
  - Serverless, scalable, durable, easy SDK

- **Integration**:
  - Optional Seamless **Encryption** using `KMS`
  - **Security** through `IAM`
  - **Notifications** with Amazon `EventBridge`
  - **Integration** with `CloudFormation`

![ssm_parameter_store](./pic/ssm_parameter_store.png)

- Sample:
  - You have a secret value that you use for encryption purposes, and you want to **store and track the value**s of this secret over time. Which AWS service should you use?
    - **SSM Parameters Store** can be used to **store secrets and has built-in version tracking** capability. Each time you edit the value of a parameter, SSM Parameter Store creates a new version of the parameter and retains the previous versions. You can view the details, including the values, of all versions in a parameter's history.
  - You would like to externally maintain the **configuration values** of your main database, to be picked up at runtime by your application. What's the best place to store them to maintain control and **version history**?
    - SSM Parameters Store

---

- Hierarchy

![ssm_parameter_store_hierarchy](./pic/ssm_parameter_store_hierarchy.png)

---

### Standard and advanced parameter tiers

![ssm_parameter_tiers](./pic/ssm_parameter_tiers.png)

---

### Parameters Policies

- for advanced parameters
- Allow to assign a `TTL` to a parameter (`expiration date`) to **force updating or deleting** sensitive data such as passwords
- Can assign **multiple policies** at a time

![ssm_parameter_policies](./pic/ssm_parameter_policies.png)

---

## Hands-on

- String parameter
  ![ssm_parameter_store_handson01](./pic/ssm_parameter_store_handson01.png)

![ssm_parameter_store_handson01](./pic/ssm_parameter_store_handson02.png)

![ssm_parameter_store_handson01](./pic/ssm_parameter_store_handson03.png)

- Security string

![ssm_parameter_store_handson01](./pic/ssm_parameter_store_handson04.png)

![ssm_parameter_store_handson01](./pic/ssm_parameter_store_handson05.png)

![ssm_parameter_store_handson01](./pic/ssm_parameter_store_handson06.png)

![ssm_parameter_store_handson01](./pic/ssm_parameter_store_handson07.png)

![ssm_parameter_store_handson01](./pic/ssm_parameter_store_handson08.png)

- Get parameter using CLI

```sh
aws ssm get-parameters --names /my-app/dev-pwd /my-app/dev-url
```

![ssm_parameter_store_handson01](./pic/ssm_parameter_store_handson09.png)

- Decrype parameter

```sh
# GET PARAMETERS WITH DECRYPTION
aws ssm get-parameters --names /my-app/dev-pwd /my-app/dev-url --with-decryption
```

![ssm_parameter_store_handson10](./pic/ssm_parameter_store_handson10.png)

- Get parameters by path

```sh
# GET PARAMETERS BY PATH
aws ssm get-parameters-by-path --path /my-app/dev/
```

![ssm_parameter_store_handson10](./pic/ssm_parameter_store_handson11.png)

- Get by path recursively and decryption

```sh
# GET PARAMETERS BY PATH WITH DECRYPTION
aws ssm get-parameters-by-path --path /my-app/ --recursive --with-decryption
```

![ssm_parameter_store_handson10](./pic/ssm_parameter_store_handson12.png)

---

## Hands-on: integrate with lambda

![ssm_parameter_store_handson10](./pic/ssm_parameter_store_handson13.png)

![ssm_parameter_store_handson10](./pic/ssm_parameter_store_handson14.png)

- function code:

```py
import json
import boto3
import os

ssm = boto3.client('ssm', region_name="us-east-1")
app_name = os.environ['APP_NAME']

def lambda_handler(event, context):
    db_url = ssm.get_parameters(Names=[app_name + "/dev-url"])
    print(db_url)
    db_password = ssm.get_parameters(Names=[app_name + "/dev_pwd"], WithDecryption=True)
    print(db_password)
    return "worked!"
```

- Add environment variables

![ssm_parameter_store_handson10](./pic/ssm_parameter_store_handson23.png)

- Edit role: access to SSM

![ssm_parameter_store_handson10](./pic/ssm_parameter_store_handson15.png)

![ssm_parameter_store_handson10](./pic/ssm_parameter_store_handson16.png)

![ssm_parameter_store_handson10](./pic/ssm_parameter_store_handson17.png)

![ssm_parameter_store_handson10](./pic/ssm_parameter_store_handson18.png)

![ssm_parameter_store_handson10](./pic/ssm_parameter_store_handson19.png)

![ssm_parameter_store_handson10](./pic/ssm_parameter_store_handson20.png)

- Test

![ssm_parameter_store_handson10](./pic/ssm_parameter_store_handson24.png)

- Edit role: (skip this step)
  - access to KMS for decryption if using Customer managed keys

![ssm_parameter_store_handson10](./pic/ssm_parameter_store_handson21.png)

![ssm_parameter_store_handson10](./pic/ssm_parameter_store_handson22.png)

---
