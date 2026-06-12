demo

1.helm create

2.helm install
3.helm test
4.change wget error; helm upgrade; confirm fails

---

demo: decouple testing script with helm test

create a cm for testing script
test hook
files.Glob test-scripts with tpl function
create script in test-scripts: shell apk update, wget

template to confirm script get injected values

update test
command
volumes configmap; defaultmode 0744; volumemount

helm upgrade
helm test

---

demo: helm test with values
