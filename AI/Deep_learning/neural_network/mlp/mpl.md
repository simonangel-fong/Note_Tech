# Deep Learning - Multilayer Perceptrons (MLP)

[Back](../../index.md)

- [Deep Learning - Multilayer Perceptrons (MLP)](#deep-learning---multilayer-perceptrons-mlp)
  - [Terminology](#terminology)
  - [Forward Propagation vs Backward Propagation](#forward-propagation-vs-backward-propagation)
    - [Example](#example)
  - [Dropout](#dropout)

---

## Terminology

- `ReLU` / `Rectified Linear Unit`:

  - allowing model **to learn complex patterns** and relationships in the data.
  - `ReLU(x)=max(0,x)`
    - 负数为零
    - 正数为 x 值
    - 取值范围 `[0, )`

---

## Forward Propagation vs Backward Propagation

- `Forward Propagation`:

  - Purpose: **Compute predictions or outputs** of the neural network given input data.
  - Order: Input data is passed through the network layer by layer, undergoing weighted sums and `activation functions` until the final output is generated.
  - Key Steps:
    - 1. Input data enters the input layer.
    - 2. Weighted sums and biases are calculated at each layer.
    - 3. Activation functions introduce non-linearity.
    - 4. Final predictions or outputs are produced.
    - 5. Loss is computed by comparing predictions to actual targets.
  - Use chain rule from calculus

---

- `Backward Propagation (Backpropagation)`:

  - Purpose: **Update model parameters to minimize the loss** during training.
  - Order: **Gradients** of the loss with respect to parameters are calculated and used to **adjust** the model's weights and biases.
  - Key Steps:
    - 1. Compute gradients of the loss with respect to model parameters using the chain rule.
    - 2. Gradients guide the optimization algorithm (e.g., gradient descent) to **update** parameters.
    - 3. The process is repeated for multiple iterations to improve the model's performance.

- Note: `Backward propagation` follows `forward propagation` and is essential for training the neural network. It enables the model to learn and improve by iteratively adjusting its parameters based on the computed gradients. 先 forward, 后 backward

  - 所以在代码中是先 pred_y(forward), 然后计算 loss, 然后 backward 计算梯度, 然后 grad 优化性能.

---

### Example

```py
import torch
import torch.nn as nn
import torch.optim as optim

# Example neural network architecture with one hidden layer
class ExampleModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(ExampleModel, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.activation = nn.Sigmoid()
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        # Forward Propagation
        hidden_layer_output = self.activation(self.fc1(x))
        predicted_output = self.activation(self.fc2(hidden_layer_output))
        return predicted_output, hidden_layer_output

# Example data
input_data = torch.tensor([[0, 1], [1, 0], [1, 1], [0, 0]], dtype=torch.float32)
target_output = torch.tensor([[1], [1], [0], [0]], dtype=torch.float32)

# Initialize the neural network, loss function, and optimizer
input_size = 2
hidden_size = 2
output_size = 1
learning_rate = 0.1
epochs = 10000

model = ExampleModel(input_size, hidden_size, output_size)
criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=learning_rate)

# Training the neural network
for epoch in range(epochs):
    # Forward Propagation
    predicted_output, _ = model(input_data)

    # Compute the loss
    loss = criterion(predicted_output, target_output)

    # Backward Propagation
    optimizer.zero_grad()  # Clear previous gradients
    loss.backward()  # Compute gradients
    optimizer.step()  # Update weights

    # Print the loss every 1000 epochs
    if epoch % 1000 == 0:
        print(f"Epoch {epoch}, Loss: {loss.item()}")

# Test the trained model
test_input = torch.tensor([[1, 1], [0, 1]], dtype=torch.float32)
predicted_output, _ = model(test_input)
print("Predicted Output for Test Input:", predicted_output)

```

---

## Dropout

- `co-adaptation`:

  - a phenomenon where certain neurons or groups of neurons in the network become **highly specialized or overly dependent** on each other during the training process.模型自身 layer 相互依赖
  - `Dropout` breaks up `co-adaptation`

- `DROPOUT`:
  - a regularization technique used t**o prevent overfitting** and **improve** the generalization **performance** of the model.
  - randomly **zero a proportion** of neurons during training, **making the network more robust and less reliant** on specific neurons.

```py
class ModelWithDropout(nn.Module):
    def __init__(self, dropout_rate=0.5):
        super(ModelWithDropout, self).__init__()
        self.fc1 = nn.Linear(in_features=..., out_features=...)
        self.dropout = nn.Dropout(p=dropout_rate)               # drop out
        self.fc2 = nn.Linear(in_features=..., out_features=...)

    def forward(self, x):
        x = self.fc1(x)
        x = self.dropout(x)  # Applying dropout after the first layer
        x = torch.relu(x)
        x = self.fc2(x)
        return x
```

- `dropout probability`:
  - determines the **likelihood** of "dropping out" a neuron during training when using dropout as a regularization technique in neural networks.

---

[TOP](#deep-learning---multilayer-perceptrons-mlp)
