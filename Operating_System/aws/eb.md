# AWS - Elastic Beanstalk

[Back](./index.md)

- [AWS - Elastic Beanstalk](#aws---elastic-beanstalk)
  - [`Elastic Beanstalk`](#elastic-beanstalk)
  - [EB CLI](#eb-cli)
  - [Install EB CLI on Windows](#install-eb-cli-on-windows)
  - [Command](#command)

---

## `Elastic Beanstalk`

- `Elastic Beanstalk`
  - an orchestration service.
  - a web infrastructure management service.
  - handles deployment and scaling for web applications and services.

- Automatically managed AWS services: AWS EC2 (Elastic Compute Cloud), Amazon S3 (Simple Storage Service), AWS RDS (Relational Database Service), Amazon DynamoDB, and Amazon SimpleDB.

- Ref:
  - https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/Welcome.html
  
---

## EB CLI

- `EB CLI`
  - `AWS Elastic Beanstalk Command Line Interface`
  - a command line client that you can use to create, configure, and manage Elastic Beanstalk environments.

---

## Install EB CLI on Windows

- Install the EB CLI using `pip`

```sh
# install cli package
$ pip install awsebcli

# check version
$ eb --version
```

---

## Command

- Ref:
  - https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb3-cmd-commands.html

| Command        | Description                                                                  |
| -------------- | ---------------------------------------------------------------------------- |
| `eb init`      | Initiates the current directory for Elastic Beanstalk applications           |
| `eb list`      | Lists all environments                                                       |
| `eb status`    | Provides information about the status of the environment.                    |
| `eb create`    | Creates an environment                                                       |
| `eb deploy`    | Deploys the application source bundle from the initialized project directory |
| `eb open`      | Opens the public URL of website in the default browser.                      |
| `eb terminate` | Terminates the running environment                                           |

---

[TOP](#aws---elastic-beanstalk)
