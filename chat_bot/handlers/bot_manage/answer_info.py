#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/27
# @Author  : JiaoJianglong

import json
from handlers.base.basehandler import BaseHandler
from models.es.rg_question_answer import RGQuestionAnswer

class AnswerInfoHandler(BaseHandler):
    answer_model = RGQuestionAnswer()

    @BaseHandler.decorator.threadpool_decorator
    def get(self, *args, **kwargs):
        """
        搜索返回答案列表
        :param args:
        :param kwargs:
        :return:
        """
        result = self.init_parameter()
        answer_title = self.get_argument("title","")
        if answer_title:
            res = self.answer_model.search({"query":{"match":{"title":answer_title}}},_source=["title","id"])['hits']['hits']
        else:
            res = self.answer_model.search({"query": {"match_all":""}}, _source=["title", "id"])['hits']['hits']
        result['data'] = [{"value":answer.get("_source").get("title"),"id":answer.get("_source").get("id")}for answer in res]
        print(result)
        return result


class AnswerInfoDetailHandler(BaseHandler):
    answer_model = RGQuestionAnswer()

    @BaseHandler.decorator.threadpool_decorator
    def get(self, *args, **kwargs):
        """
        获取答案详细信息
        :param args:
        :param kwargs:
        :return:
        """
        result = self.init_parameter()
        answer_id = self.get_argument("answer_id")
        answer = self.answer_model.get(answer_id).get("_source")
        answers = []
        for emotion_value, emotion in self.answer_model.emotion_dict.items():
            for answer_ in answer.get("answers", []):
                if emotion_value == answer_.get("emotion"):
                    answers.append(
                        {"answer": answer_.get("answer"), "emotion": emotion, "emotion_value": emotion_value})
                    break
            else:
                answers.append({"answer": "", "emotion": emotion, "emotion_value": emotion_value})
        answer["answers"] = answers
        result['data'] = answer
        return result


    @BaseHandler.decorator.threadpool_decorator
    def put(self):
        """
        修改答案数据
        :return:
        """
        answer_info = json.loads(self.request.body.decode())
        answers = answer_info.get("answers")
        answer_list = []
        for answer in answers:
            answer_list.append({"answer":answer.get("answer"),"emotion":answer.get("emotion_value")})
        answer_info['answers'] = answer_list
        self.answer_model.index(answer_info,answer_info.get("id"))
        return "success"