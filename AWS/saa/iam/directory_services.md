# AWS - Directory Services

[Back](../index.md)

- [AWS - Directory Services](#aws---directory-services)
  - [`Microsoft Active Directory (AD)`](#microsoft-active-directory-ad)
  - [`AWS Directory Services`](#aws-directory-services)
    - [Types of Directory Services](#types-of-directory-services)
    - [Integrate with IAM Identity Center](#integrate-with-iam-identity-center)
    - [Hands-on](#hands-on)

---

## `Microsoft Active Directory (AD)`

- Found on any `Windows Server` with `AD Domain Services`
- **Database of objects**:
  - User Accounts, Computers, Printers, File Shares, Security Groups
- Centralized security management, create account, assign permissions
- Objects are **organized in `trees`**
- A group of `trees` is a `forest`

![win_ad_diagram](./pic/win_ad_diagram.png)

---

## `AWS Directory Services`

- `AWS Directory Services`

  - allow Windows ec2 instance to join the domain controllers for your network and share all the logins, credentials, and so on.
  - A directory in AWS make it closer to ec2 instances running windows.

---

### Types of Directory Services

- `AWS Managed Microsoft AD`

  - Create your own AD in AWS, manage **users locally**, supports MFA
  - Establish “trust” **connections** with your **on-premises AD**
  - On-premises 或 Directory Services 任何一方认证即可访问另一方资源.

![directory_service_managed_microsoft_ad](./pic/directory_service_managed_microsoft_ad.png)

- `AD Connector`

  - `Directory Gateway` (proxy) to **redirect** to on-premises AD supports MFA
  - **Users** are solely **managed on the on-premises AD**
  - connector is just proxy, all users are managed on the on-premises AD.

![directory_service_ad_connector](./pic/directory_service_ad_connector.png)

- `Simple AD`
  - AD-compatible managed directory **on AWS**
  - **Cannot be joined** with **on-premises** AD
  - no on-premises AD

![directory_service_simple_ad](./pic/directory_service_simple_ad.png)

---

### Integrate with IAM Identity Center

- `IAM Identity Center` connect to an `AWS Managed Microsoft AD (Directory Service)`
  - Integration is **out of the box**

![directory_service_identity_center](./pic/directory_service_identity_center.png)

- `IAM Identity Center` connect to a **Self-Managed Directory**
  - 2 ways to build integration:
    - Create **Two-way Trust Relationship** using` AWS Managed Microsoft AD`
    - Create an `AD Connector`

![directory_service_identity_center_selfmanaged](./pic/directory_service_identity_center_selfmanaged.png)

---

### Hands-on

![directory_service_handson01](./pic/directory_service_handson01.png)

![directory_service_handson01](./pic/directory_service_handson02.png)

---

[TOP](#aws---directory-services)
