# Bootstrap Table - Table Option表格属性

[返回Bootstrap Table首页](../bootstrap_table_index.md)

## 目录

- [Bootstrap Table - Table Option表格属性](#bootstrap-table---table-option表格属性)
  - [目录](#目录)
  - [声明引用BT](#声明引用bt)
  - [每行显示选择框](#每行显示选择框)
  - [指定唯一id绑定的数据字段](#指定唯一id绑定的数据字段)
  - [指定ajax函数](#指定ajax函数)
 
## 声明引用BT

`data-toggle="table"`



## 每行显示选择框

`data-click-to-select="true"`

## 指定唯一id绑定的数据字段

`data-unique-id="id"`

- 该处`"id"`是数据字段中的`id`字段。

## 指定ajax函数

`data-ajax="<function>"`

- \<function\>是js中定义的函数名称。注意，其中不含括小括号和参数。

```html
<table data-ajax="ajax_loadTable"></table>
```

- 初始化页面时，会调用ajax的函数下载数据;
- 当需要刷新数据时，使用`.bootstrapTable('refresh')`方法，会自动调用ajax指定的函数下载数据。

```javascript
  function ajax_loadTable(params) {
    $.get(url_ajax_list).then(function (res) {
      params.success(res)
    })
  }
```

[回到目录](#目录)

***

[返回Bootstrap Table首页](../bootstrap_table_index.md)
