# GitHub Actions - Setup Local Environment

[Back](../index.md)

- [GitHub Actions - Setup Local Environment](#github-actions---setup-local-environment)
  - [Install](#install)
    - [Install Node.js](#install-nodejs)
  - [Connect GitHub with SSH](#connect-github-with-ssh)

---

## Install

### Install Node.js

- ref: https://nodejs.org/en/download

```sh
# confirm
node -v
# v24.14.1
```

---

## Connect GitHub with SSH

```sh
# generate ssh key
ssh-keygen -t ed25519 -C "your_email@example.com"
```

- Add an ssh key in githug with *.pub
- move the .pub to .ssh/
- git push