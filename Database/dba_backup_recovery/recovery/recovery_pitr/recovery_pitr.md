# Recovery - `Point-in-Time Recovery`

[Back](../../index.md)

- [Recovery - `Point-in-Time Recovery`](#recovery---point-in-time-recovery)
  - [Point-in-time Recovery](#point-in-time-recovery)
  - [Terminology](#terminology)
  - [Specifying the Recovery Point in Time](#specifying-the-recovery-point-in-time)

---

## Point-in-time Recovery

- `Point-in-time Recovery`

- Benefits:

  - Quick recovery of one or more objects to an earlier time, without affecting the state of the other tablespaces and objects in the database.
  - No effect on other objects

- Recovery scope:

  - `Database point-in-time recovery (DBPITR)`(`incomplete recovery`):
    - To recover of an **entire database** to a specified **past target time**, SCN, or log sequence number
    - To **migrate** a database to a **different platform** by creating a new database on the destination platform and performing a transport of **all the user** tablespaces, but **excluding the `SYSTEM` tablespace**
  - `Tablespace point-in-time recovery (TSPITR)`:
    - To recover one or more contained **tablespaces** to an earlier point in time
  - `Table point-in-time recovery (TPITR)`:
    - To recover one or more **tables** or **table partitions** to an earlier point in time

---

## Terminology

- `Target time`:
  - The **point in time** or **SCN** that an object will **be recovered to**
- `Recovery set`:
  - `data files` composing the **tablespaces to be recovered**
- `Auxiliary set`:
  - Required `data files` that are not part of the recovery set. It typically **includes**:
    - A copy of `SYSTEM` tablespace
    - `Data files` that contain **undo segments** from the target instance
    - In some cases, a `temporary tablespace`, used during the **export** of database objects from the `auxiliary instance`
- `Auxiliary destination`:
  - A **location on disk** that can be used to store any of the `auxiliary set` **data files**, **control files**, and **online logs** of the `auxiliary instance` during `PITR`.
  - Files stored in the auxiliary destination **can be deleted** after PITR is complete.

---

## Specifying the Recovery Point in Time

- Specify Point in Time by:
  - `UNTIL SCN integer`:
    - `system change number (SCN)`
    - The SCN is an **upper**, **noninclusive** limit.
  - `UNTIL TIME 'date string'`:
    - The time inthe date format:
      - Of the `NLS_LANG` and `NLS_DATE_FORMAT` **environment variables**,
      - Date constants
        - e.g., `SYSDATE -5` = 5 days earlier than the system date
  - `UNTIL SEQUENCE integer (THREAD integer)`:
    - The log sequence number and thread number
    - RMAN selects only files that it **can use** to restore or recover up to but **not including** the specified sequence number.

---

[TOP](#recovery---point-in-time-recovery)
