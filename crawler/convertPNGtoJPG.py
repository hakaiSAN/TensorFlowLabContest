#! /usr/bin/env python -S
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
import csv
import sys
import os.path
import subprocess

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
    path,ext = os.path.splitext(row[1])
    array2d.append([])
#    print(ext)
    newfile = '../data/' + argvs[3]+'/'+path+'.jpg'
    cmd = "convert %s %s" % (argvs[2]+'/'+row[1], newfile)
    subprocess.call(cmd, shell=True)
    array2d[len(array2d)-1].append(newfile)
    array2d[len(array2d)-1].append(tables[row[0].decode('utf-8')])
f.close()

outcsvfile = (argvs[4])
f = open(outcsvfile, 'w')
writer = csv.writer(f, lineterminator='\n')
writer.writerows(array2d)
f.close()
