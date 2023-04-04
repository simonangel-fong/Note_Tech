# Machine Learning - Logistic Regression

[Back](./index.md)

- [Machine Learning - Logistic Regression](#machine-learning---logistic-regression)
  - [Logistic Regression](#logistic-regression)
  - [Example: Predict Tumor](#example-predict-tumor)
    - [DataSet](#dataset)
    - [Create Logistic Regression Model](#create-logistic-regression-model)
    - [Predict](#predict)
    - [Coefficient](#coefficient)
    - [Probability](#probability)

---

## Logistic Regression

- `Logistic regression` aims to solve **classification problems**. It does this by predicting **categorical outcomes**, unlike linear regression that predicts a continuous outcome.

- Example:
  - In the simplest case there are two outcomes, which is called `binomial`, an example of which is predicting if a tumor is malignant(恶性的) or benign(良性的). This means it has **only two possible outcomes**.
  - Other cases have more than two outcomes to classify, in this case it is called `multinomial`多项的. A common example for multinomial logistic regression would be predicting the class of an iris flower between 3 different species.

## Example: Predict Tumor

### DataSet

- `numpy.reshape()`: Gives a new shape to an array without changing its data.
  - parameter:
    - newshape: `int`, The new shape should be compatible with the original shape.

```py
import numpy

# X_LIST: represents the size of a tumor in centimeters.
# reshape(): convert 1-D array into 2-D array
# -1,1: 每行1列, 行数由numpy计算
# Note: X has to be reshaped into a column from a row for the LogisticRegression() function to work.
X_LIST = numpy.array([3.78, 2.44, 2.09, 0.14, 1.72, 1.65, 4.92, 4.37, 4.96, 4.52, 3.69, 5.88]).reshape(-1,1)
print("X_LIST", X_LIST)
# X_LIST [[3.78]
#  [2.44]
#  [2.09]
#  [0.14]
#  [1.72]
#  [1.65]
#  [4.92]
#  [4.37]
#  [4.96]
#  [4.52]
#  [3.69]
#  [5.88]]

# Y_LIST: represents whether or not the tumor is cancerous (0 for "No", 1 for "Yes").
Y_LIST = numpy.array([0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1])

print("Y_LIST", Y_LIST)
# Y_LIST [0 0 0 0 0 0 1 1 1 1 1 1]
```

---

### Create Logistic Regression Model

- `sklearn.linear_model.LogisticRegression()`: create a logistic regression object.

- `sklearn.linear_model.LogisticRegression().fit()`: takes the independent and dependent values as parameters and fills the regression object with data that describes the relationship.

```py
from sklearn import linear_model

predict_model = linear_model.LogisticRegression()

predict_model.fit(X_LIST, Y_LIST)
```

### Predict

- `sklearn.linear_model.LogisticRegression().predict()`: Predict class labels for samples in X.

```py
# predict if tumor is cancerous where the size is 3.46mm:

target_value = 3.46
target_list = numpy.array(target_value).reshape(-1, 1)

predicted_value = predict_model.predict(target_list)
print(predicted_value)

# We have predicted that a tumor with a size of 3.46mm will not be cancerous.
```

---

### Coefficient

- In logistic regression the `coefficient` is the expected change in log-odds of having the outcome per unit change in X.

- `sklearn.linear_model.LogisticRegression().coef_`: Coefficient of the features in the decision function.
- `sklearn.linear_model.LogisticRegression().intercept_`: Intercept (a.k.a. bias) added to the decision function.

```py
log_odds = predict_model.coef_
# numpy.exp(): Calculate the exponential of all elements in the input array.
odds = numpy.exp(log_odds)

print(odds)
# [[4.03541657]]
# This tells us that as the size of a tumor increases by 1mm the odds of it being a tumor increases by 4x.
```

---

### Probability

- The `coefficient` and `intercept` values can be used to find the `probability` that each tumor is cancerous.

- Create a function that uses the model's coefficient and intercept values to return a new value that represents probability that the given observation is a tumor

```py
def logit2prob(logr, x):
    log_odds = logr.coef_ * x + logr.intercept_
    odds = numpy.exp(log_odds)
    probability = odds / (1 + odds)
    return (probability)


print(logit2prob(predict_model, X_LIST))
# Results Explained
# 3.78 0.61: The probability that a tumor with the size 3.78cm is cancerous is 61%.
# 2.44 0.19: The probability that a tumor with the size 2.44cm is cancerous is 19%.
# 2.09 0.13: The probability that a tumor with the size 2.09cm is cancerous is 13%.
```

---

[Top](#machine-learning---logistic-regression)
