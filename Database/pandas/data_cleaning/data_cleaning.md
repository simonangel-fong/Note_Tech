# Pandas - Cleaning

[Back](../index.md)

- [Pandas - Cleaning](#pandas---cleaning)
  - [Data Cleaning](#data-cleaning)
    - [Cleaning Empty Cells(`dropna()`)](#cleaning-empty-cellsdropna)
    - [Replace Empty Values(`fillna()`)](#replace-empty-valuesfillna)
    - [Replace Only For Specified Columns](#replace-only-for-specified-columns)
    - [Replace Using Mean, Median, or Mode(`fillna()`)](#replace-using-mean-median-or-modefillna)
      - [`mean()`](#mean)
      - [`median()`](#median)
      - [`mode()`](#mode)
  - [Data of Wrong Format](#data-of-wrong-format)
    - [Convert Into a Correct Format](#convert-into-a-correct-format)
    - [Removing Rows](#removing-rows)
  - [Wrong Data](#wrong-data)
  - [Removing Duplicates](#removing-duplicates)
    - [Removing Duplicates(`drop_duplicates()`)](#removing-duplicatesdrop_duplicates)

---

## Data Cleaning

- `Data cleaning` means fixing bad data in your data set.

- Bad data could be:

  - Empty cells
  - Data in wrong format
  - Wrong data
  - Duplicates

- Load data

```py
import pandas as pd

df = pd.read_csv("data_cleaning.csv")

df.info()
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 32 entries, 0 to 31
# Data columns (total 5 columns):
#  #   Column    Non-Null Count  Dtype
# ---  ------    --------------  -----
#  0   Duration  32 non-null     int64
#  1   Date      31 non-null     object
#  2   Pulse     32 non-null     int64
#  3   Maxpulse  32 non-null     int64
#  4   Calories  30 non-null     float64
# dtypes: float64(1), int64(3), object(1)
# memory usage: 1.4+ KB
```

---

### Cleaning Empty Cells(`dropna()`)

- Empty Cells

  - can potentially give you a wrong result when you analyze data.

- One way to deal with empty cells is to remove rows that contain empty cells.
  - This is usually OK, since data sets can be very big, and removing a few rows will not have a big impact on the result.

---

- `dropna()`
  - By default, returns a **new** DataFrame, and will **not change** the original.
  - If you want to **change the original** DataFrame, use the `inplace = True` argument:

```py
new_df = df.dropna()
new_df.info()
# <class 'pandas.core.frame.DataFrame'>
# Index: 29 entries, 0 to 31
# Data columns (total 5 columns):
#  #   Column    Non-Null Count  Dtype
# ---  ------    --------------  -----
#  0   Duration  29 non-null     int64
#  1   Date      29 non-null     object
#  2   Pulse     29 non-null     int64
#  3   Maxpulse  29 non-null     int64
#  4   Calories  29 non-null     float64
# dtypes: float64(1), int64(3), object(1)
# memory usage: 1.4+ KB

# change the original data
df.dropna(inplace=True)
df.info()
# <class 'pandas.core.frame.DataFrame'>
# Index: 29 entries, 0 to 31
# Data columns (total 5 columns):
#  #   Column    Non-Null Count  Dtype
# ---  ------    --------------  -----
#  0   Duration  29 non-null     int64
#  1   Date      29 non-null     object
#  2   Pulse     29 non-null     int64
#  3   Maxpulse  29 non-null     int64
#  4   Calories  29 non-null     float64
# dtypes: float64(1), int64(3), object(1)
# memory usage: 1.4+ KB
```

---

### Replace Empty Values(`fillna()`)

- Another way of dealing with empty cells is to insert a new value instead.
  - This way you do not have to delete entire rows just because of some empty cells.
- `fillna()`
  - allows us to replace empty cells with a value

```py
import pandas as pd
df = pd.read_csv('data_cleaning.csv')
df.info()
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 32 entries, 0 to 31
# Data columns (total 5 columns):
#  #   Column    Non-Null Count  Dtype
# ---  ------    --------------  -----
#  0   Duration  32 non-null     int64
#  1   Date      31 non-null     object
#  2   Pulse     32 non-null     int64
#  3   Maxpulse  32 non-null     int64
#  4   Calories  30 non-null     float64
# dtypes: float64(1), int64(3), object(1)
# memory usage: 1.4+ KB

df.fillna(130, inplace = True)
df.info()
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 32 entries, 0 to 31
# Data columns (total 5 columns):
#  #   Column    Non-Null Count  Dtype
# ---  ------    --------------  -----
#  0   Duration  32 non-null     int64
#  1   Date      32 non-null     object
#  2   Pulse     32 non-null     int64
#  3   Maxpulse  32 non-null     int64
#  4   Calories  32 non-null     float64
# dtypes: float64(1), int64(3), object(1)
# memory usage: 1.4+ KB
```

---

### Replace Only For Specified Columns

- To only replace empty values for one column, specify the column name for the DataFrame

```py
import pandas as pd

df = pd.read_csv('data_cleaning.csv')
df.info()
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 32 entries, 0 to 31
# Data columns (total 5 columns):
#  #   Column    Non-Null Count  Dtype
# ---  ------    --------------  -----
#  0   Duration  32 non-null     int64
#  1   Date      31 non-null     object
#  2   Pulse     32 non-null     int64
#  3   Maxpulse  32 non-null     int64
#  4   Calories  30 non-null     float64
# dtypes: float64(1), int64(3), object(1)
# memory usage: 1.4+ KB

df["Calories"].fillna(130, inplace=True)
df.info()
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 32 entries, 0 to 31
# Data columns (total 5 columns):
#  #   Column    Non-Null Count  Dtype
# ---  ------    --------------  -----
#  0   Duration  32 non-null     int64
#  1   Date      31 non-null     object
#  2   Pulse     32 non-null     int64
#  3   Maxpulse  32 non-null     int64
#  4   Calories  32 non-null     float64
# dtypes: float64(1), int64(3), object(1)
# memory usage: 1.4+ KB
```

---

### Replace Using Mean, Median, or Mode(`fillna()`)

- A common way to replace empty cells, is to calculate the mean, median or mode value of the column.

- Pandas uses the `mean()` `median()` and `mode()` methods to calculate the respective values for a specified column.

---

#### `mean()`

```py
import pandas as pd

df = pd.read_csv('data_cleaning.csv')
x = df["Calories"].mean()
df["Calories"].fillna(x, inplace = True)
```

---

#### `median()`

```py
import pandas as pd

df = pd.read_csv('data.csv')

x = df["Calories"].median()

df["Calories"].fillna(x, inplace = True)
```

---

#### `mode()`

```py
import pandas as pd

df = pd.read_csv('data.csv')

x = df["Calories"].mode()[0]

df["Calories"].fillna(x, inplace = True)
```

---

## Data of Wrong Format

- Cells with data of wrong format can make it difficult, or even impossible, to analyze data.
  - To fix it, you have two options:
    - remove the rows
    - convert all cells in the columns into the same format.

---

### Convert Into a Correct Format

```py
import pandas as pd

df = pd.read_csv('data.csv')

df['Date'] = pd.to_datetime(df['Date'])

print(df.to_string())
```

---

### Removing Rows

```py
import pandas as pd

df = pd.read_csv('data_cleaning.csv')
df.dropna(subset=['Date'], inplace = True)
df
```

---

## Wrong Data

- One way to fix wrong values is to **replace** them with something else.

```py
import pandas as pd
df = pd.read_csv('data_cleaning.csv')
df.loc[7,'Duration'] = 45

for x in df.index:
  if df.loc[x, "Duration"] > 120:
    df.loc[x, "Duration"] = 120

print(df.to_string())
```

- Another way of handling wrong data is to **remove** the rows that contains wrong data.

```py
for x in df.index:
  if df.loc[x, "Duration"] > 120:
    df.drop(x, inplace = True)
```

---

## Removing Duplicates

- `duplicated()`
  - returns a Boolean values for each row

```py
df = pd.read_csv('data_cleaning.csv')
print(df.duplicated())
```

### Removing Duplicates(`drop_duplicates()`)

- `drop_duplicates()`:
  - To remove duplicates

```py
import pandas as pd

df = pd.read_csv('data_cleaning.csv')
df.info()
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 32 entries, 0 to 31
# Data columns (total 5 columns):
#  #   Column    Non-Null Count  Dtype
# ---  ------    --------------  -----
#  0   Duration  32 non-null     int64
#  1   Date      31 non-null     object
#  2   Pulse     32 non-null     int64
#  3   Maxpulse  32 non-null     int64
#  4   Calories  30 non-null     float64
# dtypes: float64(1), int64(3), object(1)
# memory usage: 1.4+ KB

df.drop_duplicates(inplace = True)
df.info()
# <class 'pandas.core.frame.DataFrame'>
# Index: 31 entries, 0 to 31
# Data columns (total 5 columns):
#  #   Column    Non-Null Count  Dtype
# ---  ------    --------------  -----
#  0   Duration  31 non-null     int64
#  1   Date      30 non-null     object
#  2   Pulse     31 non-null     int64
#  3   Maxpulse  31 non-null     int64
#  4   Calories  29 non-null     float64
# dtypes: float64(1), int64(3), object(1)
# memory usage: 1.5+ KB
```

---

[TOP](#pandas---cleaning)
