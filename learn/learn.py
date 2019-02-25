import numpy as np
import tensorflow as tf
from tensorflow.contrib.layers import fully_connected

x_data, y_data = [], []
with open("data/test.txt", "r") as data_file:
    for line in data_file:
        left, right = line.split('\t')
        x_data.append([float(x_i) for x_i in left.split(',')])
        y_data.append(int(right))

x_data = np.array(x_data)
y_data = np.array(y_data)

#
# y_data = np.array([
#     [0.5,   0.5],
#     [0.64,  0.36],
#     [0.52,  0.48],
#     [0.72,  0.28],
#     [0.96,  0.04],
#     [0.42,  0.58],
#     [0.38,  0.62],
#     [0.4,   0.6],
#     [0.56,  0.44],
#     [0.6,   0.4],
#     [0.44,  0.56],
#     [0.64,  0.36],
#     [0.54,  0.46],
#     [0.7,   0.3],
#     [0.54,  0.46],
#     [0.54,  0.46],
#     [0.66,  0.34],
#     [0.74,  0.26],
#     [0.68,  0.32],
#     [0.64,  0.36],
#     [0.5,   0.5],
#     [0.66,  0.34],
#     [0.52,  0.48],
#     [0.64,  0.36],
#     [0.52,  0.48]
# ])
# y_data = np.array([np.argmax(y) for y in y_data])
# x_data = np.zeros((25, 2))
# for n_nodes, i in zip(range(50, 300, 50), range(5)):
#     for n_seeds, j in zip(range(5, 30, 5), range(5)):
#         x_data[5 * i + j] = np.array([n_nodes, n_seeds])

n_inputs = 2
n_hidden1 = 20
n_hidden2 = 20
n_outputs = 2

learning_rate = .01
n_epochs = 1000
batch_size = 10

x = tf.placeholder(tf.float32, shape=(None, n_inputs), name="x")
y = tf.placeholder(tf.int64, shape=(None,), name="y")

with tf.name_scope("dnn"):
    hidden1 = fully_connected(x, n_hidden1, scope="hidden1")
    hidden2 = fully_connected(hidden1, n_hidden2, scope="hidden2")
    logits = fully_connected(hidden2, n_outputs, scope="outputs", activation_fn=None)

with tf.name_scope("loss"):
    xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(
        labels=y,
        logits=logits
    )
    loss = tf.reduce_mean(xentropy, name="loss")

with tf.name_scope("train"):
    optimizer = tf.train.GradientDescentOptimizer(learning_rate)
    training_op = optimizer.minimize(loss)

with tf.name_scope("eval"):
    correct = tf.nn.in_top_k(logits, y, 1)
    accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))

init = tf.global_variables_initializer()
saver = tf.train.Saver()

with tf.Session() as sess:
    print("training...")
    init.run()

    for epoch in range(n_epochs):
        shuffle = np.arange(len(x_data))
        np.random.shuffle(shuffle)
        x_data, y_data = x_data[shuffle], y_data[shuffle]

        for i in range(len(x_data) // batch_size):
            start, end = i * batch_size, (i + 1) * batch_size
            x_batch, y_batch = x_data[start:end], y_data[start:end]

            sess.run(training_op, feed_dict={x: x_batch, y: y_batch})

            # acc_train = accuracy.eval(feed_dict={
            #     x: x_batch,
            #     y: y_batch
            # })
            # print(epoch, "train accuracy:", acc_train)

            acc_test = accuracy.eval(feed_dict={
                x: x_data,
                y: y_data
            })
            print(epoch, "test accuracy:", acc_test)

    save_path = saver.save(sess, "./model.ckpt")
    print("done!")


def graph_to_input(graph_nx, graph_dict):
    pass

def results_to_output(results):
    pass
