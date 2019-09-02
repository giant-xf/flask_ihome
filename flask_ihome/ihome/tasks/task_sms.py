# coding: utf-8

from celery import Celery
from ihome.libs.yuntongxun.sms import CCP

# 定义celery对象
celery_app = Celery('ihome', broker='redis://192.168.43.150/1')


@celery_app.task
def send_sms(to, datas, temp_id):
    '''发送短信的异步任务'''
    ccp = CCP()
    ccp.send_template_sms(to, datas, temp_id)

#celery命令开启：
# celery -A ihome.tasks.task_sms worker -l info


