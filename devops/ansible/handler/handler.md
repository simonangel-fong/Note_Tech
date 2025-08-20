# Ansible - Handler

[Back](../ansible.md)

---

## Handler

- `handler`
  - a **special** kind of task that **runs only when it is explicitly notified by another task**.
  - Handlers are typically used for actions that should happen only when a change occurs, such as restarting a service after a configuration file is updated.
  - help create dependency between tasks.
  - trigger the task by events/notification
- Example

```yaml
- name: Deploy Application
  hosts: application_servers
  tasks:
    - name: Copy Application Code
      copy:
        src: app_code/
        dest: /opt/application/
      notify: Restart Application Service # notify the handler

  handlers:
    - name: Restart Application Service
      service:
        name: application_service
        state: restarted
```
