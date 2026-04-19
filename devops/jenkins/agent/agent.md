# Jenkins - Agent

[Back](../index.md)

- [Jenkins - Agent](#jenkins---agent)
  - [Dedicated Docker Agent (long-running)](#dedicated-docker-agent-long-running)
  - [Ephemeral Docker Agents](#ephemeral-docker-agents)
  - [Kubernetes Agents](#kubernetes-agents)

---

## Dedicated Docker Agent (long-running)

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

## Ephemeral Docker Agents

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

## Kubernetes Agents

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
