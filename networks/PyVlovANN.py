import numpy as np

X = np.array([(1, 0, 0, 0), (0, 1, 0, 0), (1, 0, 100, 100), (0, 1, 100, 100)], dtype=float)
y = np.array([(100, 100), (0, 0), (-100, -100), (100, 100)], dtype=float)
X = X / np.amax(X, axis=0)
y = y / 100


class ANN:
    def __init__(self):
        self.input_size = 4
        self.output_size = 2
        self.hidden_size = 3

        self.hidden_node_in = np.random.randn(self.input_size,
                                              self.hidden_size)  # (3x4) weight matrix from input to hidden layer
        self.hidden_node_out = np.random.randn(self.hidden_size,
                                               self.output_size)  # (3x2) weight matrix from hidden to output layer

    def forward(self, X):
        # forward propagation through our network
        self.z = np.dot(X, self.hidden_node_in)  # dot product of X (input) and first set of (3x2) weights
        self.z2 = self.sigmoid(self.z)  # activation function
        self.z3 = np.dot(self.z2,
                         self.hidden_node_out)  # dot product of hidden layer (z2) and second set of (3x2) weights
        output = self.sigmoid(self.z3)  # final activation function
        return output

    def sigmoid(self, s):
        # Sigmoid function applied in activation
        return 1 / (1 + np.exp(-s))

    def sigmoid_prime(self, s):
        # Inverse function, used when back propagation to reverse the activation process
        return s * (1 - s)

    def backward(self, X, y, output):
        # back propagation method used and comments supplied are sourced from:
        # https://dev.to/shamdasani/build-a-flexible-neural-network-with-backpropagation-in-python
        self.output_error = y - output  # error in output
        self.output_delta = self.output_error * self.sigmoid_prime(output)  # applying derivative of sigmoid to error

        self.z2_error = self.output_delta.dot(
            self.hidden_node_out.T)  # z2 error: how much our hidden layer weights contributed to output error
        self.z2_delta = self.z2_error * self.sigmoid_prime(self.z2)  # applying derivative of sigmoid to z2 error

        self.hidden_node_in += X.T.dot(self.z2_delta)  # adjusting first set (input --> hidden) weights
        self.hidden_node_out += self.z2.T.dot(self.output_delta)  # adjusting second set (hidden --> output) weights

    def train(self, X, y):
        output = self.forward(X)
        self.backward(X, y, output)


network = ANN()

global first_time
first_time = True


def interact(punish, reward, x, y):
    global first_time
    global X
    global output
    if first_time:
        X = np.array([(1, 0, 0, 0), (0, 1, 0, 0), (1, 0, 100, 100), (0, 1, 100, 100)], dtype=float)
        y = np.array([(100, 100), (0, 0), (-100, -100), (100, 100)], dtype=float)
        X = X / np.amax(X, axis=0)
        y = y / 100
        for i in range(500):
            network.train(X, y)

        first_time = False
        output = network.forward(X)[0]
    else:
        previous_left_output = output[0]
        previous_right_output = output[1]
        X = np.array((punish, reward, previous_left_output, previous_right_output), dtype=float)
        y = np.array((), dtype=float)
        X = X / np.amax(X, axis=0)
        y = y / 100
        output = network.forward(X)[0]
    print(output)
    return output



