

demo: hooks

job: echo message
pre-upgrade

1.install; confirm by kube get -o yaml for annontation
no job
2.change image tag; upgrade; job execute
confirm job complete
3.update hook-succeeded
upgrade
confirm job get deleted

---

demo: weight

2 jobs, echo
weight: 1,2

execute, check job -w


---

failure

demo: pre-upgrade

deploy: nginx tag=0
job: pre-upgrade; exit 1; limit fail=2


install
update nginx tag=1; upgrade
confirm helm history: fail
k get job
k get po; confirm nginx tag=0

---

demo: post upgrade

deploy: nginx tag=0
job: post-upgrade; exit 1; limit fail=2

install
update tag=1; upgrade
confirm history
k get po: tag=1

- upgrade --atomic
confirm: tag=0
history: auto rollback to last successful deploy