# Django - Deploy to Elastic Beanstalk

[Back](../index.md)

- [Django - Deploy to Elastic Beanstalk](#django---deploy-to-elastic-beanstalk)
  - [Delpoy Django](#delpoy-django)
    - [Prerequisites](#prerequisites)
    - [Configure local Django project for EB](#configure-local-django-project-for-eb)
    - [Create an EB environment and Deploy](#create-an-eb-environment-and-deploy)
  - [Clean up EB instance](#clean-up-eb-instance)

---

## Delpoy Django

### Prerequisites

- AWS account
- EB CLLI
- local django project

---

### Configure local Django project for EB

- By default, `Elastic Beanstalk` looks for a file named `application.py` to start your application.

- Configures Django project for Elastic Beanstalk:

1. General `requirements.txt`
  
```sh
$ pip freeze > requirements.txt
```

---

2. Create a directory named `.ebextensions`.

```sh
$ mkdir .ebextensions
```

---

3. In the `.ebextensions` directory, add a configuration file named `django.config` with the following text:

```config
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: ebdjango.wsgi:application
  aws:elasticbeanstalk:environment:proxy:staticfiles:
    /static: static
```

- `WSGIPath`, specifies the location of the `WSGI` script that Elastic Beanstalk uses to start application.
- `/static`, specifies static dir

---

- Check files structure:

```
~/proj_container/
|-- .ebextensions
|   `-- django.config
|-- proj_dir
|   |-- __init__.py
|   |-- settings.py
|   |-- urls.py
|   `-- wsgi.py
|-- db.sqlite3
|-- manage.py
`-- requirements.txt
```

---

### Create an EB environment and Deploy

1. Initialize  `EB CLI` repository with the eb init command.

```sh
~/proj_container$ eb init -p python-3.7 <app_name>
```

---

2. (Optional) Run eb init again to configure a default **key pair** so that can use `SSH` to connect to the EC2 instance running your application.

```
~/proj_container$ eb init
Do you want to set up SSH for your instances?
(y/n): y
Select a keypair.
1) my-keypair
2) [ Create new KeyPair ]
```

---

3. Create an environment

```sh
~/proj_container$ eb create <env_name>
```

- This command creates a load-balanced `Elastic Beanstalk` **environment** named env_name. Creating an environment takes about 5 minutes. As Elastic Beanstalk creates the resources needed to run your application, it outputs informational messages that the EB CLI relays to your terminal.

---

4. Find the domain name of new environment by running `eb status`.

```
~/ebdjango$ eb status
Environment details for: <env_name>
  Application name: <app_name>
  ...
  CNAME: eb-django-app-dev.elasticbeanstalk.com
  ...
```

- environment's domain name is the value of the `CNAME` property.


---

5. Open the `settings.py` file in the ebdjango directory. Locate the `ALLOWED_HOSTS` setting, and then add your application's domain name that you found in the previous step to the setting's value. If you can't find this setting in the file, add it to a new line.

```py
ALLOWED_HOSTS = [
  'eb-django-app-dev.elasticbeanstalk.com'
]
```

---

6. Deploy application by running `eb deploy`. When run `eb deploy`, the EB CLI **bundles up the contents of your project directory** and deploys it to your environment.

```sh
~/proj_container$ eb deploy
```

---

7. When the environment update process completes, open website with `eb open`.

```sh
~/proj_container$ eb open
```
- This opens a browser window using the domain name created for application. You should see the same Django website that you created and tested locally.

---

## Clean up EB instance

```sh
~/project_container$ eb terminate env-name
```

- terminates the environment and all of the AWS resources that run within it. 
- It doesn't delete the application, however, so you can always create more environments with the same configuration by running `eb create` again. 

---

[TOP](#django---elastic-beantalk)
