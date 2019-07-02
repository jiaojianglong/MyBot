#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/14
# @Author  : JiaoJianglong

import jieba

from models.connect.mongodb import MongoDB
from tools.utils import Singleton
from handlers.base.decorator import preload
from settings import _root

class Entity(MongoDB,metaclass=Singleton):
    _field = ["实体","近义词","反义词","实体类型"]
    name = "x_qa.entity"
    def __init__(self):
        super(Entity,self).__init__()
        self.entities = self.get_entity()
        self.my_jieba = self.get_myjieba()

    def get_myjieba(self):
        my_jieba = jieba
        for entity in self.entities:
            my_jieba.add_word(entity)
        return my_jieba

    def get_entity(self):
        with open(_root+"/source/words.txt","r",encoding="utf8") as af:
            entities = [words.strip() for words in af]
        return entities


    def get_content_entity(self,content):
        c_words = self.my_jieba.cut(content)
        c_entity = [entity for entity in c_words if entity in self.entities]
        return c_entity



