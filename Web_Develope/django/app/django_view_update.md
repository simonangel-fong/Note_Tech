# Django - 视图：修改数据

[返回Django首页](../django_index.md)

## 目录

- [Django - 视图：修改数据](#django---视图修改数据)
  - [目录](#目录)
  - [总结：](#总结)
      - [实例：修改数据update](#实例修改数据update)

***

## 总结：

#### 实例：修改数据update

```python

def workout_ajax_update(request):
    data = {}

    if request.method == "POST":
        post_data = json.loads(request.POST["data"])

        submit_dict = submitDict_to_modelDict(post_data, Workout)     #自定义函数，根据模型提取数据为字典
        submit_data = submitDict_tran_fieldType(submit_dict, Workout)     #自定义函数，根据模型定义转换字典值的类型

        if Workout.objects.filter(wk_date=submit_data["wk_date"]).exists():           #判断是否有相同date的数据
            try:
                callback = Workout.objects.filter(wk_date=submit_data["wk_date"]).update(**post_data)
                data["info"] = "success"
                data["data"] = "Successfully update " + str(callback) + " record(s) !"                 #保存信息
            except Exception as error:
                data["info"] = "error"
                data["data"] = str(error)                  #返回异常信息
        else:
            data["info"] = "error"
            data["data"] = "Database has no workout record with the same date!"

    print(data)
    return JsonResponse(data, safe=False)

```

***




