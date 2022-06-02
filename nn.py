import numpy as np


class NeuralNetwork:

    def __init__(self, layer_sizes):
        """
        Neural Network initialization.
        Given layer_sizes as an input, you have to design a Fully Connected Neural Network architecture here.
        :param layer_sizes: A list containing neuron numbers in each layers. For example [3, 10, 2] means that there are
        3 neurons in the input layer, 10 neurons in the hidden layer, and 2 neurons in the output layer.
        """
        # TODO (Implement FCNNs architecture here)
        self.layer_sizes = layer_sizes
        self.weights = []
        self.biases = []
        for i in range(1, len(layer_sizes)):
            self.weights.append(np.random.normal(0, 1, (layer_sizes[i], layer_sizes[i - 1])))
            self.biases.append(np.zeros(layer_sizes[i]))

    def activation(self, x):
        """
        The activation function of our neural network, e.g., Sigmoid, ReLU.
        :param x: Vector of a layer in our network.
        :return: Vector after applying activation function.
        """
        # TODO (Implement activation function here)

        return np.maximum(0, x)
        #return 1 / (1 + np.e ** x)

    def forward(self, x):
        """
        Receives input vector as a parameter and calculates the output vector based on weights and biases.
        :param x: Input vector which is a numpy array.
        :return: Output vector
        """
        # TODO (Implement forward function here)
        for i in range(len(self.weights)):
            x = self.activation((self.weights[i] @ x) + self.biases[i])
        return x
