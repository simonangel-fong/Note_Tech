show parameter db_recovery

----
SELECT flashback_on 
FROM v$database;

----
ALTER DATABASE FLASHBACK ON;

SELECT flashback_on 
FROM v$database;

---

CREATE RESTORE POINT rpl GUARANTEE FLASHBACK DATABASE;

SELECT FLASHBACK_ON
FROM V$DATABASE;

SELECT NAME, SCN, TIME, DATABASE_INCARNATION#,
GUARANTEE_FLASHBACK_DATABASE,STORAGE_SIZE
FROM V$RESTORE_POINT;


SELECT NAME, SCN, TIME, DATABASE_INCARNATION#,
GUARANTEE_FLASHBACK_DATABASE,STORAGE_SIZE
FROM V$RESTORE_POINT
WHERE GUARANTEE_FLASHBACK_DATABASE = 'YES';


-----------

ALTER SESSION set container=orclpdb;

SELECT current_scn
FROM v$database;
-- 8767254
---

SELECT sum (salary) 
FROM hr.employees;
-- 691416

SELECT count (*) 
FROM hr.employees 
WHERE department_id=90;
-- 3

---

update hr.employees
set department_id = 90
where job_id = 'IT_PROG';
/
update hr.employees e
set salary = least(e.salary,
(select (min_salary + max_salary)/2 * 1.10
from hr.jobs j
where j.job_id = e.job_id))
where job_id not like 'AD_%'
/
COMMIT;

SELECT current_scn 
FROM v$database;
-- 8767447

--------

SELECT sum(salary) 
FROM hr.employees;

SELECT count(*) 
FROM hr.employees 
WHERE department_id=90;

---

ALTER SESSION set container=cdb$root;

ALTER PLUGGABLE DATABASE orclpdb CLOSE;

FLASHBACK PLUGGABLE DATABASE orclpdb TO SCN 8767254;

---

ALTER PLUGGABLE DATABASE orclpdb OPEN;

ALTER PLUGGABLE DATABASE orclpdb OPEN RESETLOGS;

---

ALTER SESSION set container = orclpdb;
show con_name

SELECT sum(salary)
FROM hr.employees;

SELECT count(*)
FROM hr.employees
WHERE department_id=90;

---
ALTER SESSION set container=cdb$root;
DROP RESTORE POINT rpl;

SELECT NAME, SCN, TIME, DATABASE_INCARNATION#,
GUARANTEE_FLASHBACK_DATABASE,STORAGE_SIZE
FROM V$RESTORE_POINT;