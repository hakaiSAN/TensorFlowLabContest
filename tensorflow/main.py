#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import cv2
import numpy as np
import tensorflow as tf
import tensorflow.python.platform
from datetime import datetime
import random
import time
import os

import data_input
import model

LOGDIR = './tmp/data.%s' % datetime.now().isoformat()
print LOGDIR

flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_string('train', '../data/training.csv', 'File name of train data')
flags.DEFINE_string('test', '../data/test.csv', 'File name of train data')
flags.DEFINE_string('train_dir', LOGDIR, 'Directory to put the training data.')
#訓練回数
flags.DEFINE_integer('max_steps', 100000, 'Number of steps to run trainer.')
#1回の訓練で使う画像の数
flags.DEFINE_integer('batch_size', 80, 'Batch size Must divide evenly into the dataset sizes.')
flags.DEFINE_float('learning_rate', 1e-4, 'Initial learning rate.')

def main(ckpt = None):
    #with tf.Graph().as_default():
    with tf.Session().graph.as_default():
        keep_prob = tf.placeholder("float")

        # データ準備
        images, labels, _ = data_input.load_data([FLAGS.train], FLAGS.batch_size, shuffle = True, distored = True)
        # モデル構築
        logits = model.inference_deep(images, keep_prob, data_input.DST_LONG_SIZE,data_input.DST_SHORT_SIZE, data_input.NUM_CLASS)
        loss_value = model.loss(logits, labels)
        train_op = model.training(loss_value, FLAGS.learning_rate)
        acc = model.accuracy(logits, labels)

        saver = tf.train.Saver(max_to_keep = 0)
        sess = tf.Session()
        sess.run(tf.initialize_all_variables())
        if ckpt:
            print 'restore ckpt', ckpt
            saver.restore(sess, ckpt)
        tf.train.start_queue_runners(sess)

        summary_op = tf.merge_all_summaries()
        summary_writer = tf.train.SummaryWriter(FLAGS.train_dir, sess.graph_def)

        #モデル構築をモニタリング
        for step in range(FLAGS.max_steps):
            start_time = time.time()
            _, loss_result, acc_res = sess.run([train_op, loss_value, acc], feed_dict={keep_prob: 0.99})
            duration = time.time() - start_time

            if step % 10 == 0:
                num_examples_per_step = FLAGS.batch_size
                examples_per_sec = num_examples_per_step / duration
                sec_per_batch = float(duration)
                format_str = ('%s: step %d, loss = %.2f (%.1f examples/sec; %.3f sec/batch)')
                print (format_str % (datetime.now(), step, loss_result, examples_per_sec, sec_per_batch))
                print 'acc_res', acc_res

            if step % 100 == 0:
                summary_str = sess.run(summary_op,feed_dict={keep_prob: 1.0})
                summary_writer.add_summary(summary_str, step)

            if step % 1000 == 0 or (step + 1) == FLAGS.max_steps or loss_result == 0:
                checkpoint_path = os.path.join(FLAGS.train_dir, 'model.ckpt')
                save_path = saver.save(sess, checkpoint_path, global_step=step)
                print('%s saved' % save_path)

            if loss_result == 0:
                print('loss is zero')
                break

if __name__ == '__main__':
    ckpt = None
    if len(sys.argv) == 2:
        ckpt = sys.argv[1]
    main(ckpt)

