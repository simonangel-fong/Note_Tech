# Bootstrap Table - Method方法

[返回Bootstrap Table首页](../bootstrap_table_index.md)

## 目录

- [Bootstrap Table - Method方法](#bootstrap-table---method方法)
  - [目录](#目录)
    - [获取一行的数据](#获取一行的数据)
    - [获取(多)行的数据](#获取多行的数据)
    - [刷新表数据](#刷新表数据)
 
### 获取一行的数据

`<table>.bootstrapTable('getRowByUniqueId', <index>)`

- 参数`<index>`是数字类型，是指定数据所在的行数;
- 返回值是对象`{}`.

### 获取(多)行的数据

`<table>.bootstrapTable('getSelections')`

- 该方法需要结合`data-click-to-select="true"`的属性使用;
- 在数据行被选取后，使用该方法会返回数据；
- 返回值是数列`[]`.

### 刷新表数据

`<table>.bootstrapTable('refresh');`


[回到目录](#目录)

***

[返回Bootstrap Table首页](../bootstrap_table_index.md)
