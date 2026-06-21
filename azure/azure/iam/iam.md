# Azure: IAM

[Back](../index.md)

- [Azure: IAM](#azure-iam)
  - [IAM](#iam)
  - [Authentication \& Authorization](#authentication--authorization)
  - [Entra ID](#entra-id)
  - [RABC](#rabc)
  - [Zero Trust security model](#zero-trust-security-model)

---

## IAM

- `Identity`:
  - a representation of a person, application, or device.

- Identity management system:
  - `Entra ID` (extended `Active Directory`)

---

## Authentication & Authorization

- `authentication`:
  - the process of **verifying** the `identity` of a user, device, or application attempting to **access** Microsoft Azure cloud resources.
  - password, certificate, MFA

- `authorization`:
  - the process that **determines** what an authenticated user, application, or device is **allowed to do**.
  - Once you prove who you are (authentication),

---

## Entra ID

- `Active Directory (AD)`
  - Microsoft's **directory service** for Windows domain networks.
  - acts as a centralized, hierarchical database that securely stores and manages critical IT resources.
  - protocols:
    - `LDAP`
    - `Kerberos`

---

- `Entra ID`
  - formerly known as `Azure Active Directory`
  - Microsoft’s cloud-based Identity and Access Management (IAM) service.
  - protocols:
    - `SAML` and `Oauth`

- `Single Sign-On(SSO)`
  - an **authentication method** that allows users to **log in with a single set** of credentials (like a username and password) to **access multiple**, independent software systems or applications.

- `Multi-Factor Authentication (MFA)`:
  - a **security process** where a user provides two or more different **verification factors** to gain access to an account or system.
  - factors:
    - evidence that is only owned by a user privately.
    - username is not a factor
    - common:
      - mobile phone: SMS, authentication app
      - fingerprint, face scan

---

## RABC

- `Principle of Least Privilege (PoLP)`
  - a core cybersecurity concept stating that any user, program, or process **must only have the minimum access rights** necessary to perform its job, and nothing more.

- `Azure RBAC (Role-Based Access Control)`
  - a security system that manages who can access your cloud resources and what they are allowed to do with them.
  - enforces the `principle of least privilege` by ensuring users only get the permissions strictly necessary to perform their jobs.

- three core elements:
  - `Security Principal`:
    - Who gets the access (a user, a group, a service principal, or a managed identity).
  - `Role Definition`:
    - What they can do (a set of allowed or denied actions, such as "Read", "Write", or "Delete").
  - `Scope`:
    - Where the access applies.
    - e.g., `Management Group`, `Subscription`, `Resource Group` or individual `resource`.

- **Built-in Roles**
  - `Owner`:
    - **Full access** to manage everything, including **granting** access to others.
  - `Contributor`:
    - Full access to **create and manage** Azure resources, but **cannot assign** roles to others.
  - `Reader`:
    - Can **only view** existing Azure resources but cannot make any changes.
  - Specific Resource Roles:
    - Roles **tailored** to certain tasks (e.g., Virtual Machine Contributor or Storage Blob Data Reader).

---

## Zero Trust security model

- `Zero Trust security model`
  - a framework based on the principle: "Never trust, always verify."
  - Instead of assuming everyone inside a corporate network is safe, it **treats** every user, device, and connection **as untrusted by default**, requiring continuous verification to access resources.

- three core pillars:
  - **Verify Explicitly**:
    - Every **access request** is authenticated and authorized using all available data points (identity, device health, location, and workload context).
  - **Use Least Privilege**:
    - Users and workloads are only given the **exact permissions** they need to do their job, and only for the shortest time required.
  - **Assume Breach**:
    - Security is designed with the expectation that attackers will eventually infiltrate the environment.
    - It **limits the "blast radius"** by segmenting networks so attackers cannot move laterally.

---

- core operational mechanisms that enforce Zero Trust security:
  - `Just-Enough Access (JEA)`
    - a security model grants users or systems the absolute **minimum permissions required** to perform a specific task, and nothing more.
    - It ensures a smaller security footprint (or "blast radius") so that compromised accounts can't cause widespread damage.

  - `Just-in-Time (JIT)`
    - a security model that grants users or applications **elevated permissions only when** strictly necessary, and automatically **revokes them immediately after** the task is completed.
    - eliminates "standing privileges" (always-on administrative rights), significantly reducing the window of opportunity for cybercriminals.
