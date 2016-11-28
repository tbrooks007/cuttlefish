import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)

n_nodes = 40
n_lyear = 5
hm_epochs = 300

n_classes = 10
batch_size = 100

x = tf.placeholder('float', [None, 784])
y = tf.placeholder('float')


# TODO: this will be the interface for driving function for kicking off training
def run(nn_config):
    __train_neural_network(x)


def __neural_network_model(data):
    index = 1
    for i in range(0, n_lyear + 1):
        if i == 0:
            globals()['layer%s' % index] = {'weights': tf.Variable(tf.random_normal([784, n_nodes])),
                                            'biases': tf.Variable(tf.random_normal([n_nodes]))}

        elif i == n_lyear:
            output_layer = {'weights': tf.Variable(tf.random_normal([n_nodes, n_classes])),
                            'biases': tf.Variable(tf.random_normal([n_classes])), }

        else:
            globals()['layer%s' % index] = {'weights': tf.Variable(tf.random_normal([n_nodes, n_nodes])),
                                            'biases': tf.Variable(tf.random_normal([n_nodes]))}
        print(['layer%s' % index][0])
        index = index + 1

    index = 1
    for i in range(0, n_lyear + 1):
        if i == 0:
            globals()['l%s' % index] = tf.add(tf.matmul(data, globals()['layer%s' % index]['weights']),
                                              globals()['layer%s' % index]['biases'])
            globals()['l%s' % index] = tf.nn.relu(globals()['l%s' % index])
        elif i == n_lyear:
            temp = n_lyear
            output = tf.matmul(globals()['l%s' % temp], output_layer['weights']) + output_layer['biases']
        else:
            temp = index - 1
            globals()['l%s' % index] = tf.add(
                tf.matmul(globals()['l%s' % temp], globals()['layer%s' % index]['weights']),
                globals()['layer%s' % index]['biases'])
            globals()['l%s' % index] = tf.nn.relu(globals()['l%s' % index])

        print(['l%s' % index][0])
        index = index + 1

    return output


def __train_neural_network(x):
    prediction = __neural_network_model(x)
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(prediction, y))
    optimizer = tf.train.AdamOptimizer().minimize(cost)

    with tf.Session() as sess:
        sess.run(tf.initialize_all_variables())

        for epoch in range(hm_epochs):
            epoch_loss = 0
            for _ in range(int(mnist.train.num_examples / batch_size)):
                epoch_x, epoch_y = mnist.train.next_batch(batch_size)
                _, c = sess.run([optimizer, cost], feed_dict={x: epoch_x, y: epoch_y})
                epoch_loss += c

            print('Epoch', epoch, 'completed out of', hm_epochs, 'loss:', epoch_loss)

        correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))

        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
        print('Accuracy:', accuracy.eval({x: mnist.test.images, y: mnist.test.labels}))