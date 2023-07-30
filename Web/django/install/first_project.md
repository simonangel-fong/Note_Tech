# Django - First Django Project

[Back](../index.md)

- [Django - First Django Project](#django---first-django-project)
  - [Create and Activate Virtual Environment](#create-and-activate-virtual-environment)
  - [Install Django in Virtual Environment](#install-django-in-virtual-environment)
  - [Create Django Project](#create-django-project)
  - [Create Application](#create-application)
    - [Create a View](#create-a-view)
    - [Create Application URL File](#create-application-url-file)
    - [Update Project URL File](#update-project-url-file)
    - [Run Project](#run-project)
  - [VS Code: Create Debug File](#vs-code-create-debug-file)

---

## Create and Activate Virtual Environment

1. Create a project directory.

2. Change the current directory to the project directory

   ```sh
   cd <protject_dir>
   ```

   - `<protject_dir>`: the path of project directory.

3. Create Virtual Environtmet:

   ```sh
   python -m venv <env_name>
   ```

   - `<env_name>`: the name of virtual environment.

4. Activate Virtual Environment:

- 1. CLI:
  ```sh
  \project_dir> <env_name>\scripts\activate
  ```
- 2. VScode:
  - <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>
  - select python interpreter

---

## Install Django in Virtual Environment

- CLI:

  ```sh
  (env_name)\project_dir> python -m pip install django
  ```

- Verify:
  - CLI:
  ```sh
  (env_name)\project_dir> py -m django --version
  # the version nubmer will be returned.
  ```

---

## Create Django Project

- Change current directory to project directory

  ```sh
  cd project_dir
  ```

- Create project directory using `django-admin` command:

  ```sh
  (env_name)\project_dir> django-admin startproject <proj_name> .
  ```

  - `<proj_name>`: the name of project directory
  - `.`: create the project directory within the current directory.

- The following files and folder are created:

  - `project_dir/`: a container for project

    - `manage.py`: a py file associated with many django commands.
    - `proj_name/`: the actual Python package for the project. Its name is the Python package name to be used to import.
      - `__init__.py`: An empty file that tells Python that this directory should be considered a Python package.
      - `asgi.py`: An entry-point for ASGI-compatible web servers to serve the project.用于处理具有异步功能的标准接口。
      - `settings.py`: a py file to store all project settings
      - `urls.py`: The URL declarations for this Django project;
      - `wsgi.py`: a py file that acts as the Web Server Gateway Interface for deployment.

- Verify: Run the django project
  - CLI:
    ```sh
    (env_name)\project_dir> py manage.py runserver
    ```
  - a local address can be visited.
    - http://127.0.0.1:8000/

---

## Create Application

- Change current working directory into project directory `<project_dir>`, not the django proejct directory `<proj_name>`

  ```sh
  py manage.py startapp <app_name>
  ```

  - `<app_name>`: the name of application

- The following folder and files are created:

  - `app_name/`: a directory as a Python package for the application.
    - `__init__.py`: a py file to indicate that the current folder should be considered a Python package.
    - `admin.py`: a py file to store models used with Django’s admin interface.
    - `apps.py`: a py file to store application specific configurations
    - `models.py`: a py file to store the application’s data models
    - `tests.py`: a py file to store test functions to test code
    - `views.py`: a py file to store functions that handle requests and return responses
    - `migrations/`: a directory stores database specific information
      - `__init__.py`: a py file to indicate that the current folder should be considered a Python package.

---

### Create a View

- `<app_name>\view.py`:

```py
from django.shortcuts import render
from django.http import HttpResponse    # import HttpResponse from http module

# create an index function taking request as parameter
def index(request):
    return HttpResponse("Hellow world!")  # return a HttpResponse object with a string content.
```

---

### Create Application URL File

- Create a `<app_name>\url.py` file:

```py
from django.urls import path    # import path function from urls module
from <app_name> import views    # import views module from <app_name> package

# define a list of url patterns
urlpatterns = [
    path("", views.index, name="index"),
  ]

```

---

### Update Project URL File

- Update `<proj_name>\urls.py`

```py
from django.contrib import admin
from django.urls import path, include   # import path, include function from urls module

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include("<app_name>.urls"))
]
```

---

### Run Project

- CLI:
  ```sh
  (env_name)\project_dir> py manage.py runserver
  ```

---

## VS Code: Create Debug File

- VS Code > `RUN AND DEBUG` > `create a launch.json file`
- Select `debugger for`: `Python`
- Select `debug configuration`: Django
- Enter the path to manage.py: default

- `launch.json` file:

  ```json
  {
    "version": "0.2.0",
    "configurations": [
      {
        "name": "Python: Django", // name of launch configuration
        "type": "python", // type
        "request": "launch",
        "program": "${workspaceFolder}\\manage.py", // path to django manage.py file
        "args": ["runserver", "--noreload", "5000"], // django command argument
        "django": true,
        "justMyCode": true
      }
    ]
  }
  ```

- Press `F5` to lauch debug.

---

[TOP](#django---first-django-project)
