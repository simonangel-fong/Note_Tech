```sh
sudo su - oracle
. oraenv
sqlplus / as sysdba
```

```sql
-- drop pdb1
ALTER PLUGGABLE DATABASE pdb1 CLOSE;
DROP PLUGGABLE DATABASE pdb1 INCLUDING DATAFILES;

-- Create pdb1
CREATE PLUGGABLE DATABASE pdb1 ADMIN USER pdb1_adm IDENTIFIED BY QazWsx_12345#
FILE_NAME_CONVERT=('/u01/app/oracle/oradata/ORCL/pdbseed/','/u01/app/oracle/oradata/ORCL/pdb1/');

ALTER PLUGGABLE DATABASE pdb1 OPEN;
SELECT pdb_name, status FROM DBA_PDBS;

-- drop pdb2
ALTER PLUGGABLE DATABASE pdb2 CLOSE;
DROP PLUGGABLE DATABASE pdb2 INCLUDING DATAFILES;

-- Create pdb2
CREATE PLUGGABLE DATABASE pdb2 ADMIN USER pdb2_adm IDENTIFIED BY QazWsx_12345#
FILE_NAME_CONVERT=('/u01/app/oracle/oradata/ORCL/pdbseed/','/u01/app/oracle/oradata/ORCL/pdb2/');

ALTER PLUGGABLE DATABASE pdb2 OPEN;
SELECT pdb_name, status FROM DBA_PDBS;

exit
```

- tnsname:

```sh
vi $ORACLE_HOME/network/admin/tnsnames.ora
```

```config
PDB1=
  (DESCRIPTION =
    (ADDRESS_LIST =
      (ADDRESS = (PROTOCOL = TCP)(HOST = oracledb)(PORT = 1521))
    )
  (CONNECT_DATA =
    (SERVICE_NAME = pdb1)
  )
)

PDB2=
  (DESCRIPTION =
    (ADDRESS_LIST =
      (ADDRESS = (PROTOCOL = TCP)(HOST = oracledb)(PORT = 1521))
    )
  (CONNECT_DATA =
    (SERVICE_NAME = pdb2)
  )
)
```

- Test

```sh
tnsping pdb1
tnsping pdb2
```

- If account lock

```sh
. oraenv
sqlplus / as sysdba
```

```sql
ALTER USER SYSTEM ACCOUNT UNLOCK;
ALTER USER SYSTEM IDENTIFIED BY QazWsx_12345#;
```