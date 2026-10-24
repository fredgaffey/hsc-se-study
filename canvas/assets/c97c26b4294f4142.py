import numpy as np

class NeuralNetwork:
    def __init__(self, layers, learning_rate=0.01):
        """
        Initialize the neural network with the number of neurons in each layer (layers) and the learning rate.
        layers: List containing the number of neurons in each layer (e.g., [input_dim, hidden1, hidden2, output_dim]).
        learning_rate: Step size for updating weights during training.
        """
        self.layers = layers
        self.learning_rate = learning_rate
        self.weights = []
        self.biases = []
        self.initialize_weights()
    
    def initialize_weights(self):
        """
        Initialize weights and biases for the network.
        Weights are initialized randomly using a normal distribution.
        Biases are initialized randomly as well.
        """
        for i in range(len(self.layers) - 1):
            weight = np.random.randn(self.layers[i], self.layers[i + 1])
            bias = np.random.randn(1, self.layers[i + 1])
            self.weights.append(weight)
            self.biases.append(bias)
    
    def activation(self, z):
        """
        ReLU activation function.
        ReLU returns the input if it's positive, otherwise it returns 0.
        """
        return np.maximum(0, z)
    
    def activation_derivative(self, z):
        """
        Derivative of ReLU function.
        It returns 1 if the input is positive, otherwise 0.
        """
        return np.where(z > 0, 1, 0)

    def softmax(self, z):
        """
        Softmax activation function for the output layer (used for multi-class classification).
        """
        exp_z = np.exp(z - np.max(z))  # Subtract max to avoid overflow
        return exp_z / exp_z.sum(axis=1, keepdims=True)
    
    def forward(self, X):
        """
        Perform the forward pass. 
        X: Input data.
        """
        self.z_values = []  # Pre-activation values (weighted sums)
        self.a_values = [X]  # Post-activation values (activations)
        
        # Forward propagation through all layers except the last
        for i in range(len(self.weights) - 1):
            z = np.dot(self.a_values[-1], self.weights[i]) + self.biases[i]
            a = self.activation(z)
            self.z_values.append(z)
            self.a_values.append(a)
        
        # Forward propagation through the last layer (softmax for output)
        z_output = np.dot(self.a_values[-1], self.weights[-1]) + self.biases[-1]
        a_output = self.softmax(z_output)
        
        self.z_values.append(z_output)
        self.a_values.append(a_output)
        
        return a_output
    
    def backward(self, X, y):
        """
        Perform the backward pass (backpropagation) and update weights and biases.
        X: Input data.
        y: True labels (one-hot encoded).
        """
        m = X.shape[0]  # Number of samples
        
        # Compute the gradient of the loss with respect to the output layer
        dz_output = self.a_values[-1] - y  # Softmax output - true labels
        dw_output = np.dot(self.a_values[-2].T, dz_output) / m
        db_output = np.sum(dz_output, axis=0, keepdims=True) / m
        
        # Update the last layer's weights and biases
        self.weights[-1] -= self.learning_rate * dw_output
        self.biases[-1] -= self.learning_rate * db_output
        
        # Backpropagate through the hidden layers
        da = dz_output
        for i in reversed(range(len(self.weights) - 1)):
            dz = da.dot(self.weights[i + 1].T) * self.activation_derivative(self.z_values[i])
            dw = np.dot(self.a_values[i].T, dz) / m
            db = np.sum(dz, axis=0, keepdims=True) / m
            
            # Update weights and biases for this layer
            self.weights[i] -= self.learning_rate * dw
            self.biases[i] -= self.learning_rate * db
            
            # Continue backpropagation
            da = dz
    
    def compute_loss(self, y_true, y_pred):
        """
        Compute the cross-entropy loss.
        y_true: One-hot encoded true labels.
        y_pred: Predicted probabilities.
        """
        m = y_true.shape[0]
        loss = -np.sum(y_true * np.log(y_pred + 1e-8)) / m  # Adding a small value to avoid log(0)
        return loss
    
    def train(self, X, y, epochs=1000):
        """
        Train the neural network using the provided training data.
        X: Input data.
        y: True labels (one-hot encoded).
        epochs: Number of times to iterate over the entire training dataset.
        """
        for epoch in range(epochs):
            # Forward pass
            y_pred = self.forward(X)
            
            # Backward pass
            self.backward(X, y)
            
            # Compute and print loss every 100 epochs
            if epoch % 100 == 0:
                loss = self.compute_loss(y, y_pred)
                print(f'Epoch {epoch}, Loss: {loss:.4f}')
    
    def predict(self, X):
        """
        Make predictions for new data.
        X: Input data.
        """
        y_pred = self.forward(X)
        return np.argmax(y_pred, axis=1)

# Usage Example:

# Generate dummy data (e.g., 3 classes, input features)
np.random.seed(42)
X_train = np.random.rand(100, 4)  # 100 samples, 4 features
y_train = np.zeros((100, 3))
y_train[np.arange(100), np.random.choice(3, 100)] = 1  # Random one-hot encoding for 3 classes

# Initialize and train the neural network
nn = NeuralNetwork(layers=[4, 5, 3], learning_rate=0.01)
nn.train(X_train, y_train, epochs=1000)

# Predict on new data
X_test = np.random.rand(10, 4)  # 10 new samples
predictions = nn.predict(X_test)
print("Predictions:", predictions)
