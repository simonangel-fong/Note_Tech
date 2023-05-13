# AWS - AMI

[Back](../index.md)

- [AWS - AMI](#aws---ami)
  - [AMI](#ami)
  - [AMI Process](#ami-process)
  - [EC2 Image Builder](#ec2-image-builder)

---

## AMI

- `AMI`

  - Amazon Machine Image
  - a customization of an EC2 instance
    - You add your own software, configuration, operating system, monitoring…
  - Faster boot / configuration time because all your software is pre-packaged

- AMI are built **for a specific region** (and can be **copied across regions**)
- You can launch EC2 instances from:
  - A **Public** AMI: AWS provided
  - Your **own** AMI: you make and maintain them yourself
  - An AWS **Marketplace** AMI: an AMI someone else made (and potentially sells)

---

## AMI Process

1. Start an EC2 instance and customize it
2. Stop the instance (for data integrity)
3. Build an AMI – this will also create EBS snapshots
4. Launch instances from other AMIs

---

## EC2 Image Builder

- `EC2 Image Builder`
  - Used to **automate the creation** of Virtual Machines or container images
    - => Automate the **creation, maintain, validate and test** EC2 AMIs
- Can be run on a **schedule** (weekly, whenever packages are updated, etc…)
- **Free** service (only pay for the underlying resources)
- 会自动创建 EC2,并按设置安装包.
- 创建好 AMI 后, EC2 会自动结束 terminzated. 一个 test 的 EC2 会自动创建.
- 测试后, 该 EC2 会结束 terminzated.
- 以上 EC2 的 createBy 是 EC2 Image Builder
- 绑定 AZ

---

[TOP](#aws---ami)
