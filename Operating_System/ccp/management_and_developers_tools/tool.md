# AWS - Management and Developers Tools

[Back](../index.md)

- [AWS - Management and Developers Tools](#aws---management-and-developers-tools)
  - [Fundamental](#fundamental)
    - [Account ID](#account-id)
    - [Amazon Resource Name (ARN)](#amazon-resource-name-arn)
    - [Access Keys](#access-keys)
    - [AWS Documentation](#aws-documentation)
  - [API](#api)
  - [Console](#console)
  - [AWS CloudShell](#aws-cloudshell)
    - [AWS Tools for Powershell](#aws-tools-for-powershell)
  - [AWS CLI](#aws-cli)
  - [AWS Software Developement Kit (SDK)](#aws-software-developement-kit-sdk)
  - [Infrastructure as Code (IaC)](#infrastructure-as-code-iac)
    - [CloudFormation](#cloudformation)
    - [Cloud Development Kit (CDK)](#cloud-development-kit-cdk)
  - [AWS Toolkit for VSCdoe](#aws-toolkit-for-vscdoe)

---

## Fundamental

### Account ID

- Every AWS Account has a unique Account ID.

- The Account ID can be easily found by dropping down the current user in the Global Navigation.

- The AWS Account ID is composed of 12 digits.

- The AWS Account ID is used:

  - When **logging in** with a non-root user account
  - Cross-account roles
  - Support cases

- Example: role
  ![Cross-account roles](./pic/account_id_role.png)

- Example: policy
  ![Cross-account policy](./pic/account_id_policy.png)

---

### Amazon Resource Name (ARN)

- `Amazon Resource Name (ARN)`

  - uniquely identify AWS resources.
  - `ARNs` are required to specify a resource unambiguously across all of AWS.

- ARNs format variations:

  - `arn.partition:service:region:account-id:resource-id`
  - `arn.partition:service:region:account-id:resource-type/resource-id`
  - `arn.partition:service:region:account-id:resource-type:resource-id`

- `Partition`

  - `aws`: AWS Regions
  - `aws-cn`: China Regions
  - `aws-us-gov`: AWS GovCloud (US) Regions

- `Service`: Identifies the service

  - ec2
  - s3
  - iam

- `Region`: which AWS resource

  - us-east-1
  - ca-cetral-1

- `Account ID`

- `Resource ID`: could be a number name or path

  - user: Bob
  - instance name

- Resource ARNs can include a path
- Paths can include a wildcard character, namely an asterisk (`*`)

  ![asterisk](./pic/arn_asterisk.png)

---

### Access Keys

- `Access Keys`

  - a key and secret required to have programmatic access to AWS resources when interacting with the AWS API outside of the AWS Management Console.
  - An Access Key is commonly referred to as `AWS Credentials`

- Never share user's access keys
- Never commit access keys to a codebase
- An user can have two active Access Keys
- An user can deactivate Access Keys.
- Access Keys have whatever access a user has to AWS resources.

![access key](./pic/access_key01.png)

![access key](./pic/access_key02.png)

- Create Access Key

![create access key](./pic/access_key_create.png)

---

### AWS Documentation

- `AWS Documentation`

  - a large collection of technical documentation on how to use AWS Services.

- AWS Documentation: https://docs.aws.amazon.com/

- AWS Labs(examples and tutorial): https://github.com/awslabs

---

## API

- `Application Programming Interface(API)`

  - a software that allows two application/services to talk to each other.
  - The most common type of API is via `HTTP` requests.

- `AWS API`

  - an `HTTP API` and user can interact by sending `HTTPS` requests
  - Rarely do users directly send HTTP requests directly to the AWS API. Its much easier to interact with the API via a variety of Developer Tools.

  ![api_tool](./pic/api_tool.png)

- Example:

  ![api](./pic/api_example.png)

- List of Service endpoints: https://docs.aws.amazon.com/general/latest/gr/aws-service-information.html

---

## Console

- `Management Console`

  - a web-based unified console to build, manage, and monitor resources from simple web apps to complex cloud deployment.

- `Service Console`
  - AWS Service each have their own customized console.
  - User can access these consoles by searching service name.
  - Some AWS Service Consoles contain many AWS Sevices.

---

## AWS CloudShell

- `AWS CloudShell`
  - a browser based shell built into the AWS Management Console.
  - is scoped per region
  - same credentials as logged in user
  - Free Service
  - Include 1GB of storage free per AWS region
  - Saved files and settings
    - files saved in home directory are available in future sessions for the same AWS region.
  - Preinstalled Tools
    - AWS CLI, Python, Node.js, git, make,pip, sudo, tar, tmux,vim wget, and zip and more.

---

### AWS Tools for Powershell

- `Powershell`
  - a task automation and configuration management framework.
  - A command-line shell and a scripting lauguage.
- Unlinke most shells, which accept and return text, PowerShell is built on top of the `.NET` Common Language Runtime (CLR), and accepts and returns `.NET` objects.

- `Cmdlet`

  - a special type of command in PowerShell in the form of capitalized verb-and-noun e.g.`New-S3Bucket`

- `AWS Tools for Powershell` lets user interact with the AWS API via PowerShell `Cmdlets`.

- `pwsh`: Command to Switch to PowerShell in AWS CloudShell

  ![pwsh](./pic/aws_cloudshell_powershell01.png)

- Documentation: https://docs.aws.amazon.com/powershell/index.html

---

## AWS CLI

- `Command Line Interface (CLI)`

  - processes commands to a computer program in the form of lines of text.
  - OS implement a command-line interface **in a shell**.

- `Terminal`

  - a text only interface (input/output environment)

- `Console`

  - a console is a physical computer to physically input information into a terminal.

- `Shell`

  - the command line program that users interact with to input commands.

- `AWS Command Line Interface (CLI)`

  - allow users to programmatically **interact with** the `AWS API` via entering single or multi-line commands into a shell or terminal.
  - a python executable program.
  - Python is required to install AWS CLI.
  - need to be instelled on OS
  - The name of the CLI program is `aws`
  - Important!: CLI is available for a few region.

- About AWS CLI: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html

---

## AWS Software Developement Kit (SDK)

- `Software Developement Kit (SDK)`

  - a collection of software development tools in one installable package.

- `AWS SDK`

  - a package used to create, modify, delete or interact with AWS resources.

- AWS SDK for Python: https://aws.amazon.com/sdk-for-python/

- `AWS Cloud9`
  - An AWS cloud **IDE** for writing, running, and debugging code

---

## Infrastructure as Code (IaC)

- `Infrastructure as Code (IaC)`

  - user write a configuration script to automate creating, updating or destroying cloud infrastrure.
  - is a blueprint of infrastructure.
  - allow to easily share, version or inventory cloud infrastructure.

- AWS has two offering for writing Infrastructure as Code.
  - `AWS CloudFormation (CFN)`: CFN is a Declarative IaC tool
    - Declarative
      - What user see is what user get. Explicit
      - More verbose, but zero chance of mis-configuration
      - Users scripting language. e.g., JSON, YAML, XML
  - `AWS Cloud Development Kit (CDK)`: CDK is an Imperative IaC tool.
    - Imperative
      - User say what user want, and the reset is filled in. Implicit
      - Less verbose, user could end up with misconfiguration
      - Does more than Declarative
      - Users programming languages. e.g., Python, Ruby, JS

---

### CloudFormation

- `AWS CloudFormation`

  - allows user to write `Infrastructure as Code (IaC)` as either a `JSON` or `YAML` file.

- `CloudFormation` is simple but it can lead to large files or is limited in some regard to creating dynamic or repeatable infrastructure compared to CDK.

- `CloudFormation` can be easier for DevOps Engineers who **do not have a background in web programming languages**.

- Since CDK generates out `CloudFormation`, it's still important to be able to read and understand `CloudFormation` in order to debug IaC stacks.

- Create a `CloudFormation` Stack:

  - Cloud9 + CLI
  - CloudFormation console

- AWS CloudFormation: https://aws.amazon.com/cloudformation/

---

### Cloud Development Kit (CDK)

- `AWS CDK`

  - allows to user user's favortite programming language to write Infrastructure as Code (IaC)
  - e.g.: TypeScript, Node.js, Python, Java, .NET

- `CDK` is powered by CloudFormation (it generates out CloudFormation templates)

  - The result of CDK execution will display in CloudFormation console.

- `CDK Construct`: a large library of reusable cloud components. https://constructs.dev

- `CDK` comes with its own CLI

- `CDK` Piplines to quickly setup CI/CD pipelines for CDK projects.

- `CDK` has a testing framework for Unit and Integration Testing.

- CDK documentation: https://docs.aws.amazon.com/cdk/api/v2/

- About CDK: https://aws.amazon.com/cdk/

---

## AWS Toolkit for VSCdoe

- `AWS Toolkit`

  - an open-source plugin for VSCode to create, debug, deploy AWS resources.

- `AWS Explorer`: Explore a wide range of AWS resources to user's linked AWS Account.

- `AWS CDK Explorer`: Allows to explore user's stacks defined by CDK.

- `Amazon Elastic Container Service`: Provides IntelliSense for ECS task-definition files.

- `Serverless Applications`:Create, debug and deploy serverless applications via `SAM` and `CFN`

---

[Top](#aws---management-and-developers-tools)
