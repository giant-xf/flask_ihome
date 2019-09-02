# coding: utf-8


from celery import Celery
# from ihome.tasks import config

# 定义celery对象
celery_app = Celery('ihome')

# 引用配置信息
celery_app.config_from_object('ihome.tasks.config')

# 自动搜索异步任务,指明到包目录就行了
celery_app.autodiscover_tasks(['ihome.tasks.sms'])

# 启动celery -A ihome.tasks.main worker -l info