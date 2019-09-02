# coding:utf-8

from werkzeug.routing import BaseConverter
from flask import session, jsonify, g
from ihome.utils.response_code import RET

import functools
# 定义正则转换器
class ReConverter(BaseConverter):
    '''万能正则转换器'''
    def __init__(self, url_map, regex):
        # 调用父类的初始化方法
        super(ReConverter, self).__init__(url_map)
        # 保存正则表达式
        self.regex = regex

# 定义登录校验装饰器
def login_required(view_func):

    # 加入这个装饰器可以保证原来被装饰的函数的属性不变
    # eg: print(login.__name__),print(login.__doc__)
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        # 判断用户的登录状态
        user_id = session.get('user_id')

        # 如果用户是登录，执行视图函数
        if user_id is not None:
            # 将user_id保存到g对象中，在视图函数中可以直接通过g对象获取保存的数据，
            # 可以减少redis数据库查询
            g.user_id = user_id
            return view_func(*args,**kwargs)
        else:
            # 如果用户未登录
            return jsonify(errno=RET.SESSIONERR, errmsg='用户未登录')
    return wrapper




