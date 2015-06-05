#!/usr/bin/env python
#-*-coding:utf-8-*-

__author__ = 'akic'

from flaskr import app
import os

#解决字符编码问题
import sys
reload(sys)
sys.setdefaultencoding('utf8')

app.config.update(dict(
    DATABASE = os.path.join(app.root_path,'flaskr.db'),
    DEBUG = True,
    SECRET_KEY = 'akfkjkhggjuuwnbg',
    #防止跨站点请求伪造攻击
    CSRF_ENABLED = True,
    USERNAME = 'admin',
    PASSWORD = 'admin'
))