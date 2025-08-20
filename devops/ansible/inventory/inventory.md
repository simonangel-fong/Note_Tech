# Ansible - Inventory

[Back](../ansible.md)

- [Ansible - Inventory](#ansible---inventory)
  - [Inventory](#inventory)
    - [Inventory Files](#inventory-files)
    - [Parent and Child relationship](#parent-and-child-relationship)
      - [`yaml` file](#yaml-file)

---

## Inventory

- `inventory`

  - a file or directory that defines the hosts (servers, devices, etc.) that Ansible manages, and how they are organized into groups.
  - enable agentless connections.

- Connections can be built:

  - Linux: SSH
  - Windows: Powershell Remoting

- It defines:

  - `Hosts`: individual systems (by name or IP).
  - `Groups`: logical collections of hosts (e.g., webservers, dbservers).
  - `Variables`: connection details, credentials, or custom settings per host/group.

- Ansible parameter for connection
  - `ansible_host=server1.company.com`: specify the FQDN or IP address of a server.
  - `ansible_connection=ssh/vinrm/localhost`: specify the connection
  - `ansible_port=22`: specify the connection port
  - `ansible_user=root`: specify the connection user
  - `ansible_ssh_pass=pwd`: specify the connection password

---

### Inventory Files

- Default inventory file

  - `/etc/ansible/hosts`

- Group by:

  - [GROUP_NAME]

- Can be in `INI` or `YAML` format.

### Parent and Child relationship

- common configuration can be applied to parent group level
- specific configuration can be applied to children group level

- Parent and child semantic

- ini file

```ini
[webservers:children]
webservers_us
webservers_eu

[webservers_us]
server1_us.com ansible_host=192.168.8.101
server2_us.com ansible_host=192.168.8.102

[webservers_eu]
server1_eu.com ansible_host=10.12.0.101
server2_eu.com ansible_host=10.12.0.102
```

- yaml file

```yaml
all:
  children:
    webservers:
      children:
        webservers_us:
          hosts:
            server1_us.com:
              ansible_host: 192.168.8.101
            server2_us.com:
              ansible_host: 192.168.8.102
        webservers_eu:
          hosts:
            server1_eu.com:
              ansible_host: 10.12.0.101
            server2_eu.com:
              ansible_host: 10.12.0.102
```

````

---

#### `ini` file

```ini
[webservers]
web1 ansible_host=192.168.1.10 ansible_user=ubuntu
web2 ansible_host=192.168.1.11 ansible_user=ubuntu

[dbservers]
db1 ansible_host=192.168.1.20 ansible_user=postgres
````

---

- Example:
  - using alias and parameters

```ini
# define hosts

# define a alias, host, connection method, and password
web ansible_host=server1.company.com ansible_connection=ssh ansible_user=root
db ansible_host=server2.company.com ansible_connection=winrm ansible_user=admin ansible_password=P@#
mail ansible_host=server3.company.com ansible_connection=ssh ansible_ssh_pass=P@#
web2 ansible_host=server4.company.com ansible_connection=winrm

# define connection with localhost
localhost ansible_connection=localhost

# grouping
[webservers]
web
web2
localhost

[dbservers]
db

# group of group
[all_servers:children]
webservers
dbservers
```

---

#### `yaml` file

- can be used for complex structures

```yaml
all:
  children:
    webservers:
      hosts:
        web1.example.com:
        web2.example.com:
    dbservers:
      hosts:
        db1.example.com:
        db2.example.com:
```
