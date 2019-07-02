#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/27
# @Author  : JiaoJianglong


from handlers.base.basehandler import BaseHandler
from models.es.rg_search_question import RGSearchQuestion
from tools.utils import md5


class QuestionInfoHandler(BaseHandler):

    question_model = RGSearchQuestion()

    @BaseHandler.decorator.threadpool_decorator
    def get(self):
        """
        检索获取问题列表
        :return:
        """
        pass

class QuestionInfoDetailHandler(BaseHandler):
    question_model = RGSearchQuestion()

    @BaseHandler.decorator.threadpool_decorator
    def get(self, *args, **kwargs):
        """
        获取问题详细信息
        :param args:
        :param kwargs:
        :return:
        """
        result = self.init_parameter()
        question_id = self.get_argument("question_id")
        res = self.question_model.get(question_id).get("_source")
        result['data'] = res
        return result

    @BaseHandler.decorator.threadpool_decorator
    def post(self, *args, **kwargs):
        """
        新建问题信息
        :param args:
        :param kwargs:
        :return:
        """
        question = self.get_argument("question")
        similar_question = self.get_argument("similar_question","")
        answer_id = self.get_argument("answer_id")
        question_id = md5(question)
        question_info = {"title":question,"id":question_id,"answer_id":answer_id}
        if similar_question:
            similar_questions = similar_question.split("\n")
            question_info.update({"similar_titles":similar_questions})
        self.question_model.index(question_info,question_id)
        return "success"

    @BaseHandler.decorator.threadpool_decorator
    def put(self, *args, **kwargs):
        """
        修改问题信息
        :param args:
        :param kwargs:
        :return:
        """
        question = self.get_argument("title")
        similar_question = self.get_argument("similar_questions", "")
        answer_id = self.get_argument("answer_id")
        question_id = self.get_argument("id")
        new_question_id = md5(question)
        question_info = {"title": question, "id": new_question_id, "answer_id": answer_id}
        if similar_question:
            similar_questions = similar_question.split("\n")
            question_info.update({"similar_titles": similar_questions})
        self.question_model.index(question_info, new_question_id)
        if question_id!=new_question_id:
            self.question_model.delete(question_id)
        return "success"
