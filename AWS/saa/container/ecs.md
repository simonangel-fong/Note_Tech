# AWS - ECS

[Back](../index.md)

- [AWS - ECS](#aws---ecs)
  - [`Amazon ECS`](#amazon-ecs)
  - [Types](#types)
    - [EC2 Launch Type](#ec2-launch-type)
    - [Fargate Launch Type](#fargate-launch-type)
  - [IAM Roles for ECS](#iam-roles-for-ecs)
  - [Load Balancer Integrations](#load-balancer-integrations)
  - [Data Volumes/Data Persistence (EFS)](#data-volumesdata-persistence-efs)
  - [Service Auto Scaling](#service-auto-scaling)
    - [EC2 Launch Type – Auto Scaling EC2 Instances](#ec2-launch-type--auto-scaling-ec2-instances)
  - [Hands-on](#hands-on)
  - [Sulotion Architecture](#sulotion-architecture)
  - [`Amazon ECR`](#amazon-ecr)

---

## `Amazon ECS`

- `ECS` = `Elastic Container Service`

---

## Types

### EC2 Launch Type

- EC2 Launch Type:

  - you **must provision & maintain the infrastructure** (the EC2 instances)
  - **Launch Docker containers** on AWS = Launch **ECS Tasks on ECS Clusters**

- Each EC2 Instance must run the `ECS Agent` to **register** in the `ECS Cluster`
- AWS takes care of **starting** / **stopping** containers

![ecs_ec2_launch_type](./pic/ecs_ec2_launch_type.png)

---

### Fargate Launch Type

- You do **not provision** the infrastructure (no EC2 instances to manage)

  - no more EC2 instances(easier to manage than EC2 launch type)
  - Launch Docker containers **on AWS**

- It’s all **Serverless**!
- You just create **task definitions**
- AWS just runs ECS Tasks for you based on the **CPU / RAM you need**
- To **scale**, just increase the number of tasks. Simple

![ecs_fargate_launch_type.png](./pic/ecs_fargate_launch_type.png)

- Sample:
  - You have multiple Docker-based applications hosted on-premises that you want to migrate to AWS. You don't want to provision or manage any infrastructure; you just want to run your containers on AWS. Which AWS service should you choose?
  - `AWS Fargate` allows you to run your containers on AWS **without managing any servers.**

---

## IAM Roles for ECS

- EC2 Instance **Profile Role** (`EC2 Launch Type` **only**):

  - Used by the `ECS agent`
  - Makes **API calls** to ECS service
  - Send container **logs** to `CloudWatch Logs`
  - Pull Docker **image** from `ECR`
  - Reference **sensitive data** in `Secrets Manager` or `SSM Parameter` Store

- ECS Task **Role**: (Both for EC2 type and Fargate type)

  - Allows each **task** to have a **specific role**
  - Use different roles for the different ECS Services you run
  - **Task Role** is defined in the **task definition**

- **ECS Task Role** is the `IAM Role` used by the **ECS task** itself. Use when your container wants to **call other AWS services** like `S3`, `SQS`, etc.

![ecs_iam_role](./pic/ecs_iam_role.png)

- Sample:
  - You are deploying an application on an ECS Cluster made of EC2 instances. Currently, the cluster is hosting one application that is issuing API calls to DynamoDB successfully. Upon adding a second application, which issues API calls to S3, you are getting **authorization issues**. What should you do to resolve the problem and ensure proper security?
  - Create an IAM Task Role for new application.

---

## Load Balancer Integrations

- To expose task as http/https endpoint.

- `Classic Load Balancer` supported but **not recommended** (no advanced features – no Fargate)
- `Application Load Balancer` supported and works for most use cases
- `Network Load Balancer` recommended only for **high throughput / high performance** use cases, or to pair it with `AWS Private Link`

![ecs_load_balancer](./pic/ecs_load_balancer.png)

---

## Data Volumes/Data Persistence (EFS)

- `EFS volume` can be shared between different `EC2 instances` and different `ECS Tasks`.

  - It can be used as a persistent **multi-AZ shared storage** for your **containers**.

- **Mount** `EFS` file systems onto **ECS tasks**

  - Works for **both** `EC2` and `Fargate` launch types
  - Tasks running in **any AZ** will share the same data in the EFS file system
  - `Fargate` + `EFS` = `Serverless`

- **Note**:

  - Amazon `S3` **cannot be mounted** as a file system

- **Use cases**:
  - persistent multi-AZ shared storage for your containers

![ecs_data_volume](./pic/ecs_data_volume.png)

---

## Service Auto Scaling

- Automatically **increase/decrease** the desired number of ECS **tasks**

- `Amazon ECS Auto Scaling` uses `AWS Application Auto Scaling` with 3 metrics:

  - ECS Service Average **CPU** Utilization
  - ECS Service Average **Memory** Utilization - Scale on RAM
  - ALB **Request Count Per Target** – metric coming from the ALB

- **Types of Auto Scaling:**

  - **Target Tracking**

    - scale based on **target value** for a specific `CloudWatch` **metric**

  - **Step Scaling**

    - scale based on a specified `CloudWatch` **Alarm**

  - **Scheduled Scaling**

    - scale based on a **specified date/time** (predictable changes)

- `ECS Service Auto Scaling` (**task level**) **≠** `EC2 Auto Scaling` (EC2 **instance level**)

- `Fargate Auto Scaling` is much **easier** to setup (because **Serverless**)

---

### EC2 Launch Type – Auto Scaling EC2 Instances

- Accommodate ECS Service Scaling by **adding underlying EC2 Instances**

- **Ways to auto scaling EC2 instacnes**:

  - **Auto Scaling Group Scaling**

    - Scale your ASG based on **CPU** Utilization
    - **Add** EC2 **instances** over time

  - **ECS Cluster Capacity Provider**: a recommandated feature
    - Used to **automatically provision and scale** the infrastructure for your ECS Tasks
    - Capacity Provider paired with an `Auto Scaling Group`
    - Add EC2 Instances when you’re missing capacity (CPU, RAM…)

![ecs_scaling_cpu_diagram](./pic/ecs_scaling_cpu_diagram.png)

---

## Hands-on

- Create Cluster

![ecs_handson01](./pic/ecs_handson01.png)

![ecs_handson02](./pic/ecs_handson02.png)

![ecs_handson03](./pic/ecs_handson03.png)

![ecs_handson04](./pic/ecs_handson04.png)

![ecs_handson05](./pic/ecs_handson05.png)

- Create Task

![ecs_handson06](./pic/ecs_handson06.png)

![ecs_handson06](./pic/ecs_handson07.png)

- Image URL: nginxdemos/hello
  - https://hub.docker.com/r/nginxdemos/hello/

![ecs_handson06](./pic/ecs_handson08.png)

- Create service

![ecs_handson06](./pic/ecs_handson09.png)

![ecs_handson06](./pic/ecs_handson10.png)

![ecs_handson06](./pic/ecs_handson11.png)

![ecs_handson06](./pic/ecs_handson12.png)

![ecs_handson06](./pic/ecs_handson13.png)

![ecs_handson06](./pic/ecs_handson14.png)

![ecs_handson06](./pic/ecs_handson15.png)

![ecs_handson06](./pic/ecs_handson16.png)

![ecs_handson06](./pic/ecs_handson17.png)

![ecs_handson06](./pic/ecs_handson18.png)

![ecs_handson06](./pic/ecs_handson19.png)

![ecs_handson06](./pic/ecs_handson20.png)

![ecs_handson06](./pic/ecs_handson21.png)

![ecs_handson06](./pic/ecs_handson22.png)

- Scaling up task.

![ecs_handson06](./pic/ecs_handson23.png)

![ecs_handson06](./pic/ecs_handson24.png)

![ecs_handson06](./pic/ecs_handson25.png)

![ecs_handson06](./pic/ecs_handson26.png)

- 效果:
  - 相当于有 3 个 instance 共同指向一个 ALB
  - 刷新时, 会显示不同 IP.

![ecs_handson06](./pic/ecs_handson27.png)

![ecs_handson06](./pic/ecs_handson28.png)

![ecs_handson06](./pic/ecs_handson29.png)

---

## Sulotion Architecture

- Serverless + DB

![ecs_solution_architecture_event_bridge](./pic/ecs_solution_architecture_event_bridge.png)

- Schedule Serverless

![ecs_solution_architecture_event_bridge_schedule.png](./pic/ecs_solution_architecture_event_bridge_schedule.png)

- SQS Queue

![ecs_solution_architecture_sqs](./pic/ecs_solution_architecture_sqs.png)

- Monitor ECS task

![ecs_solution_architecture_event_bridge_intercept_stopped_tasks.png](./pic/ecs_solution_architecture_event_bridge_intercept_stopped_tasks.png)

---

## `Amazon ECR`

- `ECR` = `Elastic Container Registry`

  - **Store** and **manage** Docker **images** on AWS
  - Private and Public repository (Amazon ECR Public Gallery https://gallery.ecr.aws)
  - Fully integrated with ECS, **backed** by Amazon `S3`

- **Access is controlled** through `IAM` (permission errors => policy)
- Supports image vulnerability scanning, versioning, image tags, image lifecycle, …

![ecr_diagram](./pic/ecr_diagram.png)

---

[TOP](#aws---ecs)
