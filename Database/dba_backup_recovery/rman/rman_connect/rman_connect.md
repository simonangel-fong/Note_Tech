## `RMAN` - Connect

[Back](../../index.md)

---

## Connect

- Start `RMAN` and authentication

```sh
rman target '"username@service_name as sysdba|sysbackup"'

rman target username@service_name
rman target backupadmin@pdb1

```

- Connecting and authenticate

```sql
-- Connecting With OS Authentication - Implicit
connect target /

-- Connecting with OS Authentication - Explicit
connect target "/ as sysdba"

-- Connecting to the Root with a Net Service Name
rman target common_user@service_name;
rman target c##bkuser@sales;

-- Connecting with Password File Authentication
connect target "backupadmin@pdb1 AS SYSBACKUP";
```
