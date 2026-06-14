# Ansible - with `AWS`

[Back](../ansible.md)

- [Ansible - with `AWS`](#ansible---with-aws)
  - [AWS Configuration](#aws-configuration)
    - [Lab: Query Default VPC](#lab-query-default-vpc)
    - [Lab: Create EC2](#lab-create-ec2)
    - [Lab: Delete EC2](#lab-delete-ec2)

---

## AWS Configuration

- Create key-pair for Ansible: `ansible`

- Ansible modules uses AWS SDK Boto3 for Python

```sh
# Install the AWS SDK for Python
pip install boto3 botocore

# confirm
ansible --version
python3 -c "import boto3, botocore; print('boto3:', boto3.__version__); print('botocore:', botocore.__version__)"
# boto3: 1.43.29
# botocore: 1.43.29

# Install the Ansible AWS collection
ansible-galaxy collection install amazon.aws

# Configure AWS Authentication
export AWS_ACCESS_KEY_ID="access_key_id"
export AWS_SECRET_ACCESS_KEY="secret_access_key"
export AWS_DEFAULT_REGION="us-east-1"

# command to confirm aws connection
ansible localhost -m amazon.aws.aws_caller_info
# localhost | SUCCESS => {
#     "account": "account_id",
#     "account_alias": "account_alias",
#     "arn": "arn",
#     "changed": false,
#     "user_id": "access_key_id"
# }

```

---

### Lab: Query Default VPC

```sh
# confirm with querying default vpc
cat > demo_aws_default_vpc.yml <<'EOF'
---
- name: Get AWS default VPC ID
  hosts: localhost
  connection: local
  gather_facts: false

  vars:
    aws_region: "{{ lookup('env', 'AWS_DEFAULT_REGION') | default('ca-central-1', true) }}"

  tasks:
    - name: Get default VPC information
      amazon.aws.ec2_vpc_net_info:
        region: "{{ aws_region }}"
        filters:
          isDefault: "true"
      register: default_vpc_result

    - name: Show default VPC ID
      ansible.builtin.debug:
        msg: "Default VPC ID in {{ aws_region }} is {{ default_vpc_result.vpcs[0].vpc_id }}"

    - name: Show full default VPC object
      ansible.builtin.debug:
        var: default_vpc_result.vpcs[0]
EOF

ansible-playbook demo_aws_default_vpc.yml --syntax-check
# playbook: demo_aws_default_vpc.yml

ansible-playbook demo_aws_default_vpc.yml
# PLAY [Get AWS default VPC ID] ******************************************************************************************************************************

# TASK [Get default VPC information] *************************************************************************************************************************
# ok: [localhost]

# TASK [Show default VPC ID] *********************************************************************************************************************************
# ok: [localhost] => {
#     "msg": "Default VPC ID in ca-central-1 is vpc-068d3dae3e308ea63"
# }

# TASK [Show full default VPC object] ************************************************************************************************************************
# ok: [localhost] => {
#     "default_vpc_result.vpcs[0]": {
#         "block_public_access_states": {
#             "internet_gateway_block_mode": "off"
#         },
#         "cidr_block": "172.31.0.0/16",
#         "cidr_block_association_set": [
#             {
#                 "association_id": "vpc-cidr-assoc-000bf93932e692ed0",
#                 "cidr_block": "172.31.0.0/16",
#                 "cidr_block_state": {
#                     "state": "associated"
#                 }
#             }
#         ],
#         "dhcp_options_id": "dopt-077605ecfdd0f617f",
#         "enable_dns_hostnames": true,
#         "enable_dns_support": true,
#         "id": "vpc-068d3dae3e308ea63",
#         "instance_tenancy": "default",
#         "is_default": true,
#         "owner_id": "099139718958",
#         "state": "available",
#         "tags": {
#             "Name": "Default VPC"
#         },
#         "vpc_id": "vpc-068d3dae3e308ea63"
#     }
# }

# PLAY RECAP *************************************************************************************************************************************************
# localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

```

---

### Lab: Create EC2

```yaml
# create-ec2.yml
---
- name: Create one EC2 instance from local Ansible
  hosts: localhost
  connection: local
  gather_facts: false

  vars:
    aws_region: "{{ lookup('env', 'AWS_DEFAULT_REGION') | default('ca-central-1', true) }}"
    ec2_name: "ansible-ec2"
    ec2_ami_id: "ami-084b86d4cca33d327"
    ec2_instance_type: "t3.micro"
    ec2_key_name: "ansible"
    ec2_subnet_id: "subnet-072bd92fbc35ffaca"

  tasks:
    - name: Create a security group in AWS for SSH access and HTTP
      amazon.aws.ec2_security_group:
        name: ansible
        tags:
          Name: "ansible"
          ManagedBy: "Ansible"
        description: Ansible Security Group
        region: "{{ aws_region }}"
        rules:
          - proto: tcp
            from_port: 80
            to_port: 80
            cidr_ip: 0.0.0.0/0
          - proto: tcp
            from_port: 22
            to_port: 22
            cidr_ip: 0.0.0.0/0
      register: ec2_secure_group

    - name: Create EC2 instance
      amazon.aws.ec2_instance:
        name: "{{ ec2_name }}"
        region: "{{ aws_region }}"
        instance_type: "{{ ec2_instance_type }}"
        image_id: "{{ ec2_ami_id }}"
        key_name: "{{ ec2_key_name }}"
        security_group: "{{ ec2_secure_group.group_id  }}"
        vpc_subnet_id: "{{ ec2_subnet_id }}"
        network:
          assign_public_ip: true
        wait: true
        count: 1
        tags:
          Name: "{{ ec2_name }}"
          ManagedBy: "Ansible"
        state: running
      register: ec2

    - name: Re-query instance to make sure public IP is populated
      amazon.aws.ec2_instance_info:
        region: "{{ aws_region }}"
        instance_ids: "{{ ec2.instances | map(attribute='instance_id') | list }}"
      register: ec2_info

    - name: Add all instance public IPs to host group
      add_host:
        hostname: "{{ item.public_ip_address }}"
        groups: ansible_hosts
      loop: "{{ ec2_info.instances }}"
      when: item.public_ip_address is defined

    - name: Show group
      debug:
        var: groups.ansible_hosts
```

```sh
ansible-playbook create-ec2.yml --syntax-check
# playbook: create-ec2.yml

ansible-playbook create-ec2.yml --list-hosts
# playbook: create-ec2.yml

#   play #1 (localhost): Create one EC2 instance from local Ansible       TAGS: []
#     pattern: ['localhost']
#     hosts (1):
#       localhost

ansible-playbook create-ec2.yml
# PLAY [Create one EC2 instance from local Ansible]
# ...
# TASK [Show group] ******************************************************************************************************************************************
# ok: [localhost] => {
#     "groups.ansible_hosts": [
#         "3.98.122.214"
#     ]
# }

```

---

### Lab: Delete EC2

```yaml
# delete-ec2.yml
---
- name: Delete EC2 instance by tag name
  hosts: localhost
  connection: local
  gather_facts: false

  vars:
    aws_region: "{{ lookup('env', 'AWS_DEFAULT_REGION') | default('ca-central-1', true) }}"
    ec2_name: "ansible-ec2"

  tasks:
    - name: Find EC2 instance by Name tag
      amazon.aws.ec2_instance_info:
        region: "{{ aws_region }}"
        filters:
          "tag:Name": "{{ ec2_name }}"
          instance-state-name:
            - pending
            - running
            - stopping
            - stopped
      register: found_instances

    - name: Terminate EC2 instance
      amazon.aws.ec2_instance:
        region: "{{ aws_region }}"
        instance_ids: "{{ found_instances.instances | map(attribute='instance_id') | list }}"
        state: absent
        wait: true
      when: found_instances.instances | length > 0

    - name: Show result
      ansible.builtin.debug:
        msg: "Deleted {{ found_instances.instances | length }} instance(s)."
```

```sh
ansible-playbook delete-ec2.yml
# PLAY [Delete EC2 instance by tag name] *********************************************************************************************************************

# TASK [Find EC2 instance by Name tag] ***********************************************************************************************************************
# ok: [localhost]

# TASK [Terminate EC2 instance] ******************************************************************************************************************************
# changed: [localhost]

# TASK [Show result] *****************************************************************************************************************************************
# ok: [localhost] => {
#     "msg": "Deleted 3 instance(s)."
# }

# PLAY RECAP *************************************************************************************************************************************************
# localhost                  : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
