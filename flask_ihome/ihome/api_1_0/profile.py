# coding:utf-8

from . import api
from flask import g, jsonify, request, session
from ihome.utils.commons import login_required
from ihome.utils.response_code import RET
from ihome.utils.image_storage import storage
from ihome.models import User
from ihome import constants
from ihome import db

import logging

@api.route('/users/avatar', methods=["POST"])
@login_required
def set_user_avatar():
    '''设置用户头像
    参数：图片(多媒体表单格式， 用户id(user_id)    
    '''
    # 获取参数
    # 装饰器中已经将user_id保存在g对象中，所以视图中可以直接读取
    user_id = g.user_id
    # 获取图片对象
    image_file = request.files.get('avatar')

    if image_file is None:
        return jsonify(errno=RET.PARAMERR, errmsg='未上传图片')
    # 读取图片对象数据,二进制图片数据
    image_data = image_file.read()
    try:
        # 上传图片到七牛，获取图片的名字
        file_name = storage(image_data)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg='上传图片失败')

    try:
        # 将文件名保存到数据库中的avatar_url中
        User.query.filter_by(id=user_id).update({'avatar_url':file_name})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return jsonify(errno=RET.DBERR,errmsg='保存图片信息失败')

    # 保存图片信息成功
    # 拼接出地址
    avatar_url = constants.QINIU_URL_DOMAIN + file_name
    return jsonify(errno=RET.OK, errmsg='保存成功', data={'avatar_url':avatar_url})


@api.route('/users/name', methods=['PUT'])
@login_required
def change_user_name():
    '''修改用户名'''
    # 获取数据
    user_id = g.user_id
    # 将json格式转换成字典
    req_data = request.get_json()

    if not req_data:
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

    # 获取用户想要设置的name
    name = req_data.get('name')

    # name不能为空
    if name is None:
        return jsonify(errno=RET.NODATA, errmsg='数据出错')

    try:
        # 获取用户，保存用户name
        User.query.filter_by(id=user_id).update({'name':name})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存用户名失败')

    # 修改session中的name字段
    session['name'] = name

    return jsonify(errno=RET.OK, errmsg='保存成功')

@api.route('/users', methods=['GET'])
@login_required
def get_user_profile():
    '''获取用户的用户名和手机号'''
    # 获取数据
    user_id = g.user_id
    # 查询数据库中信息
    try:
        user = User.query.get(user_id)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='获取用户信息失败')

    if user is None:
        return jsonify(errno=RET.NODATA, errmsg='无效操作')
    return jsonify(errno=RET.OK, errmsg='OK', data=user.to_dict())


@api.route("/users/auth", methods=["GET"])
@login_required
def get_user_auth():
    '''获取实名认证信息'''
    # 获取数据
    user_id = g.user_id
    # 查询数据库中用户信息
    try:
        user = User.query.get(user_id)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='获取用户信息失败')

    if user is None:
        return jsonify(errno=RET.NODATA, errmsg='无效操作')

    return jsonify(errno=RET.OK, errmsg="OK", data=user.auth_to_dict())


@api.route('/users/auth', methods=['POST'])
@login_required
def set_user_auth():
    '''修改实名认证信息'''
    # 获取数据
    user_id = g.user_id
    req_data = request.get_json()

    if req_data is None:
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

    real_name = req_data.get('real_name')
    id_card = req_data.get('id_card')
    print real_name+':'+id_card
    # real_name 和 id_card 不能为空
    if not all([real_name, id_card]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 更新实名信息
    try:
        User.query.filter_by(id=user_id, real_name=None, id_card=None).update({'real_name': real_name,'id_card':id_card})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存用户实名信息失败')

    return jsonify(errno=RET.OK, errmsg='更新成功')














