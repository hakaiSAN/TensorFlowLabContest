#!/usr/bin/env python
#! -*- coding: utf-8 -*-

import sys
import numpy as np
import cv2
import tensorflow as tf #cv2より前にimportするとcv2.imreadになぜか失敗する(Noneを返す)
import os
import data_input
import model

CHANNELS = 1 #grayscale


def evaluation(imgpath, ckpt_path):
    tf.reset_default_graph()

    jpeg = tf.read_file(filename)
    image = tf.image.decode_jpeg(jpeg, channels=CHANNELS )
    #この時点でimageはuint8 tensor型
    image = tf.cast(image, tf.float32)
    image.reshape([IMAGE_LONG_SIZE, IMAGE_SHORT_SIZE, CHANNELS]) #大きさの統一 データのピクセル数合わせておけば…

    logits = model.inference_deep(image, 1.0, data_input.DST_LONG_SIZE, data_input.DST_SHORT_SIZE, data_input.NUM_CLASS)
    sess = tf.InteractiveSession()
    saver = tf.train.Saver()
    sess.run(tf.initialize_all_variables())
    if ckpt_path:
        saver.restore(sess, ckpt_path)

    softmax = logits.eval()

    result = softmax[0]
    rates = [round(n * 100.0, 1) for n in result]
    print rates

    pred = np.argmax(result)
    print data_input.NAMES[pred]

    pokemons = []
    for idx, rate in enumerate(rates):
        name = mcz_input.NAMES[idx]
        pokemons.append({
            'name_ascii': name[1],
            'name': name[0],
            'rate': rate
        })
    rank = sorted(pokemons, key=lambda x: x['rate'], reverse=True)

    return (rank, pred)

def execute(imgpaths, img_root_dir, ckpt_path):
    res = []
    for imgpath in imgpaths:
        (rank, pred) = evaluation(img_root_dir + '/' + imgpath, ckpt_path)
        res.append({
            'file': imgpath,
            'top_pokemon_id': pred,
            'rank': rank
        })
    return res

if __name__ == '__main__':
    ckpt_path = sys.argv[1]
    imgfile1 = sys.argv[2]
    imgfile2 = sys.argv[3]
    #main([imgfile], ckpt_path)
    #main2(imgfile1, ckpt_path)
    print execute([imgfile1,imgfile2], '.', ckpt_path)
