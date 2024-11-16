# Project - Isntall Wordpress on Ubuntu

[Back](./index.md)

---

- [Project - Isntall Wordpress on Ubuntu](#project---isntall-wordpress-on-ubuntu)
  - [Install packages](#install-packages)
  - [Configure the MySQL Database Server](#configure-the-mysql-database-server)
  - [Configure NGINX](#configure-nginx)
  - [Download WordPress](#download-wordpress)
  - [Assign File Permissions for WordPress](#assign-file-permissions-for-wordpress)
  - [Determine Your IP Address](#determine-your-ip-address)
  - [Complete the Web Application Install](#complete-the-web-application-install)

---

## Install packages

```sh
# update packages
sudo apt update -y

# install NGINX.
sudo apt install -y nginx

# Install and Configure the MySQL Database Server
sudo apt install -y mysql-server

# Install PHP
sudo apt install -y php-fpm

# Install the required PHP modules.
sudo apt install -y php-mysql php-curl php-mbstring php-imagick php-xml php-zip

# Install unzip
sudo apt install -y unzip
```

---

## Configure the MySQL Database Server

```sh
# create a database named "wordpress"
sudo mysqladmin create wordpress
# Connect to the MySQL server
sudo mysql
```

```sql
CREATE USER wordpress@localhost identified by 'wordpress123';
GRANT ALL on wordpress.* to wordpress@localhost;
exit
```

---

## Configure NGINX

- need to tell NGINX to send all PHP requests to PHP FPM for processing.

```sh
# update the default NGINX configuration.
cd /etc/nginx/sites-available/
sudo vi default
```

- Change this line from:

```conf
index index.html index.htm index.nginx-debian.html;
```

to:

```conf
index index.php index.html index.htm index.nginx-debian.html;
```

---

- change this line from:

```conf
try_files $uri $uri/ =404;
```

to:

```conf
try_files $uri $uri/ /index.php$is_args$args;
```

---

- Change these lines from:

```conf
#location ~ \.php$ {
# include snippets/fastcgi-php.conf;
#
# # With php-fpm (or other unix sockets):
# fastcgi_pass unix:/var/run/php/php7.4-fpm.sock;
# # With php-cgi (or other tcp sockets):
# fastcgi_pass 127.0.0.1:9000;
#}
```

to:

```conf
location ~ \.php$ {
  include snippets/fastcgi-php.conf;
  # With php-fpm (or other unix sockets):
  # change the path of sock as necessary.
  fastcgi_pass unix:/var/run/php/php8.3-fpm.sock;
  # # With php-cgi (or other tcp sockets):
  # fastcgi_pass 127.0.0.1:9000;
}
```

---

- reload Nginx configuration

```sh
# check syntax error
sudo nginx -t
# reload
sudo systemctl reload nginx
```

---

## Download WordPress

```sh
cd ~
# download latest wordpress
curl -O https://wordpress.org/latest.zip
unzip latest.zip
sudo mv wordpress/* /var/www/html
```

---

## Assign File Permissions for WordPress

- change the ownership of the configuration file to "www-data".

```sh
sudo chown -R www-data:www-data /var/www/html
```

---

## Determine Your IP Address

```sh
ip a
# 192.168.204.154
```

---

## Complete the Web Application Install

- In browser, navigat to ip address for the further configuration.

---

[TOP](#project---isntall-wordpress-on-ubuntu)
