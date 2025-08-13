# Terraform - AWS: IAM

[Back](../../index.md)

- [Terraform - AWS: IAM](#terraform---aws-iam)
  - [IAM](#iam)

---

## IAM

- `Identity & Access Management`

  - a service to control access to AWS resources
  - can create:
    - users
    - groups
    - roles

- `User`

  - can authenticate
    - login/password
    - token: MFA
    - access key + secret key

- `group`

  - can be assigned to user
  - can be given privileges
    - attach AWS policies
    - attach custom policies

- `role`

  - assigned to users / services temporary access
  - can be
    - atteched to EC2 instances where a user / service can obtain access credentials.

- `Assume role`

  - grant **temporary credentials** with additional **privileges** to `users` as needed.
  - Example:
    - create a mybucket-access role
    - give read and write permissions
    - attathed to an EC2 instance permission
    - The EC2 instance is given temporary access credentials to access bucket

- `instance profile`
  - a container for an IAM `role` that you can use to pass role information to an EC2 **instance** when the instance starts.
  - Steps:
    - 1. Create role with AssumeRole action and ec2 service
    - 2. Create instance profile with role
    - 3. Attatch instance profile with an EC2 instance
    - 4. Update S3 role policy by defining the created role and resources to allow the role to access the resources.
