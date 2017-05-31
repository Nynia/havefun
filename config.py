import os
basedir = os.path.abspath(os.path.dirname(__file__))

STATIC_URL_PREFIX = 'http://221.228.17.87/res/'
ORDER_REQUEST_URL = 'http://61.160.185.51:9250/ismp/serviceOrder'
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'skks'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    #task
    JOBS = [
        {
            'id': 'job1',
            'func': 'app.tasks:job1',
            'args': (1, 2),
            'trigger': 'cron',
            'hour': '17',
            'minute': '23',
            'second': '1'
        }
    ]
    SCHEDULER_API_ENABLED = True

    @staticmethod
    def init_app(app):
        pass

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:admin@127.0.0.1/havefun'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:admin@192.168.114.139/havefun'

config = {
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default':Pro
}
