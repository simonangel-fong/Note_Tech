# AWS CICD - Deploy Django App from Github

[Back](../index.md)

- [AWS CICD - Deploy Django App from Github](#aws-cicd---deploy-django-app-from-github)
  - [Create role](#create-role)
  - [Create Instance](#create-instance)
  - [CodeDeploy](#codedeploy)
  - [Pipline](#pipline)

---

## Create role


---

## Create Instance

---

## CodeDeploy

Deploy - CodeDeploy

create Applications

create deployment group

    Environment configuration: Amazon EC2 instances
    tag:
        name value= instance name
    Deployment settings: AllAtOnce
    for simple app, no load balancer

---

## Pipline

    create pipline
        name
    SOurce stage
        Github version 2
        connection: 
            Connection Name
            Install a new app > login github
        Repository name
        Branch name
      build stage: skip this
      deploy stage
        Deploy provider: AWS CodeDeploy
        Application name: app name created above
        Deployment group: group above

---

[TOP](#aws-cicd---deploy-django-app-from-github)
