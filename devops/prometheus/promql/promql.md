# Prometheus - PromQL

[Back](../index.md)

- [Prometheus - PromQL](#prometheus---promql)
  - [PromQL](#promql)
    - [Data Types](#data-types)
  - [Lab:](#lab)
  - [Operator](#operator)
    - [Comparison Binary Operators](#comparison-binary-operators)
    - [Set operator](#set-operator)
    - [Fileter Matchers/Selectors](#fileter-matchersselectors)
    - [Aggregation Operator](#aggregation-operator)
    - [Time Offsets](#time-offsets)
  - [Functions](#functions)

---

## PromQL

### Data Types

- Scalar:
  - Float
    - include integer
    - i.e., 1, 1.5
    - using `""`
  - String
    - using `""`/`''`
- Example:

```promql
<!-- store -->
prometheus_http_requests_total{code="200",job="prometheus"}

<!-- query, query a metric with 2** code-->
prometheus_http_requests_total{code=~"2.*",job="prometheus"}
<!-- query, query a metric with 200 code -->
prometheus_http_requests_total{code=~"200",job="prometheus"}
```

- `Instant Vectors`
  - Instance vector selections allow the selection of a set of time series and a single sample value for each at a given timestamp
  - Only a metric name is specified.
  - result can be filtered by labels.

```promsql
auth_api_hit  # 5
auth_api_hit{count=1,time_taken=800}  # 1
```

- `Range Vectors`

  - similar to `instant vector` except they select a range of samples.
  - need to specify a time range
  - `label_name[time_spec]`

- 2 factors affect the return
  - scrape_interval in the cf
  - time_spec in the query

```promsql
auth_api_hit[5m]    # returns the last 5 minutes
```

| Time spec | Time span               |
| --------- | ----------------------- |
| ms        | milliseconds            |
| m         | seconds                 |
| h         | hours                   |
| d         | days (a day has 24h)    |
| w         | weeks (a week has 7d)   |
| y         | years (a year has 365d) |

---

## Lab:

- Instant Vector

```promql
node_network_info
# node_network_info{address="00:00:00:00:00:00", adminstate="up", app="app_server", broadcast="00:00:00:00:00:00", device="lo", instance="192.168.100.105:9100", job="app_server", operstate="unknown"}	1
# node_network_info{address="00:0c:29:f1:f4:7f", adminstate="up", app="app_server", broadcast="ff:ff:ff:ff:ff:ff", device="ens33", duplex="full", instance="192.168.100.105:9100", job="app_server", operstate="up"}	1
# node_network_info{address="c2:77:27:7b:04:a4", adminstate="up", app="app_server", broadcast="ff:ff:ff:ff:ff:ff", device="docker0", duplex="unknown", instance="192.168.100.105:9100", job="app_server", operstate="down"}	1
# node_network_info{address="26:3a:40:b1:42:0c", adminstate="up", app="app_server", broadcast="ff:ff:ff:ff:ff:ff", device="veth5ec9950", duplex="full", instance="192.168.100.105:9100", job="app_server", operstate="up"}	1
# node_network_info{address="7e:4e:0f:4a:ca:e2", adminstate="up", app="app_server", broadcast="ff:ff:ff:ff:ff:ff", device="vethc0cfc39", duplex="full", instance="192.168.100.105:9100", job="app_server", operstate="up"}	1
# node_network_info{address="a6:c3:b4:ab:17:b6", adminstate="up", app="app_server", broadcast="ff:ff:ff:ff:ff:ff", device="br-3c4ecf18ecdc", duplex="unknown", instance="192.168.100.105:9100", job="app_server", operstate="up"}	1
```

- Range Vector

```promql
node_network_info[5s]
# node_network_info{address="00:00:00:00:00:00", adminstate="up", app="app_server", broadcast="00:00:00:00:00:00", device="lo", instance="192.168.100.105:9100", job="app_server", operstate="unknown"}
# 1 @ 1753822910.579
# 1 @ 1753822925.547
# node_network_info{address="00:0c:29:f1:f4:7f", adminstate="up", app="app_server", broadcast="ff:ff:ff:ff:ff:ff", device="ens33", duplex="full", instance="192.168.100.105:9100", job="app_server", operstate="up"}
# 1 @ 1753822910.579
# 1 @ 1753822925.547
# node_network_info{address="26:3a:40:b1:42:0c", adminstate="up", app="app_server", broadcast="ff:ff:ff:ff:ff:ff", device="veth5ec9950", duplex="full", instance="192.168.100.105:9100", job="app_server", operstate="up"}
# 1 @ 1753822910.579
# 1 @ 1753822925.547
# node_network_info{address="7e:4e:0f:4a:ca:e2", adminstate="up", app="app_server", broadcast="ff:ff:ff:ff:ff:ff", device="vethc0cfc39", duplex="full", instance="192.168.100.105:9100", job="app_server", operstate="up"}
# 1 @ 1753822910.579
# 1 @ 1753822925.547
# node_network_info{address="a6:c3:b4:ab:17:b6", adminstate="up", app="app_server", broadcast="ff:ff:ff:ff:ff:ff", device="br-3c4ecf18ecdc", duplex="unknown", instance="192.168.100.105:9100", job="app_server", operstate="up"}
# 1 @ 1753822910.579
# 1 @ 1753822925.547
# node_network_info{address="c2:77:27:7b:04:a4", adminstate="up", app="app_server", broadcast="ff:ff:ff:ff:ff:ff", device="docker0", duplex="unknown", instance="192.168.100.105:9100", job="app_server", operstate="down"}
# 1 @ 1753822910.579
# 1 @ 1753822925.547
```

---

## Operator

| Operator | Desc           |
| -------- | -------------- |
| `+`      | Addition       |
| `-`      | Subtraction    |
| `*`      | Multiplication |
| `/`      | Divison        |
| `%`      | Modulo         |
| `^`      | Power          |

- Scalar + instant Vector

  - Applies to every value of instant vector

- Instant Vector + Instant Vector

  - Applies to every value of left vector and it matching value in the right vector

- Example

| A     |     | B     |     | A+5   |     | A+B   |              |
| ----- | --- | ----- | --- | ----- | --- | ----- | ------------ |
| M1{a} | 3   | M1{a} | 37  | M1{a} | 8   | M1{a} | 40           |
| M1{b} | 4   | M1{b} | 6   | M1{b} | 9   | M1{b} | 10           |
| M1{c} | 9   |       |     | M1{c} | 14  |       | Empty result |

```promQL
# Scalar + instant Vector

# single isntant vector
node_selinux_enabled
# node_selinux_enabled{app="app_server", instance="192.168.100.105:9100", job="app_server"}	0

node_selinux_enabled + 10
# {app="app_server", instance="192.168.100.105:9100", job="app_server"}	10

# multiple isntant vectors
prometheus_sd_updates_total
# prometheus_sd_updates_total{app="prometheus", instance="localhost:9090", job="prometheus", name="notify"}	1
# prometheus_sd_updates_total{app="prometheus", instance="localhost:9090", job="prometheus", name="scrape"}	1

prometheus_sd_updates_total + 10
# {app="prometheus", instance="localhost:9090", job="prometheus", name="notify"}	11
# {app="prometheus", instance="localhost:9090", job="prometheus", name="scrape"}	11

# Instant Vector + Instant Vector
node_selinux_enabled - node_arp_entries
# Empty query result

node_arp_entries - node_arp_entries
# {app="app_server", device="br-3c4ecf18ecdc", instance="192.168.100.105:9100", job="app_server"}	0
# {app="app_server", device="ens33", instance="192.168.100.105:9100", job="app_server"}	0
```

---

### Comparison Binary Operators

| Operator | Desc               |
| -------- | ------------------ |
| `==`     | Equal              |
| `!=`     | Non-equal          |
| `>`      | Greater            |
| `>=`     | Greater or Equal   |
| `<`      | Less-than          |
| `<=`     | Less-than or Equal |

- Result:
  - `1`: true
  - `0`: false

```promql
node_network_up
# node_network_up{app="app_server", device="br-3c4ecf18ecdc", instance="192.168.100.105:9100", job="app_server"}	1
# node_network_up{app="app_server", device="docker0", instance="192.168.100.105:9100", job="app_server"}	0
# node_network_up{app="app_server", device="ens33", instance="192.168.100.105:9100", job="app_server"}	1
# node_network_up{app="app_server", device="lo", instance="192.168.100.105:9100", job="app_server"}	0
# node_network_up{app="app_server", device="vethc0cfc39", instance="192.168.100.105:9100", job="app_server"}	1
# node_network_up{app="app_server", device="veth5ec9950", instance="192.168.100.105:9100", job="app_server"}	1

node_network_up == 0
# node_network_up{app="app_server", device="docker0", instance="192.168.100.105:9100", job="app_server"}	0
# node_network_up{app="app_server", device="lo", instance="192.168.100.105:9100", job="app_server"}	0

```

---

### Set operator

- Applied on `Instant Vectors` only

| Set operator | Desc                                       |
| ------------ | ------------------------------------------ |
| `and`        | Common instant vector                      |
| `or`         | All isntant vectors                        |
| `D`          | the instant vectors exist only on the letf |

---

### Fileter Matchers/Selectors

- `=`: two value must be equal
- `!=`: two value must not be equal
- `=~`: value on left must match the regex on right
- `!~`: value on left must NOT match the regex on right

```promql
metric_name{filter_key=value, ...}

# example
prometheus_http_requests_total{code=200,job="prometheus"}
prometheus_http_requests_total{code=~"2.*",job="prometheus"}

prometheus_http_response_size_bytes_bucket
# Result series: 207

prometheus_http_response_size_bytes_bucket{handler =~ "/api/.*"}
# Result series: 135

prometheus_http_response_size_bytes_bucket{handler = "/api/v1/query"}
# Result series: 9
```

---

### Aggregation Operator

- Aggregate the elements of a single Instant Vector
- The result is a new Instant Vector with aggregated values.

| Aggregation    | Desc                                                                          |
| -------------- | ----------------------------------------------------------------------------- |
| `sum`          | Sum over dimensions                                                           |
| `min`          | Select minimum over dimensions                                                |
| `max`          | Select maximum over dimensions                                                |
| `avg`          | Select average over dimensions                                                |
| `count`        | Select number of elements over dimensions                                     |
| `group`        | Group elements over dimensions. All values in resulting vector are equal to 1 |
| `count_values` | Counts the number of elements with the same values                            |
| `topk`         | Top N Largest elements                                                        |
| `bottomk`      | Bottom N smallest elements                                                    |
| `stddev`       | standard deviation over dimensions                                            |
| `stdvar`       | standard variation over dimensions                                            |

- Syntax:

```promql
aggregation_operator(instant_vector)
sum(node_cpu_total)

# filter includes labels
aggregation_operator(instant_vector) by (label_list)
sum(node_cpu_total) by (http_code)

# filter excludes labels
aggregation_operator(instant_vector) without (label_list)
sum(node_cpu_total) without (http_code)
```

- Example

```promsql
node_cpu_seconds_total
# Result series: 32

sum(node_cpu_seconds_total)
# {}	37763.36

sum(node_cpu_seconds_total) by (cpu)
# {cpu="0"}	9555.39
# {cpu="1"}	9564.59
# {cpu="2"}	9560.93
# {cpu="3"}	9565.119999999999

sum(node_cpu_seconds_total) without (cpu)
# {app="app_server", instance="192.168.100.105:9100", job="app_server", mode="idle"}	37999.770000000004
# {app="app_server", instance="192.168.100.105:9100", job="app_server", mode="iowait"}	6.63
# {app="app_server", instance="192.168.100.105:9100", job="app_server", mode="irq"}	0
# {app="app_server", instance="192.168.100.105:9100", job="app_server", mode="nice"}	0.06999999999999999
# {app="app_server", instance="192.168.100.105:9100", job="app_server", mode="softirq"}	11.83
# {app="app_server", instance="192.168.100.105:9100", job="app_server", mode="steal"}	0
# {app="app_server", instance="192.168.100.105:9100", job="app_server", mode="system"}	254.62
# {app="app_server", instance="192.168.100.105:9100", job="app_server", mode="user"}	213.73000000000002

topk(2,sum(node_cpu_seconds_total) without (cpu))
# {app="app_server", instance="192.168.100.105:9100", job="app_server", mode="idle"}	38238.67
# {app="app_server", instance="192.168.100.105:9100", job="app_server", mode="system"}	255.96

bottomk(2,sum(node_cpu_seconds_total) without (cpu))
# {app="app_server", instance="192.168.100.105:9100", job="app_server", mode="steal"}	0
# {app="app_server", instance="192.168.100.105:9100", job="app_server", mode="irq"}	0

group(node_cpu_seconds_total) by (cpu)
# {cpu="0"}	1
# {cpu="1"}	1
# {cpu="2"}	1
# {cpu="3"}	1

avg(node_cpu_seconds_total) by (mode)
# {mode="idle"}	9738.37
# {mode="iowait"}	1.6625
# {mode="irq"}	0
# {mode="nice"}	0.017499999999999998
# {mode="softirq"}	3.005
# {mode="steal"}	0
# {mode="system"}	64.9875
# {mode="user"}	54.195
```

---

### Time Offsets

- By default, promQL return the latest time series.
- Instead of returning the latest, using `offset`
- Always after the metric, especially with aggregation.

```promql
# last scrape
prometheus_http_requests_total{handler="/api/v1/notifications/live"}
# 94

prometheus_http_requests_total{handler="/api/v1/notifications/live"} offset 10d
# Empty query result
# because instance has just stated and do not have time series in 10 days.

# last 10 minutes
prometheus_http_requests_total{handler="/api/v1/notifications/live"} offset 10m
# 81

# with aggregation
avg(prometheus_http_requests_total offset 3m) by (code)
```

---

## Functions

| Function                          | Description                                                                          |
| --------------------------------- | ------------------------------------------------------------------------------------ |
| `absent(instant_vector)`          | Check if an instant vector has any members. If has elements, returns an empty vector |
| `absent_over_time(range_vector)`  | Check if a range vector has any members.If has elements, returns an empty vector     |
| `abs(instant_vector)`             | Convert all values to absolute value                                                 |
| `ceil(instant_vector)`            | Convert all values to nearest larger integer                                         |
| `floor(instant_vector)`           | Convert all values to nearest smaller integer                                        |
| `clamp(instant_vector, min, max)` | clamps element with a lower limit of min and an upper limit of max                   |
| `clamp_min(instant_vector, min)`  | clamps the values of all float samples in v to have a lower limit of min             |
| `clamp_max(instant_vector, max)`  | clamps the values of all float samples in v to have an upper limit of max            |
| `day_of_month(instant_vector)`    | Returns the day of the month (in UTC) for each of those timestamps.                  |
| `day_of_week(instant_vector)`     | Returns the day of the week (in UTC) for each of those timestamps.                   |
| `delta(instant_vector)`           | Can only be used with Gauges                                                         |
| `idelta(range_vector)`            | Returns the difference between first and last items                                  |
| `log2(instant_vector)`            | Returns binary logarithm of each scalar value                                        |
| `log10(instant_vector)`           | Returns decimal logarithm of each scalar value                                       |
| `ln(instant_vector)`              | Returns neutral logarithm of each scalar value                                       |
| `sort(instant_vector)`            | Sorts elements in ascending order                                                    |
| `sort_desc(instant_vector)`       | Sorts elements in descending order                                                   |
| `time()`                          | Returns a near-current time stamp                                                    |
| `timestamp(instant_vector)`       | Returns the time stamp of each time series element                                   |
| `avg_over_time(range_vector)`     | Returns the average of items in a range vector                                       |
| `sum_over_time(range_vector)`     | Returns the sum of items in a range vector                                           |
| `min_over_time(range_vector)`     | Returns the min of items in a range vector                                           |
| `max_over_time(range_vector)`     | Returns the max of items in a range vector                                           |
| `count_over_time(range_vector)`   | Returns the count of items in a range vector                                         |

```promql
node_cpu_seconds_total
# Result series: 32

absent(node_cpu_seconds_total)
# Empty query result

node_cpu_seconds_total{cpu="fdsfsd"}
# Empty query result

absent(node_cpu_seconds_total{cpu="fdsfsd"})
# {cpu="fdsfsd"}	1

node_cpu_seconds_total[20s]
# Result series: 32

absent_over_time(node_cpu_seconds_total[20s])
# Empty query result

absent_over_time(node_cpu_seconds_total{cpu="fdsfsd"}[20s])
# {cpu="fdsfsd"}	1

node_cpu_seconds_total{cpu="0"}
# node_cpu_seconds_total{app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="idle"}	11444.8
# node_cpu_seconds_total{app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="iowait"}	2.74
# node_cpu_seconds_total{app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="irq"}	0
# node_cpu_seconds_total{app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="nice"}	0
# node_cpu_seconds_total{app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="softirq"}	3.83
# node_cpu_seconds_total{app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="steal"}	0
# node_cpu_seconds_total{app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="system"}	81.72
# node_cpu_seconds_total{app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="user"}	62.22

clamp(node_cpu_seconds_total{cpu="0"}, 50, 100)
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="idle"}	100
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="iowait"}	50
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="irq"}	50
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="nice"}	50
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="softirq"}	50
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="steal"}	50
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="system"}	82.2
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="user"}	62.47

clamp_min(node_cpu_seconds_total{cpu="0"}, 100)
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="idle"}	11565.41
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="iowait"}	100
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="irq"}	100
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="nice"}	100
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="softirq"}	100
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="steal"}	100
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="system"}	100
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="user"}	100

clamp_max(node_cpu_seconds_total{cpu="0"}, 70)
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="idle"}	70
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="iowait"}	2.74
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="irq"}	0
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="nice"}	0
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="softirq"}	3.88
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="steal"}	0
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="system"}	70
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="user"}	62.69

sort(clamp(node_cpu_seconds_total{cpu="0"}, 50, 100))
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="iowait"}	50
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="irq"}	50
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="nice"}	50
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="softirq"}	50
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="steal"}	50
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="user"}	64.49
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="system"}	87.08
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="idle"}	100

sort_desc(clamp(node_cpu_seconds_total{cpu="0"}, 50, 100))
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="idle"}	100
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="system"}	87.34
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="user"}	64.58
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="iowait"}	50
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="irq"}	50
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="nice"}	50
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="softirq"}	50
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="steal"}	50

timestamp(clamp(node_cpu_seconds_total{cpu="0"}, 50, 100))
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="idle"}	1753833001.613
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="iowait"}	1753833001.613
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="irq"}	1753833001.613
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="nice"}	1753833001.613
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="softirq"}	1753833001.613
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="steal"}	1753833001.613
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="system"}	1753833001.613
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="user"}	1753833001.613


avg_over_time(node_cpu_seconds_total[2h])
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="idle"}	10664.17512195122
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="iowait"}	2.5307723577235772
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="irq"}	0
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="nice"}	0
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="softirq"}	3.5448780487804874
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="steal"}	0
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="system"}	75.20353658536585
# {app="app_server", cpu="0", instance="192.168.100.105:9100", job="app_server", mode="user"}	56.99808943089431
# ...
```
