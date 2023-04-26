# Django - model:FileField

[返回Django首页](../django_index.md)


## 实例:上传并储存文件

- 前段：
  - 使用`input`组件选择上存的文件
- 后端：模型
  - 使用`FileField`字段
- 后端：`view`
  - 从`request.FILES`获取上存的文件
  - 将上存的文件的直接赋值到`FileField`字段，自动储存上存的文件

***

- Html代码

```Html
    <form id="form" action="'music_test_upload'" method="post" enctype="multipart/form-data">
        csrf_token 

        <input id="music_name" name="music_name" class="form-control col-md-6 my-2" />

        <input id="file" type="file" class="form-control col-md-6 my-2" name="upload_file" />
        <button id="btn" class="btn btn-primary" type="submit">submit</button>
    </form>

```

>代码说明:
>- `form`的属性`enctype="multipart/form-data"`：将`input`上存的文件赋值给`request.FILE`; 如果没有该属性, 则不会上存文件。
>- `input`的属性`name="upload_file"`：赋值上存的文件到`request.FILE["upload_file"]`。

***

- model_py

```python
class Music(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='music/') 
```

>代码说明:
>- 创建Music模型，用于储存music的信息。
>- `file`字段是用于储存上存的mp3文件，其字段类型是`FileField()`。
>- `FileField`类型本质上是储存文件的路径。
>- `FileField`类型的`upload_to`属性：指定储存文件的具体文件夹。默认值是`""`,即`settings.MEDIA_ROOT`。
>- 例如：`upload_to='music/'`，即储存上存文件到文件夹`settings.MEDIA_ROOT/music/`。

***

- view_py

```python
def music_test_upload(request):
    context = {}
    html = "AppMusic/test.html"
    data = {}

    if request.method == 'POST' and request.FILES['upload_file']:     #先判断提交的方法和是否有上存文件;
        music_name = request.POST["music_name"]
        upload_file = request.FILES['upload_file']    #获取上存的文件
        upload_file.name = music_name + ".mp3"    #修改上存文件的文件名

        submit_data ={}
        submit_data["name"] = music_name
        submit_data["file"] = upload_file   #直接将上存的文件赋值到FileField类型的字段

        try:
            new_music = Music(**submit_data)
            new_music.save()
            print(new_music.file.url)
            data["success"] = "Successfully create a new record !"                 #保存信息
        except Exception as error:                      #异常时
            data["error"] = str(error)                  #返回异常信息
        
        context['data'] = data
    return render(request,html,context)

```

>代码说明:
>- `new_music.save()`：当保存新建数据时，上存的文件会自动保存到`FileField`指定的文件中。
>- `new_music.file.url`：`FileField`类型的`url`属性是访问上存文件的url。该属性值是：`settings.MEDIA_URL` + `FileField`的`upload_to`属性 + `upload_file.name`。
>- 当在前段需要引用上存文件时，可以直接使用`{{file.url}}`
>- 注意：上存的文件与已存在的文件重名，django会自动修改新上存文件的文件名并自动记录在`FileField`字段中。

***
