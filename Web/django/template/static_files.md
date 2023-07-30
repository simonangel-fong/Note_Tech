# Django - Static Files

[Back](../index.md)

- [Django - Static Files](#django---static-files)
  - [Cheapsheet](#cheapsheet)
  - [Static Files](#static-files)
  - [Configuring Static Files During Development](#configuring-static-files-during-development)
    - [`settings.py`](#settingspy)
    - [Templates](#templates)
    - [Static Files Folder](#static-files-folder)
    - [Alternative](#alternative)
  - [Configuring Static Files During Deployment(IIS)](#configuring-static-files-during-deploymentiis)
    - [`settings.py`](#settingspy-1)
    - [`collectstatic`](#collectstatic)
    - [创建 web.config 文件](#创建-webconfig-文件)
    - [设置 IIS 虚拟目录](#设置-iis-虚拟目录)

---

## Cheapsheet

| Development        | Deployment    | Description                           |
| ------------------ | ------------- | ------------------------------------- |
| `STATIC_URL`       |               | Static files url                      |
| `STATICFILES_DIRS` |               | Global Static File Physical location  |
|                    | `STATIC_ROOT` | Physical location for `collectstatic` |

---

## Static Files

- Static Files

  - additional files to support web application, such as images, JavaScript, or CSS.

- Django 处理静态文件有两种模式

  1. App Static Files, APP 专用，静态文件根据约定的文件结构仅用于对应的 APP;
  2. Global Static Files, 公共静态文件，可以跨 APP 引用。

- Search Order
  - The search starts in the directories listed in `STATICFILES_DIRS`, using the order you have provided.
  - Then, if the file is not found, the search continues in the **static folder of each application**.
  - If you have files with the **same name**, Django will use the **first occurrence** of the file.
  - `STATICFILES_DIRS` > App Static Folder

---

## Configuring Static Files During Development

- Debug mode
  - `settings.DEBUG = True`

### `settings.py`

- 1. `INSTALLED_APPS`: includes `django.contrib.staticfiles`

- 2. `STATIC_URL`：

  - URL to use when referring to static files located in `STATIC_ROOT`.
  - It must end in a **slash** if set to a non-empty value.
    ```py
    # by default
    STATIC_URL = "static/"
    ```
  - 如果缺少该参数，会显示异常`You're using the staticfiles app without having set the required STATIC_URL setting.`

- 3. `STATICFILES_DIRS`: global static files, if applied.

  - list all the directories where Django should look for static files.
  - Example:

    ```python
    from pathlib import Path

    STATICFILES_DIRS = [
        BASE_DIR / 'static',
        BASE_DIR / 'collectstatic',
    ]
    ```

---

### Templates

- In templates, use the **static template tag** to build the URL for the given relative path.

```django
<!-- add at the top of html codes -->
<!-- load static -->

<!-- using static tag to referencing static files -->
<img src="static 'my_app/example.jpg'" alt="My image"> <!-- without {} % signs due to github deploy --->
<link rel="stylesheet" type="text/css" href="static '/Workout/carousel.css' " />
```

---

### Static Files Folder

- Store your static files in a folder called `static` in your app.

- 约定的文件夹结构 app static file

- `<app_name>/`
  - `static/`
    - `<app_name>/`: by putting static files inside another directory named for the application itself, namespace issue can be prevented.
      - css
      - img
      - js

---

### Alternative

- If `INSTALLED_APPS` does not have `django.contrib.staticfiles`, `django.views.static.serve()` can serve static files manually.
- 不推荐

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... the rest of your URLconf goes here ...
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

---

## Configuring Static Files During Deployment(IIS)

- `settings.py`
  - `DEBUG = False`

---

### `settings.py`

- `STATIC_ROOT`

  - The **absolute path to the directory** where collectstatic will collect static files for deployment.

- Example:

  ```py
  STATIC_ROOT = "/var/www/example.com/static/"

  STATIC_ROOT = BASE_DIR / 'collect_static/'
  ```

---

### `collectstatic`

- Run the `collectstatic` management command
- This will copy all files from your static folders into the STATIC_ROOT directory.

  ```sh
  $ cd <django_project>
  $ python manage.py collectstatic
  ```

---

### 创建 web.config 文件

- 在`STATIC_ROOT`参数指定的文件夹创建设置文件：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <system.webServer>
    <!-- 覆盖FastCGI handler,让IIS访问静态文件 -->
      <handlers>
        <clear/>
        <add name="StaticFile"
             path="*"
             verb="*"
             modules="StaticFileModule"
             resourceType="File"
             requireAccess="Read" />
      </handlers>
    </system.webServer>
</configuration>
```

> 代码说明：
>
> - 如果没有该代码，当浏览器打开 static_root 地址时会返回 url 错误的信息；当存在该代码时，会返回 404 的服务器代码，即将 static_root 的访问的路由错误变为服务器的权限错误。

---

### 设置 IIS 虚拟目录

1. 打开 IIS
2. 点选网站，右键"添加虚拟目录"

![图片](../pics/static/图片1.png)

3. 设置参数。
   - 别名：站点显示的虚拟文件目录名称。
   - 物理路径：指定\/static_collected\/文件夹。

![图片3](../pics/static/图片3.png)

![图片4](../pics/static/图片4.png)

---

[TOP](#django---static-files)
