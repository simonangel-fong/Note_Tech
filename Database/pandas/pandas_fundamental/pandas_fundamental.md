# Pandas - Fundamental

[Back](../index.md)

- [Pandas - Fundamental](#pandas---fundamental)
  - [Pandas Series](#pandas-series)
    - [Labels](#labels)
    - [Key/Value Objects as Series](#keyvalue-objects-as-series)
  - [DataFrames](#dataframes)
    - [Locate Row](#locate-row)
    - [Named Indexes](#named-indexes)
  - [Load Files Into a DataFrame](#load-files-into-a-dataframe)
    - [Read CSV](#read-csv)
    - [Read json](#read-json)
  - [Meta Data](#meta-data)
  - [Preview](#preview)

---

## Pandas Series

- A `Pandas Series` is like a **column** in a table.

  - It is a **one-dimensional array** holding data of any type.

```py
# Pandas Series

import pandas as pd

arr = []
df = pd.Series(arr)
print(df)
# Series([], dtype: object)

arr = [[]]
df = pd.Series(arr)
print(df)
# 0    []
# dtype: object

arr = [1, 7, 2]
df = pd.Series(arr)
print(df)
# # 0    1
# # 1    7
# # 2    2
# # dtype: int64

arr = [[1, 7, 2], [3,4,6]]
df = pd.Series(arr)
print(df)
# 0    [1, 7, 2]
# 1    [3, 4, 6]
# dtype: object
```

---

### Labels

- If nothing else is specified, the values are labeled with their **index number**.

  - First value has index 0, second value has index 1 etc.

- This label can be used to access a specified value.

```py
# Labels

import pandas as pd

arr = []
df = pd.Series(arr)
print(df[0])
# ValueError: 0 is not in range

arr = [[]]
df = pd.Series(arr)
print(df[0])
# []

arr = [1, 7, 2]
df = pd.Series(arr)
print(df[0])
# 1

arr = [[1, 7, 2], [3, 4]]
df = pd.Series(arr)
print(df[0])
# [1, 7, 2]
```

---

- **Create Labels**
  - With the `index` argument, you can name your own labels.

```py
# Create lable

import pandas as pd

arr = []
df = pd.Series(arr, index=["x"])
print(df)
# ValueError: Length of values (0) does not match length of index (3)

arr = [[]]
df = pd.Series(arr, index=["x"])
print(df)
# x    []
# dtype: object

print(df['x'])
# []
print(df.x)
# []

arr = [1, 7, 2]
df = pd.Series(arr, index=["x", "y", "z"])
print(df)
# x    1
# y    7
# z    2
# dtype: int64
print(df[0])
# 1
print(df["x"])
# 1
print(df.x)
# 1


arr = [[1, 7, 2], [], [3, 5]]
df = pd.Series(arr, index=["x", "y", "z"])
print(df)
# x    [1, 7, 2]
# y           []
# z       [3, 5]
# dtype: object

print(df.y)
# []
print(df['z'])
# [3,5]
```

---

### Key/Value Objects as Series

```py
# Key/Value Objects as Series

import pandas as pd

x_dict = {"day1": 420, "day2": 380, "day3": 390}
df = pd.Series(x_dict)
print(df)
# day1    420
# day2    380
# day3    390
# dtype: int64

x_dict = {"day1": 420, "day2": 380, "day3": 390}
# Create a Series using only data from "day1" and "day2":
df = pd.Series(x_dict, index = ["day1", "day2"])
print(df)
# day1    420
# day2    380
# dtype: int64
```

---

## DataFrames

- `DataFrame`:
  - Data sets in Pandas are usually **multi-dimensional tables**.
  - `Series` is like a **column**, a `DataFrame` is the whole table.

```py
# DataFrame
import pandas as pd

data = {
    "calories": [420, 380, 390],
    "duration": [50, 40, 45]
}
df = pd.DataFrame(data)

print(df)
#    calories  duration
# 0       420        50
# 1       380        40
# 2       390        45
```

---

### Locate Row

- `loc` attribute:
  - return one or more specified **row**(s)

```py
print(df.loc[0])
# calories    420
# duration     50
# Name: 0, dtype: int64

print(df.loc[[0, 1]])
#    calories  duration
# 0       420        50
# 1       380        40
```

---

### Named Indexes

- `index` argument: to name indexes

```py
# index

import pandas as pd

data = {
    "calories": [420, 380, 390],
    "duration": [50, 40, 45]
}
df = pd.DataFrame(data, index=["day1", "day2", "day3"])

# print(df)
#       calories  duration
# day1       420        50
# day2       380        40
# day3       390        45

# Locate Named Indexes
print(df.loc["day2"])
# calories    380
# duration     40
# Name: day2, dtype: int64
```

---

## Load Files Into a DataFrame

### Read CSV

```py
# Load Files Into a DataFrame

import pandas as pd

df = pd.read_csv('data.csv')
print(df)
#    Duration   Pulse   Maxpulse   Calories
# 0        60     110        130      409.1
# 1        60     117        145      479.0
# 2        60     103        135      340.0
```

---

### Read json

```py
# read json data
import pandas as pd

df = pd.read_json('data.json')

print(df.head(5))

#    Duration  Pulse  Maxpulse  Calories
# 0        60    110       130     409.1
# 1        60    117       145     479.0
# 2        60    103       135     340.0
# 3        45    109       175     282.4
# 4        45    117       148     406.0
```

---

## Meta Data

```py
# Meta

import pandas as pd

df = pd.read_csv('data.csv')
print(df.info())
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 169 entries, 0 to 168
# Data columns (total 4 columns):
#  #   Column    Non-Null Count  Dtype  
# ---  ------    --------------  -----  
#  0   Duration  169 non-null    int64  
#  1   Pulse     169 non-null    int64  
#  2   Maxpulse  169 non-null    int64  
#  3   Calories  164 non-null    float64
# dtypes: float64(1), int64(3)
# memory usage: 5.4 KB
# None

print(df.columns)
# Index(['Duration', 'Pulse', 'Maxpulse', 'Calories'], dtype='object')

df.dtypes
# Duration      int64
# Pulse         int64
# Maxpulse      int64
# Calories    float64
# dtype: object
```

---

## Preview

```py
import pandas as pd

df = pd.read_csv('data.csv')
print(df.head(3))
#    Duration  Pulse  Maxpulse  Calories
# 0        60    110       130     409.1
# 1        60    117       145     479.0
# 2        60    103       135     340.0

print(df.tail(3))
    #  Duration  Pulse  Maxpulse  Calories
# 166        60    115       145     310.2
# 167        75    120       150     320.4
# 168        75    125       150     330.4
```


---

[TOP](#pandas---fundamental)
