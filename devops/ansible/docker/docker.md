# Ansible - with Docker

[Back](../ansible.md)

- [Ansible - with Docker](#ansible---with-docker)
  - [Docker](#docker)

---

## Docker

```yaml
# demo_create_nginx_container.yaml
---
- name: Create nginx container using local Docker
  hosts: localhost
  connection: local
  gather_facts: false

  tasks:
    - name: Pull nginx image
      community.docker.docker_image:
        name: nginx
        source: pull

    - name: Create and start nginx container
      community.docker.docker_container:
        name: ansible-nginx
        image: nginx
        state: started
        restart_policy: unless-stopped
        published_ports:
          - "8080:80"
```

```sh
ansible-playbook demo_create_nginx_container.yaml
# PLAY [Create nginx container using local Docker] ***********************************************************************************************

# TASK [Pull nginx image] ************************************************************************************************************************
# ok: [localhost]

# TASK [Create and start nginx container] ********************************************************************************************************
# changed: [localhost]

# PLAY RECAP *************************************************************************************************************************************
# localhost                  : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

docker ps
# CONTAINER ID   IMAGE                                  COMMAND                  CREATED              STATUS              PORTS                                                                                  NAMES
# 5ad500fe3b42   nginx                                  "/docker-entrypoint.…"   About a minute ago   Up About a minute   0.0.0.0:8080->80/tcp                                                                   ansible-nginx
```

---

```yaml
# delete-nginx-container.yml
---
- name: Delete nginx container
  hosts: localhost
  connection: local
  gather_facts: false

  tasks:
    - name: Stop and remove nginx container
      community.docker.docker_container:
        name: ansible-nginx
        state: absent
```

```sh
ansible-playbook delete-nginx-container.yml
# PLAY [Delete nginx container] ******************************************************************************************************************

# TASK [Stop and remove nginx container] *********************************************************************************************************
# changed: [localhost]

# PLAY RECAP *************************************************************************************************************************************
# localhost                  : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

docker ps
# CONTAINER ID   IMAGE                                  COMMAND                  CREATED      STATUS          PORTS                                                                                  NAMES
```
