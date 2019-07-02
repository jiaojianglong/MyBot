#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/20
# @Author  : JiaoJianglong
from tornado.web import RequestHandler
from handlers.base import decorator
from handlers.base import exceptions
from common_qa import processor

class BaseHandler(RequestHandler):
    """
    基础接口模块
    """
    exception = exceptions
    decorator = decorator
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def init_parameter(self):
        """初始化返回参数"""
        result = {'code': 200, 'msg': '返回成功','data':{}}
        return result

    def initialize(self, **kwargs):
        """作为URL规范的第三个参数会作为关键词参数传给该方法"""
        pass

    def on_connection_close(self):
        """客户端关闭连接后调用，清理和长连接相关的资源"""
        pass

    def set_default_headers(self):
        """在请求开始时设置请求头部"""
        pass

    @decorator.threadpool_decorator
    def options(self, *args, **kwargs):
        result = self.init_parameter()
        print("接收到options请求")
        return result


class QABaseHandler(BaseHandler):
    process = processor

    def process_flow(self,process_list):
        process_instance = None
        for i in range(len(process_list)):
            process_instance = process_list[-i-1](process_instance)
        return process_instance






