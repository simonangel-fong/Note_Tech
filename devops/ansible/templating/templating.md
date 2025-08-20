# Ansible - Templating

[Back](../ansible.md)

- [Ansible - Templating](#ansible---templating)
  - [Templating](#templating)

---

## Templating

- `templating`

  - dynamically **generating text files** (like configuration files, scripts, or YAML/JSON) **using variables, conditionals, and loops**.

- Ansible uses the Jinja2 templating engine (same as in Flask/Django) to achieve this.

  - extension: `.j2`

- Example

- `nginx.conf.j2`

```config
server {
    listen 80;
    server_name {{ server_name }};

    location / {
        proxy_pass http://{{ backend_host }}:{{ backend_port }};
    }
}
```

- playbook.yaml

```yaml
- hosts: webservers
  vars:
    server_name: mysite.com
    backend_host: 127.0.0.1
    backend_port: 5000

  tasks:
    - name: Deploy nginx configuration
      template:
        src: templates/nginx.conf.j2
        dest: /etc/nginx/nginx.conf
      notify: Restart nginx
```

- Jinja2 Features

```yaml
# Variable substitution
Hello {{ user }}

# Default values:
{{ user | default('guest') }}

# Conditionals:
{% if env == 'prod' %}
DEBUG = False
{% else %}
DEBUG = True
{% endif %}

# Loops:
{% for host in groups['dbservers'] %}
- {{ host }}
{% endfor %}

# Filters
{{ "hello" | upper }}   # Output: HELLO
{{ list | join(", ") }} # Join list into a string

```

- Ansible fileter

```config
{{ "/etc/hosts" | basename }}    # hosts
{{ "c:\windows\hosts" | win_basename }}    # hosts, in windows
{{ "c:\windows\hosts" | win_splitdrive }}    # ["c:","\windows\hosts"]
{{ "c:\windows\hosts" | win_splitdrive | first }}    # "c:"

```
