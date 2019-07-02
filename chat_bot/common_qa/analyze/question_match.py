#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/14
# @Author  : JiaoJianglong

import jieba

from models.mongodb.entity import Entity

entity = Entity()
def question_match(results,content):
    """
    实体相同就判断为相同
    :param results:
    :param content:
    :return:
    """
    match_question = {}
    content_e = entity.get_content_entity(content)
    print("content实体：",content_e)
    for result in results:
        result_e = entity.get_content_entity(result.get("title"))
        print("result实体：", result_e)
        if set(content_e) == set(result_e):
            match_question = result
            break
    return match_question





if __name__ == "__main__":
    question_match([{"title":"申请撤销遗嘱公证需要提供哪些材料"},
                    {"title":"申办遗嘱公证需要那些材料？"},
                    {"title":"办理遗嘱公证需要提交哪些材料？"}
                    ],"办理遗嘱公证需要带的材料有哪些？")





