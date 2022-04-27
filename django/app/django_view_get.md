# Django - 视图：查找数据

[返回Django首页](../django_index.md)

## 目录

- [Django - 视图：查找数据](#django---视图查找数据)
  - [目录](#目录)
  - [总结：](#总结)
      - [获取单个对象](#获取单个对象)
  - [前提：模型model](#前提模型model)
  - [方法get()：获取单个对象](#方法get获取单个对象)
    - [常用代码](#常用代码)
  - [方法all()：获取所有对象](#方法all获取所有对象)
  - [方法value()：获取多个对象](#方法value获取多个对象)

***

## 总结：

#### 获取单个对象
```python
def <function>(request):
    ...
    try:
        om = <object_model>.objects.get(field_name=value)
    except ObjectDoesNotExist:      #异常：对象不存在
        pass        #异常处理
    except MultipleObjectsReturned:     #异常：多个对象
        pass        #异常处理
    ...
```

***

## 前提：模型model

以下方法会调用`object_model`.

```python
from django.db import models

class <object_model>(models.Model):
    field_name = ...
    field_name = ...

```

***

## 方法get()：获取单个对象

- **命令**：
```python
om = <object_model>.objects.get(field_name=value)
```
>**代码说明**：
>- 返回值：符合条件的对象；
>- 适用情况仅限于查询**一个**对象的情况，否则会异常；
>- `<object_model>.objects.get(field_name=value)`相当于`<object_model>.objects.filter(field_name=value).get()`

### 常用代码

```python
def <function>(request):
    ...
    try:
        om = <object_model>.objects.get(field_name=value)
    except ObjectDoesNotExist:      #异常：对象不存在
        pass        #异常处理
    except MultipleObjectsReturned:     #异常：多个对象
        pass        #异常处理
    ...
```

>**代码说明**：
>- 使用`try except`，以防出现异常。
>- 常见异常
>   - `ObjectDoesNotExist`：**没有**满足查询条件的对象；
>   - `MultipleObjectsReturned`：有**多个**满足查询条件的对象

[回到目录](#目录)

***

## 方法all()：获取所有对象

- **命令**
```python
oms = <object_model>.objects.all()
```

## 方法value()：获取多个对象


