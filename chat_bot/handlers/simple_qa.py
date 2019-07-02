#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/22
# @Author  : JiaoJianglong


from handlers.base.basehandler import QABaseHandler

from models.es.rg_search_question import RGSearchQuestion
from models.es.rg_question_answer import RGQuestionAnswer

class SimpleQAHandler(QABaseHandler):

    question_model = RGSearchQuestion()
    answer_model = RGQuestionAnswer()

    @QABaseHandler.decorator.threadpool_decorator
    def post(self, *args, **kwargs):
        result = self.init_parameter()
        content = self.get_argument("content")

        parameter = {"content":content}

        process_list = [
            self.process.QuestionSearchProcessor,#问题检索
        ]
        process_instance = self.process_flow(process_list)
        result_parameter = process_instance.handle(parameter)
        result = result_parameter.get("result")
        return result


