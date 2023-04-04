# Preprocessing - Categorical Data

[Back](./index.md)

- [Preprocessing - Categorical Data](#preprocessing---categorical-data)
  - [Categorical Data](#categorical-data)
    - [One Hot Encoding](#one-hot-encoding)
    - [Dummifying](#dummifying)

---

## Categorical Data

- When data has categories represented by strings, it will be difficult to use them to train machine learning models which often **only accepts numeric data**.

- Instead of ignoring the categorical data and excluding the information from our model, they can be tranformed

```py
import pandas as pd

cars = pd.read_csv('data.csv')
cars.head()
# 	Car	Model	Volume	Weight	CO2
# 0	Toyoty	Aygo	1000	790	99
# 1	Mitsubishi	Space Star	1200	1160	95
# 2	Skoda	Citigo	1000	929	95
# 3	Fiat	500	900	865	90
# 4	Mini	Cooper	1500	1140	105
```

- 上例中 car 和 model 不是数字,不能参与线性回归.

---

### One Hot Encoding

- cannot make use of the Car or Model column in our data since they are not numeric.
- A linear relationship between a categorical variable, Car or Model, and a numeric variable, CO2, cannot be determined.

- To fix this issue, we must have a numeric representation of the categorical variable.

  - one way to this is one hot encoding

- `one hot encoding`: to have a column representing each group in the category.

  - For each column, the values will be 1 or 0 where 1 represents the inclusion of the group and 0 represents the exclusion.

- `pandas.get_dummies()`: Convert categorical variable into dummy/indicator variables.

- use this additional information alongside the volume and weight to predict CO2
  - `pandas.concat()`: Concatenate pandas objects along a particular axis.

```py

ohe_cars = pd.get_dummies(cars[['Car']])
# print(ohe_cars.to_string())

X = pd.concat([cars[['Volume', 'Weight']], ohe_cars], axis=1)
# print(X.to_string())

y = cars['CO2']
# print(y.to_string())
```

- create model and fir data

```py
from sklearn import linear_model
regr = linear_model.LinearRegression()
regr.fit(X, y)

# predict the CO2 emission of a Volvo where the weight is 2300kg, and the volume is 1300cm3:
predictedCO2 = regr.predict(
    [[2300, 1300, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]])
print(predictedCO2)     # [122.45153299]
```

---

### Dummifying

- Instead of One Hot Encoding, to create one column for each group in your category, the data can be transformed using 1 column less than the number of groups.

  - 即在上一个方法中,是将一列中的类别拆分为若干 N 个列,再进行线性回归.
  - 本方法是将类别拆分为 N-1 个列, 使用这些列的组合指代具体的类别,再进行线性回归.

- `pandas.get_dummies(drop_first)`

  - drop_first: bool, default False
    - Whether to get `k-1` dummies out of `k` categorical levels by removing the first level.

- Example: a column representing colors

  - 2 Colors

  ```py
  import pandas as pd

  colors = pd.DataFrame({'color': ['blue', 'red']})
  print("colors", colors)

  dummies = pd.get_dummies(colors, drop_first=True)
  print("dummies", dummies)
  # the first column for blue is dropped.
  # to represent color blue, it takes color_red as 0 or false.
  ```

  - 3 colors

  ```py
  # If there are 3 colors

  import pandas as pd

  colors = pd.DataFrame({'color': ['blue', 'red', 'green']})
  print("colors\n", colors)

  dummies = pd.get_dummies(colors, drop_first=True)
  print("dummies\n", dummies)

  # dummies['color'] = colors['color']                # add orignal color column
  # new data set, adding colors and dummies
  new_colors = pd.concat([colors, dummies], axis=1)

  print(new_colors)
  ```

---

[TOP](#preprocessing---categorical-data)
