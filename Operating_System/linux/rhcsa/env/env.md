# RHCSA - Environment Configuration

[Back](../../index.md)

- [RHCSA - Environment Configuration](#rhcsa---environment-configuration)
  - [Server](#server)
  - [ServerA](#servera)

---

## Server

```sh

```

---

## ServerA

```sh
useradd unilao
echo "unilao:abc123" | chpasswd

dnf upgrade -y
dnf install httpd -y

sudo systemctl start httpd
sudo systemctl enable httpd
sudo systemctl status httpd

sudo nano /etc/httpd/conf/httpd.conf
# Listen 82

sudo nano /etc/httpd/conf.d/hello_world.conf
# <VirtualHost *:82>
#     ServerAdmin admin@localhost
#     ServerName localhost
#     ServerAlias localhost
#     DocumentRoot /var/www/html/hello_world
#     ErrorLog "/var/log/httpd/hello_world_error.log"
#     CustomLog "/var/log/httpd/hello_world_access.log" combined
# </VirtualHost>

sudo mkdir -p /var/www/html/hello_world
cat > /var/www/html/hello_world/index.html << EOF
<!DOCTYPE html>
<html>
<head>
    <title>Hello World</title>
</head>
<body>
    <h1>Hello, World!</h1>
</body>
</html>
EOF

# sudo chown -R apache:apache /var/www/html/hello_world/index.html

sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --permanent --add-port=82/tcp
sudo firewall-cmd --reload
sudo firewall-cmd --list-all

systemctl restart httpd
```
