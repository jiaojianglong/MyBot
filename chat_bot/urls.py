#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/22
# @Author  : JiaoJianglong

from handlers.simple_qa import SimpleQAHandler
from handlers.bot_manage.qa_data import QADataHandler,QADataDetailHandler
from handlers.bot_manage.answer_info import AnswerInfoHandler,AnswerInfoDetailHandler
from handlers.bot_manage.question_info import QuestionInfoHandler,QuestionInfoDetailHandler

handler = [
    (r'/api/simple_qa',SimpleQAHandler),
    (r'/api/qa_data',QADataHandler),
    (r'/api/qa_data_detail',QADataDetailHandler),
    (r'/api/answer_info',AnswerInfoHandler),
    (r'/api/answer_detail_info',AnswerInfoDetailHandler),
    (r'/api/question_info',QuestionInfoHandler),
    (r'/api/question_detail_info',QuestionInfoDetailHandler),
]