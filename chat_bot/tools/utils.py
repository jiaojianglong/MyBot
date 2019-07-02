#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/20
# @Author  : JiaoJianglong

import re
import time
import os
import pickle
import hashlib
import logging
from functools import wraps



import heapq

#自动按权重排序队列
class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self,item,priority):

        heapq.heappush(self._queue,(-priority,self._index,item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]

    def get_first(self):
        if self._queue:
            return self._queue[0][-1]
        return {}

    def get(self):
        res = []
        s = sorted(self._queue, key=lambda x: x[0])
        for value in s:
            res.append(value[-1])
        return res

#单例模式
class Singleton(type):
    def __init__(cls,*args,**kwargs):
        cls.__instance = None
        super().__init__(*args,**kwargs)

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args,**kwargs)
            return cls.__instance
        else:
            return cls.__instance


def error_print(info):
    print("\033[1;31;40m" + str(info) + "\033[0m")

def warning_print(info):
    print("\033[1;33;40m" + str(info) + "\033[0m")

def green_print(info):
    print("\033[1;32;40m" + str(info) + "\033[0m")

def green_prints(*args):
    print("\033[1;32;40m" + str(args) + "\033[0m")

def format_print(obj):
    if isinstance(obj, dict):
        print("  {")
        for k, v in obj.items():
            print("    %s : %s"%(k, v))
        print("  }")
    elif isinstance(obj, list):
        print("[")
        for sub_obj in obj:
            format_print(sub_obj)
        print("]")
    else:
        print(obj)


"""
格式：\033[显示方式;前景色;背景色m
 2  
 3 说明：
 4 前景色            背景色           颜色
 5 ---------------------------------------
 6 30                40              黑色
 7 31                41              红色
 8 32                42              绿色
 9 33                43              黃色
10 34                44              蓝色
11 35                45              紫红色
12 36                46              青蓝色
13 37                47              白色
14 显示方式           意义
15 -------------------------
16 0                终端默认设置
17 1                高亮显示
18 4                使用下划线
19 5                闪烁
20 7                反白显示
21 8                不可见
"""


# 去除文本标点符号
def remove_punctuation(text, punctuation='，！？：;。“”‘’、,!?:;."\"\'`',extend_str=""):
    punctuation = punctuation + extend_str
    text = re.sub(r'[{}]+'.format(punctuation), '', text)
    return text.strip()



# 输出函数执行时间
def time_staticstic(func):
    def handler(*args,**kwargs):
        start_time = time.time()
        result = func(*args,**kwargs)
        time_useage = time.time() - start_time
        logging.info("函数：%s,消耗时间：%s%s"%(func.__name__,int(time_useage*1000), "ms"))
        return result
    return handler


# 存储模型
def save_model(mpath, mname, obj):
    with open(os.path.join(mpath, mname), 'wb') as f:
        pickle.dump(obj, f)
    f.close()
    print("Sucessed save model %s" % (mname))


# 读取模型
def load_model(mpath, mname):
    with open(os.path.join(mpath, mname), 'rb') as f:
        obj = pickle.load(f)
    f.close()
    logging.info("Sucessed load model %s" % (mname))
    return obj


def half2full(stren):
    ret_txt = ''
    for r in stren:
        if 33 <= ord(r) <= 126:
            ret_txt += chr(ord(r) + 65248)
        else:
            ret_txt += r
    return ret_txt

def md5(mingwen):
    m = hashlib.md5()
    mdr_str = mingwen.encode()
    m.update(mdr_str)
    ciphertext = m.hexdigest()
    return ciphertext


