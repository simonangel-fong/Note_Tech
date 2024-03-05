# Deep Learning

[Back](../../index.md)

---

- [Deep Learning](./deep_learning/deep_learning.md)

- [Environment Configuration](./env_config/env_config.md)

---

- [Neural Network](./neural_network/neural_network/neural_network.md)

  - [Linear Neural Networks for Classification](./neural_network/classification/classification.md)
  - [Multilayer Perceptrons (MLP)](./neural_network/mlp/mpl.md)

---

- Summary:

- Essential part of DL:

  - data:
    - tensor
  - model:

    - forward function
    - activation function
      - linear: ax
      - simoid: (0, 1), output layer with two categories.
      - relu: (0, x), hidden layer
      - softmax: %, output layers with more than two categories

  - Objective function:

    - loss fnction
    - criterion
      - MSELoss: linear regression
      - CrossEntropyLoss: multi-class classification

  - Algorithm:
    - optimizer
      - Backward Propagation: find gradient
      - gradient descent:
        - find gradient + update weights
        - lr (how fast model learns) + gradient (direction the model learns)
        - rely Backward Propagation
        - optim.SGD(params)
      - optim.Adam(params)

---

[TOP](#deep-learning)
