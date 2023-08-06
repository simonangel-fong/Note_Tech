# Django

[All Notes](../../index.md)

---

## Catalog

- [Install](./install/install.md)

  - [First Django Project](./install/first_project.md)

- Settings

  - [Settings Variable](./settings/settings_var.md)

- [URL](./url/url.md)

  - [`django.urls` Module](./url/django.urls.md)

- View

  - [Request Objects](./view/request.md)
  - [Response Objects](./view/response.md)
  - [`shortcuts` Package](./view/shortcuts.md)

- [Model](./model/model.md)

  - [Meta](./model/meta.md)
  - [Field](./model/field.md)
  - [Relationship](./model/relationship.md)
  - [QuerySet](./model/queryset.md)

- [Template](./template/template.md)

  - [Template inheritance](./template/inheritance.md)
  - [Template tags and filters](./template/tag_filter.md)
  - [Static Files](./template/static_files.md)

- [Form](./form/form.md)
  - [Form Field](./form/form_field.md)
  - [Model Form](./form/modelform.md)

- [Authentication](./auth/auth.md)
  - [User](./auth/user.md)
  - [Permissions and Groups](./auth/perm.md)
  - [Authentication Views](./auth/auth_view.md)
- References

  - [`manage.py`](./ref/manage.md)


---

- Labs:
  - [Streaming Video](./labs/streaming.md)

- [Django - 部署到 IIS](./app/django_iis.md)
- [Django - 视图：增加数据](./app/django_view_add.md)
- [Django - model:FileField](./app/django_model_filefield.md)
- [Django - model:\_meta API](./app/django_model_meta.md)
- [Django - View: StreamingHttpResponse](./app/django_view_streaminghttpresponse.md)

---

## Resource:

- Ref:

  - https://docs.djangoproject.com/en/4.0/

- w3school:

  - https://www.w3schools.com/django/index.php

- Udemy:
  - https://www.udemy.com/course/python-and-django-full-stack-web-developer-bootcamp/

---

## Terminology

- `Django`

  - a back-end server side web framework.
  - free, open source and written in Python.

- `Django` follows the `MVT` design pattern (**Model View Template**):

  - `Model` The model provides data from the database.

    - The models are usually located in a file called `models.py`.

  - `View`: A request handler that returns the relevant template and content - based on the request from the user.
  - `Template`: A text file (like an HTML file) containing the layout of the web page, with logic on how to display the data.

- `project`

  - A Python package – i.e. a directory of code – that contains all the settings for an instance of Django.
  - This would include database configuration, Django-specific options and application-specific settings.

- `app`

  - A Django Application is created to perform a particular functionality for your entire web application.
  - can then be plugged into other Django Projects

- `Project` 与 `app` 之间的关系：

  - 一个 Project 可以包含多个 app；
  - 在 Project 中的每个 app 实现一个独立功能；
  - 一个 app 可以在多个 Project 中；
  - 一个 app 仅仅是遵循 Django 约定的**Python 包**。

- **django-admin 工具**是 Django 管理命令行工具之一，安装好 Django 包后可以直接调用。

---
