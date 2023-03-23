-- query the unique rows

DROP TABLE set_a;

CREATE TABLE set_a(
  id int
, name VARCHAR(30)
);

DROP TABLE set_b;

CREATE TABLE set_b(
  id int
, name VARCHAR(30)
);

INSERT INTO set_a VALUES (
  1
, 'AAA'
);

INSERT INTO set_a VALUES (
  2
, 'BBB'
);

INSERT INTO set_b VALUES (
  2
, 'BBB'
);

INSERT INTO set_b VALUES (
  3
, 'CCC'
);

SELECT *
FROM set_a;

SELECT *
FROM set_b;

-- SELECT *
-- FROM set_a a
--   CROSS JOIN set_b b
-- WHERE a.id<>b.id;

SELECT a.id
FROM set_a a
  LEFT JOIN set_b b
  ON a.id =b.id
WHERE b.id IS NULL UNION
  SELECT b.id
  FROM set_a a
    RIGHT JOIN set_b b
    ON a.id =b.id
  WHERE a.id IS NULL;