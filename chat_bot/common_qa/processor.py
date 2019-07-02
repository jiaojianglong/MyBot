#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/19
# @Author  : JiaoJianglong

import re
import logging
import random
from abc import abstractmethod, ABCMeta
from common_qa.analyze.tfidf import my_tfidf_model
from models.es.rg_search_question import RGSearchQuestion
from common_qa.analyze.question_match import question_match
from models.es.rg_question_answer import RGQuestionAnswer

class Processor(metaclass=ABCMeta):
    """
    问答处理流程父类，子类负责处理各个功能，组成不同的模块，执行顺序在handle中指定
    """

    def __init__(self, parent=None):
        self.parent = parent

    @abstractmethod
    def handle(self,parameter):
        pass


class QuestionSearchProcessor(Processor):
    """
    问题匹配
    """
    question_model = RGSearchQuestion()
    answer_model = RGQuestionAnswer()
    def handle(self,parameter):
        parameter["words_weight"] = my_tfidf_model.get_weight_tfidf(parameter.get("content"))
        result = self.question_model.search_question(parameter)
        match_question = question_match(result,parameter['content'])
        print(result)
        print("匹配到问题：",match_question)
        answer_id = match_question.get("answer_id")
        res = self.answer_model.get(answer_id)
        answer = res.get("_source",{}).get("answers")
        for r in answer:
            if r.get("emotion") == 0:
                answer = r.get("answer")
        result = {}
        result['data'] = {"answer":answer}
        parameter['result'] = result
        if self.parent:
            return self.parent.handle(parameter)
        else:
            return parameter



