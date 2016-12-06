from load_dataset import load_dataset
from load_dataset import load_grayscale

import tensorflow as tf
import numpy as np

class Trainer:

    def __init__(self, dataset_loading_function):
        self.X_train, self.y_train, self.X_test, self.y_test = dataset_loading_function()
        self.n_train = len(self.X_train)
        self.n_test = len(self.X_test)
        self.image_size = self.X_train[0].shape[0]
        self.n_classes = 42
        self.n_channels = self.X_train[0].shape[2]

        print('Training examples: {}'.format(len(self.X_train)))
        print('Test examples: {}'.format(len(self.X_test)))

    def _reformat(self, dataset, labels):
        dataset = dataset.reshape(
            (-1, self.image_size, self.image_size, self.n_channels)).astype(np.float32)
        labels = (np.arange(self.n_classes) == labels[:,None]).astype(np.float32)
        return dataset, labels

    def _accuracy(self, predictions, labels):
        return (100.0 * np.sum(np.argmax(predictions, 1) == np.argmax(labels, 1)) / predictions.shape[0])

    def train(self):
        image_size = self.image_size
        num_labels = self.n_classes
        num_channels = self.n_channels

        print('Image size {}'.format(image_size))
        print('Num labels {}'.format(num_labels))
        print('Num channels {}'.format(num_channels))

        train_dataset, train_labels = self._reformat(self.X_train, self.y_train)
        test_dataset, test_labels = self._reformat(self.X_test, self.y_test)
        print('Training set', train_dataset.shape, train_labels.shape)
        print('Test set', test_dataset.shape, test_labels.shape)

        batch_size = 8
        patch_size = 5
        depth = 16
        num_hidden = 64

        graph = tf.Graph()

        with graph.as_default():

            # Input data.
            tf_train_dataset = tf.placeholder(tf.float32, shape=(batch_size, image_size, image_size, num_channels))
            tf_train_labels = tf.placeholder(tf.float32, shape=(batch_size, num_labels))
            tf_test_dataset = tf.constant(test_dataset)
          
            # Initialize variables
            layer1_weights = tf.Variable(tf.truncated_normal(
                [patch_size, patch_size, num_channels, depth], stddev=0.001))
            layer1_biases = tf.Variable(tf.zeros([depth]))
            layer2_weights = tf.Variable(tf.truncated_normal(
              [patch_size, patch_size, depth, depth], stddev=0.1))
            layer2_biases = tf.Variable(tf.constant(1.0, shape=[depth]))
            layer3_weights = tf.Variable(tf.truncated_normal(
              [image_size // 4 * image_size // 4 * depth, num_hidden], stddev=0.001))
            layer3_biases = tf.Variable(tf.constant(1.0, shape=[num_hidden]))
            layer4_weights = tf.Variable(tf.truncated_normal(
              [num_hidden, num_labels], stddev=0.1))
            layer4_biases = tf.Variable(tf.constant(1.0, shape=[num_labels]))
          
            # Model.
            def model(data):
                convolutional_layer_1 = tf.nn.conv2d(data, layer1_weights, [1, 1, 1, 1], padding='SAME')
                convolutional_layer_1 = tf.nn.bias_add(convolutional_layer_1, layer1_biases)
                convolutional_layer_1 = tf.nn.relu(convolutional_layer_1)
                hidden = tf.nn.max_pool(convolutional_layer_1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
                
                conv = tf.nn.conv2d(hidden, layer2_weights, [1, 2, 2, 1], padding='SAME')
                hidden = tf.nn.relu(conv + layer2_biases)
                shape = hidden.get_shape().as_list()
                reshape = tf.reshape(hidden, [shape[0], shape[1] * shape[2] * shape[3]])
                hidden = tf.nn.relu(tf.matmul(reshape, layer3_weights) + layer3_biases)
                return tf.matmul(hidden, layer4_weights) + layer4_biases
          
          # Training computation.
            logits = model(tf_train_dataset)
            loss = tf.reduce_mean(
                tf.nn.softmax_cross_entropy_with_logits(logits, tf_train_labels))
            
          # Optimizer.
            optimizer = tf.train.GradientDescentOptimizer(0.001).minimize(loss)
          
          # Predictions for the training, validation, and test data.
            train_prediction = tf.nn.softmax(logits)
            test_prediction = tf.nn.softmax(model(tf_test_dataset))

            num_steps = 100

            with tf.Session(graph=graph) as session:
                tf.initialize_all_variables().run()
                print('Initialized')
                for step in range(num_steps):
                    offset = (step * batch_size) % (train_labels.shape[0] - batch_size)
                    batch_data = train_dataset[offset:(offset + batch_size), :, :, :]
                    batch_labels = train_labels[offset:(offset + batch_size), :]
                    feed_dict = {tf_train_dataset : batch_data, tf_train_labels : batch_labels}
                    _, l, predictions = session.run([optimizer, loss, train_prediction], feed_dict=feed_dict)
                    if (step % 50 == 0):
                        print('Minibatch loss at step %d: %f' % (step, l))
                        print('Minibatch accuracy: %.1f%%' % self._accuracy(predictions, batch_labels))
                        print('Test accuracy: %.1f%%' % self._accuracy(test_prediction.eval(), test_labels))
                        # print('Validation accuracy: %.1f%%' % self._accuracy(
                        # valid_prediction.eval(), valid_labels))
                print('Test accuracy: %.1f%%' % self._accuracy(test_prediction.eval(), test_labels))


if __name__ == "__main__":
    Trainer(load_grayscale).train()