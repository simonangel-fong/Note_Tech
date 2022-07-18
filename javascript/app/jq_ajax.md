# jQuery类 - Ajax

[返回Javascript首页](../js_index.md)

### 目录


- [jQuery类 - Ajax](#jquery类---ajax)
    - [目录](#目录)
  - [实例：get/post方法](#实例getpost方法)
  - [实例: csrftoken跨站请求伪造](#实例-csrftoken跨站请求伪造)
  

## 实例：get/post方法

- 使用`$.get`或`$.post`方法提交

```javascript

  var data = {};
  data["csrfmiddlewaretoken"] = {{ csrf_token | safe }};    //获取token
  data["data"] = $("#").attr("data-**");      //获取提交的数据

  $.post(
    post_url,
    data,
    function (resp_data) {      //resp_data是反馈的数据
      switch (resp_data["info"]) {
        case "success":
          //处理成功的信息message
          break;

        case "error":
          //处理成功的信息message
          break;

        default:
        //处理数据data
      }
    }
  );

```

- Django视图 Views: 处理提交数据

  - 视图处理：
  - 1. 判断token;
  - 2. 判断提交是否post/get;
  - 3. 获取`request.POST["data"]`
  - 4. 将提交的JSON字符串转为Dict`json.loads()`
  - 5. 处理数据

```python

def 函数(request):
  data = {}     #定义data，用于返回数据
  if request.method == "POST":
    req_data = request.POST["data"]
    load_data = json.loads(req_data)
    # do something about data
    # 1.自定义函数，根据模型提取数据

    # 2.自定义函数，根据模型转换字段类型
  
  print(data)       #在终端显示反馈数据
  return JsonResponse(data, safe=False)     #返回json对象

```

***

## 实例: csrftoken跨站请求伪造

- 提交: template -> view 
  - 单一数据：`{"csrfmiddlewaretoken":"","data":{}}`
  - 多个数据：`{"csrfmiddlewaretoken":"","data":[{},{}]}`

***

[返回Javascript首页](../js_index.md)
