# Linux - SELinux: Targeted Policy

[Back](../../index.md)

- [Linux - SELinux: Targeted Policy](#linux---selinux-targeted-policy)
  - [Targeted Policy](#targeted-policy)
    - [Confined Processes](#confined-processes)
    - [Unconfined Processes](#unconfined-processes)

---

## Targeted Policy

- `Targeted policy`

  - the **default** SELinux policy used in Red Hat Enterprise Linux.
  - When using targeted policy:
    - **targeted processes** run in a **confined** domain
    - **non-targeted processes** run in an **unconfined** domain.
    - e.g., by default, **logged-in users** run in the `unconfined_t` domain, and **system processes** started by init run in the `initrc_t` domain; both of these domains are **unconfined**.

- `Executable and writable memory checks` may apply to **both** confined and unconfined domains.
  - However, by default, subjects running in an `unconfined domain` **cannot allocate writable memory** and execute it.
    - This reduces vulnerability to buffer overflow attacks.
    - These memory checks are **disabled** by setting `Booleans`, which allow the SELinux policy to be modified at runtime.

---

### Confined Processes

- Almost every **service that listens on a network**, such as `sshd` or `httpd`, is **confined** in Red Hat Enterprise Linux. 
- Most processes that run as the Linux **root user** and **perform tasks for users**, such as the `passwd` application, are **confined**. 
- When a process is **confined**, it **runs in its own domain**, such as the `httpd` process running in the `httpd_t` domain. 
  - If a **confined** process is **compromised** by an attacker, depending on SELinux policy configuration, an attacker's **access** to resources and the possible **damage** they can do is **limited**.


- Confined process requires that SELinux is enabled

---

### Unconfined Processes

- You can **customize the permissions** for confined users in your SELinux policy according to specific needs by **adjusting** `booleans` in the policy.
