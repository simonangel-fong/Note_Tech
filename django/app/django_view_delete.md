# Django - 视图：删除数据

[返回Django首页](../django_index.md)

## 目录

- [Django - 视图：删除数据](#django---视图删除数据)
  - [目录](#目录)
  - [总结：](#总结)
      - [实例：删除数据delete](#实例删除数据delete)

***

## 总结：


#### 实例：删除数据delete

```python

def workout_ajax_delete(request):
    data = {}

    if request.method == "POST":
        req_data = request.POST["data"]
        load_data = json.loads(req_data)
        
        i = 0
        try:
            for row in load_data:
                index = Workout.objects.filter(wk_date=row["wk_date"]).delete()[0]
                i += index
            data["info"] = "success"
            data["data"] = "Successfully delete " + str(i) + " record(s)."
        except Exception as e:
            data["info"] = "error"
            data["data"] = str(e)
    
    print(data)
    return JsonResponse(data, safe=False)
```

***
