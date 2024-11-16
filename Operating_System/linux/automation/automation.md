# Linux - Automation

[Back](../index.md)

---

- [Linux - Automation](#linux---automation)
  - [Cron](#cron)
    - [`Crontab` Format](#crontab-format)
  - [Cron COmmand](#cron-command)
    - [Example: Create a cron job](#example-create-a-cron-job)

---

## Cron

- `CRON`/`command run on notice`

  - a daemon/background process executing **non-interactive** jobs.
  - A **time based job** scheduling service.

- `crontab`
  - A program to create, read, update, and delete your job schedules.
  - Use cron to **schedule** and **automate** tasks.

---

### `Crontab` Format

- 2 parts:

  - when to run
    - match definition with current date and time.
  - what command to run

![cron](./pic/cron.jpeg)

- `* * * * * command`

  - Minute (0-59)
  - Hour (0-23)
  - Day of the Month (1-31)
  - Month of the Year (1-12)
  - Day of the Week (0-6)
    - `0`: Sunday

- Example

```sh
# Run every Monday at 07:00.
0 7 * * 1 /opt/sales/bin/weekly-report

# Run at 02:00 every day and
# send output to a log file.
0 2 * * * /root/backupdb > /tmp/db.log 2>&1

# Run every 15 minutes.
0,15,30,45 * * * * /opt/acme/bin/15-min-check
# Run every 15 minutes.
*/15 * * * * /opt/acme/bin/15-min-check

# Run every 30 minutes.
0,30 * * * * /opt/acme/bin/half-hour-check

# Another way to do the same thing.
* */2 * * * /opt/acme/bin/half-hour-check

# Run for the first 5 minutes of the hour
0-4 * * * * /opt/acme/bin/first-five-mins
```

---

- Crontab Shortcuts

| Shortcut    | Time        |
| ----------- | ----------- |
| `@hourly`   | `0 * * * *` |
| `@midnight` | `0 0 * * *` |
| `@daily`    | `0 0 * * *` |
| `@weekly`   | `0 0 * * 0` |
| `@monthly`  | `0 0 1 * *` |
| `@yearly`   | `0 0 1 1 *` |
| `@annually` | `0 0 1 1 *` |

---

## Cron COmmand

| CMD            | DESC                             |
| -------------- | -------------------------------- |
| `crontab file` | Install a new crontab from file. |
| `crontab -l`   | List your cron jobs.             |
| `crontab -e`   | Edit your cron jobs.             |
| `crontab -r`   | Remove all of your cron jobs.    |

---

### Example: Create a cron job

```sh
# create a cron file
vi 5-min-log-cron

# run every 5 minutes
*/5 * * * * echo "$(date) hello world" >> /home/rheladmin/log

# create a cron job
crontab 5-min-log-cron

# list all cron job
crontab -l
# # run every 5 minutes
# */5 * * * * echo "$(date) Hello world" >> /home/rheladmin/log

# remove all cron jobs
crontab -r
```
