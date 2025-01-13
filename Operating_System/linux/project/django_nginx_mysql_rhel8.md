# Web Application - Django-Nginx-MySQL-RHEL8

[Back](../index.md)

- [Web Application - Django-Nginx-MySQL-RHEL8](#web-application---django-nginx-mysql-rhel8)
  - [Install Server Software](#install-server-software)
  - [Install MySQL Database](#install-mysql-database)
  - [Create Django Project](#create-django-project)
  - [Configure Gunicorn](#configure-gunicorn)
  - [Configure Nginx](#configure-nginx)
  - [Setup Cloudflare tunne](#setup-cloudflare-tunne)

---

## Install Server Software

```sh
dnf upgrade -y
dnf install nginx

systemctl enable --now nginx
systemctl status nginx
```

---

## Install MySQL Database

```sh
dnf install -y mysql-community-server
systemctl enable --now mysqld
systemctl status mysqld
```

---

## Create Django Project

- For security, create a user dedicated to the django project

```sh
useradd django_demo_admin
passwd django_demo_admin
```

- Create hello world Django project

```sh
mkdir -p /home/django_demo_admin/app

# create venv
python3 -m venv /home/django_demo_admin/app/.env
source /home/django_demo_admin/app/.env/bin/activate

# install django
pip install django
# create django project
django-admin startproject hello_world /home/django_demo_admin/app/
# test
python3 /home/django_demo_admin/app//manage.py runserver 8000
```

- Update view

```sh
cat > /home/django_demo_admin/app/hello_world/views.py <<EOF
from django.views.generic.base import TemplateView

# View of home page
class HomeView(TemplateView):
    template_name = "index.html"     # the template of this view
    extra_context = {'title': "Django-Hello World"}    # the title of HTML
EOF
```

- Update URLs

```sh
cat > /home/django_demo_admin/app/hello_world/urls.py <<EOF
from django.contrib import admin
from django.urls import path
from .views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),    # Define home url
    path('admin/', admin.site.urls),     # define admin url
]
EOF
```

- Create html

```sh
mkdir -p /home/django_demo_admin/app/templates
cat > /home/django_demo_admin/app/templates/index.html <<EOF
<!DOCTYPE html>
<html>
<head>
<title>{{title}}</title>
</head>
<body>

<h1>Django Hello world</h1>
<p>This is a test page.</p>

</body>
</html>
EOF
```

- update configure for template

```sh
mkdir -p /home/django_demo_admin/app/static/

vi /home/django_demo_admin/app/hello_world/settings.py
# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [Path(BASE_DIR, 'templates'),],    # define project level template
#         'APP_DIRS': True,  # By default, templates are manged at App Level
#     },
# # ...
# ]

# # Static files (CSS, JavaScript, images)
# # URL referring to static files
# STATIC_URL = '/static/'
# # project level static
# STATICFILES_DIRS = [BASE_DIR / 'static', ]
# # absolute path to the directory for deployment
# STATIC_ROOT = Path(BASE_DIR, 'collectstatic')

# ALLOWED_HOSTS = ['<server-ip>', 'localhost']
```

- Collect static files

```sh
python3 /home/django_demo_admin/app/manage.py collectstatic
# 128 static files copied to '/home/django_demo_admin/app/collectstatic'.
```

- Test locally

```sh
python3 /home/django_demo_admin/app/manage.py runserver 8000
```

- Database Migration

```sh
python3 /home/django_demo_admin/app/manage.py makemigrations
python3 /home/django_demo_admin/app/manage.py migrate
```

- Create super user

```sh
python3 /home/django_demo_admin/app/manage.py createsuperuser
```

- Change ownership of the project dir

```sh
chown django_demo_admin:django_demo_admin -R /home/django_demo_admin/app
```

---

## Configure Gunicorn

```sh
# install
source /home/django_demo_admin/app/.env/bin/activate
pip install gunicorn

# test
# move to manage.py dir
cd /home/django_demo_admin/app
# Access the server at http://<server-ip>:8000. If it works, proceed to create a Gunicorn systemd service.
gunicorn --bind 0.0.0.0:8000 hello_world1.wsgi
# [2025-01-12 22:34:46 -0500] [24445] [INFO] Starting gunicorn 21.2.0
# [2025-01-12 22:34:46 -0500] [24445] [INFO] Listening at: http://0.0.0.0:8000 (24445)
# [2025-01-12 22:34:46 -0500] [24445] [INFO] Using worker: sync
# [2025-01-12 22:34:46 -0500] [24448] [INFO] Booting worker with pid: 24448
```

- Create gunicorn server cf

```sh
# Create a Gunicorn service file
cat > /etc/systemd/system/gunicorn.service << EOF
[Unit]
Description=gunicorn daemon for Django Hello World
After=network.target

[Service]
User=django_demo_admin
Group=django_demo_admin
WorkingDirectory=/home/django_demo_admin/app/
ExecStart=/home/django_demo_admin/app/.env/bin/gunicorn \
  --workers 3 \
  --bind unix:/home/django_demo_admin/app/hello_world.sock hello_world.wsgi

[Install]
WantedBy=multi-user.target
EOF
```

- Reload systemd, start, and enable Gunicorn:

```sh
systemctl daemon-reload
systemctl start gunicorn
systemctl enable gunicorn
systemctl status gunicorn
```

---

## Configure Nginx

```sh
cat > /etc/nginx/conf.d/django_hello_world.conf <<EOF
server {
    listen 80;
    server_name localhost 192.168.1.11;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/django_demo_admin/app;
    }

    location / {
        # include proxy_params;
        proxy_pass http://unix:/home/django_demo_admin/app/hello_world.sock;
    }
}
EOF

# test syntax
nginx -t
# nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
# nginx: configuration file /etc/nginx/nginx.conf test is successful

sudo systemctl restart nginx
```

---

- SELinux???

```sh
semanage fcontext -a -t httpd_sys_content_t "/home/django_demo_admin/app(/.*)?"
restorecon -Rv /home/django_demo_admin/app

systemctl restart gunicorn
systemctl restart nginx

systemctl status nginx gunicorn
```

- Test

---

## Setup Cloudflare tunne

```sh
curl -L --output cloudflared.rpm https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-x86_64.rpm &&

sudo yum localinstall -y cloudflared.rpm &&

sudo cloudflared service install <hash_code>
```
