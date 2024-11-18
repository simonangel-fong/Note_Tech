# Linux - Package

[Back](../index.md)

---

- [Linux - Package](#linux---package)
  - [Package \& Package Manager](#package--package-manager)
  - [`RPM` distros](#rpm-distros)
    - [`rpm`](#rpm)
    - [`yum`: RHEL 7 / CentOS 7 \& Earlier](#yum-rhel-7--centos-7--earlier)
    - [`dnf`: RHEL 8 / CentOS 8 \& Later](#dnf-rhel-8--centos-8--later)
    - [Example: `DNF` install `nginx`](#example-dnf-install-nginx)
  - [`DEB` Distro](#deb-distro)
    - [`APT`: Advanced Packaging Tool](#apt-advanced-packaging-tool)
    - [`dpkg`: low-level package manager](#dpkg-low-level-package-manager)

---

## Package & Package Manager

- `Packages`

  - A collection of files
  - Data / Metadata
    - Package description
    - Version
    - Dependencies

- `Package Manager`

  - used to installs, upgrades, and removes packages
  - Manages dependencies
  - Keeps track of what is installed

- Package Types
  - `RPM(Red Hat Package Manager)` distros
    - RHEL, CentOS, and Oracle Linux
  - `DEB(Debian package)` distros
    - Debian, Ubuntu, and Linux Mint

---

## `RPM` distros

### `rpm`

- `rpm`
  - `Red Hat Package Manager`
  - a free, open-source program that manages software packages in Linux
  - a lower level command

| CMD                     | DESC                          |
| ----------------------- | ----------------------------- |
| `rpm -qa`               | List all installed packages   |
| `rpm -q`                | List an installed package     |
| `rpm -qf /path/to/file` | List the file's package       |
| `rpm -ql package`       | List the package's files      |
| `rpm -ivh package.rpm`  | Install the package           |
| `rpm -e package`        | Erase (uninstall) the package |

---

### `yum`: RHEL 7 / CentOS 7 & Earlier

- `yum`:
  - `Yellowdog Updater Modified`
  - an open-source package **manager** for Linux that uses the `RPM` package manager to manage packages in the `.rpm` file format.

| CMD                          | DESC                                                            |
| ---------------------------- | --------------------------------------------------------------- |
| `yum upgrade -y`             | update version of all package and **removes** outdated packages |
| `yum update -y`              | update version of all package                                   |
| `yum upgrade -y package`     | Update a package                                                |
| `yum search string`          | Search for string                                               |
| `yum info`                   | Display all info                                                |
| `yum info package`           | Display info of a package                                       |
| `yum info "bash*"`           | Display info of a package matching the pattern                  |
| `yum list installed`         | List all installed package                                      |
| `yum list installed package` | List an installed package                                       |
| `yum install -y package`     | Install package                                                 |
| `yum remove package`         | Remove package                                                  |

---

### `dnf`: RHEL 8 / CentOS 8 & Later

- `dnf`:
  - `Dandified Yum`
  - a package manager for Linux systems that uses `RPM` packages

| CMD                          | DESC                          |
| ---------------------------- | ----------------------------- |
| `dnf upgrade -y`             | update version of all package |
| `dnf upgrade -y package`     | Update a package              |
| `dnf search string`          | Search for string             |
| `dnf info package`           | Display info                  |
| `dnf list installed`         | List all installed packages   |
| `dnf list installed package` | List an installed package     |
| `dnf install -y package`     | Install package               |
| `dnf remove package`         | Remove package                |

- **Keep Your System Clean**
  - `dnf autoremove`

---

### Example: `DNF` install `nginx`

```sh
# search package in the remove repositories
# return a list of packages container the target packages name.
dnf search nginx

# query the package's information
dnf info nginx

# install nginx as super user
sudo dnf install -y nginx

# confirm pacakge has been installed
dnf list installed nginx
which nginx

# remove package
sudo dnf remove -y nginx
```

---

## `DEB` Distro

### `APT`: Advanced Packaging Tool

- `apt`
  - Combination of `apt-cache` and `apt-get`

| CMD                          | DESC                                     |
| ---------------------------- | ---------------------------------------- |
| `apt`                        |                                          |
| `apt-get update`             | Update the local list of remote packages |
| `apt-get upgrade -y`         | Upgrade all installed packages           |
| `apt-get install -y package` | Install package                          |
| `apt-get remove package`     | Remove package, leaving configuration    |
| `apt-get purge package`      | Remove package, deleting configuration   |
| `apt-cache search string`    | Search for string                        |
| `apt-cache show package`     | Display information about the package    |
| `apt upgrade -y`             |                                          |
| `apt update -y`              |                                          |
| `apt search package`         |                                          |
| `apt install -y package`     |                                          |
| `apt purge package`          |                                          |
| `apt list --installed`       | List all packages                        |

- **Keep Your System Clean**
  - `apt autoremove`

---

### `dpkg`: low-level package manager

- `DPKG`
  - `Debian Package Manager`
  - a low-level package manager
  - allows users to install, build, remove, and manage Debian packages on Debian-based systems.

| CMD                     | DESC                           |
| ----------------------- | ------------------------------ |
| `dpkg -l`               | List the installed packages    |
| `dpkg -S /path/to/file` | List the file's package        |
| `dpkg -L package`       | List all the files in package  |
| `dpkg -i package.deb`   | Install the package            |
| `dpkg -r package`       | Remove (uninstall) the package |

---

[TOP](#linux---package)
