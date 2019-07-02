#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/25
# @Author  : JiaoJianglong


from handlers.base.basehandler import BaseHandler
from models.es.rg_question_answer import RGQuestionAnswer
from models.es.rg_search_question import RGSearchQuestion
from tools.utils import md5
import time


class QADataHandler(BaseHandler):
    question_model = RGSearchQuestion()
    answer_model = RGQuestionAnswer()
    @BaseHandler.decorator.threadpool_decorator
    def post(self, *args, **kwargs):
        """
        分页，返回问答数据
        :param args:
        :param kwargs:
        :return:
        """
        print("接收到请求")
        result = self.init_parameter()
        page = self.get_argument("page",0)
        content = self.get_argument("content","")
        if content:
            res = self.question_model.search({"query":{"match":{"title":content}}},page=page)['hits']['hits']
        else:
            res = self.question_model.search({"query": {"match_all": {}}}, page=page)['hits']['hits']
        res = [r.get("_source") for r in res]
        for i in res:
            try:
                i["answers"] = self.answer_model.get(i.get("answer_id"))["_source"].get("answers")
            except:
                i["answers"] = []
        result['data'] = res
        return result


class QADataDetailHandler(BaseHandler):
    question_model = RGSearchQuestion()
    answer_model = RGQuestionAnswer()

    @BaseHandler.decorator.threadpool_decorator
    def get(self, *args, **kwargs):
        """
        获取单个问答数据
        :param args:
        :param kwargs:
        :return:
        """
        result = self.init_parameter()
        question_id = self.get_argument("question_id")
        question = self.question_model.get(question_id).get("_source")
        answer = self.answer_model.get(question.get("answer_id","")).get("_source")
        answers = []
        for emotion_value,emotion in self.answer_model.emotion_dict.items():
            for answer_ in answer.get("answers",[]):
                if emotion_value == answer_.get("emotion"):
                    answers.append({"answer":answer_.get("answer"),"emotion":emotion,"emotion_value":emotion_value})
                    break
            else:
                answers.append({"answer":"","emotion":emotion,"emotion_value":emotion_value})
        answer["answers"] = answers
        result["data"] = {"question":question,"answer":answer}
        return result

    @BaseHandler.decorator.threadpool_decorator
    def post(self, *args, **kwargs):
        """
        添加问题答案
        :param args:
        :param kwargs:
        :return:
        """
        try:
            question = self.get_argument("question")
            answer = self.get_argument("answer")
            answer_id = md5(answer)
            question_id = md5(question)
            self.answer_model.index({"id":answer_id,"answers":[answer],"check_state":0,"update_time":time.time(),"title":question},answer_id)
            self.question_model.index({"id":question_id,"answer_id":answer_id,"title":question},question_id)
            return "success"
        except:
            return "field"


    @BaseHandler.decorator.threadpool_decorator
    def delete(self, *args, **kwargs):
        """
        删除问题答案
        :param args:
        :param kwargs:
        :return:
        """
        try:
            question_id = self.get_argument("question_id")
            answer_id = self.get_argument("answer_id")
            self.question_model.delete(question_id)
            self.answer_model.delete(answer_id)
            return "success"
        except:
            return "field"

    @BaseHandler.decorator.threadpool_decorator
    def put(self, *args, **kwargs):
        """
        修改问题答案
        :param args:
        :param kwargs:
        :return:
        """
        pass


