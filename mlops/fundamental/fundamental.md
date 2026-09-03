# MLOPS - Fundamental

[Back](../index.md)

- [MLOPS - Fundamental](#mlops---fundamental)
  - [Machine learning](#machine-learning)
    - [Stages of the Machine Learning Life Cycle](#stages-of-the-machine-learning-life-cycle)
  - [MLOps](#mlops)
  - [`Continuous Training (CT)`](#continuous-training-ct)

---

## Machine learning

- `Machine learning`
  - a subset of `artificial intelligence` where computers **learn patterns from data** and **make predictions or decisions** without being explicitly programmed.
  - a `machine learning model` is trained on examples, allowing it to adapt and improve automatically.
  - output of machine learning: a model that a mathematical function.

- **How It Works**:
  - **feed the computer data** alongside the desired output,
  - the algorithm **figures out the rules** that connect them.
- `Model Training`:
  - iterative process involves **feeding data** into an algorithm, checking its **accuracy**, and **adjusting parameters** to minimize errors.
  - Over time, the model "learns" and can generalize its knowledge to new, unseen data.

---

- Types of Machine Learning
  - `Supervised Learning`:
    - The model is trained on `labeled data`, which serves as an "answer key".
    - For example, by analyzing thousands of images tagged as "cat" or "dog," the model learns to identify these animals in new photos.
  - `Unsupervised Learning`:
    - The algorithm receives unlabelled data and must discover hidden structures or patterns on its own.
    - A common use is `clustering`, such as an e-commerce site grouping customers by their purchasing habits.
  - `Reinforcement Learning`:
    - The model learns **through trial and error** by performing actions in an environment and receiving rewards or penalties.
    - It is commonly used in robotics and to teach AI to play complex strategy games.

---

### Stages of the Machine Learning Life Cycle

1. **Problem Definition**
   - Define the business problem, machine learning objective, success metrics, and constraints.

2. **Data Collection**
   - Gather relevant data from reliable internal and external sources.

3. **Data Cleaning**
   - Handle missing values, duplicates, errors, inconsistencies, and outliers.

4. **Feature Engineering**
   - Create, transform, and select useful input features, then split the data into training, validation, and test sets.

5. **Model Selection**
   - Compare suitable algorithms and select a model based on the problem, data, and baseline performance.

6. **Model Training**
   - Train the selected model on the training data to learn its parameters.

7. **Model Evaluation**
   - Evaluate generalization on unseen data using metrics appropriate to the problem.

8. **Hyperparameter Tuning**
   - Optimize hyperparameters using validation data or cross-validation, then confirm performance on the test set.

9. **Model Deployment**
   - Integrate the validated model into a production system to generate predictions.

10. **Model Monitoring and Maintenance**
    - Track performance, data drift, concept drift, and operational health; retrain or update the model when needed.

---

## MLOps

- `MLOps (Machine Learning Operations)`
  - a set of engineering practices that **automates and streamlines the lifecycle** of `machine learning models`.
  - bridges the gap between `data science` and `IT operations`, allowing teams to build, test, deploy, and continuously monitor models in production reliably and efficiently.

- Features:
  - **Automation**:
    - Triggers **automated retraining** when the environment or underlying data changes.
  - **Model Drift**:
    - Continuously **monitors** deployed models to ensure they **maintain high accuracy** as real-world data evolves.
  - **Reproducibility**:
    - **Tracks** exactly which data, code, and hyperparameters were used to train a specific **model version**.

---

## `Continuous Training (CT)`

- `Continuous Training (CT)`
  - **automates the re-execution** of the `model training pipeline` without manual intervention.
- **Automated Triggers**:
  - Pipelines are automatically kicked off based on schedules, new data arrivals, or when monitoring systems detect performance degradation.
- **Model Training**:
  - Automated ingestion of new data, feature engineering, and training algorithms.
- **Model Evaluation & Registry**:
  - The newly trained model is evaluated against validation metrics
    - e.g., accuracy, F1-score
  - registered only if it outperforms the current production model.
