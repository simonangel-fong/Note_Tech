# RHCSA YUM

[Back](../../index.md)

- [RHCSA YUM](#rhcsa-yum)
  - [Question](#question)
  - [Solution](#solution)

---

## Question

```conf
Configure your server a VM repository installed the packages distribution is available via YUM:

Base os url = http://content.example.com/rhel9.0/x86_64/dvd/BaseOS
App stream url= http://content.example.com/rhel9.0/x86_64/dvd/AppStream
```

---

## Solution

```sh
# Optional: Remove Default Repositories 
# sudo mv /etc/yum.repos.d/*.repo /etc/yum.repos.d/backup/

# create repo cf
sudo vi /etc/yum.repo.d/myrepo.repo

# [baseos]
# name=Base os
# baseurl=http://content.example.com/rhel9.0/x86_64/dvd/BaseOS
# enabled=1
# gpgcheck=0
#
# [appstream]
# name=App stream
# baseurl=http://content.example.com/rhel9.0/x86_64/dvd/AppStream
# enabled=1
# gpgcheck=0

# Verify Repository Configuration
yum repolist
# Updating Subscription Management repositories.
# repo id                              repo name
# app                                  App stream
# base                                 Base os
```
