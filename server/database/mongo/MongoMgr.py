# coding=utf-8

__author__ = 'guanjian'

import settings
from pymongo import MongoClient

# HOST = settings.m_host
# PORT = settings.m_port
# HOST2 = settings.m_host2
# PORT2 = settings.m_port2
# USER = settings.m_user
# PASS = settings.m_pass
# DB = settings.m_db
#
# # 连接RichFun线上库
# uri = 'mongodb://%s:%s@%s:%s,%s:%s/%s?readPreference=nearest' % (USER, PASS, HOST, PORT, HOST2, PORT2, DB)
#
# client = MongoClient(uri)
# db = client[DB]

# 连接richfun 管理数据库
# mghost = "10.18.101.3",mgdatabase
# mgport = 27027,
# mguser = "shaoge",
# mgpassword = "123456",
# mgdatabase = "activities",

_robot_client = MongoClient(settings.MONGO_URI)
_robot_db = _robot_client[settings.MONGO_DB]

def get_mongo():
    return  _robot_db
