# Django - 视图：增加数据

[返回Django首页](../django_index.md)

## 目录

- [Django - 视图：增加数据](#django---视图增加数据)
  - [目录](#目录)
  - [总结：](#总结)
  - [前提：模型model](#前提模型model)
  - [方法：save()](#方法save)
    - [无参数](#无参数)
    - [参数 force_insert](#参数-force_insert)
      - [实例:添加新数据: save](#实例添加新数据-save)
  - [方法：create()](#方法create)
    - [参数**kwarg](#参数kwarg)

***

## 总结：



***

## 前提：模型model

以下方法会调用`object_model`.

```python
from django.db import models

class object_model(models.Model):
    field_name = ...
    field_name = ...

```

***

## 方法：save()

- 效果：
  - 当实例是新的对象时，相当于一条`INSERT`的SQL语句。
  - 当实例是数据表内的对象时，相当于一条`update`的SQL语句。


### 无参数

- 思路：
  - 1. 创建模型的一个实例；
  - 2. 对模型各个字段赋值；
  - 3. 使用save方法保存。

**views_py:**
```python
def <function>(request):
  ...
  md = object_model()  
  //对模型各个字段赋值
  md.save()
  ...
```

或

```python
def <function>(request):
  ...
  md = object_model(
    field_name=value,
    field_name=value,
    ...
    )  
  md.save()
  ...
```

### 参数 force_insert

- 参数类型：布尔

```python
def <function>(request):
  ...
  md = object_model(
    field_name=value,
    field_name=value,
    ...
    )  
  md.save(force_insert=true)
  ...
```

>适用情况：
当新添加的对象有手动输入的主键，`save()`会发生与现存的对象的主键重复。由于主键要唯一，则会抛出异常IntegrityError。
使用该参数时，会忽略该异常，始终创建新对象。

[回到目录](#目录)

***

#### 实例:添加新数据: save

```python
def workout_ajax_add(request):
    data = {}

    if request.method == "POST":
        post_data = json.loads(request.POST["data"])

        submit_dict = submitDict_to_modelDict(post_data, Workout)   #自定义函数, 根据模型字段提取数据
        submit_data = submitDict_tran_fieldType(submit_dict, Workout)   #自定义函数, 根据模型的定义转换字段值的类型

        if Workout.objects.filter(wk_date=submit_data["wk_date"]).exists():           #检查是否有相同date的数据
            data["info"] = "error"
            data["data"] = "Database has contain the workout record with the same date!"
        else:
            try:
                wk = Workout(**submit_data)     #根据dict生成model
                wk.save()     #保存对象
                data["info"] = "data"
                data['data']  =  list(Workout.objects.values().all().order_by("wk_date"))               #生成返回数据
            except Exception as error:                      #异常时
                data["info"] = "error"
                data["data"] = str(error)                  #返回异常信息
    
    print(data)
    return JsonResponse(data, safe=False)

```

[回到目录](#目录)

***

## 方法：create()

### 参数**kwarg

参数类型：字典

```python
def <function>(request):
  ...
  md = object_model.objects.create(
    field_name=value, 
    field_name=value, 
    ...
    )
  ...
```

或

```Django
def <function>(request):
  ...
  object_dict = {
    "field_name":value, 
    "field_name":value, 
    ...
    }
  md = object_model.objects.create(**object_dict)
  ...
```

>代码说明：
>1. 返回的md是create后的对象；
>2. 星号**不能省略。

[回到目录](#目录)

***





