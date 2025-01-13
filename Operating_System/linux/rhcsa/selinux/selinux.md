# RHCSA SELinux

[Back](../../index.md)

- [RHCSA SELinux](#rhcsa-selinux)
  - [Question: Port](#question-port)
    - [Setup](#setup)
    - [Solution](#solution)

---

## Question: Port

```conf
In your system, httpd service has some files in /var/www/html (do not change or alter files)
Solve the problem, httpd service of your system having some issues, service is not running on port 82.
```

### Setup

```sh
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
# Job for httpd.service failed because the control process exited with error code.
# See "systemctl status httpd.service" and "journalctl -xeu httpd.service" for details.
```

```sh
# install
dnf install -y nginx

systemctl enable nginx
systemctl start nginx
systemctl status nginx


mkdir -p /var/www/html
cat > /var/www/html/index.html <<EOF
<html>
<head>
    <title>Httpd Index</title>
</head>
<body>
    <p>This is a httpd page.</p>
</body>
</html>
EOF

cat > /etc/nginx/conf.d/httpd.conf <<EOF
server {
        listen   82;
        server_name  localhost;
        access_log  /var/log/nginx/localhost.access.log;
        location / {
                root   /var/www/html;
                index  index.html;
        }
}
EOF
```

---

### Solution

```sh
# enable port 82
firewall-cmd --add-port=82/tcp --permanent
firewall-cmd --reload
firewall-cmd --list-all

# restart nginx fail
# check error, port 82 permission denied
tail /var/log/nginx/error.log
# 2025/01/10 15:14:26 [emerg] 33387#33387: bind() to 0.0.0.0:82 failed (13: Permission denied)
semanage port -l | grep http_port_t
# http_port_t                    tcp      80, 81, 443, 488, 8008, 8009, 8443, 9000
semanage port -a -t http_port_t -p tcp 82
systemctl restart nginx
systemctl status nginx

# confirm
ss -tulnp | grep 82
Netid State  Recv-Q Send-Q Local Address:Port  Peer Address:PortProcess
tcp   LISTEN 0      511          0.0.0.0:82         0.0.0.0:*    users:(("nginx",pid=33443,fd=7),("nginx",pid=33442,fd=7),("nginx",pid=33441,fd=7))

# If the page is forbidden, update file context
semanage fcontext -a -t httpd_sys_content_t "/var/www/html(/.*)?"
restorecon -R -v /var/www/html
```
