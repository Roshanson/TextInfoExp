#! /usr/bin/env python

import tensorflow as tf
from tensorflow.python.platform import gfile
import numpy as np
import os
import time
import datetime
import data_helpers
from text_cnn import TextCNN
from memory_profiler import profile

# Parameters
# ==================================================

# Model Hyperparameters
tf.flags.DEFINE_integer("embedding_dim", 128, "Dimensionality of character embedding (default: 128)")
tf.flags.DEFINE_string("filter_sizes", "1,2,3,4,5,6,8", "Comma-separated filter sizes (default: '1,2,3,4,5,6,8')")
tf.flags.DEFINE_string("num_filters", "50,100,150,150,200,200,200", "Number of filters per filter size (default: 50,100,150,150,200,200,200)")
tf.flags.DEFINE_float("dropout_keep_prob", 0.5, "Dropout keep probability (default: 0.5)")
tf.flags.DEFINE_float("l2_reg_lambda", 0.0, "L2 regularizaion lambda (default: 0.0)")

# Training parameters
tf.flags.DEFINE_integer("batch_size", 32, "Batch Size (default: 32)")
tf.flags.DEFINE_integer("num_epochs", 200, "Number of training epochs (default: 200)")
tf.flags.DEFINE_integer("evaluate_every", 100, "Evaluate model on dev set after this many steps (default: 100)")
tf.flags.DEFINE_integer("checkpoint_every", 100, "Save model after this many steps (default: 100)")
# Misc Parameters
tf.flags.DEFINE_string("checkpoint", '', "Resume checkpoint")
tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")

FLAGS = tf.flags.FLAGS
print("\nParameters:")
for attr, value in sorted(FLAGS.__flags.iteritems()):
  print("{}={}".format(attr.upper(), value))
print("")


# Data Preparatopn
# ==================================================

# Load data
print("Loading data...")
x, y, vocabulary, vocabulary_inv = data_helpers.load_data()
print x,y,vocabulary,vocabulary_inv
# Randomly shuffle data
np.random.seed(10)
shuffle_indices = np.random.permutation(np.arange(len(y)))
x_shuffled = x[shuffle_indices]
y_shuffled = y[shuffle_indices]
# Split train/test set
# TODO: This is very crude, should use cross-validation
x_train, x_dev = x_shuffled[:-300], x_shuffled[-300:]
y_train, y_dev = y_shuffled[:-300], y_shuffled[-300:]
sequence_length = x_train.shape[1]
print("Vocabulary Size: {:d}".format(len(vocabulary)))
print("Train/Dev split: {:d}/{:d}".format(len(y_train), len(y_dev)))
print("Sequnence Length: {:d}".format(sequence_length))


# Training
# ==================================================

