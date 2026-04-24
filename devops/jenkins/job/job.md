# Jenkins - Job

[Back](../index.md)

- [Jenkins - Job](#jenkins---job)
  - [Job](#job)
    - [Trigger](#trigger)
  - [Lab: Execute a bash script](#lab-execute-a-bash-script)
  - [Lab: Parameterized](#lab-parameterized)
    - [String Parameters](#string-parameters)
    - [Choose Parameters](#choose-parameters)
    - [Boolean Parameters](#boolean-parameters)
  - [API Call](#api-call)
    - [Lab: triger a job via API](#lab-triger-a-job-via-api)

---

## Job

When creating a job in Jenkins, it creates a new directory in the `/var/jenkins_home/workspace/`

- `/var/jenkins_home/workspace/<job_name>`

![pic](./pic/job01.png)

---

### Trigger

| Trigger Method                  | Description                                                                                               |
| ------------------------------- | --------------------------------------------------------------------------------------------------------- |
| **Manual trigger**              | clicks **Build Now** in Jenkins. Common for test, staging, or production deployment approval.             |
| **SCM polling**                 | Jenkins checks Git **regularly** for changes, such as every 5 minutes.                                    |
| **Webhook trigger**             | Repo **sends a request** to Jenkins when code is pushed or a PR is created.                               |
| **Scheduled trigger**           | Runs by **cron schedule**, such as nightly builds or **weekly security scans**.                           |
| **Upstream/downstream trigger** | One Jenkins **job triggers another job** after success or failure.                                        |
| **Parameterized trigger**       | User or another system starts a **job with parameters**, such as `env=dev` or `version=1.2.0`.            |
| **Remote/API trigger**          | External tools call Jenkins `REST API` to start a job.                                                    |
| **Pull request trigger**        | Jenkins runs checks automatically when a **PR is opened or updated**. Common for validation before merge. |

- `Poll SCM`
  - a build **trigger mechanism** that **periodically checks** (polls) your `Source Control Management system` (like Git or SVN) for code changes.

- Cron syntax:

```txt
Minute Hour Date Month weekday
```

---

## Lab: Execute a bash script

- Env:
  - Host OS: ubuntu
  - Jenkins Deploy: Docker

---

- Create a shell script

```sh
cat > demo-script.sh <<'EOF'
#!/bin/bash

NICKNAME=$1
MSG=$2

echo "Hi, $NICKNAME. This is the message: $MSG"
EOF

chmod +x demo-script.sh

./demo-script.sh Adam "Mission completed."
# Hi, Adam. This is the message: Mission completed.

# copy to docker container
docker ps
# CONTAINER ID   IMAGE                       COMMAND                  CREATED          STATUS          PORTS                                                                                          NAMES
# c818c31087ad   jenkins/jenkins:lts-jdk21   "/usr/bin/tini -- /u…"   32 minutes ago   Up 32 minutes   0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp, 0.0.0.0:50000->50000/tcp, [::]:50000->50000/tcp   jenkins
docker cp demo-script.sh jenkins:/tmp/demo-script.sh
# Successfully copied 2.05kB to jenkins:/tmp/demo-script.sh

# test in container
docker exec -it jenkins /tmp/demo-script.sh Adam "Mission completed."
# Hi, Adam. This is the message: Mission completed.
```

- Update the job
  - shell script

```sh
/tmp/demo-script.sh Adam "Mission completed."
```

![pic](./pic/job02.png)

---

## Lab: Parameterized

### String Parameters

- Based on previous bash script
- Set parameters
  - "This project is parameterized" -> "String Parameter"

![pic](./pic/job03.png)

- Update job shell script

```sh
echo "NICKNAME: $NICKNAME"
echo "MSG: $MSG"
/tmp/demo-script.sh $NICKNAME $MSG
```

![pic](./pic/job04.png)

---

### Choose Parameters

![pic](./pic/job05.png)

- Update shell script

```sh
/tmp/demo-script.sh $NICKNAME $MSG $SUBFIX
```

- execute

![pic](./pic/job06.png)

---

### Boolean Parameters

- Update shell script

```sh
cat > demo-script.sh <<'EOF'
#!/bin/bash

NICKNAME=$1
MSG=$2
FLAG=$3

if [ "$FLAG" = "true" ]; then
  echo "Hi, $NICKNAME. This is the message: $MSG"
else
  echo "Flag is not true."
fi

EOF

# test locally
./demo-script.sh Adam "Mission completed." true
# Hi, Adam. This is the message: Mission completed.
./demo-script.sh Adam "Mission completed."
# Flag is not true.

docker cp demo-script.sh jenkins:/tmp/demo-script.sh
# Successfully copied 2.05kB to jenkins:/tmp/demo-script.sh
```

- Add boolean param

![pic](./pic/job07.png)

- Update job script

```sh
echo "NICKNAME: $NICKNAME"
echo "MSG: $MSG"
echo "FLAG: $FLAG"
/tmp/demo-script.sh $NICKNAME $MSG $FLAG
```

- Execute

![pic](./pic/job08.png)

---

## API Call

- ref: https://www.jenkins.io/doc/book/using/remote-access-api/
- Job can be invoked by API call
- Common paths:
  - `/job/<job_name>/build`: build a job
  - `/job/<folder>/job/<job_name>/build`: with folder
  - `/job/<pipeline>/job/<branch>/build`: with pipeline and branch

---

### Lab: triger a job via API

- Create user: jenkins_trigger
- Create global role: trigger
  - Overall: Read
  - Job: Build, Read
- Assign role
- Login as new user
- Create API token: User profile > Security > API Token > Add new token
- Test: build a job
- enable CSRF protection:
  - Manage Jenkins > Security: CSRF Protection = Crumb Issuer

- Trigger non-parameterized job

```sh
# Step 1: Get crumb
CRUMB=$(curl -u jenkins_trigger:<api_token> \
  http://<jenkins_host>/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb))

# Step 2: Use crumb
curl -u jenkins_trigger:<api_token> \
  -H "$CRUMB" \
  -X POST http://<jenkins_host>/job/<job_name>/build?delay=0sec
```

- Parameterized jobs

```sh
curl -u jenkins_trigger:<api_token> \
  -X POST "http://<jenkins_host>/job/<job_name>/buildWithParameters"
  --data param1=value1 --data param2=value2
```

![pic](./pic/trigger_api01.png)

---
