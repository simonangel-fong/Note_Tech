# GitHub Actions - Setup Local Environment

[Back](../index.md)

- [GitHub Actions - Setup Local Environment](#github-actions---setup-local-environment)
  - [Tools: `act`](#tools-act)
    - [Install](#install)
    - [Common Commands](#common-commands)
    - [Lab: Push](#lab-push)

---

## Tools: `act`

- `act`
  - https://nektosact.com/installation/winget.html
  - https://github.com/nektos/act

---

### Install

```sh
winget install nektos.act
```

---

### Common Commands

| Command            | Description |
| ------------------ | ----------- |
| `act -l`           | List all    |
| `act push`         | Push event  |
| `act pull_request` | PR event    |

---

### Lab: Push


```sh
act -l

act push
# time="2026-04-26T22:27:18-04:00" level=info msg="Using docker host 'npipe:////./pipe/docker_engine', and daemon socket 'npipe:////./pipe/docker_engine'"
# [01 - Building Block/echo-hello] ⭐ Run Set up job
# [01 - Building Block/echo-bye  ] ⭐ Run Set up job
# [01 - Building Block/echo-bye  ] 🚀  Start image=catthehacker/ubuntu:act-latest
# [01 - Building Block/echo-hello] 🚀  Start image=catthehacker/ubuntu:act-latest
# [01 - Building Block/echo-hello]   🐳  docker pull image=catthehacker/ubuntu:act-latest platform= username= forcePull=true
# [01 - Building Block/echo-bye  ]   🐳  docker pull image=catthehacker/ubuntu:act-latest platform= username= forcePull=true
# [01 - Building Block/echo-bye  ] using DockerAuthConfig authentication for docker pull
# [01 - Building Block/echo-hello] using DockerAuthConfig authentication for docker pull
# [01 - Building Block/echo-hello]   🐳  docker create image=catthehacker/ubuntu:act-latest platform= entrypoint=["tail" "-f" "/dev/null"] cmd=[] network="host"
# [01 - Building Block/echo-bye  ]   🐳  docker create image=catthehacker/ubuntu:act-latest platform= entrypoint=["tail" "-f" "/dev/null"] cmd=[] network="host"
# [01 - Building Block/echo-bye  ]   🐳  docker run image=catthehacker/ubuntu:act-latest platform= entrypoint=["tail" "-f" "/dev/null"] cmd=[] network="host"
# [01 - Building Block/echo-hello]   🐳  docker run image=catthehacker/ubuntu:act-latest platform= entrypoint=["tail" "-f" "/dev/null"] cmd=[] network="host"
# [01 - Building Block/echo-bye  ]   🐳  docker exec cmd=[node --no-warnings -e console.log(process.execPath)] user= workdir=
# [01 - Building Block/echo-hello]   🐳  docker exec cmd=[node --no-warnings -e console.log(process.execPath)] user= workdir=
# [01 - Building Block/echo-bye  ]   ✅  Success - Set up job
# [01 - Building Block/echo-hello]   ✅  Success - Set up job
# [01 - Building Block/echo-bye  ] ⭐ Run Main fails
# [01 - Building Block/echo-hello] ⭐ Run Main say hello
# [01 - Building Block/echo-bye  ]   🐳  docker exec cmd=[bash -e /var/run/act/workflow/0] user= workdir=
# [01 - Building Block/echo-hello]   🐳  docker exec cmd=[bash -e /var/run/act/workflow/0] user= workdir=
# | will fail
# [01 - Building Block/echo-bye  ]   ❌  Failure - Main fails [125.7148ms]
# | hello world
# [01 - Building Block/echo-hello]   ✅  Success - Main say hello [121.2167ms]
# [01 - Building Block/echo-bye  ] exitcode '1': failure
# [01 - Building Block/echo-hello] ⭐ Run Complete job
# [01 - Building Block/echo-hello] Cleaning up container for job echo-hello
# [01 - Building Block/echo-bye  ] ⭐ Run Complete job
# [01 - Building Block/echo-bye  ]   ✅  Success - Complete job
# [01 - Building Block/echo-bye  ] 🏁  Job failed
# [01 - Building Block/echo-hello]   ✅  Success - Complete job
# [01 - Building Block/echo-hello] 🏁  Job succeeded
# Error: Job 'echo-bye' failed
```