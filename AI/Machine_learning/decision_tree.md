# Machine Learning - Decision Tree

[Back](./index.md)

- [Machine Learning - Decision Tree](#machine-learning---decision-tree)
  - [Example: Decision Tree](#example-decision-tree)
    - [1. Load Data](#1-load-data)
    - [2. Clean Data](#2-clean-data)
    - [3. Split feature columns and the target column](#3-split-feature-columns-and-the-target-column)
    - [4. Create Decision Tree Model and Fit Data](#4-create-decision-tree-model-and-fit-data)
    - [5. Predict Values](#5-predict-values)

---

## Example: Decision Tree

Predict whether a customer go to a comedy show, based on series of data.

- **Different Results**

  - The Decision Tree yields different results, even if model is fed with the same data.
  - That is because the Decision Tree does not give a 100% certain answer. It is based on the probability of an outcome, and the answer will vary.

---

### 1. Load Data

- `panda.read_csv()`

```py
import pandas as pd

FILE_PATH = "./data_decision_tree.csv"
file_data = pd.read_csv(FILE_PATH)

# file_data.shape
# file_data.columns
# file_data.info()
# print(file_data)

file_data.head()

```

---

### 2. Clean Data

- Missing data

- To make a decision tree, all data has to be numerical.
  - to convert the non numerical data into numerical values.
  - `pandas.map()`

```py
# Convert nationality into numerical values
map_nationality = {'UK': 0, 'USA': 1, 'N': 2}
file_data['Nationality'] = file_data['Nationality'].map(map_nationality)

# Convert go into numerical values
map_go = {'YES': 1, 'NO': 0}
file_data['Go'] = file_data['Go'].map(map_go)

print(file_data)
```

---

### 3. Split feature columns and the target column

- `feature column`: the columns with the values that target values are predicted from.

- `target column`: the column with the values that are to be predicted.

```py
features = ['Age', 'Experience', 'Rank', 'Nationality']

feature_list = file_data[features]
target_list = file_data['Go']

# print(feature_list)
# print(target_list)
```

---

### 4. Create Decision Tree Model and Fit Data

- `sklearn.tree.DecisionTreeClassifier()`: create a decision tree model object

```py
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree

import matplotlib.pyplot as plt

predict_model = DecisionTreeClassifier()
predict_model = predict_model.fit(feature_list.values, target_list.values)

# sklearn.tree.plot_tree(): Plot a decision tree.
#   decision_tree: The decision tree to be plotted.
#   feature_names: Names of each of the features.
tree.plot_tree(predict_model, feature_names=features)

plt.show()
```

![decision tree](./pic/decision_tree.png)

- Rank <= 6.5 means that every comedian with a rank of 6.5 or lower will follow the True arrow (to the left), and the rest will follow the False arrow (to the right).

- gini = 0.497 refers to the quality of the split, and is always a number between 0.0 and 0.5, where 0.0 would mean all of the samples got the same result, and 0.5 would mean that the split is done exactly in the middle.

- samples = 13 means that there are 13 comedians left at this point in the decision, which is all of them since this is the first step.

- value = [6, 7] means that of these 13 comedians, 6 will get a "NO", and 7 will get a "GO".

---

### 5. Predict Values

- Predict whether a customer will to to a comedy ranking of 7, performed by a 40 years old American comedian with 10 years of experience.

```py
predict_value = predict_model.predict([[40, 10, 7, 1]])

# print(predict_value)
print("Yes" if predict_value[0] else "No")      # No
```

---

[TOP](#machine-learning---decision-tree)
