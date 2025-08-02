CREATE USER 'readOnlyUser'  IDENTIFIED BY 'I5FrZOoXKY3sP5s0mbtMcPERFVg=';

GRANT SELECT ON business.* TO 'readOnlyUser'@'localhost';


