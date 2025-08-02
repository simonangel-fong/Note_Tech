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

CREATE LOGIN Grafana WITH PASSWORD = 'SecurePassword';
GO

CREATE USER Grafana FOR LOGIN Grafana;
GO


GRANT SELECT ON DATABASE::Business TO Grafana;
GO
