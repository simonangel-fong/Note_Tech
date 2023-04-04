# Machine Learning - Grid Search

[Back](./index.md)

- [Machine Learning - Grid Search](#machine-learning---grid-search)
  - [Grid Search](#grid-search)
  - [Example: Find the best C](#example-find-the-best-c)
    - [Using Default Parameters](#using-default-parameters)
    - [Implementing Grid Search](#implementing-grid-search)
    - [Results Explained](#results-explained)
  - [Note on Best Practices](#note-on-best-practices)

---

## Grid Search

- The majority of machine learning models contain parameters that can be adjusted to vary how the model learns.

  - For example, the logistic regression model, from sklearn, has a `parameter C` that controls regularization, which affects the complexity of the model. 控制模型的复杂程度
  - How do we pick the best value for C? The best value is dependent on the data used to train the model.

- `grid search`: try out different values and then pick the value that gives the **best score**.

  - If we had to select the values for two or more parameters, we would evaluate **all combinations** of the sets of values thus forming a grid of values.

- **Higher values of C** tell the model, the training data resembles real world information, place a **greater weight** on the training data. While lower values of C do the opposite.

---

## Example: Find the best C

### Using Default Parameters

1. Load in the dataset

- `sklearn.datasets.load_iris()`: Load and return the iris dataset (classification).

- The `iris dataset` is a classic and very easy multi-class classification dataset.

  - These measures were used to create a linear discriminant model 线性判别分析 to classify the species.

    | Feature           |                |
    | ----------------- | -------------- |
    | Classes           | 3              |
    | Samples per class | 50             |
    | Samples total     | 150            |
    | Dimensionality    | 4              |
    | Features          | real, positive |

```py
from sklearn import datasets
iris = datasets.load_iris()

X = iris['data']
y = iris['target']

print("X",X)
print("y",y)
```

---

- 2. Create Prediction Model

  - Using logistic model for classifying the iris flowers.

    - setting `max_iter` to a higher value to ensure that the model finds a result.

  - `max_iterint`: default=100
    - Maximum number of iterations taken for the solvers to converge.

```py
from sklearn.linear_model import LogisticRegression

predict_model = LogisticRegression(max_iter=10000)
predict_model.fit(X, y)
```

- 3. Evaluate the model

  - `sklearn.linear_model.LogisticRegression().score()`: Return the mean accuracy on the given test data and labels.

    - return: float

  - With the default setting of C = 1, we achieved a score of 0.973.

```py
score = predict_model.score(X, y)

print("score", score)
#  score 0.9733333333333334
```

---

### Implementing Grid Search

Since the default value for C is 1, we will set a range of values surrounding it.

1. create a range of value arround 1, which is the default value.
2. loop over the range of values and append to a score list.

```py

C = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2]

scores = []
for choice in C:
    # set_params(): Set the parameters of this estimator.
    predict_model.set_params(C=choice)
    # fit data after setting parameters
    predict_model.fit(X, y)
    scores.append(predict_model.score(X, y))

print(scores)
# [0.9666666666666667, 0.9666666666666667, 0.9733333333333334, 0.9733333333333334, 0.98, 0.98, 0.9866666666666667, 0.9866666666666667]
```

### Results Explained

- The lower values of C performed worse than the base parameter of 1. However, as we increased the value of C to 1.75 the model experienced increased accuracy.

It seems that increasing C beyond this amount **does not help** increase model accuracy.

---

## Note on Best Practices

- We scored our logistic regression model by using the same data that was used to train it. If the model corresponds too closely to that data, it may not be great at predicting unseen data. This statistical error is known as `over fitting`.

To avoid being misled by the scores on the training data, we can put aside a portion of our data and use it specifically for the purpose of testing the model.

---

[TOP](#grid-search)
