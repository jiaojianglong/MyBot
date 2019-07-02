#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/22
# @Author  : JiaoJianglong

import time
from elasticsearch import helpers
from models.connect.es import es_conn
from models.es.rg_question_answer import RGQuestionAnswer
from models.es.rg_search_question import RGSearchQuestion
from settings import _root
import hashlib


question_model = RGSearchQuestion()
answer_model = RGQuestionAnswer()


def md5(mingwen):
    m = hashlib.md5()
    mdr_str = mingwen.encode()
    m.update(mdr_str)
    ciphertext = m.hexdigest()
    return ciphertext

def loda_qa_data():
    with open(_root+"/source/qa_data.txt","r",encoding="utf8") as af:
        qas = af.read().split("\n\n")

    answer_list = []
    question_list = []

    for qa in qas:
        try:
            question = qa.split("\n")[0]
            answer = qa.split("\n")[1]
            answer_id = md5(answer)
            question_id = md5(question)

            answer_data = {
                '_index': 'rg_question_answer',
                '_type': 'doc',
                '_id': answer_id,
                '_source': {"id":answer_id,"answers":[{"emotion":0,"answer":answer}],"check_state":0,"update_time":time.time(),"title":question}
            }
            answer_list.append(answer_data)

            question_data = {
                '_index': 'rg_search_question',
                '_type': 'doc',
                '_id': question_id,
                '_source': {"id":question_id,"answer_id":answer_id,"title":question}
            }
            question_list.append(question_data)
        except:
            pass

    for i in range(10000):
        answer_data = answer_list[i*10000:(i+1)*10000]
        print(len(answer_data))
        helpers.bulk(es_conn,answer_data)
        question_data = question_list[i * 10000:(i + 1) * 10000]
        print(len(question_data))
        helpers.bulk(es_conn, question_data)
        if len(question_data) == 0:
            break

if __name__ == "__main__":
    loda_qa_data()





