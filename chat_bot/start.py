#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/22
# @Author  : JiaoJianglong


import tornado.ioloop
import tornado.web
from urls import handler
import tornado.httpserver

application = tornado.web.Application(handler, debug=False)

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.bind(8887)
    http_server.start()
    tornado.ioloop.IOLoop.current().start()
