# AWS Certified Solutions Architect Associate SAA-C03

[All Note](../../index.md)

- [AWS Certified Solutions Architect Associate SAA-C03](#aws-certified-solutions-architect-associate-saa-c03)
  - [Admin](#admin)
  - [Solution Architeture](#solution-architeture)
  - [Servies](#servies)
    - [Compute Service](#compute-service)
    - [Container Service](#container-service)
    - [Storage Service](#storage-service)
    - [Database Service](#database-service)
    - [Networking](#networking)
  - [Security](#security)

---

- Exame:

  - `AWS Certified Solution Architect - Associate (SAA-C03)`

- [Certification Path](./cert_path/cert_path.md)

---

## Admin

- [AWS Infrastructure](./infrastructure/infrastructure.md)

- Identity

  - [`AWS IAM`](./iam/iam.md)
  - [`AWS Organizations`](./iam/advanced_identity.md)
  - [`AWS Control Tower`(Account Creation)](./iam/control_tower.md)
  - [`Trusted Advisor`(Account Acccessment)](./solution_architecture/trusted_advisor/trusted_advisor.md)

- Login

  - [`IAM Identity Center`(SSO)](./iam/identity_center.md)
  - [`AWS Directory Services`(Win DA)](./iam/directory_services.md)
  - [`AWS Cognito`(Web+App)](./iam/cognito.md)

- [Monitor, Audit, Compliance](./monitor_audit_compliance/monitor_audit_compliance.md)

  - [`Amazon CloudWatch`(Metric, Log, Alarm, Insight)](./monitor_audit_compliance/cloudwatch.md)

  - [`AWS CloudTrail`(audit)](./monitor_audit_compliance/cloudtrail.md)
  - [`AWS Config`(compliance, rule, notification, remediation)](./monitor_audit_compliance/config.md)

- Billing
  - [Budget](./billing/budget/budget.md)
  - [`Cost Explorer`(Visualize, Save plan)](./billing/cost_explorer/cost_explorer.md)

---

## Solution Architeture

- Solution Architecture

  - [Classic Solution Architecture](./solution_architecture/classic/classic.md)
  - [Advanced Solution Architecture](./solution_architecture/advanced/advanced.md)
  - [Serverless](./solution_architecture/serverless/serverless.md)
    - [Serverless Architecture](./solution_architecture/serverless/architecture.md)
    - [`Step Functions`(visual workflow, human approval)](./solution_architecture/serverless/step_func.md)
  - [Well Architected Framework & Tool](./solution_architecture/framework/framework.md)

- [Messaging and Integration](./solution_architecture/decouple/messaging.md)

  - [`AWS SQS`(FIFO, retention, Grouping, IAM+AP,Visibility Timeout, Long Polling, asg, buffer)](./solution_architecture/decouple/sqs.md)
  - [`AWS SNS`(Message Filtering, IAM+AP, Fan-out)](./solution_architecture/decouple/sns.md)
  - [`AWS Kinesis`(Ingest real-time data, Streams(Real-time, can store replay, Partition Key), Firehose(serverless, near Real-time, to load), Analytics, Video Stream)](./solution_architecture/decouple/kinesis.md)
  - [`Amazon MQ`(MQ Broker, Multi-AZ with failover)](./solution_architecture/decouple/mq.md)
  - [`Amazon EventBridge`(Schema Registry, Resource-based Policy(centrol aggregate))](./solution_architecture/decouple/eventbridge.md)

- Deploymnet
  - [`Beanstalk`(deploying app)](./solution_architecture/beanstalk/beanstalk.md)
  - [`Amplify`(web + mobile)](./solution_architecture/amplify/amplify.md)
  - [`App Runner`(Container, Web app/API)](./solution_architecture/app_runner/app_runner.md)

---

## Servies

### Compute Service

- [`AWS EC2`](./compute/ec2/ec2.md)

  - [EC2 Network](./compute/ec2/ec2_network.md)
  - Storage
    - [`Elastic Block Storage`(lock AZ)](./compute/ec2/ebs.md)
    - [`Elastic File System`(across-AZ)](./compute/ec2/efs.md)
  - [Availability & Scalability](./compute/ec2/availability_scalability.md)
    - [`Auto Scale Group`](./compute/ec2/ec2_asg.md)
    - [`Elastic Load Balancer`](./compute/ec2/load_balancer.md)

- [`AWS Lambda`](./compute/lambda/lambda.md)

---

### Container Service

- [Container](./container/container.md)

  - [`AWS ECS`, `ECR` and `Fargate`](./container/ecs.md)
  - [`AWS EKS`(Kubernetes, Data Volumes)](./container/eks.md)

---

### Storage Service

- [Storage](./storage/storage.md)

  - [`AWS S3`(Object Store)](./storage/s3.md)
  - [`Amazon FSx`(3rd-party File system)](./storage/fsx.md)
  - [`AWS Storage Gateway`(Bridge on-premises <> AWS)](./storage/storage_gateway.md)

- **Data Migaration**

  - [`AWS Snow Family`(Physical Data Migration, Edge Computing)](./storage/snow.md)
  - [`AWS Transfer Family`(FTP)](./storage/transfer_family.md)
  - [`AWS DataSync`(Schedule data sync On-premises -> AWS)](./storage/datasync.md)

---

### Database Service

- Database Service

  - [`RDS`](./db_service/rds/rds.md)
  - [`Aurora`](./db_service/aurora/aurora.md)
  - [`ElasticCache`(in-memory databases)](./db_service/elasticcache/elasticcache.md)
  - [`AWS Dynamo` & `Dax`(nosql)](./db_service/dynamo/dynamo.md)
  - [Other Database](./db_service/db_service.md)

- [Disaster Recovery](./disaster_recovery/dr.md)

- [Migration](./migration/migration/migration.md)

  - [`Database Migration Service` & `SCT`(DB, continious replication )](./migration/dms/dms.md)
  - [`AWS Backup`(Centrally manage and automate backups)](./migration/backup/backup.md)
  - [`Application Discovery Service` & `Migration Hub`(plan, gather info)](./migration/app_disc/app_disc.md)
  - [`Application Migration Service(MGN)`(simplify migrating applications)](./migration/mgn/mgn.md)
  - [`AppFlow`(transfer data between Software-as-a-Service (SaaS) app and AWS)](./service/appflow/appflow.md)

- [Data & Analytics](./data_analytics/data_analytics/data_analytics.md)

  - [`Amazon Athena`(serverless, SQL, Federated Query, Parquet)](./data_analytics/athena/athena.md)
  - [`Amazon Redshift`(OLAP, Spectrum(S3 without loading), Enhanced VPC routing)](./data_analytics/redshift/redshift.md)
  - [`Amazon EMR`(Big Data, MapReduce, hadoop)](./data_analytics/emr/emr.md)
  - [`Amazon QuickSight`(Serverless, ml, BI, define users & groups dashboard )](./data_analytics/quicksight/quicksight.md)
  - [`AWS Glue`(serverless, ETL, Job Bookmarks,Elastic Views, DataBrew, Data Catalog, json CSV > Parquet)](./data_analytics/glue/glue.md)
  - [`AWS Lake Formation`(data lake, centralized access control)](./data_analytics/lake_formation/lake_formation.md)
  - [`Amazon OpenSearch`(partial matches, search any field, nearly real time)](./data_analytics/opensearch/opensearch.md)
  - [`Kinesis Data Analytics`(Real-time, Time-series, SQL app(firehose), Apache Flink(data stream))](./data_analytics/kinesis_analytics/kinesis_analytics.md)
  - [`Amazon MSK`(Apache Kafka, = Kinesis)](./data_analytics/msk/msk.md)

---

### Networking

- [Networking(VPC)](./networking/networking.md)

  - [Pricing(public > private)](./networking/pricing.md)
  - [`AWS VPC`(5 \* 5, /16-28, default, reserves)](./networking/vpc.md)
  - [`Bastion Host`(SSH)](./networking/bastion_host.md)
  - [`Internet Gateway(IGW)`(connect to the Internet, 1/vpc, route tb)](./networking/igw.md)
  - [`Nat Gateway`(Elastic IP, no sg, lock to AZ, route tb)](./networking/natgw.md)
  - [`NACL` (1/subnet,precedence, allow+deny, Stateless, Default, update) & `Security Group`(allow only, Stateful, refference)](./networking/nacl.md)
  - [`Egress-only Internet Gateway`( NATGW for IPv6, route tb)](./networking/egress_IGW.md)
  - [`VPC Peering`(Privately connect two VPCs, NOT transitive, accounts/regions, route tb)](./networking/peering.md)
  - [`VPC Endpoints`(connect to AWS services by PrivateLink,Interface(ENI$),Gateway(r tb: s3+dyn))](./networking/endpoint.md)
  - [`Site-to-Site VPN`(public, VPGW(Route Propagation,ICMP)+CGW(public IP)), `VPN CloudHub`(diff sites), `Direct Connect (DX)`(Dedicated private, 1M, Hybrid,Dedicated/Host, not encrypted,Gateway: cross regions)](./networking/vpn_dx.md)
  - [`Transit Gateway`(transitive peering, Xregion/account, VPN ECMP:bandwidth)](./networking/transit.md)
  - [`VPC Flow Logs`(monitor, Troubleshoot SG & NACL)](./networking/flow_log.md)
  - [`Traffic Mirroring`(capture ENIs)](./networking/traffic_mirroring.md)

- **Networking Service**

  - [`Route 53`(Hosted Zones, TTL(cache locally), Alias Records:AWS resource, Health Checks, Routing Policies)](./networking/route53/route53.md)
  - [`AWS CloudFront`(cached, Origin Access Control+s3 policy, TTL, Geo, Price Classes, Cache Invalidation) & `Global Accelerator`(route app by internal, lowest latency, non-HTTP + Static IP)](./networking/cloudfront/cloudfront.md)
  - [`AWS API Gateway`(versioning, Cache API responses, Edge-Optimized:default, IAM+Cognito)](./networking/gateway/gateway.md)

- [Machine learning services](./ml/ml.md)

- Other Services
  - [`CloudFormation`(infrastructure as code, template)](./service/cloudformation/cloudformation.md)
  - [`Simple Email Service`](./service/ses/ses.md)
  - [`Pinpoint`(marketing communications, sms)](./service/pinpoint/pinpoint.md)
  - [`Elastic Transcoder`(convert media files, s3)](./service/transcoder/transcoder.md)
  - [`AWS Batch`(batch processing, using ECS(Docker))](./service/batch/batch.md)

---

## Security

- [Encryption](./encryption/encryption.md)

  - [`AWS KMS`(manages encryption keys, only customer keys need creation, C/M automatic rotation:1Y Import:mannual, lock to region, AC:policy(xAccount), Client-side+multi-region key, S3 Replication:de+en, Xacc: share KMS CMK)](./encryption/kms.md)
  - [`AWS Systems Manager(SSM)`(View operational data, Parameter Store:(secrets+version, environment variables, Policies+TTL:force delete), Session Manager(shell+no SSH), Run Command(script), Patch Manager, Maintenance Windows(Automation) )](./encryption/systems_manager.md)
  - [`AWS Secrets Manager`(storing secrets, Multi-Region Secrets(replica))](./encryption/secret_manager.md)
  - [`AWS Certificate Manager(ACM)`(in-flight encryption, import cert notify expired:EventBridge+SNS,CloudFront :us-east-1)](./encryption/acm.md)

- [Security](./security/security.md)

  - [`AWS Web Application Firewall(WAF)`(http/Layer 7, ACL, no NLB, fixed IP: Globle acc+WAF+ALB)](./security/waf.md)
  - [`AWS Shield`(DDoS attack, Advanced:24/7+bill)](./security/shield.md)
  - [`AWS Firewall Manager`(Organization, Central:Security policy)](./security/firewall_manager.md)
  - [`Amazon GuardDuty`(Account thread, ml, no CW log, VPC Flow+DNS+CloudTrail Event)](./security/guardDuty.md)
  - [`Amazon Inspector`(Security Assessments:ec2, ecs, lambda)](./security/inspector.md)
  - [`AWS Macie`(S3 sensitive data)](./security/macie.md)
  - [`AWS Network Firewall`(VPC, traffic filtering)](./security/network_firewall.md)

---

[TOP](#aws-certified-solutions-architect-associate-saa-c03)
