#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import cv2
import random
import numpy as np
import tensorflow as tf
import os.path

IMAGE_LONG_SIZE = 600
IMAGE_SHORT_SIZE = 400 
INPUT_LONG_SIZE = 540
INPUT_SHORT_SIZE = 360
DST_SHORT_SIZE = 40
DST_LONG_SIZE = 60
NUM_CLASS = 6
NUM_EXAMPLES_PER_EPOCH_FOR_TRAIN = 500
CHANNELS = 1

NAMES = {
    0: [u"ゼニガメ", "zenigame"],
    1: [u"ワニノコ", "waninoko"],
    2: [u"ミズゴロウ", "mizugorou"],
    3: [u"ポッチャマ", "pocchama"],
    4: [u"ミジュマル", "mijumaru"],
    5: [u"ケロマツ", "keromatsu"],
}

def load_data_for_test(csv, batch_size):
    return load_data(csv, batch_size, shuffle = False, distored = False)

#データをtensor型に変換する
def load_data(csv, batch_size, shuffle = True, distored = True):
    #csvデータの読み込み
    queue = tf.train.string_input_producer(csv, shuffle=shuffle)
    reader = tf.TextLineReader()
    # 1行ずつ読み込む
    key, value = reader.read(queue)
    # 型の例("path", 1) parseを行う
    filename, label = tf.decode_csv(value, [["path"],[1]])

    #labelはプレースホルダー（実行時に入力する変数）
    label = tf.cast(label, tf.int64)
    #one_hot:one-of-K表現
    #１つの多クラス識別問題→多数の2クラス識別問題へ分解できる（1次元ベクトル→多次元ベクトルへ変換）
    #depth(NUM_CLASS)の分だけ分解する
    label = tf.one_hot(label, depth = NUM_CLASS, on_value = 1.0, off_value = 0.0, axis = -1)

    jpeg = tf.read_file(filename)
    image = tf.image.decode_jpeg(jpeg, channels=CHANNELS )
    #この時点でimageはuint8(pngはuint16?) tensor型
    image = tf.cast(image, tf.float32)
    image.set_shape([IMAGE_LONG_SIZE, IMAGE_SHORT_SIZE, CHANNELS])
    #大きさの統一 データのピクセル数合わせておけば…

    #データ拡張 cropしたり，回転したり，コントラストいじったり
    if distored:
        cropsizel = random.randint(INPUT_LONG_SIZE, INPUT_LONG_SIZE + (IMAGE_LONG_SIZE - INPUT_LONG_SIZE) / 2)
        framesizel = INPUT_LONG_SIZE + (cropsizel - INPUT_LONG_SIZE) * 2
        cropsizes = random.randint(INPUT_SHORT_SIZE, INPUT_SHORT_SIZE + (IMAGE_SHORT_SIZE - INPUT_SHORT_SIZE) / 2)
        framesizes = INPUT_SHORT_SIZE + (cropsizes - INPUT_SHORT_SIZE) * 2
#        image = tf.image.resize_image_with_crop_or_pad(image, framesizel, framesizes)
#        image = tf.random_crop(image, [cropsizel, cropsizes, CHANNELS])
        image = tf.image.random_flip_left_right(image)
        image = tf.image.random_brightness(image, max_delta=0.8)
        image = tf.image.random_contrast(image, lower=0.8, upper=1.0)
        #RGBじゃないので不可
        #image = tf.image.random_hue(image, max_delta=0.04)
        #image = tf.image.random_saturation(image, lower=0.6, upper=1.4)

    #tensorのサイズを変更　計算可能領域
    #tensorの標準化
    image = tf.image.resize_images(image, DST_LONG_SIZE , DST_SHORT_SIZE)
    image = tf.image.per_image_whitening(image)

    # シャッフル値の設定
    min_fraction_of_examples_in_queue = 0.4
    min_queue_examples = int(NUM_EXAMPLES_PER_EPOCH_FOR_TRAIN * min_fraction_of_examples_in_queue)

    return _generate_image_and_label_batch(
            image,
            label,
            filename,
            min_queue_examples, batch_size,
            shuffle=shuffle)

def _generate_image_and_label_batch(image, label, filename, min_queue_examples,
                                    batch_size, shuffle):

    # データを処理するバッチ，キューを生成
    # その後バッチサイズを
    # read 'batch_size' image_batch + labels from the example queue.
    num_preprocess_threads = 16
    capacity = min_queue_examples + 3 * batch_size

    #shuffle がtrue ならばシャッフルを行う（通常は行う）min_after_dequeueの値
    if shuffle:
        image_batch, label_batch, filename = tf.train.shuffle_batch(
            [image, label, filename],
            batch_size=batch_size,
            num_threads=num_preprocess_threads,
            capacity=capacity,
            min_after_dequeue=min_queue_examples)
    else:
        image_batch, label_batch, filename = tf.train.batch(
            [image, label, filename],
            batch_size=batch_size,
            num_threads=num_preprocess_threads,
            capacity=capacity)

    # visualizerで可視化.
    tf.image_summary('image', image_batch, max_images = 100)

    labels = tf.reshape(label_batch, [batch_size, NUM_CLASS])
    return image_batch, labels, filename
