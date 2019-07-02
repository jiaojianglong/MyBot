#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/14
# @Author  : JiaoJianglong


import os
from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer

DATA_PATH = "/home/jiaojianglong/data"
LTPMODEL_PATH = os.path.join(DATA_PATH, "pyltp_model/ltp-data-v3.3.1/ltp_data/")

class MyLTP(object):
    def __init__(self):
        self.segmentor = Segmentor()
        self.postagger = Postagger()
        self.parser = Parser()
        self.recognizer = NamedEntityRecognizer()


    def load(self, step='all'):
        self.segmentor.load(LTPMODEL_PATH + "cws.model")
        self.postagger.load(LTPMODEL_PATH + "pos.model")
        self.parser.load(LTPMODEL_PATH + "parser.model")
        self.recognizer.load(LTPMODEL_PATH + "ner.model")

    def release(self):
        self.segmentor.release()
        self.postagger.release()
        self.parser.release()
        self.recognizer.release()

    def ne_result(self, content):
        words = self.segmentor.segment(content)
        postags = self.postagger.postag(words)
        netags = self.recognizer.recognize(words, postags)
        # print(netags)
        return words, postags, netags

    def arcs_result(self, content):
        words = self.segmentor.segment(content)
        postags = self.postagger.postag(words)
        arcs = self.parser.parse(words, postags)
        return arcs

    def seg(self, sent):
        words = self.segmentor.segment(sent)
        words = ' '.join(words).split()
        return words


    def analyze_all_info(self,content):
        words = self.segmentor.segment(content)
        postags = self.postagger.postag(words)
        recognizer = self.recognizer.recognize(words, postags)
        arcs = self.parser.parse(words, postags)
        print("|".join(words))
        print("|".join(postags))
        print("|".join(recognizer))
        print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))
        return words,postags,recognizer,arcs
my_ltp = MyLTP()
my_ltp.load()
ltp_count = 0

if __name__ == '__main__':
    words = my_ltp.segmentor.segment("原子序数在83（铋）或以上的元素都具有放射性，但某些原子序数小于83的元素（如锝）也具有放射性。")  #分词
    print("|".join(words))
    postags = my_ltp.postagger.postag(words)            #词性标注
    print("|".join(postags))
    recognizer = my_ltp.recognizer.recognize(words,postags)     #实体识别
    print("|".join(recognizer))
    arcs = my_ltp.parser.parse(words,postags)
    print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs)) #句法依存关系
    # import jieba
    # print(ATT_and_VOB_extend(list(jieba.cut('别人借我钱，我起诉后，还不还，该怎么办？？')), ['钱', '起诉']))