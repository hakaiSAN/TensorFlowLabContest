#! /usr/bin/env python -S
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
import csv
import sys
import os.path

#sys.setdefaultencoding('utf-8')
argvs = sys.argv
incsvfile = (argvs[1])
f = open(incsvfile, "r")
reader = csv.reader(f)
# header = next(reader)


tables={
        u'ゼニガメ':0,
        u'ワニノコ':1,
        u'ミズゴロウ':2,
        u'ポッチャマ':3,
        u'ミジュマル':4,
        u'ケロマツ':5
       }

# 1行ずつ読み込む
array2d =[]
for row in reader :
#        print tables[row[0].decode('utf-8')] #for debug
    array2d.append([])
    path,ext = os.path.splitext(row[1])
#    print(ext)
    if (ext == ".JPEG" or ext == ".JPG" or ext == ".jpg" or ext == ".jpeg") :
        array2d[len(array2d)-1].append('../data/'+argvs[2]+'/'+path+'.jpg')
    elif (ext == ".PNG" or ext == ".png") :
        array2d[len(array2d)-1].append('../data/'+argvs[2]+'/'+path+'.png')
    array2d[len(array2d)-1].append(tables[row[0].decode('utf-8')])
f.close()



outcsvfile = (argvs[3])
f = open(outcsvfile, 'w')
writer = csv.writer(f, lineterminator='\n')
writer.writerows(array2d)
f.close()
