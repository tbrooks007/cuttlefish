import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("/tmp/data/", one_hot = True)

x = tf.placeholder('float', [None, 784])
y = tf.placeholder('float')
n_nodes = 40
n_lyear = 5
hm_epochs = 5

n_classes = 10
batch_size = 100

# Flags for defining the tf.train.ClusterSpec
tf.app.flags.DEFINE_string("ps_hosts", "localhost:2222", "...")
tf.app.flags.DEFINE_string("worker_hosts", "localhost:2223", "...")
tf.app.flags.DEFINE_string("job_name", "", "...")
tf.app.flags.DEFINE_integer("task_index", 0, "...")

FLAGS = tf.app.flags.FLAGS

def neural_network_model(data):
    index=1
    for i in  range(0,n_lyear+1):
        if i==0:
           globals()['layer%s' % index] = {'weights':tf.Variable(tf.random_normal([784, n_nodes])),
                                                'biases':tf.Variable(tf.random_normal([n_nodes]))}

        elif i==n_lyear:
            output_layer = {'weights':tf.Variable(tf.random_normal([n_nodes, n_classes])),
                            'biases':tf.Variable(tf.random_normal([n_classes])),}

        else:
            globals()['layer%s' % index] = {'weights':tf.Variable(tf.random_normal([n_nodes, n_nodes])),
                                             'biases':tf.Variable(tf.random_normal([n_nodes]))}
        print (['layer%s' % index][0])
        index=index+1

    index=1
    for i in  range(0,n_lyear+1):
        if i==0:
           globals()['l%s' % index] = tf.add(tf.matmul(data,globals()['layer%s' % index]['weights']), globals()['layer%s' % index]['biases'])
           globals()['l%s' % index] = tf.nn.relu(globals()['l%s' % index])
        elif i==n_lyear:
            temp=n_lyear
            output = tf.matmul(globals()['l%s' % temp],output_layer['weights']) + output_layer['biases']
        else:
            temp=index-1
            globals()['l%s' % index] = tf.add(tf.matmul(globals()['l%s' % temp],globals()['layer%s' % index]['weights']), globals()['layer%s' % index]['biases'])
            globals()['l%s' % index] = tf.nn.relu(globals()['l%s' % index])

        print (['l%s' % index][0])
        index=index+1

    return output

def main(_):
    ps_hosts = FLAGS.ps_hosts.split(",")
    worker_hosts = FLAGS.worker_hosts.split(",")

    # Create a cluster from the parameter server and worker hosts.
    cluster = tf.train.ClusterSpec({"ps": ps_hosts, "worker": worker_hosts})

    # Create and start a server for the local task.
    server = tf.train.Server(cluster, job_name=FLAGS.job_name, task_index=FLAGS.task_index)

    if FLAGS.job_name == "ps":
        server.join()
    elif FLAGS.job_name == "worker":
        pass

    # Assigns ops to the local worker by default.
        with tf.device(tf.train.replica_device_setter(worker_device="/job:worker/task:%d" % FLAGS.task_index, cluster=cluster)):

               #Build model...
               global_step = tf.Variable(0)
               prediction = neural_network_model(x)
               cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(prediction,y))
               optimizer = tf.train.AdagradOptimizer(0.01).minimize(cost, global_step=global_step)

               saver = tf.train.Saver()
               correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))
               accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
               summary_op = tf.merge_all_summaries()
               init_op = tf.initialize_all_variables()

               #Create a "supervisor", which oversees the training process.
               sv = tf.train.Supervisor(is_chief=(FLAGS.task_index == 0),
                   logdir="/tmp/train_logs",
                   init_op=init_op,
                   summary_op=summary_op,
                   saver=saver,
                   global_step=global_step,
                  save_model_secs=600)


            #The supervisor takes care of session initialization, restoring from
            #a checkpoint, and closing when done or an error occurs.
        with sv.managed_session(server.target) as sess:
               #Loop until the supervisor shuts down or 1000000 steps have completed.
            step = 0

            while not sv.should_stop() and step < hm_epochs:
                epoch_loss = 0
                step = step + 1
                for _ in range(int(mnist.train.num_examples/batch_size)):

                    epoch_x, epoch_y = mnist.train.next_batch(batch_size)
                    _, c = sess.run([optimizer, cost], feed_dict={x: epoch_x, y: epoch_y})
                    epoch_loss += c

                print('Epoch', step, 'completed out of',hm_epochs,'loss:',epoch_loss)

            print("Accuracy: ", sess.run(accuracy, feed_dict={x: mnist.test.images, y: mnist.test.labels})*100)
           # Ask for all the services to stop.
        sv.stop()

if __name__ == "__main__":
    tf.app.run()
