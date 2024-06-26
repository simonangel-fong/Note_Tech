# Backup and Recovery

## DBA Responsibilites

- Protect the database from failure wherever possible
- Increase the `mean time between failures (MTBF)`
  - Ensures that hardware is as reliable as possible.
  - operating system maintenance is performed in a timely manner.
  - advanced configuration options ( RAK and Oracle Data Guard )
- Protect critical components by using **redundancy**
- Decrease the `mean time to recover (MTTR)`
  - practicing recovery procedures in advance and configuring backups so that they are readily available when needed
- Minimize the loss of data
  - `Archive log files`
  - `Flashback` technology

---

## Categories of Failure

- **Statement failure**:
  - A single database operation (select, insert, update, or delete) fails.
  - e.g.:
    - invalid data
    - insufficient privileges
    - space allocation
    - logic errors
  - dba sovle these without any retoring backup.
- **User process failure**:
  - A single database session fails.
    - e.g.,
      - abnormal disconnect.
      - session abnormal terminated.
      - program error to terminates the session.
    - DBA action is not needed.
- **Network failure**:
  - Connectivity to the database is lost.
  - e.g., listener fails, nic fails, network fails
  - It should be solved by network people.
- **User error**:
  - A user successfully completes an operation, but the operation (dropping a table or entering bad data) is incorrect.
  - e.g., inadvertently deletes or modifies data, drop data.
  - user can rollback a transaction, DBA can recover from recycle bin or can recover from backup.
- **Instance failure**:
  - The database instance shuts down unexpectedly.
  - e.g., power outage, hardware failure, bg processes failure, procedure shutdown.
- **Media failure**:
  - A loss of any file that is needed for database operation (that is, the files have been deleted or the disk has failed).
  - e.g., failure of disk drive, disk controller, failure of a critical file.

---

## incomplete vs. complete recovery.

- Both terms are used to describe different methods of recovering the database from media failure That is when you lose actual database data files and not just restart your Oracle instance after it has crashed.
- `complete recovery`: you bring your database to the state where it is fully up to date including all completed transactions and database modifications up to the present date and time.
- `incomplete recovery`: which brings your database to a specific point in time in the test.
  - This is also known as `point in time recovery`, or `PITR`

![diagram_completed](./pic/diagram_complete.png)

---

## redo logs and archived redo logs

- the `Oracle redo logs` contain a **log of all transactions** which have been applied to your Oracle database. Every single insert, delete, or update statement is recorded in the redo logs.
- The **Oracle database** requires at least two Redo Log Files at any given time, as it writes to them in a cyclic manner.
- The database writes to the first Redo Log File, and once that Redo Log File is filled up, the database will start writing to the second Redo Log File. This is called a Redo Log switch
