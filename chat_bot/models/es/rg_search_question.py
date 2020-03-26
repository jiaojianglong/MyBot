#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/22
# @Author  : JiaoJianglong



from models.connect.es import ES


class RGSearchQuestion(ES):
    _index = "rg_search_question"
    _type = "_doc"
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
        "pinyin_analyzer": { "type": "custom","tokenizer": "my_pinyin"},
        "smart_analyzer": { "type": "custom","char_filter": [ "html_strip"],"tokenizer": "ik_smart"}},
      "tokenizer": {
        "my_pinyin": { "lowercase": "true","keep_original": "false","remove_duplicated_term": "false","keep_separate_first_letter": "false","type": "pinyin","limit_first_letter_length": "16","keep_full_pinyin": "true"}}},

  },
  "mappings": {
    "doc": {
      "properties": {
        "id": {
          "type": "string",
          "index": "not_analyzed"
        },
        "title": {
          "type": "string",
          "analyzer": "my_analyzer"
        },
        "similar_titles":{
          "type": "string",
          "analyzer": "my_analyzer"
        },
        "answer_id":{
            "type":"string",
            "index": "not_analyzed"
        }
      }
    }
  }
}


    def search_question(self,parameter):
        content = parameter.get("content")
        words_weight = parameter.get("words_weight")

        query_body = {"query":{"bool":{"should":[
            {"match":{"question":content}},
        ]}}}

        if any(words_weight):
            for w_words,w_weight in words_weight:
                query_body['query']['bool']['should'].append(
                    {"match":{"question":{
                        "query": w_words,
                        "boost": w_weight}}}
                )
        print("question_query",query_body)
        res = self.search(query_body,_source=["answer_id","question"])["hits"]["hits"]
        search_result = [{"score":question.get("_score"),
                          "question":question.get("_source").get("question"),
                          "answer_id":question.get("_source").get("answer_id")}for question in res]

        return search_result


        # if res:
        #     answer_id = res[0].get("_source",{}).get("answer_id")
        #     res = self.answer_model.get(answer_id)
        #     answer = res.get("_source",{}).get("answers")
        #     for r in answer:
        #         if r.get("emotion") == 0:
        #             answer = r.get("answer")
        #     result['data'] = {"answer":answer}




if __name__ == "__main__":
    RGSearchQuestion().create_index()#创建索引
    #RGSearchQuestion().delete_index()






