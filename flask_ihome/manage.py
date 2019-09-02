# coding:utf-8


from ihome import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import logging
from flask import current_app

# 利用工厂创建flask对象
app = create_app('develop')

# 创建manage管理对象
manager = Manager(app)

Migrate(app, db)
manager.add_command('db',MigrateCommand)


if __name__ == '__main__':
    # logging.error('error msg')  # 错误级别
    # logging.warn('warn msg')    # 警告级别
    # logging.info('info msg')    # 消息提示
    # logging.debug('debug msg')  # 调试级别

    # current_app.logger.error('error msg')
    # current_app.logger.warn('warn msg')
    # current_app.logger.info('info msg')
    # current_app.logger.debug('debug msg')

    print (app.url_map)
    # print (app.config)
    manager.run()


