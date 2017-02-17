import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import tensorflow as tf  # Version r0.10
from giotto.ml.dataset import Dataset
from pprint import pprint

class RNNNeuralNetwork:
    def __init__(self):
        self.n_hidden = 32
        self.learning_rate = 0.0025
        self.lambda_loss_amount = 0.0015
        self.batch_size = 1500
        self.display_iter = 30000

    def test(self, training_dataset, testing_dataset):
        training_dataset, used_features = training_dataset.to_tsfresh_features()
        testing_dataset, _ = testing_dataset.to_tsfresh_features(used_features)

        self.scaler = training_dataset.scaler()
        training_dataset.scale(self.scaler)
        testing_dataset.scale(self.scaler)

        self.labels = training_dataset.labels()
        self.n_classes = len(self.labels)
        self.X_train = training_dataset.transpose_samples()
        self.y_train = training_dataset.indexed_labels(self.labels)
        training_data_count = len(self.X_train)
        self.training_iters = training_data_count * 1000

        X_test = testing_dataset.transpose_samples()
        y_test = testing_dataset.indexed_labels(self.labels)
        self.__dataset_info(X_test, y_test)

        test_data_count = len(X_test)
        n_steps = len(self.X_train[0])
        n_input = len(self.X_train[0][0])

        x = tf.placeholder(tf.float32, [None, n_steps, n_input])
        y = tf.placeholder(tf.float32, [None, self.n_classes])

        weights = {
            'hidden': tf.Variable(tf.random_normal([n_input, self.n_hidden])),
            'out': tf.Variable(tf.random_normal([self.n_hidden, self.n_classes], mean=1.0))
        }
        biases = {
            'hidden': tf.Variable(tf.random_normal([self.n_hidden])),
            'out': tf.Variable(tf.random_normal([self.n_classes]))
        }

        pred = self.__LSTM_RNN(x, weights, biases, n_input, n_steps)

        l2 = self.lambda_loss_amount * sum(
            tf.nn.l2_loss(tf_var) for tf_var in tf.trainable_variables()
        )
        cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(pred, y)) + l2
        optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(cost)

        correct_pred = tf.equal(tf.argmax(pred,1), tf.argmax(y,1))
        accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

        test_losses = []
        test_accuracies = []
        train_losses = []
        train_accuracies = []

        self.sess = tf.Session()
        tf.global_variables_initializer().run(session=self.sess)

        step = 1
        while step * self.batch_size <= self.training_iters:
            batch_xs = self.__extract_batch_size(self.X_train, step, self.batch_size)
            batch_ys = self.__one_hot(self.__extract_batch_size(self.y_train, step, self.batch_size))

            _, loss, acc = self.sess.run(
                [optimizer, cost, accuracy],
                feed_dict={
                    x: batch_xs,
                    y: batch_ys
                }
            )
            train_losses.append(loss)
            train_accuracies.append(acc)

            if (step * self.batch_size % self.display_iter == 0) or (step == 1) or (step * self.batch_size > self.training_iters):

                print "Training iter #" + str(step * self.batch_size) + \
                    ":   Batch Loss = " + "{:.6f}".format(loss) + \
                    ", Accuracy = {}".format(acc)

                loss, acc = self.sess.run(
                    [cost, accuracy],
                    feed_dict={
                        x: X_test,
                        y: self.__one_hot(y_test)
                    }
                )
                test_losses.append(loss)
                test_accuracies.append(acc)
                print "PERFORMANCE ON TEST SET: " + \
                    "Batch Loss = {}".format(loss) + \
                    ", Accuracy = {}".format(acc)

            step += 1

        print "Optimization Finished!"

        one_hot_predictions, accuracy, final_loss = self.sess.run(
            [pred, accuracy, cost],
            feed_dict={
                x: X_test,
                y: self.__one_hot(y_test)
            }
        )

        test_losses.append(final_loss)
        test_accuracies.append(accuracy)

        print "FINAL RESULT: " + \
            "Batch Loss = {}".format(final_loss) + \
            ", Accuracy = {}".format(accuracy)

        # X_one, y_one = Dataset([testing_dataset.samples[0]]).transpose_samples(self.labels)
        #
        # predictions = self.sess.run(
        #     [pred],
        #     feed_dict={
        #         x: X_one
        #     }
        # )
        # pprint(predictions)

        self.plot(train_losses, train_accuracies, test_losses, test_accuracies)

    def plot(self, train_losses, train_accuracies, test_losses, test_accuracies):
        # (Inline plots: )
        # %matplotlib inline

        font = {
            'family' : 'Bitstream Vera Sans',
            'weight' : 'bold',
            'size'   : 18
        }
        matplotlib.rc('font', **font)

        width = 12
        height = 12
        plt.figure(figsize=(width, height))

        indep_train_axis = np.array(range(self.batch_size,
            (len(train_losses)+1)*self.batch_size, self.batch_size))
        plt.plot(indep_train_axis, np.array(train_losses),     "b--", label="Train losses")
        plt.plot(indep_train_axis, np.array(train_accuracies), "g--", label="Train accuracies")

        indep_test_axis = np.array(range(self.batch_size,
            len(test_losses)*self.display_iter, self.display_iter)[:-1] + [self.training_iters])
        plt.plot(indep_test_axis, np.array(test_losses),     "b-", label="Test losses")
        plt.plot(indep_test_axis, np.array(test_accuracies), "g-", label="Test accuracies")

        plt.title("Training session's progress over iterations")
        plt.legend(loc='upper right', shadow=True)
        plt.ylabel('Training Progress (Loss or Accuracy values)')
        plt.xlabel('Training iteration')

        plt.show()


    def __extract_batch_size(self, _train, step, batch_size):
        # Function to fetch a "batch_size" amount of data from "(X|y)_train" data.

        shape = list(_train.shape)
        shape[0] = batch_size
        batch_s = np.empty(shape)

        for i in range(batch_size):
            # Loop index
            index = ((step-1)*batch_size + i) % len(_train)
            batch_s[i] = _train[index]

        return batch_s

    def __one_hot(self, y_):
        # Function to encode output labels from number indexes
        # e.g.: [[5], [0], [3]] --> [[0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0]]

        y_ = y_.reshape(len(y_))
        n_values = len(self.labels)
        return np.eye(n_values)[np.array(y_, dtype=np.int32)]  # Returns FLOATS


    def __LSTM_RNN(self, _X, _weights, _biases, n_input, n_steps):
        # Function returns a tensorflow LSTM (RNN) artificial neural network from given parameters.
        # Moreover, two LSTM cells are stacked which adds deepness to the neural network.
        # Note, some code of this notebook is inspired from an slightly different
        # RNN architecture used on another dataset:
        # https://tensorhub.com/aymericdamien/tensorflow-rnn

        # (NOTE: This step could be greatly optimised by shaping the dataset once
        # input shape: (batch_size, n_steps, n_input)
        _X = tf.transpose(_X, [1, 0, 2])  # permute n_steps and batch_size
        # Reshape to prepare input to hidden activation
        _X = tf.reshape(_X, [-1, n_input])
        # new shape: (n_steps*batch_size, n_input)

        # Linear activation
        _X = tf.nn.relu(tf.matmul(_X, _weights['hidden']) + _biases['hidden'])
        # Split data because rnn cell needs a list of inputs for the RNN inner loop
        _X = tf.split(0, n_steps, _X)
        # new shape: n_steps * (batch_size, n_hidden)

        # Define two stacked LSTM cells (two recurrent layers deep) with tensorflow
        lstm_cell_1 = tf.nn.rnn_cell.BasicLSTMCell(self.n_hidden, forget_bias=1.0, state_is_tuple=True)
        lstm_cell_2 = tf.nn.rnn_cell.BasicLSTMCell(self.n_hidden, forget_bias=1.0, state_is_tuple=True)
        lstm_cells = tf.nn.rnn_cell.MultiRNNCell([lstm_cell_1, lstm_cell_2], state_is_tuple=True)
        # Get LSTM cell output
        outputs, states = tf.nn.rnn(lstm_cells, _X, dtype=tf.float32)

        # Get last time step's output feature for a "many to one" style classifier,
        # as in the image describing RNNs at the top of this page
        lstm_last_output = outputs[-1]

        # Linear activation
        return tf.matmul(lstm_last_output, _weights['out']) + _biases['out']

    def __dataset_info(self, X_test, y_test):
        # Some debugging info

        print "Some useful info to get an insight on dataset's shape and normalisation:"
        print "(X shape, y shape, every X's mean, every X's standard deviation)"
        print (X_test.shape,
                y_test.shape,
                np.mean(X_test),
                np.std(X_test))
        print "The dataset is therefore properly normalised, as expected, but not yet one-hot encoded."

