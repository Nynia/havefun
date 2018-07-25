# -*-coding:utf-8-*-
from flask import Flask
from flask_apscheduler import APScheduler
from flask_bootstrap import Bootstrap
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, AnonymousUserMixin
from app.utils.ftp import MyFTP
from app.utils.redis_middle import RedisClient

import logging,sys

bootstrap = Bootstrap()
db = SQLAlchemy()

login_manager = LoginManager()
# 设置成strong将无法自动从cookies登录
# login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

# scheduler = APScheduler()
# init redis
redis_cli = RedisClient()
logger = logging.getLogger()


class MyAnonymousUser(AnonymousUserMixin):
    def __init__(self):
        self.id = id(self)

    def get_id(self):
        return self.id


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    # login_manager.anonymous_user = MyAnonymousUser
    # scheduler.init_app(app)
    # scheduler.start()

    # myftp.login()
    #setup logger
    #logger = logging.getLogger("Main")

    # 指定logger输出格式
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)-8s: %(message)s')

    # 文件日志
    file_handler = logging.FileHandler("havefun.log")
    file_handler.setFormatter(formatter)

    # 控制台日志
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter

    # 为logger添加的日志处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # 指定日志的最低输出级别，默认为WARN级别
    logger.setLevel(logging.INFO)

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