with tf.Graph().as_default():
  session_conf = tf.ConfigProto(
    allow_soft_placement=FLAGS.allow_soft_placement,
    log_device_placement=FLAGS.log_device_placement)
  sess = tf.Session(config=session_conf)
  with sess.as_default():
    cnn = TextCNN(
      sequence_length=sequence_length,
      num_classes=2,
      vocab_size=len(vocabulary),
      embedding_size=FLAGS.embedding_dim,
      filter_sizes=map(int, FLAGS.filter_sizes.split(",")),
      num_filters=map(int, FLAGS.num_filters.split(",")),
      l2_reg_lambda=FLAGS.l2_reg_lambda)

    # Define Training procedure
    global_step = tf.Variable(0, name="global_step", trainable=False)
    optimizer = tf.train.AdamOptimizer(1e-4)
    grads_and_vars = optimizer.compute_gradients(cnn.loss, aggregation_method=2)
    train_op = optimizer.apply_gradients(grads_and_vars, global_step=global_step)

    # Keep track of gradient values and sparsity (optional)
    grad_summaries = []
    for g, v in grads_and_vars:
      if g is not None:
        grad_hist_summary = tf.summary.histogram("{}/grad/hist".format(v.name), g)
        sparsity_summary = tf.summary.scalar("{}/grad/sparsity".format(v.name), tf.nn.zero_fraction(g))
        grad_summaries.append(grad_hist_summary)
        grad_summaries.append(sparsity_summary)
    grad_summaries_merged = tf.summary.merge(grad_summaries)

    # Output directory for models and summaries
    if FLAGS.checkpoint == "":
      timestamp = str(int(time.time()))
      out_dir = os.path.abspath(os.path.join(os.path.curdir, "runs", timestamp))
      print("Writing to {}\n".format(out_dir))
    else:
      out_dir = FLAGS.checkpoint

    # Summaries for loss and accuracy
    loss_summary = tf.summary.scalar("loss", cnn.loss)
    acc_summary = tf.summary.scalar("accuracy", cnn.accuracy)

    # Train Summaries
    train_summary_op = tf.summary.merge([loss_summary, acc_summary, grad_summaries_merged])
    train_summary_dir = os.path.join(out_dir, "summaries", "train")
    train_summary_writer = tf.summary.FileWriter(train_summary_dir, sess.graph_def)

    # Dev summaries
    dev_summary_op = tf.summary.merge([loss_summary, acc_summary])
    dev_summary_dir = os.path.join(out_dir, "summaries", "dev")
    dev_summary_writer = tf.summary.FileWriter(dev_summary_dir, sess.graph_def)

    # Checkpoint directory. Tensorflow assumes this directory already exists so we need to create it
    checkpoint_dir = os.path.abspath(os.path.join(out_dir, "checkpoints"))
    checkpoint_prefix = os.path.join(checkpoint_dir, "model")
    if not os.path.exists(checkpoint_dir):
      os.makedirs(checkpoint_dir)
    saver = tf.train.Saver(tf.all_variables())

    # Initialize all variables
    sess.run(tf.initialize_all_variables())

    ckpt = tf.train.get_checkpoint_state(os.path.join(FLAGS.checkpoint, 'checkpoints'))
    if ckpt and gfile.Exists(ckpt.model_checkpoint_path):
      print "Reading model parameters from %s" % ckpt.model_checkpoint_path
      saver.restore(sess, ckpt.model_checkpoint_path)


    @profile(precision=4)
    def train_step(x_batch, y_batch):
      """
      A single training step
      """
      feed_dict = {
        cnn.input_x: x_batch,
        cnn.input_y: y_batch,
        cnn.dropout_keep_prob: FLAGS.dropout_keep_prob
      }
      _, step, summaries, loss, accuracy = sess.run(
        [train_op, global_step, train_summary_op, cnn.loss, cnn.accuracy],
        feed_dict)
      time_str = datetime.datetime.now().strftime("%d, %b %Y %H:%M:%S")
      print("{}: step {}, loss {:g}, acc {:g}".format(time_str, step, loss, accuracy))
      train_summary_writer.add_summary(summaries, step)


    @profile(precision=4)
    def dev_step(x_batch, y_batch, writer=None):
      """
      Evaluates model on a dev set
      """
      feed_dict = {
        cnn.input_x: x_batch,
        cnn.input_y: y_batch,
        cnn.dropout_keep_prob: 1.0
      }
      step, summaries, loss, accuracy = sess.run(
        [global_step, dev_summary_op, cnn.loss, cnn.accuracy],
        feed_dict)
      time_str = datetime.datetime.now().strftime("%d, %b %Y %H:%M:%S")
      print("{}: step {}, loss {:g}, acc {:g}".format(time_str, step, loss, accuracy))
      if writer:
        writer.add_summary(summaries, step)

    # Generate batches
    batches = data_helpers.batch_iter(
      zip(x_train, y_train), FLAGS.batch_size, FLAGS.num_epochs)
    # Training loop. For each batch...
    for batch in batches:
      x_batch, y_batch = zip(*batch)
      train_step(x_batch, y_batch)
      current_step = tf.train.global_step(sess, global_step)
      if current_step % FLAGS.evaluate_every == 0:
        print("\nEvaluation:")
        dev_step(x_dev, y_dev, writer=dev_summary_writer)
        print("")
      if current_step % FLAGS.checkpoint_every == 0:
        path = saver.save(sess, checkpoint_prefix, global_step=current_step)
        print("Saved model checkpoint to {}\n".format(path))



