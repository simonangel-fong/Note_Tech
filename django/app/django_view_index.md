# Django - 视图：QuerySet

[返回Django首页](../django_index.md)

#### 目录

- [Django - 视图：QuerySet](#django---视图queryset)
      - [目录](#目录)
      - [总结](#总结)
      - [QuerySet对象](#queryset对象)
      - [QuerySet的方法](#queryset的方法)
      - [QuerySet的处理](#queryset的处理)

***

#### 总结



***

#### QuerySet对象
- 对应关系：
  |Django对象|数据库|SQL|
  |---|---|---|
  | 一个模型类 model class | 一个数据表 database table ||
  |一个模型类的实例instance|一个特定记录record||
  |一个QuerySet类实例|一系列的数据库对象a collection of objects|一条`select`SQL语句|
  |`filters`方法||`where`和`limit`的SQL语句|

[回到目录](#目录)

***

#### QuerySet的方法

- QuerySet的方法有两类：
  - 返回新的QuerySet；
  - 返回非QuerySet；

- 链式filter：在后的方法是在在前的方法返回QuerySet的基础上执行。

- 方法不会马上执行，只会在被evaluated的时候才会执行。
- 参数
  - 数据表字段名field
  - 限定参数，如exact,contains等

[回到目录](#目录)

***

#### QuerySet的处理

- 遍历QuerySet的方法：`for in`语句

```python
#使用filter方法获取QuerySet实例
<instance> = <models>.objects.filter(**kwargs)       
#遍历QuerySet实例
for row in <instance>:      
    pass
```

[回到目录](#目录)

***
