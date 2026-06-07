# Kubernetes Security: Fundamental

[Back](../../index.md)

- [Kubernetes Security: Fundamental](#kubernetes-security-fundamental)
  - [Symmetric Encryption \& Asymmetric Encryption](#symmetric-encryption--asymmetric-encryption)
    - [Symmetric Encryption](#symmetric-encryption)
    - [Asymmetric Encryption](#asymmetric-encryption)
  - [Certificate Authortity](#certificate-authortity)
    - [Certificate](#certificate)
    - [Public Key Infrastructure](#public-key-infrastructure)
    - [`Chain of Trust` model](#chain-of-trust-model)
    - [Self-signed certificates](#self-signed-certificates)
  - [HTTPS/TLS](#httpstls)
    - [Lab: SSH TLS](#lab-ssh-tls)
    - [Openssl Lab: Create keys](#openssl-lab-create-keys)
  - [Certificate Signing Request (CSR)](#certificate-signing-request-csr)
    - [Lab: Create CSR and self-signed](#lab-create-csr-and-self-signed)

---

## Symmetric Encryption & Asymmetric Encryption

### Symmetric Encryption

- `Symmetric encryption`
  - uses a single shared key to both encrypt and decrypt data.
- Common algorithm
  - `Advanced Encryption Standard(AES)`

- model:
  - sender and reciever share the key
  - sender encrypts data with the shared key
  - sender sends encrypted data
  - reciever decrypts data with the same key

- pros
  - it is fast and simple, therefore, good for encrypting large amounts of data
- cons
  - have to somehow share the key securely beforehand

- Use case:
  - zip files
  - disk encryption

---

### Asymmetric Encryption

- `Asymmetric encryption`
  - uses a **pair** of mathematically linked keys: a `public key` and a `private key`.
- Common algorithm
  - `RSA`

- model:
  - reciever post and share the `public key` with sender
  - sender encrypts data with the `public key`
  - sender sends encrypted data
  - receiver decrypts data with the `private key`

- Pros
  - No Secure Key Exchange Required
  - High Security
- cons
  - much slower, rarely used for bulk data.
  - Computational Cost

- Use case:
  - HTTPS, SSH, and email signing.

---

- `public key`
  - used for encryption; locks the data.
  - anyone can have it
  - Common `public key` file name
    - `server.crt`
    - `server.pem`
    - `client.crt`
    - `client.pem`

- `private key`
  - used for decryption; unlocks the data.
  - Common `private key` file name
    - `server.key`
    - `server-key.pem`
    - `client.key`
    - `client-key.pem`

---

## Certificate Authortity

- `Certificate Authortity(CA)`
  - a trusted, third-party organization that **verifies the identities** of websites, devices, or individuals and binds them to cryptographic keys.
  - a private CA can be deployed internally

- Popular CAs
  - `Let's Encrypt`: A free, automated, and open public CA.
  - `DigiCert`: A widely used commercial CA for enterprise security.
  - `SSL.com`: Offers a variety of SSL and digital signing certificates.

---

### Certificate

A `certificate` is essentially a signed document containing:

- `Serial Number`:
  - A **unique identifier** assigned by the `Certificate Authority (CA)` to track the certificate.
- `Issuer`:
  - The identifying information and distinguished **name of the trusted `Certificate Authority (CA)`** that issued and vetted the certificate.
- `CA's Digital Signature`:
  - A **cryptographic signature** created by the CA using its own private key, which proves the certificate is authentic and has not been tampered with.
- `Subject (Identity)`:
  - Identifies the **certificate owner**
  - e.g., website domain, company name, department, or individual.
- `Public Key`:
  - A copy of the owner's public key, which is used to encrypt data and verify digital signatures.
- `Validity Period`:
  - The exact dates and times indicating when the certificate is **active** and when it **expires**.

---

### Public Key Infrastructure

- `Public Key Infrastructure (PKI)`
  - a comprehensive security framework that **creates, manages, and revokes** `digital certificates` and `public-key encryption`.
  - use asymmetric cryptography
    - `Public Key`: Shared openly with anyone; used to encrypt data or verify a digital signature.
    - `Private Key`: Kept strictly secret by the owner; used to decrypt incoming messages or sign outgoing documents

- Core Components
  - `Certificate Authority`
    - a **trusted** organization/system that \*\*issues `digital certificates`.
    - **verifies** the identity of a website/server, then **signs its certificate**.
    - signs that certificate using the CA’s `private key`.

  - `digital certificate`
    - an **electronic credential** used to prove the **identity** of a device, server, or user, and to facilitate secure, encrypted communication
    - securely connect an identity to its `public key`.
  - `Registration Authority (RA)`:
    - Often acts as the **front-end** to the `CA`;
    - verifies the user’s identity before a certificate is issued.
  - `Certificate Revocation List (CRL)`:
    - A **repository** of certificates that have been **compromised or expired** before their scheduled end date.

---

### `Chain of Trust` model

- `chain of trust`
  - a **hierarchical system** where **trust is passed down** from a highly secure, recognized **source** (the "trust anchor") to other **entities**.
  - It ensures that if the foundation is trusted, everything correctly linked to it can also be trusted.

- `Root Certificate Authority (Root CA)`
  - the top-most, trusted authority in a `Public Key Infrastructure (PKI)` that issues `digital certificates`.
  - It acts as the **ultimate "trust anchor"** for verifying identities, ensuring secure, encrypted communications across the internet and private networks.
  - `CA private keys` are so valuable, CA typically stays offline.
  - `Root Certificate`:
    - A self-signed root certificate generated by Root CA.
    - verifies its own identity.
    - inherently trusted by devices and operating systems

- `Intermediate Certificates` (or `intermediate CAs`)
  - Issues certs on `Root CA`'s behalf
  - acts as a **trusted bridge** between a highly secure `Root CA` and `End-Entity Certificates`
  - handle day-to-day certificate issuance.
  - `Intermediate Certificates`
    - act as a bridge.
    - signed by the Root CA and are used to issue certificates to end-users, keeping the root certificate securely offline to minimize risk.

- `End-Entity Certificates`(or `leaf certificate`)
  - is the **final, functional** `digital certificate` issued to a specific subject—like a web server (TLS/SSL), an email client, or an IoT device.
  - identifies a specific resource and cannot issue other certificates.Key Characteristics

- OS and browser come **pre-loaded** with a list of ~150 `root CAs` whose `public keys` they already trust unconditionally.
  - Everything else derives trust from being signed by one of those roots.

---

### Self-signed certificates

- `Self-signed certificates`
  - a certificate is created and signed itself, **without any CA**.
  - has all the same fields, but browsers will show a big scary warning because there's nobody vouching for it.
  - Fine for internal tools, not for public sites.

---

## HTTPS/TLS

- TLS handshake
  - 1. Client connects to webserver.
  - 2. Server sends `certificate` containing server `public key`.
    - 3rd party can also see the public key.
  - 3. Client **verifies** the `certificate`.
  - 4. Client and server use asymmetric cryptography/key exchange to create a `shared symmetric session key`.
  - 5. Client and server both use that `shared symmetric key` to encrypt and decrypt traffic.
    - 3rd party may capture encrypted traffic, but **cannot** easily decrypt it without the `session key`.

```txt
Client                              Server
  |                                   |
  | --------- ClientHello ----------> |
  |                                   |
  | <--- Certificate + key info ----- |
  |                                   |
  | Verify server certificate         |
  |                                   |
  | ---- key exchange public info --->|
  | <--- key exchange public info ----|
  |                                   |
  | Client calculates session key     |
  | Server calculates session key     |
  |                                   |
  | ===== encrypted HTTP traffic =====|
  |        using session key          |
```

- After the TLS handshake, the traffic looks like this:
  - Client and server encrypt and decrypt request with `shared session key`.

- Asymmetric crypto:
  - Used at the **beginning** for **identity** and **key exchange**.

- Symmetric crypto:
  - Used for the **actual request/response data**.

---

### Lab: SSH TLS

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

### Openssl Lab: Create keys

```sh
# private key
openssl genrsa -out my.key 1024
# my.key

# public key
openssl rsa -in my.key -pubout > my.pem
# my.pem

```

---

## Certificate Signing Request (CSR)

- `Certificate Signing Request (CSR)`
  - a block of **encoded text** generated by server sent to a `Certificate Authority (CA)` to apply for an SSL/TLS certificate.
  - Data Included:
    - the public key
    - `Common Name (CN)`: The fully qualified domain name (e.g., www.example.com or \*.example.com for wildcards).
    - `Organization (O)` & `Organizational Unit (OU)`: legal business name and specific department.
    - Locality `(L)`, State/Province `(S)`, and Country `(C)`: location details.
  - steps:
    - create private key and public key
    - create CSR
    - CA validates and issues the final SSL certificate

---

### Lab: Create CSR and self-signed

```sh
# Generate a private key
openssl genrsa -out mysite.key 2048

ls
# mysite.key

cat mysite.key
# -----BEGIN PRIVATE KEY-----
# MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC27G5SGy9ORt1h
# DY5TlHLxlL1CgdydahuHeuwIvE6+1JX3DrR04F6719MlR9BMDGm4mrnNpEgM/IeM
# uhsbN1c23zM6HDJ0i3vsK5LHSHUON4z2SG/E7szTDmWZ7JcVCZqGKOEr7H9RX9MP
# mTAGhkNW621YtOig4nWXPzoSmxXKH/VbotmogAO7Df67kdhfS93fOdXCdeNoBzeZ
# usiLksTIW4z7M2nuS/b8Dx3UFDskZMUuuFj0PcBt5xPXgAaf5CKSlMp6czCBAL0+
# Zh/ukDmeNa2BO/BLO/umdwXgRigcVB7/zCniri4LI2TnNSPP++GPn2lt6gAwVDgh
# Bd4qIBATAgMBAAECggEAIfAFm8gdY7l0EzCPqmQNW1LMNk2fn7jy+JTOu+Qr++23
# EQoyYsjJ6rHlI7KKK8HVz4EtXcDP+VDU2UAiDU+cJ7sLZwmaNtM2H6AJ8F06EnQt
# +/d+fRwM9k9ifEdP1IBeoetts1eCW5easfcq2NsKHVM6i02tJ0Q8qt35KUCKr2Ak
# M+bY2F9Lqv03rNRgVHTpX6/xyP0YZsfEWNuwkuHy4bpkx9leTf0OTBgA2xfke7ek
# HnQVXfAL4VOTIPXWUrcEASZ6xiT6m+A+ov/e4s3CpWFl6uIJe9CMYm9XLURVYJu4
# MObYALYhQ1ehcPB32tfd6QmzdzTTy6c/klx+dTJWyQKBgQDd05kLsASYimnMFkOW
# rnVYkrTPlbsjCv9f7/QD/2gvyRGxmB/1KT36Oite0KKm3i3DRubXtrVDM8Xiwn2Z
# L9oVncXVuLwBrBqz0d5X9+cqeHsWko07etY/y5riHBhXY3GXwDU2DTKOBFwc5/PK
# pG7psgvGdWbpteoaCcmvEDYX9QKBgQDTGpNbqXDpZ6irHigaTTQhyItPNrY3ba5b
# 1E4zjh0HKSjq0JOcXZCaQw1EM4mBgIMEY1Gqof7x4aZPEsHj0JD+ckLcqEl+saK3
# GKOeDRc6KJH9kQM19vJ/xCCC61RPaFQvGgyLCN+ycGkRSS3V05IBYlUoX4ZfS4vt
# FZzOZ7Fq5wKBgGALtkBxPgwuIhDTswATGYv4OYGH+zb5FAmeA7GXbK0ECj0y+ONV
# sBggB5dODp7hpD7g/CJ6YZFvYUcFnwwsw+iIH5iiHAU9V3J0dCjylYy2DdWALtaK
# ISoOJkmwkHmF/TEPb/qvTCxhhuCdLdmXyM424RJU0vJuaaZMhp7eDg3hAoGAbrD0
# q4+BQSG1c2Rwqrnop/477eFGUnIUhtof1zChT+vpJJcRj2AQPpMCFczgQSNdj6N0
# YwBmafZj+fpf6FCodoL7RDCJuQDzzQYCZRGAKGK1ijvLbzR5mzz/vyYeIzUVT01d
# Xlnc0ffXX9T7T6+MU2V4OZ89GiLG0B4RBrmgcekCgYBQEWGlg2i3OO5qmlpS5hEy
# uHAvLIriCUkkP9AhnRgUJeLeuFNEaul3+J0dyKrUXpzLPWp0R41rpuH5/GBKoFvr
# Y2COR4kObM3+8moLNtsNPOOaHnxsSMwTNL1iI1KIDDnXiWe4dHGtuUPlyf977JjX
# l0Etmb90WfK9pfCrK88u/A==
# -----END PRIVATE KEY-----

# Print the private key in text
openssl rsa -in mysite.key -text -noout
# Private-Key: (2048 bit, 2 primes)
# modulus:
#     00:b6:ec:6e:52:1b:2f:4e:46:dd:61:0d:8e:53:94:
#     72:f1:94:bd:42:81:dc:9d:6a:1b:87:7a:ec:08:bc:
#     4e:be:d4:95:f7:0e:b4:74:e0:5e:bb:d7:d3:25:47:
#     d0:4c:0c:69:b8:9a:b9:cd:a4:48:0c:fc:87:8c:ba:
#     1b:1b:37:57:36:df:33:3a:1c:32:74:8b:7b:ec:2b:

# Derive the public key from the private key.
openssl rsa -in mysite.key -pubout -out mysite.pub
# writing RSA key

ls
# mysite.key  mysite.pub

cat mysite.pub
# -----BEGIN PUBLIC KEY-----
# MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtuxuUhsvTkbdYQ2OU5Ry
# 8ZS9QoHcnWobh3rsCLxOvtSV9w60dOBeu9fTJUfQTAxpuJq5zaRIDPyHjLobGzdX
# Nt8zOhwydIt77CuSx0h1DjeM9khvxO7M0w5lmeyXFQmahijhK+x/UV/TD5kwBoZD
# VuttWLTooOJ1lz86EpsVyh/1W6LZqIADuw3+u5HYX0vd3znVwnXjaAc3mbrIi5LE
# yFuM+zNp7kv2/A8d1BQ7JGTFLrhY9D3AbecT14AGn+QikpTKenMwgQC9PmYf7pA5
# njWtgTvwSzv7pncF4EYoHFQe/8wp4q4uCyNk5zUjz/vhj59pbeoAMFQ4IQXeKiAQ
# EwIDAQAB
# -----END PUBLIC KEY-----

# Create a CSR (Certificate Signing Request)
openssl req -new -key mysite.key -out mysite.csr
ls
# mysite.csr  mysite.key  mysite.pub

# Inspect the CSR
openssl req -in mysite.csr -text -noout -verify
# Certificate request self-signature verify OK
# Certificate Request:
#     Data:
#         Version: 1 (0x0)
#         Subject: C = CA, ST = Ontario, L = Toronto, O = Arguswatcher, CN = *.arguswatcher.net
#         Subject Public Key Info:
#             Public Key Algorithm: rsaEncryption
#                 Public-Key: (2048 bit)
#                 Modulus:
#                     00:b6:ec:6e:52:1b:2f:4e:46:dd:61:0d:8e:53:94:
#                     72:f1:94:bd:42:81:dc:9d:6a:1b:87:7a:ec:08:bc:
#                     4e:be:d4:95:f7:0e:b4:74:e0:5e:bb:d7:d3:25:47:
#                     d0:4c:0c:69:b8:9a:b9:cd:a4:48:0c:fc:87:8c:ba:
#                     1b:1b:37:57:36:df:33:3a:1c:32:74:8b:7b:ec:2b:
#                     92:c7:48:75:0e:37:8c:f6:48:6f:c4:ee:cc:d3:0e:
#                     65:99:ec:97:15:09:9a:86:28:e1:2b:ec:7f:51:5f:
#                     d3:0f:99:30:06:86:43:56:eb:6d:58:b4:e8:a0:e2:
#                     75:97:3f:3a:12:9b:15:ca:1f:f5:5b:a2:d9:a8:80:
#                     03:bb:0d:fe:bb:91:d8:5f:4b:dd:df:39:d5:c2:75:
#                     e3:68:07:37:99:ba:c8:8b:92:c4:c8:5b:8c:fb:33:
#                     69:ee:4b:f6:fc:0f:1d:d4:14:3b:24:64:c5:2e:b8:
#                     58:f4:3d:c0:6d:e7:13:d7:80:06:9f:e4:22:92:94:
#                     ca:7a:73:30:81:00:bd:3e:66:1f:ee:90:39:9e:35:
#                     ad:81:3b:f0:4b:3b:fb:a6:77:05:e0:46:28:1c:54:
#                     1e:ff:cc:29:e2:ae:2e:0b:23:64:e7:35:23:cf:fb:
#                     e1:8f:9f:69:6d:ea:00:30:54:38:21:05:de:2a:20:
#                     10:13
#                 Exponent: 65537 (0x10001)
#         Attributes:
#             (none)
#             Requested Extensions:
#     Signature Algorithm: sha256WithRSAEncryption
#     Signature Value:
#         54:09:8d:e1:41:8e:4b:95:48:b2:f2:df:85:a4:6b:6d:1c:2d:
#         d9:bf:d5:4b:bb:2b:45:b3:60:f7:01:9a:0b:ed:c8:dc:57:2a:
#         ad:96:96:ae:35:28:52:9e:b5:14:49:29:c3:69:21:58:41:fc:
#         11:73:95:2f:8d:0e:19:9c:24:a6:d8:78:57:5e:87:29:7d:cf:
#         80:15:f2:62:d0:5f:8d:9f:5e:07:36:29:ca:f4:2c:80:d4:69:
#         5e:09:9f:ff:56:42:65:61:dc:18:ed:ac:1b:4a:52:35:07:52:
#         2d:13:76:32:a0:af:7e:b3:ad:92:73:18:a5:f8:48:26:db:1d:
#         55:ca:f6:ae:2e:ec:21:97:d6:b2:e7:22:c1:5b:fa:af:41:3d:
#         a5:49:19:c4:9a:50:8a:c4:4e:7b:dd:0b:dd:b3:9a:11:21:71:
#         a7:cc:18:6b:2f:c3:37:3a:e9:83:81:25:ed:2b:87:8b:ae:cf:
#         b7:da:d4:b6:6f:98:e6:95:3e:95:a9:4a:2c:ae:a0:88:94:de:
#         0b:b9:f9:52:1d:14:62:92:20:3c:ae:58:ef:38:fb:34:11:38:
#         01:37:86:69:17:78:a3:d7:7d:fd:8e:a4:ce:e9:8c:62:70:aa:
#         2b:fd:b3:37:c4:24:fa:0c:84:69:fe:e8:82:d8:57:1f:94:d4:
#         8c:3f:8f:6a

# Self-signed
openssl x509 -req -in mysite.csr -signkey mysite.key -out mysite.crt -days 1800
# Certificate request self-signature ok
# subject=C = CA, ST = Ontario, L = Toronto, O = Arguswatcher, CN = *.arguswatcher.net

ls
# mysite.crt  mysite.csr  mysite.key  mysite.pub

cat mysite.crt
# -----BEGIN CERTIFICATE-----
# MIIDUTCCAjkCFAf9ftfTGIaD8Rd58ZSfiZeT9ch5MA0GCSqGSIb3DQEBCwUAMGUx
# CzAJBgNVBAYTAkNBMRAwDgYDVQQIDAdPbnRhcmlvMRAwDgYDVQQHDAdUb3JvbnRv
# MRUwEwYDVQQKDAxBcmd1c3dhdGNoZXIxGzAZBgNVBAMMEiouYXJndXN3YXRjaGVy
# Lm5ldDAeFw0yNjA2MDcxNjEwMzZaFw0zMTA1MTIxNjEwMzZaMGUxCzAJBgNVBAYT
# AkNBMRAwDgYDVQQIDAdPbnRhcmlvMRAwDgYDVQQHDAdUb3JvbnRvMRUwEwYDVQQK
# DAxBcmd1c3dhdGNoZXIxGzAZBgNVBAMMEiouYXJndXN3YXRjaGVyLm5ldDCCASIw
# DQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALbsblIbL05G3WENjlOUcvGUvUKB
# 3J1qG4d67Ai8Tr7UlfcOtHTgXrvX0yVH0EwMabiauc2kSAz8h4y6Gxs3VzbfMzoc
# MnSLe+wrksdIdQ43jPZIb8TuzNMOZZnslxUJmoYo4Svsf1Ff0w+ZMAaGQ1brbVi0
# 6KDidZc/OhKbFcof9Vui2aiAA7sN/ruR2F9L3d851cJ142gHN5m6yIuSxMhbjPsz
# ae5L9vwPHdQUOyRkxS64WPQ9wG3nE9eABp/kIpKUynpzMIEAvT5mH+6QOZ41rYE7
# 8Es7+6Z3BeBGKBxUHv/MKeKuLgsjZOc1I8/74Y+faW3qADBUOCEF3iogEBMCAwEA
# ATANBgkqhkiG9w0BAQsFAAOCAQEAmTQu3EkpIVzoGFDoVYAWQMLNGWFALc3v9qdY
# xGbcZEoASeQgk2r9fKH37wwsLFLHepA8IdSHKsWX1f9pkHpZpi6iiGpya8ZZW9V1
# x8DVnnV8SJ0CsJZ0Cb4fF2LdgEjTyf5hNNUS3jQfM+DYAkzKg71d+bZv9Fq0SnK9
# lfZy4What56dCHpNSz4vaguO4m9RblGbfxyqqGg7PlsJCjYHUwdUp2x8KdlSsfw3
# vb58FhmRsWdNEm0tzpMKEzV95FISQmGb+Godkf55TVRgUJ3R8FP7DPw1MbY5Kvtn
# GWHH1MGwzd/1QbhtsgPfgTSJnBo3GCHcnfH+VWjsz3X68CXIHQ==
# -----END CERTIFICATE-----

# Check contents of cert
openssl x509 -in mysite.crt -text -noout
# Certificate:
#     Data:
#         Version: 1 (0x0)
#         Serial Number:
#             07:fd:7e:d7:d3:18:86:83:f1:17:79:f1:94:9f:89:97:93:f5:c8:79
#         Signature Algorithm: sha256WithRSAEncryption
#         Issuer: C = CA, ST = Ontario, L = Toronto, O = Arguswatcher, CN = *.arguswatcher.net
#         Validity
#             Not Before: Jun  7 16:10:36 2026 GMT
#             Not After : May 12 16:10:36 2031 GMT
#         Subject: C = CA, ST = Ontario, L = Toronto, O = Arguswatcher, CN = *.arguswatcher.net
# ...
```

---
