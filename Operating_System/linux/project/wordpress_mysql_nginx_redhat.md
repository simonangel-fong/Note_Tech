# Project - Wordpress-Mysql-Nginx-Redhat

[Back](../index.md)

- [Project - Wordpress-Mysql-Nginx-Redhat](#project---wordpress-mysql-nginx-redhat)
  - [Prerequisites](#prerequisites)
  - [Install Nginx Web Server](#install-nginx-web-server)
  - [Install PHP Programing Language](#install-php-programing-language)
  - [Install Mysql Server](#install-mysql-server)
  - [Install PHP-FPM and Additional PHP Modules](#install-php-fpm-and-additional-php-modules)
  - [Install WordPress in RHEL](#install-wordpress-in-rhel)
  - [Configure Nginx for WordPress](#configure-nginx-for-wordpress)

---

## Prerequisites

```sh
# update packages
sudo dnf update -y
```

## Install Nginx Web Server

- install and enable nginx

```sh
# install NGINX.
sudo dnf install -y nginx

# enable Nginx
sudo systemctl enable nginx
sudo systemctl start nginx
sudo systemctl status nginx
```

- edit firewall rules to allow HTTP requests on web server

```sh
sudo firewall-cmd --permanent --zone=public --add-service=http
sudo firewall-cmd --permanent --zone=public --add-service=https
sudo firewall-cmd --reload
```

- Verify
  - Visit ip address in browser, nginx test page is available.

---

## Install PHP Programing Language

- install `PHP`

```sh
sudo dnf install -y php php-mysqlnd php-pdo php-gd php-mbstring
```

- restart web server so that Nginx knows that it will be serving `PHP` requests

```sh
sudo systemctl restart nginx
```

- Test:
  - test a PHP by creating a simple `info.php` file
  - brownse `http://server-ip-address/info.php`

```sh
sudo vi /usr/share/nginx/html/info.php
# <?php phpinfo() ?>
```

---

## Install Mysql Server

- Install mysql server package

```sh
# Install MySQL server packages:
sudo dnf install -y mysql-server
# Start the mysqld service
sudo systemctl start mysqld.service
# Enable the mysqld service to start at boot
sudo systemctl enable mysqld.service
```

- Create Database for WordPress

```sh
sudo mysql -u root -p

CREATE DATABASE wordpress;
CREATE USER wordpress@localhost identified by 'wordpress123';
GRANT ALL on wordpress.* to wordpress@localhost;
FLUSH PRIVILEGES;
EXIT;
```

---

## Install PHP-FPM and Additional PHP Modules

```sh
sudo dnf install -y php php-mysqlnd php-pdo php-gd php-mbstring php-fpm

#  enable and start the PHP-FPM daemon.
sudo systemctl enable php-fpm
sudo systemctl start php-fpm
```

- Configure PHP-FPM

```sh
sudo vi /etc/php-fpm.d/www.conf

# modify the user and group attributes to nginx
# user = nginx
# group = nginx
```

- Restart

```sh
sudo systemctl restart php-fpm
# verify
# sudo systemctl status php-fpm
```

---

## Install WordPress in RHEL

```sh
cd ~
wget https://wordpress.org/latest.zip
unzip latest.zip
cp wordpress/wp-config-sample.php wordpress/wp-config.php
vi ~/wordpress/wp-config.php
```

```conf
/** MySQL database name */
define('DB_NAME', 'wordpress');

/** MySQL database username */
define('DB_USER', 'wordpress');

/** MySQL database password */
define('DB_PASSWORD', 'wordpress123');
```

- Copy

```sh
sudo cp -R wordpress /usr/share/nginx/html
sudo chown -R nginx:nginx /usr/share/nginx/html
sudo chmod -R 775 /usr/share/nginx/html
```

---

## Configure Nginx for WordPress

- create a server block file for WordPress

```sh
sudo vi /etc/nginx/conf.d/wordpress.conf
sudo cat > /etc/nginx/conf.d/wordpress.conf <<EOF
server {
    listen 80;
    server_name localhost 192.168.204.153;

    root /usr/share/nginx/html/wordpress;
    index index.php index.html index.htm;

    location / {
        try_files $uri $uri/ /index.php?$args;
    }

    location = /favicon.ico {
        log_not_found off;
        access_log off;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico)$ {
        expires max;
        log_not_found off;
    }

    location = /robots.txt {
        allow all;
        log_not_found off;
        access_log off;
    }

    location ~ \.php$ {
        include /etc/nginx/fastcgi_params;
        fastcgi_pass unix:/run/php-fpm/www.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    }
}
EOF
```

---

- modify the Nginx main configuration file
  - Locate the line that starts with root and specify the path to the webroot directory.

```sh
sudo vim /etc/nginx/nginx.conf

# root         /usr/share/nginx/html/wordpress;
```

- Test syntax

```sh
sudo nginx -t
```

- restart Nginx and PHP-FPM services.

```sh
sudo systemctl restart nginx
sudo systemctl restart php-fpm
```

---

- set SELinux to permissive.

```sh
sudo vim /etc/selinux/config

# SELINUX=permissive

sudo reboot
# verify
getenforce
```

---

- Visit `http://ip` in browser.
