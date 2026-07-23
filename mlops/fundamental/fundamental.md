# MLOPS - Fundamental

[Back](../index.md)

- [MLOPS - Fundamental](#mlops---fundamental)
  - [Machine learning](#machine-learning)
    - [Key steps to train a model](#key-steps-to-train-a-model)

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

### Key steps to train a model

1. **Define the Problem**

- Clearly establish what the model is trying to predict or classify
  - e.g., forecasting sales, detecting fraud, or translating languages
- Set **measurable metrics** to evaluate its success
  - e.g., accuracy, precision, or F1-score

2. **Collect and Prepare Data**

- Gather relevant, high-quality data and clean it by handling missing values and removing duplicates.
- must also **annotate (label)** the data if working with a `supervised learning` task.

3. **Split the Dataset**

- Divide the data into **three distinct sets** to prevent the model from simply memorizing the information (overfitting):
  - `Training Set`:
    - The bulk of the **data used to train** the model.
  - `Validation Set`:
    - Used during training to tune parameters and **check for accuracy**.
  - `Testing Set`:
    - Kept entirely separate until the very end to **evaluate real-world performance**.

4. **Choose an Algorithm**

- Select a foundational algorithm or pre-trained model based on the specific task.
- Common options include
  - traditional `machine learning models`
    - e.g., Random Forests, Linear Regression
  - `deep learning neural networks`.

5. **Train and Optimize**

- Process the training data in iterative cycles (`epochs`) and batches.
  - During this stage, the model makes predictions, calculates errors using a `loss function`, and optimizes its internal parameters (weights and biases) via `backpropagation` to minimize that error.
- adjust `hyperparameters` (like learning rate) to maximize performance.

6. **Evaluate and Validate**

- Test the trained model on the **unseen testing data** to measure its reliability, or use cross-validation techniques for a more robust assessment.
- Compare training vs. testing metrics to detect `underfitting` or `overfitting`.

7. **Deploy and Monitor**

- Once the model meets the performance criteria, integrate it into a real-world application or API and continuously monitor it to ensure it adapts to changing real-world data over time.

---
