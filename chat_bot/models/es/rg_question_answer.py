#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/22
# @Author  : JiaoJianglong



from models.connect.es import ES
import collections


class RGQuestionAnswer(ES):
    _index = "rg_question_answer"
    _type = "doc"
    index_mapping = {
  "settings": {
    "number_of_shards": 2,
    "number_of_replicas": 1,
    "analysis": {
      "filter": {
        "my_stopwords": {
          "type": "stop",
          "stopwords_path": "stopwords-es2.txt"}},
      "analyzer": {
        "my_analyzer": { "type": "custom","char_filter": [ "html_strip"],"tokenizer": "ik_max_word"},
        "smart_analyzer": { "type": "custom","char_filter": [ "html_strip"],"tokenizer": "ik_smart"}},
    },
  },
  "mappings": {
    "doc": {
      "properties": {
        "answers": {
          "type": "nested",
          "properties": {
            "emotion": {
              "type": "integer"
            },
            "answer": {
              "type": "string",
              "index":"not_analyzed"
            },
            "picture": {
              "type": "string",
              "index": "not_analyzed"
            },
          }
        },
        "check_state": {
          "type": "integer"
        },
        "id": {
          "type": "string",
          "index": "not_analyzed",
        },
        "update_time": {
          "type": "long"
        },
        "title": {
          "analyzer": "my_analyzer",
          "type": "string"
        },
      }
    }
  }
}

    emotion_dict = collections.OrderedDict()
    emotion_dict[2] = "很好"
    emotion_dict[1] = "较好"
    emotion_dict[0] = "一般"
    emotion_dict[-1] = "较差"
    emotion_dict[-2] = "很差"



if __name__ == "__main__":
    RGQuestionAnswer().create_index()
    #RGQuestionAnswer().delete_index()
