# Redis - Common Commands

[Back](../index.md)

---

## Utility

| Command                  | Description                   |
| ------------------------ | ----------------------------- |
| `redis-cli PING`         | Test connection               |
| `redis-cli INFO`         | Show server info and stats    |
| `redis-cli MONITOR`      | Log all requests (debugging)  |
| `redis-cli DBSIZE`       | Count keys in current DB      |

---


```sh
redis-cli set mykey myvalue
redis-cli expire mykey 60
redis-cli get mykey
redis-cli del mykey
redis-cli set mykey 100 ex 10


redis-cli JSON.SET item:1 $ '{"name":"Noise-cancelling Bluetooth headphones","description":"Wireless Bluetooth headphones with noise-cancelling technology","connection":{"wireless":true,"type":"Bluetooth"},"price":99.98,"stock":25,"colors":["black","silver"]}'

redis-cli JSON.GET item:1 $
```