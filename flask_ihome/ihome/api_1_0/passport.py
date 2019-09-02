# coding:utf-8

from . import api
from flask import request, jsonify, session
from ihome.utils.response_code import RET
from ihome import redis_store, db, constants
from ihome.models import User
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash

import re
import logging
# 传过来的数据 mobile, sms_code, password, password2
@api.route('/users', methods=['POST'])
def register():
    '''注册
    请求参数：手机号，短信验证码，密码，确认密码
    参数格式：json
    :return: 
    '''
    # 获取请求的json数据，返回字典
    req_dict = request.get_json()
    mobile =req_dict.get('mobile')
    sms_code = req_dict.get('sms_code')
    password = req_dict.get('password')
    password2 = req_dict.get('password2')

    # 校验参数
    if not all([mobile, sms_code, password, password2]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

    # 判断手机格式,匹配正确返回匹配对象
    if not re.match(r'1[35678]\d{9}', mobile):
        # 匹配失败，表示数据格式不正确
        return jsonify(errno=RET.PARAMERR, errmsg='手机格式错误')

    # 判两次密码是否相同
    if password != password2:
        return jsonify(errno=RET.PARAMERR, errmsg='两次密码不一致')

    # 业务处理：
    # 从redis中取出短信验证码
    try:
        # 按格式取出短信验证码
       real_sms_code = redis_store.get('sms_code_%s' % mobile)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='读取真实短信验证码异常')

    # 判断短信验证码是否过期
    if real_sms_code is None:
        return jsonify(errno=RET.DBERR, errmsg='短信验证码已失效')

    # # todo:成功取出验证码后删除redis中的验证码信息,用户输入错误后不能重复利用
    # try:
    #     redis_store.delete('sms_code_%s' % mobile)
    # except Exception as e:
    #     logging.error(e)

    # 判断短信验证码的正确性
    if real_sms_code != sms_code:
        return jsonify(errno=RET.DBERR, errmsg='短信验证码不正确')

    # todo:验证成功后删除redis中的验证码信息,用户输入错误可以重复利用
    try:
        redis_store.delete('sms_code_%s' % mobile)
    except Exception as e:
        logging.error(e)


    # 注册时的密码处理：在密码后面加上一个随机的 '盐值',这样两个相同明文密码保存的密文就不相同了，
    # 用户1   password='123456'+ 'abc'    sha1加密或者sha256     abc$dajwjlkej
    # 用户2   password='123456'+ 'efg'    sha1加密或者sha256     efg$asdasfgwq

    # 判断用户的手机号是否注册过
    # 保存用户的注册信息到数据库中
    # todo:由于我们设置的表中mobile是唯一字段，不能重复，添加数据不成功表示已存在，反之表示不存在，可以添加，这样可以减少数据库查询次数
    user = User(name=mobile, mobile=mobile)
    # 设置属性，设置密码，加密方式在模型类中完成
    user.password =password
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        # 表示手机号出现重复，报唯一键重复的错误，
        logging.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DATAEXIST, errmsg='手机号已注册')
    except Exception as e:
        # 其他错误，比如连接出错
        logging.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='查询数据库出错')

    # 保存用户的登录状态
    session['name'] = user.name
    session['mobile'] = mobile
    session['user_id'] = user.id
    # 返回结果
    return jsonify(errno=RET.OK, errmsg='注册成功')


# 前端传过来的数据：mobile、password
@api.route('/login', methods=["POST"])
def login():
    '''登录
    请求参数：mobile、password
    参数格式：json
    :return: 
    '''
    # 获取数据
    req_dict = request.get_json()
    mobile = req_dict.get('mobile')
    password = req_dict.get('password')

    # 校验参数的完整性
    if not all([mobile,password]):
        return jsonify(errno=RET.PARAMERR,errmsg='参数不完整')

    # 手机号的格式
    if not re.match(r"1[34578]\d{9}", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机号格式错误")

    # 判断错误次数是否超过限制，如果超过限制，则返回
    # redis记录： "access_nums_请求的ip": "次数"
    user_ip = request.remote_addr  # 获取用户的ip地址
    try:
        access_nums = redis_store.get("access_num_%s" % user_ip)
    except Exception as e:
        logging.error(e)
    else:
        if access_nums is not None and int(access_nums) >=constants.LOGIN_ERROR_MAX_TIMES:
            return jsonify(errno=RET.REQERR, errmsg="错误次数过多，请稍后重试")

    # 查询数据库中是否存在该账号
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取用户信息失败")


    # 使用数据库封装的函数检查用户的密码
    if user is None or not user.check_password(password):
        # 如果验证失败，记录错误次数，返回信息
        try:
            # redis的incr可以对字符串类型的数字数据进行加一操作，如果数据一开始不存在，则会初始化为1
            redis_store.incr("access_num_%s" % user_ip)
            redis_store.expire("access_num_%s" % user_ip,constants.LOGIN_ERROR_FORBID_TIME)
        except Exception as e:
            logging.error(e)

        # 用户名或者密码不正确
        return jsonify(errno=RET.PWDERR,errmsg='用户名或密码不正确')

    # 如果验证成功，保存用户的登录状态在session中
    session['name']=user.name
    session['mobile']=user.mobile
    session['user_id']=user.id

    return jsonify(errno=RET.OK,errmsg='登录成功')

@api.route('/check_login',methods=['GET'])
def check_login():
    """检查登陆状态"""
    # 尝试从session中获取用户的名字
    name = session.get("name")
    # 如果session中数据name名字存在，则表示用户已登录，否则未登录
    if name is not None:
        return jsonify(errno=RET.OK, errmsg="true", data={"name": name})
    else:
        return jsonify(errno=RET.SESSIONERR, errmsg="false")

@api.route("/logout", methods=["DELETE"])
def logout():
    """登出"""
    # 清除session数据
    # 后来添加的，获取csrf_token值
    csrf_token = session.get("csrf_token")
    session.clear()
    # 设置session中的csrf_token在redis中
    session["csrf_token"] = csrf_token
    return jsonify(errno=RET.OK, errmsg="OK")

