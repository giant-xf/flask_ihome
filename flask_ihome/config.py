# coding:utf-8

import redis

class Config(object):
    '''flask配置信息'''

    # 秘钥(csrf、session)
    SECRET_KEY = "XHSOI*Y9dfs9cshd9"

    # 数据库连接配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@192.168.43.150/flask_ihome'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # redis配置信息
    REDIS_HOST='192.168.43.150'
    REDIS_PORT=6379

    # flask_session配置
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT)
    SESSION_USE_SIGNER = True   # 对cookie中的session_id进行加密混淆
    PERMANENT_SESSION_LIFETIME = 86400  # session数据有效期，单位秒

class DevelopmentConfig(Config):
    '''开发模式的配置信息'''
    DEBUG = True

class ProductionConfig(Config):
    '''生产环境配置信息'''
    pass


config_map = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig
}


