# Prometheus - Grafana Data Source: SQL Server

[Back](../../index.md)

- [Prometheus - Grafana Data Source: SQL Server](#prometheus---grafana-data-source-sql-server)
  - [Data Source: SQL Server](#data-source-sql-server)

---

## Data Source: SQL Server

- Create SQL Server using Docker compose

- Create schema

```sql
-- sql server
CREATE DATABASE Business
GO

USE [Business];
GO

CREATE TABLE Product
(
    Id INT NOT NULL PRIMARY KEY IDENTITY(1,1),
    Name varchar(200) not null
)
GO

Create Table Sales
(
    Id INT NOT NULL PRIMARY KEY IDENTITY(1,1),
    ProductId INT NOT NULL,
    Amount INT NOT NULL,
    SalesDateTime DATETIME NOT NULL
)
GO

INSERT INTO Product (Name) VALUES('Jeans')
INSERT INTO Product (Name) VALUES('Shirts')
GO

USE [master];
GO

CREATE LOGIN Grafana WITH PASSWORD = 'SecurePassword';
GO

CREATE USER Grafana FOR LOGIN Grafana;
GO


GRANT SELECT ON DATABASE::Business TO Grafana;
GO

```

- Mock data

```sql
insert into Sales (ProductId, Amount, SalesDateTime) values (1, 3, '2024-03-08');
insert into Sales (ProductId, Amount, SalesDateTime) values (2, 1, '2024-06-11');
insert into Sales (ProductId, Amount, SalesDateTime) values (1, 2, '2024-05-23');
insert into Sales (ProductId, Amount, SalesDateTime) values (2, 2, '2024-05-07');
insert into Sales (ProductId, Amount, SalesDateTime) values (1, 1, '2024-05-01');
-- ...
```

- Query in Grafana Dashboard

```sql
SELECT
	$.__time(S.SalesDateTime)  -- filter time range dynamically
	, P.Name
	, SUM(S.Amount) as Total
FROM Product AS P
INNER JOIN Sales as S
On P.Id = S.ProductId
WHERE p.name = "Jeans"
GROUP BY S.SalesDateTime, P.Name
HAVING $.__time(S.SalesDateTime)
;
```
