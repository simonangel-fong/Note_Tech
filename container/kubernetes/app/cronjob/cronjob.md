# Kubernetes - CronJob

[Back](../../index.md)

- [Kubernetes - CronJob](#kubernetes---cronjob)
  - [CronJobs](#cronjobs)
    - [schedule](#schedule)
    - [Suspending and resuming](#suspending-and-resuming)
    - [Automatically removing finished Jobs](#automatically-removing-finished-jobs)
    - [start deadline](#start-deadline)
  - [Job concurrency](#job-concurrency)
    - [Imperative Command](#imperative-command)
  - [Lab: CronJob](#lab-cronjob)

---

## CronJobs

- `CronJob`

  - configure a job to run at a specific time.
  - specify a **Job template** and a **schedule**
    - `CronJob controller` creates a new `Job object` from the **template**, according to the `schedule`
    - `controller` will **continue** to create `Jobs` according to the **schedule** **until** the CronJob object gets **deleted**.

- When a `CronJob` Object is created, `CronJob Controller` creates a `Job` object controlled by the `CronJob` object underneath, which creates `pod` based on the schedule.

  - `Job` Object is controlled by the `CronJob`
    - no additional labels are added
    - The number at the end of the `job` name is the scheduled time of the Job in `Unix Epoch Time`, converted to minutes.
  - the underlying `pod` object is controlled by the `Job`
    - additional labels are added by the `Job` object

- When you **delete** the `CronJob`, all the `Jobs` it created will also be **deleted**.
  - When they’re deleted, the `Pods` are **deleted** as well, which causes their `containers` to **shut down gracefully**.
  - `kubectl delete cj --cascade=orphan`: keep the Jobs and the underlying Pods,

---

### schedule

- Format: `Minute Hour Day-of-Month Month Day-of-week `
- Expression:

  - `*`: matches any value
  - `5`: field value matches 5
  - `MAY`: Month field value matches "MAY"
  - `1-5`: A range of values, **includes** both limits
  - `JAN-MAY`: A range of values in Month field; between January and May (inclusive).
  - `1,2,5-8`: A list of numbers or ranges.
  - `*\/3`: Every Nth value, starting with the first value.; e.g., matches January, April, July, and October
  - `5/2`: Every Nth value, starting with the specified value; e.g., starting in May, May, July, September, or November.
  - `3-10/2`: The /N pattern can also be applied to ranges. e.g., March, May, July, and September.
  -

- special values

  - `@hourly`: to run the Job every hour (at the top of the hour)
  - `@daily`: to run it every day at **midnight**
  - `@weekly`: to run it every **Sunday at midnight**
  - `@monthly`: to run it at 0:00 on the **first day of each month**
  - `@yearly`/ `@annually`: to run it at **0:00 on January 1st** of each year.

- Setting the Time Zone
  - By **default**, the `CronJob controller` schedules `CronJobs` based on the **time zone** used by the `Controller Manager`.
  - `timeZone` field: specify the timezone

```yaml
spec:
  schedule: "0 3 * * *"
  timeZone: CET # Central European Time (CET time zone)
  jobTemplate:
```

---

### Suspending and resuming

- Suspend
  - `kubectl patch cj NAME -p '{"spec":{"suspend": true}}'`
- resume
  - `kubectl patch cj NAME -p '{"spec":{"suspend": false}}'`

---

### Automatically removing finished Jobs

- `successfulJobsHistoryLimit`:
  - specify how many successful `Jobs` to keep.
  - default: keeps 3 successful
- `failedJobsHistoryLimit`:
  - specify how many failed `Jobs` to keep.
  - default: keeps 1 failed Job.
- `Pod` associated with the `Jobs` are also **preserved**.

---

### start deadline

- if the cluster’s `Control Plane` is **overloaded** or if the `Controller Manager` component running the CronJob controller is **offline**, the delay of creating `Job` may be longer.

  - If it’s crucial that the `Job` shouldn’t start **too far after its scheduled time**, you can set a deadline in the `startingDeadlineSeconds` field

- `startingDeadlineSeconds` field

  - specify the limit of time when the job must be created; Otherwise, the Job won't be created.
  - a `MissSchedule` event will be generated

```yaml
spec:
  schedule: "* * * * *"
  startingDeadlineSeconds: 30
```

- If the `startingDeadlineSeconds` field **isn’t set** and the `CronJob controller` is **offline** for an extended period of time, undesirable behavior may occur when the controller **comes back online**.
  - the `controller` will **immediately create all** the Jobs that should have been created while it was offline.
  - However, this will only happen if the **number of missing jobs** is **less than 100**.
    - If the `controller` detects that **more than 100 Jobs** were missed, it **doesn’t create any Jobs**.
    - Instead, it generates a `TooManyMissedTimes` event.
  - By setting the start deadline, you can prevent this from happening.

---

## Job concurrency

- `Job concurrency`

  - multiple `jobs` of a `CronJob` run at a time

- By default, the `CronJob controller` creates new Jobs **regardless of** how many previous Jobs are **still active**.

- `spec.concurrencyPolicy` field

  - specify the behavior of job concurrency
  - `Allow`:

    - default
    - allow 2 jobs run concurrently
    - new Job will be created on schedule, regarless of whether the previous Job completed or not.

  - `Forbid`

    - Concurrent runs are prohibited.
    - If the **previous run** is still **active** when a new run is to be scheduled, the `CronJob controller` records a `JobAlreadyActive` event and **skips creating** a new Job.

  - `Replace`
    - The **active Job** is **canceled** and **replaced** by a **new** one.
    - The `CronJob controller` **cancels the active Job** by **deleting** the Job object.
    - The `Job controller` then **deletes** the Pods, but they’re allowed to **terminate gracefully**.
      - This means that two Jobs are still running at the same time, but one of them is being terminated.

---

### Imperative Command

| Command                                                                | Description                                                                         |
| ---------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `kubectl get cronjobs`/`kubectl get cj`                                | Lists all CronJobs, showing the schedule and last run time.                         |
| `kubectl describe cronjob <name>`                                      | Shows the schedule, active jobs, and the history of successful/failed runs.         |
| `kubectl create cronjob <name> --image=<img> --schedule="*/5 * * * *"` | Creates a new CronJob that runs every 5 minutes.                                    |
| `kubectl create job <job-name> --from=cronjob/<cj-name>`               | Manual Trigger: Runs the CronJob task immediately without waiting for the schedule. |
| `kubectl patch cronjob <name> -p '{"spec" : {"suspend" : true}}'`      | Pause: Stops the CronJob from triggering new tasks.                                 |
| `kubectl patch cronjob <name> -p '{"spec" : {"suspend" : false}}'`     | Resume: Allows a suspended CronJob to start running on schedule again.              |
| `kubectl edit cronjob <name>`                                          | Opens the CronJob YAML in your editor to quickly change the schedule or image.      |
| `kubectl delete cronjob <name>`                                        | Deletes the CronJob and all Jobs/Pods it previously created.                        |

---

## Lab: CronJob

```yaml
# demo-cronjob-minute.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: demo-cronjob-minute
spec:
  schedule: "10 * * * *" # every 10 minutes
  jobTemplate:
    metadata:
      labels:
        app: busybox
    spec:
      template:
        metadata:
          labels:
            app: busybox
        spec:
          restartPolicy: OnFailure
          volumes:
            - name: local-storage
              hostPath:
                path: /tmp/data
                type: DirectoryOrCreate
          containers:
            - name: busybox
              image: busybox
              volumeMounts:
                - name: local-storage
                  mountPath: /data
              command:
                - "/bin/sh"
                - "-c"
              args:
                - |
                  echo "$(date) CronJob message";
                  echo "$(date) CronJob message" >> /data/message.txt;
                  sleep 30;
```

```sh
kubectl apply -f demo-cronjob-minute.yaml
# cronjob.batch/demo-cronjob-minute created

kubectl get cronjob -w
# NAME                  SCHEDULE       TIMEZONE   SUSPEND   ACTIVE   LAST SCHEDULE   AGE
# demo-cronjob-minute   */10 * * * *   <none>     False     0        <none>          9m20s
# demo-cronjob-minute   */10 * * * *   <none>     False     1        0s              9m36s
# demo-cronjob-minute   */10 * * * *   <none>     False     0        34s             10m
# demo-cronjob-minute   */10 * * * *   <none>     False     1        0s              19m
# demo-cronjob-minute   */10 * * * *   <none>     False     0        36s             20m

#
kubectl describe cronjob demo-cronjob-minute
# Name:                          demo-cronjob-minute
# Namespace:                     default
# Labels:                        <none>
# Annotations:                   <none>
# Schedule:                      */10 * * * *
# Concurrency Policy:            Allow
# Suspend:                       False
# Successful Job History Limit:  3
# Failed Job History Limit:      1
# Starting Deadline Seconds:     <unset>
# Selector:                      <unset>
# Parallelism:                   <unset>
# Completions:                   <unset>
# Pod Template:
#   Labels:  app=busybox
#   Containers:
#    busybox:
#     Image:      busybox
#     Port:       <none>
#     Host Port:  <none>
#     Command:
#       /bin/sh
#       -c
#     Args:
#       echo "$(date) CronJob message";
#       echo "$(date) CronJob message" >> /data/message.txt;
#       sleep 30;

#     Environment:  <none>
#     Mounts:
#       /data from local-storage (rw)
#   Volumes:
#    local-storage:
#     Type:            HostPath (bare host directory volume)
#     Path:            /tmp/data
#     HostPathType:    DirectoryOrCreate
#   Node-Selectors:    <none>
#   Tolerations:       <none>
# Last Schedule Time:  Sat, 03 Jan 2026 14:00:00 -0500
# Active Jobs:         <none>
# Events:
#   Type    Reason            Age   From                Message
#   ----    ------            ----  ----                -------
#   Normal  SuccessfulCreate  11m   cronjob-controller  Created job demo-cronjob-minute-29457770
#   Normal  SawCompletedJob   10m   cronjob-controller  Saw completed job: demo-cronjob-minute-29457770, condition: Complete
#   Normal  SuccessfulCreate  76s   cronjob-controller  Created job demo-cronjob-minute-29457780
#   Normal  SawCompletedJob   40s   cronjob-controller  Saw completed job: demo-cronjob-minute-29457780, condition: Complete`


# confirm create a job and run per 10 min
kubectl get job -w
# NAME                           STATUS    COMPLETIONS   DURATION   AGE
# demo-cronjob-minute-29457770   Running   0/1                      0s
# demo-cronjob-minute-29457770   Running   0/1           0s         0s
# demo-cronjob-minute-29457770   Running   0/1           4s         4s
# demo-cronjob-minute-29457770   Running   0/1           33s        33s
# demo-cronjob-minute-29457770   SuccessCriteriaMet   0/1           34s        34s
# demo-cronjob-minute-29457770   Complete             1/1           34s        34s
# demo-cronjob-minute-29457780   Running              0/1                      0s
# demo-cronjob-minute-29457780   Running              0/1           0s         0s
# demo-cronjob-minute-29457780   Running              0/1           4s         4s
# demo-cronjob-minute-29457780   Running              0/1           35s        35s
# demo-cronjob-minute-29457780   SuccessCriteriaMet   0/1           36s        36s
# demo-cronjob-minute-29457780   Complete             1/1           36s        36s

# confirm controled by cronjob
kubectl describe job demo-cronjob-minute-29457770
# Name:             demo-cronjob-minute-29457770
# Namespace:        default
# Selector:         batch.kubernetes.io/controller-uid=c43ac375-388f-452b-b215-204c6816bcb7
# Labels:           app=busybox
# Annotations:      batch.kubernetes.io/cronjob-scheduled-timestamp: 2026-01-03T18:50:00Z
# Controlled By:    CronJob/demo-cronjob-minute
# Parallelism:      1
# Completions:      1
# Completion Mode:  NonIndexed
# Suspend:          false
# Backoff Limit:    6
# Start Time:       Sat, 03 Jan 2026 13:50:00 -0500
# Completed At:     Sat, 03 Jan 2026 13:50:34 -0500
# Duration:         34s
# Pods Statuses:    0 Active (0 Ready) / 1 Succeeded / 0 Failed
# Pod Template:
#   Labels:  app=busybox
#            batch.kubernetes.io/controller-uid=c43ac375-388f-452b-b215-204c6816bcb7
#            batch.kubernetes.io/job-name=demo-cronjob-minute-29457770
#            controller-uid=c43ac375-388f-452b-b215-204c6816bcb7
#            job-name=demo-cronjob-minute-29457770
#   Containers:
#    busybox:
#     Image:      busybox
#     Port:       <none>
#     Host Port:  <none>
#     Command:
#       /bin/sh
#       -c
#     Args:
#       echo "$(date) CronJob message";
#       echo "$(date) CronJob message" >> /data/message.txt;
#       sleep 30;

#     Environment:  <none>
#     Mounts:
#       /data from local-storage (rw)
#   Volumes:
#    local-storage:
#     Type:          HostPath (bare host directory volume)
#     Path:          /tmp/data
#     HostPathType:  DirectoryOrCreate
#   Node-Selectors:  <none>
#   Tolerations:     <none>
# Events:
#   Type    Reason            Age   From            Message
#   ----    ------            ----  ----            -------
#   Normal  SuccessfulCreate  12m   job-controller  Created pod: demo-cronjob-minute-29457770-tfmrj
#   Normal  Completed         11m   job-controller  Job completed

# confirm create a pod per 10 min
kubectl get pod
# NAME                                 READY   STATUS      RESTARTS      AGE
# demo-cronjob-minute-29457770-tfmrj   0/1     Completed   0             13m
# demo-cronjob-minute-29457780-n7fd9   0/1     Completed   0             3m7s

# confirm: per 10 min
kubectl get pod -w
# NAME                                  READY   STATUS    RESTARTS      AGE
# demo-cronjob-minute-29457770-tfmrj   0/1     Pending   0             0s
# demo-cronjob-minute-29457770-tfmrj   0/1     Pending   0             0s
# demo-cronjob-minute-29457770-tfmrj   0/1     ContainerCreating   0             0s
# demo-cronjob-minute-29457770-tfmrj   1/1     Running             0             3s
# demo-cronjob-minute-29457770-tfmrj   0/1     Completed           0             32s
# demo-cronjob-minute-29457770-tfmrj   0/1     Completed           0             34s
# demo-cronjob-minute-29457770-tfmrj   0/1     Completed           0             34s
# demo-cronjob-minute-29457780-n7fd9   0/1     Pending             0             0s
# demo-cronjob-minute-29457780-n7fd9   0/1     Pending             0             0s
# demo-cronjob-minute-29457780-n7fd9   0/1     ContainerCreating   0             0s
# demo-cronjob-minute-29457780-n7fd9   1/1     Running             0             3s
# demo-cronjob-minute-29457780-n7fd9   0/1     Completed           0             34s
# demo-cronjob-minute-29457780-n7fd9   0/1     Completed           0             36s
# demo-cronjob-minute-29457780-n7fd9   0/1     Completed           0             36s

# cofnirm: controlled by job
kubectl describe pod demo-cronjob-minute-29457780-n7fd9
# Name:             demo-cronjob-minute-29457780-n7fd9
# Namespace:        default
# Priority:         0
# Service Account:  default
# Node:             docker-desktop/192.168.65.3
# Start Time:       Sat, 03 Jan 2026 14:00:00 -0500
# Labels:           app=busybox
#                   batch.kubernetes.io/controller-uid=b49e44de-881b-4459-998d-8daadd455727
#                   batch.kubernetes.io/job-name=demo-cronjob-minute-29457780
#                   controller-uid=b49e44de-881b-4459-998d-8daadd455727
#                   job-name=demo-cronjob-minute-29457780
# Annotations:      <none>
# Status:           Succeeded
# IP:               10.1.4.196
# IPs:
#   IP:           10.1.4.196
# Controlled By:  Job/demo-cronjob-minute-29457780
# Containers:
#   busybox:
#     Container ID:  docker://5c4f643661177a4842aa77c3ea458be22d43a93d9f555b0b35db34c29ab900db
#     Image:         busybox
#     Image ID:      docker-pullable://busybox@sha256:d80cd694d3e9467884fcb94b8ca1e20437d8a501096cdf367a5a1918a34fc2fd
#     Port:          <none>
#     Host Port:     <none>
#     Command:
#       /bin/sh
#       -c
#     Args:
#       echo "$(date) CronJob message";
#       echo "$(date) CronJob message" >> /data/message.txt;
#       sleep 30;

#     State:          Terminated
#       Reason:       Completed
#       Exit Code:    0
#       Started:      Sat, 03 Jan 2026 14:00:03 -0500
#       Finished:     Sat, 03 Jan 2026 14:00:33 -0500
#     Ready:          False
#     Restart Count:  0
#     Environment:    <none>
#     Mounts:
#       /data from local-storage (rw)
#       /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-sd879 (ro)
# Conditions:
#   Type                        Status
#   PodReadyToStartContainers   False
#   Initialized                 True
#   Ready                       False
#   ContainersReady             False
#   PodScheduled                True
# Volumes:
#   local-storage:
#     Type:          HostPath (bare host directory volume)
#     Path:          /tmp/data
#     HostPathType:  DirectoryOrCreate
#   kube-api-access-sd879:
#     Type:                    Projected (a volume that contains injected data from multiple sources)
#     TokenExpirationSeconds:  3607
#     ConfigMapName:           kube-root-ca.crt
#     Optional:                false
#     DownwardAPI:             true
# QoS Class:                   BestEffort
# Node-Selectors:              <none>
# Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
#                              node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
# Events:
#   Type    Reason     Age    From               Message
#   ----    ------     ----   ----               -------
#   Normal  Scheduled  3m31s  default-scheduler  Successfully assigned default/demo-cronjob-minute-29457780-n7fd9 to docker-desktop
#   Normal  Pulling    3m30s  kubelet            Pulling image "busybox"
#   Normal  Pulled     3m29s  kubelet            Successfully pulled image "busybox" in 1.383s (1.383s including waiting). Image size: 2224358 bytes.
#   Normal  Created    3m28s  kubelet            Created container: busybox
#   Normal  Started    3m28s  kubelet            Started container busybox

# check log confirm write message per 10 min
kubectl exec -it observer -- cat /data/message.txt
# Sat Jan  3 18:50:02 UTC 2026 CronJob message
# Sat Jan  3 19:00:03 UTC 2026 CronJob message

kubectl exec -it observer -- rm /data/message.txt
```

---
