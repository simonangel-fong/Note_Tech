# Docker - Oracle Database

[Back](./index.md)

- [Docker - Oracle Database](#docker---oracle-database)
  - [Pull Image](#pull-image)
  - [Starting an Oracle Database Server Instance](#starting-an-oracle-database-server-instance)
  - [Connecting from within the container](#connecting-from-within-the-container)
  - [Database Alert Logs](#database-alert-logs)
  - [Changing the Default Password for SYS User](#changing-the-default-password-for-sys-user)
    - [Custom Configurations](#custom-configurations)

---

## Pull Image

- ref:

  - https://container-registry.oracle.com/ords/f?p=113:4:104124566835401

- Pull Command for 19c

```sh
docker pull container-registry.oracle.com/database/enterprise:19.3.0.0
```

---

## Starting an Oracle Database Server Instance

- To start an Oracle Database server instance, execute the following command where <oracle-db> is the name of the container:

```sh
docker run -d --name orcl container-registry.oracle.com/database/enterprise:19.3.0.0
# 7c57d8229b8f581b21465b3181ee62ab679f78f7a7d8e17200153c75ceed29d1
```

- Oracle Database server is ready to use when the STATUS field shows (healthy):

```sh
docker ps
```

---

## Connecting from within the container

You can connect to Oracle Database server by executing a SQL\*Plus command from within the container using one of the following commands:

```sh
docker exec -it orcl sqlplus / as sysdba
```

- Discover the mapped port by executing the following command:

```sh
docker port orcl
```

- To connect from outside of the container using SQL\*Plus, execute the following:

```sql
sqlplus sys@orclcdb//localhost:1521 as sysdba
```

---

## Database Alert Logs

- You can access the database alert log using the following command where <oracle-db> is the name of the container:

```sh
docker logs orcl
```

---

## Changing the Default Password for SYS User

On the first startup of the container, a random password will be generated for the database if not provided. The user has to mandatorily change the password after the database is created and the corresponding container is healthy.

Using the docker exec command, change the password for those accounts by invoking the setPassword.sh script that is found in the container. Note that the container must be running. For example:

```sh
docker exec orcl ./setPassword.sh welcome
```

---

### Custom Configurations

Oracle Database server container also provides configuration parameters that can be used when starting the container. Following is the detailed docker run command supporting all custom configurations:

```sh
docker run -d --name <container_name> \
 -p <host_port>:1521 -p <host_port>:5500 \
 -e ORACLE_SID=<your_SID> \
 -e ORACLE_PDB=<your_PDBname> \
 -e ORACLE_PWD=<your_database_password> \
 -e INIT_SGA_SIZE=<your_database_SGA_memory_MB> \
 -e INIT_PGA_SIZE=<your_database_PGA_memory_MB> \
 -e ORACLE_EDITION=<your_database_edition> \
 -e ORACLE_CHARACTERSET=<your_character_set> \
 -e ENABLE_ARCHIVELOG=true \
 -v [<host_mount_point>:]/opt/oracle/oradata \
container-registry.oracle.com/database/enterprise:21.3.0.0

Parameters:
 --name:                 The name of the container (default: auto generated
 -p:                     The port mapping of the host port to the container port.
                         Two ports are exposed: 1521 (Oracle Listener), 5500 (OEM Express)
 -e ORACLE_SID:          The Oracle Database SID that should be used (default:ORCLCDB)
 -e ORACLE_PDB:          The Oracle Database PDB name that should be used (default: ORCLPDB1)
 -e ORACLE_PWD:          The Oracle Database SYS, SYSTEM and PDBADMIN password (default: auto generated)
 -e INIT_SGA_SIZE:       The total memory in MB that should be used for all SGA components (optional)
 -e INIT_PGA_SIZE:       The target aggregate PGA memory in MB that should be used for all server processes attached to the instance (optional)
 -e ORACLE_EDITION:      The Oracle Database Edition (enterprise/standard, default: enterprise)
 -e ORACLE_CHARACTERSET: The character set to use when creating the database (default: AL32UTF8)
 -e ENABLE_ARCHIVELOG:   To enable archive log mode when creating the database (default: false). Supported 19.3 onwards.
 -v /opt/oracle/oradata
                         The data volume to use for the database. Has to be writable by the Unix "oracle" (uid: 54321) user inside the container
                         If omitted the database will not be persisted over container recreation.
 -v /opt/oracle/scripts/startup | /docker-entrypoint-initdb.d/startup
                         Optional: A volume with custom scripts to be run after database startup.
                         For further details see the "Running scripts after setup and on
                         startup" section below.
 -v /opt/oracle/scripts/setup | /docker-entrypoint-initdb.d/setup
                         Optional: A volume with custom scripts to be run after database setup.
                         For further details see the "Running scripts after setup and on startup" section below.
The supported configuration options are:
```

ORACLE_SID

This parameter changes the Oracle system identifier (SID) of the database. This parameter is optional and the default value is set to ORCLCDB.

ORACLE_PDB

This parameter modifies the name of the pluggable database (PDB). This parameter is optional and the default value is set to ORCLPDB1.

ORACLE_PWD

This parameter modifies the password for the SYS, SYSTEM and PDBADMIN users. This parameter is optional and the default value is randomly generated. This password can be changed later as described in the section titled "Changing the Default Password for SYS User".

INIT_SGA_SIZE

This parameter modifies the memory in MB that should be used for all SGA components. This parameter is optional, and the default value is calculated during database creation if it isn¿t provided. The user can refer to the section titled ¿Setting the SGA and PGA memory¿ for more details.

INIT_PGA_SIZE

This parameter modifies the target aggregate memory in MB that should be used for all server processes attached to the instance. This parameter is optional, and the default value is calculated during database creation if it isn¿t provided. The user can refer to the section titled ¿Setting the SGA and PGA memory¿ for more details.

ORACLE_EDITION

This parameter modifies the edition of the database when the container is started for the first time. This parameter is optional and the two values are enterprise or standard. The default value is enterprise.

ORACLE_CHARACTERSET

This parameter modifies the character set of the database. This parameter is optional and the default value is set to AL32UTF8.

ENABLE_ARCHIVELOG

This parameter enables the ARCHIVELOG mode while creating the database for the first time. Default value of this parameter is false.

---

[TOP](#docker---oracle-database)
