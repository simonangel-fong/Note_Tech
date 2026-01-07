# Security Fundamental

[Back](../../index.md)

---



## TLS Cerfificates

对称加密

---

## Asymmetric Encryption

1. User access the webserver
2. Webserver **return** the `public key`
   - 3rd-party also acquire the `public key`
3. User **encrypt and send** the data with `public key`
   - 3rd-party can get the encripted data
4. Webserver **descript** with `private key`.
   - 3rd-party **not easy to descript** the encrypted data **without** a `private key`.
5. Webserver returns and encripted data with public key
   - 3rd-party **not easy to descript** the encrypted data **without** a `private key`.

- Common `public key` file name

  - `server.crt`
  - `server.pem`
  - `client.crt`
  - `client.pem`

- Common `private key` file name
  - `server.key`
  - `server-key.pem`
  - `client.key`
  - `client-key.pem`

---

### Server Certificate

- A middle man server act as the remote server

  - Solution: Cerficate
    - `url` + `public key` + `issuer`
      - The `requested url` must match the `certificate url`
        - Otherwise, requested url is not secure.
      - `issuer` must be valid
    - Otherwise, `self-signed certificate` is **not secure**.
      - common web browser will **issue a warning** when the certificate is not valid.

- `Certificate Authortity(CA)`

  - the organization to **validate a certificate**.
  - e.g., symantec
  - a private CA can be deployed internally

- `root certificate`

  - a certificate used for `Certificate Authortity(CA)`

- `Certificate Signing Request (CSR)`
  - the **request sent** by a DNS owner to **verify a certificate**
    - DNS owner send CSR
    - CA validate the information
    - CA sign and return certificate

```sh
# CSR
openssl req -new -key my.key -out my.csr -subj "/C=US/ST=CA/O=MyOrg, Inc./CN=my.com"
# my.key my.csr
```

---

### Client Cerficates

- How client verify themselves when creating a secure connection with the remote server.

  - Client **create** a `Certificate Signing Request (CSR)` and **verified** with the `Certificate Authortity(CA)`.
  - Client **send and encrypt** the data with the `certificate`.
  - Server **recieves** the data and **verify** the `cerficate` with the `Certificate Authortity(CA)`.
  - If the certificate is valid, server **decrypts the data** with `private key`.

- `Public Key Infrastructure(PKI)`

---

### TLS example: SSH

```sh
# generate keys
ssh-keygen
# id_rsa: private key
# id_rsa.pub: public key

# copy public key
ssh-copy-id -i id_rsa.pub user@remote_server
# .ssh/authorized_keys

# access remote
ssh user@remote_server
```

### TLS example: Openssl

```sh
# private key
openssl genrsa -out my.key 1024
# my.key

# public key
openssl rsa -in my.key -pubout > my.pem
# my.pem

```

---