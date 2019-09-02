# coding:utf-8

from flask import current_app,jsonify,make_response,request
from . import api
from ihome.utils.captcha.captcha import captcha
from ihome.utils.response_code import RET
from ihome import redis_store,constants,db
from ihome.models import User
from ihome.libs.yuntongxun.sms import CCP
from ihome.tasks.sms.tasks import send_sms

import logging
import random
# GET  127.0.0.1:5000/api/v1.0/image_codes/<image_code_id>

@api.route('/image_codes/<image_code_id>')
def get_image_code(image_code_id):
    '''
    获取图片验证码
    :param image_code_id: 图片验证码编号
    :return: 正常:图片验证码    异常:json
    '''
    # 业务逻辑处理：生成验证码图片
    # 名字，真实文本，图片数据
    name, text, image_data = captcha.generate_captcha()

    # 将验证码真实值与编号保存到redis中，设置有效期
    # redis:字符串，列表，哈希，set，zset
    # 使用哈希维护的时候有效期只能整体是指
    # 单条维护记录，选用字符串
    # 'image_code_编号id':'真实值'
    # redis_store.set('image_code_%s' % image_code_id, text)
    # redis_store.expire('image_code_%s' % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES)    # 单位秒
    #  参数：记录名字 ， 有效期， 记录文本值
    try:
        redis_store.setex('image_code_%s' % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        # 记录日志信息
        logging.error(e)
        return jsonify(errno=RET.DBERROR, errsg='保存验证码失败')


    # 返回图片
    resp = make_response(image_data)
    resp.headers['Content-Type'] = 'image/jpg'
    return resp

#GET  127.0.0.1:5000/api/v1.0/sms_codes/<mobile>?image_code=xx&image_code_id=xx
@api.route("/sms_codes/<re(r'1[35678]\d{9}'):mobile>")
def get_sms_code(mobile):
    '''
    获取短信验证码
    :param mobile: 用户输入的手机号
    :return: 
    '''
    # 获取参数
    image_code = request.args.get('image_code')
    image_code_id = request.args.get(('image_code_id'))
    # 校验参数
    if not all([image_code,image_code_id]):
        return jsonify(errno=RET.PARAMERR,errmsg='参数不完整')

    # 业务逻辑：发送验证码
    # 从redis中取出真实的图片验证码
    try:
        real_image_code = redis_store.get('image_code_%s' % image_code_id)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DATAERR,errmsg='redis数据库异常')

    # 判断图片验证码是否过期,取出来的是None表示过期
    if real_image_code is None:
        return jsonify(errno=RET.NODATA,errmsg='图片验证码过期')

    # todo:删除redis中image_code的值，防止用户用一张图片验证码多次验证
    try:
        redis_store.delete('image_code_%s' % image_code_id)
    except Exception as e:
        logging.error(e)

    # 与用户输入的值进行对比
    if image_code.lower() != real_image_code.lower():
        # 表示用户填写错误
        return jsonify(errno=RET.DATAERR,errmsg='图片验证码输入错误')

    # todo: 在用户图片验证码校验完成后，我们进行redis数据库中的查询手机号在60s是否发送过操作短信，查询手机号的记录
    try:
        send_flag = redis_store.get('send_sms_code_%s' % mobile)
    except Exception as e:
        logging.error(e)
    else:
        if send_flag is not None:
            # 表示在60s内有操作过
            return jsonify(errno=RET.REQERR,errmsg='请求过于频繁,请60秒后重试')

    # 判断输入的手机是否已经注册
    # 连接可能出错，放在try中
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        logging.error(e)
    else:
        # 手机号已经注册
        if user is not None:
            return jsonify(errno=RET.DATAEXIST,errmsg='手机号已注册')

    # todo: 如果用户未注册，则生成短信验证码
    sms_code = '%06d' % random.randint(0,999999)

    # 保存真实的短信验证码
    try:
        redis_store.setex('sms_code_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # todo: 保存发送短信了的这个手机号的记录，防止用户在60s内再次发送短信的操作
        redis_store.setex('send_sms_code_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR,errmsg='验证码保存失败')

    # todo：普通发送短信的方式
    #发送短信
    # try:
    #     ccp = CCP()
    #     result = ccp.send_template_sms(mobile, [sms_code,int(constants.SMS_CODE_REDIS_EXPIRES/60)],1)
    # except Exception as e:
    #     logging.error(e)
    #     return jsonify(errno=RET.THIRDERR, errmsg='发送发送异常')
    #
    # if result==0:
    #     # 发送成功
    #     return jsonify(errno=RET.OK,errmsg='发送成功')
    # else:
    #     # 发送失败
    #     return jsonify(errno=RET.THIRDERR, errmsg='发送失败')

    # todo: 使用celery发送短信方式
    result = send_sms.delay(mobile, [sms_code,int(constants.SMS_CODE_REDIS_EXPIRES/60)],1)
    # 返回异步结果对象的编号
    print (result.id)
    # 通过get能获取celery异步执行的结果
    # get方法默认是阻塞行为，会等到有结果的再返回
    # get也能接收超时时间timeout，超过时间，还没有拿到返回结果自动返回
    ret = result.get()
    print (ret)


    # 发送成功
    return jsonify(errno=RET.OK,errmsg='发送成功')

