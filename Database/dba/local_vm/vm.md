# DBA - Local Virtual Machine

[Back](../index.md)

- [DBA - Local Virtual Machine](#dba---local-virtual-machine)
  - [Oracle VM VirtualBox](#oracle-vm-virtualbox)
  - [OS: Oracle Linux 7.6](#os-oracle-linux-76)
    - [Enable clipboard](#enable-clipboard)
    - [Shared Folder](#shared-folder)
    - [Map Local](#map-local)
  - [Download Oracle Database](#download-oracle-database)
  - [Prerequisites](#prerequisites)
    - [install package for 19c](#install-package-for-19c)
    - [Additional Configurations](#additional-configurations)
  - [Configure Environment Variables](#configure-environment-variables)
  - [](#)

---

## Oracle VM VirtualBox

- Website:
  - https://www.virtualbox.org/

---

## OS: Oracle Linux 7.6

- Website:

  - https://edelivery.oracle.com/osdc/faces/Home.jspx

- Version:

  - `Oracle Linux 7.6.0.0.0`
  - `x86 64 bit`

- File:
  - Oracle Linux Release 7 Update 6 for x86 (64 bit), 4.3 GB
  - V980739-01.iso

```sh
# root pwd: oracle01vm
# admin user: sfong
#     pwd: S!3
```

---

---

### Enable clipboard

```sh
# switch root account
su root
# input password

# overwrite configure file
vi /etc/selinux/config

# locate the line:
#   SELINUX=enforcing
# Overwrite into:
#   SELINUX=disable
# command to save and quit editor: :wq

# reboot vm after configure
reboot
```

- Insert Guest Additions CD image...

- Reboot

- Test Clipboard

---

### Shared Folder

- Virtual Box > Settings > Shared Folders > Add new shared folder.

```sh
# switch root
su root

# add admin into vboxsf group
usermod -a -G vboxsf user_name

# reboot vm
reboot
```

---

### Map Local

- Edit hosts files

```sh
# switch to root
su root

# get host name
hostname    # test.com

# get ip address
ifconfig    # 192.168.0.42

# add new line to host file
#   <IP-address>  <fully-qualified-machine-name>  <machine-name>
vi /etc/hosts
# 192.168.0.42  test.com test

# test mapping
ping test
```

---

## Download Oracle Database

- Oracle Database 19c for Linux x86-64
  - zip file version

---

## Prerequisites

### install package for 19c

- ref:
  - https://oracle-base.com/articles/19c/oracle-db-19c-installation-on-oracle-linux-9#oracle_installation_prerequisites

```sh
# switch to root
su root

# Automatic Setup package
yum install -y oracle-database-preinstall-19c

# verify installation
id oracle   # package will create a user oracle with different groups

```

---

### Additional Configurations

```sh
# switch to root
su root

# create directory where the Oracle software will be installed
mkdir -p /u01/app/oracle/product/19.0.0/dbhome_1
mkdir -p /u02/oradata

# Change ownership of directories to user oracle and group oinstall
chown -R oracle:oinstall /u01 /u02

# Change permission of directories
# owner and group can read, write, and execute.
# others can read and execute, but cannot write.
chmod -R 775 /u01 /u02

# disable firewall
# only for training. Don't in production.
systemctl stop firewalld
systemctl disable firewalld

# change pwd for user oracle
passwd oracle   #orcl_12345

# add oracle into vboxsf group
usermod -a -G vboxsf oracle
id oracle
# uid=54321(oracle) gid=54321(oinstall) groups=54321(oinstall),976(vboxsf),54322(dba),54323(oper),54324(backupdba),54325(dgdba),54326(kmdba),54330(racdba)
```

---

## Configure Environment Variables

- Note: bash_profile is a configuration file defines tasks that the shell executes for every user who logs in.

- `ORACLE_BASE`:

  - Specifies the base of the Oracle directory, `/u01/app/oracle`

- `ORACLE_HOME`:

  - Specifies the directory containing the Oracle software , `$ORACLE_BASE/product/19.0.0/dbhome_1`

- `ORACLE_SID`:

  - Specifies the Oracle system identifier, `orcl`
  - Note: `ORACLE_SID` is a **unique name** for an Oracle database instance on a specific host

- `ORACLE_UNQNAME`:

  - is an operating system environment variable that holds the database's unique name value, `orcl`

- In single instance database
  - `ORACLE_SID`= instance name = `ORACLE_UNQNAME` = db_name

---

- Log in as user oracle

```sh
# Create a "scripts" directory.
mkdir /home/oracle/scripts

# Create an environment file called "setEnv.sh".
cat > /home/oracle/scripts/setEnv.sh <<EOF
# Oracle Settings
export TMP=/tmp
export TMPDIR=\$TMP

export ORACLE_HOSTNAME=oracle9.localdomain
export ORACLE_UNQNAME=orcl
export ORACLE_BASE=/u01/app/oracle
export ORACLE_HOME=\$ORACLE_BASE/product/19.0.0/dbhome_1
export ORA_INVENTORY=/u01/app/oraInventory
export ORACLE_SID=orcl
export PDB_NAME=pdb1
export DATA_DIR=/u02/oradata

export PATH=/usr/sbin:/usr/local/bin:\$PATH
export PATH=\$ORACLE_HOME/bin:\$PATH

export LD_LIBRARY_PATH=\$ORACLE_HOME/lib:/lib:/usr/lib
export CLASSPATH=\$ORACLE_HOME/jlib:\$ORACLE_HOME/rdbms/jlib
EOF
```

- Add a reference to the "setEnv.sh" file at the end of the "/home/oracle/.bash_profile" file.

```sh
echo ". /home/oracle/scripts/setEnv.sh" >> /home/oracle/.bash_profile
```

- Create a "start_all.sh" and "stop_all.sh" script that can be called from a startup/shutdown service.
- Make sure the ownership and permissions are correct.

```sh
cat > /home/oracle/scripts/start_all.sh <<EOF
#!/bin/bash
. /home/oracle/scripts/setEnv.sh

export ORAENV_ASK=NO
. oraenv
export ORAENV_ASK=YES

dbstart \$ORACLE_HOME
EOF


cat > /home/oracle/scripts/stop_all.sh <<EOF
#!/bin/bash
. /home/oracle/scripts/setEnv.sh

export ORAENV_ASK=NO
. oraenv
export ORAENV_ASK=YES

dbshut \$ORACLE_HOME
EOF

chown -R oracle:oinstall /home/oracle/scripts
chmod u+x /home/oracle/scripts/*.sh
```

- Logout
- Log in as user oracle

```sh
# verify
echo $ORACLE_HOME   # /u01/app/oracle/product/19.0.0/dbhome_1
```

---

## 

```sh
vi /home/oracle/.bash_profile


export TMP=/tmp
export TMPDIR=$TMP
export ORACLE_HOSTNAME=test.com
export ORACLE_UNQNAME=orcl
export ORACLE_BASE=/u01/app/oracle
export ORACLE_HOME=$ORACLE_BASE/product/19.0.0/dbhome_1
export ORACLE_SID=orcl
export PATH=/usr/sbin:$PATH
export PATH=$ORACLE_HOME/bin:$PATH
export LD_LIBRARY_PATH=$ORACLE_HOME/lib:/lib:/usr/lib
export CLASSPATH=$ORACLE_HOME/jlib:$ORACLE_HOME/rdbms/jlib

```

- Install

```sh
# configuration

# sys/sytem/pdbadmin pwd: QazWsx_12345#
# Oracle Enterprise Manager Database Express URL: https://test.com:5500/em

# command to verify installation
sqlplus 
```

---

[TOP](#dba---local-virtual-machine)
