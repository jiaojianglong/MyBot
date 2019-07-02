#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/14
# @Author  : JiaoJianglong

import jieba
from settings import _data_path
from tools.utils import load_model
class MyTfidfModel():
    dct_model_name = "dictionary.pkl"
    tfidf_model_name = "tfidf.pkl"


    def __init__(self):
        self.tfidf_model,self.dct_model = self.get_model()

    def get_model(self):
        dct_model = load_model(_data_path, self.dct_model_name)
        tfidf_model = load_model(_data_path, self.tfidf_model_name)
        return  tfidf_model,dct_model

    def get_weight_tfidf(self,content):
        words = list(jieba.cut(content))
        rec = self.dct_model.doc2bow(words)
        vector = self.tfidf_model[rec]
        words_weight = [(self.dct_model[w_index],w_weight) for w_index,w_weight in vector if w_weight>0.5]
        return words_weight

my_tfidf_model = MyTfidfModel()
