# AWS Certified Solutions Architect Associate SAA-C03

[All Note](../../index.md)

- [AWS Certified Solutions Architect Associate SAA-C03](#aws-certified-solutions-architect-associate-saa-c03)
  - [Admin](#admin)
  - [Solution Architeture](#solution-architeture)
  - [Servies](#servies)
  - [Security](#security)
  - [Disaster Recovery \& Migration](#disaster-recovery--migration)

---

- Exame:
  - `AWS Certified Solution Architect - Associate (SAA-C03)`

## Admin

- [AWS Infrastructure](./infrastructure/infrastructure.md)

- Identity

  - [`AWS IAM`](./iam/iam.md)
  - [`AWS Organizations`](./iam/advanced_identity.md)
  - [`IAM Identity Center`](./iam/identity_center.md)
  - [`AWS Directory Services`](./iam/directory_services.md)
  - [`AWS Control Tower`](./iam/control_tower.md)
  - [`AWS Cognito`](./iam/cognito.md)

- [Monitor, Audit, Compliance](./monitor_audit_compliance/monitor_audit_compliance.md)

  - [`Amazon CloudWatch`](./monitor_audit_compliance/cloudwatch.md)
  - [`Amazon EventBridge`](./monitor_audit_compliance/eventbridge.md)
  - [`AWS CloudTrail`](./monitor_audit_compliance/cloudtrail.md)
  - [`AWS Config`](./monitor_audit_compliance/config.md)

- Billing
  - [Budget](./billing/budget/budget.md)
  - [Cost Explorer](./billing/cost_explorer/cost_explorer.md)

---

## Solution Architeture

- Solution Architecture

  - [Classic Solution Architecture](./solution_architecture/classic/classic.md)
  - [Advanced Solution Architecture](./solution_architecture/advanced/advanced.md)
  - [`Beanstalk`](./solution_architecture/beanstalk/beanstalk.md)
  - [`Amplify`](./solution_architecture/amplify/amplify.md)
  - [Serverless](./solution_architecture/serverless/serverless.md)
    - [Serverless Architecture](./solution_architecture/serverless/architecture.md)

---

## Servies

- **Compute services**

  - [`AWS EC2`](./compute/ec2/ec2.md)

    - [EC2 Network](./compute/ec2/ec2_network.md)
    - Storage
      - [`Elastic Block Storage`](./compute/ec2/ebs.md)
      - [`Elastic File System`](./compute/ec2/efs.md)
    - [Availability & Scalability](./compute/ec2/availability_scalability.md)
      - [`Auto Scale Group`](./compute/ec2/ec2_asg.md)
      - [`Elastic Load Balancer`](./compute/ec2/load_balancer.md)

  - [`AWS Lambda`](./compute/lambda/lambda.md)

- [**Container Service**](./container/container.md)

  - [`AWS ECS` and `Fargate`](./container/ecs.md)
  - [`AWS EKS`](./container/eks.md)

- [**Storage**](./storage/storage.md)

  - [`AWS S3`](./storage/s3.md)
  - [`AWS Snow Family`](./storage/snow.md)
  - [`Amazon FSx`](./storage/fsx.md)
  - [`AWS Storage Gateway`](./storage/storage_gateway.md)
  - [`AWS Transfer Family`](./storage/transfer_family.md)
  - [`AWS DataSync`](./storage/datasync.md)

- [**Database Service**](./db_service/db_service.md)

  - [`RDS`](./db_service/rds/rds.md)
  - [`Aurora`](./db_service/aurora/aurora.md)
  - [`ElasticCache`](./db_service/elasticcache/elasticcache.md)
  - [`AWS Dynamo`](./db_service/dynamo/dynamo.md)

- [**Networking(VPC)**](./networking/networking.md)

  - [Pricing](./networking/pricing.md)
  - [`AWS VPC`](./networking/vpc.md)
  - [`Bastion Host`](./networking/bastion_host.md)
  - [`Internet Gateway(IGW)`](./networking/igw.md)
  - [`Nat Gateway`](./networking/natgw.md)
  - [`NACL` & Security Group](./networking/nacl.md)
  - [`Egress-only Internet Gateway`](./networking/egress_IGW.md)
  - [`VPC Peering`](./networking/peering.md)
  - [`VPC Endpoints`](./networking/endpoint.md)
  - [`Site-to-Site VPN` + `Direct Connect (DX)`](./networking/vpn_dx.md)
  - [`Transit Gateway`](./networking/transit.md)
  - [`VPC Flow Logs`](./networking/flow_log.md)
  - [`Traffic Mirroring`](./networking/traffic_mirroring.md)

- **Networking Service**

  - [`Route 53`](./networking/route53/route53.md)
  - [`AWS CloudFront` & `Global Accelerator`](./networking/cloudfront/cloudfront.md)
  - [`AWS API Gateway`](./networking/gateway/gateway.md)

- [**Messaging and Integration**](./decouple/messaging.md)

  - [`AWS SQS`](./decouple/sqs.md)
  - [`AWS SNS`](./decouple/sns.md)
  - [`AWS Kinesis`](./decouple/kinesis.md)

- [**Data & Analytics**](./data_analytics/data_analytics/data_analytics.md)

  - [`Amazon Athena`](./data_analytics/athena/athena.md)
  - [`Amazon Redshift`](./data_analytics/redshift/redshift.md)
  - [`Amazon OpenSearch`](./data_analytics/opensearch/opensearch.md)
  - [`Amazon EMR`](./data_analytics/emr/emr.md)
  - [`Amazon QuickSight`](./data_analytics/quicksight/quicksight.md)
  - [`AWS Glue`](./data_analytics/glue/glue.md)
  - [`AWS Lake Formation`](./data_analytics/lake_formation/lake_formation.md)
  - [`Kinesis Data Analytics`](./data_analytics/kinesis_analytics/kinesis_analytics.md)
  - [`Amazon MSK`](./data_analytics/msk/msk.md)

- [**Machine learning services**](./ml/ml.md)

- Other Services
  - [`CloudFormation`](./service/cloudformation/cloudformation.md)
  - [`Simple Email Service`](./service/ses/ses.md)
  - [`Pinpoint`](./service/pinpoint/pinpoint.md)
  - [`Elastic Transcoder`](./service/transcoder/transcoder.md)
  - [`AWS Batch`](./service/batch/batch.md)
  - [`AppFlow`](./service/appflow/appflow.md)

---

## Security

- [**Encryption**](./encryption/encryption.md)

  - [`AWS KMS`](./encryption/kms.md)
  - [`AWS Systems Manager(SSM)`](./encryption/systems_manager.md)
  - [`AWS Secrets Manager`](./encryption/secret_manager.md)
  - [`AWS Certificate Manager(ACM)`](./encryption/acm.md)

- [**Security**](./security/security.md)

  - [`AWS Web Application Firewall(WAF)`](./security/waf.md)
  - [`AWS Shield`](./security/shield.md)
  - [`AWS Firewall Manager`](./security/firewall_manager.md)
  - [`Amazon GuardDuty`](./security/guardDuty.md)
  - [`Amazon Inspector`](./security/inspector.md)
  - [`AWS Macie`](./security/macie.md)
  - [`AWS Network Firewall`](./security/network_firewall.md)

---

## Disaster Recovery & Migration

- Disaster Recovery

  - [Disaster Recovery](./disaster_recovery/dr.md)

- [Migration](./migration/migration/migration.md)
  - [`Database Migration Service`](./migration/dms/dms.md)
  - [`AWS Backup`](./migration/backup/backup.md)
  - [`Application Discovery Service`](./migration/app_disc/app_disc.md)
  - [`Application Migration Service(MGN)`](./migration/mgn/mgn.md)

---

[TOP](#aws-certified-solutions-architect-associate-saa-c03)
