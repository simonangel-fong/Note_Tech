# Flashback - `Flashback Version Query`

[Back](../../index.md)

- [Flashback - `Flashback Version Query`](#flashback---flashback-version-query)
  - [`Flashback Version Query`](#flashback-version-query)

---

## `Flashback Version Query`

- `Flashback Version Query`:

  - enables you to use the `VERSIONS` clause to **retrieve all the versions of the rows** that exist between two points in time or two SCNs.
  - Used to **audit** the rows of a table and information about the transactions that affected the rows. 用于审计影响行的交易信息.

- **Characteristics**:

  - The rows returned **represent a history of changes for the rows** across transactions. 返回行历史
    - retrieves **only committed** data.
      - **Uncommitted** row versions within a transaction are **not** shown.
    - returned also **include deleted and subsequently reinserted** versions of the rows. 包括已删除和重新插入的行数据
  - can then use the returned `transaction identifier` (the `VERSIONS_XID`
    pseudocolumn) to perform **transaction mining** by using `LogMiner` or to perform a Flashback `Transaction Query`. 可用于数据挖掘
  - Certain maintenance operations, such as a segment shrink, may **move table rows across blocks**.
    - In this case, the `version query` **filters out** such phantom(虚构的) versions because the row data remains the same. 会自动过滤虚幻的版本

- `SELECT ... VERSION` clause:

  - **cannot** be used to query `external tables`, `temporary tables`, `fixed tables`, or `views`.
    - However, you can **create a view** with the `VERSIONS` clause.
  - cannot produce versions of rows across the `DDL` statements that change the structure of the corresponding tables.
    - the query **stops** producing rows after it **reaches a time** in the past when the table structure was **changed**. 不能跨 DDL 查询, 返回结果只反映同一个 DDL.

- Example:

```sql
SELECT versions_xid, salary FROM employees
VERSIONS BETWEEN TIMESTAMP <tl> and <t2>
WHERE employee id = 200;
```

---

[TOP](#flashback---flashback-version-query)
