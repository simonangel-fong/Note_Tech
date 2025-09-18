# Redis - Install

[Back](../index.md)

---

## Ubuntu

```sh
# Add the repository to the APT index, update it, and install Redis
sudo apt-get install lsb-release curl gpg
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
sudo chmod 644 /usr/share/keyrings/redis-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
sudo apt-get update
sudo apt-get install -y redis

# enable and start redis service
sudo systemctl enable --now redis-server

# confirm
redis-cli --version
# redis-cli 8.2.1
```

---

## Redhat

```sh
sudo yum install -y redis
sudo systemctl enable --now redis
```

---

## Docker Container

```sh
docker run -d --name redis -p 6379:6379 redis
docker exec -it redis redis-cli --version
# redis-cli 8.0.3
```

- Using a local configuration file

```sh
docker run -v /myredis/conf:/usr/local/etc/redis --name myredis redis redis-server /usr/local/etc/redis/redis.conf
```

## Docker Compose

```yaml
services:
  redis:
    container_name: redis-instance
    image: redis:latest
    restart: always
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"

volumes:
  redis_data:
```

- Confirm

```sh
docker compose up -d
docker compose exec -it redis redis-cli --version
# redis-cli 8.0.3
```