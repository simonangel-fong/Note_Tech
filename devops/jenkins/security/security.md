# Jenkins - Security

[Back](../index.md)

- [Jenkins - Security](#jenkins---security)
  - [Good Practices](#good-practices)
  - [Role-based Authorization Strategy](#role-based-authorization-strategy)
  - [Lab: Manage Users with RBAS](#lab-manage-users-with-rbas)

---

## Good Practices

- **User login**
  - Disable allow users sign up
  - Authorization:
    - disable **allow anonymous read access**: users who are not authenticated to access Jenkins in a read-only mode.

- **Secure Jenkins Controller**
  - set the number of executors on the built-in node to 0
    - `built-in node`: Jenkins controller itself — the machine where Jenkins is running.
    - Do NOT run any build jobs on the controller node.

---

## Role-based Authorization Strategy

- **Install Plugins**
  - `Role-based Authorization Strategy`: Enables user authorization using a Role-Based strategy.
    - enable: security > Authorization = Role-Based Strategy
    - Manage Jenkins > Security > Manage and Assign Roles

    ![pic](./pic/rbas01.png)

- `role`:
  - a set of permission to be granted

---

## Lab: Manage Users with RBAS

- Create new user and login
  - Access Denied, bob is missing the Overall/Read permission

![pic](./pic/rbas02.png)

- Create read-only role

![pic](./pic/rbas_role_create.png)

- Assign Role

![pic](./pic/rbas_role_assign01.png)

- re-login

![pic](./pic/rbas_role_assign02.png)

- Add permission: read job

![pic](./pic/rbas_role_assign03.png)

- re-login

![pic](./pic/rbas_role_assign04.png)

---

- Create new role: run-job

![pic](./pic/rbas_role_assign05.png)

![pic](./pic/rbas_role_assign06.png)

![pic](./pic/rbas_role_assign07.png)

---

- Global roles: dev
  - overall: read
  - job: read

![pic](./pic/rbas_role_assign08.png)

- Item roles: 1st
  - pattern: 1st.\*

![pic](./pic/rbas_role_assign09.png)

- Assign

![pic](./pic/rbas_role_assign10.png)

- re-login
  - 1st-\*: can see and run
  - docker\*: can see only

![pic](./pic/rbas_role_assign11.png)
