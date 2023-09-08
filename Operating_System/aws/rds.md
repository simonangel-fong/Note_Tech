# AWS - RDS

[Back](./index.md)

- [AWS - RDS](#aws---rds)
  - [Connect to RDS with EC2](#connect-to-rds-with-ec2)
  - [Djnago connect to RDS](#djnago-connect-to-rds)

---

## Connect to RDS with EC2

- Make sure RDS in a Security Group that allow port `3306`
  - Otherwise, `ERROR 2002 (HY000): Can't connect to server on 'endpoint' (115)`

- For Ubuntu

```sh
sudo apt-get update
sudo apt-get install -y mariadb-server
sudo systemctl enable mariadb
sudo systemctl start mariadb

mysql -h <endpoint> -P 3306 -u <username> -p

```

---

## Djnago connect to RDS

```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '<database_name>',
        'USER': '<database_user>',
        'PASSWORD': '<database_password>',
        'HOST': '<database_endpoint>',
        'PORT': '3306',
    }
}
```



---
[TOP](#aws---rds)