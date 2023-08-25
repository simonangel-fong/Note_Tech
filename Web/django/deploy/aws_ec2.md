# Django - Deploy EC2

[Back](../index.md)

- [Django - Deploy EC2](#django---deploy-ec2)
  - [Prerequisite](#prerequisite)
  - [`Ubuntu`: Update](#ubuntu-update)
  - [`ufw`: Firewall](#ufw-firewall)
  - [`git`: Load Django project codes](#git-load-django-project-codes)
  - [`venv`: Virtual Environment](#venv-virtual-environment)
    - [Install packages within venv](#install-packages-within-venv)
    - [Test Django Project](#test-django-project)
    - [Deactivate venv](#deactivate-venv)
  - [`gunicorn`: Python WSGI](#gunicorn-python-wsgi)
    - [Install](#install)
    - [Configuration](#configuration)
    - [Troubleshooting](#troubleshooting)
  - [`nginx`: Server](#nginx-server)
    - [Install](#install-1)
    - [Configuration](#configuration-1)
    - [Troubleshooting](#troubleshooting-1)
  - [`supervisor`: Background](#supervisor-background)
    - [Install](#install-2)
    - [Configuration](#configuration-2)
    - [Troubleshooting](#troubleshooting-2)
  - [Configuration Bash](#configuration-bash)

---

- Good ref:
  - https://dev.to/rmiyazaki6499/deploying-a-production-ready-django-app-on-aws-1pk3#installing-dependencies
  - https://www.youtube.com/watch?v=7O1H9kr1CsA&t=4s
  - https://www.youtube.com/watch?v=PzSUOyshA6k

---

## Prerequisite

- EC2 Instance
  - OS: Ubuntu
  - Security Group:
    - inbound: http, ssh

- Django project on Github, with `requirements.txt`

---

## `Ubuntu`: Update

- Update packages

```sh
# updates the package index files
sudo apt-get update

# upgrades the actual packages installed on system
sudo apt-get upgrade
```

- If any prompt comes up, just press enter.

---

## `ufw`: Firewall

```sh
sudo apt-get install ufw
# Block all incoming and outgoing traffic except ssh 
sudo ufw default allow outgoing
sudo ufw default deny incoming
sudo ufw allow ssh

# while configuring deployment, allow the port 8000 (Django uses this port run the development server)
sudo ufw allow 8000

# enabling ufw 
# make sure to enable ssh before enabling ufw
sudo ufw enable
# Command may disrupt existing ssh connections. Proceed with operation (y|n)? y
# Firewall is active and enabled on system startup
```

---

- After testing

```sh
# after testing
sudo ufw delete allow 8000 
sudo ufw allow http/tcp
sudo ufw allow https/tcp
sudo ufw allow "Nginx HTTPS"
#for status
sudo ufw status

# list which profiles are currently available
sudo ufw app list
```

---

## `git`: Load Django project codes

```sh
git clone github_rep_url
```

---

## `venv`: Virtual Environment

- Creates virtual environment `ve_name` within target directory `target_dir` that has django project codes.

```sh
# install venv
sudo apt-get install python3-venv

# change current dir
cd target_dir

# creates virtual environment
python3 -m venv ve_name

# activates venv
source ve_name/bin/activate
```

---

### Install packages within venv

```sh
# install django within virtual environment
pip install django

# or
pip install -r requirements.txt
```

---

### Test Django Project

```sh
python3 manage.py runserver 0.0.0.0:8000
```

- Visiting public IP with port 8000.

---

### Deactivate venv

```sh
deactivate
```

---


## `gunicorn`: Python WSGI

- `gunicorn`
  - a Python WSGI HTTP Server for UNIX.
  - Gunicorn establishes connection between Django Application and Website within the Linux server. 

---

### Install

```sh
# install gunicorn using venv
pip install gunicorn
```

- 该处是pip, 不是pip3. 因为是在虚拟环境中.

---

### Configuration

- `gunicorn.socket`

```sh
sudo nano /etc/systemd/system/gunicorn.socket

```

```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

---

- `gunicorn.service`

```sh
sudo nano /etc/systemd/system/gunicorn.service
```

- `<user_name>`: OS username
- `<django_proj_path>`: path of django project, not container, starting from home
  - 是manage.py所在的文件夹, 是否以斜杠结束都可以.
- `<venv_path>`: path of virtual environment, staring from home
  - 是虚拟环境的文件夹
- `<django_proj_name>`: name of django project, not path.

```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=<user_name>
Group=www-data 
WorkingDirectory=<django_proj_path>
ExecStart=<venv_path>/bin/gunicorn \
--access-logfile - \
--workers 3 \
--bind unix:/run/gunicorn.sock \
<django_proj_name>.wsgi:application

[Install]
WantedBy=multi-user.target
```

---

- Apply configuration

```sh
# Start gunicorn
sudo systemctl start gunicorn.socket

# enable on boots
sudo systemctl enable gunicorn.socket
# Created symlink /etc/systemd/system/sockets.target.wants/gunicorn.socket → /etc/systemd/system/gunicorn.socket.

# check status
sudo systemctl status gunicorn.socket
# ● gunicorn.socket - gunicorn socket
#      Loaded: loaded (/etc/systemd/system/gunicorn.socket; enabled; vendor preset: enabled)
#      Active: active (running) since Fri 2023-08-18 00:53:27 UTC; 19min ago
#    Triggers: ● gunicorn.service
#      Listen: /run/gunicorn.sock (Stream)
#      CGroup: /system.slice/gunicorn.socket

# verify gunicorn.sock is created
file /run/gunicorn.sock
# /run/gunicorn.sock: socket
```

---

- Test gunicorn.service

```sh
curl --unix-socket /run/gunicorn.sock localhost
# will return the html code of index page
# ● gunicorn.socket - gunicorn socket
#      Loaded: loaded (/etc/systemd/system/gunicorn.socket; enabled; vendor preset: enabled)
#      Active: active (running) since Fri 2023-08-18 00:53:27 UTC; 19min ago
#    Triggers: ● gunicorn.service
#      Listen: /run/gunicorn.sock (Stream)
#      CGroup: /system.slice/gunicorn.socket

# Aug 18 00:53:27 ip-172-31-40-195 systemd[1]: Listening on gunicorn socket.
# (env) ubuntu@ip-172-31-40-195:~/deployment$ ^C
# (env) ubuntu@ip-172-31-40-195:~/deployment$ curl --unix-socket /run/gunicorn.sock localhost
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Ttest</title>
# </head>
# <body>
#     Test
# </body>


# re-check status
sudo systemctl status gunicorn
# ● gunicorn.service - gunicorn daemon
#      Loaded: loaded (/etc/systemd/system/gunicorn.service; disabled; vendor preset: enabled)
#      Active: active (running) since Fri 2023-08-18 01:12:42 UTC; 3min 16s ago
# TriggeredBy: ● gunicorn.socket
#    Main PID: 20742 (gunicorn)
#       Tasks: 4 (limit: 1141)
#      Memory: 86.4M
#         CPU: 773ms
#      CGroup: /system.slice/gunicorn.service
#              ├─20742 /home/ubuntu/deployment/env/bin/python3 /home/ubuntu/deployment/env/bin/gunicorn --access-logfile - --workers 3 --bind unix:>
#              ├─20743 /home/ubuntu/deployment/env/bin/python3 /home/ubuntu/deployment/env/bin/gunicorn --access-logfile - --workers 3 --bind unix:>
#              ├─20744 /home/ubuntu/deployment/env/bin/python3 /home/ubuntu/deployment/env/bin/gunicorn --access-logfile - --workers 3 --bind unix:>
#              └─20745 /home/ubuntu/deployment/env/bin/python3 /home/ubuntu/deployment/env/bin/gunicorn --access-logfile - --workers 3 --bind unix:>

# Aug 18 01:12:42 ip-172-31-40-195 systemd[1]: Started gunicorn daemon.
# Aug 18 01:12:42 ip-172-31-40-195 gunicorn[20742]: [2023-08-18 01:12:42 +0000] [20742] [INFO] Starting gunicorn 21.2.0
# Aug 18 01:12:42 ip-172-31-40-195 gunicorn[20742]: [2023-08-18 01:12:42 +0000] [20742] [INFO] Listening at: unix:/run/gunicorn.sock (20742)
# Aug 18 01:12:42 ip-172-31-40-195 gunicorn[20742]: [2023-08-18 01:12:42 +0000] [20742] [INFO] Using worker: sync
# Aug 18 01:12:42 ip-172-31-40-195 gunicorn[20743]: [2023-08-18 01:12:42 +0000] [20743] [INFO] Booting worker with pid: 20743
```

---

### Troubleshooting

```sh
# return log 
sudo journalctl -u gunicorn.socket

# edit configuration
nano /etc/supervisor/conf.d/gunicorn.conf

# restart after fixed
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo systemctl status gunicorn.socket
```

---

## `nginx`: Server

- `nginx`
  - an open-source web server software used for reverse proxy, load balancing, and caching. 

---

### Install

```sh
# install nginx
sudo apt-get install nginx
```

- Verify: 
  - Visits the public IP of EC2 using `http`, Ngix welcome page will display.
  - `https` might not work due to configuration of EC2's Security Group or require additional package.
  
---

### Configuration

- `nginx.conf`

```sh
# modify nginx.conf
sudo nano /etc/nginx/nginx.conf
```

```sh
# Change user as root, so that prevent issues caused by permission deny errors.
# can be the name of user.
user root;
```

---

- `.conf`

```sh
# proj_name_conf: a file for current project with configuration of nginx 
sudo nano /etc/nginx/sites-available/proj_name_conf
```

- `<ip_address>`: AWS public IP or domain name
- `<django_proj_path>`: path of django project, starting from home
- `proxy_pass`: the path where settings.py locates.

```
server {
  listen 80;
  server_name <ip_address>;
  location = /favicon.ico { access_log off; log_not_found off; }
  location /static/ {
    root <django_proj_path>;
  }

  location /media/ {
    root <django_proj_path>;    
  }

  location / {
    include proxy_params;
    proxy_pass http://unix:/run/gunicorn.sock;
  }
}

```

---

- create a link of `.conf` file to `/etc/nginx/sites-enabled`

```sh
# create a link of `.conf` file to `/etc/nginx/sites-enabled`
sudo ln -sf /etc/nginx/sites-available/django.conf /etc/nginx/sites-enabled
```

---

- Test configuration and Restart Nginx service

```sh
# test syntax
sudo nginx -t
# nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
# nginx: configuration file /etc/nginx/nginx.conf test is successful

# restart nginx
sudo systemctl restart nginx

```

---

### Troubleshooting

```sh
# status
systemctl status nginx

# error log
nano /var/log/nginx/error.log
sudo tail -30 /var/log/nginx/error.log

# nginx configuration
nano /etc/nginx/sites-available/django.conf

# syntax test
sudo nginx -t

# restart service
sudo service nginx restart


sudo systemctl reload nginx


systemctl status nginx
```

---

## `supervisor`: Background

- `supervisor`
  - allow application run in the background.

---

### Install 

```sh
# install supervisor
sudo apt-get install supervisor
```

---

### Configuration

- Configuration of `gunicorn.conf` file
  - `proj_name`: name of project dir

```sh
# Creates log dir for logging
sudo mkdir /var/log/gunicorn

# Configures supervisor by creating gunicorn.conf
sudo nano /etc/supervisor/conf.d/gunicorn.conf
```

---

- `gunicorn.conf` file:
  - `<django_proj_path>`: the path of django project, starting from `/home`
  - `<venv_path>`: the path of venv, starting from `/home`
  - `<django_proj_name>`: the name of django project

```
[program:gunicorn]
    directory=<django_proj_path>
    command=<venv_path>/bin/gunicorn --workers 3 --bind unix:/run/gunicorn.sock  <django_proj_name>.wsgi:application
    autostart=true
    autorestart=true
    stderr_logfile=/var/log/gunicorn/gunicorn.err.log
    stdout_logfile=/var/log/gunicorn/gunicorn.out.log

[group:guni]
    programs:gunicorn
```

---

- Update supervisor configuration

```sh
# tell supervisor read configuration file
sudo supervisorctl reread    # guni: available

# update supervisor configuration
sudo supervisorctl update    # guni: added process group

# verify configuration status
sudo supervisorctl status    # guni:gunicorn                    RUNNING   pid 18586, uptime 0:01:13
```

---

### Troubleshooting

```sh
# error log
sudo nano /var/log/gunicorn/gunicorn.err.log

# edit configuration
sudo nano /etc/supervisor/conf.d/gunicorn.conf
```

---

## Configuration Bash

```sh
#!/bin/bash
#Program Name: deploy_conf_script.sh
#Author name: Wenhao Fang
#Date Created: Aug 23rd 2023
#Date updated:
#Description of the script: Configuration for deployment.

github_url=''

# Updates OS
sudo apt-get update   # update the package on Linux system. 
sudo apt-get upgrade  # downloads and installs the updates for each outdated package and dependency

# Firewall
sudo apt-get install ufw          # install firewall
sudo ufw default allow outgoing   # Allow outgoing traffic
sudo ufw default deny incoming    # Deny all incoming traffic
sudo ufw allow ssh                # Allow ssh traffic
sudo ufw allow 8000               # Allow the port 8000, the port to test django while configuring deployment
sudo ufw enable                   # Enables firewall

# Download codes from github
if [ $github_url="" ];then
        echo 'dsdsdsds'
fi
git clone github_rep_url

```

---

[TOP](#django---deploy-ec2)