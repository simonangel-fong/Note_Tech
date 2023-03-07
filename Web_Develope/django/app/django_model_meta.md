# Django - model:_meta API

[返回Django首页](../django_index.md)

## 目录
 - [Django - model:FileField](#django---model_meta-api)
   - [目录](#目录)
     - [实例:遍历模型的所有字段](#实例遍历模型的所有字段)
     - [实例:返回字段类型](#实例返回字段类型)


### 实例:遍历模型的所有字段

`Model._meta.fields`: 模型所有字段的集合

`.attname`: 字段名称

- 根据模型字段名，提取数据

```python
def submitDict_to_modelDict(submit_dict, Model):

    data = {}
    for field in Model._meta.fields:                #遍历模型字段
        if field.attname in submit_dict.keys():            #如果提交的数据对象含有模型字段的键
            data[field.attname] = submit_dict[field.attname]       #将post键值赋给data
    
    return data
```

[回到目录](#目录)

***

### 实例:返回字段类型

- 根据模型字段类型，转换字典的值的类型

`.get_internal_type`:字符串，返回字段类型名称；

```python
def submitDict_tran_fieldType(dict_data, Model):
    data = dict_data

    for field in Workout._meta.fields:                  #_meta.fields返回所有字段名
        # print(field.get_internal_type())
        if field.get_internal_type() == "DecimalField":     #get_internal_type()返回字段类型，是字符串
            data[field.attname] = float(data[field.attname])
        if field.get_internal_type() == "IntegerField":
            data[field.attname] = int(data[field.attname])
    return data
```

[回到目录](#目录)

***

[返回Django首页](../django_index.md)
