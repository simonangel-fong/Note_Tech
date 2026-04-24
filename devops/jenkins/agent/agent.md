# Jenkins - Agent

[Back](../index.md)

- [Jenkins - Agent](#jenkins---agent)
  - [Jenkins Agent](#jenkins-agent)
  - [Static Docker Agent](#static-docker-agent)
  - [Dynamic Agents](#dynamic-agents)
    - [Docker Agents](#docker-agents)
    - [Kubernetes Agents](#kubernetes-agents)

---

## Jenkins Agent

- `Jenkins agent`
  - formerly "slave" or simply "node"
  - a **separate machine, virtual machine, or container** that connects to a `Jenkins controller` to **execute build, test, and deployment jobs**

| Agent Type         | Description                                                                                  |
| ------------------ | -------------------------------------------------------------------------------------------- |
| **Built-in agent** | Runs jobs directly on the **Jenkins controller** itself Jenkins controller runs jobs locally |
| **Static agent**   | A **fixed** VM, physical server, or long-running machine connected to Jenkins                |
| **Dynamic agent**  | An agent created **on demand** when a job starts and removed after the job finishes          |

- Docker agent needs to mount host Docker socket: `-v /var/run/docker.sock:/var/run/docker.sock`

---

## Static Docker Agent

- Architecture:
  - Jenkins controller (Docker)
  - Separate container running:
    - long-running
    - jenkins-agent image

```sh
docker network create jenkins-net

# connect jenkins
docker network connect jenkins-net jenkins
```

- Setup agent
  - Manage Jenkins -> Nodes -> New node

![pic](./pic/agent_docker01.png)

![pic](./pic/agent_docker02.png)

- Create agent

```sh
docker run -d \
  --name jenkins-agent \
  --network jenkins-net \
  -e JENKINS_URL=http://jenkins:8080/ \
  -e JENKINS_AGENT_NAME=docker-agent \
  -e JENKINS_SECRET=<secret>  \
  -v jenkins-agent-work:/home/jenkins/agent \
  jenkins/inbound-agent
```

- run pipeline

```groovy
pipeline {
    agent { label 'docker' }

    stages {
        stage('Hello') {
            steps {
                sh 'echo Hello World from agent'
                sh 'hostname'
            }
        }
    }
}
```

![pic](./pic/agent_docker03.png)

---

## Dynamic Agents

### Docker Agents

- need:
  - mount host Docker socket: `-v /var/run/docker.sock:/var/run/docker.sock`
- Spins up a fresh container per build
- production standard

- Example:

```groovy
pipeline {
    agent {
        docker {
            image 'node:18'
        }
    }
    stages {
        stage('Build') {
            steps {
                sh 'node -v'
                sh 'npm install'
            }
        }
    }
}
```

---

### Kubernetes Agents

- MOST COMMON in production
  - EKS / GKE / AKS environments
- With Kubernetes plugin:
  - Jenkins dynamically creates pods as agents

```groovy
pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: node
    image: node:18
    command:
    - cat
    tty: true
"""
        }
    }
    stages {
        stage('Build') {
            steps {
                container('node') {
                    sh 'node -v'
                }
            }
        }
    }
}
```
