# Machine Learning - Bootstrap Aggregation (Bagging)

[Back](./index.md)

- [Machine Learning - Bootstrap Aggregation (Bagging)](#machine-learning---bootstrap-aggregation-bagging)
  - [Bagging](#bagging)
  - [Evaluating a Base Classifier](#evaluating-a-base-classifier)

---

## Bagging

- `Overfitting`:

  - a concept in data science, which occurs when a statistical model fits exactly against its training data.
  - occurs when the model has a high variance, i.e., the model performs well on the training data but does not perform accurately in the evaluation set.
  - A statistical model is said to be `overfitted` when the model **does not make accurate predictions on testing data**. When a model gets trained with so much data, it **starts learning from the noise and inaccurate data entries** in our data set.

- Problem:

  - Methods such as `Decision Trees`, can be prone to 倾向于 overfitting on the training set which can lead to wrong predictions on new data.

- `Bootstrap Aggregation` (`bagging`): a ensembling method that attempts to resolve overfitting for classification or regression problems.
  - Bagging aims to **improve the accuracy and performance** of machine learning algorithms. It does this **by taking random subsets** of an original dataset, with replacement, and fits either a classifier (for classification) or regressor (for regression) to each subset. The predictions for each subset are then aggregated through majority vote for classification or averaging for regression, increasing prediction accuracy.
  - Bagging 算法，又称 bootstrap aggregation（引导聚集算法），是一种集成学习算法，通常用于降低噪声数据集中的方差。 在 bagging 方法中，训练集中的随机数据样本通过替换进行选择，意味着可多次选择单个数据点。

---

## Evaluating a Base Classifier

To see how bagging can improve model performance, we must start by evaluating how the base classifier performs on the dataset. If you do not know what decision trees are review the lesson on decision trees before moving forward, as bagging is an continuation of the concept.

We will be looking to identify different classes of wines found in Sklearn's wine dataset.



---

[TOP](#machine-learning---bootstrap-aggregation-bagging)
