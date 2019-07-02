#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/22
# @Author  : JiaoJianglong

import os
from tornado.options import options


_root = BASE_DIR = os.path.dirname(__file__)
_data_path = os.path.join(os.path.dirname(_root),"data")
try:
    DEBUG = options.debug
except:
    DEBUG = True


ES_DB = dict(
        HOSTS=["http://127.0.0.1:9200"],
        # HTTP_AUTH=("aegis","shield"),
        TIMEOUT=60,
        TYPE="es",
        MAXSIZE=40,
    )

MONGO_DB = dict(
    HOST="127.0.0.1",
    PORT=8975,
    DB="admin",
    USERNAME="admin",
    PASSWORD="root",
    )