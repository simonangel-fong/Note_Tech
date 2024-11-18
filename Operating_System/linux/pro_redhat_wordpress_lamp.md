# Project - Isntall Wordpress on Redhat (LAMP)

[Back](./index.md)

---

- [Project - Isntall Wordpress on Redhat (LAMP)](#project---isntall-wordpress-on-redhat-lamp)
  - [Install packages](#install-packages)

---

## Install packages

```sh
sudo yum upgrade -y 

sudo yum install -y httpd

sudo systemctl enable httpd
sudo systemctl start httpd
sudo systemctl status httpd

sudo firewall-cmd --permanent --zone=public --add-service=http
sudo firewall-cmd --permanent --zone=public --add-service=https
sudo firewall-cmd --reload
```

```sh
sudo yum install -y php php-mysqlnd php-pdo php-gd php-mbstring
sudo systemctl restart httpd
```

```sh
sudo yum install -y mariadb-server mariadb

sudo systemctl enable mariadb
sudo systemctl start mariadb
sudo systemctl status mariadb
```

```sh
mysql_secure_installation
```

```sh
mysql -e "SHOW DATABASES;" -p

sudo mysql -u root -p
CREATE DATABASE wordpress_db;
GRANT ALL ON wordpress_db.* TO 'wordpress_user'@'localhost' IDENTIFIED BY 'wordpress123';
FLUSH PRIVILEGES;
exit;
```

```sh
cd ~
wget https://wordpress.org/latest.tar.gz
tar -xvf latest.tar.gz
cp wordpress/wp-config-sample.php wordpress/wp-config.php

vi wordpress/wp-config.php
```

```sh
sudo cp -R wordpress /var/www/html/
sudo chown -R apache:apache /var/www/html/wordpress
sudo chcon -t httpd_sys_rw_content_t /var/www/html/wordpress -R
sudo chmod -Rf 775  /var/www/html
```

```sh
sudo vi /etc/httpd/conf.d/wordpress.conf
```

```xml
<VirtualHost *:80>
    ServerAdmin rheladmin@localhost
    DocumentRoot /var/www/html/wordpress

    <Directory "/var/www/html/wordpress">
        Options Indexes FollowSymLinks
        AllowOverride all
        Require all granted
    </Directory>

    ErrorLog /var/log/httpd/wordpress_error.log
    CustomLog /var/log/httpd/wordpress_access.log common
</VirtualHost>
```

```sh
sudo systemctl restart httpd
```

```sh
sudo semanage fcontext -a -t httpd_sys_rw_content_t "/var/www/html/wordpress(/.*)?"
```

```sh
sudo restorecon -Rv /var/www/html/wordpress
```


```sh
sudo systemctl enable httpd
sudo systemctl enable mariadb
```